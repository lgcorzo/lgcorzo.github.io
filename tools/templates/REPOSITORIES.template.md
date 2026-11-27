# Dark Gravity Ecosystem Repository Map

Dark Gravity is a unified **Continuous Agentic / Continuous Deployment (CA/CD)** Autonomous Software Factory — not a collection of unrelated standalone repositories.

## Canonical Topology

```text
Dark Gravity Autonomous Software Factory
│
├── Core Control Plane & Orchestration
│   ├── rust_CACD_autonomous_factory   # Core 5-crate Rust 2024 orchestrator, AgentWorkspace CRD, Hatchet DAG & runtime MCP
│   ├── speckit-superpowers-bridge     # Spec-Kit (WHAT) <-> Superpowers (HOW) handoff contract & boundary guard
│   ├── Internal GitOps Control Plane  # Pull-based FluxCD v2 cluster reconciler, SealedSecrets, OpenZiti & NetworkPolicies
│   └── Internal Incident Remediation  # FluxCD alert classifier, MLflow tracker & autonomous patch synthesizer
│
├── Public Knowledge Hub & Agent Entry
│   ├── lgcorzo.github.io              # /start-here, /ai-agents, RESEARCH.md, EXPERIMENTS.md, /docs/auditor/, KG, Metrics & dark-gravity-mcp (Rust)
│   └── lgcorzo                        # GitHub Profile entry point routing reviewers & agents to the ecosystem
│
├── Owned Applications & Domain Standards
│   ├── mlops-python-package           # Enterprise MLOps standard (DVC, MLflow, Hydra, SHAP, CycloneDX, OpenWiki)
│   ├── llmops-python-package          # ISO 42010/15289 LLMOps platform (Hatchet DSL, MCP registry, OpenWiki)
│   └── fastapi-autogen-team           # High-throughput Rust (Axum + Rig) streaming SSE multi-agent squad service
│
└── Maintained Sovereign Infrastructure Forks (42 forks under MAINTAINED_FORK_PROFILE)
    ├── R2R-Engine / R2R-Application   # Hybrid pgvector + Leiden GraphRAG corporate memory
    ├── dark-litellm                   # Sovereign LLM router & FinOps X-Vtag priority policy gateway
    ├── deepwiki-rs                    # Tree-sitter Rust AST analyzer & Orphan Symbol Rate (OSR < 5%) verifier
    ├── semantica                      # Causal provenance graph & conflict detection engine
    ├── spec-kit / superpowers         # Spec-Driven Development & execution discipline upstreams
    └── MinIO S3 & SIMD Stack          # 38 Go/S3/KMS/SIMD sovereign forks (lgcorzo/kes archived FROZEN_READONLY)
```

## Canonical Portfolio Statistics (`data/canonical-claims.json`)

- **Public Baseline**: `64` public GitHub repositories = `22` original + `42` maintained forks (`5` categories: `4` agent/spec tooling, `5` memory/docs/gateway, `10` storage platform, `17` Go libraries, `6` experiments/learning).
- **Historical Baseline**: `69` repositories including `5` historical private/archived repos.
- **Spec 004 Ecosystem Audit**: `72` total repositories (`66` public + `6` private).
- **Fork Governance (`MAINTAINED_FORK_PROFILE`)**: Preserves upstream directory layouts, omits `upstream` remotes, retains original `LICENSE`, routes vulnerabilities to GitHub Private Security Advisories, prefixes agent commits `[agent]`, and keeps `lgcorzo/kes` permanently `FROZEN_READONLY`.
