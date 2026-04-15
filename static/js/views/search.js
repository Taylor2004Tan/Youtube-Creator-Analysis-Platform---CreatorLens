/**
 * views/search.js
 */
let _searchTimer = null;

function renderSearch() {
  document.getElementById('app').innerHTML = `
  <div class="container page">
    <div class="section-header">
      <div class="section-title">🔍 Search a Creator</div>
      <div class="section-sub">Type a channel name to find and select it for analysis</div>
    </div>
    <div class="search-bar">
      <svg class="search-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/>
      </svg>
      <input
        type="text"
        id="search-input"
        placeholder="e.g. MrBeast, MKBHD, Graham Stephan…"
        autocomplete="off"
        oninput="onSearchInput(this.value)"
      />
    </div>
    <div id="search-results"></div>
  </div>`;

  setTimeout(() => document.getElementById('search-input')?.focus(), 100);
}

function onSearchInput(val) {
  clearTimeout(_searchTimer);
  const q = val.trim();
  if (!q) { document.getElementById('search-results').innerHTML = ''; return; }
  document.getElementById('search-results').innerHTML = `
    <div class="loading-overlay" style="padding:40px">
      <div class="spinner"></div>
    </div>`;
  _searchTimer = setTimeout(() => doSearch(q), 500);
}

async function doSearch(q) {
  try {
    const { results } = await API.searchChannels(q);
    const el = document.getElementById('search-results');
    if (!el) return;

    if (!results.length) {
      el.innerHTML = `
        <div class="empty-state">
          <div class="empty-icon">🔎</div>
          <div class="empty-title">No channels found</div>
          <div class="empty-sub">Try a different search term</div>
        </div>`;
      return;
    }

    el.innerHTML = `<div class="search-results-grid">${results.map(ch => `
      <div class="channel-result-card" onclick="selectChannel(${JSON.stringify(ch).replace(/"/g,'&quot;')})">
        <img src="${ch.thumbnail}" alt="${escHtml(ch.title)}" onerror="this.src=''" />
        <div>
          <div style="font-weight:700;font-size:.9rem">${escHtml(ch.title)}</div>
          <div style="font-size:.75rem;color:var(--txt-secondary);margin-top:4px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden">
            ${escHtml(ch.description || 'YouTube Channel')}
          </div>
          <div style="margin-top:8px">
            <span class="btn btn-primary btn-sm" style="font-size:.78rem;padding:6px 12px">Analyse →</span>
          </div>
        </div>
      </div>`).join('')}</div>`;
  } catch (e) {
    showToast(e.message, 'error');
    document.getElementById('search-results').innerHTML = '';
  }
}

function selectChannel(ch) {
  AppState.selectedChannel = ch;
  navigate('/analyze');
}
