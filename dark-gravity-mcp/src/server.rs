use std::collections::BTreeSet;

use jiff::Timestamp;
use rmcp::{
    ErrorData, RoleServer, ServerHandler,
    handler::server::{router::tool::ToolRouter, wrapper::Parameters},
    model::{
        CallToolResult, ContentBlock, Implementation, ListResourcesResult,
        PaginatedRequestParams, ReadResourceRequestParams, ReadResourceResponse,
        ReadResourceResult, Resource, ResourceContents, ServerCapabilities, ServerConfig,
    },
    schemars,
    service::RequestContext,
    tool, tool_handler, tool_router,
};
use serde::Deserialize;
use serde_json::{Value, json};

use crate::store::{KnowledgeStore, StoreConfig, StoreError};

const SCHEMA_VERSION: &str = "1.0";

const RESOURCE_SPECS: &[(&str, &str, &str, &str)] = &[
    (
        "dark-gravity://manifest",
        "DARK_GRAVITY_MANIFEST.md",
        "DARK_GRAVITY_MANIFEST.md",
        "text/markdown",
    ),
    (
        "dark-gravity://knowledge-graph",
        "knowledge_graph.json",
        "knowledge_graph.json",
        "application/json",
    ),
    (
        "dark-gravity://auditor/executive-summary",
        "docs/auditor/executive-summary.md",
        "docs/auditor/executive-summary.md",
        "text/markdown",
    ),
    (
        "dark-gravity://auditor/architecture",
        "docs/auditor/architecture.md",
        "docs/auditor/architecture.md",
        "text/markdown",
    ),
    (
        "dark-gravity://auditor/research",
        "docs/auditor/research.md",
        "docs/auditor/research.md",
        "text/markdown",
    ),
    (
        "dark-gravity://auditor/metrics",
        "docs/auditor/metrics.md",
        "docs/auditor/metrics.md",
        "text/markdown",
    ),
    (
        "dark-gravity://auditor/ecosystem",
        "docs/auditor/ecosystem.md",
        "docs/auditor/ecosystem.md",
        "text/markdown",
    ),
];

#[derive(Debug, Deserialize, schemars::JsonSchema)]
pub struct GetArchitectureRequest {
    /// Target scope: "global" or a canonical Dark Gravity repository name/id (default: "global").
    pub scope: Option<String>,
    /// Include inline Mermaid diagram overview when scope is "global" (default: false).
    pub include_diagrams: Option<bool>,
}

#[derive(Debug, Deserialize, schemars::JsonSchema)]
pub struct GetResearchRequest {
    /// Optional Research Question ID filter ("RQ1", "RQ2", "RQ3", "RQ4").
    pub rq_id: Option<String>,
}

#[derive(Debug, Deserialize, schemars::JsonSchema)]
pub struct GetRepositoryMapRequest {
    /// Optional tier filter ("core_factory", "orchestration_bridge", "owned_domain", "public_portal", "maintained_fork", "private_gitops").
    pub tier: Option<String>,
    /// Whether to include maintained forks and frozen archive entries (default: true).
    pub include_forks: Option<bool>,
}

#[derive(Debug, Deserialize, schemars::JsonSchema)]
pub struct GetAdrsRequest {
    /// Optional ADR identifier filter (e.g. "ADR-008").
    pub adr_id: Option<String>,
    /// Optional status filter ("proposed", "accepted", "superseded", "deprecated").
    pub status: Option<String>,
}

#[derive(Debug, Deserialize, schemars::JsonSchema)]
pub struct GetExperimentsRequest {
    /// Optional Experiment ID filter (e.g. "EXP-2026-014").
    pub exp_id: Option<String>,
    /// Optional Research Question filter (e.g. "RQ1").
    pub rq_id: Option<String>,
    /// Optional outcome filter ("passed", "partial", "failed", "baseline").
    pub outcome: Option<String>,
}

#[derive(Debug, Deserialize, schemars::JsonSchema)]
pub struct GetMetricsRequest {
    /// Optional KPI domain filter ("development", "quality", "security", "agents").
    pub domain: Option<String>,
    /// Include baseline_pending / UNMEASURED KPIs (default: true).
    pub include_pending: Option<bool>,
}

#[derive(Debug, Clone)]
pub struct DarkGravityMcpServer {
    store: KnowledgeStore,
    tool_router: ToolRouter<Self>,
}

