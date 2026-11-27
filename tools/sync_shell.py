#!/usr/bin/env python3
"""Keep the header, footer and prev/next pager identical on every page.

Each page holds three marker pairs, e.g.
  <!--SHELL:HEADER--> ... <!--/SHELL:HEADER-->
This script rewrites what sits between the markers using depth-aware relative URLs
so root pages and subdirectory pages (/start-here/, /ai-agents/) stay consistent.
Run after editing: python3 tools/sync_shell.py
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = [  # (file, nav label, one-line description used by the pager, title tooltip)
    ("index.html", "Home", "What Dark Gravity is, what works today", None),
    ("start-here/index.html", "Start Here", "Unified ecosystem entry portal for engineers &amp; auditors", "5-minute onboarding across repos, RQs, metrics & MCP"),
    ("ai-agents/index.html", "AI Agents", "Machine-readable Auditor Pack, KG, Manifest &amp; Rust MCP", "Quick-entry portal for external AI coding agents"),
    ("architecture.html", "Architecture", "How the system is built and where it runs", None),
    ("lifecycle.html", "Lifecycle", "How one mission goes from issue to pull request", "Mission flow: from issue to human-reviewed PR"),
    ("fork-policy.html", "Fork policy", "Why the lab forks open-source projects", "Dependency governance: 42 maintained open-source forks"),
    ("metrics.html", "Metrics", "Permanent 13-KPI dashboard across 4 factory domains", "Development, Quality, Security &amp; Agents KPIs"),
    ("notebooks.html", "Lab notebook", "Experiments, failures and lessons", None),
]
COMPAT_PAGES = ["start-here.html"]

LOGO = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
    'aria-hidden="true"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>'
)


def rel_prefix(cur: str) -> str:
    depth = len(pathlib.PurePosixPath(cur).parts) - 1
    return "../" * depth


def header(cur: str) -> str:
    prefix = rel_prefix(cur)
    lines = []
    for f, l, _, t in PAGES:
        cur_attr = ' aria-current="page"' if f == cur else ""
        title_attr = f' title="{t}"' if t else ""
        lines.append(f'          <li><a href="{prefix}{f}" class="nav-link"{cur_attr}{title_attr}>{l}</a></li>')
    lines.append('          <li><a href="https://github.com/lgcorzo" class="nav-link" title="GitHub profile and ecosystem overview (@lgcorzo)">GitHub Overview</a></li>')
    items = "\n".join(lines)
    return f'''
  <header class="site-header">
    <div class="container">
      <nav class="site-nav" aria-label="Main">
        <a href="{prefix}index.html" class="site-brand">{LOGO}<span>Dark Gravity Lab</span></a>
        <ul class="nav-menu">
{items}
        </ul>
      </nav>
    </div>
  </header>
  '''


def footer(cur: str) -> str:
    prefix = rel_prefix(cur)
    links = "\n".join(f'            <li><a href="{prefix}{f}">{l}</a></li>' for f, l, _, _ in PAGES)
    return f'''
  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-col">
          <p class="footer-title">About this site</p>
          <p>A public engineering notebook. Every claim carries a status tag;
          see <a href="{prefix}index.html#status-tags">what the tags mean</a> and the
          <a href="{prefix}index.html#glossary">glossary</a>.</p>
        </div>
        <div class="footer-col">
          <p class="footer-title">Pages</p>
          <ul class="footer-links">
{links}
          </ul>
        </div>
        <div class="footer-col">
          <p class="footer-title">Sources</p>
          <ul class="footer-links">
            <li><a href="https://github.com/lgcorzo/rust_CACD_autonomous_factory">Main repository</a></li>
            <li><a href="https://github.com/lgcorzo/rust_CACD_autonomous_factory/tree/main/evidence">Evidence folder</a></li>
            <li><a href="https://github.com/lgcorzo">All public repositories</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>Site content &amp; original code: MIT License. Forked repositories: respective upstream open-source licenses.</span>
        <span>Version: <a href="https://github.com/lgcorzo/rust_CACD_autonomous_factory/releases/tag/v0.3.4">v0.3.4</a></span>
      </div>
    </div>
  </footer>
  '''


def pager(cur: str) -> str:
    prefix = rel_prefix(cur)
    page_files = [f for f, _, _, _ in PAGES]
    if cur not in page_files:
        f, l, d, _ = PAGES[1]
        return (
            '\n      <nav class="pager" aria-label="Reading order">\n        '
            f'<a class="next" href="{prefix}{f}" rel="next"><small>Canonical Portal &rarr;</small><strong>{l}</strong><br><span class="note">{d}</span></a>'
            "\n      </nav>\n      "
        )
    i = page_files.index(cur)
    out = []
    if i > 0:
        f, l, d, _ = PAGES[i - 1]
        out.append(f'<a class="prev" href="{prefix}{f}" rel="prev"><small>&larr; Previous</small><strong>{l}</strong><br><span class="note">{d}</span></a>')
    if i < len(PAGES) - 1:
        f, l, d, _ = PAGES[i + 1]
        out.append(f'<a class="next" href="{prefix}{f}" rel="next"><small>Next &rarr;</small><strong>{l}</strong><br><span class="note">{d}</span></a>')
    return '\n      <nav class="pager" aria-label="Reading order">\n        ' + "\n        ".join(out) + '\n      </nav>\n      '


def sub(text: str, tag: str, body: str) -> str:
    pat = re.compile(rf"(<!--SHELL:{tag}-->).*?(<!--/SHELL:{tag}-->)", re.S)
    if not pat.search(text):
        raise SystemExit(f"marker SHELL:{tag} missing")
    return pat.sub(lambda m: m.group(1) + body + m.group(2), text)


def main() -> int:
    targets = [f for f, _, _, _ in PAGES] + [f for f in COMPAT_PAGES if (ROOT / f).is_file()]
    for f in targets:
        p = ROOT / f
        t = p.read_text(encoding="utf-8")
        t = sub(t, "HEADER", header(f))
        t = sub(t, "FOOTER", footer(f))
        t = sub(t, "PAGER", pager(f))
        p.write_text(t, encoding="utf-8")
        print("synced", f)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
