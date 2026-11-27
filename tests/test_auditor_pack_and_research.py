from __future__ import annotations

import pathlib
import re
import sys

import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import verify_ecosystem_knowledge as vek  # noqa: E402

AUDITOR_DIR = REPO_ROOT / "docs" / "auditor"
EXPECTED_AUDITOR_ROLES = [
    "executive-summary",
    "architecture",
    "research",
    "metrics",
    "ecosystem",
]
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)


def parse_frontmatter(path: pathlib.Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    assert m is not None, f"{path.name}: missing YAML frontmatter"
    meta = yaml.safe_load(m.group(1))
    assert isinstance(meta, dict), f"{path.name}: frontmatter must parse as mapping"
    return meta, text[m.end() :]


def test_auditor_pack_documents_and_frontmatter() -> None:
    for role in EXPECTED_AUDITOR_ROLES:
        path = AUDITOR_DIR / f"{role}.md"
        assert path.is_file(), f"Missing auditor pack document: {path}"
        meta, body = parse_frontmatter(path)
        assert meta.get("doc_role") == role
        assert meta.get("schema_version") == "1.0"
        assert meta.get("visibility") == "public"
        assert meta.get("verified") == "false", (
            f"{path.name}: generated/repo auditor doc must default verified: 'false'"
        )
        sources = meta.get("canonical_sources", [])
        assert isinstance(sources, list) and len(sources) >= 2
        assert all(isinstance(s, str) and s.startswith("https://") for s in sources)
        assert len(body.strip()) > 200
        leaks = vek.detect_doc011_leaks(path.read_text(encoding="utf-8"), f"docs/auditor/{role}.md")
        assert not leaks, f"DOC-011 leaks in {path.name}: {leaks}"


def test_research_covers_rq1_through_rq4() -> None:
    text = (REPO_ROOT / "RESEARCH.md").read_text(encoding="utf-8")
    for rq in ("RQ1", "RQ2", "RQ3", "RQ4"):
        assert rq in text, f"RESEARCH.md missing {rq}"
    assert "No third-party certification" in text or "no third-party certification" in text
    assert "TESTED" in text and "AUD-010" in text
    assert not vek.detect_doc011_leaks(text, "RESEARCH.md")


def test_experiments_covers_exp_001_through_014() -> None:
    text = (REPO_ROOT / "EXPERIMENTS.md").read_text(encoding="utf-8")
    for idx in range(1, 15):
        exp_id = f"EXP-2026-{idx:03d}"
        assert exp_id in text, f"EXPERIMENTS.md missing {exp_id}"
        anchor = f"#exp-2026-{idx:03d}"
        assert anchor in text, f"EXPERIMENTS.md missing notebooks anchor {anchor}"
    assert "64" in text and "69" in text
    assert not vek.detect_doc011_leaks(text, "EXPERIMENTS.md")


def test_unified_portal_sections_and_internal_links() -> None:
    start_pages = [REPO_ROOT / "start-here" / "index.html", REPO_ROOT / "start-here.html"]
    required_ids = [
        "executive-summary",
        "architecture-overview",
        "repository-map",
        "research-vision",
        "experiments-catalog",
        "platform-metrics",
        "ai-agent-entry",
    ]
    for page in start_pages:
        assert page.is_file(), f"Missing portal page: {page}"
        html = page.read_text(encoding="utf-8")
        for sec_id in required_ids:
            assert f'id="{sec_id}"' in html, f"{page.name} missing section id='{sec_id}'"
        assert not vek.detect_doc011_leaks(html, str(page.relative_to(REPO_ROOT)))

    agents_page = REPO_ROOT / "ai-agents" / "index.html"
    assert agents_page.is_file()
    agents_html = agents_page.read_text(encoding="utf-8")
    for tool_name in (
        "get_architecture",
        "get_research",
        "get_repository_map",
        "get_adrs",
        "get_experiments",
        "get_metrics",
    ):
        assert tool_name in agents_html, f"ai-agents/index.html missing MCP tool '{tool_name}'"
    assert not vek.detect_doc011_leaks(agents_html, "ai-agents/index.html")

    href_re = re.compile(r'href="([^"]+)"')
    for page in [*start_pages, agents_page]:
        html = page.read_text(encoding="utf-8")
        for raw_href in href_re.findall(html):
            if raw_href.startswith(("http://", "https://", "#", "mailto:", "data:")):
                continue
            target_part = raw_href.split("#", 1)[0]
            if not target_part:
                continue
            resolved = (page.parent / target_part).resolve()
            if target_part.endswith("/"):
                resolved_index = resolved / "index.html"
                exists = resolved_index.is_file()
            else:
                exists = resolved.is_file() or (resolved / "index.html").is_file()
            assert exists, f"Broken relative link in {page.relative_to(REPO_ROOT)}: href='{raw_href}' -> {resolved}"
