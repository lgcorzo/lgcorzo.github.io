# Dark Gravity — Cross-Repository Remediation Matrix

| ID | Priority | Repository | Finding | Action | Test | Status | Evidence |
|---|---|---|---|---|---|---|---|
| REM-001 | P0 | `lgcorzo.github.io` | Verify canonical claims, `DOC-011` boundary, and 12-repo knowledge packs | Ran `verify_ecosystem_knowledge.py`, `check_public_claims.py`, and `pytest -q` | `21 passed`, `0` drift/DOC-011 errors | VERIFIED | `lgcorzo.github.io` commit `8c0bd72` |
| REM-002 | P1 | `rust_CACD_autonomous_factory` | Held-out adversarial scanner misses `16/40` evasions (TPR `60.00%`, FPR `0.00%`) | Hardened `SastScanResult::inspect_diff` (`execve`, `ureq`/`hyper`, SQL `+`, `.truncate(true)`, `hex::decode`/`concat!`) | `adversarial_suite` (`3 passed`), `security_analyzer_tests` (`2 passed`) | PARTIAL | TPR improved `60.00%` -> `67.50%` (`27/40`), FPR `0.00%` (`0/20`); `13` missed |
| REM-003 | P1 | `rust_CACD_autonomous_factory` | `FR-008` / `CTRL-02` `TESTED` while `AUD-010` `OPEN` (`host_runtime_handler_observed: null`) | Preserve `TESTED` status; do not claim `VERIFIED` without host `runsc` proof | `evidence_contract_tests` + live `zeroclaw-validate` | VERIFIED | `sandbox-job-544c1af1-q6k2k` attestation |
| REM-004 | P1 | `lgcorzo.github.io` | Operational benchmarks `UNMEASURED` / `N=1` | Keep unmeasured KPIs as `UNMEASURED` (`baseline_pending`); document `N=1` limits | `tests/test_platform_metrics.py` | VERIFIED | `data/metrics.json` |
| REM-005 | P2 | `lgcorzo.github.io` | Read-only Rust MCP (`dark-gravity-mcp`) boundary & latency | Verified 6 read-only tools, 7 resources, `< 100 ms` p95 | `cargo test --manifest-path dark-gravity-mcp/Cargo.toml` | VERIFIED | `3 passed; 0 failed` |
