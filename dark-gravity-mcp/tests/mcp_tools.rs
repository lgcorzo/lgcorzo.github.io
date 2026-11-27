use std::path::PathBuf;
use std::process::Stdio;
use std::time::Instant;

use dark_gravity_mcp::server::{
    GetAdrsRequest, GetArchitectureRequest, GetExperimentsRequest, GetMetricsRequest,
    GetRepositoryMapRequest, GetResearchRequest,
};
use dark_gravity_mcp::{DarkGravityMcpServer, KnowledgeStore, StoreConfig};
use rmcp::ServerHandler;
use rmcp::handler::server::wrapper::Parameters;
use serde_json::Value;
use tokio::io::{AsyncBufReadExt, AsyncWriteExt, BufReader};
use tokio::process::Command;

fn repo_root() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .expect("lgcorzo.github.io parent")
        .to_path_buf()
}

fn test_server() -> DarkGravityMcpServer {
    let tmp = tempfile::tempdir().expect("tempdir").keep();
    let store = KnowledgeStore::new(StoreConfig {
        data_dir: Some(repo_root()),
        base_url: "https://lgcorzo.github.io".to_string(),
        cache_dir: tmp,
    });
    DarkGravityMcpServer::new(store)
}

fn parse_tool_json(res: rmcp::model::CallToolResult) -> Value {
    let txt = res
        .content
        .first()
        .and_then(|c| c.as_text())
        .expect("text content block")
        .text
        .clone();
    serde_json::from_str(&txt).expect("valid JSON tool payload")
}

#[tokio::test]
async fn test_all_six_tools_and_read_only_guarantees() {
    let server = test_server();
    let info = server.get_info();
    assert_eq!(info.server_info.name, "dark-gravity-mcp");
    assert!(info.capabilities.tools.is_some());
    assert!(info.capabilities.resources.is_some());

    // 1. get_architecture global + scoped + unknown scope
    let global_arch = parse_tool_json(
        server
            .get_architecture(Parameters(GetArchitectureRequest {
                scope: Some("global".to_string()),
                include_diagrams: Some(true),
            }))
            .await
            .expect("global architecture"),
    );
    assert_eq!(global_arch["schema_version"], "1.0");
    assert_eq!(global_arch["onion_crates"].as_array().unwrap().len(), 5);
    assert!(global_arch["diagram_mermaid"].as_str().unwrap().contains("flowchart"));

    let scoped_arch = parse_tool_json(
        server
            .get_architecture(Parameters(GetArchitectureRequest {
                scope: Some("rust_CACD_autonomous_factory".to_string()),
                include_diagrams: Some(false),
            }))
            .await
            .expect("scoped architecture"),
    );
    assert_eq!(scoped_arch["scope"], "rust_CACD_autonomous_factory");

    let unknown_err = server
        .get_architecture(Parameters(GetArchitectureRequest {
            scope: Some("nonexistent-repo-xyz".to_string()),
            include_diagrams: None,
        }))
        .await
        .expect_err("unknown scope should fail");
    assert!(unknown_err.message.contains("UNKNOWN_SCOPE"));

    // 2. get_research
    let research = parse_tool_json(
        server
            .get_research(Parameters(GetResearchRequest { rq_id: Some("RQ1".to_string()) }))
            .await
            .expect("get_research"),
    );
    assert_eq!(research["research_hypotheses"].as_array().unwrap().len(), 1);
    assert_eq!(research["research_hypotheses"][0]["id"], "RQ1");

    // 3. get_repository_map including has_repositories_md
    let repo_map = parse_tool_json(
        server
            .get_repository_map(Parameters(GetRepositoryMapRequest {
                tier: None,
                include_forks: Some(true),
            }))
            .await
            .expect("get_repository_map"),
    );
    assert_eq!(repo_map["repository_statistics"]["public_repositories_total"], 64);
    assert_eq!(repo_map["repository_statistics"]["maintained_forks"], 42);
    let repos = repo_map["repositories"].as_array().unwrap();
    assert!(repos.iter().all(|r| r.get("has_repositories_md").is_some()));

    // 4. get_adrs
    let adrs = parse_tool_json(
        server
            .get_adrs(Parameters(GetAdrsRequest {
                adr_id: Some("ADR-008".to_string()),
                status: None,
            }))
            .await
            .expect("get_adrs"),
    );
    assert_eq!(adrs["count"], 1);
    assert_eq!(adrs["adrs"][0]["id"], "ADR-008");

    // 5. get_experiments
    let exps = parse_tool_json(
        server
            .get_experiments(Parameters(GetExperimentsRequest {
                exp_id: None,
                rq_id: None,
                outcome: None,
            }))
            .await
            .expect("get_experiments"),
    );
    assert_eq!(exps["count"], 14);

    // 6. get_metrics
    let metrics = parse_tool_json(
        server
            .get_metrics(Parameters(GetMetricsRequest {
                domain: None,
                include_pending: Some(true),
            }))
            .await
            .expect("get_metrics"),
    );
    assert_eq!(metrics["kpi_count"], 13);
}

