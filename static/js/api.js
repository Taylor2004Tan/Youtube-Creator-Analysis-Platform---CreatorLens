/**
 * api.js — Centralised HTTP client
 */
const API = {
  BASE: '',

  async get(path) {
    const res = await fetch(this.BASE + path);
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || `HTTP ${res.status}`);
    return data;
  },

  async post(path, body) {
    const res = await fetch(this.BASE + path, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || `HTTP ${res.status}`);
    return data;
  },

  searchChannels: (q) => API.get(`/api/search?q=${encodeURIComponent(q)}`),
  getCategories: ()   => API.get('/api/categories'),
  getCategoryCreators: (name) => API.get(`/api/categories/${encodeURIComponent(name)}`),
  resolveHandle: (handle) => API.get(`/api/resolve/${encodeURIComponent(handle)}`),
  analyze: (body) => API.post('/api/analyze', body),
};

// Toast helper
function showToast(msg, type = 'info') {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.className = type;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 3500);
}

// Format subscriber count nicely
function fmtSubs(n) {
  n = parseInt(n, 10);
  if (isNaN(n)) return '';
  if (n >= 1_000_000) return (n / 1_000_000).toFixed(1) + 'M subscribers';
  if (n >= 1_000)     return (n / 1_000).toFixed(0)     + 'K subscribers';
  return n + ' subscribers';
}

// HTML sanitization helper
function escHtml(str) {
  return String(str).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}
