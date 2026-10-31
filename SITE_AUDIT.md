# Dark Gravity Lab — Technical Site Audit & Polish Report

**Date**: 2026-10-31  
**Branch**: `site-polish`  
**Target Repository**: `https://github.com/lgcorzo/lgcorzo.github.io`  
**Site URL**: `https://lgcorzo.github.io`  
**Auditor**: Senior Web Engineer & Technical Editor  

---

## 1. Executive Summary

This audit report documents the comprehensive editorial, technical, architectural, and accessibility refactoring performed on the Dark Gravity engineering laboratory site (`lgcorzo.github.io`). All modifications adhere strictly to the non-negotiable rules:
- **No invented metrics or unverified facts**: Every statement is anchored to verified code, repository artifacts, or explicitly tagged as *Designed* / *Planned*.
- **No private data disclosures**: Removed internal account counts (such as private repository counts) to prevent operational leakage.
- **URL continuity guaranteed**: The rename from `sovereignty.html` to `fork-policy.html` preserves existing incoming URLs via an automated `<meta http-equiv="refresh">` redirect, a `<link rel="canonical">` header, and accessible fallback navigation.
- **Consistent voice & tone**: Neutral, honest, evidence-based tone in the first person singular (`I`), avoiding marketing superlatives and false claims.
- **Lighthouse mobile performance**: All pages achieve 100/100 or >= 95 across Performance, Accessibility, Best Practices, and SEO.

---

## 2. Checklist of Requirements (A – G)

| Section | Topic | Status | Justification / Implementation Details |
| :--- | :--- | :---: | :--- |
| **A** | **Portada: Claridad inmediata** | **HECHO** | Headline updated to the concrete description: *"An autonomous software factory in Rust and Kubernetes where AI agents propose pull requests in isolated sandboxes and a human decides the merge."* Added single descriptive tagline, research question callout box, prominent primary CTA button for Lab Notebook, and secondary navigation buttons. |
| **B** | **Jerga y Actual Factory Status** | **HECHO** | Plain-language explanations for all 4 states (*Verified, Deployed, Implemented, Designed*) with explicit evidence paths. Deep technical specifics (crate topology, admission policies, Ed25519 NHI, LiteLLM vtags) folded into clean `<details>` blocks. The *54.2 ns* memory wipe metric is fully contextualized (Criterion benchmark, AMD x86_64, `cargo bench` reproduction). Key acronyms wrapped with `<abbr title="...">` throughout. |
| **C** | **Lab Notebook: Contenido real** | **HECHO** | Added a prominent Summary Index Table listing all 14 entries with real titles, dates, status tags, and one-sentence factual outcomes. Validated that all 14 entries exist and strictly follow the 5-question standard (*Intent, Architecture & Setup, What actually happened, Lessons & Limitations, Industrial Application Transfer*). Translated lingering Spanish walkthrough paragraph to English. |
| **D** | **Coherencia de datos y texto** | **HECHO** | Reconciled GitHub repository count via live CLI (`22 original + 42 forks = 64 public repositories`), omitting references to private repos. Unified narrative voice to first person singular (`I`, `my`). Unified footer to a single version (`v0.2.8`) linking to release notes. Unified Fork Policy name and canonical URL (`fork-policy.html`). Defined clear MIT License for site & original code vs. upstream licenses for forks. |
| **E** | **Enlaces y recursos** | **HECHO** | 100% of internal links (251) and 100% of external links (87) verified with HTTP 200 / valid DOM targets (zero broken links). Confirmed that the NotebookLM link redirects to Google Login (HTTP 302) and is not public; kept excluded from public resources. Added descriptive context tooltips to *Lifecycle* and *Fork policy* in navigation. |
| **F** | **SEO y metadatos** | **HECHO** | Enforced `<title>` &le; 60 chars (34–41 chars) and `<meta name="description">` &le; 160 chars (129–150 chars) across all pages. Exactly 1 `<h1>` per page. Added complete Open Graph and Twitter Card tags with a custom 1200x630 social card (`assets/og-image.png`). `<link rel="canonical">` and `lang="en"` verified on every page. |
| **G** | **Accesibilidad y calidad técnica** | **HECHO** | WCAG AA contrast ratio enforced across both dark and light modes. Interactive elements have visible focus rings (`--focus-ring`). Full keyboard navigation. `prefers-reduced-motion` respected. Mobile responsiveness validated down to 360px without horizontal scroll. Mobile Lighthouse scores: 100 / 100 / 100 / 100 on 4 pages, and 96 / 100 / 96 / 100 on Notebooks. |
| **H** | **Opcional: Resumen en español** | **PENDIENTE DECISIÓN** | Drafted proposed summary in Section 6 below, awaiting user confirmation before applying to homepage. |

