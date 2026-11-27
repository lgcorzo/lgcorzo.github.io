# `dark-gravity-mcp` — Strictly Read-Only Knowledge MCP Server

`dark-gravity-mcp` is Dark Gravity's official **read-only** [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server written in **Rust Edition 2024** (`rmcp`).

## Isolation & Security Contract
- **Strictly read-only**: exposes architectural documentation, repository topology, ADRs, research questions (`RQ1`–`RQ4`), experiment logs (`EXP-2026-001`..`014`), and KPI metrics.
- **Zero privileged surface**: never spawns sandbox pods, mutates repositories, triggers Hatchet DAGs, or reads Kubernetes/Vault secrets. Completely decoupled from `rust_CACD_autonomous_factory/crates/factory-mcp-server`.
- **DOC-011 clean**: reads only public `lgcorzo.github.io` artifacts (via local checkout `DARK_GRAVITY_DATA_DIR` or ETag/SHA-256 cached HTTPS `DARK_GRAVITY_BASE_URL`).

## Exposed MCP Tools (6)

1. `get_architecture(scope="global", include_diagrams=false)`
2. `get_research(rq_id=null)`
3. `get_repository_map(tier=null, include_forks=true)` (includes `has_repositories_md`)
4. `get_adrs(adr_id=null, status=null)`
5. `get_experiments(exp_id=null, rq_id=null, outcome=null)`
6. `get_metrics(domain=null, include_pending=true)`

## Exposed Resources (7 `dark-gravity://` URIs)
- `dark-gravity://manifest`
- `dark-gravity://knowledge-graph`
- `dark-gravity://auditor/executive-summary`
- `dark-gravity://auditor/architecture`
- `dark-gravity://auditor/research`
- `dark-gravity://auditor/metrics`
- `dark-gravity://auditor/ecosystem`

## Local Client Quickstart (`stdio`)

Build and run directly from the `lgcorzo.github.io` checkout:

```bash
cargo run --manifest-path dark-gravity-mcp/Cargo.toml -- --transport stdio
```

### Claude Code / Cursor / GitHub Copilot (`mcpServers`)

```json
{
  "mcpServers": {
    "dark-gravity": {
      "command": "cargo",
      "args": ["run", "--quiet", "--manifest-path", "dark-gravity-mcp/Cargo.toml"],
      "env": {
        "DARK_GRAVITY_BASE_URL": "https://lgcorzo.github.io"
      }
    }
  }
}
```

Or using the prebuilt static container via Docker (`stdio` or `--transport streamable-http --bind 0.0.0.0:8080`).

## Verification

```bash
cargo test --manifest-path dark-gravity-mcp/Cargo.toml
```
