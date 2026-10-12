The **Dark Gravity Autonomous Software Factory (V7.2 / V7.3)** is a production-grade, Rust-based **Continuous Agentic / Continuous Deployment (CA/CD)** system designed for zero-trust, air-gapped, and highly regulated enterprise environments [1, 2]. It replaces manual software engineering iteration cycles with an autonomous loop of specialized multi-agent personas governed by **Spec-Driven Development (SDD)**, **Domain-Driven Design (DDD)**, and strict hardware and cryptographic boundaries [1, 3, 4].

---

### 1. Architectural Architecture & Enterprise Software Factory Integration

The physical architecture of Dark Gravity follows a strict **Onion Architecture** across a 5-crate Cargo workspace in Rust 2024 [5-7]:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                            DARK GRAVITY WORKSPACE                           │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. factory-core        │ Domain Core (Zero I/O, pure aggregates & security) │
│ 2. factory-application │ Application Layer (Agent logic & Hatchet 6-phase DAG)│
│ 3. factory-infrastructure│ Infrastructure Adapters (Kafka, Vault, Ziti, R2R, S3)│
│ 4. factory-mcp-server  │ Interface Adapter (Axum MCP HTTP/SSE & gVisor)     │
│ 5. factory-cli         │ Entry Point (Hatchet worker & GitPlatformPoller)   │
└─────────────────────────────────────────────────────────────────────────────┘
```

* **`factory-core`**: Pure domain models (`Mission`, `Task`), aggregate roots, domain error types, and security traits (`SecurityBounds`, `SecurityValidator`) with zero external I/O [6-8].
* **`factory-application`**: Contains agent workflow logic (`Rustant`, `ZeroClaw`, `DevOpsAgent`, `DocAgent`) and Hatchet durable DAG definitions [6-8].
* **`factory-infrastructure`**: External service adapters for Apache Kafka, CloudNativePG (`pgvector`), HashiCorp Vault, R2R GraphRAG, OpenZiti, S3 storage, and Semantica-AGI [6-8].
* **`factory-mcp-server`**: Axum-based Model Context Protocol (MCP) server running on port `8100` that dispatches tool executions and launches gVisor sandboxes [6, 8, 9].
* **`factory-cli`**: The compiled entrypoint binary that wires the workspace dependencies, starts the Hatchet worker, and runs the `GitPlatformPoller` daemon [6, 8, 10].

#### Enterprise Integration Patterns

Dark Gravity integrates into enterprise software factories through three non-invasive, pull-based interfaces:

1. **Outbound Polling for Work Items (`GitPlatformPoller`)**: The `factory-cli poller` daemon periodically queries GitHub/GitLab APIs (every 30–60 seconds) for Issues or Work Items tagged with `autonomous-mission` or `dark-gravity` [11-13]. It extracts operational boundaries (e.g., `[RESOURCE_LIMIT: RAM <= 30Mi, TIMEOUT <= 300s]`), signs the mission payload with an **Ed25519 Verifiable Credential**, and publishes it to the local Kafka bus (`mission-input`) [11, 14].
2. **Interactive Pull Request Directives**: Developers interact with active Pull Requests (PRs) or Merge Requests (MRs) via comment mentions (e.g., `@darkgravity /status`, `/spec`, `/refine`, `/retry`, `/validate`) [15]. The poller acknowledges directives instantly with an "eyes" reaction (👀) and posts a single comprehensive reply upon execution completion, suppressing self-author bot loops [16, 17].
3. **GitOps Delivery & Closed-Loop Remediation**: Code changes are pushed to isolated remote feature branches, opening formal PRs/MRs linked to the originating issue (`Closes #ID`) [18, 19]. Infrastructure deployment is handled out-of-band by **FluxCD** using a pull-based reconciliation model [20, 21]. Runtime production crashes are monitored every 15 minutes by `QAObserverAgent` via **Sentry**, which maps stacktraces to source code ASTs using **R2R GraphRAG** and auto-files prioritized backlog issues [3, 22, 23].

---

### 2. Zero-Trust Security & Runtime Isolation Model

