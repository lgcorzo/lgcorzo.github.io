#!/usr/bin/env python3
"""Keep the header, footer and prev/next pager identical on every page.

Each page holds three marker pairs, e.g.
  <!--SHELL:HEADER--> ... <!--/SHELL:HEADER-->
This script rewrites what sits between the markers. Run it after editing
the PAGES list below:  python3 tools/sync_shell.py
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = [  # (file, nav label, one-line description used by the pager, title tooltip)
    ("index.html", "Home", "What Dark Gravity is, what works today", None),
    ("architecture.html", "Architecture", "How the system is built and where it runs", None),
    ("lifecycle.html", "Lifecycle", "How one mission goes from issue to pull request", "Mission flow: from issue to human-reviewed PR"),
    ("fork-policy.html", "Fork policy", "Why the lab forks open-source projects", "Dependency governance: 42 maintained open-source forks"),
    ("notebooks.html", "Lab notebook", "Experiments, failures and lessons", None),
]
LOGO = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
        'aria-hidden="true"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>')

def header(cur):
    lines = []
    for f, l, _, t in PAGES:
        cur_attr = ' aria-current="page"' if f == cur else ''
        title_attr = f' title="{t}"' if t else ''
        lines.append(f'          <li><a href="{f}" class="nav-link"{cur_attr}{title_attr}>{l}</a></li>')
    items = "\n".join(lines)
    return f'''
  <header class="site-header">
    <div class="container">
      <nav class="site-nav" aria-label="Main">
        <a href="index.html" class="site-brand">{LOGO}<span>Dark Gravity Lab</span></a>
        <ul class="nav-menu">
{items}
        </ul>
      </nav>
    </div>
  </header>
  '''

def footer():
    links = "\n".join(f'            <li><a href="{f}">{l}</a></li>' for f, l, _, _ in PAGES)
    return f'''
  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-col">
          <p class="footer-title">About this site</p>
          <p>A public engineering notebook. Every claim carries a status tag;
          see <a href="index.html#status-tags">what the tags mean</a> and the
          <a href="index.html#glossary">glossary</a>.</p>
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
        <span>Version: <a href="https://github.com/lgcorzo/rust_CACD_autonomous_factory/releases/tag/v0.2.8">v0.2.8</a></span>
      </div>
    </div>
  </footer>
  '''

def pager(cur):
    i = [f for f, _, _, _ in PAGES].index(cur)
    out = []
    if i > 0:
        f, l, d, _ = PAGES[i - 1]
        out.append(f'<a class="prev" href="{f}" rel="prev"><small>&larr; Previous</small><strong>{l}</strong><br><span class="note">{d}</span></a>')
    if i < len(PAGES) - 1:
        f, l, d, _ = PAGES[i + 1]
        out.append(f'<a class="next" href="{f}" rel="next"><small>Next &rarr;</small><strong>{l}</strong><br><span class="note">{d}</span></a>')
    return '\n      <nav class="pager" aria-label="Reading order">\n        ' + "\n        ".join(out) + '\n      </nav>\n      '

def sub(text, tag, body):
    pat = re.compile(rf"(<!--SHELL:{tag}-->).*?(<!--/SHELL:{tag}-->)", re.S)
    if not pat.search(text):
        raise SystemExit(f"marker SHELL:{tag} missing")
    return pat.sub(lambda m: m.group(1) + body + m.group(2), text)

for f, _, _, _ in PAGES:
    p = ROOT / f
    t = p.read_text(encoding="utf-8")
    t = sub(t, "HEADER", header(f))
    t = sub(t, "FOOTER", footer())
    t = sub(t, "PAGER", pager(f))
    p.write_text(t, encoding="utf-8")
    print("synced", f)
