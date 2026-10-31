# Dark Gravity & Lab Fact List (Rule 1 & Rule 2 Evidence Ledger)

This fact list serves as the canonical source of truth for the `lgcorzo.github.io` portfolio refactor. Every statement and claim on the site is verified against the repositories below.

---

## 1. Core Architecture, Crate Topology & Language Standards
- **5-Crate Onion Architecture**:
  - `factory-core`: Pure domain model, zero external I/O, security traits (`SecurityBounds`, `SecurityValidator`).
  - `factory-application`: Workflow coordination (`Rustant`, `ZeroClaw`, `DevOpsAgent`, `DocAgent`), Hatchet durable DAG definitions.
  - `factory-infrastructure`: Adapters for Apache Kafka, CloudNativePG (`pgvector`), HashiCorp Vault, R2R GraphRAG, OpenZiti, S3 storage, Semantica.
  - `factory-mcp-server`: Axum-based MCP HTTP/SSE server (port 8100), tool dispatching, gVisor sandbox launcher.
  - `factory-cli`: Entry point binary, Hatchet mission worker runner, GitPlatformPoller daemon, ADR-008 CRD operator controller.
  - *Source Path*: `rust_CACD_autonomous_factory/Cargo.toml`, `rust_CACD_autonomous_factory/README.md`, `wiki/architecture/strategic_design.md`.
- **Rust Edition & Compiler**:
  - Rust Edition 2024, `rust-version = "1.85"`.
  - *Source Path*: `rust_CACD_autonomous_factory/Cargo.toml:4`.
- **Release Version**:
  - Tagged `v0.2.8` (latest release tag).
  - *Source Path*: `git describe --tags` -> `v0.2.8`, `git tag --list`.

---

## 2. Kubernetes Topology & Isolation Standards (ADR-008 v3.1)
- **Namespaces**:
  - Operational namespaces in baseline and GitOps: `agents`, `orchestrators`, `jules-remediator`, `ml-apps`, `dark-gravity`, `sandbox-exec`, `development`, `storage`, `security`, `openziti`, `flux-system`, `confluent`, `container-registry`.
  - Actual live MicroK8s cluster namespaces: 21 namespaces total, including active functional namespaces `agents`, `orchestrators`, `development`, `jules-remediator`, `ml-apps`, `storage`, `security`, `openziti`, `flux-system`, `confluent`.
  - *Source Path*: `evidence/baseline.md:13-14`, `deploy/policies/validating-admission-policies.yaml`, `specs/008-crd-workspace-standard/plan.md`.
- **Sandbox Technology**:
  - Micro-sandboxing uses **gVisor (`runsc`)** user-space kernel Sentry emulation (`RuntimeClass=gvisor`).
  - Firecracker microVMs were researched and evaluated as viable, but gVisor is the deployed choice for lightweight ~150ms startup latency and native CNI/CRI integration.
  - *Source Path*: `deploy/crds/agentworkspaces.darkgravity.io.yaml`, `specs/004-crypto-security-hardening/research.md`, `evidence/baseline.md:96`, `evidence/security/threat-model.md`.
- **Sandbox Resource Bounds (ADR-008 & Baseline)**:
  - ValidatingAdmissionPolicy `dg-sandbox-bounds-jobs` and `dg-sandbox-bounds-pods` enforce strict clamping in `development` and `sandbox-exec`:
    - Memory limit: `<= 30Mi`
    - CPU limit: `<= 250m`
    - Requests: must declare both `cpu` and `memory`, where requests <= limits.
    - Ephemeral containers: forbidden.
    - Privilege escalation: forbidden (`allowPrivilegeEscalation: false`, `capabilities: drop ["ALL"]`, `readOnlyRootFilesystem: true`).
  - *Source Path*: `deploy/policies/validating-admission-policies.yaml:35-43`, `evidence/baseline.md:15`, `specs/008-crd-workspace-standard/contracts/validating-admission-policies.yaml`.

---

## 3. Orchestration, Messaging & Messaging Topics
- **Workflow Engine**:
  - **Hatchet 6-Phase Durable DAG** (`cacd-mission-dag`):
    - `rustant:plan` -> PO agent produces atomic SDD tasks.
    - `zeroclaw:execute` -> Developer agent executes code changes.
    - `zeroclaw:validate` -> Runs tests and linters in gVisor.
    - `rustant:review` -> LLM-as-a-Judge SAST security evaluation (score >= 8.0/10.0).
    - `factory:deliver` -> Opens formal PR/MR with linked issues (`Closes #ID`).
  - Execution timeout: 30 minutes (1800s) across DAG tasks.
  - State checkpoints: PostgreSQL backed, MinIO S3 checkpoints (`/tmp/checkpoints` / S3).
  - *Source Path*: `crates/factory-application/src/workflows/autonomous_mission.rs`, `crates/factory-mcp-server/src/tools/bridge.rs`, PR #550 commit `490cef7f`.
