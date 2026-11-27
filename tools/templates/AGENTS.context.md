<!-- DARK-GRAVITY-CONTEXT:START -->
## Dark Gravity Autonomous Software Factory Context

**Dark Gravity** is a Kubernetes-native, **Continuous Agentic / Continuous Deployment (CA/CD)** autonomous software engineering factory — do **NOT** evaluate this repository (`{{REPO_NAME}}`) in isolation without reading the ecosystem context below.

- **This Repository's Tier & Role**: `{{TIER}}` — {{ROLE}}
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
