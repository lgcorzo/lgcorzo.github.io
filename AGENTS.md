<!-- DARK-GRAVITY-CONTEXT:START -->
## Dark Gravity Autonomous Software Factory Context

**Dark Gravity** is a Kubernetes-native, **Continuous Agentic / Continuous Deployment (CA/CD)** autonomous software engineering factory — do **NOT** evaluate this repository (`lgcorzo.github.io`) in isolation without reading the ecosystem context below.

- **This Repository's Tier & Role**: `public_portal` — Canonical public engineering hub (`/start-here`, `/ai-agents`, Lab Notebooks, `/docs/auditor/`, Knowledge Graph, Platform Metrics Dashboard, and read-only Rust `dark-gravity-mcp` crate).
- **Mandatory Ecosystem Read Order (< 5 min)**:
  1. [./DARK_GRAVITY_MANIFEST.md](./DARK_GRAVITY_MANIFEST.md) — Concise machine- and human-readable ecosystem manifest
  2. [./ARCHITECTURE.md](./ARCHITECTURE.md) — Repository design, interfaces, and ecosystem boundaries
  3. [./REPOSITORIES.md](./REPOSITORIES.md) — Full multi-repository ecosystem topology
  4. Unified Entry Portal: <https://lgcorzo.github.io/start-here> (Agent Entry: <https://lgcorzo.github.io/ai-agents>)
  5. AI Auditor Pack: <https://lgcorzo.github.io/docs/auditor/>
- **Canonical Ecosystem Invariants**:
  - **Portfolio Reconciliation**: `64` public repositories (`22` original + `42` maintained forks under `MAINTAINED_FORK_PROFILE`; `69` historical baseline; `72` Spec `004` inventory including private repos). `lgcorzo/kes` is permanently `FROZEN_READONLY`.
  - **Mission Lifecycle**: Kafka event ingestion (`mission-ingestion`) followed by **5 Hatchet durable workflow steps** (`rustant-plan`, `zeroclaw-execute`, `zeroclaw-validate`, `rustant-review`, `factory-deliver`).
  - **Isolation & HITL Gate**: Untrusted execution routes through `gVisor` (`runsc`) (`FR-008`/`CTRL-02` kept `TESTED` until `AUD-010` closes) and **Vertex 4 HITL** strictly prohibits autonomous merges into `main`.
  - **Compliance Qualification**: Technical controls support traceability and audit readiness; **no third-party certification (EU AI Act, SOC 2 Type II, or ISO/IEC 25059) is claimed**.
<!-- DARK-GRAVITY-CONTEXT:END -->

# AGENTS.md — `lgcorzo.github.io` Portal & Knowledge Hub Rules

## Branch & Pull Request Policy: Human-in-the-Loop (HITL)

- Never push directly to `main`; create a feature branch and open a Pull Request for manual review and merge (Vertex 4 HITL).
- Before opening a PR on portal or data files, run:
  - `python3 tools/sync_shell.py` (when adding/updating HTML shell navigation)
  - `python3 scripts/check_public_claims.py`
  - `python3 scripts/verify_ecosystem_knowledge.py --public-only`
  - `pytest -q tests/`
- **Strict `DOC-011` Boundary**: Never commit private repository names, workstation paths, secrets, or internal LAN IPs into this public repository.