---

## 3. Unverified Claims & Remediation Actions

In accordance with **Rule 1**, all statements on the site were cross-referenced against codebase artifacts (`Cargo.toml`, `evidence/verified_status.json`, `reliability-tests.md`, `benches/memory_zeroize_bench.rs`, and MicroK8s baseline):

1. **Multi-Node Chaos Drills & Soak Testing**:
   - *Previous status*: Implied continuous multi-node resilience.
   - *Audit finding*: Single-pod worker kill recovery was empirically verified in `evidence/reliability-tests.md`, but multi-node cluster loss and multi-day soak tests have not been executed or published.
   - *Remediation*: Explicitly marked as **Designed** with transparent scope limitation: *"Multi-node cluster failure drills and continuous multi-day soak tests are architecturally planned but not yet published as verified facts."*
2. **Third-Party Regulatory & Compliance Certifications**:
   - *Previous status*: Occasional mention of "EU AI Act Conformity Assessment" and "SOC 2 Type II compliance".
   - *Audit finding*: The repository contains architectural readiness measures and verifiable audit logging traits, but no formal third-party audit or conformity stamp has been awarded.
   - *Remediation*: Added explicit compliance disclaimer: *"Compliance wording: all controls are architectural readiness measures. No third-party certification (EU AI Act, SOC 2 or other) is claimed."*
3. **Repository Fleet Totals & Private Account Leakage**:
   - *Previous status*: Stated "72 repositories across the lab (64 public, 8 private)".
   - *Audit finding*: Publishing private repository numbers exposes internal operational account metadata on a public site.
   - *Remediation*: Normalized to public verified facts: *"64 public repositories (22 original source repositories + 42 maintained forks)"*.
4. **Criterion Micro-Benchmark (54.2 ns)**:
   - *Previous status*: Highlighted as an isolated headline metric.
   - *Audit finding*: While accurate according to `benches/memory_zeroize_bench.rs`, presenting "54.2 ns" without context reads like marketing hyperbole.
   - *Remediation*: Fully contextualized under the memory zeroization capability with hardware specification (AMD x86_64) and exact reproduction command (`cargo bench --bench memory_zeroize_bench`).

---

## 4. Broken Link & Navigation Audit Results

### 4.1 Internal Links & Document Anchors
- **Total internal links checked**: 251
- **Broken internal links**: **0**
- **Orphaned anchors**: **0**

### 4.2 External URLs
- **Total external links checked**: 87 unique URLs
- **HTTP status**: **100% returned HTTP 200 OK**
- **Verified domains**: `github.com`, `youtube-nocookie.com`, `w3.org`, `microk8s.io`, `hatchet.run`, `openziti.io`, `cloudnative-pg.io`, `gvisor.dev`.

### 4.3 NotebookLM Link Verification
- **URL checked**: `https://notebook.google.com/notebook/116d5f03-2fb0-4fa7-bd7c-1c9849920abc`
- **Result**: `HTTP/2 302` redirecting to Google Login (`https://notebook.google.com/login?continue=...`).
- **Conclusion**: Unauthenticated / anonymous visitors cannot access this resource. It has been excluded from the public footer and resources list.

---

## 5. Lighthouse Mobile Audit Scores (Before vs. After)

All audits executed via Lighthouse 12.8.2 on mobile emulation (`--form-factor=mobile --chrome-flags="--headless --no-sandbox"`).

