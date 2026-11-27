# Architecture: `lgcorzo.github.io` in Dark Gravity

## Ecosystem Role & Tier

- **Tier**: `public_portal`
- **Role**: Canonical public Knowledge Hub, Entry Portal (`/start-here`, `/ai-agents`), Experimental Lab Notebook, AI Auditor Pack (`/docs/auditor/`), machine-readable Knowledge Graph host (`knowledge_graph.{json,graphml,rdf}`), Platform Metrics Dashboard (`metrics.html`), RAG sync tooling (`tools/rag_pipeline/`), and read-only Rust MCP server (`dark-gravity-mcp/`).
- **Visibility**: `public`

## Internal Component Design

- **Static Portal (`index.html`, `architecture.html`, `lifecycle.html`, `fork-policy.html`, `notebooks.html`, `start-here/`, `ai-agents/`, `metrics.html`)**: Vanilla HTML5/CSS3/ES2022 JS pages synchronized via `tools/sync_shell.py` (`<!--SHELL:HEADER/FOOTER/PAGER-->`).
- **Canonical Data & Validation (`data/`, `scripts/`, `tests/`)**: `data/canonical-claims.json` and `data/ecosystem-registry.json` drive deterministic checks (`check_public_claims.py`, `verify_ecosystem_knowledge.py`, `pytest`) and CI workflows under `.github/workflows/`.
- **Knowledge Automation (`tools/`)**: Python 3.12 generators for triple-format Knowledge Graph emission, telemetry-grounded metrics collection, and 8-category R2R v3 RAG ingestion.
- **Official Read-Only MCP Crate (`dark-gravity-mcp/`)**: Co-located Rust (Edition 2024, `rmcp`) crate compiling to a native `stdio`/`streamable-http` server and `< 15 MB` distroless/scratch container image without duplicating schemas across repositories.

## Upstream & Downstream Ecosystem Interfaces

```text
rust_CACD_autonomous_factory (ADRs + evidence/records/*.json) ──┐
Sibling Active Repos (AGENTS/ARCHITECTURE/MANIFEST) ───────────┼──► lgcorzo.github.io (Registry + KG + Metrics + /docs/auditor/)
GitHub Public REST API (inventory + release/PR/alert telemetry)┘         │
                                                                         ├──► External Coding/Audit Agents (/start-here, /ai-agents, dark-gravity-mcp)
                                                                         └──► R2R v3 Engine & Optional Sinks (RAG Knowledge Base CronJob)
```

## Security Boundary & Governance

- **Read-Only Public Surface (`DOC-011`)**: Exposes zero cluster credentials, zero internal LAN/OpenZiti endpoints, and zero private repository names (`verify_ecosystem_knowledge.py` enforces strict SHA-256 redaction).
- **Decoupled from Runtime Factory MCP**: `dark-gravity-mcp` never launches gVisor sandboxes, mutates Git repos, or accesses HashiCorp Vault (`rust_CACD_autonomous_factory/crates/factory-mcp-server` handles privileged cluster operations inside private network boundaries).
- **Epistemic Integrity**: All claims map to explicit verification states (`verified`, `implemented`, `tested`, `designed`, or `baseline_pending` / `UNMEASURED`); no third-party certification is claimed.

## Canonical Cross-Links

- [DARK_GRAVITY_MANIFEST.md](./DARK_GRAVITY_MANIFEST.md)
- [REPOSITORIES.md](./REPOSITORIES.md)
- [Global Architecture Portal](https://lgcorzo.github.io/architecture.html)
- [Unified Start-Here Portal](https://lgcorzo.github.io/start-here)
- [AI Auditor Pack](https://lgcorzo.github.io/docs/auditor/)
