# Changelog — Cross-Repository Remediation

## 2026-11-27 (Phase A — Baseline)

- Created branch `remediation/dark-gravity-cross-repo` in `lgcorzo.github.io`.
- Recorded baseline verification for `lgcorzo.github.io` (`21 passed`, `0` `DOC-011` errors) and `rust_CACD_autonomous_factory` (`adversarial_suite` held-out TPR `60.00%`, FPR `0.00%`).
- Authored initial `REMEDIATION_REPORT.md`, `REMEDIATION_MATRIX.md`, `EVIDENCE_INDEX.md`, `PUBLIC_CLAIMS_AUDIT.md`, `BENCHMARK_STATUS.md`, `SECURITY_REMEDIATION.md`, and `CHANGELOG_REMEDIATION.md`.

## 2026-11-27 (Phase B–E — Security Remediation & Validation)

- Hardened `SastScanResult::inspect_diff` in `rust_CACD_autonomous_factory/crates/factory-core/src/security.rs`, improving held-out adversarial TPR from `60.00%` (`24/40`) to `67.50%` (`27/40`) with `0.00%` FPR (`0/20`).
- Verified `adversarial_suite` (`3 passed; 0 failed`) and `security_analyzer_tests` (`2 passed; 0 failed`).
