/**
 * charts.js — Chart.js wrappers
 */
const ChartColors = {
  positive: '#10b981',
  neutral:  '#f59e0b',
  negative: '#ef4444',
  grid:     'rgba(255,255,255,0.05)',
  tick:     '#7e8da0',
};

let _pieChart = null;
let _barChart = null;

function destroyCharts() {
  if (_pieChart) { _pieChart.destroy(); _pieChart = null; }
  if (_barChart) { _barChart.destroy(); _barChart = null; }
}

function renderPieChart(canvasId, data) {
  const ctx = document.getElementById(canvasId).getContext('2d');
  _pieChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Positive', 'Neutral', 'Negative'],
      datasets: [{
        data: [data.positive, data.neutral, data.negative],
        backgroundColor: [ChartColors.positive, ChartColors.neutral, ChartColors.negative],
        borderWidth: 0,
        hoverOffset: 8,
      }]
    },
    options: {
      cutout: '68%',
      plugins: {
        legend: {
          position: 'bottom',
          labels: { color: ChartColors.tick, padding: 16, font: { size: 12, family: 'Inter' } }
        },
        tooltip: {
          callbacks: {
            label: (ctx) => ` ${ctx.label}: ${ctx.raw} comments`
          }
        }
      },
      animation: { animateRotate: true, duration: 800 },
    }
  });
}

function renderBarChart(canvasId, perVideoResults) {
  const ctx = document.getElementById(canvasId).getContext('2d');
  const labels = perVideoResults.map((r, i) => `Video ${i + 1}`);
  const pos = perVideoResults.map(r => r.sentiments.positive_pct);
  const neu = perVideoResults.map(r => r.sentiments.neutral_pct);
  const neg = perVideoResults.map(r => r.sentiments.negative_pct);

  _barChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        { label: 'Positive %', data: pos, backgroundColor: ChartColors.positive, borderRadius: 4 },
        { label: 'Neutral %',  data: neu, backgroundColor: ChartColors.neutral,  borderRadius: 4 },
        { label: 'Negative %', data: neg, backgroundColor: ChartColors.negative, borderRadius: 4 },
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: { color: ChartColors.tick, padding: 14, font: { size: 12, family: 'Inter' } }
        }
      },
      scales: {
        x: {
          stacked: true,
          grid: { color: ChartColors.grid },
          ticks: { color: ChartColors.tick, font: { size: 11 } }
        },
        y: {
          stacked: true,
          max: 100,
          grid: { color: ChartColors.grid },
          ticks: { color: ChartColors.tick, font: { size: 11 }, callback: v => v + '%' }
        }
      },
      animation: { duration: 800 },
    }
  });
}
