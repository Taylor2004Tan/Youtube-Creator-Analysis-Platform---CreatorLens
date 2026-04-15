/**
 * views/categories.js
 */
async function renderCategories() {
  const app = document.getElementById('app');
  app.innerHTML = `
  <div class="container page">
    <div class="section-header">
      <div class="section-title">Browse by Category</div>
      <div class="section-sub">Choose a niche to explore top creators</div>
    </div>
    <div class="category-grid" id="cat-grid">
      <div class="loading-overlay"><div class="spinner"></div><div class="loading-text">Loading categories…</div></div>
    </div>
  </div>`;

  try {
    const { categories } = await API.getCategories();
    document.getElementById('cat-grid').innerHTML = categories.map(c => `
      <div class="category-card" onclick="navigate('/categories/${encodeURIComponent(c.name)}')">
        <div class="cat-icon">${c.icon}</div>
        <div class="cat-name">${c.name}</div>
        <div class="cat-count">👥 ${c.count} creators</div>
      </div>`).join('');
  } catch (e) {
    showToast(e.message, 'error');
  }
}

async function renderCategoryDetail(categoryName) {
  const app = document.getElementById('app');
  app.innerHTML = `
  <div class="container page">
    <button class="back-btn" onclick="navigate('/categories')">← Back to Categories</button>
    <div class="section-header">
      <div class="section-title" id="cat-title">Loading…</div>
      <div class="section-sub">Click a creator to analyse their audience</div>
    </div>
    <div class="creators-grid" id="creators-grid">
      <div class="loading-overlay"><div class="spinner"></div><div class="loading-text">Fetching creators…</div></div>
    </div>
  </div>`;

  try {
    const { category, icon, creators } = await API.getCategoryCreators(categoryName);
    document.getElementById('cat-title').textContent = `${icon} ${category}`;

    document.getElementById('creators-grid').innerHTML = creators.map(c => `
      <div class="creator-card" id="ccard-${c.handle}" onclick="selectCreatorByHandle('${c.handle}', '${escHtml(c.name)}')">
        <div class="creator-avatar" id="av-${c.handle}">
          ${c.name.charAt(0).toUpperCase()}
        </div>
        <div class="creator-info">
          <div class="creator-name">${escHtml(c.name)}</div>
          <div class="creator-desc">${escHtml(c.desc)}</div>
          <div class="creator-subs" id="subs-${c.handle}">Loading…</div>
        </div>
      </div>`).join('');

    // Resolve handles lazily (fire-and-forget, update UI when done)
    creators.forEach(c => resolveAndUpdate(c.handle));

  } catch (e) {
    showToast(e.message, 'error');
  }
}

async function resolveAndUpdate(handle) {
  try {
    const ch = await API.resolveHandle(handle);
    const subsEl = document.getElementById(`subs-${handle}`);
    const avEl   = document.getElementById(`av-${handle}`);
    if (subsEl) subsEl.textContent = fmtSubs(ch.subscriber_count);
    if (avEl && ch.thumbnail) {
      avEl.innerHTML = `<img src="${ch.thumbnail}" alt="" loading="lazy" />`;
    }
    // Store channel_id on the card for click handling
    const card = document.getElementById(`ccard-${handle}`);
    if (card) card.dataset.channelId = ch.channel_id;
  } catch (_) { /* silently ignore */ }
}

function selectCreatorByHandle(handle, name) {
  const card = document.getElementById(`ccard-${handle}`);
  const channelId = card ? card.dataset.channelId : null;
  if (!channelId) {
    showToast('Still resolving channel… please wait a moment and try again.', 'info');
    return;
  }
  // Store channel info and navigate to analyze
  AppState.selectedChannel = {
    channel_id: channelId,
    title: name,
    thumbnail: card.querySelector('img') ? card.querySelector('img').src : '',
    subscriber_count: card.querySelector('.creator-subs') ? card.querySelector('.creator-subs').textContent : '',
  };
  navigate('/analyze');
}
