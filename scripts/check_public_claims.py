#!/usr/bin/env python3
"""Deterministic consistency checker for lgcorzo.github.io public claims (T040).

Compares data/canonical-claims.json against index.html, architecture.html,
lifecycle.html, notebooks.html, fork-policy.html, and sovereignty.html.
Requires zero external network calls or privileged tokens.
"""

from __future__ import annotations

import json
import pathlib
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
CANONICAL_PATH = REPO_ROOT / "data" / "canonical-claims.json"

REQUIRED_PAGES = [
    "index.html",
    "architecture.html",
    "lifecycle.html",
    "notebooks.html",
    "fork-policy.html",
    "sovereignty.html",
]


def main() -> int:
    errors: list[str] = []

    if not CANONICAL_PATH.is_file():
        print(f"ERROR: Missing canonical claims file: {CANONICAL_PATH}", file=sys.stderr)
        return 1

    canonical = json.loads(CANONICAL_PATH.read_text(encoding="utf-8"))
    stats = canonical.get("repository_statistics", {})
    public_total = stats.get("public_repositories_total")
    original_count = stats.get("original_repositories")
    fork_count = stats.get("maintained_forks")
    cat_counts = stats.get("fork_category_counts", {})

    if original_count + fork_count != public_total:
        errors.append(
            f"Canonical math mismatch: original ({original_count}) + forks ({fork_count}) != total ({public_total})"
        )
    if sum(cat_counts.values()) != fork_count:
        errors.append(
            f"Canonical fork category sum ({sum(cat_counts.values())}) != maintained_forks ({fork_count})"
        )

    pages: dict[str, str] = {}
    for page_name in REQUIRED_PAGES:
        p = REPO_ROOT / page_name
        if not p.is_file():
            errors.append(f"Missing required HTML page: {page_name}")
        else:
            pages[page_name] = p.read_text(encoding="utf-8")

    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1

    # 1. Verify repository statistics consistency across index.html, fork-policy.html, notebooks.html
    if f"{public_total} public repositories" not in pages["index.html"]:
        errors.append(f"index.html missing canonical '{public_total} public repositories' count")
    if f"{fork_count} maintained" not in pages["index.html"]:
        errors.append(f"index.html missing canonical '{fork_count} maintained' forks count")
    if f"Out of {public_total} public repositories across the lab, {fork_count} are maintained" not in pages["fork-policy.html"]:
        errors.append(
            f"fork-policy.html missing canonical '{public_total} public repositories / {fork_count} forks' statement"
        )
    if "64 public" not in pages["notebooks.html"]:
        errors.append(
            "notebooks.html mentions 69 repositories without reconciling against the 64 public repositories (22 original + 42 forks) canonical statistic"
        )

    # 2. Verify Hatchet 5-step lifecycle consistency across pages
    if "5-phase durable mission pipeline" not in pages["index.html"]:
        errors.append("index.html missing canonical '5-phase durable mission pipeline'")
    if "five Hatchet steps" not in pages["architecture.html"]:
        errors.append("architecture.html missing canonical 'five Hatchet steps'")
    if "same five\n          steps" not in pages["lifecycle.html"] and "five steps" not in pages["lifecycle.html"]:
        errors.append("lifecycle.html missing canonical five-step workflow reference")
    if "6-phase DAG" in pages["notebooks.html"] and "5 Hatchet" not in pages["notebooks.html"]:
        errors.append(
            "notebooks.html contains unqualified '6-phase DAG' without clarifying Kafka ingestion + 5 Hatchet phases"
        )

    # 3. Verify compliance / certification qualification consistency
    if "No third-party certification (EU AI Act, SOC 2 or other) is claimed." not in pages["index.html"]:
        errors.append("index.html missing mandatory compliance qualification statement")
    for name, content in pages.items():
        if "SOC 2 Type II compliance in" in content:
            errors.append(
                f"{name} contains unqualified 'SOC 2 Type II compliance in' claim contradicting index.html"
            )

    # 4. Verify every canonical fact has non-empty evidence_source and valid status
    valid_statuses = {
        "designed",
        "implemented",
        "tested",
        "deployed",
        "runtime_verified",
        "verified",
        "experimental",
        "unverified",
    }
    
    # Priority 7 (DG-RVP-014 §9): Verify actual evidence records, SHA-256 digests, and qualifying classes
    factory_repo_root = (REPO_ROOT.parent / "rust_CACD_autonomous_factory").resolve()
    has_factory_repo = (factory_repo_root / "evidence").is_dir()
    
    for fact in canonical.get("canonical_facts", []):
        fid = fact.get("fact_id", "<unknown>")
        status = fact.get("verification_status")
        if status not in valid_statuses:
            errors.append(f"Fact {fid} has invalid verification_status '{status}'")
        evidence_src = fact.get("evidence_source", "")
        if not evidence_src.startswith("https://"):
            errors.append(f"Fact {fid} is missing a valid https:// evidence_source link")
            
        # For verified / runtime_verified claims, validate underlying evidence record
        if status in ("verified", "runtime_verified") and has_factory_repo:
            if "live-gvisor-isolation.json" in evidence_src:
                rel_ev_file = "evidence/security/live-gvisor-isolation.json"
                ev_path = factory_repo_root / rel_ev_file
                if not ev_path.is_file():
                    errors.append(f"Fact {fid} references missing live evidence file: {rel_ev_file}")
                else:
                    try:
                        ev_data = json.loads(ev_path.read_text(encoding="utf-8"))
                        # Verify structured telemetry exists and gVisor isolation was corroborated
                        checks = ev_data.get("checks", [])
                        gvisor_checks = [c for c in checks if "gvisor" in c.get("check_id", "").lower() or "runtime_verified" in c.get("classification", "").lower()]
                        if not gvisor_checks:
                            errors.append(f"Fact {fid} live-gvisor-isolation.json lacks verified gVisor runtime checks")
                    except Exception as e:
                        errors.append(f"Fact {fid} corrupt live evidence JSON {rel_ev_file}: {e}")
            elif "records/" in evidence_src or evidence_src.endswith(".json"):
                # If pointing to an evidence record, ensure it is non-mock, exit_code 0, passed
                filename = evidence_src.split("/")[-1]
                rec_path = factory_repo_root / "evidence" / "records" / filename
                if rec_path.is_file():
                    try:
                        rec_data = json.loads(rec_path.read_text(encoding="utf-8"))
                        if rec_data.get("outcome") != "passed":
                            errors.append(f"Fact {fid} evidence record {filename} outcome is '{rec_data.get('outcome')}', expected 'passed'")
                        if rec_data.get("exit_code") != 0:
                            errors.append(f"Fact {fid} evidence record {filename} exit_code is {rec_data.get('exit_code')}, expected 0")
                        if rec_data.get("verification_class") == "mock":
                            errors.append(f"Fact {fid} backed by mock evidence class, forbidden for verified status")
                    except Exception as e:
                        errors.append(f"Fact {fid} corrupt evidence record {filename}: {e}")

    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1

    print(
        f"OK: Verified {len(canonical.get('canonical_facts', []))} canonical facts and repository statistics across {len(REQUIRED_PAGES)} pages."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
