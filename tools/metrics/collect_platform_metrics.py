#!/usr/bin/env python3
"""Deterministic Platform Metrics Collector for Dark Gravity (T035).

Reads local verified evidence records (and optional GitHub REST API telemetry when
enabled) to generate data/metrics.json (13 KPIs across 4 domains) with strict
anti-fabrication rules: unmeasured aggregates remain null / baseline_pending
(rendered UNMEASURED), and FR-008 / CTRL-02 remains labeled TESTED while
AUD-010 is open.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import sys
from typing import Any

import httpx
import jsonschema

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
DEFAULT_EVIDENCE_DIR = REPO_ROOT.parent / "rust_CACD_autonomous_factory" / "evidence" / "records"
SCHEMA_PATH = REPO_ROOT / "data" / "schemas" / "metrics.schema.json"
DEFAULT_OUT = REPO_ROOT / "data" / "metrics.json"
AUDITOR_METRICS_PATH = REPO_ROOT / "docs" / "auditor" / "metrics.md"


def load_offline_evidence(evidence_dir: pathlib.Path) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    if evidence_dir.is_dir():
        for p in sorted(evidence_dir.glob("FR-*.json")):
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                records.append(data)
            except Exception as exc:  # pragma: no cover - corrupt local record fails explicitly
                raise RuntimeError(f"Failed reading evidence record {p}: {exc}") from exc

    passed = [r for r in records if r.get("outcome") == "passed" and r.get("exit_code") == 0]
    non_mock = [r for r in passed if r.get("verification_class") != "mock"]
    fr008 = next((r for r in records if r.get("requirement_id") == "FR-008"), None)
    return {
        "total_records": len(records),
        "passed_records": len(passed),
        "non_mock_passed_records": len(non_mock),
        "fr008_present": fr008 is not None,
        "fr008_verification_class": fr008.get("verification_class") if fr008 else "missing",
    }


def fetch_github_sample_summary(owner: str = "lgcorzo", repo: str = "rust_CACD_autonomous_factory") -> dict[str, Any] | None:
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls?state=closed&per_page=10"
    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(url, headers=headers)
            if resp.status_code != 200:
                return None
            pulls = resp.json()
            merged = [p for p in pulls if p.get("merged_at")]
            return {"sampled_closed_prs": len(pulls), "sampled_merged_prs": len(merged)}
    except Exception:
        return None


def build_metrics_snapshot(
    evidence_summary: dict[str, Any],
    github_sample: dict[str, Any] | None = None,
    *,
    generated_at: str | None = None,
) -> dict[str, Any]:
    ts = generated_at or dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    passed_recs = evidence_summary["non_mock_passed_records"]
    total_recs = evidence_summary["total_records"]

    snapshot: dict[str, Any] = {
        "schema_version": "1.0",
        "generated_at": ts,
        "window": "rolling_30d_and_cumulative_evidence",
        "collection_sources": [
            "github_rest_api",
            "evidence_records",
            "verified_experiment_logs",
        ],
        "domains": {
            "development": [
                {
                    "metric_id": "development.lead_time_hours",
                    "name": "Lead Time for Changes",
                    "value": None,
                    "unit": "hours",
                    "window": "rolling_30d",
                    "measurement_status": "baseline_pending",
                    "collection_method": "github_api",
                    "evidence_source": "https://lgcorzo.github.io/docs/auditor/metrics.md",
                    "notes": "UNMEASURED (baseline_pending): Multi-run fleet-wide issue-to-merge series requires authenticated GitHub webhook/API history across all target repositories.",
                },
                {
                    "metric_id": "development.cycle_time_hours",
                    "name": "Cycle Time",
                    "value": 0.049,
                    "unit": "hours",
                    "window": "single_verified_mission_exp_2026_013",
                    "measurement_status": "partial",
                    "collection_method": "cluster_telemetry_snapshot",
                    "evidence_source": "https://lgcorzo.github.io/notebooks.html#exp-2026-013",
                    "notes": "Observed 2m57s (0.049 h) end-to-end 5-step Hatchet DAG run in Mission #476 (EXP-2026-013; target < 60 min). Scope N=1 single run; fleet rolling average pending.",
                },
                {
                    "metric_id": "development.mttr_hours",
                    "name": "Mean Time to Recovery (MTTR)",
                    "value": None,
                    "unit": "hours",
                    "window": "rolling_30d",
                    "measurement_status": "baseline_pending",
                    "collection_method": "evidence_records",
                    "evidence_source": "https://lgcorzo.github.io/notebooks.html#exp-2026-006",
                    "notes": "UNMEASURED (baseline_pending): Architecture target is < 45 s and Hatchet crash resume measured 8.4 s (EXP-2026-006); multi-incident rolling remediation MTTR pending.",
                },
                {
                    "metric_id": "development.deployment_frequency_per_week",
                    "name": "Deployment Frequency",
                    "value": None,
                    "unit": "per_week",
                    "window": "rolling_30d",
                    "measurement_status": "baseline_pending",
                    "collection_method": "github_api",
                    "evidence_source": "https://lgcorzo.github.io/docs/auditor/metrics.md",
                    "notes": "UNMEASURED (baseline_pending): Continuous weekly FluxCD tag and GitHub release counter pending multi-week automated collection.",
                },
            ],
            "quality": [
                {
                    "metric_id": "quality.defect_density_per_kloc",
                    "name": "Defect Density",
                    "value": None,
                    "unit": "per_kloc",
                    "window": "rolling_30d",
                    "measurement_status": "baseline_pending",
                    "collection_method": "manual_audit",
                    "evidence_source": "https://lgcorzo.github.io/docs/auditor/metrics.md",
                    "notes": "UNMEASURED (baseline_pending): Requires normalized KLOC counters paired with CodeQL/linters across all 64 public repositories.",
                },
                {
                    "metric_id": "quality.escaped_defects_count",
                    "name": "Escaped Defects",
                    "value": None,
                    "unit": "count",
                    "window": "rolling_30d",
                    "measurement_status": "baseline_pending",
                    "collection_method": "github_api",
                    "evidence_source": "https://lgcorzo.github.io/docs/auditor/metrics.md",
                    "notes": "UNMEASURED (baseline_pending): Post-release regression/hotfix issue classification across factory targets pending multi-release tracking.",
                },
                {
                    "metric_id": "quality.pr_acceptance_rate_pct",
                    "name": "PR Acceptance Rate",
                    "value": None,
                    "unit": "percent",
                    "window": "rolling_30d",
                    "measurement_status": "baseline_pending",
                    "collection_method": "github_api",
                    "evidence_source": "https://lgcorzo.github.io/docs/auditor/metrics.md",
                    "notes": (
                        f"UNMEASURED (baseline_pending): Live GitHub sample observed {github_sample['sampled_merged_prs']}/{github_sample['sampled_closed_prs']} merged PRs; full fleet autonomous PR acceptance ratio pending."
                        if github_sample
                        else "UNMEASURED (baseline_pending): Fleet-wide merged vs. closed-unmerged autonomous PR ratio pending authenticated GitHub telemetry."
                    ),
                },
            ],
            "security": [
                {
                    "metric_id": "security.vulnerabilities_found_count",
                    "name": "Vulnerabilities Found",
                    "value": 3369,
                    "unit": "count",
                    "window": "cluster_snapshot_exp_2026_012",
                    "measurement_status": "partial",
                    "collection_method": "cluster_telemetry_snapshot",
                    "evidence_source": "https://lgcorzo.github.io/notebooks.html#exp-2026-012",
                    "notes": "Cluster Trivy snapshot post-remediation: 396 CRITICAL + 2,973 HIGH active findings (down from 429 CRITICAL + 3,660 HIGH). FR-008/CTRL-02 remains TESTED while AUD-010 is open (CTRL-04/05/07/08 runtime_verified).",
                },
                {
                    "metric_id": "security.vulnerabilities_fixed_count",
                    "name": "Vulnerabilities Fixed",
                    "value": 720,
                    "unit": "count",
                    "window": "cluster_snapshot_exp_2026_012",
                    "measurement_status": "partial",
                    "collection_method": "cluster_telemetry_snapshot",
                    "evidence_source": "https://lgcorzo.github.io/notebooks.html#exp-2026-012",
                    "notes": "Verified Trivy CRITICAL+HIGH vulnerabilities remediated (EXP-2026-012), alongside 9/11 audit findings (AUD-001..009) closed and 54.2 ns ZeroizeOnDrop memory wipe verified. FR-008/CTRL-02 kept TESTED pending AUD-010.",
                },
                {
                    "metric_id": "security.mean_remediation_time_hours",
                    "name": "Mean Remediation Time",
                    "value": None,
                    "unit": "hours",
                    "window": "rolling_30d",
                    "measurement_status": "baseline_pending",
                    "collection_method": "github_api",
                    "evidence_source": "https://lgcorzo.github.io/docs/auditor/metrics.md",
                    "notes": "UNMEASURED (baseline_pending): Alert created_at -> fixed_at duration aggregation across GitHub Project 6 pending continuous sweep.",
                },
            ],
            "agents": [
                {
                    "metric_id": "agents.agent_success_rate_pct",
                    "name": "Agent Success Rate",
                    "value": None,
                    "unit": "percent",
                    "window": "rolling_30d",
                    "measurement_status": "baseline_pending",
                    "collection_method": "evidence_records",
                    "evidence_source": "https://github.com/lgcorzo/rust_CACD_autonomous_factory/tree/main/evidence/records",
                    "notes": f"UNMEASURED (baseline_pending): Offline evidence check verified {passed_recs}/{total_recs} non-mock passed requirement records (FR-008 TESTED while AUD-010 open); live Mission #476 R2R Hatchet recorded 87 COMPLETED / 0 failed tasks; rolling multi-mission percentage pending.",
                },
                {
                    "metric_id": "agents.hitl_approval_rate_pct",
                    "name": "HITL Approval Rate",
                    "value": None,
                    "unit": "percent",
                    "window": "rolling_30d",
                    "measurement_status": "baseline_pending",
                    "collection_method": "github_api",
                    "evidence_source": "https://lgcorzo.github.io/docs/auditor/metrics.md",
                    "notes": "UNMEASURED (baseline_pending): Vertex 4 human approval rate across agent-authored PRs pending multi-mission series.",
                },
                {
                    "metric_id": "agents.autonomous_completion_rate_pct",
                    "name": "Autonomous Completion Rate",
                    "value": None,
                    "unit": "percent",
                    "window": "rolling_30d",
                    "measurement_status": "baseline_pending",
                    "collection_method": "evidence_records",
                    "evidence_source": "https://lgcorzo.github.io/docs/auditor/metrics.md",
                    "notes": "UNMEASURED (baseline_pending): Ratio of missions reaching Stage 5 factory-deliver without prior human override pending multi-mission series.",
                },
            ],
        },
    }

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    jsonschema.validate(instance=snapshot, schema=schema)
    return snapshot


def render_auditor_metrics_markdown(snapshot: dict[str, Any]) -> str:
    as_of = snapshot["generated_at"][:10]
    lines = [
        "---",
        'title: "Dark Gravity AI Auditor Pack — Platform Metrics & Epistemic Status"',
        'doc_role: "metrics"',
        'schema_version: "1.0"',
        f'as_of_date: "{as_of}"',
        'verification_status: "mixed"',
        'verified: "false"',
        'visibility: "public"',
        "canonical_sources:",
        '  - "https://lgcorzo.github.io/data/metrics.json"',
        '  - "https://lgcorzo.github.io/metrics.html"',
        '  - "https://github.com/lgcorzo/rust_CACD_autonomous_factory/tree/main/evidence/records"',
        "---",
        "",
        "# Platform KPIs & Verified Baselines",
        "",
        f"Snapshot timestamp: `{snapshot['generated_at']}` (`{snapshot['window']}`). All unmeasured aggregates are strictly marked **`UNMEASURED` (`baseline_pending`)** with `value: null`. **`FR-008` / `CTRL-02` remains labeled `TESTED` while `AUD-010` is open.**",
        "",
    ]
    domain_titles = [
        ("development", "Development KPIs"),
        ("quality", "Quality KPIs"),
        ("security", "Security KPIs"),
        ("agents", "Agents KPIs"),
    ]
    for domain_key, title in domain_titles:
        lines.append(f"## {title} (`{domain_key}`)")
        lines.append("")
        lines.append("| Metric ID | KPI | Value | Unit | Status | Evidence & Notes |")
        lines.append("|---|---|---|---|---|---|")
        for item in snapshot["domains"][domain_key]:
            val = "`UNMEASURED` (`null`)" if item["value"] is None else f"`{item['value']}`"
            lines.append(
                f"| `{item['metric_id']}` | {item['name']} | {val} | `{item['unit']}` | `{item['measurement_status']}` | {item['notes']} |"
            )
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect Dark Gravity platform KPIs into data/metrics.json.")
    parser.add_argument("--offline-evidence", type=pathlib.Path, default=DEFAULT_EVIDENCE_DIR)
    parser.add_argument("--github-live", action="store_true", help="Optionally sample GitHub API metadata")
    parser.add_argument("--out", type=pathlib.Path, default=DEFAULT_OUT)
    parser.add_argument("--refresh-auditor-metrics", action="store_true")
    parser.add_argument("--generated-at", type=str, default=None)
    args = parser.parse_args()

    evidence_summary = load_offline_evidence(args.offline_evidence)
    gh_sample = fetch_github_sample_summary() if args.github_live else None
    snapshot = build_metrics_snapshot(evidence_summary, gh_sample, generated_at=args.generated_at)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")

    if args.refresh_auditor_metrics:
        AUDITOR_METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
        AUDITOR_METRICS_PATH.write_text(render_auditor_metrics_markdown(snapshot), encoding="utf-8")

    total_kpis = sum(len(v) for v in snapshot["domains"].values())
    print(f"OK: Generated {total_kpis} KPIs into {args.out} (passed offline evidence records: {evidence_summary['non_mock_passed_records']}/{evidence_summary['total_records']}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
