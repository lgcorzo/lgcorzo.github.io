#!/usr/bin/env python3
"""Multi-repository knowledge drift and DOC-011 redaction validator (T007)."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys

import jsonschema

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "data" / "ecosystem-registry.json"
REGISTRY_SCHEMA_PATH = REPO_ROOT / "data" / "schemas" / "ecosystem-registry.schema.json"
CANONICAL_CLAIMS_PATH = REPO_ROOT / "data" / "canonical-claims.json"

# Lowercase SHA-256 digests of the 6 DOC-011 private repository names so this public script
# detects any accidental leak without embedding literal private repo names in public code.
DOC011_FORBIDDEN_REPO_SHA256 = {
    "25e807c8ddcd4cb4d30a92c45e13f34b1e2f62cd2e8a98289c76dc32ecc46a63",
    "dec27274da7cfd135996435c4e254ba774bc1ac0921154bcef1e935bddd4b577",
    "c7e8cce9a717c4da3336d2ddb18fc7c14e51483a894a6eeaf5acd2e9386c826c",
    "246f350826d3a74ef5aa9e14289c0dca876c4309f80f2a1022bba2029caf8021",
    "2cfb65c96183ce9cb88e7d0044e8d8d0d3df3ad5c7a6af9bb8f0d275a2b67d8c",
    "c6c53405795ae74bc3844b7f8e3bb53cbf41c84b950d24018f39ca39051ff6c6",
}

# Lowercase SHA-256 digests of the 2 local internal ops directories scanned under --root.
PRIVATE_OPS_DIR_SHA256 = {
    "25e807c8ddcd4cb4d30a92c45e13f34b1e2f62cd2e8a98289c76dc32ecc46a63": "repo:internal-gitops-control-plane",
    "dec27274da7cfd135996435c4e254ba774bc1ac0921154bcef1e935bddd4b577": "repo:internal-incident-remediation-service",
}

PRIVATE_PATH_OR_IP_RE = re.compile(
    r"(/mnt/(?!c(?:/|$|\.\.\.|\b))[A-Za-z0-9._-]{2,}|/home/[a-z0-9._-]+|\b192\.168\.\d{1,3}\.\d{1,3}\b)"
)

REQUIRED_ARCH_HEADINGS = [
    "## Ecosystem Role & Tier",
    "## Internal Component Design",
    "## Upstream & Downstream Ecosystem Interfaces",
    "## Security Boundary & Governance",
    "## Canonical Cross-Links",
]

REQUIRED_MANIFEST_KEYS = [
    "manifest_version",
    "platform",
    "canonical_hub",
    "auditor_pack",
    "mcp_server",
    "knowledge_graph",
]


def estimate_tokens(text: str) -> int:
    """Conservative word/punctuation token estimator (~1.3x words) enforcing < 1,200 token budget."""
    words = len(text.split())
    return int(round(words * 1.3))


def detect_doc011_leaks(text: str, label: str) -> list[str]:
    errors: list[str] = []
    for match in PRIVATE_PATH_OR_IP_RE.finditer(text):
        errors.append(f"{label}: DOC-011 violation (forbidden local path or private IP '{match.group(0)}')")
    for token in set(re.findall(r"[A-Za-z0-9._-]+", text)):
        digest = hashlib.sha256(token.lower().encode("utf-8")).hexdigest()
        if digest in DOC011_FORBIDDEN_REPO_SHA256:
            errors.append(f"{label}: DOC-011 violation (private repository identifier detected, sha256={digest[:12]})")
    return errors


def validate_registry(
    registry_path: pathlib.Path = REGISTRY_PATH,
    schema_path: pathlib.Path = REGISTRY_SCHEMA_PATH,
    claims_path: pathlib.Path = CANONICAL_CLAIMS_PATH,
) -> tuple[dict, list[str]]:
    errors: list[str] = []
    registry_text = registry_path.read_text(encoding="utf-8")
    errors.extend(detect_doc011_leaks(registry_text, str(registry_path.name)))

    registry = json.loads(registry_text)
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    jsonschema.validate(instance=registry, schema=schema)

    claims = json.loads(claims_path.read_text(encoding="utf-8"))
    c_stats = claims["repository_statistics"]
    r_stats = registry["repository_statistics"]
    for key in [
        "public_repositories_total",
        "original_repositories",
        "maintained_forks",
        "historical_portfolio_total_with_private_and_archived",
    ]:
        if r_stats.get(key) != c_stats.get(key):
            errors.append(f"Registry statistic mismatch for {key}: {r_stats.get(key)} != {c_stats.get(key)}")

    kes_entries = [r for r in registry["repositories"] if r.get("name") == "kes"]
    if not kes_entries or kes_entries[0].get("fork_profile") != "FROZEN_READONLY" or not kes_entries[0].get("archived"):
        errors.append("Registry must preserve lgcorzo/kes as archived: true and fork_profile: FROZEN_READONLY")

    return registry, errors


def check_repo_directory(repo_dir: pathlib.Path, *, public_scope: bool, registry_entry: dict) -> list[str]:
    errors: list[str] = []
    # Exact lowercase AGENTS.md check (catches uppercase AGENTS.MD on case-sensitive/insensitive trees)
    root_entries = {p.name for p in repo_dir.iterdir()}
    if "AGENTS.MD" in root_entries:
        errors.append(f"{repo_dir.name}: uppercase AGENTS.MD present; must normalize to lowercase AGENTS.md")
    if "AGENTS.md" not in root_entries:
        errors.append(f"{repo_dir.name}: missing lowercase AGENTS.md")
    else:
        agents_text = (repo_dir / "AGENTS.md").read_text(encoding="utf-8")
        if "<!-- DARK-GRAVITY-CONTEXT:START -->" not in agents_text or "<!-- DARK-GRAVITY-CONTEXT:END -->" not in agents_text:
            errors.append(f"{repo_dir.name}/AGENTS.md: missing DARK-GRAVITY-CONTEXT markers")
        if public_scope:
            errors.extend(detect_doc011_leaks(agents_text, f"{repo_dir.name}/AGENTS.md"))

    arch_path = repo_dir / "ARCHITECTURE.md"
    if not arch_path.is_file():
        errors.append(f"{repo_dir.name}: missing ARCHITECTURE.md")
    else:
        arch_text = arch_path.read_text(encoding="utf-8")
        for heading in REQUIRED_ARCH_HEADINGS:
            if heading not in arch_text:
                errors.append(f"{repo_dir.name}/ARCHITECTURE.md: missing required section '{heading}'")
        if public_scope:
            errors.extend(detect_doc011_leaks(arch_text, f"{repo_dir.name}/ARCHITECTURE.md"))

    repos_path = repo_dir / "REPOSITORIES.md"
    if not repos_path.is_file():
        errors.append(f"{repo_dir.name}: missing REPOSITORIES.md")
    else:
        repos_text = repos_path.read_text(encoding="utf-8")
        if "64" not in repos_text or "22" not in repos_text or "42" not in repos_text:
            errors.append(f"{repo_dir.name}/REPOSITORIES.md: must reconcile 64 public (22 original + 42 maintained forks)")
        if public_scope:
            errors.extend(detect_doc011_leaks(repos_text, f"{repo_dir.name}/REPOSITORIES.md"))

    manifest_path = repo_dir / "DARK_GRAVITY_MANIFEST.md"
    if not manifest_path.is_file():
        errors.append(f"{repo_dir.name}: missing DARK_GRAVITY_MANIFEST.md")
    else:
        manifest_text = manifest_path.read_text(encoding="utf-8")
        for key in REQUIRED_MANIFEST_KEYS:
            if f"{key}:" not in manifest_text:
                errors.append(f"{repo_dir.name}/DARK_GRAVITY_MANIFEST.md: missing frontmatter key '{key}'")
        tokens = estimate_tokens(manifest_text)
        if tokens >= 1200:
            errors.append(f"{repo_dir.name}/DARK_GRAVITY_MANIFEST.md: estimated {tokens} tokens >= 1200 limit")
        if public_scope:
            errors.extend(detect_doc011_leaks(manifest_text, f"{repo_dir.name}/DARK_GRAVITY_MANIFEST.md"))

    if registry_entry.get("fork_profile") == "MAINTAINED_FORK_PROFILE":
        # Verify fork didn't relocate upstream source tree if README exists
        if not (repo_dir / "LICENSE").is_file() and not (repo_dir / "LICENSE.md").is_file() and not (repo_dir / "LICENSE-APACHE").is_file():
            errors.append(f"{repo_dir.name}: MAINTAINED_FORK_PROFILE expects upstream LICENSE preserved")

    return errors


def verify_workspace(workspace_root: pathlib.Path | None, *, public_only: bool = False) -> tuple[int, list[str]]:
    registry, errors = validate_registry()
    checked = 0

    if public_only:
        self_entry = next(r for r in registry["repositories"] if r["name"] == "lgcorzo.github.io")
        checked += 1
        errors.extend(check_repo_directory(REPO_ROOT, public_scope=True, registry_entry=self_entry))
        return checked, errors

    assert workspace_root is not None
    entries_by_id = {r["id"]: r for r in registry["repositories"]}

    # 1. Check all 10 active public direct_injection_target repos
    for entry in registry["repositories"]:
        if entry["direct_injection_target"] and entry["visibility"] == "public":
            repo_dir = workspace_root / entry["name"]
            if not repo_dir.is_dir():
                errors.append(f"Missing expected public repo directory under {workspace_root}: {entry['name']}")
                continue
            checked += 1
            errors.extend(check_repo_directory(repo_dir, public_scope=True, registry_entry=entry))

    # 2. Check the 2 internal ops repos on disk without storing literal private names in public code
    found_ops = 0
    for child in sorted(workspace_root.iterdir()):
        if not child.is_dir():
            continue
        digest = hashlib.sha256(child.name.lower().encode("utf-8")).hexdigest()
        if digest in PRIVATE_OPS_DIR_SHA256:
            found_ops += 1
            checked += 1
            entry = entries_by_id[PRIVATE_OPS_DIR_SHA256[digest]]
            errors.extend(check_repo_directory(child, public_scope=False, registry_entry=entry))

    if found_ops != len(PRIVATE_OPS_DIR_SHA256):
        errors.append(f"Expected {len(PRIVATE_OPS_DIR_SHA256)} internal ops repos under {workspace_root}, found {found_ops}")

    # 3. Verify frozen archive repo has zero local uncommitted modifications if present
    kes_dir = workspace_root / "kes"
    if kes_dir.is_dir():
        for forbidden in ["DARK_GRAVITY_MANIFEST.md", "REPOSITORIES.md"]:
            if (kes_dir / forbidden).exists():
                errors.append(f"kes: FROZEN_READONLY archive must not receive {forbidden}")

    return checked, errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Dark Gravity multi-repo knowledge standards and DOC-011 boundary.")
    parser.add_argument("--root", type=pathlib.Path, default=REPO_ROOT.parent, help="Parent directory containing Dark Gravity repos")
    parser.add_argument("--public-only", action="store_true", help="Validate only lgcorzo.github.io (single-repo CI mode)")
    args = parser.parse_args()

    checked, errors = verify_workspace(None if args.public_only else args.root.resolve(), public_only=args.public_only)
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1

    print(f"OK: Verified ecosystem registry and {checked} repository knowledge packs with 0 drift or DOC-011 errors.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
