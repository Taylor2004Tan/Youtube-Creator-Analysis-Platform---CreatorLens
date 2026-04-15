/**
 * views/home.js
 */
function renderHome() {
  document.getElementById('app').innerHTML = `
  <div class="container page">
    <div class="hero">
      
      <h1>Find the Right <span class="grad">YouTube Creator</span><br>for Your Brand</h1>
      <p class="hero-sub">
        Analyse real audience sentiment from thousands of comments.
        Get data-driven collaboration recommendations — in seconds.
      </p>
      <div class="hero-actions">
        <button class="btn btn-primary" onclick="navigate('/search')">
          🔍 Search a Creator
        </button>
        <button class="btn btn-secondary" onclick="navigate('/categories')">
          📂 Browse Categories
        </button>
      </div>
    </div>

    <div class="features-strip">
      <div class="feature-item">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Sentiment Analysis</div>
        <div class="feature-desc">VADER NLP classifies every comment as Positive, Neutral, or Negative in real time.</div>
      </div>
      <div class="feature-item">
        <div class="feature-icon">📈</div>
        <div class="feature-title">Visual Insights</div>
        <div class="feature-desc">Interactive doughnut & stacked bar charts reveal audience mood at a glance.</div>
      </div>
      <div class="feature-item">
        <div class="feature-icon">🤝</div>
        <div class="feature-title">Collaboration Score</div>
        <div class="feature-desc">A clear Recommend / Conditional / Not Recommended verdict based on sentiment data.</div>
      </div>
      <div class="feature-item">
        <div class="feature-icon">🔍</div>
        <div class="feature-title">Category Discovery</div>
        <div class="feature-desc">Browse 6 niches with 16+ curated top creators — or search any channel directly.</div>
      </div>
    </div>
  </div>`;
}
