# Dark Gravity — Cross-Repository Remediation Report

**Date**: 2026-11-27  
**Branch**: `remediation/dark-gravity-cross-repo`  
**Scope**: `lgcorzo/lgcorzo.github.io` (portal), `lgcorzo/rust_CACD_autonomous_factory` (core factory), and linked ecosystem repositories.

---

## 1. Executive Summary

This report documents the baseline inventory and cross-repository remediation of the Dark Gravity Autonomous Software Factory ecosystem. All findings are grounded in live command execution, test suites, and source inspection.

## 2. Initial Baseline (Phase A)

| Area | Baseline State | Evidence |
|---|---|---|
| `lgcorzo.github.io` Portal & KG | `21 passed` (`pytest -q`), `0` `DOC-011` or drift errors across 12 repo packs, `5` canonical facts verified across 10 pages | `scripts/verify_ecosystem_knowledge.py`, `scripts/check_public_claims.py`, `pytest -q` |
| `dark-gravity-mcp` (Rust MCP) | `3 passed; 0 failed` (`< 100 ms` p95 cached latency, read-only) | `cargo test --manifest-path dark-gravity-mcp/Cargo.toml` |
| Adversarial SAST Scanner (`rust_CACD_autonomous_factory`) | `60` held-out samples (`40` adversarial, `20` benign): `24` blocked, `16` missed (**TPR 60.00%**, **FPR 0.00%**) | `cargo test -p factory-application --test adversarial_suite -- --nocapture` |
| `FR-008` / `CTRL-02` / `AUD-010` | `FR-008` / `CTRL-02` labeled `TESTED`; `AUD-010` remains `OPEN` (K8s Pod API alone cannot prove host `runsc` handler: `host_runtime_handler_observed: null`) | Live `zeroclaw-validate` output & `crates/factory-cli/src/evidence.rs` |
| Operational Benchmarks | `UNMEASURED` / `baseline_pending` (`value: null`) in `data/metrics.json`; `real-mission-e7-001-1795803707` executed `T001`–`T003` and `cargo test` in `gvisor` (`10,068 ms`) | `data/metrics.json`, `agents/factory-worker` logs |

## 3. Critical Findings

1. **Adversarial Scanner False Negatives (`16/40` missed, TPR 60.00%)**: `SastScanResult::inspect_diff` misses evasion patterns including secret assignments without whitespace, string-concatenation obfuscation, `execve`, hex-encoded payloads, DNS tunneling, WASM host function abuse, and SQL concatenation.
2. **`FR-008` / `CTRL-02` vs `AUD-010` Gap**: Live `zeroclaw-validate` confirms `observed_runtime_class_name: "gvisor"`, `run_as_non_root: true`, `read_only_root_filesystem: true`, `capabilities_dropped: ["ALL"]`, `seccomp_profile: "RuntimeDefault"`, but `host_runtime_handler_observed` is `null`, keeping `AUD-010` `OPEN` and `FR-008`/`CTRL-02` strictly at `TESTED` (never `VERIFIED`).
3. **Operational Benchmarks**: Fleet-wide `N > 1` benchmarks remain `UNMEASURED` (`baseline_pending`); single-mission execution (`N=1`) cannot be generalized as a statistical fleet benchmark.

## 4. Next Phases

- **Phase B**: Remediate `SastScanResult::inspect_diff` false negatives in `rust_CACD_autonomous_factory` while preserving `0.00%` FPR on benign cases, and add regression coverage.
- **Phase C–E**: Update `REMEDIATION_MATRIX.md`, `SECURITY_REMEDIATION.md`, `EVIDENCE_INDEX.md`, and `CHANGELOG_REMEDIATION.md` with verified post-fix test results.
