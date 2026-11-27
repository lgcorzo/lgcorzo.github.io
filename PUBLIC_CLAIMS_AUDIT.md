# Dark Gravity — Public Claims Audit

| Claim | Published Location | Evidence Available | Status | Action Taken |
|---|---|---|---|---|
| `64` public repos (`22` original + `42` maintained forks; `69` historical; `72` Spec `004` incl. `6` private) | `data/canonical-claims.json`, `index.html`, `start-here/` | `scripts/check_public_claims.py` (`10` pages) | VERIFIED | Scope explicitly defined per count |
| `lgcorzo/kes` is `FROZEN_READONLY` | `DARK_GRAVITY_MANIFEST.md`, `REPOSITORIES.md` | `verify_ecosystem_knowledge.py` | VERIFIED | Preserved read-only |
| `FR-008` / `CTRL-02` (`gVisor` isolation) | `docs/auditor/architecture.md`, `data/metrics.json` | `zeroclaw-validate` + `AUD-010` open | TESTED | Strictly labeled `TESTED` (not `VERIFIED`) |
| Fleet-wide operational KPIs | `data/metrics.json`, `metrics.html` | `tests/test_platform_metrics.py` | UNMEASURED | Kept `value: null` (`baseline_pending`) |
