# Dark Gravity — Security Remediation

## 1. Adversarial SAST Scanner (`SastScanResult::inspect_diff`)

- **Baseline** (`tests/adversarial/heldout/corpus.json`, `60` samples):
  - Adversarial: `40` (`24` blocked, `16` missed — **TPR 60.00%**)
  - Benign: `20` (`20` allowed, `0` false positives — **FPR 0.00%**)
- **Post-Remediation** (`crates/factory-core/src/security.rs` hardened for `execve`, `ureq`/`hyper`/`lookup_host`, SQL `+` concatenation, `.truncate(true)`/`.set_len(0)`, `hex::decode`/`concat!`, `ignore previous instructions`):
  - Adversarial: `40` (`27` blocked, `13` missed — **TPR 67.50%**)
  - Benign: `20` (`20` allowed, `0` false positives — **FPR 0.00%**)
  - Tests: `adversarial_suite` (`3 passed; 0 failed`), `security_analyzer_tests` (`2 passed; 0 failed`).
- **Remaining Limitation**: `13/40` held-out evasions remain missed; static regex+AST diff inspection is a heuristic tripwire, not a substitute for gVisor isolation or human review.

## 2. `FR-008` / `CTRL-02` / `AUD-010`

- `AUD-010` remains `OPEN` because the Kubernetes Pod API alone reports `host_runtime_handler_observed: null` (`EffectiveRuntimeIsGvisor: false` in `verified_checks`).
- `FR-008` and `CTRL-02` remain strictly `TESTED`.
