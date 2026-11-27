use std::collections::HashMap;
use std::path::{Path, PathBuf};
use std::sync::Arc;

use reqwest::header::{ETAG, IF_NONE_MATCH};
use serde_json::Value;
use sha2::{Digest, Sha256};
use thiserror::Error;
use tokio::sync::RwLock;

#[derive(Debug, Error)]
pub enum StoreError {
    #[error("knowledge artifact not found: {0}")]
    NotFound(String),
    #[error("failed reading local artifact {path}: {source}")]
    Io {
        path: String,
        #[source]
        source: std::io::Error,
    },
    #[error("failed fetching remote artifact {url}: {source}")]
    Http {
        url: String,
        #[source]
        source: reqwest::Error,
    },
    #[error("unexpected HTTP status {status} fetching {url}")]
    HttpStatus { url: String, status: u16 },
    #[error("invalid JSON in {path}: {source}")]
    Json {
        path: String,
        #[source]
        source: serde_json::Error,
    },
}

#[derive(Debug, Clone)]
pub struct StoreConfig {
    pub data_dir: Option<PathBuf>,
    pub base_url: String,
    pub cache_dir: PathBuf,
}

impl Default for StoreConfig {
    fn default() -> Self {
        let data_dir = std::env::var_os("DARK_GRAVITY_DATA_DIR")
            .filter(|v| !v.is_empty())
            .map(PathBuf::from);
        let base_url = std::env::var("DARK_GRAVITY_BASE_URL")
            .ok()
            .filter(|v| !v.trim().is_empty())
            .unwrap_or_else(|| "https://lgcorzo.github.io".to_string());
        let cache_dir = std::env::var_os("DARK_GRAVITY_CACHE_DIR")
            .filter(|v| !v.is_empty())
            .map(PathBuf::from)
            .unwrap_or_else(default_cache_dir);
        Self {
            data_dir,
            base_url,
            cache_dir,
        }
    }
}

fn default_cache_dir() -> PathBuf {
    if let Some(home) = std::env::var_os("HOME").filter(|h| !h.is_empty()) {
        return PathBuf::from(home).join(".cache").join("dark-gravity-mcp");
    }
    std::env::temp_dir().join("dark-gravity-mcp-cache")
}

#[derive(Debug, Clone)]
pub struct KnowledgeStore {
    config: StoreConfig,
    http: reqwest::Client,
    mem_cache: Arc<RwLock<HashMap<String, String>>>,
}

impl KnowledgeStore {
    pub fn new(config: StoreConfig) -> Self {
        let http = reqwest::Client::builder()
            .user_agent(concat!("dark-gravity-mcp/", env!("CARGO_PKG_VERSION")))
            .timeout(std::time::Duration::from_secs(15))
            .build()
            .unwrap_or_else(|_| reqwest::Client::new());
        Self {
            config,
            http,
            mem_cache: Arc::new(RwLock::new(HashMap::new())),
        }
    }

    pub fn data_dir(&self) -> Option<&Path> {
        self.config.data_dir.as_deref()
    }

    /// Strict read-only text resolution:
    /// 1. In-memory cache (guarantees < 1 ms cached reads)
    /// 2. `DARK_GRAVITY_DATA_DIR/<rel_path>` if present on disk
    /// 3. Disk cache + HTTPS conditional ETag sync (`If-None-Match`) with SHA-256 verification
    pub async fn read_text(&self, rel_path: &str) -> Result<String, StoreError> {
        let normalized = rel_path.trim_start_matches('/');
        if normalized.contains("..") {
            return Err(StoreError::NotFound(normalized.to_string()));
        }

        if let Some(cached) = self.mem_cache.read().await.get(normalized).cloned() {
            return Ok(cached);
        }

        if let Some(dir) = &self.config.data_dir {
            let local_path = dir.join(normalized);
            if local_path.is_file() {
                let text = tokio::fs::read_to_string(&local_path)
                    .await
                    .map_err(|source| StoreError::Io {
                        path: local_path.display().to_string(),
                        source,
                    })?;
                self.mem_cache
                    .write()
                    .await
                    .insert(normalized.to_string(), text.clone());
                return Ok(text);
            }
        }

        let text = self.fetch_or_load_cached(normalized).await?;
        self.mem_cache
            .write()
            .await
            .insert(normalized.to_string(), text.clone());
        Ok(text)
    }

