use std::net::SocketAddr;
use std::sync::Arc;

use axum::{Json, Router, routing::get};
use clap::{Parser, ValueEnum};
use dark_gravity_mcp::{DarkGravityMcpServer, KnowledgeStore, StoreConfig};
use rmcp::ServiceExt;
use rmcp::transport::stdio;
use rmcp::transport::streamable_http_server::{
    StreamableHttpServerConfig, StreamableHttpService, session::local::LocalSessionManager,
};
use serde_json::json;
use tokio::net::TcpListener;
use tracing_subscriber::EnvFilter;

#[derive(Debug, Clone, Copy, ValueEnum)]
enum TransportMode {
    Stdio,
    StreamableHttp,
}

#[derive(Debug, Parser)]
#[command(
    name = "dark-gravity-mcp",
    version,
    about = "Read-only Model Context Protocol (MCP) server for Dark Gravity ecosystem knowledge"
)]
struct Cli {
    /// Transport mode to expose ("stdio" for local clients, "streamable-http" for cluster HTTP)
    #[arg(long, env = "DARK_GRAVITY_MCP_TRANSPORT", value_enum, default_value = "stdio")]
    transport: TransportMode,

    /// Bind address for streamable-http transport
    #[arg(long, env = "DARK_GRAVITY_MCP_BIND", default_value = "0.0.0.0:8080")]
    bind: SocketAddr,
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // Log diagnostics strictly to stderr so stdio JSON-RPC frames remain uncorrupted.
    tracing_subscriber::fmt()
        .with_env_filter(
            EnvFilter::try_from_default_env().unwrap_or_else(|_| EnvFilter::new("info")),
        )
        .with_writer(std::io::stderr)
        .init();

    let cli = Cli::parse();
    let store = KnowledgeStore::new(StoreConfig::default());

    match cli.transport {
        TransportMode::Stdio => {
            let server = DarkGravityMcpServer::new(store);
            let running = server.serve(stdio()).await?;
            running.waiting().await?;
        }
        TransportMode::StreamableHttp => {
            let session_manager = Arc::new(LocalSessionManager::default());
            let mcp_service = StreamableHttpService::new(
                move || Ok(DarkGravityMcpServer::new(store.clone())),
                session_manager,
                StreamableHttpServerConfig::default(),
            );
            let app = Router::new()
                .route(
                    "/healthz",
                    get(|| async { Json(json!({"status": "ok", "read_only": true})) }),
                )
                .nest_service("/mcp", mcp_service);

            tracing::info!("dark-gravity-mcp listening on http://{}/mcp", cli.bind);
            let listener = TcpListener::bind(cli.bind).await?;
            axum::serve(listener, app).await?;
        }
    }

    Ok(())
}