impl DarkGravityMcpServer {
    pub fn from_env() -> Self {
        Self::new(KnowledgeStore::new(StoreConfig::default()))
    }

    pub fn new(store: KnowledgeStore) -> Self {
        Self {
            store,
            tool_router: Self::tool_router(),
        }
    }

    pub fn store(&self) -> &KnowledgeStore {
        &self.store
    }

    async fn resolve_source_timestamp(&self) -> String {
        if let Ok(kg) = self.store.read_json("knowledge_graph.json").await
            && let Some(ts) = kg.get("generated_at").and_then(Value::as_str)
        {
            return ts.to_string();
        }
        Timestamp::now().to_string()
    }
}

fn map_store_error(err: StoreError) -> ErrorData {
    match err {
        StoreError::NotFound(msg) => ErrorData::resource_not_found(msg, None),
        other => ErrorData::internal_error(other.to_string(), None),
    }
}

fn ok_json(payload: Value) -> Result<CallToolResult, ErrorData> {
    let pretty = serde_json::to_string_pretty(&payload)
        .map_err(|e| ErrorData::internal_error(e.to_string(), None))?;
    Ok(CallToolResult::success(vec![ContentBlock::text(pretty)]))
}

#[tool_router]
impl DarkGravityMcpServer {
    /// Retrieve Dark Gravity system architecture overview or scoped repository architecture details (read-only).
    #[tool(
        name = "get_architecture",
        description = "Read-only architecture overview globally or scoped to a Dark Gravity repository (crates, Hatchet 5-step pipeline, gVisor, NHI, HITL Vertices).",
        annotations(
            title = "Get Dark Gravity Architecture",
            read_only_hint = true,
            destructive_hint = false,
            idempotent_hint = true,
            open_world_hint = false
        )
    )]
    pub async fn get_architecture(
        &self,
        Parameters(req): Parameters<GetArchitectureRequest>,
    ) -> Result<CallToolResult, ErrorData> {
        let scope = req
            .scope
            .unwrap_or_else(|| "global".to_string())
            .trim()
            .to_string();
        let include_diagrams = req.include_diagrams.unwrap_or(false);

        let registry = self
            .store
            .read_json("data/ecosystem-registry.json")
            .await
            .map_err(map_store_error)?;
        let kg = self
            .store
            .read_json("knowledge_graph.json")
            .await
            .map_err(map_store_error)?;
        let ts = resolve_ts(&kg);

        let repos = registry
            .get("repositories")
            .and_then(Value::as_array)
            .cloned()
            .unwrap_or_default();

        let mut valid_scopes: BTreeSet<String> = BTreeSet::from(["global".to_string()]);
        for r in &repos {
            if let Some(name) = r.get("name").and_then(Value::as_str) {
                valid_scopes.insert(name.to_string());
            }
            if let Some(id) = r.get("id").and_then(Value::as_str) {
                valid_scopes.insert(id.to_string());
            }
        }

        if scope.eq_ignore_ascii_case("global") {
            let arch_doc = self.store.read_text("docs/auditor/architecture.md").await.ok();
            let mut body = json!({
                "schema_version": SCHEMA_VERSION,
                "source_timestamp": ts,
                "scope": "global",
                "onion_crates": [
                    "factory-core",
                    "factory-application",
                    "factory-infrastructure",
                    "factory-mcp-server",
                    "factory-cli"
                ],
                "mission_pipeline": {
                    "trigger": "Kafka mission-input",
                    "hatchet_steps": [
                        "rustant-plan",
                        "zeroclaw-execute",
                        "zeroclaw-validate",
                        "rustant-review",
                        "factory-deliver"
                    ]
                },
                "runtime_isolation": {
                    "sandbox_runtime": "gVisor (runsc)",
                    "micro_sandbox_limits": "30Mi RAM / 250m CPU",
                    "compilation_sandbox_limits": "512Mi RAM / 500m CPU",
                    "fr008_ctrl02_status": "TESTED (kept TESTED while AUD-010 open)"
                },
                "nhi_security": {
                    "signing": "Ed25519 W3C-VC",
                    "credentials": "HashiCorp Vault JIT (300s TTL)",
                    "memory_wipe_ns": 54.2
                },
                "hitl_vertices": [
                    {"vertex": 1, "name": "Strategic Injection", "status": "designed"},
                    {"vertex": 2, "name": "Sprint Mobilization", "status": "designed"},
                    {"vertex": 3, "name": "Exception Override", "status": "designed"},
                    {"vertex": 4, "name": "Categorical Scrutiny", "status": "implemented", "enforced_rule": "Autonomous merges to main strictly prohibited"}
                ],
                "namespaces": ["agents", "orchestrators", "confluent", "storage", "knowledge", "llm-apps", "security", "openziti", "development", "flux-system"],
                "auditor_extract": arch_doc,
            });
            if include_diagrams {
                body["diagram_mermaid"] = json!(
                    "flowchart LR\n  GitHub[Labeled Issue] -->|GitPlatformPoller Ed25519| Kafka[Kafka mission-input]\n  Kafka --> P1[1. rustant-plan]\n  P1 --> P2[2. zeroclaw-execute in gVisor]\n  P2 --> P3[3. zeroclaw-validate]\n  P3 --> P4[4. rustant-review >= 8.0]\n  P4 --> P5[5. factory-deliver PR]\n  P5 -->|Vertex 4 HITL| Human[Human Merge Decision]"
                );
            }
            return ok_json(body);
        }

        let matched = repos.into_iter().find(|r| {
            r.get("name")
                .and_then(Value::as_str)
                .is_some_and(|n| n.eq_ignore_ascii_case(&scope))
                || r.get("id")
                    .and_then(Value::as_str)
                    .is_some_and(|id| id.eq_ignore_ascii_case(&scope))
        });

        let Some(repo) = matched else {
            let valid_vec: Vec<String> = valid_scopes.into_iter().collect();
            return Err(ErrorData::invalid_params(
                format!("UNKNOWN_SCOPE: unsupported architecture scope '{scope}'"),
                Some(json!({
                    "code": "UNKNOWN_SCOPE",
                    "scope": scope,
                    "valid_scopes": valid_vec
                })),
            ));
        };

        let repo_id = repo.get("id").and_then(Value::as_str).unwrap_or("");
        let repo_name = repo.get("name").and_then(Value::as_str).unwrap_or("");
        let neighbors: Vec<Value> = kg
            .get("edges")
            .and_then(Value::as_array)
            .map(|edges| {
                edges
                    .iter()
                    .filter(|e| {
                        e.get("source").and_then(Value::as_str) == Some(repo_id)
                            || e.get("target").and_then(Value::as_str) == Some(repo_id)
                    })
                    .cloned()
                    .collect()
            })
            .unwrap_or_default();

        let local_arch_md = if repo.get("visibility").and_then(Value::as_str) == Some("public") {
            if repo_name == "lgcorzo.github.io" {
                self.store.read_text("ARCHITECTURE.md").await.ok()
            } else {
                self.store.try_read_sibling_architecture(repo_name).await
            }
        } else {
            None
        };

        ok_json(json!({
            "schema_version": SCHEMA_VERSION,
            "source_timestamp": ts,
            "scope": repo_name,
            "repository": repo,
            "kg_neighbors": neighbors,
            "architecture_markdown": local_arch_md,
        }))
    }

    /// Query explicit research questions (RQ1-RQ4), target KPIs, and linked experiments (read-only).
    #[tool(
        name = "get_research",
        description = "Read-only query of Dark Gravity Research Questions (RQ1-RQ4), operational hypotheses, target metric IDs, and linked experiments.",
        annotations(
            title = "Get Dark Gravity Research Questions",
            read_only_hint = true,
            destructive_hint = false,
            idempotent_hint = true,
            open_world_hint = false
        )
    )]
    pub async fn get_research(
        &self,
        Parameters(req): Parameters<GetResearchRequest>,
    ) -> Result<CallToolResult, ErrorData> {
        let kg = self
            .store
            .read_json("knowledge_graph.json")
            .await
            .map_err(map_store_error)?;
        let research_md = self.store.read_text("RESEARCH.md").await.ok();
        let ts = resolve_ts(&kg);

        let rq_filter = req.rq_id.as_deref().map(str::trim).filter(|s| !s.is_empty());
        let mut rqs: Vec<Value> = kg
            .get("nodes")
            .and_then(Value::as_array)
            .map(|nodes| {
                nodes
                    .iter()
                    .filter(|n| n.get("entity_type").and_then(Value::as_str) == Some("ResearchHypothesis"))
                    .filter(|n| match rq_filter {
                        Some(want) => n.get("id").and_then(Value::as_str).is_some_and(|id| id.eq_ignore_ascii_case(want)),
                        None => true,
                    })
                    .cloned()
                    .collect()
            })
            .unwrap_or_default();

        if let Some(want) = rq_filter
            && rqs.is_empty()
        {
            return Err(ErrorData::invalid_params(
                format!("UNKNOWN_RQ: '{want}' not found in RQ1..RQ4"),
                Some(json!({"code": "UNKNOWN_RQ", "rq_id": want})),
            ));
        }

        // Enrich with linked Experiment IDs from edges
        let edges = kg.get("edges").and_then(Value::as_array).cloned().unwrap_or_default();
        for node in &mut rqs {
            if let Some(id) = node.get("id").and_then(Value::as_str).map(str::to_string) {
                let validating_exps: Vec<String> = edges
                    .iter()
                    .filter(|e| {
                        e.get("relation").and_then(Value::as_str) == Some("VALIDATES_HYPOTHESIS")
                            && e.get("target").and_then(Value::as_str) == Some(&id)
                    })
                    .filter_map(|e| e.get("source").and_then(Value::as_str).map(str::to_string))
                    .collect();
                if let Some(obj) = node.as_object_mut() {
                    obj.insert("validating_experiments".to_string(), json!(validating_exps));
                }
            }
        }

        ok_json(json!({
            "schema_version": SCHEMA_VERSION,
            "source_timestamp": ts,
            "filter_rq_id": rq_filter,
            "research_hypotheses": rqs,
            "vision_excerpt": research_md.as_deref().and_then(|s| s.get(..s.floor_char_boundary(900))),
        }))
    }

    /// Retrieve the DOC-011-clean repository map, canonical statistics, and standards flags (read-only).
    #[tool(
        name = "get_repository_map",
        description = "Read-only DOC-011-compliant map of Dark Gravity repositories, canonical counts (64 public = 22 original + 42 forks), and file standards compliance booleans including has_repositories_md.",
        annotations(
            title = "Get Dark Gravity Repository Map",
            read_only_hint = true,
            destructive_hint = false,
            idempotent_hint = true,
            open_world_hint = false
        )
    )]
    pub async fn get_repository_map(
        &self,
        Parameters(req): Parameters<GetRepositoryMapRequest>,
    ) -> Result<CallToolResult, ErrorData> {
        let registry = self
            .store
            .read_json("data/ecosystem-registry.json")
            .await
            .map_err(map_store_error)?;
        let ts = self.resolve_source_timestamp().await;

        let include_forks = req.include_forks.unwrap_or(true);
        let tier_filter = req.tier.as_deref().map(str::trim).filter(|s| !s.is_empty());

        let repos: Vec<Value> = registry
            .get("repositories")
            .and_then(Value::as_array)
            .map(|items| {
                items
                    .iter()
                    .filter(|r| include_forks || !r.get("is_fork").and_then(Value::as_bool).unwrap_or(false))
                    .filter(|r| match tier_filter {
                        Some(want) => r.get("tier").and_then(Value::as_str).is_some_and(|t| t.eq_ignore_ascii_case(want)),
                        None => true,
                    })
                    .cloned()
                    .collect()
            })
            .unwrap_or_default();

        ok_json(json!({
            "schema_version": SCHEMA_VERSION,
            "source_timestamp": ts,
            "repository_statistics": registry.get("repository_statistics").cloned().unwrap_or(json!({})),
            "portal_urls": registry.get("portal_urls").cloned().unwrap_or(json!({})),
            "filters": {
                "tier": tier_filter,
                "include_forks": include_forks
            },
            "count": repos.len(),
            "repositories": repos,
        }))
    }

    /// Retrieve indexed Architecture Decision Records (ADRs) including ADR-001 and ADR-008 (read-only).
    #[tool(
        name = "get_adrs",
        description = "Read-only Architecture Decision Record (ADR) index filtered by ADR ID or status (proposed, accepted, superseded, deprecated).",
        annotations(
            title = "Get Dark Gravity ADRs",
            read_only_hint = true,
            destructive_hint = false,
            idempotent_hint = true,
            open_world_hint = false
        )
    )]
    pub async fn get_adrs(
        &self,
        Parameters(req): Parameters<GetAdrsRequest>,
    ) -> Result<CallToolResult, ErrorData> {
        let kg = self
            .store
            .read_json("knowledge_graph.json")
            .await
            .map_err(map_store_error)?;
        let ts = resolve_ts(&kg);

        let id_filter = req.adr_id.as_deref().map(str::trim).filter(|s| !s.is_empty());
        let status_filter = req.status.as_deref().map(str::trim).filter(|s| !s.is_empty());

        let adrs: Vec<Value> = kg
            .get("nodes")
            .and_then(Value::as_array)
            .map(|nodes| {
                nodes
                    .iter()
                    .filter(|n| n.get("entity_type").and_then(Value::as_str) == Some("ArchitectureDecision"))
                    .filter(|n| match id_filter {
                        Some(want) => n.get("id").and_then(Value::as_str).is_some_and(|id| id.eq_ignore_ascii_case(want)),
                        None => true,
                    })
                    .filter(|n| match status_filter {
                        Some(want) => n
                            .pointer("/properties/adr_status")
                            .and_then(Value::as_str)
                            .is_some_and(|st| st.eq_ignore_ascii_case(want)),
                        None => true,
                    })
                    .cloned()
                    .collect()
            })
            .unwrap_or_default();

        ok_json(json!({
            "schema_version": SCHEMA_VERSION,
            "source_timestamp": ts,
            "count": adrs.len(),
            "adrs": adrs,
        }))
    }

    /// Query structured empirical experiment logs EXP-2026-001..014 (read-only).
    #[tool(
        name = "get_experiments",
        description = "Read-only filterable index of Dark Gravity empirical experiments (EXP-2026-001 through EXP-2026-014) with hypotheses, outcomes, and evidence anchors.",
        annotations(
            title = "Get Dark Gravity Experiments",
            read_only_hint = true,
            destructive_hint = false,
            idempotent_hint = true,
            open_world_hint = false
        )
    )]
    pub async fn get_experiments(
        &self,
        Parameters(req): Parameters<GetExperimentsRequest>,
    ) -> Result<CallToolResult, ErrorData> {
        let kg = self
            .store
            .read_json("knowledge_graph.json")
            .await
            .map_err(map_store_error)?;
        let ts = resolve_ts(&kg);

        let exp_filter = req.exp_id.as_deref().map(str::trim).filter(|s| !s.is_empty());
        let rq_filter = req.rq_id.as_deref().map(str::trim).filter(|s| !s.is_empty());
        let outcome_filter = req.outcome.as_deref().map(str::trim).filter(|s| !s.is_empty());

        let experiments: Vec<Value> = kg
            .get("nodes")
            .and_then(Value::as_array)
            .map(|nodes| {
                nodes
                    .iter()
                    .filter(|n| n.get("entity_type").and_then(Value::as_str) == Some("Experiment"))
                    .filter(|n| match exp_filter {
                        Some(want) => n.get("id").and_then(Value::as_str).is_some_and(|id| id.eq_ignore_ascii_case(want)),
                        None => true,
                    })
                    .filter(|n| match rq_filter {
                        Some(want) => n
                            .pointer("/properties/related_rqs")
                            .and_then(Value::as_array)
                            .is_some_and(|arr| {
                                arr.iter()
                                    .filter_map(Value::as_str)
                                    .any(|rq| rq.eq_ignore_ascii_case(want))
                            }),
                        None => true,
                    })
                    .filter(|n| match outcome_filter {
                        Some(want) => n
                            .pointer("/properties/outcome")
                            .and_then(Value::as_str)
                            .is_some_and(|out| out.eq_ignore_ascii_case(want)),
                        None => true,
                    })
                    .cloned()
                    .collect()
            })
            .unwrap_or_default();

        ok_json(json!({
            "schema_version": SCHEMA_VERSION,
            "source_timestamp": ts,
            "count": experiments.len(),
            "experiments": experiments,
        }))
    }

    /// Retrieve platform KPI snapshot across Development, Quality, Security, and Agents preserving UNMEASURED baseline_pending tags (read-only).
    #[tool(
        name = "get_metrics",
        description = "Read-only retrieval of the 13 canonical platform KPIs from data/metrics.json preserving measurement_status (verified, partial, baseline_pending) and evidence_source.",
        annotations(
            title = "Get Dark Gravity Platform Metrics",
            read_only_hint = true,
            destructive_hint = false,
            idempotent_hint = true,
            open_world_hint = false
        )
    )]
    pub async fn get_metrics(
        &self,
        Parameters(req): Parameters<GetMetricsRequest>,
    ) -> Result<CallToolResult, ErrorData> {
        let metrics = self
            .store
            .read_json("data/metrics.json")
            .await
            .map_err(map_store_error)?;
        let ts = metrics
            .get("generated_at")
            .and_then(Value::as_str)
            .map(str::to_string)
            .unwrap_or_else(|| Timestamp::now().to_string());

        let domain_filter = req.domain.as_deref().map(str::trim).filter(|s| !s.is_empty());
        let include_pending = req.include_pending.unwrap_or(true);

        let all_domains = ["development", "quality", "security", "agents"];
        if let Some(want) = domain_filter
            && !all_domains.iter().any(|d| d.eq_ignore_ascii_case(want))
        {
            return Err(ErrorData::invalid_params(
                format!("UNKNOWN_DOMAIN: '{want}' must be one of development, quality, security, agents"),
                Some(json!({"code": "UNKNOWN_DOMAIN", "valid_domains": all_domains})),
            ));
        }

        let mut filtered_domains = serde_json::Map::new();
        let mut total_kpis = 0usize;
        if let Some(domains_obj) = metrics.get("domains").and_then(Value::as_object) {
            for d in all_domains {
                if let Some(want) = domain_filter
                    && !d.eq_ignore_ascii_case(want)
                {
                    continue;
                }
                let items: Vec<Value> = domains_obj
                    .get(d)
                    .and_then(Value::as_array)
                    .map(|arr| {
                        arr.iter()
                            .filter(|item| {
                                include_pending
                                    || item.get("measurement_status").and_then(Value::as_str) != Some("baseline_pending")
                            })
                            .cloned()
                            .collect()
                    })
                    .unwrap_or_default();
                total_kpis += items.len();
                filtered_domains.insert(d.to_string(), Value::Array(items));
            }
        }

        ok_json(json!({
            "schema_version": SCHEMA_VERSION,
            "source_timestamp": ts,
            "window": metrics.get("window").cloned().unwrap_or(json!("rolling_30d")),
            "collection_sources": metrics.get("collection_sources").cloned().unwrap_or(json!([])),
            "include_pending": include_pending,
            "kpi_count": total_kpis,
            "domains": Value::Object(filtered_domains),
        }))
    }
}