Dark Gravity enforces a **Zero-Trust** security architecture across network, kernel, process memory, and application layers [5, 24, 25]:

```
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │                       ZERO-TRUST DEFENSE IN DEPTH                           │
 ├─────────────────────────────────────────────────────────────────────────────┤
 │ • Perimeter: Zero Public Ingress Ports (Outbound Polling & OpenZiti mTLS)   │
 │ • Identity: W3C Verifiable Credentials (Ed25519 NHI) & 5-min Vault JIT Tokens│
 │ • Runtime: gVisor Kernel Isolation (RAM <= 30 MiB / CPU <= 250m)             │
 │ • Memory: Forensic Null-Byte Wipe (zeroize on drop in 54.2 ns)             │
 │ • Governance: Heterogeneous LLM SAST Judge (security_review >= 8.0/10.0)    │
 └─────────────────────────────────────────────────────────────────────────────┘
```

* **Zero Public Ingress Ports & Dark Network Overlay**: All inter-service communication across Kubernetes namespaces is encapsulated within an **OpenZiti mTLS 1.3** dark network overlay [26-28]. Host ports are completely closed, making the factory invisible to public network scans [24, 28, 29]. Outbound Kubernetes `NetworkPolicies` enforce a Deny-All default egress posture, permitting traffic solely to OpenZiti edge routers and Kafka brokers [25, 30].
* **Non-Human Identities (NHI) & W3C Verifiable Credentials**: Every autonomous agent operates as a cryptographically verifiable **Non-Human Identity (NHI)** [22, 31]. Every Git commit, database transaction, and agent-to-agent message is signed with an **Ed25519** keypair (`ed25519-dalek` v2) and wrapped in a W3C Verifiable Credential (`Ed25519Signature2020` / JWS) [28, 32-34].
* **HashiCorp Vault Just-In-Time (JIT) Credentials**: Static database passwords or Git tokens are strictly prohibited [35, 36]. `VaultSecurityBounds` issues short-lived, non-renewable JIT access tokens from isolated Vault paths (`secret/data/repos/<repo>/*`) with a strict **5-minute (300-second) TTL** [28, 32, 34].
* **gVisor User-Space Sandboxing**: All untrusted agent-generated code, compilation steps, and test suites run in ephemeral pods or Kubernetes Jobs utilizing the **gVisor (`runsc`)** user-space kernel runtime [37-39]. Sandbox containers are imperatively resource-clamped to **RAM \\(\le 30\text{ MiB}\\)** and **CPU \\(\le 250\text{m}\\)**, while sidecars are clamped to **RAM \\(\le 20\text{ MiB}\\)** and **CPU \\(\le 100\text{m}\\)** [28, 38, 40].
* **Forensic Memory Zeroization (`zeroize`)**: Credential structs implement `#[derive(Zeroize, ZeroizeOnDrop)]` [41, 42]. Upon task completion, failure, or dropping from stack/heap, secrets in RAM undergo an automated null-byte forensic overwrite [38, 41]. Criterion benchmarks measure this memory wipe at **\\(54.2\text{ ns}\\)** (\\(0.0542\,\mu\text{s}\\)), destroying credentials ~80x faster than the \\(4.33\,\mu\text{s}\\) SLA requirement [41, 43].

---

### 3. Human Control & Human-In-The-Loop (HITL) Governance

Dark Gravity replaces manual coding with an **"On-The-Loop"** supervisory model, preventing unguided AI hallucination by binding human authority to **four zero-friction governance vertices** [1, 44-46]:

```
  [ Vertex 1: Strategic Injection ] ──> Human PO creates Epic (autonomous-mission)
                 │
                 ▼
  [ Vertex 2: Sprint Mobilization ] ──> Tech Lead approves PO Agent Spec-Kit artifacts
                 │
                 ▼
  [ Vertex 3: Exception Override  ] ──> Human Architect unblocks Agent-Stuck (3-retry limit)
                 │
                 ▼
  [ Vertex 4: Categorical Scrutiny] ──> Senior Reviewer conducts final MR review & merges
```

