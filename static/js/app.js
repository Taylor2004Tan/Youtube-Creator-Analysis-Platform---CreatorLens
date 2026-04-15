/**
 * app.js — Client-side router & bootstrap
 */

// Global application state
const AppState = {
  selectedChannel: null,
};

// Navigation links for active-state management
const NAV_MAP = {
  '/':           'nav-home',
  '/categories': 'nav-categories',
  '/search':     'nav-search',
  '/analyze':    null,
};

function setActiveNav(path) {
  document.querySelectorAll('.nav-link').forEach(el => el.classList.remove('active'));
  const base = '/' + (path.split('/')[1] || '');
  const id = NAV_MAP[base];
  if (id) document.getElementById(id)?.classList.add('active');
}

function navigate(path) {
  window.location.hash = '#' + path;
}

function route(hash) {
  const path = hash.replace(/^#/, '') || '/';
  setActiveNav(path);
  destroyCharts();

  const segments = path.split('/').filter(Boolean);

  if (segments.length === 0 || segments[0] === '') {
    renderHome();
  } else if (segments[0] === 'categories' && segments.length === 1) {
    renderCategories();
  } else if (segments[0] === 'categories' && segments.length >= 2) {
    renderCategoryDetail(decodeURIComponent(segments[1]));
  } else if (segments[0] === 'search') {
    renderSearch();
  } else if (segments[0] === 'analyze') {
    renderAnalyze();
  } else {
    renderHome();
  }
}

// Handle hash changes
window.addEventListener('hashchange', () => route(window.location.hash));

// Initial load
window.addEventListener('DOMContentLoaded', () => {
  route(window.location.hash || '#/');
});
