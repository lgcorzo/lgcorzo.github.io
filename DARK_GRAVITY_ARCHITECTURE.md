# Dark Gravity Autonomous Software Factory — Architecture & Governance Reference

The **Dark Gravity Autonomous Software Factory (`V7.2 / V7.3`)** is a Rust-based **Continuous Agentic / Continuous Deployment (CA/CD)** engineering platform designed for zero-trust, air-gapped, and security-critical environments [1, 2]. It coordinates specialized multi-agent personas through **Spec-Driven Development (SDD)**, **Domain-Driven Design (DDD)**, and strict cryptographic, kernel, and human-in-the-loop (HITL) boundaries [1, 3, 4].

---

### 0. Actual Operational Status Matrix (`Implemented` vs. `Deployed` vs. `Designed`)

To avoid conflating architectural targets with live cluster state, Dark Gravity tracks all subsystems across four explicit verification states aligned with [`rust_CACD_autonomous_factory/README.md`](https://github.com/lgcorzo/rust_CACD_autonomous_factory) and its machine-readable evidence ledger (`evidence/verified_status.json`):

| Lifecycle State | Meaning | Subsystems & Current Verification Evidence |
| :--- | :--- | :--- |
| **`Implemented` & `Verified` (Rust Workspace)** | Compiled, unit-tested, and benchmarked inside the 5-crate Rust 2024 workspace (`rustc 1.85+`, verified on `1.97.1`). | • **5-Crate Onion Workspace**: `factory-core`, `factory-application`, `factory-infrastructure`, `factory-mcp-server`, `factory-cli` (`cargo clippy --all-targets -- -D warnings`, `cargo test --workspace`).<br/>• **Cryptographic Non-Human Identities (NHI)**: Ed25519 signing (`ed25519-dalek` v2) and W3C Verifiable Credential (`Ed25519Signature2020`) envelopes.<br/>• **Forensic Memory Zeroization**: `#[derive(Zeroize, ZeroizeOnDrop)]` on credential carriers, micro-benchmarked via Criterion at **`54.2 ns`** (`0.0542 µs`).<br/>• **Governance & Safety Guards**: `CircuitBreakerGuard` (3-retry cap, diff-hash loop detection, FinOps velocity limits) and 4-Vertex HITL state transitions.<br/>• **GitPlatformPoller & PR Directives**: Outbound polling and `@darkgravity /status`, `/interact`, `/refine`, `/validate` command parsing. |
| **`Deployed` (Kubernetes Cluster & CI/CD)** | Provisioned and reconciled via FluxCD GitOps across the 10-namespace Kubernetes topology or running as scheduled GitHub/cluster pipelines. | • **10-Namespace Kubernetes Topology**: `agents`, `orchestrators`, `confluent`, `storage`, `knowledge`, `llm-apps`, `security`, `openziti`, `development`, and `flux-system`.<br/>• **Event & Orchestration Backbone**: Hatchet Engine (`:7077` / `:8000`) and Apache Kafka (KRaft consensus) topics (`mission-ingestion`, `agent-thought`, `mission-events`).<br/>• **Sovereign Data & Storage Plane**: CloudNativePG PostgreSQL 16 (`pgvector`) and decoupled `@lgcorzo` MinIO S3 (`ghcr.io/lgcorzo/operator:v7.1.1-lgcorzo.3`, `ghcr.io/lgcorzo/minio:v0.1.0-lgcorzo.2`, `ghcr.io/lgcorzo/mc:v0.1.1-lgcorzo.2`).<br/>• **Cognitive & LLM Plane**: `dark-litellm` proxy (`:4000/:4001`), `R2R-Engine` GraphRAG (`:7272`), and `semantica` knowledge graph memory.<br/>• **Autonomous Vulnerability & Jules Remediation Pipeline**: Hourly scanner (`monitor_pipeline.py`) tracking Dependabot & CodeQL alerts in **GitHub Project 6**, dispatching `@jules` fixes, and enforcing CI verification across all 67 active repositories. |
| **`Designed` / In Validation** | Contracts, adapters, and manifests are implemented; full multi-node production chaos testing or external third-party audits remain in validation. | • **End-to-End Chaos & Failover Drills**: Live saturation and multi-node fault-injection across gVisor sandboxes and OpenZiti routers.<br/>• **Regulatory Readiness (EU AI Act, SOC 2 Type II, ISO/IEC 25059)**: The architecture implements the technical controls (audit trails, HITL gates, NHI signing, SDD traceability) for **regulatory readiness and architectural alignment**; it does not claim formal third-party certification.<br/>• **Automated Hazitek / SPRI Grant Packager (`DocAgent`)**: End-to-end telemetry export from live cluster runs into MinIO compliance buckets. |

---

### 1. Workspace Architecture & Enterprise Software Factory Integration

The physical architecture of Dark Gravity follows a strict **Onion Architecture** across a 5-crate Cargo workspace in **Rust Edition 2024** (`rust-version = "1.85"`) [5–7]:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                            DARK GRAVITY WORKSPACE                           │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. factory-core          │ Domain Core (Zero I/O, pure aggregates & security)│
│ 2. factory-application   │ Application Layer (Agent logic & Hatchet 6-phase) │
│ 3. factory-infrastructure│ Infrastructure Adapters (Kafka, Vault, Ziti, R2R) │
│ 4. factory-mcp-server    │ Interface Adapter (Axum MCP HTTP/SSE & gVisor)    │
│ 5. factory-cli           │ Entry Point (Hatchet worker & GitPlatformPoller)  │
└─────────────────────────────────────────────────────────────────────────────┘
```

* **`factory-core`**: Pure domain models (`Mission`, `Task`), aggregate roots, domain error types, and security traits (`SecurityBounds`, `SecurityValidator`) with zero external I/O [6–8].
* **`factory-application`**: Contains agent workflow logic (`Rustant`, `ZeroClaw`, `DevOpsAgent`, `DocAgent`) and Hatchet durable DAG definitions [6–8].
* **`factory-infrastructure`**: External service adapters for Apache Kafka, CloudNativePG (`pgvector`), HashiCorp Vault, R2R GraphRAG, OpenZiti, S3 storage, and Semantica-AGI [6–8].
* **`factory-mcp-server`**: Axum-based Model Context Protocol (MCP) server running on port `8100` that dispatches tool executions and launches gVisor sandboxes [6, 8, 9].
* **`factory-cli`**: The compiled entrypoint binary that wires the workspace dependencies, starts the Hatchet worker, and runs the `GitPlatformPoller` daemon [6, 8, 10].

#### Enterprise Integration Patterns

Dark Gravity integrates into enterprise software factories through three non-invasive, pull-based interfaces:

1. **Outbound Polling for Work Items (`GitPlatformPoller`)**: The `factory-cli poller` daemon periodically queries GitHub/GitLab APIs (every 30–60 seconds) for Issues or Work Items tagged with `autonomous-mission` or `dark-gravity` [11–13]. It extracts operational boundaries (e.g., `Resource limits: CPU: 500m, RAM: 512Mi, Timeout: 300s` or sandbox clamps `RAM <= 30Mi`), signs the mission payload with an **Ed25519 Verifiable Credential**, and publishes it to the local Kafka bus (`mission-input`) [11, 14].
2. **Interactive Pull Request Directives**: Developers interact with active Pull Requests (PRs) or Merge Requests (MRs) via comment mentions (e.g., `@darkgravity /status`, `/interact`, `/refine`, `/validate`) [15]. The poller acknowledges directives with an "eyes" reaction (👀) and posts a structured reply upon execution completion, suppressing self-author bot loops [16, 17].
3. **GitOps Delivery & Closed-Loop Remediation**: Code changes are pushed to isolated remote feature branches, opening formal PRs/MRs linked to the originating issue (`Closes #ID`) [18, 19]. Infrastructure deployment is handled out-of-band by **FluxCD** using a pull-based reconciliation model [20, 21], while cluster and repository alerts are continuously remediated via `Jules_remediator` and the **GitHub Project 6** vulnerability pipeline [3, 22, 23].

---

### 2. Zero-Trust Security & Runtime Isolation Model

Dark Gravity enforces a **Zero-Trust** security architecture across network, kernel, process memory, and application layers [5, 24, 25]:

```text
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │                       ZERO-TRUST DEFENSE IN DEPTH                           │
 ├─────────────────────────────────────────────────────────────────────────────┤
 │ • Perimeter: Zero Public Ingress Ports (Outbound Polling & OpenZiti mTLS)   │
 │ • Identity: W3C Verifiable Credentials (Ed25519 NHI) & 5-min Vault JIT Tokens│
 │ • Runtime: gVisor Kernel Isolation (Container Clamps & Ephemeral K8s Jobs)  │
 │ • Memory: Forensic Null-Byte Wipe (zeroize on drop; 54.2 ns micro-benchmark)│
 │ • Governance: Heterogeneous LLM SAST Judge (security_review >= 8.0/10.0)    │
 └─────────────────────────────────────────────────────────────────────────────┘
```

* **Zero Public Ingress Ports & Dark Network Overlay**: Inter-service communication across Kubernetes namespaces is encapsulated within an **OpenZiti mTLS 1.3** dark network overlay [26–28]. Host ingress ports remain closed to public scans [24, 28, 29], and Kubernetes `NetworkPolicies` (Cilium/Calico CNI) enforce a default-deny egress posture, permitting traffic only to authorized OpenZiti routers and Kafka brokers [25, 30].
* **Non-Human Identities (NHI) & W3C Verifiable Credentials**: Every autonomous agent operates as a cryptographically verifiable **Non-Human Identity (NHI)** [22, 31]. Agent-authored commits, database transactions, and inter-agent messages are signed with an **Ed25519** keypair (`ed25519-dalek` v2) and wrapped in a W3C Verifiable Credential (`Ed25519Signature2020` / JWS) [28, 32–34].
* **HashiCorp Vault Just-In-Time (JIT) Credentials**: Static long-lived secrets are replaced by `VaultSecurityBounds`, which issues short-lived, non-renewable JIT access tokens from isolated Vault paths (`secret/data/repos/<repo>/*`) with a **5-minute (300-second) TTL** [28, 32, 34].
* **gVisor User-Space Sandboxing**: Untrusted agent-generated code, compilation steps, and test suites execute inside ephemeral pods or Kubernetes Jobs utilizing the **gVisor (`runsc`)** user-space kernel runtime [37–39], with strict container resource quotas enforced per workload profile [28, 38, 40].
* **Forensic Memory Zeroization (`zeroize`)**: Credential structs implement `#[derive(Zeroize, ZeroizeOnDrop)]` [41, 42]. Upon task completion or drop from stack/heap, secrets in RAM undergo an automated null-byte overwrite [38, 41]. Criterion micro-benchmarks measure this wipe at **`54.2 ns`** (`0.0542 µs`), well within the `4.33 µs` design budget [41, 43].

---

### 3. Human Control & Human-In-The-Loop (HITL) Governance

Dark Gravity operates on an **"On-The-Loop" / Human-in-the-Loop (HITL)** supervisory model, binding human authority to **four governance vertices** [1, 44–46]:

```text
  [ Vertex 1: Strategic Injection ] ──> Human PO creates Epic (autonomous-mission)
                 │
                 ▼
  [ Vertex 2: Sprint Mobilization ] ──> Tech Lead approves PO Agent Spec-Kit artifacts
                 │
                 ▼
  [ Vertex 3: Exception Override  ] ──> Human Architect unblocks Agent-Stuck (3-retry limit)
                 │
                 ▼
  [ Vertex 4: Categorical Scrutiny] ──> Senior Reviewer conducts final PR/MR review & merges
```

1. **Vertex 1: Strategic Injection (Epic Creation)**: The human Product Owner creates a strategic Epic or Work Item tagged with `autonomous-mission` or `dark-gravity` [44, 45, 47]. Agents do not self-initiate unrequested features [45].
2. **Vertex 2: Sprint Mobilization (Technical Approval)**: The PO Agent (`Rustant`) parses requirements and generates machine-verifiable **Spec-Kit** SDD artifacts (`constitution.md`, `spec.md`, `plan.md`, `tasks.md`) [11, 47]. A human Tech Lead reviews the specification and approves mobilization before execution begins [44, 45, 47].
3. **Vertex 3: Exception Override (Agent-Stuck Resolution)**: If an agent task fails 3 consecutive iterations, produces duplicate diff-hash deadlocks, or breaches spend velocity limits (`> +$1.00 / 60s`), the **`CircuitBreakerGuard`** trips [25, 48, 49]. The DAG pauses, JIT credentials are revoked, and the mission transitions to `Agent-Stuck`, alerting a human Architect [25, 45, 49].
4. **Vertex 4: Categorical Scrutiny (Merge Approval)**: On HITL-governed repositories (`rust_CACD_autonomous_factory`, `fastapi-autogen-team`, `mlops-python-package`), agents are **prohibited from auto-merging** into `main` [45, 47, 50]. Once all CI/CD pipelines, linters, and CodeQL checks are green, the agent presents the PR link and verification evidence for manual human review and merge [44, 45, 47].

---

### 4. Strategic Forking of Principal Open-Source Projects & Code Quality Governance

A defining architectural principle of the `@lgcorzo` lab is that **principal open-source dependencies required by the autonomous factory are forked and maintained under our own strict code quality, security, and release governance** (41 forked repositories out of 71 total).

#### Why We Fork Principal Projects
Autonomous software factories cannot depend on unpinned upstream rolling branches without inheriting systemic fragility:
* **Protocol & Schema Determinism (SDD & Agent Skills)**: The factory's planning and execution loop depends on exact contract compatibility between [`lgcorzo/spec-kit`](https://github.com/lgcorzo/spec-kit) (WHAT: `constitution.md` → `spec.md` → `plan.md` → `tasks.md`), [`lgcorzo/superpowers`](https://github.com/lgcorzo/superpowers) (HOW: TDD, git worktrees, subagent dispatch, code review), and [`lgcorzo/speckit-superpowers-bridge`](https://github.com/lgcorzo/speckit-superpowers-bridge) (handoff state machine & guard rules). Forking guarantees that upstream CLI changes or skill rewrites never break the factory's handoff contract without passing our smoke tests.
* **Proactive Vulnerability Remediation in AI/RAG Stacks**: Upstream AI repositories ([`semantica`](https://github.com/lgcorzo/semantica), [`dark-litellm`](https://github.com/lgcorzo/dark-litellm), [`deepwiki-rs`](https://github.com/lgcorzo/deepwiki-rs), [`adk-rust`](https://github.com/lgcorzo/adk-rust), [`CodeWiki`](https://github.com/lgcorzo/CodeWiki), [`openwiki`](https://github.com/lgcorzo/openwiki), [`deepwiki-open`](https://github.com/lgcorzo/deepwiki-open), [`openevolve`](https://github.com/lgcorzo/openevolve), [`TradingAgents`](https://github.com/lgcorzo/TradingAgents), [`FinRobot`](https://github.com/lgcorzo/FinRobot)) frequently accumulate transitive CVEs in Python (`aiohttp`, `cryptography`, `authlib`, `pygments`, `pytest`), Rust (`rand`, `rustls`), or Node.js (`next`, `undici`, `axios`, `lodash`). Maintaining our own forks allows immediate security patching and lockfile pinning.
* **Sovereign Infrastructure & Licensing Stability**: The 38 decoupled MinIO storage, KMS (`kes`), NVMe CSI (`directpv`), and SIMD cryptography (`sha256-simd`, `blake2b-simd`, `simdjson-go`, `crc64nvme`) repositories insulate the cluster from upstream distribution removals and external container registries (`quay.io`, `docker.io`).

#### Code Quality & Security Rules Enforced Across Maintained Forks
1. **Language-Specific Linting & Test Matrices**:
   * **Rust**: `cargo clippy --all-targets -- -D warnings`, `rustfmt --check`, and `cargo test --workspace`.
   * **Python**: `ruff` lint/format checks, static type checking (`mypy`), and multi-OS/multi-version `pytest` suites (up to Python 3.13/3.14).
   * **Shell / SDD Bridges**: `shellcheck`, `markdownlint`, extension version guards, and end-to-end bash/PowerShell bridge smoke suites.
2. **Cryptographic Dependency Locking & Audit Gates**:
   * Every Python and Node project enforces deterministic lockfiles (`poetry.lock`, `uv.lock`, `package-lock.json` `overrides`) or SHA-256 hash-pinned `security-audit-requirements.txt` verified via `pip-audit`, `cargo audit`, and GitHub Dependency Review.
3. **Custom CodeQL & Hourly Autonomous Remediation (Project 6)**:
   * Repositories enforce dedicated `.github/workflows/codeql.yml` static analysis (with conflicting GitHub Default Setup explicitly disabled where custom workflows govern Python/Actions/Rust scanning).
   * An hourly autonomous vulnerability monitor (`monitor_pipeline.py`) scans all active repositories for Dependabot and CodeQL alerts, creates root-cause tracking issues in **GitHub Project 6**, dispatches **Jules** remediation PRs, posts failure diagnostics to conserve tokens, and auto-merges verified dependency fixes on non-HITL repos while respecting human merge gates on core factory repos.
4. **AST-Synchronized Living Documentation (OpenWiki & OKF)**:
   * Core repositories maintain automated **OpenWiki** (`openwiki/quickstart.md`) and **ISO/IEC/IEEE 42010 / 15289 OKF** documentation generated from source ASTs (`deepwiki-rs`, `ast-okf-documenter`) rather than hand-edited prose.

---

### 5. Infrastructure Topology & Orchestration Engine

The cluster infrastructure is organized across 10 isolated Kubernetes namespaces [51, 52]:

| Namespace | Active Workloads & Platform Services |
| :--- | :--- |
| **`agents`** | `factory-worker`, `factory-mcp-server` (Axum SSE `:8100`), `factory-deep-research-worker` (`:8200`) [9]. |
| **`orchestrators`** | **Hatchet Engine** (gRPC `:7077`, API `:8000`), `keda-operator` autoscalers [53, 54]. |
| **`confluent`** | **Apache Kafka** (KRaft consensus): `mission-ingestion`, `agent-thought`, `mission-events` [54]. |
| **`storage`** | **CloudNativePG PostgreSQL 16** (`mlflow-db-rw`), **Sovereign MinIO S3 Object Storage** (`ghcr.io/lgcorzo/*`) [51, 53]. |
| **`knowledge`** | `pgvector` CNPG Cluster, `deepwiki-rs` Tree-sitter AST parser [51, 52]. |
| **`llm-apps`** | **Dark-LiteLLM Gateway** (`:4000/:4001`), **Semantica-AGI Engine**, **R2R GraphRAG** (`:7272`) [53, 55]. |
| **`security`** | **HashiCorp Vault**, Bitnami SealedSecrets, Keycloak OIDC [52]. |
| **`openziti`** | OpenZiti Controller (`:8441`) and Ziti Edge Routers (`:3022`) [52, 53]. |
| **`development`** | Ephemeral **gVisor (`runsc`)** sandbox Pods and K8s Jobs [37, 52]. |
| **`flux-system`** | **FluxCD** GitOps reconciliation controllers [52]. |

#### The Hatchet 6-Phase Durable Workflow DAG

Mission execution is governed by a crash-resilient **Hatchet 6-Phase Durable DAG** (`cacd-mission-dag`) backed by PostgreSQL state checkpoints (`BridgeState` / `StepCheckpoints`) stored in MinIO S3 (`dg-factory-checkpoints`) [5, 56–58]:

```text
[ Ingestion ] ──> [ Phase 1: rustant:plan ] ──> [ Phase 2: zeroclaw:execute ]
                                                       │ (SddTaskItem Chaining)
[ Delivery ] <── [ Phase 4: rustant:review ] <── [ Phase 3: zeroclaw:validate ]
```

1. **Mission Ingestion**: Kafka `mission-ingestion` topic triggers the Hatchet DAG [54, 58].
2. **Phase 1 (`rustant:plan`)**: PO Agent (`Rustant`) queries R2R GraphRAG, executes Spec-Kit slash commands (`/speckit-*`), and produces atomic `tasks.md` items (`constitution.md` → `spec.md` → `plan.md` → `tasks.md`) [11, 58].
3. **Phase 2 (`zeroclaw:execute`)**: Developer Agent (`ZeroClaw`) consumes `tasks.md` via the `speckit-superpowers-bridge`, applying surgical AST code mutations inside gVisor sandboxes using **ADK-Rust** [58–61].
4. **Phase 3 (`zeroclaw:validate`)**: Executes `cargo test`, `clippy`, `pytest`, or `ruff` suites inside the isolated gVisor sandbox [58, 60].
5. **Phase 4 (`rustant:review`)**: Invokes the `security_review` MCP tool (**LLM-as-a-Judge SAST** routed through `dark-litellm` to an independent frontier model family) [28, 58, 62]. Requires an enforced score threshold of **`>= 8.0 / 10.0`** and records causal lineage in **Semantica** [28, 60, 62, 63].
6. **Phase 5 (`factory:deliver`)**: Opens a formal PR/MR with linked issue references (`Closes #ID`) and posts an execution summary to the work item thread for human review [19, 58, 64].

#### Predictive FinOps & Virtual Tags (Vtags)

All LLM inference calls route through the **`dark-litellm` Gateway**, which injects HTTP Virtual Tags (`x-vtags-team: dark-gravity-ops`, `x-vtags-epic`, `x-vtags-microservice`, `x-vtags-cost_center`) [28, 48]. `FinOpsAgent` monitors spending telemetry every 60 seconds [28, 48]. If spend velocity exceeds **`+$1.00 / 60s`**, an anomaly alert fires; if total spend reaches **90% of the daily budget** (`$45.00` of `$50.00` `FINOPS_MAX_DAILY_BUDGET`), a **HardStop** pauses active DAGs, revokes JIT tokens, and emits a `budget-exceeded` event to Kafka [28, 48].

---

### 6. Regulatory Readiness & Architectural Alignment

Dark Gravity is architected to provide verifiable technical controls aligned with major European and global engineering standards *(note: these controls represent technical readiness and architectural alignment, not formal third-party regulatory certification)* [3, 65, 66]:

| Regulatory / Quality Framework | Target Technical Requirement | Dark Gravity Architectural Control & Evidence |
| :--- | :--- | :--- |
| **EU AI Act (Art. 12 & 14 Readiness)** | Automated logging of high-risk AI events & mandatory human oversight mechanisms [66, 67]. | Real-time cognitive streaming to Kafka `agent-thought` topics [54, 68]. Causal provenance mapping in **Semantica** linking requirements to AST mutations [62, 63]. Enforced 4-Vertex HITL governance mesh blocking autonomous merges to `main` [44, 45, 47]. |
| **SOC 2 Type II (Control Readiness)** | Logical access control, elimination of static shared secrets, and tamper-evident audit trails [66, 67, 69]. | Non-Human Identities (**NHI**) with **Ed25519 W3C Verifiable Credentials** [31–33]. HashiCorp Vault **5-minute JIT tokens** [32, 34]. Forensic memory zeroing (`zeroize`, micro-benchmarked at `54.2 ns`) [41, 43]. |
| **ISO/IEC 25059 & ISO/IEC/IEEE 42010** | AI system functional suitability, fault tolerance, security, and architecture description coherence [70–76]. | **Spec-Driven Development** (`spec-kit` + `speckit-superpowers-bridge`) enforcing `tasks.md` contract compliance [71]. Crash recovery via Hatchet PostgreSQL checkpoints [72]. **Orphan Symbol Rate (`OSR < 5%`)** and AST documentation verified via `deepwiki-rs` and OpenWiki [74, 77]. |
| **Hazitek / SPRI (R&D Telemetry Design)** | Technical audit documentation and compute telemetry for R&D project tracking [78–80]. | **`DocAgent` R&D Packager (Designed)**: Aggregates sandbox compute core-hours, LiteLLM token spend, and AST code delta statistics into structured audit reports in MinIO (`factory-artifacts/compliance/`) [63, 78–80]. |