1. **Vertex 1: Strategic Injection (Epic Creation)**: The human Product Owner creates a strategic Epic or Work Item tagged with `autonomous-mission` or `autonomous-plan` [44, 45, 47]. Agents remain completely blind to goals until this tag is explicitly applied [45].
2. **Vertex 2: Sprint Mobilization (Technical Approval)**: The PO Agent (`Rustant`) parses requirements and generates machine-verifiable **Spec-Kit** SDD artifacts (`[suspicious link removed]`, `[suspicious link removed]`, `[suspicious link removed]`, `[suspicious link removed]`) [11, 47]. A human Tech Lead reviews the plan and approves sprint mobilization, unlocking execution [44, 45, 47].
3. **Vertex 3: Exception Override (Agent-Stuck Resolution)**: If an agent task fails 3 consecutive iterations, generates duplicate diff-hash deadlocks, or breaches spend velocity limits (\\(> +\$1.00/60\text{s}\\)), the **`CircuitBreakerGuard`** trips [25, 48, 49]. The DAG freezes, JIT credentials are revoked, and the mission transitions to `Agent-Stuck`, alerting a human Architect to intervene [25, 45, 49].
4. **Vertex 4: Categorical Scrutiny (Merge Approval)**: Agents are **physically blocked from auto-merging** code into `main` or production branches [45, 47, 50]. A Senior Reviewer evaluates the generated MR for architectural coherence and business logic before clicking "Merge" [44, 45, 47].

---

### 4. Infrastructure Topology & Orchestration Engine

The production infrastructure operates within an internal Kubernetes cluster divided across 10 isolated namespaces [51, 52]:

| Namespace | Active Workloads & Platform Services |
| :--- | :--- |
| **`agents`** | `factory-worker`, `factory-mcp-server` (Axum SSE :8100), `factory-deep-research-worker` (:8200) [9]. |
| **`orchestrators`** | **Hatchet Engine** (gRPC :7077, API :8000), `keda-operator` autoscalers [53, 54]. |
| **`confluent`** | **Apache Kafka** (KRaft consensus): `mission-ingestion`, `agent-thought`, `mission-events` [54]. |
| **`storage`** | **CloudNativePG PostgreSQL 16** (`mlflow-db-rw`), **MinIO S3 Object Storage** [51, 53]. |
| **`knowledge`** | `pgvector` CNPG Cluster, `deepwiki-rs` Tree-sitter AST parser [51, 52]. |
| **`llm-apps`** | **LiteLLM Gateway** (:4000/:4001), **Semantica-AGI Engine**, **R2R GraphRAG** (:7272) [53, 55]. |
| **`security`** | **HashiCorp Vault**, Bitnami SealedSecrets, Keycloak OIDC [52]. |
| **`openziti`** | OpenZiti Controller (:8441) and Ziti Edge Routers (:3022) [52, 53]. |
| **`development`** | Ephemeral **gVisor (`runsc`)** sandbox Pods and K8s Jobs [37, 52]. |
| **`flux-system`** | **FluxCD** GitOps reconciliation controllers [52]. |

#### The Hatchet 6-Phase Durable Workflow DAG

Mission execution is governed by a crash-resilient **Hatchet 6-Phase Durable DAG** (`cacd-mission-dag`) backed by PostgreSQL state checkpoints (`BridgeState` / `StepCheckpoints`) stored in MinIO S3 (`dg-factory-checkpoints`) [5, 56-58]:

```
[ Ingestion ] ──> [ Phase 1: rustant:plan ] ──> [ Phase 2: zeroclaw:execute ]
                                                       │ (SddTaskItem Chaining)
[ Delivery ] <── [ Phase 4: rustant:review ] <── [ Phase 3: zeroclaw:validate ]
```