- **Kafka Topics**:
  - `mission-input`: Core mission intake topic consumed by Hatchet workers and KEDA ScaledObjects.
  - `mission-ingestion`: Intake and intention injection topic used by tests and CLI tools.
  - `agent-thought`: Real-time cognitive streaming topic for agent thoughts.
  - `mission-events` / `mission-artifact`: Event telemetry and build artifacts.
  - *Source Path*: `crates/factory-infrastructure/src/kafka.rs`, `crates/factory-mcp-server/src/tools/inspect_kafka_topic.rs`, `evidence/baseline.md:79-80`, `specs/005-pipeline-error-remediation/spec.md:131`.

---

## 4. Security, Cryptography & Non-Human Identity (NHI)
- **Cryptographic NHI**:
  - Ed25519 asymmetric keypairs (`ed25519-dalek` v2) generating W3C Verifiable Credential envelopes (`Ed25519Signature2020`).
  - *Source Path*: `crates/factory-core/src/security_nhi.rs`, `evidence/security-tests.md`.
- **Zero-Trust Network**:
  - OpenZiti overlay network providing dark services with mTLS and no open inbound listening ports.
  - HashiCorp Vault JIT tokens with 5-minute TTL.
  - *Source Path*: `crates/factory-infrastructure/src/ziti.rs`, `crates/factory-infrastructure/src/vault.rs`, `evidence/baseline.md:95`.
- **Forensic Memory Zeroization**:
  - `#[derive(Zeroize, ZeroizeOnDrop)]` on credential carriers and tokens.
  - Micro-benchmarked via Criterion at **54.2 ns** (0.0542 µs).
  - *Source Path*: `benches/memory_zeroize_bench.rs`, `crates/factory-core/src/security.rs`, `evidence/baseline.md`.
- **Human-in-the-Loop (HITL) Policy**:
  - Strict human review required before merging any PR or MR to `main`. Autonomous agents cannot merge to default branches.
  - *Source Path*: `AGENTS.md:13-17`, `wiki/security/hitl_governance.md`.

---

## 5. FinOps & Budget Controls
- **LiteLLM Gateway Virtual Tags (Vtags)**:
  - Injected headers: `x-vtags-team: dark-gravity-ops`, `x-vtags-epic: E6.3`, `x-vtags-microservice`, `x-vtags-cost_center: eu-rd-grants`.
  - *Source Path*: `crates/factory-application/src/agents/finops.rs:25-30`.
- **Spend Anomaly & HardStop Thresholds**:
  - Velocity Anomaly: Alert triggered when spend velocity exceeds **+$1.00 / 60 seconds** (`raw_delta / elapsed_minutes > 1.0`).
  - HardStop: Triggered when spend reaches **90% of the daily budget** (`current_spend >= max_daily_budget * 0.90`), defaulting to **$45.00** of **$50.00** (`FINOPS_MAX_DAILY_BUDGET`). HardStop halts active missions and emits a `budget-exceeded` event to Kafka.
  - *Source Path*: `crates/factory-application/src/agents/finops.rs:133-180`.

---

## 6. GitHub Profile & Repository Counts
- **Verified Account Totals** (`gh repo list lgcorzo` as of 2026-10-31):
  - **72 total repositories** (64 public, 8 private).
  - **42 forked repositories** (including SDD tools, semantic memory, LLM proxies, and MinIO storage stack).
  - *Source Path*: GitHub GraphQL/REST API via `gh repo list lgcorzo --limit 100 --json name,isFork,visibility`.

---

## 7. Status Classification Standard (Rule 3)
- **`Designed`**: Described in specifications or wiki architecture only; live cluster verification in progress.
  - *Examples*: Multi-node chaos drills, Hazitek/SPRI automated telemetry packager (`DocAgent`).
- **`Implemented`**: Code exists in workspace, compiles cleanly, and is covered by unit or integration tests.
  - *Examples*: 5-crate Rust workspace, Criterion memory zeroization benchmark (54.2 ns), FinOpsAgent velocity evaluation.
- **`Deployed`**: Running and reconciled in the Kubernetes cluster or production CI/CD workflows.
  - *Examples*: CloudNativePG PostgreSQL 16 cluster, OpenZiti controller/routers, MinIO S3 cluster, Hatchet engine.
- **`Verified`**: Confirmed by published test suites or empirical evidence files.
  - *Examples*: `evidence/baseline.md`, `evidence/reliability-tests.md`, `evidence/security-tests.md`, `evidence/verified_status.json`.
