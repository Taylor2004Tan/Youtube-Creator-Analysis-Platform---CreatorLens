/**
 * views/analyze.js
 */
function renderAnalyze() {
  const ch = AppState.selectedChannel;
  const app = document.getElementById('app');

  if (!ch) {
    app.innerHTML = `
    <div class="container page">
      <div class="empty-state">
        <div class="empty-icon">🎯</div>
        <div class="empty-title">No creator selected</div>
        <div class="empty-sub">Go back and choose a creator to analyse</div>
        <button class="btn btn-primary" style="margin-top:24px" onclick="navigate('/search')">Search a Creator</button>
      </div>
    </div>`;
    return;
  }

  app.innerHTML = `
  <div class="container page">
    <button class="back-btn" onclick="history.back()">← Back</button>

    <div class="analyze-form">
      <div class="selected-channel-banner">
        <img src="${ch.thumbnail || ''}" alt="" onerror="this.style.display='none'" id="chan-thumb" />
        <div>
          <div class="selected-title">${escHtml(ch.title)}</div>
          <div class="selected-subs">${ch.subscriber_count ? fmtSubs(ch.subscriber_count) : 'YouTube Channel'}</div>
        </div>
      </div>

      <div class="form-group">
        <label class="form-label">
          Videos to Analyse
          <span id="vid-val">5</span>
        </label>
        <input type="range" class="slider-input" id="vid-count" min="1" max="10" value="5"
          oninput="document.getElementById('vid-val').textContent=this.value" />
        <div class="slider-ticks"><span>1</span><span>5</span><span>10</span></div>
      </div>

      <div class="form-group">
        <label class="form-label">
          Comments per Video
          <span id="com-val">20</span>
        </label>
        <input type="range" class="slider-input" id="com-count" min="5" max="100" value="20" step="5"
          oninput="document.getElementById('com-val').textContent=this.value" />
        <div class="slider-ticks"><span>5</span><span>50</span><span>100</span></div>
      </div>

      <button class="btn btn-primary" style="width:100%;justify-content:center;font-size:1rem;padding:14px"
        id="run-btn" onclick="runAnalysis()">
        ▶ Run Analysis
      </button>
    </div>

    <div id="results-area"></div>
  </div>`;
}

