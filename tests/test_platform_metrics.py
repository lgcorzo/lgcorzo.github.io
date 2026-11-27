from __future__ import annotations

import json
import pathlib
import sys

import jsonschema

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import verify_ecosystem_knowledge as vek  # noqa: E402

METRICS_PATH = REPO_ROOT / "data" / "metrics.json"
METRICS_SCHEMA = REPO_ROOT / "data" / "schemas" / "metrics.schema.json"
AUDITOR_METRICS_MD = REPO_ROOT / "docs" / "auditor" / "metrics.md"

REQUIRED_KPIS = {
    "development": {
        "development.lead_time_hours",
        "development.cycle_time_hours",
        "development.mttr_hours",
        "development.deployment_frequency_per_week",
    },
    "quality": {
        "quality.defect_density_per_kloc",
        "quality.escaped_defects_count",
        "quality.pr_acceptance_rate_pct",
    },
    "security": {
        "security.vulnerabilities_found_count",
        "security.vulnerabilities_fixed_count",
        "security.mean_remediation_time_hours",
    },
    "agents": {
        "agents.agent_success_rate_pct",
        "agents.hitl_approval_rate_pct",
        "agents.autonomous_completion_rate_pct",
    },
}


def test_metrics_schema_and_all_13_kpis_present() -> None:
    raw = METRICS_PATH.read_text(encoding="utf-8")
    assert not vek.detect_doc011_leaks(raw, "data/metrics.json")

    snapshot = json.loads(raw)
    schema = json.loads(METRICS_SCHEMA.read_text(encoding="utf-8"))
    jsonschema.validate(instance=snapshot, schema=schema)

    for domain, expected_ids in REQUIRED_KPIS.items():
        actual_ids = {item["metric_id"] for item in snapshot["domains"][domain]}
        assert actual_ids == expected_ids


def test_metrics_anti_fabrication_and_epistemic_rules() -> None:
    snapshot = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    all_items = [item for items in snapshot["domains"].values() for item in items]

    for item in all_items:
        if item["measurement_status"] == "baseline_pending":
            assert item["value"] is None, f"{item['metric_id']}: baseline_pending must set value=null"
            assert "UNMEASURED" in item["notes"]
        else:
            assert item["value"] is not None
        assert item["measurement_status"] in {"verified", "partial", "baseline_pending"}

    sec_text = json.dumps(snapshot["domains"]["security"])
    assert "TESTED" in sec_text and "AUD-010" in sec_text


def test_auditor_metrics_markdown_synced_with_json() -> None:
    snapshot = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    md = AUDITOR_METRICS_MD.read_text(encoding="utf-8")
    assert not vek.detect_doc011_leaks(md, "docs/auditor/metrics.md")
    for expected_ids in REQUIRED_KPIS.values():
        for mid in expected_ids:
            assert mid in md, f"docs/auditor/metrics.md missing KPI {mid}"
    assert snapshot["generated_at"][:10] in md