| Page | Metric | Before Refactor | After Refactor | Delta |
| :--- | :--- | :---: | :---: | :---: |
| **`index.html`** | Performance | 100 | **100** | — |
| | Accessibility | 98 | **100** | +2 |
| | Best Practices | 100 | **100** | — |
| | SEO | 100 | **100** | — |
| **`architecture.html`** | Performance | 100 | **100** | — |
| | Accessibility | 100 | **100** | — |
| | Best Practices | 100 | **100** | — |
| | SEO | 100 | **100** | — |
| **`lifecycle.html`** | Performance | 100 | **100** | — |
| | Accessibility | 100 | **100** | — |
| | Best Practices | 100 | **100** | — |
| | SEO | 100 | **100** | — |
| **`fork-policy.html`** | Performance | 100 | **100** | — |
| | Accessibility | 100 | **100** | — |
| | Best Practices | 100 | **100** | — |
| | SEO | 100 | **100** | — |
| **`notebooks.html`** | Performance | 96 | **96** | — |
| | Accessibility | 100 | **100** | — |
| | Best Practices | 96 | **96** | — |
| | SEO | 100 | **100** | — |

*Note on `notebooks.html`*: Best Practices (96) and Performance (96) are slightly moderated due to the embedded YouTube iframe player (`youtube-nocookie.com`) for the architectural demonstration screencast. Both scores comfortably exceed the &ge; 90 threshold.

---

## 6. Decisions Requiring User Confirmation

1. **NotebookLM Knowledge Base**:
   - *Finding*: `https://notebook.google.com/notebook/116d5f03-2fb0-4fa7-bd7c-1c9849920abc` requires Google authentication.
   - *Action taken*: Excluded from public footer/resources.
   - *Question for user*: Would you like to keep it private/omitted, or configure NotebookLM public sharing and restore the link once public access is confirmed?
2. **Optional Spanish Summary on Homepage (Section H)**:
   - *Proposal*: Add a collapsible or dedicated bilingual summary block on `index.html`:
     ```html
     <details class="callout">
       <summary>Resumen en español (Dark Gravity Lab)</summary>
       <p>
         Dark Gravity es una fábrica de software autónoma experimental implementada en Rust y Kubernetes.
         Los agentes de IA reciben issues de GitHub, generan especificaciones técnicas (SDD), ejecutan cambios de código
         en micro-sandboxes aisladas (gVisor con límites estrictos de 30Mi RAM y 250m CPU) y proponen pull requests verificadas.
         Una persona revisa y aprueba manualmente cualquier merge a ramas principales (gobernanza Human-in-the-Loop).
       </p>
     </details>
     ```
   - *Question for user*: Would you like this summary added directly to the hero section of `index.html`?
3. **Old URL Redirection (`sovereignty.html`)**:
   - *Action taken*: Kept as an active redirection stub with `<meta http-equiv="refresh" content="0; url=fork-policy.html">`, canonical link, and manual proceed button.
   - *Recommendation*: Retain indefinitely to ensure existing GitHub or web citations never hit a 404.

---

## 7. Atomic Commits Summary

All commits were created on branch `site-polish` with strict pre-commit verification (Gitleaks + html-validate):

1. `d13f48a` — `style(css): improve contrast, add button styles, details, and abbr support`
2. `19eec04` — `feat(seo): generate standardized 1200x630 OpenGraph social card`
3. `31a871b` — `docs(index): update hero, research question, actual factory status and glossary (#A, #B)`
4. `bbcb019` — `docs(fork-policy): unify fork policy URL and add meta refresh redirect on sovereignty.html (#D)`
5. `3e2d433` — `docs(architecture): add OpenGraph metadata, update nav/footer and clarify crate limits (#E, #F)`
6. `29fb288` — `docs(lifecycle): add OpenGraph metadata, update nav/footer and clarify 4-vertex HITL (#E, #F)`
7. `f3b7e0f` — `docs(notebooks): add summary table, align all entries to 5 questions, and unify voice (#C, #D)`
8. `36e7bd0` — `chore(shell): synchronize headers, footers, tooltips, and pagers with fork-policy.html`
9. `1eb4a28` — `style(a11y): fix button contrast in light mode and underline footer text links`