async function runAnalysis() {
  const ch = AppState.selectedChannel;
  const videoCount     = parseInt(document.getElementById('vid-count').value);
  const commentsPerVid = parseInt(document.getElementById('com-count').value);

  document.getElementById('run-btn').disabled = true;
  document.getElementById('run-btn').textContent = 'Analysing…';
  destroyCharts();

  document.getElementById('results-area').innerHTML = `
    <div class="loading-overlay">
      <div class="spinner"></div>
      <div class="loading-text">Fetching videos & comments…</div>
      <div class="loading-step">This may take 10–30 seconds depending on comment volume</div>
    </div>`;

  try {
    const data = await API.analyze({
      channel_id: ch.channel_id,
      video_count: videoCount,
      comments_per_video: commentsPerVid,
    });

    renderResults(data);
  } catch (e) {
    showToast('Analysis failed: ' + e.message, 'error');
    document.getElementById('results-area').innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">⚠️</div>
        <div class="empty-title">Analysis failed</div>
        <div class="empty-sub">${escHtml(e.message)}</div>
      </div>`;
  } finally {
    const btn = document.getElementById('run-btn');
    if (btn) { btn.disabled = false; btn.textContent = '▶ Run Analysis'; }
  }
}

function renderResults(data) {
  const agg = data.aggregated_sentiments;
  const rec = data.recommendation;
  const ch  = data.channel;

  const recIconMap = { success: '✅', warning: '⚠️', danger: '❌' };

  const scoreVal  = agg.overall_score;
  const scoreSign = scoreVal >= 0.05 ? 'pos' : scoreVal <= -0.05 ? 'neg' : 'neu';
  const scoreLabel = scoreSign === 'pos' ? 'Positive' : scoreSign === 'neg' ? 'Negative' : 'Neutral';

  document.getElementById('results-area').innerHTML = `
    <div class="results-section">

      <!-- Channel header -->
      <div class="channel-header">
        <img src="${ch.thumbnail || ''}" alt="" onerror="this.style.display='none'" />
        <div class="channel-header-info">
          <h2>${escHtml(ch.title)}</h2>
          <p>${fmtSubs(ch.subscriber_count)} · ${data.videos_analyzed} videos · ${data.total_comments} comments analysed</p>
        </div>
      </div>

      <!-- Summary stats row -->
      <div class="stats-row">
        <div class="stat-card">
          <div class="stat-value" style="color:var(--accent)">${data.videos_analyzed}</div>
          <div class="stat-label">Videos Analysed</div>
        </div>
        <div class="stat-card">
          <div class="stat-value" style="color:var(--accent-2)">${data.total_comments}</div>
          <div class="stat-label">Comments Processed</div>
        </div>
        <div class="stat-card">
          <div class="stat-value overall-score-val ${scoreSign}">${scoreVal >= 0 ? '+' : ''}${scoreVal.toFixed(3)}</div>
          <div class="stat-label">Overall Sentiment Score</div>
          <div class="overall-score-badge ${scoreSign}">${scoreLabel} Audience</div>
        </div>
        <div class="stat-card">
          <div class="stat-value" style="color:var(--positive)">${agg.positive_pct}%</div>
          <div class="stat-label">Positive Rate</div>
        </div>
      </div>

      <!-- Recommendation -->
      <div class="recommendation-banner ${rec.color}">
        <div class="rec-icon">${recIconMap[rec.color] || '📊'}</div>
        <div>
          <div class="rec-label">${escHtml(rec.label)}</div>
          <div class="rec-desc">${escHtml(rec.description)}</div>
          <div class="rec-score">🎯 Positive sentiment: ${agg.positive_pct}%</div>
        </div>
      </div>

      <!-- Sentiment metrics -->
      <div class="sentiment-metrics">
        <div class="sentiment-pill pos">
          <div class="pill-pct pos">${agg.positive_pct}%</div>
          <div class="pill-label">Positive</div>
          <div class="pill-count">${agg.positive} comments</div>
          <div class="sentiment-bar"><div class="sentiment-bar-fill pos" style="width:${agg.positive_pct}%"></div></div>
        </div>
        <div class="sentiment-pill neu">
          <div class="pill-pct neu">${agg.neutral_pct}%</div>
          <div class="pill-label">Neutral</div>
          <div class="pill-count">${agg.neutral} comments</div>
          <div class="sentiment-bar"><div class="sentiment-bar-fill neu" style="width:${agg.neutral_pct}%"></div></div>
        </div>
        <div class="sentiment-pill neg">
          <div class="pill-pct neg">${agg.negative_pct}%</div>
          <div class="pill-label">Negative</div>
          <div class="pill-count">${agg.negative} comments</div>
          <div class="sentiment-bar"><div class="sentiment-bar-fill neg" style="width:${agg.negative_pct}%"></div></div>
        </div>
      </div>

      <!-- Charts -->
      <div class="charts-row">
        <div class="chart-card">
          <div class="chart-title">Sentiment Distribution</div>
          <div class="chart-wrap"><canvas id="pie-chart"></canvas></div>
        </div>
        <div class="chart-card">
          <div class="chart-title">Per-Video Breakdown</div>
          <div class="chart-wrap"><canvas id="bar-chart"></canvas></div>
        </div>
      </div>

      <!-- Per-video table -->
      <div class="video-table">
        <div class="table-header">Per-Video Results</div>
        <div class="video-row video-row-header">
          <div>Video Title</div><div>Comments</div><div>Positive</div><div>Neutral</div><div>Negative</div>
        </div>
        ${data.per_video_results.map(r => `
        <div class="video-row">
          <div class="video-title-cell" title="${escHtml(r.video.title)}">${escHtml(r.video.title)}</div>
          <div>${r.comment_count}</div>
          <div class="pos-cell">${r.sentiments.positive_pct}%</div>
          <div class="neu-cell">${r.sentiments.neutral_pct}%</div>
          <div class="neg-cell">${r.sentiments.negative_pct}%</div>
        </div>`).join('')}
      </div>

      <div style="text-align:center;margin-top:16px">
        <button class="btn btn-secondary" onclick="navigate('/search')">🔍 Analyse Another Creator</button>
      </div>
    </div>`;

  // Render charts after DOM is ready
  requestAnimationFrame(() => {
    renderPieChart('pie-chart', agg);
    renderBarChart('bar-chart', data.per_video_results);
  });
}
