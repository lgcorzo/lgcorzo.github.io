from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
CANONICAL_PATH = REPO_ROOT / "data" / "canonical-claims.json"
CHECKER_SCRIPT = REPO_ROOT / "scripts" / "check_public_claims.py"
HTML_PAGES = [
    "index.html",
    "architecture.html",
    "lifecycle.html",
    "notebooks.html",
    "fork-policy.html",
]


def test_canonical_claims_file_exists_and_has_required_schema() -> None:
    assert CANONICAL_PATH.is_file(), f"Missing canonical claims source: {CANONICAL_PATH}"
    data = json.loads(CANONICAL_PATH.read_text(encoding="utf-8"))
    assert data.get("schema_version") == "1.0"
    assert "as_of_date" in data
    assert "repository_statistics" in data
    assert "canonical_facts" in data
    stats = data["repository_statistics"]
    assert stats["public_repositories_total"] == 64
    assert stats["original_repositories"] == 22
    assert stats["maintained_forks"] == 42
    assert stats["historical_portfolio_total_with_private_and_archived"] == 69


def test_no_contradictory_unqualified_69_repositories_claim() -> None:
    """Any mention of '69 repositories' or '69 Repos' must be explicitly qualified as the
    historical/total portfolio including private and archived repos, never contradicting
    the 64 public repositories (22 original + 42 forks) count."""
    notebooks_html = (REPO_ROOT / "notebooks.html").read_text(encoding="utf-8")
    assert "64 public" in notebooks_html, (
        "notebooks.html mentions 69 repositories without clarifying the 64 public repositories "
        "(22 original + 42 forks) vs 5 private/archived repositories distinction"
    )


def test_no_unqualified_eu_ai_act_or_soc2_compliance_claim() -> None:
    """index.html states 'No third-party certification (EU AI Act, SOC 2 or other) is claimed.'
    Other pages must not claim active 'EU AI Act Conformity Assessment & SOC 2 Type II compliance'
    without qualifying it as architectural readiness."""
    for page in HTML_PAGES:
        text = (REPO_ROOT / page).read_text(encoding="utf-8")
        assert "SOC 2 Type II compliance in" not in text, (
            f"{page} contains unqualified 'SOC 2 Type II compliance' claim contradicting index.html"
        )


def test_hatchet_phase_count_consistency_across_pages() -> None:
    """Canonical mission workflow has 5 Hatchet phases (rustant-plan, zeroclaw-execute,
    zeroclaw-validate, rustant-review, factory-deliver). Screencast notes mentioning 6 phases
    must explicitly clarify that Kafka ingestion is counted alongside the 5 Hatchet phases."""
    notebooks_html = (REPO_ROOT / "notebooks.html").read_text(encoding="utf-8")
    if "6-phase DAG" in notebooks_html:
        assert "5 Hatchet" in notebooks_html, (
            "notebooks.html mentions '6-phase DAG' without reconciling against the canonical 5 Hatchet phases"
        )


def test_check_public_claims_script_passes() -> None:
    assert CHECKER_SCRIPT.is_file(), f"Missing checker script: {CHECKER_SCRIPT}"
    proc = subprocess.run(
        [sys.executable, str(CHECKER_SCRIPT)],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, f"check_public_claims.py failed:\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
