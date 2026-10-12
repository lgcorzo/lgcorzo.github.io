/**
 * Portfolio interactions — lgcorzo.github.io
 * ------------------------------------------------------------
 * Sections:
 *  1. Dark Gravity content (pipeline, stack layers, highlights)
 *  2. Repository curation (categories, badges, featured list)
 *  3. Rendering + filtering of the project grid
 *  4. UI helpers (mobile menu, scroll reveal, active nav link)
 *
 * Data source: GITHUB_REPOS (js/repos-data.js)
 */
(() => {
  'use strict';

  /* ==========================================================
   * 1. DARK GRAVITY CONTENT
   * ========================================================== */

  /** The six durable phases of a mission (Hatchet DAG). */
  const PIPELINE = [
    {
      id: 'ingest', label: 'Ingestion', tag: 'Phase 0', accent: 'accent',
      who: 'factory-cli poller · Kafka',
      title: 'A GitHub issue becomes a signed mission',
      body: 'An outbound-only poller detects an issue labelled autonomous-mission. It reads the resource limits, signs the payload with an Ed25519 verifiable credential and publishes it to Kafka. No inbound webhook is ever exposed.',
      bullets: ['Outbound polling every 30–60 s', 'Non-human identity (NHI) per mission', 'CPU / RAM / timeout clamped up front'],
    },
    {
      id: 'plan', label: 'Plan', tag: 'Phase 1', accent: 'accent-2',
      who: 'Rustant · R2R GraphRAG · deepwiki-rs',
      title: 'The planner turns intent into a contract',
      body: 'The Product-Owner agent reads the codebase through AST graphs and GraphRAG memory, then writes a machine-verifiable Spec-Kit specification that defines exactly what “done” means.',
      bullets: ['AST-aware code context', 'Spec-driven task contracts', 'Semantic memory of past missions'],
    },
    {
      id: 'code', label: 'Code', tag: 'Phase 2', accent: 'accent-3',
      who: 'ZeroClaw · gVisor (runsc)',
      title: 'A developer agent edits code in a sandbox',
      body: 'ZeroClaw consumes the contract and applies surgical code changes inside a disposable gVisor micro-sandbox. Credentials are short-lived and are zeroized from memory as soon as they are dropped.',
      bullets: ['User-space kernel isolation', '5-minute just-in-time Git tokens', 'Memory wiped in 54.2 ns'],
    },
    {
      id: 'validate', label: 'Validate', tag: 'Phase 3', accent: 'accent',
      who: 'ZeroClaw · test runners',
      title: 'Tests and security scans run under hard limits',
      body: 'Unit tests, linters and SAST run in isolated sandboxes clamped to 30 MiB of RAM and 250m CPU. A failing check sends the mission back to the Code phase with the evidence attached.',
      bullets: ['RAM ≤ 30 MiB · CPU ≤ 250m', 'Deterministic, reproducible runs', 'Automatic retry with feedback'],
    },
    {
      id: 'review', label: 'Review', tag: 'Phase 4', accent: 'accent-2',
      who: 'Rustant · Semantica-AGI · LiteLLM',
      title: 'An independent AI judge audits the result',
      body: 'A different model family scores the change (threshold 8.0 / 10) and Semantica-AGI records causal provenance — which prompt, which model, which evidence produced each line.',
      bullets: ['Heterogeneous LLM-as-a-judge', 'Full causal provenance trail', 'FinOps budgets per virtual tag'],
    },
    {
      id: 'deliver', label: 'Delivery', tag: 'Phase 5', accent: 'accent-3',
      who: 'Pull request · Human reviewer · FluxCD',
      title: 'A pull request waits for a human',
      body: 'The factory opens a PR with all test evidence. Merging is a manual human action, enforced by branch protection. After approval, FluxCD reconciles the new state into the cluster by pulling from Git.',
      bullets: ['Human approval is mandatory', 'GitOps pull-based deployment', 'Steer with @darkgravity commands'],
    },
  ];

  /** Four layers grouping the ten Kubernetes namespaces. */
  const STACK = [
    {
      layer: 'Execution', accent: 'accent', ns: 'agents · development',
      blurb: 'Where agents think and untrusted code runs.',
      tech: ['Rust 2024', 'Axum', 'MCP (SSE)', 'gVisor runsc', 'Native sidecars'],
    },
    {
      layer: 'Orchestration & Events', accent: 'accent-2', ns: 'orchestrators · confluent',
      blurb: 'Crash-resilient workflows and an event backbone.',
      tech: ['Hatchet DAGs', 'Apache Kafka (KRaft)', 'Schema Registry', 'KEDA'],
    },
    {
      layer: 'Intelligence & Data', accent: 'accent-3', ns: 'llm-apps · knowledge · storage',
      blurb: 'Models, memory and the sovereign data tier.',
      tech: ['LiteLLM', 'R2R GraphRAG', 'Semantica-AGI', 'deepwiki-rs', 'pgvector', 'CloudNativePG', 'MinIO S3', 'DirectPV'],
    },
    {
      layer: 'Security & GitOps', accent: 'accent', ns: 'security · openziti · flux-system',
      blurb: 'Identity, dark networking and declarative delivery.',
      tech: ['HashiCorp Vault', 'SealedSecrets', 'Keycloak', 'OpenZiti (mTLS 1.3)', 'FluxCD v2'],
    },
  ];

  /** Key differentiators. */
  const HIGHLIGHTS = [
    { icon: 'M12 3 4 6v6c0 5 3.4 8 8 9 4.6-1 8-4 8-9V6l-8-3z', title: 'Zero open ports', text: 'Outbound-only polling and an OpenZiti dark overlay mean there is no inbound attack surface to scan.' },
    { icon: 'M12 8v4l3 2M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18z', title: 'Ephemeral credentials', text: 'Five-minute Vault tokens, Ed25519-signed missions and memory zeroization in 54.2 ns.' },
    { icon: 'M4 4h16v12H4zM8 20h8M12 16v4', title: 'Sandboxed by default', text: 'Every code change runs in a gVisor micro-sandbox clamped to 30 MiB RAM and 250m CPU.' },
    { icon: 'M16 11a4 4 0 1 0-8 0M4 21a8 8 0 0 1 16 0', title: 'Human always in control', text: 'No automatic merges. Branch protection plus PR directives keep a person in the loop.' },
    { icon: 'M3 12h4l3-8 4 16 3-8h4', title: 'Durable & observable', text: 'Hatchet checkpoints every step; MLflow, Kafka and provenance logs make every decision auditable.' },
    { icon: 'M12 2v4M12 18v4M4.9 4.9l2.8 2.8M16.3 16.3l2.8 2.8M2 12h4M18 12h4', title: 'Runs on a small footprint', text: 'Open-source, sovereign stack designed to operate on limited hardware without cloud lock-in.' },
  ];

  /* ==========================================================
   * 2. REPOSITORY CURATION
   * ========================================================== */

  /** Display categories. */
  const CATEGORIES = [
    { id: 'featured', label: 'Featured' },
    { id: 'all', label: 'All' },
    { id: 'mlops', label: 'MLOps & Platform' },
    { id: 'ai', label: 'AI, Agents & RAG' },
    { id: 'systems', label: 'Systems Engineering' },
  ];

  const MLOPS = new Set([
    'mlops-python-package', 'llmops-python-package', 'gitops_internal_lgcorzo', 'Jules_remediator',
    'Asynchronous-Optimization', 'devops_job_shop_scheduling', 'cod_fish_classification_app',
    'cod_fish_classification_keras_model', 'knowledge-catalog',
  ]);
  const AI = new Set([
    'R2R-Application', 'R2R-Engine', 'semantica', 'deepwiki-rs', 'deepwiki-open', 'CodeWiki', 'openwiki',
    'FinRobot', 'TradingAgents', 'ai-agents-for-beginners', 'GEN_AI_Course', 'mocogpt', 'openevolve',
    'adk-rust', 'rig', 'Documentation_agent', 'fastapi-autogen-team', 'spec-kit', 'superpowers',
    'speckit-superpowers-bridge', 'rust_CACD_autonomous_factory',
  ]);

  /** Hand-picked featured projects (order matters). */
  const FEATURED = [
    'rust_CACD_autonomous_factory', 'mlops-python-package', 'llmops-python-package', 'R2R-Engine',
    'semantica', 'deepwiki-rs', 'gitops_internal_lgcorzo', 'Jules_remediator', 'fastapi-autogen-team',
  ];

  /** Optional live demos / extra links. */
  const DEMOS = {
    'rust_CACD_autonomous_factory': { label: 'Architecture', url: 'architecture.html' },
    'docs': { label: 'Sovereignty', url: 'sovereignty.html' },
    'lgcorzo.github.io': { label: 'Live site', url: 'https://lgcorzo.github.io' },
  };

  /** Repos intentionally hidden from the grid. */
  const HIDDEN = new Set(['lgcorzo']);

  /** Keyword → tech badge rules applied to name + description. */
  const BADGE_RULES = [
    [/kubernetes|k8s|fluxcd|helm/i, 'Kubernetes'],
    [/docker|container|ghcr/i, 'Docker'],
    [/\brag\b|graphrag|retrieval/i, 'RAG'],
    [/mlflow/i, 'MLflow'],
    [/\bdvc\b/i, 'DVC'],
    [/autogen|multi-agent|agent/i, 'Agents'],
    [/llm|openai|litellm/i, 'LLM'],
    [/\bs3\b|minio|object storage/i, 'S3'],
    [/hatchet/i, 'Hatchet'],
    [/gvisor|sandbox/i, 'gVisor'],
    [/mtls|crypto|kms|sha256|blake|md5/i, 'Crypto'],
    [/simd|avx/i, 'SIMD'],
    [/fastapi/i, 'FastAPI'],
    [/\bast\b|tree-sitter/i, 'AST'],
    [/zero-trust|openziti/i, 'Zero-trust'],
  ];

  /** Resolve a repo to one of the display categories. */
  function categoryOf(repo) {
    if (MLOPS.has(repo.name)) return 'mlops';
    if (AI.has(repo.name)) return 'ai';
    return 'systems';
  }

  /** Build the tech badge list for a card (language first, max 4). */
  function badgesOf(repo) {
    const text = `${repo.name} ${repo.description || ''}`;
    const out = [];
    if (repo.language) out.push(repo.language);
    BADGE_RULES.forEach(([re, label]) => {
      if (re.test(text) && !out.includes(label)) out.push(label);
    });
    return out.slice(0, 4);
  }

  /** Strip the “Dark Gravity X:” prefix and shorten to one clear line. */
  function oneLiner(repo) {
    let d = (repo.description || 'No description yet.').replace(/^Dark Gravity [^:]+:\s*/i, '').trim();
    const dot = d.indexOf('. ');
    if (dot > 40) d = d.slice(0, dot + 1);
    return d.length > 150 ? `${d.slice(0, 147)}…` : d;
  }

  /** Dot colour per language. */
  const LANG_COLORS = {
    Rust: '#f97316', Python: '#3b82f6', Go: '#22d3ee', TypeScript: '#60a5fa', JavaScript: '#facc15',
    Shell: '#34d399', 'Jupyter Notebook': '#fb923c', Dockerfile: '#38bdf8', HTML: '#f43f5e',
  };

  /* ==========================================================
   * 3. RENDERING
   * ========================================================== */

  const $ = (sel) => document.querySelector(sel);
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const ACCENT_TEXT = { accent: 'text-accent', 'accent-2': 'text-accent-2', 'accent-3': 'text-accent-3' };
  const ACCENT_BG = { accent: 'bg-accent/10', 'accent-2': 'bg-accent-2/10', 'accent-3': 'bg-accent-3/10' };
  const ACCENT_RING = { accent: 'border-accent/60', 'accent-2': 'border-accent-2/60', 'accent-3': 'border-accent-3/60' };

  /* ---- Pipeline stepper ---- */
  function initPipeline() {
    const list = $('#pipeline-steps');
    const panel = $('#pipeline-panel');
    if (!list || !panel) return;

    list.innerHTML = PIPELINE.map((s, i) => `
      <li class="shrink-0 lg:shrink">
        <button type="button" role="tab" data-step="${i}" id="tab-${s.id}" aria-controls="pipeline-panel"
          class="step-btn flex w-full items-center gap-3 rounded-xl border border-line bg-white/[0.03] px-4 py-3 text-left transition hover:bg-white/[0.07] focus-visible:outline-2 focus-visible:outline-accent">
          <span class="grid h-8 w-8 shrink-0 place-items-center rounded-lg font-mono text-xs font-semibold ${ACCENT_BG[s.accent]} ${ACCENT_TEXT[s.accent]}">${i}</span>
          <span class="min-w-0"><span class="block text-sm font-semibold text-white">${esc(s.label)}</span>
          <span class="hidden truncate text-xs text-slate-500 lg:block">${esc(s.who)}</span></span>
        </button>
      </li>`).join('');

    const buttons = [...list.querySelectorAll('.step-btn')];

    function select(i) {
      const s = PIPELINE[i];
      buttons.forEach((b, idx) => {
        const active = idx === i;
        b.setAttribute('aria-selected', active);
        b.classList.toggle('!bg-white/10', active);
        Object.values(ACCENT_RING).forEach((c) => b.classList.remove(c));
        if (active) b.classList.add(ACCENT_RING[s.accent]);
      });
      panel.setAttribute('aria-labelledby', `tab-${s.id}`);
      panel.innerHTML = `
        <div class="flex flex-wrap items-center justify-between gap-3">
          <span class="font-mono text-xs uppercase tracking-widest ${ACCENT_TEXT[s.accent]}">${esc(s.tag)} · ${esc(s.label)}</span>
          <span class="chip">${esc(s.who)}</span>
        </div>
        <h4 class="mt-4 text-2xl font-bold leading-snug text-white">${esc(s.title)}</h4>
        <p class="mt-3 leading-relaxed text-slate-400">${esc(s.body)}</p>
        <ul class="mt-6 grid gap-2.5">
          ${s.bullets.map((b) => `<li class="flex items-start gap-2.5 text-sm text-slate-300">
            <svg class="mt-0.5 h-4 w-4 shrink-0 ${ACCENT_TEXT[s.accent]}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="m5 12 5 5 9-10"/></svg>${esc(b)}</li>`).join('')}
        </ul>
        <div class="mt-8 flex items-center gap-2" aria-hidden="true">
          ${PIPELINE.map((_, idx) => `<span class="h-1 flex-1 rounded-full ${idx <= i ? 'bg-gradient-to-r from-accent to-accent-2' : 'bg-white/10'}"></span>`).join('')}
        </div>`;
    }

    buttons.forEach((b, i) => {
      b.addEventListener('click', () => select(i));
      b.addEventListener('keydown', (e) => {
        const n = buttons.length;
        if (e.key === 'ArrowDown' || e.key === 'ArrowRight') { e.preventDefault(); buttons[(i + 1) % n].focus(); buttons[(i + 1) % n].click(); }
        if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') { e.preventDefault(); buttons[(i - 1 + n) % n].focus(); buttons[(i - 1 + n) % n].click(); }
      });
    });
    select(0);
  }

  /* ---- Stack layers + highlights ---- */
  function initStack() {
    const grid = $('#stack-grid');
    if (grid) {
      grid.innerHTML = STACK.map((l) => `
        <article class="glass card-hover reveal p-6">
          <div class="flex flex-wrap items-center justify-between gap-3">
            <h4 class="text-lg font-semibold text-white">${esc(l.layer)}</h4>
            <span class="font-mono text-[11px] ${ACCENT_TEXT[l.accent]}">ns/${esc(l.ns)}</span>
          </div>
          <p class="mt-1.5 text-sm text-slate-400">${esc(l.blurb)}</p>
          <div class="mt-4 flex flex-wrap gap-1.5">${l.tech.map((t) => `<span class="chip">${esc(t)}</span>`).join('')}</div>
        </article>`).join('');
    }
    const hl = $('#highlights-grid');
    if (hl) {
      hl.innerHTML = HIGHLIGHTS.map((h) => `
        <article class="glass card-hover reveal p-6">
          <div class="mb-4 grid h-10 w-10 place-items-center rounded-xl bg-accent/10 text-accent">
            <svg class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="${h.icon}"/></svg>
          </div>
          <h4 class="font-semibold text-white">${esc(h.title)}</h4>
          <p class="mt-2 text-sm leading-relaxed text-slate-400">${esc(h.text)}</p>
        </article>`).join('');
    }
  }

  /* ---- Project grid ---- */
  function initProjects() {
    const grid = $('#repo-grid');
    const bar = $('#filter-bar');
    const search = $('#repo-search');
    const count = $('#repo-count');
    const more = $('#show-more');
    if (!grid || typeof GITHUB_REPOS === 'undefined') return;

    const PAGE = 12;
    let category = 'featured';
    let query = '';
    let limit = PAGE;

    const repos = GITHUB_REPOS
      .filter((r) => !HIDDEN.has(r.name))
      .map((r) => ({ ...r, view: categoryOf(r), badges: badgesOf(r), summary: oneLiner(r) }));

    const stat = $('#stat-repos');
    if (stat) stat.textContent = `${repos.length}`;

    const counts = {
      featured: FEATURED.length,
      all: repos.length,
      mlops: repos.filter((r) => r.view === 'mlops').length,
      ai: repos.filter((r) => r.view === 'ai').length,
      systems: repos.filter((r) => r.view === 'systems').length,
    };

    bar.innerHTML = CATEGORIES.map((c) => `
      <button type="button" role="tab" data-cat="${c.id}"
        class="cat-btn rounded-full border border-line px-4 py-2 text-sm font-medium text-slate-400 transition hover:text-white focus-visible:outline-2 focus-visible:outline-accent">
        ${esc(c.label)} <span class="ml-1 font-mono text-[11px] opacity-60">${counts[c.id]}</span>
      </button>`).join('');

    const catButtons = [...bar.querySelectorAll('.cat-btn')];

    function filtered() {
      // A search always looks across everything; otherwise respect the tab.
      if (query) {
        // Match at word starts so "rag" finds RAG, not "sto-rag-e".
        const safe = query.replace(/[^a-z0-9 ]/gi, (c) => `\\${c}`);
        const re = new RegExp(`(^|[^a-z0-9])${safe}`, 'i');
        return repos.filter((r) => re.test(`${r.name.replace(/[-_]/g, ' ')} ${r.description || ''} ${r.badges.join(' ')}`));
      }
      if (category === 'featured') return FEATURED.map((n) => repos.find((r) => r.name === n)).filter(Boolean);
      if (category === 'all') return repos;
      return repos.filter((r) => r.view === category);
    }

    function card(r) {
      const color = LANG_COLORS[r.language] || '#94a3b8';
      const demo = DEMOS[r.name];
      const catLabel = { mlops: 'MLOps', ai: 'AI & RAG', systems: 'Systems' }[r.view];
      return `
      <article class="glass card-hover flex flex-col p-6">
        <div class="flex items-start justify-between gap-3">
          <h3 class="min-w-0 break-words font-mono text-[15px] font-semibold text-white">${esc(r.name)}</h3>
          <span class="shrink-0 rounded-full border border-line px-2 py-0.5 text-[10px] uppercase tracking-wider text-slate-400">${catLabel}</span>
        </div>
        <p class="mt-3 flex-1 text-sm leading-relaxed text-slate-400">${esc(r.summary)}</p>
        <div class="mt-4 flex flex-wrap gap-1.5">${r.badges.map((b) => `<span class="chip">${esc(b)}</span>`).join('')}</div>
        <div class="mt-5 flex items-center justify-between gap-3 border-t border-line pt-4 text-xs">
          <span class="flex items-center gap-2 text-slate-500">
            <span class="h-2.5 w-2.5 rounded-full" style="background:${color}"></span>${esc(r.language || 'n/a')}
            ${r.stars ? `<span class="ml-2">★ ${r.stars}</span>` : ''}
          </span>
          <span class="flex items-center gap-3 font-semibold">
            ${demo ? `<a class="text-accent-3 hover:underline" href="${esc(demo.url)}">${esc(demo.label)} ↗</a>` : ''}
            <a class="text-accent hover:underline" href="${esc(r.url)}" target="_blank" rel="noopener noreferrer" aria-label="${esc(r.name)} on GitHub">GitHub →</a>
          </span>
        </div>
      </article>`;
    }

    function render() {
      const list = filtered();
      const visible = list.slice(0, limit);
      grid.innerHTML = visible.length
        ? visible.map(card).join('')
        : '<p class="col-span-full rounded-2xl border border-dashed border-line p-10 text-center text-slate-500">No projects match your search.</p>';
      count.textContent = `Showing ${visible.length} of ${list.length} project${list.length === 1 ? '' : 's'}`;
      more.classList.toggle('hidden', list.length <= limit);
      catButtons.forEach((b) => {
        const active = b.dataset.cat === category && !query;
        b.setAttribute('aria-selected', active);
        b.classList.toggle('!border-accent/60', active);
        b.classList.toggle('!bg-accent/10', active);
        b.classList.toggle('!text-white', active);
      });
    }

    bar.addEventListener('click', (e) => {
      const btn = e.target.closest('.cat-btn');
      if (!btn) return;
      category = btn.dataset.cat; query = ''; search.value = ''; limit = PAGE; render();
    });
    search.addEventListener('input', (e) => { query = e.target.value.trim(); limit = PAGE; render(); });
    more.addEventListener('click', () => { limit += PAGE; render(); });
    render();
  }

  /* ==========================================================
   * 4. UI HELPERS
   * ========================================================== */

  function initMenu() {
    const btn = $('#menu-btn');
    const menu = $('#mobile-menu');
    if (!btn || !menu) return;
    btn.addEventListener('click', () => {
      const open = menu.classList.toggle('hidden') === false;
      btn.setAttribute('aria-expanded', open);
    });
    menu.addEventListener('click', (e) => {
      if (e.target.closest('a')) { menu.classList.add('hidden'); btn.setAttribute('aria-expanded', 'false'); }
    });
  }

  /** Fade-in elements when they scroll into view. */
  function initReveal() {
    const items = document.querySelectorAll('.reveal:not(.is-visible)');
    if (!('IntersectionObserver' in window)) { items.forEach((el) => el.classList.add('is-visible')); return; }
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add('is-visible'); io.unobserve(en.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    items.forEach((el) => io.observe(el));
  }

  /** Highlight the nav link of the section currently in view. */
  function initScrollSpy() {
    const links = [...document.querySelectorAll('.nav-link')];
    const sections = links.map((l) => document.querySelector(l.getAttribute('href'))).filter(Boolean);
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (!en.isIntersecting) return;
        links.forEach((l) => {
          const on = l.getAttribute('href') === `#${en.target.id}`;
          l.classList.toggle('text-white', on);
          l.classList.toggle('bg-white/5', on);
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    sections.forEach((s) => io.observe(s));
  }

  document.addEventListener('DOMContentLoaded', () => {
    initPipeline();
    initStack();
    initProjects();
    initMenu();
    initReveal();
    initScrollSpy();
  });
})();
