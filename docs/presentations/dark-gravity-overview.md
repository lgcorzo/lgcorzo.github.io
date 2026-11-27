# Dark Gravity Autonomous Software Factory — Executive Technical Walkthrough

**Portal**: <https://lgcorzo.github.io/start-here> · **AI Agents**: <https://lgcorzo.github.io/ai-agents> · **Auditor Pack**: <https://lgcorzo.github.io/docs/auditor/>

## Slide 1 — Why Dark Gravity Exists
Dark Gravity is an experimental Continuous Agentic / Continuous Deployment (`CA/CD`) research laboratory built in **Rust Edition 2024** and **Kubernetes**. It studies how autonomous coding agents can translate labeled GitHub issues into verified Pull Requests inside deterministic sandboxes while preserving **Vertex 4 Human-in-the-Loop (HITL)** merge control.

## Slide 2 — Ecosystem Topology (`64` Public = `22` Original + `42` Forks)
- **Orchestrator & Core**: `rust_CACD_autonomous_factory` (`5`-crate Onion architecture).
- **Contract Bridge**: `speckit-superpowers-bridge` uniting Spec-Kit (`WHAT`) and Superpowers (`HOW`).
- **Sovereign AI & Knowledge Layer**: `dark-litellm`, `deepwiki-rs` (`OSR < 5%`), `semantica`, `R2R-Engine`.
- **Canonical Hub & MCP**: `lgcorzo.github.io` (Portal, Knowledge Graph, Metrics Dashboard, Read-Only Rust `dark-gravity-mcp`).
- **Private Control Plane (`DOC-011`)**: `Internal GitOps Control Plane` and `Internal Incident Remediation Service`.

## Slide 3 — Mission Flow (Kafka + 5 Hatchet Steps + Vertex 4 HITL)
1. `GitPlatformPoller` signs labeled issues (Ed25519) -> Kafka `mission-input` topic.
2. **Step 1 `rustant-plan`**: R2R GraphRAG lookup + Spec-Kit planning.
3. **Step 2 `zeroclaw-execute`**: Isolated `gVisor (runsc)` sandbox jobs (`30Mi`/`250m` micro or `512Mi`/`500m` compile) + parallel Swarm lanes (`fan-in-synthesize`).
4. **Step 3 `zeroclaw-validate`**: Deterministic `cargo test`, `clippy`, `pytest`, `ruff`.
5. **Step 4 `rustant-review`**: Independent LLM SAST judge (`>= 8.0 / 10.0`) + Semantica provenance.
6. **Step 5 `factory-deliver`**: Opens Pull Request for **Vertex 4 human review & merge** (autonomous merge to `main` is strictly forbidden).
