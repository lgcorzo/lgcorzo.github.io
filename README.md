# Public Repositories & Lab Ecosystem Directory — Dr. Luis Galo Corzo

This repository (`lgcorzo.github.io`) serves as the public engineering lab portal, interactive architecture showcase, and ecosystem index for [Dr. Luis Galo Corzo (`@lgcorzo`)](https://github.com/lgcorzo).

Across **71 total repositories** (**67 active**, **4 archived**; **63 public**, **8 private internal infrastructure/factory repositories**), the ecosystem is organized around the **Dark Gravity Continuous Agentic / Continuous Deployment (CA/CD) Autonomous Software Factory** and its sovereign infrastructure, cognitive memory, and Spec-Driven Development (SDD) toolchains.

---

## 🧭 1. Actual Operational Status of the Dark Gravity Autonomous Factory

To maintain strict engineering transparency, every subsystem in the **Dark Gravity Autonomous Factory (`V7.2 / V7.3`)** is tracked across a **4-Tier Operational Lifecycle Status Model** rather than broad marketing claims:

| Status Tier | Engineering Definition | Current Factory Subsystems & Verification State |
| :--- | :--- | :--- |
| **`Implemented`** | Compiled, unit-tested, and benchmarked in the Rust 2024 5-crate workspace (`factory-core`, `factory-application`, `factory-infrastructure`, `factory-mcp-server`, `factory-cli`). | • **5-Crate Onion Architecture** (`cargo test --workspace`, `cargo clippy -- -D warnings`)<br/>• **Ed25519 Non-Human Identities (NHI)** (`ed25519-dalek` W3C Verifiable Credentials)<br/>• **Forensic Memory Zeroization** (`zeroize` on drop, micro-benchmarked at `54.2 ns` via Criterion)<br/>• **4-Vertex Human-in-the-Loop (HITL) Governance & CircuitBreakerGuard** (3-retry cap, diff-hash loop detection, FinOps spend velocity guards)<br/>• **GitPlatformPoller & Interactive PR Directives** (`@darkgravity /status`, `/interact`, `/refine`, `/validate`) |
| **`Deployed`** | Running as live Kubernetes workloads across the 10-namespace cluster topology via FluxCD GitOps reconciliation. | • **10-Namespace Kubernetes Topology** (`agents`, `orchestrators`, `confluent`, `storage`, `knowledge`, `llm-apps`, `security`, `openziti`, `development`, `flux-system`)<br/>• **Hatchet Durable DAG Orchestrator** & **Apache Kafka (KRaft)** event backbone<br/>• **Sovereign Storage & Data Plane**: CloudNativePG (`pgvector`) + decoupled `@lgcorzo` MinIO S3 (`ghcr.io/lgcorzo/minio`, `operator`, `mc`)<br/>• **Cognitive & LLM Routing Plane**: `dark-litellm` multi-model gateway, `R2R-Engine` GraphRAG, and `semantica` knowledge graph memory<br/>• **Autonomous Vulnerability & Jules Remediation Pipeline**: Hourly Dependabot/CodeQL scanner linked to GitHub Project 6 |
| **`Designed`** | Architectural contracts, trait boundaries, or Kubernetes manifests defined; currently under end-to-end cluster integration or mock-to-live transition. | • **Full Production Chaos & Multi-Node Failover Drills** across all 10 namespaces<br/>• **Live External Regulatory Certification Audits** (the architecture is engineered for **regulatory readiness and technical alignment** with EU AI Act Art. 12/14, SOC 2 Type II, and ISO/IEC 25059, rather than claiming formal third-party certification)<br/>• **Automated Hazitek / SPRI Grant Packager (`DocAgent`)** end-to-end production telemetry export |
| **`Verified`** | Backed by reproducible automated test suites, SAST/CodeQL scans, deterministic lockfiles, or Criterion benchmark artifacts in `evidence/verified_status.json`. | • **Zero-Warning Rust & Python Quality Gates** across core factory repositories<br/>• **Continuous CodeQL, Dependabot, and `pip-audit` / `cargo audit` Enforcement** across active repositories |

---

## 🛡️ 2. Why Principal Open-Source Projects Are Forked & Maintained Under Our Code Quality Rules

Out of the 71 repositories in the `@lgcorzo` lab, **41 are strategic forks** of principal open-source projects spanning **Spec-Driven Development (SDD)**, **Agentic Frameworks**, **GraphRAG & Semantic Memory**, **AST Documentation**, and **High-Performance S3 Storage / SIMD Cryptography**.

### Why We Fork Principal Upstream Projects
Relying directly on unpinned upstream repositories or public container registries (`docker.io`, `quay.io`, PyPI/Crates rolling branches) introduces four critical risks to an autonomous software factory:
1. **Upstream Breaking Changes & Contract Drift**: Autonomous agents rely on deterministic CLI contracts, JSON schemas, and AST parsers (`spec-kit`, `superpowers`, `speckit-superpowers-bridge`, `deepwiki-rs`). Silent upstream breaking changes can halt multi-agent DAG execution mid-flight.
2. **Unpatched Transitive Vulnerabilities (CVEs)**: Upstream AI and RAG frameworks (`semantica`, `dark-litellm`, `CodeWiki`, `openwiki`, `openevolve`, `TradingAgents`) frequently carry vulnerable transitive dependencies in `pip`, `poetry`, or `npm` trees that remain unmerged upstream for weeks.
3. **Licensing, Distribution & Feature Removal Shifts**: Upstream vendors (such as MinIO's 2025/2026 console and binary distribution changes) can abruptly remove administrative capabilities or alter container distribution policies.
4. **Prompt Injection & Supply-Chain Poisoning**: In an autonomous agentic system, third-party skills, MCP tools, and GitHub Actions workflows must be audited and pinned before an agent is permitted to execute them.

### How Forked Projects Are Maintained Under `@lgcorzo` Code Quality & Security Rules
Every principal fork in this ecosystem is decoupled from blind upstream rebases and governed by five mandatory engineering rules:
1. **Strict Static Analysis, Type Safety & Formatting Triad**:
   - **Rust Repositories** (`rust_CACD_autonomous_factory`, `Jules_remediator`, `fastapi-autogen-team`, `deepwiki-rs`, `adk-rust`): Enforced `cargo clippy --all-targets -- -D warnings`, `rustfmt --check`, and workspace unit/integration test suites.
   - **Python Repositories** (`mlops-python-package`, `llmops-python-package`, `spec-kit`, `semantica`, `dark-litellm`, `CodeWiki`, `openwiki`): Enforced `ruff` linting/formatting, strict typing (`mypy` / `pyright`), and `pytest` regression suites across Python 3.11–3.14 matrices.
2. **Deterministic Dependency Pinning & Cryptographic Lockfiles**:
   - Vulnerable transitive packages (e.g., `pygments`, `aiohttp`, `cryptography`, `authlib`, `pytest`, `undici`, `lodash`, `axios`) are explicitly patched and locked via `poetry.lock`, `uv.lock`, `Cargo.lock`, or SHA-256 hash-pinned `security-audit-requirements.txt` manifests verified in CI.
3. **Continuous SAST, CodeQL & Autonomous Remediation (GitHub Project 6)**:
   - Every active repository runs automated **GitHub CodeQL** (Python, Rust, Go, TypeScript, and GitHub Actions workflow analysis) and **Dependabot** security scanning.
   - An **Autonomous Vulnerability Monitor** runs hourly, aggregating alerts into **GitHub Project 6**, dispatching **Jules** / **Dark Gravity** remediation sessions with root-cause recipes, validating CI test matrices, and pruning stale branches.
4. **Spec-Driven Development (SDD) & ISO/IEC/IEEE 42010 Living Documentation**:
   - Changes follow the **Spec Kit + Superpowers Bridge** contract (`constitution.md` → `spec.md` → `plan.md` → `tasks.md` → TDD execution) and maintain AST-synchronized **OpenWiki / OKF** architectural documentation with UML 2.0 Mermaid diagrams.
5. **Human-in-the-Loop (HITL) Branch Protection & Hermetic Releases**:
   - Principal repositories enforce branch protection and **`AGENTS.md` HITL rules**: autonomous agents may open branches, fix CI failures, and submit verified PRs, but production merges into `main` on core factory repositories require explicit human architectural sign-off. Container artifacts build hermetically to `ghcr.io/lgcorzo/*` under immutable semantic tags (`v*.*.*-lgcorzo.*`).

---

## 🛰️ 3. Dark Gravity Autonomous Factory, SDD & Agent Architecture

Core orchestrators, autonomous remediation agents, Spec-Driven Development toolkits, RAG engines, and cognitive memory frameworks powering the **Dark Gravity CA/CD Autonomous Agent Factory**.

*Filter on GitHub:* [topic:dark-gravity-factory](https://github.com/stars/lgcorzo/lists/dark-gravity-factory) or search `user:lgcorzo topic:dark-gravity-factory`

| Repository | Language | Governance Role | Description & Maintenance Focus |
| :--- | :--- | :--- | :--- |
| [**rust_CACD_autonomous_factory**](https://github.com/lgcorzo/rust_CACD_autonomous_factory) | Rust | Original Core (HITL Protected) | Dark Gravity CA/CD Core: 5-crate Rust 2024 workspace, Hatchet 6-phase DAG orchestrator, Ed25519 NHI credentials & gVisor sandboxes. |
| **Jules_remediator** *(Private Factory)* | Rust | Original Core (DDD + MLOps) | Autonomous Kubernetes error remediation factory listening to FluxCD alerts, logging MLflow experiments, and triggering Jules SDK fixes. |
| [**fastapi-autogen-team**](https://github.com/lgcorzo/fastapi-autogen-team) | Rust | Original Core (HITL Protected) | High-throughput Axum & Rig microservice exposing OpenAI-compatible streaming endpoints for multi-agent squads. |
| [**mlops-python-package**](https://github.com/lgcorzo/mlops-python-package) | Python | Original Core (HITL + OpenWiki) | Industrial MLOps Standard: Reproducible ML pipelines, DVC data versioning, MLflow tracking, SHAP explainability, and SHA-256 pinned security audit lockfiles. |
| [**llmops-python-package**](https://github.com/lgcorzo/llmops-python-package) | Python | Original Core (OpenWiki + OKF) | Enterprise LLMOps Standard: ISO/IEC/IEEE 42010 agent observability, prompt lineage, deterministic evaluation gates, and OpenWiki AST docs. |
| **gitops_internal_lgcorzo** *(Private Infra)* | Shell / K8s | Original Core Infra | Cluster infrastructure, SealedSecrets, OpenZiti dark networking, FluxCD GitOps manifests, and the hourly Project 6 autonomous vulnerability monitor. |
| [**spec-kit**](https://github.com/lgcorzo/spec-kit) | Python | Hardened Fork (`github/spec-kit`) | Specification-Driven Development (SDD) toolkit and `specify` CLI; maintained with custom CodeQL gates, `pip-audit` enforcement, and multi-OS pytest matrices. |
| [**superpowers**](https://github.com/lgcorzo/superpowers) | Shell | Hardened Fork (`obra/superpowers`) | Agentic software engineering methodology (TDD, git worktrees, subagent dispatch, systematic debugging, verification-before-completion). |
| [**speckit-superpowers-bridge**](https://github.com/lgcorzo/speckit-superpowers-bridge) | Shell | Hardened Fork (`lihan3238/...`) | Thin protocol bridge combining Spec Kit (`spec.md`, `plan.md`, `tasks.md` WHAT contracts) with Superpowers (`executing-plans` HOW discipline) and guard rules. |
| [**semantica**](https://github.com/lgcorzo/semantica) | Python | Hardened Fork (`semantica-agi/semantica`) | Semantic graph memory & knowledge extraction engine for autonomous agents; continuously patched via Dependabot/CodeQL & autonomous PR verification. |
| [**deepwiki-rs**](https://github.com/lgcorzo/deepwiki-rs) | Rust | Hardened Fork (`sopaco/deepwiki-rs`) | High-performance Rust AST CodeGraph, Repomix context indexer, and architectural documentation generator enforcing Orphan Symbol Rate (`OSR < 5%`). |
| [**dark-litellm**](https://github.com/lgcorzo/dark-litellm) | Python | Hardened Fork (`BerriAI/litellm`) | Sovereign multi-model LLM gateway & FinOps proxy injecting Virtual Tags (`x-vtags-*`), cost velocity circuit breakers, and patched Python/UI dependency trees. |
| [**R2R-Engine**](https://github.com/lgcorzo/R2R-Engine) | Python | Sovereign RAG Core | Production-ready Retrieval-Augmented Generation (GraphRAG) engine powering contextual code & architecture memory in the `llm-apps` namespace. |
| [**R2R-Application**](https://github.com/lgcorzo/R2R-Application) | TypeScript | Sovereign RAG UI | Next.js/React observability dashboard for inspecting R2R GraphRAG pipelines, knowledge graphs, and agent semantic memory; hardened with pinned npm overrides. |
| [**adk-rust**](https://github.com/lgcorzo/adk-rust) | Rust | Hardened Fork (`zavora-ai/adk-rust`) | Rust Agent Development Kit: modular components for LLM models, MCP tools, memory, and realtime sessions used inside gVisor developer sandboxes. |
| [**CodeWiki**](https://github.com/lgcorzo/CodeWiki) | Python | Hardened Fork (`FSoft-AI4Code/CodeWiki`) | Holistic repository-level documentation and AST comprehension framework maintained under strict Python security audit constraints. |
| [**openwiki**](https://github.com/lgcorzo/openwiki) | Python | Hardened Fork (`TryDotAt/openwiki`) | Autonomous CLI that generates and refreshes recurring `openwiki/` architecture, workflow, and source-map documentation via GitHub Actions. |
| [**deepwiki-open**](https://github.com/lgcorzo/deepwiki-open) | TypeScript / Python | Hardened Fork (`AsyncFuncAI/deepwiki-open`) | Open-source AI-powered wiki generator for GitHub/GitLab repositories, maintained with patched Next.js/Python dependencies. |
| [**openevolve**](https://github.com/lgcorzo/openevolve) | Python | Hardened Fork (`algorithmicsuperintelligence/openevolve`) | Open-source evolutionary coding agent framework maintained under our Python dependency and CodeQL security gates. |
| [**devops_job_shop_scheduling**](https://github.com/lgcorzo/devops_job_shop_scheduling) | Python | Original Research / MLOps | Industrial job-shop scheduling optimization (OR-Tools / Metaheuristics) with automated CI/CD and security-audited dependencies. |
| [**Documentation_agent**](https://github.com/lgcorzo/Documentation_agent) | Python | Original Agent Worker | Automated codebase documentation generator and semantic analysis worker. |

---

## 🪣 4. MinIO Sovereign S3 Storage & High-Performance Primitives (38 Decoupled Forks)

High-throughput sovereign object storage, hardware-accelerated cryptographic primitives, direct NVMe CSI drivers, and Go client SDKs. Maintained independently under `@lgcorzo` with `golang:1.26-alpine` toolchains, hermetic `ghcr.io/lgcorzo/*` builds, and immutable `v*.*.*-lgcorzo.*` tags.

*Filter on GitHub:* [topic:minio-storage](https://github.com/stars/lgcorzo/lists/minio-storage) or search `user:lgcorzo topic:minio-storage`

| Repository | Language | Sub-domain | Description |
| :--- | :--- | :--- | :--- |
| [**minio**](https://github.com/lgcorzo/minio) | Go | Object Storage Core | High-performance, S3-compatible sovereign object storage server (`ghcr.io/lgcorzo/minio`). |
| [**mc**](https://github.com/lgcorzo/mc) | Go | Admin & Management | MinIO Client CLI: complete toolset for filesystem, S3 bucket, and mirror management (`ghcr.io/lgcorzo/mc`). |
| [**operator**](https://github.com/lgcorzo/operator) | Go | K8s Operator | Kubernetes operator for provisioning and managing S3 tenant instances (`ghcr.io/lgcorzo/operator`). |
| [**console**](https://github.com/lgcorzo/console) | Go / TS | Management UI | Sovereign web dashboard for monitoring S3 object storage health, tenants, and quotas. |
| [**kes**](https://github.com/lgcorzo/kes) | Go | KMS & Security | Key Encryption Server providing stateless, hardware-backed zero-trust authenticated encryption at rest. |
| [**directpv**](https://github.com/lgcorzo/directpv) | Go | K8s Storage CSI | Direct-attached NVMe storage CSI driver for Kubernetes high-throughput storage pipelines. |
| [**minio-go**](https://github.com/lgcorzo/minio-go) | Go | S3 Client SDK | Hardened S3 Go client library for zero-trust, high-throughput artifact transfer. |
| [**madmin-go**](https://github.com/lgcorzo/madmin-go) | Go | Management SDK | Administrative Go client library for monitoring and configuring sovereign storage nodes. |
| [**kms-go**](https://github.com/lgcorzo/kms-go) | Go | KMS Driver | Cryptographic key management client communication driver for storage clusters. |
| [**warp**](https://github.com/lgcorzo/warp) | Go | Benchmarking | S3 benchmarking tool for measuring throughput and latency across cluster nodes. |
| [**dperf**](https://github.com/lgcorzo/dperf) | Go | Benchmarking | High-speed TCP/UDP network throughput testing utility for low-latency storage nodes. |
| [**sidekick**](https://github.com/lgcorzo/sidekick) | Go | Traffic & Routing | High-performance multi-endpoint HTTP proxy and load-balancer for S3 clusters. |
| [**certgen**](https://github.com/lgcorzo/certgen) | Go | Security & PKI | Zero-dependency mTLS certificate generator for sovereign infrastructure nodes. |
| [**simdjson-go**](https://github.com/lgcorzo/simdjson-go) | Go | Hardware Acceleration | AVX-512 / AVX2 SIMD-accelerated JSON parser for high-throughput pipeline ingestion. |
| [**sha256-simd**](https://github.com/lgcorzo/sha256-simd) | Go | Hardware Acceleration | SIMD-accelerated SHA256 cryptographic hashing implementation (AVX512 / ARM Neon). |
| [**blake2b-simd**](https://github.com/lgcorzo/blake2b-simd) | Go | Hardware Acceleration | Fast hardware-accelerated BLAKE2b hashing primitive in pure Go. |
| [**md5-simd**](https://github.com/lgcorzo/md5-simd) | Go | Hardware Acceleration | AVX-512 / AVX2 SIMD MD5 hashing primitive for S3 multipart eTag computation. |
| [**highwayhash**](https://github.com/lgcorzo/highwayhash) | Go | Hardware Acceleration | High-speed AVX2/SSE4/NEON SIMD hashing algorithm for checksum verification. |
| [**crc64nvme**](https://github.com/lgcorzo/crc64nvme) | Go | Hardware Acceleration | Hardware-accelerated CRC64-NVMe checksum implementation via carryless multiplication. |
| [**sio**](https://github.com/lgcorzo/sio) | Go | Crypto / DARE | Data-At-Rest Encryption (DARE) library implementing authenticated encryption streams. |
| [**asm2plan9s**](https://github.com/lgcorzo/asm2plan9s) | Go | SIMD Tooling | Assembler utility for generating Plan9 assembly (`YASM` to Go `.s`) for SIMD primitives. |
| [**pkg**](https://github.com/lgcorzo/pkg) | Go | Core Primitives | Common Go system packages (disk, net, env, wildcard, locks) shared across storage services. |
| [**cli**](https://github.com/lgcorzo/cli) | Go | Automation CLI | Sovereign Go CLI package for building structured command-line utilities. |
| [**docs**](https://github.com/lgcorzo/docs) | RST / Python | Sovereign Charter | Central architectural charter, Go module decoupling specs, and Sovereign AIStor documentation. |

*(Plus 14 additional decoupled Go support libraries and test harnesses: `colorjson`, `csvparser`, `dnscache`, `filepath`, `mint`, `minio-cf`, `mtls`, `multipart-debug`, `mux`, `pkger`, `selfupdate`, `websocket`, `xxml`, and `zipindex`.)*

---

## 🌐 5. General, Financial AI, Hardware & Application Repositories

Web applications, financial multi-agent frameworks, GPU tooling, educational courses, and standalone research repositories.

*Filter on GitHub:* [topic:general-application](https://github.com/stars/lgcorzo/lists/general-application) or search `user:lgcorzo topic:general-application`

| Repository | Language | Governance Role | Description |
| :--- | :--- | :--- | :--- |
| [**lgcorzo.github.io**](https://github.com/lgcorzo/lgcorzo.github.io) | HTML / CSS / JS | Lab Portal | Public Lab for AI Systems Engineering: interactive architecture showcase, lifecycle status, fork policy, and repository explorer. |
| [**FinRobot**](https://github.com/lgcorzo/FinRobot) | Python | Hardened Fork (`AI4Finance-Foundation/FinRobot`) | Open-source AI Agent Platform for Financial Analysis and Quantitative Research using LLM multi-agents. |
| [**TradingAgents**](https://github.com/lgcorzo/TradingAgents) | Python | Hardened Fork (`TauricResearch/TradingAgents`) | Multi-agent LLM financial trading framework with market simulation and risk management personas. |
| [**gpu-unlock**](https://github.com/lgcorzo/gpu-unlock) | Shell / C | Hardware Utility | Low-level GPU configuration and compute capability utility for local lab hardware acceleration. |
| [**GEN_AI_Course**](https://github.com/lgcorzo/GEN_AI_Course) | Jupyter / Python | Educational | Practical notebooks and architectural labs on Generative AI, RAG pipelines, and LLM systems engineering. |
| [**mds**](https://github.com/lgcorzo/mds) | Python | NLP Research | Multi-document summarization and clinical/scientific NLP pipeline experimentation. |
| **la_consulta_de_marta** *(Private Web)* | HTML / JS | Healthcare Web | Psychology consultation web portal engineered with strict accessibility, UX/CRO, and automated reflection publishing skills. |
