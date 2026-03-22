// ── Tab navigation ──
function switchTab(name) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  document.getElementById(`tab-${name}`).classList.add('active');
  document.querySelector(`[data-tab="${name}"]`).classList.add('active');
}

document.querySelectorAll('.nav-item').forEach(item => {
  item.addEventListener('click', e => {
    e.preventDefault();
    switchTab(item.dataset.tab);
  });
});

// ── Range sliders ──
function bindRange(id, suffix) {
  const el = document.getElementById(id);
  const val = document.getElementById(`${id}_val`);
  el.addEventListener('input', () => { val.textContent = `${el.value} ${suffix}`; });
}
bindRange('daily_hours', 'hrs');
bindRange('num_downloads', 'files');
bindRange('social_media_hours', 'hrs');

// ── Streaming toggle ──
document.getElementById('stream-yes').addEventListener('click', () => {
  document.getElementById('streams_video').value = '1';
  document.getElementById('stream-yes').classList.add('active');
  document.getElementById('stream-no').classList.remove('active');
});
document.getElementById('stream-no').addEventListener('click', () => {
  document.getElementById('streams_video').value = '0';
  document.getElementById('stream-no').classList.add('active');
  document.getElementById('stream-yes').classList.remove('active');
});

// ── Session history ──
const sessionHistory = [];

// ── Gauge update ──
function updateGauge(gb, risk) {
  const max = 20;
  const pct = Math.min(gb / max, 1) * 100;
  const colors = { Low: '#00d4aa', Medium: '#f5a623', High: '#ff4d6d' };
  const color = colors[risk] || '#6c63ff';
  const gauge = document.getElementById('gauge');
  gauge.style.background = `conic-gradient(${color} ${pct}%, #22263a ${pct}%)`;
  document.getElementById('gaugeGb').textContent = gb;
}

// ── Analyze form submit ──
document.getElementById('analyzeForm').addEventListener('submit', async e => {
  e.preventDefault();

  const payload = {
    daily_hours: parseFloat(document.getElementById('daily_hours').value),
    streams_video: parseInt(document.getElementById('streams_video').value),
    num_downloads: parseInt(document.getElementById('num_downloads').value),
    social_media_hours: parseFloat(document.getElementById('social_media_hours').value)
  };

  document.getElementById('loading').style.display = 'flex';
  document.getElementById('resultCard').style.display = 'none';

  try {
    const res = await fetch('/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();

    if (data.error) { alert('Error: ' + data.error); return; }

    // Show result card
    document.getElementById('resultCard').style.display = 'block';
    updateGauge(data.predicted_gb, data.risk_level);

    const badge = document.getElementById('riskBadge');
    badge.textContent = `${data.risk_level} Risk`;
    badge.className = `risk-badge risk-${data.risk_level.toLowerCase()}`;

    document.getElementById('adviceBox').textContent = data.advice;

    // Store for what-if and history
    window._lastResult = data;
    window._lastInputs = payload;

    // Add to history
    sessionHistory.unshift({ inputs: payload, result: data, time: new Date() });
    renderHistory();

  } catch (err) {
    alert('Request failed: ' + err.message);
  } finally {
    document.getElementById('loading').style.display = 'none';
  }
});

// ── What-if button (from result card) ──
document.getElementById('whatifBtn').addEventListener('click', () => {
  switchTab('whatif');
  renderWhatIf(window._lastResult);
});

// ── Render what-if ──
function renderWhatIf(data) {
  const container = document.getElementById('whatifContent');
  if (!data || !data.whatif_scenarios || data.whatif_scenarios.length === 0) {
    container.innerHTML = `<div class="empty-state"><span>🔮</span><p>No simulations available for your inputs.</p></div>`;
    return;
  }

  const baseline = data.predicted_gb;
  let html = `
    <div class="card" style="margin-bottom:24px">
      <h2>Baseline: ${baseline} GB/day &nbsp;|&nbsp; Risk: <span class="risk-badge risk-${data.risk_level.toLowerCase()}" style="display:inline;padding:4px 12px">${data.risk_level}</span></h2>
    </div>
    <div class="whatif-grid">
  `;

  data.whatif_scenarios.forEach(s => {
    const saving = s.savings_gb;
    const isSave = saving > 0;
    html += `
      <div class="whatif-card">
        <div class="scenario">${s.scenario}</div>
        <div class="wi-gb">${s.predicted_gb} GB</div>
        <div class="wi-save ${isSave ? '' : 'wi-cost'}">
          ${isSave ? '▼ Save' : '▲ Cost'} ${Math.abs(saving)} GB/day
        </div>
      </div>
    `;
  });

  html += '</div>';
  container.innerHTML = html;
}

// ── Render history ──
function renderHistory() {
  const container = document.getElementById('historyContent');
  if (sessionHistory.length === 0) {
    container.innerHTML = `<div class="empty-state"><span>📋</span><p>No analyses yet.</p></div>`;
    return;
  }

  let html = '<div class="history-list">';
  sessionHistory.forEach((entry, i) => {
    const { inputs: inp, result: r, time } = entry;
    const timeStr = time.toLocaleTimeString();
    html += `
      <div class="history-item">
        <div class="history-meta">
          <strong>#${sessionHistory.length - i}</strong> &nbsp;·&nbsp; ${timeStr}<br/>
          ${inp.daily_hours}h usage &nbsp;·&nbsp; Streaming: ${inp.streams_video ? 'Yes' : 'No'}
          &nbsp;·&nbsp; ${inp.num_downloads} downloads &nbsp;·&nbsp; ${inp.social_media_hours}h social
        </div>
        <div class="history-result">
          <div class="history-gb" style="color:${riskColor(r.risk_level)}">${r.predicted_gb} GB</div>
          <div class="history-num">${r.risk_level} Risk</div>
        </div>
      </div>
    `;
  });
  html += '</div>';
  container.innerHTML = html;
}

function riskColor(risk) {
  return { Low: '#00d4aa', Medium: '#f5a623', High: '#ff4d6d' }[risk] || '#6c63ff';
}
