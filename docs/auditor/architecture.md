---
title: "Dark Gravity AI Auditor Pack — System Architecture"
doc_role: "architecture"
schema_version: "1.0"
as_of_date: "2026-11-27"
verification_status: "mixed"
verified: "false"
visibility: "public"
canonical_sources:
  - "https://lgcorzo.github.io/architecture.html"
  - "https://lgcorzo.github.io/ARCHITECTURE.md"
  - "https://github.com/lgcorzo/rust_CACD_autonomous_factory/blob/main/Cargo.toml"
  - "https://github.com/lgcorzo/rust_CACD_autonomous_factory/blob/main/wiki/architecture/decisions/adr-008-google-ax-crd-workspace-standard-v3.1.md"
---

# System Architecture Overview

1. **5-Crate Rust Edition 2024 Workspace**: `factory-core`, `factory-application`, `factory-infrastructure`, `factory-mcp-server`, `factory-cli` (`rust_CACD_autonomous_factory`).
2. **Orchestration (`Kafka -> 5 Hatchet Steps`)**: `rustant-plan`, `zeroclaw-execute`, `zeroclaw-validate`, `rustant-review`, `factory-deliver` (strict Vertex 4 HITL blocks autonomous merge).
3. **Security & Isolation**: `gVisor (runsc)` (`30Mi`/`250m` micro-sandbox; `512Mi`/`500m` compilation), Ed25519 W3C-VC NHI, 300 s Vault JIT (`54.2 ns` `ZeroizeOnDrop`), OpenZiti mTLS 1.3. **`FR-008`/`CTRL-02` remains labeled `TESTED` while `AUD-010` is open.**
4. **Read-Only Knowledge MCP (`dark-gravity-mcp`)**: Decoupled Rust Edition 2024 `rmcp` server in `lgcorzo.github.io/dark-gravity-mcp/`.

## Indexed Architecture Decision Records

| ADR ID | Title | Status | Summary |
|---|---|---|---|
| `ADR-001` | ADR-001: gVisor (runsc) Sandbox Execution & Forensic Zeroize Memory Bounds | `accepted` | Status: accepted. Source: rust_CACD_autonomous_factory/crates/factory-core/src/security.rs. |
| `ADR-008` | ADR-008: Adoption of Google AX Declarative Patterns, CRD Scope, and SSOT Reconciliation Contract (v3.1) | `accepted` | ADR-008 v3 (accepted) plus v3.1 amendment (proposed) resolving workspace↔mission cardinality, spec mutability, and the scope of the 30Mi/250m resource bound. |
