document.addEventListener('DOMContentLoaded', () => {
  // Mobile Nav Toggle if present
  const navLinks = document.querySelectorAll('.nav-link');
  
  // Highlight active link on scroll
  const sections = document.querySelectorAll('section[id]');
  window.addEventListener('scroll', () => {
    const scrollY = window.pageYOffset;
    sections.forEach(current => {
      const sectionHeight = current.offsetHeight;
      const sectionTop = current.offsetTop - 120;
      const sectionId = current.getAttribute('id');
      if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
        navLinks.forEach(link => {
          link.classList.remove('active');
          if (link.getAttribute('href') === `#${sectionId}`) {
            link.classList.add('active');
          }
        });
      }
    });
  });

  // Render Repositories
  const repoGrid = document.getElementById('repo-grid');
  const filterBtns = document.querySelectorAll('.filter-btn');
  const repoCountBadge = document.getElementById('repo-count-badge');

  function getLangClass(lang) {
    if (!lang) return 'dot-rust';
    const l = lang.toLowerCase();
    if (l.includes('rust')) return 'dot-rust';
    if (l.includes('python')) return 'dot-python';
    if (l.includes('go')) return 'dot-go';
    if (l.includes('typescript') || l.includes('javascript')) return 'dot-typescript';
    return 'dot-rust';
  }

  function getCatClass(cat) {
    switch (cat) {
      case 'core': return 'cat-core';
      case 'storage': return 'cat-storage';
      case 'crypto': return 'cat-crypto';
      default: return 'cat-app';
    }
  }

  function renderRepos(category = 'all', searchQuery = '') {
    if (!repoGrid || !window.GITHUB_REPOS) return;

    let filtered = window.GITHUB_REPOS;
    if (category !== 'all') {
      filtered = filtered.filter(r => r.category === category);
    }

    if (searchQuery.trim() !== '') {
      const q = searchQuery.toLowerCase();
      filtered = filtered.filter(r => 
        r.name.toLowerCase().includes(q) || 
        r.description.toLowerCase().includes(q)
      );
    }

    if (repoCountBadge) {
      repoCountBadge.textContent = `${filtered.length} Repositories`;
    }

    if (filtered.length === 0) {
      repoGrid.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 3rem; color: var(--text-secondary);">
          <p style="font-size: 1.1rem; margin-bottom: 0.5rem;">No repositories found matching your query.</p>
          <span style="font-size: 0.9rem; color: var(--text-muted);">Try adjusting your category filter or search keywords.</span>
        </div>
      `;
      return;
    }

    repoGrid.innerHTML = filtered.map(repo => `
      <div class="repo-card" data-category="${repo.category}">
        <div>
          <div class="repo-header">
            <a href="${repo.url}" target="_blank" rel="noopener noreferrer" class="repo-title">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color: var(--accent-cyan);">
                <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path>
              </svg>
              ${repo.name}
            </a>
            <span class="repo-category ${getCatClass(repo.category)}">${repo.category}</span>
          </div>
          <p class="repo-desc">${repo.description || 'Core repository contributing to Dark Gravity architecture and autonomous factory workflows.'}</p>
        </div>
        <div class="repo-footer">
          <div class="repo-lang">
            <span class="lang-dot ${getLangClass(repo.language)}"></span>
            <span>${repo.language}</span>
          </div>
          <a href="${repo.url}" target="_blank" rel="noopener noreferrer" class="repo-link">
            Inspect Source
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="7" y1="17" x2="17" y2="7"></line>
              <polyline points="7 7 17 7 17 17"></polyline>
            </svg>
          </a>
        </div>
      </div>
    `).join('');
  }

  // Filter Event Listeners
  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const cat = btn.getAttribute('data-filter');
      const searchInput = document.getElementById('repo-search');
      renderRepos(cat, searchInput ? searchInput.value : '');
    });
  });

  // Search Input Listener
  const searchInput = document.getElementById('repo-search');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      const activeBtn = document.querySelector('.filter-btn.active');
      const cat = activeBtn ? activeBtn.getAttribute('data-filter') : 'all';
      renderRepos(cat, e.target.value);
    });
  }

  // Initial Render
  renderRepos();
});