#[tool_handler(router = self.tool_router)]
impl ServerHandler for DarkGravityMcpServer {
    fn get_info(&self) -> ServerConfig {
        ServerConfig::new(
            ServerCapabilities::builder()
                .enable_tools()
                .enable_resources()
                .build(),
        )
        .with_server_info(Implementation::new(
            "dark-gravity-mcp",
            env!("CARGO_PKG_VERSION"),
        ))
        .with_instructions(
            "Strictly read-only MCP server for Dark Gravity ecosystem knowledge, architecture, ADRs, research questions, experiments, and KPI metrics.",
        )
    }

    async fn list_resources(
        &self,
        _request: Option<PaginatedRequestParams>,
        _context: RequestContext<RoleServer>,
    ) -> Result<ListResourcesResult, ErrorData> {
        let resources = RESOURCE_SPECS
            .iter()
            .map(|(uri, name, desc, mime)| {
                Resource::new(*uri, *name)
                    .with_description(*desc)
                    .with_mime_type(*mime)
            })
            .collect();
        Ok(ListResourcesResult::with_all_items(resources))
    }

    async fn read_resource(
        &self,
        request: ReadResourceRequestParams,
        _context: RequestContext<RoleServer>,
    ) -> Result<ReadResourceResponse, ErrorData> {
        let Some(&(uri, _, rel_path, mime)) = RESOURCE_SPECS.iter().find(|(u, ..)| *u == request.uri)
        else {
            return Err(ErrorData::resource_not_found(
                format!("unknown resource URI: {}", request.uri),
                None,
            ));
        };
        let content = self
            .store
            .read_text(rel_path)
            .await
            .map_err(map_store_error)?;
        Ok(ReadResourceResult::new(vec![
            ResourceContents::text(content, uri).with_mime_type(mime),
        ])
        .into())
    }
}

fn resolve_ts(kg: &Value) -> String {
    kg.get("generated_at")
        .and_then(Value::as_str)
        .map(str::to_string)
        .unwrap_or_else(|| Timestamp::now().to_string())
}
