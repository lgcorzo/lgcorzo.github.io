# Dark Gravity — Evidence Index

| Evidence ID | Repository | Commit | Artifact | Test | Date | Status | Limitations |
|---|---|---|---|---|---|---|---|
| EV-001 | `lgcorzo.github.io` | `8c0bd72` | `data/ecosystem-registry.json`, `data/canonical-claims.json` | `verify_ecosystem_knowledge.py`, `check_public_claims.py`, `pytest -q` (`21 passed`) | 2026-11-27 | VERIFIED | Covers 12 indexed repos |
| EV-002 | `lgcorzo.github.io` | `8c0bd72` | `dark-gravity-mcp/` | `cargo test --manifest-path dark-gravity-mcp/Cargo.toml` (`3 passed`) | 2026-11-27 | VERIFIED | Offline fixture + stdio smoke test |
| EV-003 | `rust_CACD_autonomous_factory` | `54e59490` | `tests/adversarial/heldout/corpus.json` | `cargo test -p factory-application --test adversarial_suite` | 2026-11-27 | TESTED | Baseline `60.00%` TPR (`24/40`), `0.00%` FPR (`0/20`) |
| EV-004 | `rust_CACD_autonomous_factory` | `021d8a42` | `sandbox-job-544c1af1-q6k2k` | Live `zeroclaw-validate` (`cargo test` in `gvisor`, `exit_code: 0`) | 2026-11-27 | TESTED | `host_runtime_handler_observed: null`; `AUD-010` remains `OPEN` |