1. **Mission Ingestion**: Kafka `mission-ingestion` topic triggers the Hatchet DAG [54, 58].
2. **Phase 1 (`rustant:plan`)**: PO Agent (`Rustant`) queries R2R GraphRAG, executes Spec-Kit slash commands (`/speckit-*`), and produces atomic `[suspicious link removed]` items [11, 58].
3. **Phase 2 (`zeroclaw:execute`)**: Developer Agent (`ZeroClaw`) consumes `[suspicious link removed]` via `superspec`, applying surgical AST code mutations inside gVisor sandboxes using **ADK-Rust** [58-61].
4. **Phase 3 (`zeroclaw:validate`)**: Executes `cargo test` and language unit test suites inside the isolated gVisor sandbox [58, 60].
5. **Phase 4 (`rustant:review`)**: Invokes the `security_review` MCP tool (**LLM-as-a-Judge SAST** routed through LiteLLM to an independent frontier model family) [28, 58, 62]. Requires an enforced score threshold of **\\(\ge 8.0 / 10.0\\)** [28, 60, 62]. Verifies causal lineage in **Semantica-AGI** [58, 62, 63].
6. **Phase 5 (`factory:deliver`)**: Opens a formal PR/MR with linked issue references and posts an execution summary to the work item thread [19, 58, 64].

#### Predictive FinOps & Virtual Tags (Vtags)

All LLM inference calls route through the **LiteLLM Gateway**, which injects HTTP Virtual Tags (`x-vtags-team: dark-gravity-ops`, `x-vtags-epic`, `x-vtags-microservice`, `x-vtags-cost_center`) [28, 48]. `FinOpsAgent` queries spending telemetry every 60 seconds [28, 48]. If spend velocity exceeds **\\(+\$1.00 / 60\text{s}\\)**, an anomaly alert fires [28, 48]. If total spend reaches **90% of the daily budget** (\$45.00 of \$50.00 `FINOPS_MAX_DAILY_BUDGET`), a hard stop (**HardStop**) immediately freezes active DAGs, revokes JIT tokens, and emits a `budget-exceeded` event to Kafka [28, 48].

---

### 5. Compliance Frameworks & Regulatory Alignment

Dark Gravity provides native, out-of-the-box compliance alignment across major European and global regulatory standards [3, 65, 66]:

| Regulatory Framework | Mandatory Technical Requirement | Dark Gravity Implementation & Verification Evidence |
| :--- | :--- | :--- |
| **EU AI Act (Art. 12 & 14)** | Automated logging of high-risk AI events & mandatory human oversight mechanisms [66, 67]. | Real-time cognitive streaming to Kafka `agent-thought` topics [54, 68]. Causal provenance mapping in **Semantica-AGI** linking business requirements down to exact AST line mutations [62, 63]. Enforced 4-Vertex HITL governance mesh [44, 45, 47]. |
| **SOC 2 Type II** | Continuous logical access control, zero static shared secrets, and tamper-proof audit trails [66, 67, 69]. | Non-Human Identities (**NHI**) with **Ed25519 W3C Verifiable Credentials** [31-33]. HashiCorp Vault **5-minute JIT tokens** [32, 34]. Forensic memory zeroing in **\\(54.2\text{ ns}\\)** (`zeroize`) [41, 43]. |
| **ISO/IEC 25059 (SQuaRE AI Quality)** | AI system functional suitability, fault tolerance, security, and data quality [70-76]. | **Spec-Driven Development** (Spec-Kit) enforcing `[suspicious link removed]` contract compliance [71]. Crash recovery via Hatchet PostgreSQL checkpoints [72]. gVisor user-space sandboxing [73]. **Orphan Symbol Rate (OSR \\(< 5\%\\))** gate verified by `deepwiki-rs` [74, 77]. |
| **Hazitek / SPRI (R&D Grant Packaging)** | Rigorous technical audit documentation and compute telemetry for public R&D grant reimbursement [78-80]. | **`DocAgent` R&D Grant Packager**: Automatically compiles gVisor CPU/GPU compute core-hours, LiteLLM token spend, and AST code delta statistics into official SPRI/Hazitek audit reports saved to MinIO (`factory-artifacts/compliance/`) [63, 78-80]. |

---

💡 **Next Steps**: If you would like to inspect the live verification scorecard for a specific module, review the C4 architecture diagrams, or simulate a canary mission dispatch using `factory-cli`, let me know!