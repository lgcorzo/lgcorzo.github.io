---
title: "Dark Gravity AI Auditor Pack — Ecosystem Topology & Fork Policy"
doc_role: "ecosystem"
schema_version: "1.0"
as_of_date: "2026-11-27"
verification_status: "verified"
verified: "false"
visibility: "public"
canonical_sources:
  - "https://lgcorzo.github.io/data/ecosystem-registry.json"
  - "https://lgcorzo.github.io/data/canonical-claims.json"
  - "https://lgcorzo.github.io/REPOSITORIES.md"
  - "https://lgcorzo.github.io/fork-policy.html"
---

# Ecosystem Repository Map & Fork Governance

- **Public Portfolio**: **`64`** repositories (`22` original + `42` maintained open-source forks under `MAINTAINED_FORK_PROFILE`).
- **Historical Baseline**: `69` (`EXP-2026-011`).
- **Spec `004` Inventory**: `72` (`66` public + `6` private anonymized under `DOC-011`).
- **Archived Fork Exception**: `lgcorzo/kes` is permanently **`FROZEN_READONLY`** (`archived: true`).

| Repository / Alias | Visibility | Tier | Profile | Summary |
|---|---|---|---|---|
| [R2R-Engine](https://github.com/lgcorzo/R2R-Engine) | `public` | `maintained_fork` | `MAINTAINED_FORK_PROFILE` | Sovereign hybrid vector (pgvector) + Leiden GraphRAG corporate memory engine patched for deterministic Hatchet collection graph sync. |
| [dark-litellm](https://github.com/lgcorzo/dark-litellm) | `public` | `maintained_fork` | `MAINTAINED_FORK_PROFILE` | Hardened sovereign LLM gateway and priority router enforcing X-Vtag-* FinOps telemetry, RedisPriorityScheduler, and A2A policy enforcement. |
| [deepwiki-rs](https://github.com/lgcorzo/deepwiki-rs) | `public` | `maintained_fork` | `MAINTAINED_FORK_PROFILE` | Tree-sitter Rust AST analyzer and Orphan Symbol Rate (OSR < 5%) verifier generating grounded OKF architectural maps. |
| [fastapi-autogen-team](https://github.com/lgcorzo/fastapi-autogen-team) | `public` | `owned_domain` | `First-party` | Native Rust (Axum + Rig) multi-agent streaming SSE microservice serving OpenAI-compatible multi-agent squads integrated with R2R. |
| `Internal GitOps Control Plane` (`DOC-011`) | `private` | `private_gitops` | `First-party` | Private FluxCD v2 GitOps control plane managing the 10-namespace Kubernetes topology, SealedSecrets, OpenZiti mesh, and NetworkPolicies (anonymized per DOC-011). |
| `Internal Incident Remediation Service` (`DOC-011`) | `private` | `private_gitops` | `First-party` | Private Kubernetes incident remediation daemon listening to FluxCD alerts, classifying errors, logging MLflow runs, and generating patch PRs (anonymized per DOC-011). |
| [kes](https://github.com/lgcorzo/kes) | `public` | `maintained_fork` | `FROZEN_READONLY` | Archived Key Encryption Server reference fork locked permanently to FROZEN_READONLY and cataloged read-only without mutations. |
| [lgcorzo](https://github.com/lgcorzo/lgcorzo) | `public` | `public_portal` | `First-party` | GitHub profile entry repository routing human reviewers and external agents to Dark Gravity's unified portal, auditor pack, and ecosystem topology. |
| [lgcorzo.github.io](https://lgcorzo.github.io/) | `public` | `public_portal` | `First-party` | Canonical public Dark Gravity engineering hub hosting /start-here, /ai-agents, Lab Notebooks, RESEARCH.md, EXPERIMENTS.md, /docs/auditor/, Knowledge Graph, metrics, and read-only Rust dark-gravity-mcp. |
| [llmops-python-package](https://github.com/lgcorzo/llmops-python-package) | `public` | `owned_domain` | `First-party` | Domain-driven LLMOps platform aligned with ISO/IEC/IEEE 42010 & 15289 standards, prompt evaluations, Hatchet DSLs, MCP registries, and OpenWiki living documentation. |
| [minio](https://github.com/lgcorzo/minio) | `public` | `maintained_fork` | `MAINTAINED_FORK_PROFILE` | Sovereign S3-compatible object storage fork built hermetically to GHCR storing checkpoints, provenance bundles, and R2R documents. |
| [mlops-python-package](https://github.com/lgcorzo/mlops-python-package) | `public` | `owned_domain` | `First-party` | First-party MLOps standard package (DVC, MLflow, Hydra, SHAP, CycloneDX SBOM, OpenWiki) serving as continuous validation target for autonomous missions (#476, #478). |
| [rust_CACD_autonomous_factory](https://github.com/lgcorzo/rust_CACD_autonomous_factory) | `public` | `core_factory` | `First-party` | Core 5-crate Rust 2024 CA/CD orchestrator, AgentWorkspace operator, Hatchet DAG runner, gVisor SandboxDriver, and runtime MCP server. |
| [semantica](https://github.com/lgcorzo/semantica) | `public` | `maintained_fork` | `MAINTAINED_FORK_PROFILE` | Semantic domain ontology and causal provenance engine consuming Kafka agent-thought streams and detecting cross-lane conflicts. |
| [spec-kit](https://github.com/lgcorzo/spec-kit) | `public` | `maintained_fork` | `MAINTAINED_FORK_PROFILE` | Sovereign fork of GitHub Spec-Kit powering Dark Gravity's WHAT contract workflows (/speckit-specify, /speckit-plan, /speckit-tasks). |
| [speckit-superpowers-bridge](https://github.com/lgcorzo/speckit-superpowers-bridge) | `public` | `orchestration_bridge` | `First-party` | Contract handoff bridge uniting Spec-Kit (WHAT: constitution, spec, plan, tasks) with Superpowers execution discipline (HOW: TDD, subagents, verification gates) and guard-command enforcement. |
| [superpowers](https://github.com/lgcorzo/superpowers) | `public` | `maintained_fork` | `MAINTAINED_FORK_PROFILE` | Sovereign fork of the Superpowers agentic discipline harness powering HOW workflows (TDD, subagents, debugging, verification gates). |
