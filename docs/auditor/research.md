---
title: "Dark Gravity AI Auditor Pack — Research Questions & Validation"
doc_role: "research"
schema_version: "1.0"
as_of_date: "2026-11-27"
verification_status: "mixed"
verified: "false"
visibility: "public"
canonical_sources:
  - "https://lgcorzo.github.io/RESEARCH.md"
  - "https://lgcorzo.github.io/EXPERIMENTS.md"
  - "https://lgcorzo.github.io/notebooks.html"
---

# Research Questions & Empirical Status Summary

Full canonical definitions live in [`RESEARCH.md`](../../RESEARCH.md) and [`EXPERIMENTS.md`](../../EXPERIMENTS.md).

| RQ ID | Core Question | Primary Metrics | Linked Experiments | Current Status |
|---|---|---|---|---|
| `RQ1` | Can autonomous agents reduce MTTR under strict HITL gates? | `development.mttr_hours`, `development.cycle_time_hours`, `security.mean_remediation_time_hours`, `agents.agent_success_rate_pct` | `EXP-2026-003`, `EXP-2026-006`, `EXP-2026-011`, `EXP-2026-012`, `EXP-2026-013`, `EXP-2026-014` | `partially_supported` (`2m57s` single-run Mission `#476`; multi-run `mttr_hours` `baseline_pending`) |
| `RQ2` | Can verifiable credentials improve governance & attribution? | `agents.hitl_approval_rate_pct`, `agents.agent_success_rate_pct`, `development.lead_time_hours` | `EXP-2026-005`, `EXP-2026-011`, `EXP-2026-013` | `evidence_collecting` (Ed25519 + 300s Vault JIT + `54.2 ns` zeroize implemented) |
| `RQ3` | Can GitOps & sandboxing act as an enforceable security boundary? | `security.vulnerabilities_found_count`, `security.vulnerabilities_fixed_count`, `quality.escaped_defects_count` | `EXP-2026-001`, `EXP-2026-002`, `EXP-2026-004`, `EXP-2026-005`, `EXP-2026-006`, `EXP-2026-007`, `EXP-2026-010`, `EXP-2026-011`, `EXP-2026-012` | `partially_supported` (`720` Trivy findings fixed; `9/11` `AUD-001..009` closed; `FR-008` `TESTED` pending `AUD-010`) |
| `RQ4` | Can structured agentic workflows outperform traditional ad-hoc development? | `agents.autonomous_completion_rate_pct`, `quality.pr_acceptance_rate_pct`, `quality.defect_density_per_kloc`, `development.deployment_frequency_per_week` | `EXP-2026-002`, `EXP-2026-003`, `EXP-2026-008`, `EXP-2026-009`, `EXP-2026-010`, `EXP-2026-013`, `EXP-2026-014` | `partially_supported` (`91.8%` AST token savings, `94%` first-pass accuracy, `44%` LLM-judge false-negative avoidance, `87/87` R2R Hatchet tasks) |

## Methodological Safeguards
- Single-run demonstrations (`Mission #476`, `Mission #478`) are reported with exact scope (`N = 1`) and never extrapolated into fleet-wide averages.
- All unmeasured fleet KPIs explicitly carry `baseline_pending` (`UNMEASURED`) until automated collectors verify multi-run GitHub/evidence histories.