#[tokio::test]
async fn test_cached_latency_under_100ms_p95() {
    let server = test_server();
    // Warm up cache once
    let _ = server
        .get_architecture(Parameters(GetArchitectureRequest {
            scope: None,
            include_diagrams: None,
        }))
        .await
        .unwrap();

    let mut samples_ms = Vec::with_capacity(60);
    for _ in 0..10 {
        for call_idx in 0..6 {
            let start = Instant::now();
            match call_idx {
                0 => {
                    server
                        .get_architecture(Parameters(GetArchitectureRequest {
                            scope: None,
                            include_diagrams: None,
                        }))
                        .await
                        .unwrap();
                }
                1 => {
                    server
                        .get_research(Parameters(GetResearchRequest { rq_id: None }))
                        .await
                        .unwrap();
                }
                2 => {
                    server
                        .get_repository_map(Parameters(GetRepositoryMapRequest {
                            tier: None,
                            include_forks: None,
                        }))
                        .await
                        .unwrap();
                }
                3 => {
                    server
                        .get_adrs(Parameters(GetAdrsRequest {
                            adr_id: None,
                            status: None,
                        }))
                        .await
                        .unwrap();
                }
                4 => {
                    server
                        .get_experiments(Parameters(GetExperimentsRequest {
                            exp_id: None,
                            rq_id: None,
                            outcome: None,
                        }))
                        .await
                        .unwrap();
                }
                _ => {
                    server
                        .get_metrics(Parameters(GetMetricsRequest {
                            domain: None,
                            include_pending: None,
                        }))
                        .await
                        .unwrap();
                }
            }
            samples_ms.push(start.elapsed().as_secs_f64() * 1000.0);
        }
    }
    samples_ms.sort_by(|a, b| a.partial_cmp(b).unwrap());
    let p95 = samples_ms[(samples_ms.len() * 95) / 100];
    assert!(p95 < 100.0, "Expected p95 < 100 ms, observed {p95:.2} ms");
}

#[tokio::test]
async fn test_stdio_binary_initialize_list_and_call() {
    let bin = env!("CARGO_BIN_EXE_dark-gravity-mcp");
    let mut child = Command::new(bin)
        .arg("--transport")
        .arg("stdio")
        .env("DARK_GRAVITY_DATA_DIR", repo_root())
        .env("DARK_GRAVITY_CACHE_DIR", tempfile::tempdir().unwrap().keep())
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .expect("spawn dark-gravity-mcp stdio");

    let mut stdin = child.stdin.take().unwrap();
    let stdout = child.stdout.take().unwrap();
    let mut reader = BufReader::new(stdout);

    let init_req = serde_json::json!({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "mcp-test", "version": "0.1.0"}
        }
    });
    stdin
        .write_all(format!("{init_req}\n").as_bytes())
        .await
        .unwrap();
    stdin.flush().await.unwrap();

    let mut line = String::new();
    reader.read_line(&mut line).await.unwrap();
    let init_resp: Value = serde_json::from_str(&line).expect("init json-rpc response");
    assert_eq!(init_resp["id"], 1);
    assert!(init_resp.get("result").is_some(), "init failed: {init_resp}");

    let initialized_notif = serde_json::json!({
        "jsonrpc": "2.0",
        "method": "notifications/initialized"
    });
    stdin
        .write_all(format!("{initialized_notif}\n").as_bytes())
        .await
        .unwrap();

    let list_tools_req = serde_json::json!({
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    });
    stdin
        .write_all(format!("{list_tools_req}\n").as_bytes())
        .await
        .unwrap();
    stdin.flush().await.unwrap();

    line.clear();
    reader.read_line(&mut line).await.unwrap();
    let list_resp: Value = serde_json::from_str(&line).expect("tools/list json-rpc response");
    assert_eq!(list_resp["id"], 2);
    let tools = list_resp["result"]["tools"].as_array().unwrap();
    assert_eq!(tools.len(), 6);
    for t in tools {
        assert_eq!(t["annotations"]["readOnlyHint"], true);
        assert_eq!(t["annotations"]["destructiveHint"], false);
    }

    let list_res_req = serde_json::json!({
        "jsonrpc": "2.0",
        "id": 3,
        "method": "resources/list",
        "params": {}
    });
    stdin
        .write_all(format!("{list_res_req}\n").as_bytes())
        .await
        .unwrap();
    stdin.flush().await.unwrap();

    line.clear();
    reader.read_line(&mut line).await.unwrap();
    let res_resp: Value = serde_json::from_str(&line).expect("resources/list response");
    assert_eq!(res_resp["id"], 3);
    assert_eq!(res_resp["result"]["resources"].as_array().unwrap().len(), 7);

    let read_res_req = serde_json::json!({
        "jsonrpc": "2.0",
        "id": 4,
        "method": "resources/read",
        "params": {"uri": "dark-gravity://manifest"}
    });
    stdin
        .write_all(format!("{read_res_req}\n").as_bytes())
        .await
        .unwrap();
    stdin.flush().await.unwrap();

    line.clear();
    reader.read_line(&mut line).await.unwrap();
    let read_resp: Value = serde_json::from_str(&line).expect("resources/read response");
    assert_eq!(read_resp["id"], 4);
    assert!(
        read_resp["result"]["contents"][0]["text"]
            .as_str()
            .unwrap()
            .contains("manifest_version")
    );

    drop(stdin);
    let status = child.wait().await.unwrap();
    assert!(status.success(), "stdio exited with {status}");
}
