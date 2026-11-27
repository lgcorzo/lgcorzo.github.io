---
title: "Dark Gravity AI Auditor Pack — Platform Metrics & Epistemic Status"
doc_role: "metrics"
schema_version: "1.0"
as_of_date: "2026-11-27"
verification_status: "mixed"
verified: "false"
visibility: "public"
canonical_sources:
  - "https://lgcorzo.github.io/data/metrics.json"
  - "https://lgcorzo.github.io/metrics.html"
  - "https://github.com/lgcorzo/rust_CACD_autonomous_factory/tree/main/evidence/records"
---

# Platform KPIs & Verified Baselines

Snapshot timestamp: `2026-11-27T11:17:47Z` (`rolling_30d_and_cumulative_evidence`). All unmeasured aggregates are strictly marked **`UNMEASURED` (`baseline_pending`)** with `value: null`. **`FR-008` / `CTRL-02` remains labeled `TESTED` while `AUD-010` is open.**

## Development KPIs (`development`)

| Metric ID | KPI | Value | Unit | Status | Evidence & Notes |
|---|---|---|---|---|---|
| `development.lead_time_hours` | Lead Time for Changes | `UNMEASURED` (`null`) | `hours` | `baseline_pending` | UNMEASURED (baseline_pending): Multi-run fleet-wide issue-to-merge series requires authenticated GitHub webhook/API history across all target repositories. |
| `development.cycle_time_hours` | Cycle Time | `0.049` | `hours` | `partial` | Observed 2m57s (0.049 h) end-to-end 5-step Hatchet DAG run in Mission #476 (EXP-2026-013; target < 60 min). Scope N=1 single run; fleet rolling average pending. |
| `development.mttr_hours` | Mean Time to Recovery (MTTR) | `UNMEASURED` (`null`) | `hours` | `baseline_pending` | UNMEASURED (baseline_pending): Architecture target is < 45 s and Hatchet crash resume measured 8.4 s (EXP-2026-006); multi-incident rolling remediation MTTR pending. |
| `development.deployment_frequency_per_week` | Deployment Frequency | `UNMEASURED` (`null`) | `per_week` | `baseline_pending` | UNMEASURED (baseline_pending): Continuous weekly FluxCD tag and GitHub release counter pending multi-week automated collection. |

## Quality KPIs (`quality`)

| Metric ID | KPI | Value | Unit | Status | Evidence & Notes |
|---|---|---|---|---|---|
| `quality.defect_density_per_kloc` | Defect Density | `UNMEASURED` (`null`) | `per_kloc` | `baseline_pending` | UNMEASURED (baseline_pending): Requires normalized KLOC counters paired with CodeQL/linters across all 64 public repositories. |
| `quality.escaped_defects_count` | Escaped Defects | `UNMEASURED` (`null`) | `count` | `baseline_pending` | UNMEASURED (baseline_pending): Post-release regression/hotfix issue classification across factory targets pending multi-release tracking. |
| `quality.pr_acceptance_rate_pct` | PR Acceptance Rate | `UNMEASURED` (`null`) | `percent` | `baseline_pending` | UNMEASURED (baseline_pending): Fleet-wide merged vs. closed-unmerged autonomous PR ratio pending authenticated GitHub telemetry. |

## Security KPIs (`security`)

| Metric ID | KPI | Value | Unit | Status | Evidence & Notes |
|---|---|---|---|---|---|
| `security.vulnerabilities_found_count` | Vulnerabilities Found | `3369` | `count` | `partial` | Cluster Trivy snapshot post-remediation: 396 CRITICAL + 2,973 HIGH active findings (down from 429 CRITICAL + 3,660 HIGH). FR-008/CTRL-02 remains TESTED while AUD-010 is open (CTRL-04/05/07/08 runtime_verified). |
| `security.vulnerabilities_fixed_count` | Vulnerabilities Fixed | `720` | `count` | `partial` | Verified Trivy CRITICAL+HIGH vulnerabilities remediated (EXP-2026-012), alongside 9/11 audit findings (AUD-001..009) closed and 54.2 ns ZeroizeOnDrop memory wipe verified. FR-008/CTRL-02 kept TESTED pending AUD-010. |
| `security.mean_remediation_time_hours` | Mean Remediation Time | `UNMEASURED` (`null`) | `hours` | `baseline_pending` | UNMEASURED (baseline_pending): Alert created_at -> fixed_at duration aggregation across GitHub Project 6 pending continuous sweep. |

## Agents KPIs (`agents`)

| Metric ID | KPI | Value | Unit | Status | Evidence & Notes |
|---|---|---|---|---|---|
| `agents.agent_success_rate_pct` | Agent Success Rate | `UNMEASURED` (`null`) | `percent` | `baseline_pending` | UNMEASURED (baseline_pending): Offline evidence check verified 11/11 non-mock passed requirement records (FR-008 TESTED while AUD-010 open); live Mission #476 R2R Hatchet recorded 87 COMPLETED / 0 failed tasks; rolling multi-mission percentage pending. |
| `agents.hitl_approval_rate_pct` | HITL Approval Rate | `UNMEASURED` (`null`) | `percent` | `baseline_pending` | UNMEASURED (baseline_pending): Vertex 4 human approval rate across agent-authored PRs pending multi-mission series. |
| `agents.autonomous_completion_rate_pct` | Autonomous Completion Rate | `UNMEASURED` (`null`) | `percent` | `baseline_pending` | UNMEASURED (baseline_pending): Ratio of missions reaching Stage 5 factory-deliver without prior human override pending multi-mission series. |