    pub async fn read_json(&self, rel_path: &str) -> Result<Value, StoreError> {
        let raw = self.read_text(rel_path).await?;
        serde_json::from_str(&raw).map_err(|source| StoreError::Json {
            path: rel_path.to_string(),
            source,
        })
    }

    /// Best-effort read of sibling repository ARCHITECTURE.md when `DARK_GRAVITY_DATA_DIR`
    /// lives inside a workspace containing sibling public checkouts.
    pub async fn try_read_sibling_architecture(&self, repo_name: &str) -> Option<String> {
        if repo_name.contains("..") || repo_name.contains('/') || repo_name.contains('\\') {
            return None;
        }
        let dir = self.config.data_dir.as_ref()?;
        let candidate = dir.parent()?.join(repo_name).join("ARCHITECTURE.md");
        if candidate.is_file() {
            tokio::fs::read_to_string(candidate).await.ok()
        } else {
            None
        }
    }

    async fn fetch_or_load_cached(&self, normalized: &str) -> Result<String, StoreError> {
        let safe_key = normalized.replace('/', "__");
        let body_path = self.config.cache_dir.join(format!("{safe_key}.body"));
        let etag_path = self.config.cache_dir.join(format!("{safe_key}.etag"));
        let sha_path = self.config.cache_dir.join(format!("{safe_key}.sha256"));

        let cached_body = verify_disk_cache(&body_path, &sha_path).await;
        let cached_etag = tokio::fs::read_to_string(&etag_path)
            .await
            .ok()
            .map(|s| s.trim().to_string())
            .filter(|s| !s.is_empty());

        let base = self.config.base_url.trim_end_matches('/');
        let url = format!("{base}/{normalized}");
        let mut req = self.http.get(&url);
        if cached_body.is_some()
            && let Some(etag) = &cached_etag
        {
            req = req.header(IF_NONE_MATCH, etag);
        }

        match req.send().await {
            Ok(resp) => {
                let status = resp.status();
                if status == reqwest::StatusCode::NOT_MODIFIED
                    && let Some(body) = cached_body
                {
                    return Ok(body);
                }
                if status.is_success() {
                    let etag = resp
                        .headers()
                        .get(ETAG)
                        .and_then(|v| v.to_str().ok())
                        .map(str::to_string);
                    let text = resp.text().await.map_err(|source| StoreError::Http {
                        url: url.clone(),
                        source,
                    })?;
                    let _ = persist_disk_cache(&body_path, &etag_path, &sha_path, &text, etag.as_deref()).await;
                    return Ok(text);
                }
                if let Some(body) = cached_body {
                    return Ok(body);
                }
                Err(StoreError::HttpStatus {
                    url,
                    status: status.as_u16(),
                })
            }
            Err(source) => {
                if let Some(body) = cached_body {
                    return Ok(body);
                }
                Err(StoreError::Http { url, source })
            }
        }
    }
}

async fn verify_disk_cache(body_path: &Path, sha_path: &Path) -> Option<String> {
    let body = tokio::fs::read_to_string(body_path).await.ok()?;
    let expected = tokio::fs::read_to_string(sha_path).await.ok()?;
    let actual = sha256_hex(body.as_bytes());
    if actual.eq_ignore_ascii_case(expected.trim()) {
        Some(body)
    } else {
        None
    }
}

async fn persist_disk_cache(
    body_path: &Path,
    etag_path: &Path,
    sha_path: &Path,
    body: &str,
    etag: Option<&str>,
) -> std::io::Result<()> {
    if let Some(parent) = body_path.parent() {
        tokio::fs::create_dir_all(parent).await?;
    }
    let digest = sha256_hex(body.as_bytes());
    tokio::fs::write(body_path, body).await?;
    tokio::fs::write(sha_path, digest).await?;
    if let Some(tag) = etag {
        tokio::fs::write(etag_path, tag).await?;
    }
    Ok(())
}

pub fn sha256_hex(bytes: &[u8]) -> String {
    let mut hasher = Sha256::new();
    hasher.update(bytes);
    hex::encode(hasher.finalize())
}
