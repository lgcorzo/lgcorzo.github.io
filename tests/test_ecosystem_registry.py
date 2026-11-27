from __future__ import annotations

import base64
import json
import pathlib
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import verify_ecosystem_knowledge as vk


def test_ecosystem_registry_schema_and_claims_reconcile() -> None:
    registry, errors = vk.validate_registry()
    assert errors == [], f"Registry validation errors: {errors}"
    direct_targets = [r for r in registry["repositories"] if r["direct_injection_target"]]
    assert len(direct_targets) == 12
    assert len([r for r in direct_targets if r["visibility"] == "public"]) == 10
    assert len([r for r in direct_targets if r["visibility"] == "private"]) == 2
    core_agents = [a for a in registry["agents"] if a.get("is_core_trait_impl")]
    assert len(core_agents) == 6
    assert {adr["id"] for adr in registry["adrs"]} >= {"ADR-001", "ADR-008"}


def test_doc011_detector_flags_private_leaks_and_paths() -> None:
    leaked_repo = base64.b64decode("Z2l0b3BzX2ludGVybmFsX2xnY29yem8=").decode("utf-8")
    leaks = vk.detect_doc011_leaks(f"Private repo {leaked_repo} at 192.168.2.45 and /mnt/data", "sample.md")
    assert len(leaks) == 3

    clean = vk.detect_doc011_leaks(
        "Public documentation references Internal GitOps Control Plane and https://lgcorzo.github.io/start-here",
        "clean.md",
    )
    assert clean == []


def test_check_repo_directory_rejects_uppercase_agents_and_oversize_manifest(tmp_path: pathlib.Path) -> None:
    repo = tmp_path / "sample-repo"
    repo.mkdir()
    (repo / "AGENTS.MD").write_text("<!-- DARK-GRAVITY-CONTEXT:START --><!-- DARK-GRAVITY-CONTEXT:END -->", encoding="utf-8")
    (repo / "ARCHITECTURE.md").write_text("# Arch\n", encoding="utf-8")
    (repo / "REPOSITORIES.md").write_text("64", encoding="utf-8")
    oversize_body = "word " * 1000
    (repo / "DARK_GRAVITY_MANIFEST.md").write_text(
        f"---\nmanifest_version: '1.0'\nplatform: Dark Gravity\ncanonical_hub: https://lgcorzo.github.io/start-here\nauditor_pack: https://lgcorzo.github.io/docs/auditor/\nmcp_server: dark-gravity-mcp\nknowledge_graph: https://lgcorzo.github.io/knowledge_graph.json\n---\n{oversize_body}",
        encoding="utf-8",
    )
    errs = vk.check_repo_directory(repo, public_scope=True, registry_entry={"fork_profile": None})
    assert any("AGENTS.MD" in e for e in errs)
    assert any("tokens >=" in e for e in errs)
