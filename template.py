"""HTML template for Mood Shop monthly dashboard. Built from a known-good rendering."""

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<meta name="robots" content="noindex,nofollow,noarchive">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.5.0/dist/chart.umd.js"></script>
<style>
  :root {{ color-scheme: light; }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang TC", "Microsoft JhengHei", sans-serif;
    background: #e5e7eb;
    color: #1a1a1a;
    line-height: 1.4;
  }}
  .topbar {{
    background: #fff; border-bottom: 1px solid #e5e7eb;
    padding: 10px 24px; display: flex; align-items: center; gap: 16px;
    position: sticky; top: 0; z-index: 10;
  }}
  .topbar a {{ color: #1f6feb; text-decoration: none; font-size: 13px; font-weight: 500; }}
  .topbar a:hover {{ text-decoration: underline; }}
  .topbar .sep {{ color: #cbd5e1; }}
  .page {{
    width: 1060px;
    margin: 20px auto;
    padding: 22px 26px;
    background: #fff;
    border-radius: 6px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  }}
  .page + .page {{ margin-top: 12px; }}
  header {{ margin-bottom: 14px; }}
  h1 {{ font-size: 22px; margin: 0; font-weight: 700; color: #111; }}
  .kpi-grid {{
    display: grid; grid-template-columns: repeat(5, 1fr);
    gap: 10px; margin-bottom: 14px;
  }}
  .kpi {{
    background: #fff; border: 1px solid #e5e7eb; border-radius: 8px;
    padding: 10px 12px;
  }}
  .kpi .label {{ font-size: 10px; color: #888; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 3px; }}
  .kpi .value {{ font-size: 18px; font-weight: 700; color: #111; }}
  .kpi .unit {{ font-size: 11px; color: #888; margin-left: 2px; font-weight: 500; }}
  .kpi.spend .value {{ color: #1f6feb; }}
  .kpi.revenue .value {{ color: #16a34a; }}
  .kpi.roas .value {{ color: #d97706; }}
  .kpi.purchases .value {{ color: #7c3aed; }}
  .kpi.cpp .value {{ color: #dc2626; }}
  h2 {{ font-size: 13px; margin: 0 0 8px; font-weight: 700; color: #111; }}
  .hint {{ font-size: 10px; color: #9ca3af; font-weight: 400; }}
  .compare-wrap {{
    display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 14px;
  }}
  .compare-card {{
    background: #fff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 12px 14px;
  }}
  .compare-stats {{
    display: grid; grid-template-columns: 1fr 1fr; gap: 8px;
    margin-bottom: 8px;
  }}
  .stat-box {{ padding: 8px 10px; border-radius: 6px; text-align: center; }}
  .stat-box.apparel {{ background: #fef3c7; border: 1px solid #fde68a; }}
  .stat-box.other   {{ background: #eff6ff; border: 1px solid #bfdbfe; }}
  .stat-box .slabel {{ font-size: 10px; color: #666; margin-bottom: 2px; }}
  .stat-box .svalue {{ font-size: 14px; font-weight: 700; }}
  .stat-box.apparel .svalue {{ color: #78350f; }}
  .stat-box.other .svalue {{ color: #1e3a8a; }}
  .chart-container {{ position: relative; height: 260px; }}
  .chart-container.tall {{ height: 340px; }}
  .table-wrap {{ overflow-x: auto; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 11.5px; white-space: nowrap; }}
  th, td {{ padding: 6px 10px; text-align: center; border-bottom: 1px solid #f1f3f5; color: #111; }}
  th {{ background: #fafafa; color: #555; font-weight: 600; font-size: 10.5px; text-transform: uppercase; letter-spacing: 0.03em; }}
  tr.campaign {{ cursor: pointer; }}
  tr.campaign:hover td {{ background: #fafbfc; }}
  tr.campaign td:first-child {{ text-align: left; font-weight: 500; padding-left: 14px; }}
  .caret {{
    display: inline-block; width: 0; height: 0;
    border-left: 4px solid #888; border-top: 4px solid transparent; border-bottom: 4px solid transparent;
    margin-right: 6px; transition: transform 0.15s;
  }}
  tr.campaign.open .caret {{ transform: rotate(90deg); }}
  tr.adset {{ background: #f8fafc; font-size: 11px; display: none; }}
  tr.adset.show {{ display: table-row; }}
  tr.adset td {{ color: #475569; padding: 5px 10px; border-bottom: 1px solid #eef1f4; }}
  tr.adset td:first-child {{ text-align: left; padding-left: 34px; font-weight: 400; color: #64748b; }}
  tr.adset:hover td {{ background: #f1f5f9; }}
  .stat-box .multi-stats {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 4px; margin-top: 4px; }}
  .stat-box .ms-item {{ font-size: 11px; }}
  .stat-box .ms-label {{ font-size: 9px; color: #888; display: block; margin-bottom: 1px; font-weight: 400; }}
  .stat-box .ms-value {{ font-weight: 700; font-size: 12px; }}
  .stat-box.apparel .ms-value {{ color: #78350f; }}
  .stat-box.other .ms-value {{ color: #1e3a8a; }}
  /* subtotal variants */
  tr.subtotal.apparel {{ background: #fef3c7; }}
  tr.subtotal.apparel td {{ color: #78350f; border-top: 1px solid #fde68a; border-bottom: 1px solid #fde68a; }}
  tr.subtotal.other {{ background: #eff6ff; }}
  tr.subtotal.other td {{ color: #1e3a8a; border-top: 1px solid #bfdbfe; border-bottom: 1px solid #bfdbfe; }}
  tr.subtotal {{ font-weight: 700; background: #eff6ff; }}
  tr.subtotal td {{ color: #1e3a8a; border-top: 1px solid #bfdbfe; border-bottom: 1px solid #bfdbfe; font-size: 11.5px; }}
  tr.subtotal td:first-child {{ text-align: left; padding-left: 14px; font-style: italic; }}
  tr.total {{ font-weight: 800; background: #fef3c7; }}
  tr.total td {{ color: #78350f; border-top: 2px solid #f59e0b; border-bottom: none; padding: 9px 10px; font-size: 12px; }}
  tr.total td:first-child {{ text-align: left; padding-left: 14px; }}
  .note {{ font-size: 9.5px; color: #9ca3af; margin-top: 8px; text-align: left; }}
  @media print {{
    .topbar {{ display: none; }}
    body {{ background: #fff; }}
    .page {{ box-shadow: none; margin: 0; page-break-after: always; }}
    .page:last-child {{ page-break-after: auto; }}
    @page {{ size: A4 landscape; margin: 8mm; }}
    tr.adset {{ display: table-row !important; }}
    tr.campaign .caret {{ display: none; }}
  }}
</style>
</head>
<body>

<div class="topbar">
  <a href="index.html">← 返回總覽</a>
  <span class="sep">│</span>
{month_links}
  <span style="margin-left:auto; color:#6b7280; font-size:11px;">目前檢視：{title}</span>
</div>

<!-- PAGE 1 -->
<div class="page">
<header><h1>{title}</h1></header>

<div class="kpi-grid">
  <div class="kpi spend"><div class="label">總花費</div><div class="value">${total_cost:,}<span class="unit"> TWD</span></div></div>
  <div class="kpi revenue"><div class="label">總轉換值</div><div class="value">${total_value:,}<span class="unit"> TWD</span></div></div>
  <div class="kpi roas"><div class="label">整體 ROAS</div><div class="value">{total_roas:.2f}<span class="unit">x</span></div></div>
  <div class="kpi purchases"><div class="label">購買次數</div><div class="value">{total_purchases:,}<span class="unit"> 筆</span></div></div>
  <div class="kpi cpp"><div class="label">平均每次購買成本</div><div class="value">${total_cpp:,}<span class="unit"> TWD</span></div></div>
</div>

<h2>服飾 vs 異業 類別比較 <span class="hint">（活動名稱日期後含「服飾」＝服飾；其餘＝異業）</span></h2>
<div class="compare-wrap">
  <div class="compare-card">
    <div class="compare-stats">
      <div class="stat-box apparel">
        <div class="slabel">服飾（{apparel_count} 檔）</div>
        <div class="multi-stats" id="apparelSummary">—</div>
      </div>
      <div class="stat-box other">
        <div class="slabel">異業（{other_count} 檔）</div>
        <div class="multi-stats" id="otherSummary">—</div>
      </div>
    </div>
    <div class="chart-container"><canvas id="spendRevChart"></canvas></div>
  </div>
  <div class="compare-card">
    <div class="compare-stats">
      <div class="stat-box apparel"><div class="slabel">服飾購買 / CPP</div><div class="svalue" id="apparelPurch">—</div></div>
      <div class="stat-box other"><div class="slabel">異業購買 / CPP</div><div class="svalue" id="otherPurch">—</div></div>
    </div>
    <div class="chart-container"><canvas id="purchCppChart"></canvas></div>
  </div>
</div>
</div>

<!-- PAGE 2 -->
<div class="page">
<h2>受眾包累積排行 <span class="hint">（同名廣告組合跨直播累積；依轉換值由高到低排列）</span></h2>
<div class="compare-wrap">
  <div class="compare-card">
    <div style="font-size:11px; color:#1e3a8a; font-weight:700; margin-bottom:6px; text-align:center;">服飾類受眾包</div>
    <div class="chart-container tall"><canvas id="apparelAdsetChart"></canvas></div>
  </div>
  <div class="compare-card">
    <div style="font-size:11px; color:#78350f; font-weight:700; margin-bottom:6px; text-align:center;">異業類受眾包</div>
    <div class="chart-container tall"><canvas id="otherAdsetChart"></canvas></div>
  </div>
</div>
</div>

<!-- PAGE 3 -->
<div class="page">
<h2>活動明細表 <span class="hint">（點擊活動名稱展開廣告組合；列印 PDF 時自動全部展開）</span></h2>
<div class="table-wrap">
<table id="detailTable">
  <thead><tr>
    <th>活動名稱</th><th>預算</th><th>花費</th><th>轉換值</th><th>ROAS</th><th>購買次數</th><th>每次購買成本</th>
  </tr></thead>
  <tbody id="tableBody"></tbody>
</table>
</div>
<div class="note">※ {date_range_note} 使用 Omni 購買欄位，涵蓋網站+App+On-Facebook+離線全通路。</div>
</div>

<script>
const campaignData = {campaigns_json};

campaignData.forEach(c => {{
  c.cost = c.adsets.reduce((s, a) => s + a.cost, 0);
  c.value = c.adsets.reduce((s, a) => s + a.value, 0);
  c.purchases = c.adsets.reduce((s, a) => s + a.purchases, 0);
  c.roas = c.cost > 0 ? c.value / c.cost : null;
  c.cpp = c.purchases > 0 ? c.cost / c.purchases : null;
  c.adsets.forEach(a => {{
    a.roas = a.cost > 0 ? a.value / a.cost : null;
    a.cpp = a.purchases > 0 ? a.cost / a.purchases : null;
  }});
}});

const fmt = (n) => n == null ? "—" : "$" + Math.round(n).toLocaleString();
const fmtNum = (n) => n == null ? "—" : Math.round(n).toLocaleString();
const fmtRoas = (n) => n == null || !isFinite(n) ? "—" : n.toFixed(2) + "x";

// ---- BUILD TABLE FIRST (robust against chart failures) ----
const tbody = document.getElementById("tableBody");
const groupLabels = {{}};  // will be overridden by campaign groups
const groupedCampaigns = {{}};
campaignData.forEach(c => {{
  if (!groupedCampaigns[c.group]) groupedCampaigns[c.group] = [];
  groupedCampaigns[c.group].push(c);
}});

let grandBudget = 0, grandCost = 0, grandValue = 0, grandPurchases = 0;

function getMonth(c) {{
  const m = c.name.match(/^(\d+)\/(\d+)/);
  return m ? parseInt(m[1]) : 0;
}}

Object.keys(groupedCampaigns).sort((a,b) => a - b).forEach(gKey => {{
  const list = groupedCampaigns[gKey];
  const groupHasMixed = list.some(c => c.category === "apparel") && list.some(c => c.category === "other");

  let buffer = [];
  let currentCat = null;

  function flushBuffer() {{
    if (buffer.length === 0) return;
    const sB = buffer.reduce((s, c) => s + c.budget, 0);
    const sC = buffer.reduce((s, c) => s + c.cost, 0);
    const sV = buffer.reduce((s, c) => s + c.value, 0);
    const sP = buffer.reduce((s, c) => s + c.purchases, 0);
    const sR = sC > 0 ? sV / sC : null;
    const sCpp = sP > 0 ? sC / sP : null;

    let label;
    if (groupHasMixed) {{
      const days = buffer.map(c => c.day).filter(d => d > 0);
      const month = getMonth(buffer[0]);
      const minD = Math.min(...days), maxD = Math.max(...days);
      const dateRange = minD === maxD ? `${{month}}/${{minD}}` : `${{month}}/${{minD}}–${{month}}/${{maxD}}`;
      const catLabel = currentCat === "apparel" ? "服飾" : "異業";
      label = `${{dateRange}} ${{catLabel}}小計`;
    }} else {{
      label = list[0].groupLabel;
    }}

    const tr = document.createElement("tr");
    tr.className = "subtotal" + (groupHasMixed ? " " + currentCat : "");
    tr.innerHTML = `<td>${{label}}</td><td>${{fmt(sB)}}</td><td>${{fmt(sC)}}</td><td>${{fmt(sV)}}</td><td>${{fmtRoas(sR)}}</td><td>${{fmtNum(sP)}}</td><td>${{fmt(sCpp)}}</td>`;
    tbody.appendChild(tr);
    grandBudget += sB; grandCost += sC; grandValue += sV; grandPurchases += sP;
    buffer = [];
  }}

  list.forEach(c => {{
    // Category transition → flush buffer first
    if (currentCat !== null && c.category !== currentCat) {{
      flushBuffer();
    }}
    currentCat = c.category;

    // Render campaign row
    const tr = document.createElement("tr");
    tr.className = "campaign";
    tr.innerHTML = `<td><span class="caret"></span>${{c.name}}</td><td>${{fmt(c.budget)}}</td><td>${{fmt(c.cost)}}</td><td>${{fmt(c.value)}}</td><td>${{fmtRoas(c.roas)}}</td><td>${{fmtNum(c.purchases)}}</td><td>${{fmt(c.cpp)}}</td>`;
    tbody.appendChild(tr);
    c.adsets.forEach(a => {{
      const trA = document.createElement("tr");
      trA.className = "adset";
      trA.innerHTML = `<td>└ ${{a.name}}</td><td>—</td><td>${{fmt(a.cost)}}</td><td>${{a.value === 0 ? "—" : fmt(a.value)}}</td><td>${{fmtRoas(a.roas)}}</td><td>${{a.purchases === 0 ? "—" : fmtNum(a.purchases)}}</td><td>${{fmt(a.cpp)}}</td>`;
      tbody.appendChild(trA);
    }});
    tr.addEventListener("click", () => {{
      const isOpen = tr.classList.toggle("open");
      let next = tr.nextElementSibling;
      while (next && next.classList.contains("adset")) {{
        next.classList.toggle("show", isOpen);
        next = next.nextElementSibling;
      }}
    }});

    buffer.push(c);
  }});

  flushBuffer();  // emit final buffer's subtotal
}});

const grandRoas = grandCost > 0 ? grandValue / grandCost : null;
const grandCpp = grandPurchases > 0 ? grandCost / grandPurchases : null;
const trTotal = document.createElement("tr");
trTotal.className = "total";
trTotal.innerHTML = `<td>總計（${{campaignData.length}} 檔）</td><td>${{fmt(grandBudget)}}</td><td>${{fmt(grandCost)}}</td><td>${{fmt(grandValue)}}</td><td>${{fmtRoas(grandRoas)}}</td><td>${{fmtNum(grandPurchases)}}</td><td>${{fmt(grandCpp)}}</td>`;
tbody.appendChild(trTotal);

// ---- CHARTS (wrapped in try so table still works if Chart.js fails) ----
try {{
  function agg(cat) {{
    const list = campaignData.filter(c => c.category === cat);
    const cost = list.reduce((s, c) => s + c.cost, 0);
    const value = list.reduce((s, c) => s + c.value, 0);
    const purchases = list.reduce((s, c) => s + c.purchases, 0);
    return {{ count: list.length, cost, value, purchases, cpp: purchases > 0 ? cost/purchases : 0 }};
  }}
  const apparel = agg("apparel"), other = agg("other");
  const apparelRoas = apparel.cost > 0 ? apparel.value / apparel.cost : 0;
  const otherRoas = other.cost > 0 ? other.value / other.cost : 0;
  document.getElementById("apparelSummary").innerHTML =
    `<div class="ms-item"><span class="ms-label">花費</span><span class="ms-value">${{fmt(apparel.cost)}}</span></div>` +
    `<div class="ms-item"><span class="ms-label">轉換值</span><span class="ms-value">${{fmt(apparel.value)}}</span></div>` +
    `<div class="ms-item"><span class="ms-label">ROAS</span><span class="ms-value">${{apparelRoas.toFixed(2)}}x</span></div>`;
  document.getElementById("otherSummary").innerHTML =
    `<div class="ms-item"><span class="ms-label">花費</span><span class="ms-value">${{fmt(other.cost)}}</span></div>` +
    `<div class="ms-item"><span class="ms-label">轉換值</span><span class="ms-value">${{fmt(other.value)}}</span></div>` +
    `<div class="ms-item"><span class="ms-label">ROAS</span><span class="ms-value">${{otherRoas.toFixed(2)}}x</span></div>`;
  document.getElementById("apparelPurch").textContent = `${{apparel.purchases}} 筆 / CPP ${{fmt(apparel.cpp)}}`;
  document.getElementById("otherPurch").textContent = `${{other.purchases}} 筆 / CPP ${{fmt(other.cpp)}}`;

  new Chart(document.getElementById("spendRevChart"), {{
    type: "bar",
    data: {{ labels: ["花費", "轉換值"], datasets: [
      {{ label: `服飾（${{apparel.count}} 檔）`, data: [apparel.cost, apparel.value], backgroundColor: "#d97706", borderRadius: 4 }},
      {{ label: `異業（${{other.count}} 檔）`, data: [other.cost, other.value], backgroundColor: "#1e3a8a", borderRadius: 4 }}
    ]}},
    options: {{ maintainAspectRatio: false, responsive: true,
      plugins: {{ title: {{ display: true, text: "花費 vs 轉換值", font: {{ size: 12, weight: "bold" }} }}, legend: {{ position: "bottom", labels: {{ font: {{ size: 10 }}, boxWidth: 12 }} }}, tooltip: {{ callbacks: {{ label: ctx => ctx.dataset.label + ": $" + ctx.parsed.y.toLocaleString() }} }} }},
      scales: {{ y: {{ ticks: {{ font: {{ size: 9 }}, callback: v => {{ if (v >= 1000000) return "$" + (v/1000000).toFixed(1) + "M"; if (v >= 1000) return "$" + (v/1000) + "k"; return v; }} }} }}, x: {{ ticks: {{ font: {{ size: 11 }} }} }} }}
    }}
  }});

  new Chart(document.getElementById("purchCppChart"), {{
    type: "bar",
    data: {{ labels: ["購買次數（筆）", "每次購買成本（TWD）"], datasets: [
      {{ label: "服飾", data: [apparel.purchases, apparel.cpp], backgroundColor: "#d97706", borderRadius: 4 }},
      {{ label: "異業", data: [other.purchases, other.cpp], backgroundColor: "#1e3a8a", borderRadius: 4 }}
    ]}},
    options: {{ maintainAspectRatio: false, responsive: true,
      plugins: {{ title: {{ display: true, text: "購買次數 & 每次購買成本", font: {{ size: 12, weight: "bold" }} }}, legend: {{ position: "bottom", labels: {{ font: {{ size: 10 }}, boxWidth: 12 }} }},
        tooltip: {{ callbacks: {{ label: ctx => {{ const v = ctx.parsed.y; if (ctx.dataIndex === 0) return ctx.dataset.label + ": " + v.toLocaleString() + " 筆"; return ctx.dataset.label + ": $" + Math.round(v).toLocaleString(); }} }} }}
      }},
      scales: {{ y: {{ ticks: {{ font: {{ size: 9 }} }} }}, x: {{ ticks: {{ font: {{ size: 11 }} }} }} }}
    }}
  }});

  function rollupAdsets(cat) {{
    const map = {{}};
    campaignData.filter(c => c.category === cat).forEach(c => {{
      c.adsets.forEach(a => {{
        if (!map[a.name]) map[a.name] = {{ name: a.name, cost: 0, value: 0, purchases: 0, appearIn: 0 }};
        map[a.name].cost += a.cost;
        map[a.name].value += a.value;
        map[a.name].purchases += a.purchases;
        map[a.name].appearIn += 1;
      }});
    }});
    const arr = Object.values(map);
    arr.forEach(a => {{ a.cpp = a.purchases > 0 ? a.cost / a.purchases : null; }});
    return arr.sort((a, b) => b.value - a.value);
  }}
  const apparelAdsets = rollupAdsets("apparel"), otherAdsets = rollupAdsets("other");

  function adsetChart(canvasId, data, color) {{
    if (data.length === 0) return;
    new Chart(document.getElementById(canvasId), {{
      type: "bar",
      data: {{ labels: data.map(a => `${{a.name}} (${{a.appearIn}} 場)`), datasets: [
        {{ label: "花費 (TWD)", data: data.map(a => a.cost), backgroundColor: color + "55", borderColor: color, borderWidth: 1, borderRadius: 3 }},
        {{ label: "轉換值 (TWD)", data: data.map(a => a.value), backgroundColor: color, borderRadius: 3 }}
      ]}},
      options: {{ indexAxis: "y", maintainAspectRatio: false, responsive: true,
        plugins: {{ legend: {{ position: "bottom", labels: {{ font: {{ size: 10 }}, boxWidth: 12 }} }},
          tooltip: {{ callbacks: {{ label: ctx => ctx.dataset.label + ": $" + Math.round(ctx.parsed.x).toLocaleString(), afterBody: items => {{ const i = items[0].dataIndex; const a = data[i]; return [`購買: ${{a.purchases}} 筆`, `CPP: ${{a.cpp ? "$" + Math.round(a.cpp) : "—"}}`]; }} }} }}
        }},
        scales: {{ x: {{ ticks: {{ font: {{ size: 9 }}, callback: v => {{ if (v >= 1000000) return "$" + (v/1000000).toFixed(1) + "M"; if (v >= 1000) return "$" + (v/1000) + "k"; return v; }} }} }}, y: {{ ticks: {{ font: {{ size: 10 }} }} }} }}
      }}
    }});
  }}
  adsetChart("apparelAdsetChart", apparelAdsets, "#d97706");
  adsetChart("otherAdsetChart", otherAdsets, "#1e3a8a");
}} catch (e) {{ console.error("Chart init failed:", e); }}
</script>
</body>
</html>"""


def build_index(totals_by_month, months, year, current_month, last_updated=None):
    """Build the overview page (index.html) with all monthly cards."""
    from datetime import datetime, timedelta
    import json as _json
    if last_updated is None:
        last_updated = (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")

    asc_months = sorted([m for m in months if f"{year}-{m:02d}" in totals_by_month])

    ytd = {"cost": 0, "value": 0, "purchases": 0, "count": 0, "month_count": 0}
    for m in asc_months:
        t = totals_by_month[f"{year}-{m:02d}"]
        ytd["cost"] += t["cost"]
        ytd["value"] += t["value"]
        ytd["purchases"] += t["purchases"]
        ytd["count"] += t["count"]
        ytd["month_count"] += 1
    ytd["roas"] = ytd["value"] / ytd["cost"] if ytd["cost"] > 0 else 0
    ytd["cpp"] = ytd["cost"] / ytd["purchases"] if ytd["purchases"] > 0 else 0

    chart_labels = [f"{m}月" for m in asc_months]
    chart_costs = [totals_by_month[f"{year}-{m:02d}"]["cost"] for m in asc_months]
    chart_values = [totals_by_month[f"{year}-{m:02d}"]["value"] for m in asc_months]
    chart_roas = [round(totals_by_month[f"{year}-{m:02d}"]["roas"], 2) for m in asc_months]

    def mom_change(curr_month_int, key):
        idx2 = asc_months.index(curr_month_int)
        if idx2 == 0:
            return None
        prev_m = asc_months[idx2 - 1]
        prev_v = totals_by_month[f"{year}-{prev_m:02d}"][key]
        curr_v = totals_by_month[f"{year}-{curr_month_int:02d}"][key]
        if prev_v == 0:
            return None
        return ((curr_v - prev_v) / prev_v * 100, prev_m)

    def mom_inline(change_tuple, higher_is_better=True):
        if change_tuple is None:
            return ""
        pct, prev_m = change_tuple
        if abs(pct) < 0.5:
            return '<span class="mom">— vs ' + str(prev_m) + '月</span>'
        arrow = "↑" if pct > 0 else "↓"
        return f'<span class="mom">{arrow} {abs(pct):.0f}% vs {prev_m}月</span>'

    def fmt_short(n):
        if n >= 1000000:
            return f"${n/1000000:.2f}M"
        if n >= 1000:
            return f"${n/1000:.0f}k"
        return f"${n:,}"

    def card(year_month, title, totals, month_int, is_current=False, note=""):
        status_badge = '<span class="badge-current">當月</span>' if is_current else ''
        note_html = f'<div class="month-note">{note}</div>' if note else ''
        cls = "current" if is_current else ""
        cost_mom = mom_inline(mom_change(month_int, "cost"), higher_is_better=False)
        value_mom = mom_inline(mom_change(month_int, "value"), higher_is_better=True)
        roas_mom = mom_inline(mom_change(month_int, "roas"), higher_is_better=True)
        purch_mom = mom_inline(mom_change(month_int, "purchases"), higher_is_better=True)
        cpp_mom = mom_inline(mom_change(month_int, "cpp"), higher_is_better=False)
        return f"""
    <a class="month-card {cls}" href="{year_month}.html">
      <div class="month-head">
        <div class="month-title">{title} {status_badge}</div>
        <div class="month-arrow">→</div>
      </div>
      <div class="month-kpis-row">
        <div class="kpi-cell"><span class="kc-label">花費</span><span class="kc-value spend">${totals['cost']:,}</span>{cost_mom}</div>
        <div class="kpi-cell"><span class="kc-label">轉換值</span><span class="kc-value revenue">{fmt_short(totals['value'])}</span>{value_mom}</div>
        <div class="kpi-cell"><span class="kc-label">ROAS</span><span class="kc-value roas">{totals['roas']:.2f}x</span>{roas_mom}</div>
        <div class="kpi-cell"><span class="kc-label">購買</span><span class="kc-value purch">{totals['purchases']:,} 筆</span>{purch_mom}</div>
        <div class="kpi-cell"><span class="kc-label">CPP</span><span class="kc-value cpp">${round(totals['cpp']):,}</span>{cpp_mom}</div>
      </div>
      {note_html}
    </a>
    """

    cards = []
    for m in sorted(asc_months, reverse=True):
        ym = f"{year}-{m:02d}"
        is_cur = m == current_month
        note = "※ 當月最新資料，部分場次歸因窗可能尚未完成。" if is_cur else ""
        cards.append(card(ym, f"{year} 年 {m} 月", totals_by_month[ym], m, is_cur, note))
    cards_html = "\n".join(cards)

    head = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<title>Mood Shop 廣告成效總覽</title>
<meta name="robots" content="noindex,nofollow,noarchive">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.5.0/dist/chart.umd.js"></script>
"""

    css = """<style>
  :root { color-scheme: light; }
  * { box-sizing: border-box; }
  body { margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang TC", "Microsoft JhengHei", sans-serif; background: linear-gradient(135deg, #f0f4ff 0%, #fef7ed 100%); color: #1a1a1a; line-height: 1.5; min-height: 100vh; }
  .container { max-width: 980px; margin: 0 auto; padding: 32px 24px; }
  .hero { text-align: center; margin-bottom: 20px; }
  .hero h1 { font-size: 28px; margin: 0 0 6px; color: #111; font-weight: 800; letter-spacing: -0.02em; }
  .hero p { font-size: 13px; color: #6b7280; margin: 0; }

  /* YTD: 3 big + 3 small */
  .ytd-banner { background: #fff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 20px 28px; margin-bottom: 14px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
  .ytd-title { font-size: 11px; color: #888; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 14px; font-weight: 600; }
  .ytd-primary { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; margin-bottom: 12px; padding-bottom: 12px; border-bottom: 1px solid #f1f3f5; }
  .ytd-primary .yp-label { font-size: 10px; color: #888; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 4px; }
  .ytd-primary .yp-value { font-size: 26px; font-weight: 800; color: #111; }
  .ytd-primary .yp-value.spend { color: #1f6feb; }
  .ytd-primary .yp-value.revenue { color: #16a34a; }
  .ytd-primary .yp-value.roas { color: #d97706; }
  .ytd-secondary { display: flex; gap: 18px; font-size: 12px; color: #555; }
  .ytd-secondary .ys-item { color: #555; }
  .ytd-secondary .ys-value { font-weight: 700; color: #1a1a1a; }
  .ytd-secondary .sep { color: #d1d5db; }

  /* Trend chart */
  .trend-card { background: #fff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 16px 22px 12px; margin-bottom: 22px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
  .trend-title { font-size: 11px; color: #888; text-transform: uppercase; letter-spacing: 0.06em; font-weight: 600; margin-bottom: 6px; }
  .trend-canvas-wrap { height: 180px; position: relative; }

  /* Monthly cards: compact horizontal */
  .months-grid { display: grid; grid-template-columns: 1fr; gap: 12px; }
  .month-card { background: #fff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 16px 22px; text-decoration: none; color: inherit; transition: all 0.15s ease; box-shadow: 0 2px 8px rgba(0,0,0,0.04); display: block; }
  .month-card:hover { transform: translateY(-1px); box-shadow: 0 6px 18px rgba(0,0,0,0.07); border-color: #1f6feb; }
  .month-card.current { border: 2px solid #d97706; background: linear-gradient(to right, #fff, #fef9f0); }
  .month-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
  .month-title { font-size: 16px; font-weight: 700; color: #111; display: flex; align-items: center; gap: 8px; }
  .badge-current { background: #d97706; color: #fff; font-size: 9px; padding: 2px 7px; border-radius: 4px; letter-spacing: 0.02em; font-weight: 600; }
  .month-arrow { font-size: 18px; color: #9ca3af; transition: transform 0.15s, color 0.15s; }
  .month-card:hover .month-arrow { color: #1f6feb; transform: translateX(3px); }

  .month-kpis-row { display: grid; grid-template-columns: 1.3fr 1.3fr 1fr 1.3fr 1fr; gap: 10px; }
  .kpi-cell { display: flex; flex-direction: column; gap: 1px; padding: 6px 8px; background: #fafbfc; border-radius: 5px; }
  .kc-label { font-size: 9px; color: #888; text-transform: uppercase; letter-spacing: 0.04em; }
  .kc-value { font-size: 14px; font-weight: 700; color: #111; display: inline; }
  .kc-value.spend { color: #1f6feb; }
  .kc-value.revenue { color: #16a34a; }
  .kc-value.roas { color: #d97706; }
  .kc-value.purch { color: #7c3aed; }
  .kc-value.cpp { color: #dc2626; }
  .mom { display: block; font-size: 10px; margin-top: 3px; font-weight: 500; color: #9ca3af; }

  .month-note { font-size: 10.5px; color: #92400e; background: #fef3c7; padding: 6px 10px; border-radius: 5px; margin-top: 10px; border-left: 3px solid #d97706; }
  .footer { text-align: center; margin-top: 24px; font-size: 10.5px; color: #9ca3af; line-height: 1.7; }
  .footer .updated { color: #1f6feb; font-weight: 600; }
  @media (max-width: 700px) {
    .month-kpis-row { grid-template-columns: 1fr 1fr; }
    .ytd-primary { grid-template-columns: 1fr; }
    .ytd-secondary { flex-wrap: wrap; }
    .hero h1 { font-size: 22px; }
  }
</style>
</head>
<body>
"""

    body = f"""<div class="container">
  <div class="hero">
    <h1>Mood Shop 廣告成效總覽</h1>
    <p>點擊下方月份卡片，查看該月完整報表</p>
  </div>

  <div class="ytd-banner">
    <div class="ytd-title">{year} 年累計（{ytd['month_count']} 個月）</div>
    <div class="ytd-primary">
      <div><div class="yp-label">總花費</div><div class="yp-value spend">${ytd['cost']:,}</div></div>
      <div><div class="yp-label">總轉換值</div><div class="yp-value revenue">${ytd['value']:,}</div></div>
      <div><div class="yp-label">整體 ROAS</div><div class="yp-value roas">{ytd['roas']:.2f}x</div></div>
    </div>
    <div class="ytd-secondary">
      <span class="ys-item">購買 <span class="ys-value">{ytd['purchases']:,} 筆</span></span>
      <span class="sep">|</span>
      <span class="ys-item">每次購買成本 <span class="ys-value">${round(ytd['cpp']):,}</span></span>
      <span class="sep">|</span>
      <span class="ys-item">活動總數 <span class="ys-value">{ytd['count']} 檔</span></span>
    </div>
  </div>

  <div class="trend-card">
    <div class="trend-title">月度趨勢</div>
    <div class="trend-canvas-wrap"><canvas id="trendChart"></canvas></div>
  </div>

  <div class="months-grid">
{cards_html}
  </div>

  <div class="footer">
    <span class="updated">資料最後更新：{last_updated}</span>　｜　每天台灣時間 9:00 自動更新<br>
    資料來源：Facebook Ads（Mood Shop.連線）｜歸因窗 7 天｜Omni 購買欄位
  </div>
</div>
"""

    chart_labels_json = _json.dumps(chart_labels, ensure_ascii=False)
    chart_costs_json = _json.dumps(chart_costs)
    chart_values_json = _json.dumps(chart_values)
    chart_roas_json = _json.dumps(chart_roas)

    script = f"""<script>
try {{
  const labels = {chart_labels_json};
  const costs = {chart_costs_json};
  const values = {chart_values_json};
  const roas = {chart_roas_json};
  new Chart(document.getElementById('trendChart'), {{
    data: {{
      labels: labels,
      datasets: [
        {{ type: 'bar', label: '花費 (TWD)', data: costs, backgroundColor: '#1f6feb88', borderColor: '#1f6feb', borderWidth: 1, borderRadius: 4, yAxisID: 'y' }},
        {{ type: 'bar', label: '轉換值 (TWD)', data: values, backgroundColor: '#16a34a88', borderColor: '#16a34a', borderWidth: 1, borderRadius: 4, yAxisID: 'y' }},
        {{ type: 'line', label: 'ROAS (x)', data: roas, borderColor: '#d97706', backgroundColor: '#d97706', borderWidth: 2, pointRadius: 4, tension: 0.2, yAxisID: 'y1' }}
      ]
    }},
    options: {{
      maintainAspectRatio: false, responsive: true,
      plugins: {{
        legend: {{ position: 'bottom', labels: {{ font: {{ size: 10 }}, boxWidth: 10 }} }},
        tooltip: {{ callbacks: {{ label: ctx => {{
          const v = ctx.parsed.y;
          if (ctx.dataset.label.includes('ROAS')) return ctx.dataset.label + ': ' + v.toFixed(2) + 'x';
          return ctx.dataset.label + ': $' + Math.round(v).toLocaleString();
        }} }} }}
      }},
      scales: {{
        y: {{ position: 'left', ticks: {{ font: {{ size: 9 }}, callback: v => {{ if (v >= 1000000) return '$' + (v/1000000).toFixed(1) + 'M'; if (v >= 1000) return '$' + (v/1000) + 'k'; return '$' + v; }} }} }},
        y1: {{ position: 'right', grid: {{ drawOnChartArea: false }}, ticks: {{ font: {{ size: 9 }}, callback: v => v + 'x' }} }},
        x: {{ ticks: {{ font: {{ size: 11 }} }} }}
      }}
    }}
  }});
}} catch (e) {{ console.error('Trend chart failed:', e); }}
</script>
</body>
</html>"""

    return head + css + body + script



APP_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<title>Mood Shop 廣告報表</title>
<meta name="robots" content="noindex,nofollow,noarchive">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.5.0/dist/chart.umd.js"></script>
<style>
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang TC", "Microsoft JhengHei", sans-serif; background: #f3f1ec; color: #1a1a1a; line-height: 1.5; }}
  .app {{ display: flex; min-height: 100vh; }}
  .sidebar {{ width: 240px; flex-shrink: 0; background: #faf5ee; border-right: 1px solid #e5dfd2; padding: 28px 0 20px; position: sticky; top: 0; height: 100vh; overflow-y: auto; }}
  .brand {{ padding: 0 24px 22px; border-bottom: 1px solid #ebe5d6; }}
  .brand h1 {{ font-size: 15px; margin: 0 0 4px; color: #2d2a26; font-weight: 800; letter-spacing: 0; white-space: nowrap; }}
  .brand p {{ font-size: 11.5px; color: #8a8170; margin: 0; }}
  .sb-nav {{ padding: 16px 14px; }}
  .sb-label {{ font-size: 10px; color: #b0a48f; text-transform: uppercase; letter-spacing: 0.06em; padding: 0 10px; margin-bottom: 10px; font-weight: 600; }}
  .sb-tab {{ display: block; padding: 9px 14px; border-radius: 7px; color: #4a4438; font-size: 13.5px; font-weight: 500; cursor: pointer; text-decoration: none; margin: 2px 0; transition: all 0.15s; }}
  .sb-tab:hover {{ background: #f0e8d9; }}
  .sb-tab.active {{ background: #fff; color: #1a1a1a; box-shadow: 0 1px 4px rgba(0,0,0,0.05); font-weight: 700; }}
  .sb-footer {{ margin-top: 28px; padding: 16px 24px; border-top: 1px solid #ebe5d6; font-size: 11px; color: #8a8170; }}
  .sb-footer .updated-time {{ color: #5a5246; font-weight: 600; margin-top: 2px; }}
  .main {{ flex: 1; padding: 28px 36px 40px; overflow-x: auto; max-width: 100%; }}
  .tab-content {{ display: none; }}
  .tab-content.active {{ display: block; }}
  .page-head {{ margin-bottom: 18px; }}
  .page-title {{ font-size: 24px; font-weight: 800; color: #1a1a1a; margin: 0 0 6px; }}
  .page-subtitle {{ font-size: 13px; color: #8a8170; margin: 0; }}
  .month-picker {{ display: flex; gap: 6px; margin-bottom: 22px; background: #ebe5d6; padding: 5px; border-radius: 9px; width: fit-content; }}
  .month-tab {{ padding: 7px 18px; border-radius: 6px; color: #6b6258; font-size: 13px; font-weight: 600; cursor: pointer; text-decoration: none; transition: all 0.15s; display: flex; align-items: center; gap: 6px; }}
  .month-tab:hover {{ background: #faf5ee; }}
  .month-tab.active {{ background: #fff; color: #1a1a1a; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
  .m-badge {{ background: #d97706; color: #fff; font-size: 9px; padding: 1px 5px; border-radius: 3px; font-weight: 600; }}
  .kpi-row {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 22px; }}
  .kpi-row.five {{ grid-template-columns: repeat(5, 1fr); }}
  .kpi {{ background: #fff; border: 1px solid #e7e2d6; border-radius: 10px; padding: 16px 18px; }}
  .kpi-label {{ font-size: 11px; color: #8a8170; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px; font-weight: 600; }}
  .kpi-value {{ font-size: 22px; font-weight: 800; color: #1a1a1a; line-height: 1.2; }}
  .kpi.spend .kpi-value {{ color: #1f6feb; }}
  .kpi.revenue .kpi-value {{ color: #16a34a; }}
  .kpi.roas .kpi-value {{ color: #d97706; }}
  .kpi.purch .kpi-value {{ color: #7c3aed; }}
  .kpi.cpp .kpi-value {{ color: #dc2626; }}
  .kpi.amount .kpi-value {{ color: #c2410c; font-size: 24px; }}
  .card {{ background: #fff; border: 1px solid #e7e2d6; border-radius: 10px; padding: 22px 26px; margin-bottom: 16px; }}
  .card h2 {{ font-size: 14px; margin: 0 0 14px; color: #1a1a1a; font-weight: 700; }}
  .card .hint {{ font-size: 11px; color: #9c9489; font-weight: 400; margin-left: 8px; }}
  .ytd-banner {{ background: #fff; border: 1px solid #e7e2d6; border-radius: 12px; padding: 24px 30px; margin-bottom: 18px; }}
  .ytd-title {{ font-size: 11px; color: #8a8170; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 16px; font-weight: 600; }}
  .ytd-primary {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; padding-bottom: 14px; border-bottom: 1px solid #ebe5d6; margin-bottom: 12px; }}
  .ytd-primary .yp-label {{ font-size: 10px; color: #8a8170; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 4px; }}
  .ytd-primary .yp-value {{ font-size: 28px; font-weight: 800; color: #1a1a1a; }}
  .ytd-primary .yp-value.spend {{ color: #1f6feb; }}
  .ytd-primary .yp-value.revenue {{ color: #16a34a; }}
  .ytd-primary .yp-value.roas {{ color: #d97706; }}
  .ytd-secondary {{ display: flex; gap: 22px; font-size: 12.5px; color: #5a5246; flex-wrap: wrap; }}
  .ytd-secondary b {{ color: #1a1a1a; font-weight: 700; }}
  .ytd-secondary .sep {{ color: #d4cfc0; }}
  .trend-card {{ background: #fff; border: 1px solid #e7e2d6; border-radius: 10px; padding: 18px 24px; margin-bottom: 22px; }}
  .trend-title {{ font-size: 11px; color: #8a8170; text-transform: uppercase; letter-spacing: 0.06em; font-weight: 600; margin-bottom: 8px; }}
  .trend-canvas-wrap {{ height: 200px; position: relative; }}
  .months-grid {{ display: grid; grid-template-columns: 1fr; gap: 12px; }}
  .month-card {{ background: #fff; border: 1px solid #e7e2d6; border-radius: 10px; padding: 18px 24px; text-decoration: none; color: inherit; cursor: pointer; transition: all 0.15s; display: block; }}
  .month-card:hover {{ border-color: #d97706; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,0,0,0.05); }}
  .month-card.current {{ border: 2px solid #d97706; background: #fff; }}
  .mc-head {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }}
  .mc-title {{ font-size: 17px; font-weight: 700; color: #1a1a1a; }}
  .mc-arrow {{ font-size: 18px; color: #b0a48f; }}
  .card-badge {{ background: #d97706; color: #fff; font-size: 9px; padding: 1px 6px; border-radius: 3px; font-weight: 600; margin-left: 6px; }}
  .mc-stats {{ display: grid; grid-template-columns: repeat(6, 1fr); gap: 10px; }}
  .mc-stats > div {{ display: flex; flex-direction: column; gap: 2px; }}
  .mc-label {{ font-size: 10px; color: #8a8170; text-transform: uppercase; letter-spacing: 0.04em; }}
  .mc-val {{ font-size: 14px; font-weight: 700; color: #1a1a1a; }}
  .mc-val.spend {{ color: #1f6feb; }}
  .mc-val.rev {{ color: #16a34a; }}
  .mc-val.roas {{ color: #d97706; }}
  .mc-val.purch {{ color: #7c3aed; }}
  .mc-val.cpp {{ color: #dc2626; }}
  .billing {{ display: grid; grid-template-columns: 1fr auto; gap: 8px 24px; font-size: 14px; }}
  .billing .label {{ color: #4a4438; }}
  .billing .value {{ font-weight: 600; color: #1a1a1a; text-align: right; font-variant-numeric: tabular-nums; }}
  .billing .sep {{ grid-column: 1 / -1; height: 1px; background: #ebe5d6; margin: 6px 0; }}
  .billing .total {{ font-weight: 800; color: #c2410c; font-size: 17px; }}
  .billing .add {{ color: #16a34a; }}
  .billing .sub {{ color: #dc2626; }}
  .formula {{ font-size: 11px; color: #9c9489; margin-top: 2px; font-style: italic; }}
  .info-banner {{ background: linear-gradient(to right, #fef3c7, #fef9f0); border-left: 4px solid #d97706; padding: 12px 18px; border-radius: 6px; margin: 18px 0; font-size: 13px; color: #92400e; }}
  .info-banner b {{ color: #78350f; }}
  /* ROI section reuses old dashboard styles */
  .compare-wrap {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 14px; }}
  .compare-card {{ background: #fff; border: 1px solid #e7e2d6; border-radius: 10px; padding: 14px 16px; }}
  .compare-stats {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 8px; }}
  .stat-box {{ padding: 10px 12px; border-radius: 7px; text-align: center; }}
  .stat-box.apparel {{ background: #fef3c7; border: 1px solid #fde68a; }}
  .stat-box.other {{ background: #eff6ff; border: 1px solid #bfdbfe; }}
  .stat-box .slabel {{ font-size: 11px; color: #666; margin-bottom: 4px; }}
  .stat-box .multi-stats {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 4px; margin-top: 4px; }}
  .stat-box .ms-label {{ font-size: 9px; color: #888; display: block; margin-bottom: 1px; font-weight: 400; }}
  .stat-box .ms-value {{ font-weight: 700; font-size: 12px; }}
  .stat-box.apparel .ms-value {{ color: #78350f; }}
  .stat-box.other .ms-value {{ color: #1e3a8a; }}
  .chart-container {{ position: relative; height: 240px; }}
  .chart-container.tall {{ height: 320px; }}
  .table-wrap {{ overflow-x: auto; }}
  .roi-table {{ width: 100%; border-collapse: collapse; font-size: 11.5px; white-space: nowrap; }}
  .roi-table th, .roi-table td {{ padding: 7px 10px; text-align: center; border-bottom: 1px solid #f1f3f5; color: #111; }}
  .roi-table th {{ background: #fafafa; color: #555; font-weight: 600; font-size: 10.5px; text-transform: uppercase; letter-spacing: 0.03em; }}
  .roi-table tr.campaign {{ cursor: pointer; }}
  .roi-table tr.campaign:hover td {{ background: #fafbfc; }}
  .roi-table tr.campaign td:first-child {{ text-align: left; font-weight: 500; padding-left: 14px; }}
  .caret {{ display: inline-block; width: 0; height: 0; border-left: 4px solid #888; border-top: 4px solid transparent; border-bottom: 4px solid transparent; margin-right: 6px; transition: transform 0.15s; }}
  .roi-table tr.campaign.open .caret {{ transform: rotate(90deg); }}
  .roi-table tr.adset {{ background: #f8fafc; font-size: 11px; display: none; }}
  .roi-table tr.adset.show {{ display: table-row; }}
  .roi-table tr.adset td {{ color: #475569; padding: 5px 10px; border-bottom: 1px solid #eef1f4; }}
  .roi-table tr.adset td:first-child {{ text-align: left; padding-left: 34px; font-weight: 400; color: #64748b; }}
  .roi-table tr.subtotal {{ font-weight: 700; background: #eff6ff; }} .roi-table tr.subtotal td {{ color: #1e3a8a; border-top: 1px solid #bfdbfe; border-bottom: 1px solid #bfdbfe; font-size: 11.5px; }}
  .roi-table tr.subtotal.apparel {{ background: #fef3c7; }}
  .roi-table tr.subtotal.apparel td {{ color: #78350f; border-top: 1px solid #fde68a; }}
  .roi-table tr.subtotal.other {{ background: #eff6ff; }}
  .roi-table tr.subtotal.other td {{ color: #1e3a8a; border-top: 1px solid #bfdbfe; }}
  .roi-table tr.subtotal td:first-child {{ text-align: left; padding-left: 14px; font-style: italic; }}
  .roi-table tr.total {{ font-weight: 800; background: #fef3c7; }}
  .roi-table tr.total td {{ color: #78350f; border-top: 2px solid #f59e0b; padding: 9px 10px; font-size: 12px; }}
  .roi-table tr.total td:first-child {{ text-align: left; padding-left: 14px; }}
  /* tx table */
  .tx-table {{ width: 100%; border-collapse: collapse; font-size: 12.5px; margin-top: 8px; }}
  .tx-table th {{ background: #faf5ee; color: #6b6258; font-weight: 600; font-size: 11px; text-transform: uppercase; padding: 8px 12px; text-align: left; letter-spacing: 0.04em; }}
  .tx-table td {{ padding: 7px 12px; border-bottom: 1px solid #f0ebe0; }}
</style>
</head>
<body>
<div class="mobile-header">
  <div class="mh-title">Mood Shop 廣告報表</div>
  <button class="hamburger" id="hamburgerBtn" aria-label="選單"><span></span><span></span><span></span></button>
</div>
<div class="sidebar-overlay" id="sidebarOverlay"></div>
<div class="app">
  <aside class="sidebar">
    <div class="brand"><h1>Mood Shop 廣告報表</h1><p>{year} 年</p></div>
    <nav class="sb-nav">
      <div class="sb-label">內容</div>
      <a class="sb-tab active" data-section="overview">成效總覽</a>
      <a class="sb-tab" data-section="roi">每月成效</a>
      <a class="sb-tab" data-section="fee">廣告代操費</a>
      <a class="sb-tab" data-section="card">信用卡代刷</a>
      <a class="sb-tab" data-section="total">請款合計</a>
    </nav>
    <div class="sb-footer">資料最後更新<div class="updated-time">{last_updated}</div><div style="margin-top:8px; font-size:10.5px;">每天台灣時間 9:00 自動更新</div></div>
  </aside>

  <main class="main">
    <!-- 總覽 -->
    <section id="sec-overview" class="tab-content active">
      <div class="page-head"><h1 class="page-title">成效總覽</h1><p class="page-subtitle">{year} 年累計｜點月份卡片進入該月詳細報表</p></div>
      <div class="ytd-banner">
        <div class="ytd-title">{year} 年累計（{ytd_month_count} 個月）</div>
        <div class="ytd-primary">
          <div><div class="yp-label">總花費</div><div class="yp-value spend">${ytd_cost:,}</div></div>
          <div><div class="yp-label">總轉換值</div><div class="yp-value revenue">${ytd_value:,}</div></div>
          <div><div class="yp-label">整體 ROAS</div><div class="yp-value roas">{ytd_roas:.2f}x</div></div>
        </div>
        <div class="ytd-secondary">
          <span>購買 <b>{ytd_purch:,} 筆</b></span><span class="sep">|</span>
          <span>每次購買成本 <b>${ytd_cpp_rounded:,}</b></span><span class="sep">|</span>
          <span>活動總數 <b>{ytd_count} 檔</b></span>
        </div>
      </div>
      <div class="trend-card">
        <div class="trend-title">月度趨勢</div>
        <div class="trend-canvas-wrap"><canvas id="trendChart"></canvas></div>
      </div>
      <div class="months-grid">{month_cards_html}</div>
    </section>

    <!-- 廣告成效 -->
    <section id="sec-roi" class="tab-content">
      <div class="page-head"><h1 class="page-title">每月成效</h1><p class="page-subtitle">歸因窗 7 天｜Omni 購買欄位</p></div>
      <div class="month-picker" id="mp-roi"></div>
      <div id="roi-content"></div>
    </section>

    <!-- 廣告代操費 -->
    <section id="sec-fee" class="tab-content">
      <div class="page-head"><h1 class="page-title">廣告代操費</h1><p class="page-subtitle">按月廣告總費用級距計費</p></div>
      <div class="month-picker" id="mp-fee"></div>
      <div id="fee-content"></div>
    </section>

    <!-- 信用卡代刷 -->
    <section id="sec-card" class="tab-content">
      <div class="page-head"><h1 class="page-title">信用卡代刷</h1><p class="page-subtitle">僅統計「已付款」狀態｜排除客戶卡（末 4 碼 6609）</p></div>
      <div class="month-picker" id="mp-card"></div>
      <div id="card-content"></div>
    </section>

    <!-- 請款合計 -->
    <section id="sec-total" class="tab-content">
      <div class="page-head"><h1 class="page-title">請款合計</h1><p class="page-subtitle">代刷費 + 代操費（含稅）</p></div>
      <div class="month-picker" id="mp-total"></div>
      <div id="total-content"></div>
    </section>
  </main>
</div>

<script>
const APP = {js_data};
let state = {{ section: 'overview', month: APP.currentMonth }};

// Hamburger toggle for mobile
const hamburgerBtn = document.getElementById('hamburgerBtn');
const sidebar = document.querySelector('.sidebar');
const overlay = document.getElementById('sidebarOverlay');
function toggleSidebar(force) {{
  const open = force !== undefined ? force : !sidebar.classList.contains('open');
  sidebar.classList.toggle('open', open);
  overlay.classList.toggle('show', open);
}}
if (hamburgerBtn) hamburgerBtn.addEventListener('click', () => toggleSidebar());
if (overlay) overlay.addEventListener('click', () => toggleSidebar(false));

const fmt = n => n == null ? '—' : '$' + Math.round(n).toLocaleString();
const fmtNum = n => n == null ? '—' : Math.round(n).toLocaleString();
const fmtRoas = n => n == null || !isFinite(n) ? '—' : n.toFixed(2) + 'x';

// ===== Section nav =====
document.querySelectorAll('.sb-tab').forEach(tab => {{
  tab.addEventListener('click', () => {{
    state.section = tab.dataset.section;
    toggleSidebar(false);  // close drawer on mobile
    render();
  }});
}});

function render() {{
  document.querySelectorAll('.sb-tab').forEach(t => t.classList.toggle('active', t.dataset.section === state.section));
  document.querySelectorAll('.tab-content').forEach(s => s.classList.toggle('active', s.id === 'sec-' + state.section));

  // Render month picker for non-overview sections
  if (state.section !== 'overview') {{
    const mp = document.getElementById('mp-' + state.section);
    mp.innerHTML = APP.availableMonths.map(m => {{
      const cls = m === state.month ? 'month-tab active' : 'month-tab';
      const badge = m === APP.currentMonth ? ' <span class="m-badge">當月</span>' : '';
      return `<a class="${{cls}}" data-m="${{m}}">${{m}} 月${{badge}}</a>`;
    }}).join('');
    mp.querySelectorAll('.month-tab').forEach(el => {{
      el.addEventListener('click', () => {{
        state.month = parseInt(el.dataset.m);
        render();
      }});
    }});
  }}

  // Render section content
  if (state.section === 'roi') renderRoi();
  if (state.section === 'fee') renderFee();
  if (state.section === 'card') renderCard();
  if (state.section === 'total') renderTotal();

  window.scrollTo(0, 0);
}}

// Month card click → navigate to roi
document.querySelectorAll('.month-card').forEach(card => {{
  card.addEventListener('click', () => {{
    state.section = 'roi';
    state.month = parseInt(card.dataset.month);
    render();
  }});
}});

// ===== Trend chart (overview) =====
try {{
  new Chart(document.getElementById('trendChart'), {{
    data: {{
      labels: {chart_labels_json},
      datasets: [
        {{ type: 'bar', label: '花費 (TWD)', data: {chart_costs_json}, backgroundColor: '#1f6feb88', borderColor: '#1f6feb', borderWidth: 1, borderRadius: 4, yAxisID: 'y' }},
        {{ type: 'bar', label: '轉換值 (TWD)', data: {chart_values_json}, backgroundColor: '#16a34a88', borderColor: '#16a34a', borderWidth: 1, borderRadius: 4, yAxisID: 'y' }},
        {{ type: 'line', label: 'ROAS (x)', data: {chart_roas_json}, borderColor: '#d97706', backgroundColor: '#d97706', borderWidth: 2, pointRadius: 4, tension: 0.2, yAxisID: 'y1' }}
      ]
    }},
    options: {{
      maintainAspectRatio: false, responsive: true,
      plugins: {{ legend: {{ position: 'bottom', labels: {{ font: {{ size: 10 }}, boxWidth: 10 }} }},
        tooltip: {{ callbacks: {{ label: ctx => {{ const v = ctx.parsed.y; if (ctx.dataset.label.includes('ROAS')) return ctx.dataset.label + ': ' + v.toFixed(2) + 'x'; return ctx.dataset.label + ': $' + Math.round(v).toLocaleString(); }} }} }} }},
      scales: {{
        y: {{ position: 'left', ticks: {{ font: {{ size: 9 }}, callback: v => {{ if (v >= 1000000) return '$' + (v/1000000).toFixed(1) + 'M'; if (v >= 1000) return '$' + (v/1000) + 'k'; return '$' + v; }} }} }},
        y1: {{ position: 'right', grid: {{ drawOnChartArea: false }}, ticks: {{ font: {{ size: 9 }}, callback: v => v + 'x' }} }},
        x: {{ ticks: {{ font: {{ size: 11 }} }} }}
      }}
    }}
  }});
}} catch (e) {{ console.error('Trend chart failed:', e); }}

// ===== ROI render =====
let roiCharts = [];
function renderRoi() {{
  // Destroy existing charts
  roiCharts.forEach(c => c && c.destroy && c.destroy());
  roiCharts = [];

  const m = APP.months[state.month];
  if (!m) {{ document.getElementById('roi-content').innerHTML = '<p>無資料</p>'; return; }}
  const campaigns = m.campaigns;
  // KPIs
  const totalCost = campaigns.reduce((s,c)=>s+c.adsets.reduce((ss,a)=>ss+a.cost,0),0);
  const totalValue = campaigns.reduce((s,c)=>s+c.adsets.reduce((ss,a)=>ss+a.value,0),0);
  const totalPurch = campaigns.reduce((s,c)=>s+c.adsets.reduce((ss,a)=>ss+a.purchases,0),0);
  const totalRoas = totalCost > 0 ? totalValue/totalCost : 0;
  const totalCpp = totalPurch > 0 ? totalCost/totalPurch : 0;
  const apparelCount = campaigns.filter(c => c.category === 'apparel').length;
  const otherCount = campaigns.filter(c => c.category === 'other').length;

  document.getElementById('roi-content').innerHTML = `
    <div class="kpi-row five">
      <div class="kpi spend"><div class="kpi-label">總花費</div><div class="kpi-value">${{fmt(totalCost)}}</div></div>
      <div class="kpi revenue"><div class="kpi-label">總轉換值</div><div class="kpi-value">${{fmt(totalValue)}}</div></div>
      <div class="kpi roas"><div class="kpi-label">整體 ROAS</div><div class="kpi-value">${{totalRoas.toFixed(2)}}x</div></div>
      <div class="kpi purch"><div class="kpi-label">購買次數</div><div class="kpi-value">${{fmtNum(totalPurch)}}</div></div>
      <div class="kpi cpp"><div class="kpi-label">每次購買成本</div><div class="kpi-value">${{fmt(totalCpp)}}</div></div>
    </div>
    <div class="card"><h2>服飾 vs 異業 類別比較</h2>
      <div class="compare-wrap">
        <div class="compare-card">
          <div class="compare-stats">
            <div class="stat-box apparel"><div class="slabel">服飾（${{apparelCount}} 檔）</div><div class="multi-stats" id="appS">—</div></div>
            <div class="stat-box other"><div class="slabel">異業（${{otherCount}} 檔）</div><div class="multi-stats" id="othS">—</div></div>
          </div>
          <div class="chart-container"><canvas id="srChart"></canvas></div>
        </div>
        <div class="compare-card">
          <div class="compare-stats">
            <div class="stat-box apparel"><div class="slabel">服飾購買 / CPP</div><div class="multi-stats" id="appP">—</div></div>
            <div class="stat-box other"><div class="slabel">異業購買 / CPP</div><div class="multi-stats" id="othP">—</div></div>
          </div>
          <div class="chart-container"><canvas id="pcChart"></canvas></div>
        </div>
      </div>
    </div>
    <div class="card"><h2>受眾包累積排行 <span class="hint">（同名廣告組合跨直播累積）</span></h2>
      <div class="compare-wrap">
        <div class="compare-card"><div style="font-size:11px; color:#78350f; font-weight:700; margin-bottom:6px; text-align:center;">服飾類受眾包</div><div class="chart-container tall"><canvas id="appAdsetChart"></canvas></div></div>
        <div class="compare-card"><div style="font-size:11px; color:#1e3a8a; font-weight:700; margin-bottom:6px; text-align:center;">異業類受眾包</div><div class="chart-container tall"><canvas id="othAdsetChart"></canvas></div></div>
      </div>
    </div>
    <div class="card"><h2>活動明細表 <span class="hint">（點擊活動名稱展開廣告組合）</span></h2>
      <div class="table-wrap"><table class="roi-table">
        <thead><tr><th>活動名稱</th><th>預算</th><th>花費</th><th>轉換值</th><th>ROAS</th><th>購買次數</th><th>每次購買成本</th></tr></thead>
        <tbody id="roiTableBody"></tbody>
      </table></div>
    </div>
  `;

  // Compute campaign totals
  campaigns.forEach(c => {{
    c.cost = c.adsets.reduce((s,a)=>s+a.cost,0);
    c.value = c.adsets.reduce((s,a)=>s+a.value,0);
    c.purchases = c.adsets.reduce((s,a)=>s+a.purchases,0);
    c.roas = c.cost > 0 ? c.value/c.cost : null;
    c.cpp = c.purchases > 0 ? c.cost/c.purchases : null;
    c.adsets.forEach(a => {{ a.roas = a.cost > 0 ? a.value/a.cost : null; a.cpp = a.purchases > 0 ? a.cost/a.purchases : null; }});
  }});

  // Build table
  const tbody = document.getElementById('roiTableBody');
  const grouped = {{}};
  campaigns.forEach(c => {{ if (!grouped[c.group]) grouped[c.group] = []; grouped[c.group].push(c); }});
  let gB = 0, gC = 0, gV = 0, gP = 0;

  function getMonth(c) {{ const m = c.name.match(/^(\\d+)\\/(\\d+)/); return m ? parseInt(m[1]) : 0; }}

  Object.keys(grouped).sort((a,b)=>a-b).forEach(gKey => {{
    const list = grouped[gKey];
    const groupHasMixed = list.some(c => c.category === 'apparel') && list.some(c => c.category === 'other');
    let buf = []; let curCat = null;
    function flush() {{
      if (buf.length === 0) return;
      const sB = buf.reduce((s,c)=>s+c.budget,0), sC = buf.reduce((s,c)=>s+c.cost,0);
      const sV = buf.reduce((s,c)=>s+c.value,0), sP = buf.reduce((s,c)=>s+c.purchases,0);
      const sR = sC > 0 ? sV/sC : null, sCpp = sP > 0 ? sC/sP : null;
      let label;
      if (groupHasMixed) {{
        const days = buf.map(c=>c.day).filter(d=>d>0);
        const month = getMonth(buf[0]);
        const minD = Math.min(...days), maxD = Math.max(...days);
        const dr = minD === maxD ? `${{month}}/${{minD}}` : `${{month}}/${{minD}}–${{month}}/${{maxD}}`;
        label = `${{dr}} ${{curCat === 'apparel' ? '服飾' : '異業'}}小計`;
      }} else label = list[0].groupLabel;
      const tr = document.createElement('tr');
      tr.className = 'subtotal' + (groupHasMixed ? ' ' + curCat : '');
      tr.innerHTML = `<td>${{label}}</td><td>${{fmt(sB)}}</td><td>${{fmt(sC)}}</td><td>${{fmt(sV)}}</td><td>${{fmtRoas(sR)}}</td><td>${{fmtNum(sP)}}</td><td>${{fmt(sCpp)}}</td>`;
      tbody.appendChild(tr);
      gB += sB; gC += sC; gV += sV; gP += sP;
      buf = [];
    }}
    list.forEach(c => {{
      if (curCat !== null && c.category !== curCat) flush();
      curCat = c.category;
      const tr = document.createElement('tr'); tr.className = 'campaign';
      tr.innerHTML = `<td><span class="caret"></span>${{c.name}}</td><td>${{fmt(c.budget)}}</td><td>${{fmt(c.cost)}}</td><td>${{fmt(c.value)}}</td><td>${{fmtRoas(c.roas)}}</td><td>${{fmtNum(c.purchases)}}</td><td>${{fmt(c.cpp)}}</td>`;
      tbody.appendChild(tr);
      c.adsets.forEach(a => {{
        const trA = document.createElement('tr'); trA.className = 'adset';
        trA.innerHTML = `<td>└ ${{a.name}}</td><td>—</td><td>${{fmt(a.cost)}}</td><td>${{a.value === 0 ? '—' : fmt(a.value)}}</td><td>${{fmtRoas(a.roas)}}</td><td>${{a.purchases === 0 ? '—' : fmtNum(a.purchases)}}</td><td>${{fmt(a.cpp)}}</td>`;
        tbody.appendChild(trA);
      }});
      tr.addEventListener('click', () => {{
        const isOpen = tr.classList.toggle('open');
        let next = tr.nextElementSibling;
        while (next && next.classList.contains('adset')) {{ next.classList.toggle('show', isOpen); next = next.nextElementSibling; }}
      }});
      buf.push(c);
    }});
    flush();
  }});
  const grandRoas = gC > 0 ? gV/gC : null, grandCpp = gP > 0 ? gC/gP : null;
  const trT = document.createElement('tr'); trT.className = 'total';
  trT.innerHTML = `<td>總計（${{campaigns.length}} 檔）</td><td>${{fmt(gB)}}</td><td>${{fmt(gC)}}</td><td>${{fmt(gV)}}</td><td>${{fmtRoas(grandRoas)}}</td><td>${{fmtNum(gP)}}</td><td>${{fmt(grandCpp)}}</td>`;
  tbody.appendChild(trT);

  // Charts
  try {{
    const apparel = aggCat(campaigns, 'apparel'), other = aggCat(campaigns, 'other');
    const aRoas = apparel.cost > 0 ? apparel.value/apparel.cost : 0;
    const oRoas = other.cost > 0 ? other.value/other.cost : 0;
    document.getElementById('appS').innerHTML =
      `<div class="ms-item"><span class="ms-label">花費</span><span class="ms-value">${{fmt(apparel.cost)}}</span></div>` +
      `<div class="ms-item"><span class="ms-label">轉換值</span><span class="ms-value">${{fmt(apparel.value)}}</span></div>` +
      `<div class="ms-item"><span class="ms-label">ROAS</span><span class="ms-value">${{aRoas.toFixed(2)}}x</span></div>`;
    document.getElementById('othS').innerHTML =
      `<div class="ms-item"><span class="ms-label">花費</span><span class="ms-value">${{fmt(other.cost)}}</span></div>` +
      `<div class="ms-item"><span class="ms-label">轉換值</span><span class="ms-value">${{fmt(other.value)}}</span></div>` +
      `<div class="ms-item"><span class="ms-label">ROAS</span><span class="ms-value">${{oRoas.toFixed(2)}}x</span></div>`;
    document.getElementById('appP').innerHTML =
      `<div class="ms-item"><span class="ms-label">購買</span><span class="ms-value">${{apparel.purchases}} 筆</span></div>` +
      `<div class="ms-item"><span class="ms-label">CPP</span><span class="ms-value">${{fmt(apparel.cpp)}}</span></div>` +
      `<div class="ms-item"><span class="ms-label">—</span><span class="ms-value">—</span></div>`;
    document.getElementById('othP').innerHTML =
      `<div class="ms-item"><span class="ms-label">購買</span><span class="ms-value">${{other.purchases}} 筆</span></div>` +
      `<div class="ms-item"><span class="ms-label">CPP</span><span class="ms-value">${{fmt(other.cpp)}}</span></div>` +
      `<div class="ms-item"><span class="ms-label">—</span><span class="ms-value">—</span></div>`;
    roiCharts.push(new Chart(document.getElementById('srChart'), {{
      type: 'bar', data: {{ labels: ['花費','轉換值'], datasets: [
        {{ label: `服飾（${{apparel.count}} 檔）`, data: [apparel.cost, apparel.value], backgroundColor: '#d97706', borderRadius: 4 }},
        {{ label: `異業（${{other.count}} 檔）`, data: [other.cost, other.value], backgroundColor: '#1e3a8a', borderRadius: 4 }}
      ]}},
      options: {{ maintainAspectRatio: false, plugins: {{ legend: {{ position: 'bottom', labels: {{ font: {{ size: 10 }} }} }} }}, scales: {{ y: {{ ticks: {{ callback: v => v >= 1000000 ? '$' + (v/1000000).toFixed(1)+'M' : v >= 1000 ? '$'+(v/1000)+'k' : v }} }} }} }}
    }}));
    roiCharts.push(new Chart(document.getElementById('pcChart'), {{
      type: 'bar', data: {{ labels: ['購買次數','CPP'], datasets: [
        {{ label: '服飾', data: [apparel.purchases, apparel.cpp], backgroundColor: '#d97706', borderRadius: 4 }},
        {{ label: '異業', data: [other.purchases, other.cpp], backgroundColor: '#1e3a8a', borderRadius: 4 }}
      ]}},
      options: {{ maintainAspectRatio: false, plugins: {{ legend: {{ position: 'bottom', labels: {{ font: {{ size: 10 }} }} }} }} }}
    }}));
    const apA = rollup(campaigns, 'apparel'), otA = rollup(campaigns, 'other');
    if (apA.length > 0) roiCharts.push(adsetChart('appAdsetChart', apA, '#d97706'));
    if (otA.length > 0) roiCharts.push(adsetChart('othAdsetChart', otA, '#1e3a8a'));
  }} catch (e) {{ console.error('ROI chart err:', e); }}
}}

function aggCat(camps, cat) {{
  const list = camps.filter(c => c.category === cat);
  const cost = list.reduce((s,c)=>s+c.cost,0);
  const value = list.reduce((s,c)=>s+c.value,0);
  const purchases = list.reduce((s,c)=>s+c.purchases,0);
  return {{ count: list.length, cost, value, purchases, cpp: purchases > 0 ? cost/purchases : 0 }};
}}
function rollup(camps, cat) {{
  const map = {{}};
  camps.filter(c => c.category === cat).forEach(c => c.adsets.forEach(a => {{
    if (!map[a.name]) map[a.name] = {{ name: a.name, cost: 0, value: 0, purchases: 0, appearIn: 0 }};
    map[a.name].cost += a.cost; map[a.name].value += a.value; map[a.name].purchases += a.purchases; map[a.name].appearIn += 1;
  }}));
  const arr = Object.values(map);
  arr.forEach(a => a.cpp = a.purchases > 0 ? a.cost/a.purchases : null);
  return arr.sort((a,b) => b.value - a.value);
}}
function adsetChart(id, data, color) {{
  return new Chart(document.getElementById(id), {{
    type: 'bar',
    data: {{ labels: data.map(a => `${{a.name}} (${{a.appearIn}} 場)`), datasets: [
      {{ label: '花費 (TWD)', data: data.map(a => a.cost), backgroundColor: color + '55', borderColor: color, borderWidth: 1, borderRadius: 3 }},
      {{ label: '轉換值 (TWD)', data: data.map(a => a.value), backgroundColor: color, borderRadius: 3 }}
    ]}},
    options: {{ indexAxis: 'y', maintainAspectRatio: false, plugins: {{ legend: {{ position: 'bottom', labels: {{ font: {{ size: 10 }} }} }} }} }}
  }});
}}

// ===== FEE render =====
function renderFee() {{
  const m = APP.months[state.month]; const b = m.billing;
  document.getElementById('fee-content').innerHTML = `
    <div class="kpi-row" style="grid-template-columns: 1.3fr 1fr 1fr 1.3fr;">
      <div class="kpi"><div class="kpi-label">單月廣告總費用</div><div class="kpi-value">${{fmt(b.ad_cost)}}</div></div>
      <div class="kpi"><div class="kpi-label">適用級距</div><div class="kpi-value" style="font-size:18px;">${{b.tier}}</div></div>
      <div class="kpi"><div class="kpi-label">服務費率</div><div class="kpi-value" style="color:#d97706;">${{Math.round(b.service_pct*100)}}%</div></div>
      <div class="kpi amount"><div class="kpi-label">服務費（含稅）</div><div class="kpi-value">${{fmt(b.fee_total)}}</div></div>
    </div>
    <div class="card"><h2>計算明細</h2>
      <div class="billing">
        <div class="label">單月廣告總費用</div><div class="value">${{fmt(b.ad_cost)}}</div>
        <div class="label">適用服務費率（${{b.tier}}）</div><div class="value">×${{Math.round(b.service_pct*100)}}%</div>
        <div class="sep"></div>
        <div class="label">服務費（未稅）</div><div class="value">${{fmt(b.fee_pretax)}}</div>
        <div class="label">營業稅 5%</div><div class="value add">+${{fmt(b.fee_tax)}}</div>
        <div class="sep"></div>
        <div class="label total">服務費（含稅）</div><div class="value total">${{fmt(b.fee_total)}}</div>
      </div>
    </div>
    <div class="info-banner"><b>級距規則：</b>0-10萬 → 20%；10-30萬 → 15%；30-60萬 → 13%；60萬以上 → 10%</div>
  `;
}}

// ===== CARD render =====
function renderCard() {{
  const m = APP.months[state.month]; const b = m.billing;
  const txRows = b.transactions.map(t => `<tr><td>${{t.date}}</td><td>****-****-****-${{t.card}}</td><td style="text-align:right;">${{fmt(t.amount)}}</td></tr>`).join('');
  document.getElementById('card-content').innerHTML = `
    <div class="kpi-row" style="grid-template-columns: 1fr 1fr 1fr 1.2fr;">
      <div class="kpi"><div class="kpi-label">代刷總金額</div><div class="kpi-value">${{fmt(b.card_total)}}</div></div>
      <div class="kpi"><div class="kpi-label">國外手續費 1.5%</div><div class="kpi-value" style="color:#dc2626;">+${{fmt(b.foreign_fee)}}</div></div>
      <div class="kpi"><div class="kpi-label">信用卡回饋 0.3%</div><div class="kpi-value" style="color:#16a34a;">-${{fmt(b.rebate)}}</div></div>
      <div class="kpi amount"><div class="kpi-label">實際應付</div><div class="kpi-value">${{fmt(b.card_actual)}}</div></div>
    </div>
    <div class="card"><h2>計算明細</h2>
      <div class="billing">
        <div class="label">代刷總金額（已付款）</div><div class="value">${{fmt(b.card_total)}}</div>
        <div class="label">國外交易手續費 1.5%</div><div class="value add">+${{fmt(b.foreign_fee)}}</div>
        <div class="label">信用卡回饋 0.3%</div><div class="value sub">-${{fmt(b.rebate)}}</div>
        <div class="sep"></div>
        <div class="label total">實際應付</div><div class="value total">${{fmt(b.card_actual)}}</div>
      </div>
    </div>
    <div class="card"><h2>${{state.month}} 月交易明細 <span class="hint">（${{b.transactions.length}} 筆）</span></h2>
      ${{b.transactions.length === 0 ? '<p style="color:#999; font-size:13px; margin:10px 0 0;">本月無資料（可能尚未從 FB API 抓到，或無符合的交易）。</p>' :
      `<table class="tx-table"><thead><tr><th>日期</th><th>付款方式</th><th style="text-align:right;">金額</th></tr></thead><tbody>${{txRows}}</tbody><tfoot><tr style="font-weight:800; background:#faf5ee;"><td colspan="2">合計</td><td style="text-align:right;">${{fmt(b.card_total)}}</td></tr></tfoot></table>`}}
    </div>
  `;
}}

// ===== TOTAL render =====
function renderTotal() {{
  const m = APP.months[state.month]; const b = m.billing;
  document.getElementById('total-content').innerHTML = `
    <div class="card" style="text-align:center; padding:42px; background:#fff;">
      <div style="font-size:12px; color:#8a8170; margin-bottom:10px; text-transform:uppercase; letter-spacing:0.06em; font-weight:600;">${{state.month}} 月應請款合計</div>
      <div style="font-size:54px; font-weight:800; color:#c2410c; letter-spacing:-0.02em; line-height:1;">${{fmt(b.grand_total)}}</div>
      <div style="font-size:12px; color:#8a8170; margin-top:10px;">新台幣 NTD</div>
    </div>
    <div class="card"><h2>請款明細</h2>
      <div class="billing">
        <div class="label" style="font-weight:600;">信用卡代刷（實際應付）</div><div class="value">${{fmt(b.card_actual)}}</div>
        <div class="formula" style="grid-column: 1 / -1;">代刷 ${{fmt(b.card_total)}} + 手續費 ${{fmt(b.foreign_fee)}} - 回饋 ${{fmt(b.rebate)}}</div>
        <div class="sep"></div>
        <div class="label" style="font-weight:600;">廣告代操服務費（含稅）</div><div class="value">${{fmt(b.fee_total)}}</div>
        <div class="formula" style="grid-column: 1 / -1;">廣告花費 ${{fmt(b.ad_cost)}} × ${{Math.round(b.service_pct*100)}}% = ${{fmt(b.fee_pretax)}}（未稅）+ 5% 稅 ${{fmt(b.fee_tax)}}</div>
        <div class="sep"></div>
        <div class="label total">本月應請款合計</div><div class="value total">${{fmt(b.grand_total)}}</div>
      </div>
    </div>
    <div class="info-banner"><b>備註：</b>木品時尚有限公司｜統編 90553951｜三聯發票</div>
  `;
}}

// Initial render
render();
</script>
</body>
</html>"""

def build_app(year, current_month, months_data, campaigns_by_month, available_months, last_updated=None):
    """Build single-page app with sidebar + 5 sections.
    Replaces the old per-month HTML files + index.html with a single index.html SPA.
    """
    from datetime import datetime, timedelta
    import json as _json

    if last_updated is None:
        last_updated = (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")

    # Build a normalized data structure for JS
    months_for_js = {}
    for mm in available_months:
        ym = f"{year}-{mm:02d}"
        d = months_data[ym]
        b = d.get("billing", {})
        months_for_js[str(mm)] = {
            "cost": d["cost"],
            "value": d["value"],
            "purchases": d["purchases"],
            "roas": round(d["roas"], 4),
            "cpp": round(d["cpp"], 2),
            "count": d["count"],
            "campaigns": campaigns_by_month.get(ym, {}).get("campaigns", []),
            "billing": {
                "card_total": b.get("card_total", 0),
                "foreign_fee": b.get("foreign_fee", 0),
                "rebate": b.get("rebate", 0),
                "card_actual": b.get("card_actual", 0),
                "ad_cost": b.get("ad_cost", d["cost"]),
                "tier": b.get("tier", ""),
                "service_pct": b.get("service_pct", 0),
                "fee_pretax": b.get("fee_pretax", 0),
                "fee_tax": b.get("fee_tax", 0),
                "fee_total": b.get("fee_total", 0),
                "grand_total": b.get("grand_total", 0),
                "transactions": b.get("card_transactions", []),
            },
        }

    # YTD totals
    ytd_cost = sum(d["cost"] for d in months_for_js.values())
    ytd_value = sum(d["value"] for d in months_for_js.values())
    ytd_purch = sum(d["purchases"] for d in months_for_js.values())
    ytd_count = sum(d["count"] for d in months_for_js.values())
    ytd_roas = ytd_value / ytd_cost if ytd_cost > 0 else 0
    ytd_cpp = ytd_cost / ytd_purch if ytd_purch > 0 else 0

    # Trend chart data
    chart_labels = [f"{m}月" for m in available_months]
    chart_costs = [months_for_js[str(m)]["cost"] for m in available_months]
    chart_values = [months_for_js[str(m)]["value"] for m in available_months]
    chart_roas = [months_for_js[str(m)]["roas"] for m in available_months]

    js_data = _json.dumps({
        "year": year,
        "currentMonth": current_month,
        "availableMonths": available_months,
        "months": months_for_js,
    }, ensure_ascii=False)

    chart_labels_json = _json.dumps(chart_labels, ensure_ascii=False)
    chart_costs_json = _json.dumps(chart_costs)
    chart_values_json = _json.dumps(chart_values)
    chart_roas_json = _json.dumps(chart_roas)

    # Build month cards (overview)
    month_cards_html = ""
    for mm in sorted(available_months, reverse=True):
        d = months_for_js[str(mm)]
        is_cur = mm == current_month
        badge = ' <span class="card-badge">當月</span>' if is_cur else ''
        cls = "current" if is_cur else ""
        month_cards_html += f'''
    <a class="month-card {cls}" data-month="{mm}">
      <div class="mc-head">
        <div class="mc-title">{year} 年 {mm} 月{badge}</div>
        <div class="mc-arrow">→</div>
      </div>
      <div class="mc-stats">
        <div><span class="mc-label">花費</span><span class="mc-val spend">${d["cost"]:,}</span></div>
        <div><span class="mc-label">轉換值</span><span class="mc-val rev">${d["value"]:,}</span></div>
        <div><span class="mc-label">ROAS</span><span class="mc-val roas">{d["roas"]:.2f}x</span></div>
        <div><span class="mc-label">購買</span><span class="mc-val purch">{d["purchases"]:,}</span></div>
        <div><span class="mc-label">CPP</span><span class="mc-val cpp">${round(d["cpp"]):,}</span></div>
        <div><span class="mc-label">活動數</span><span class="mc-val">{d["count"]}</span></div>
      </div>
    </a>'''

    return APP_TEMPLATE.format(
        year=year,
        current_month=current_month,
        last_updated=last_updated,
        ytd_cost=ytd_cost,
        ytd_value=ytd_value,
        ytd_purch=ytd_purch,
        ytd_count=ytd_count,
        ytd_roas=ytd_roas,
        ytd_cpp_rounded=round(ytd_cpp),
        ytd_month_count=len(available_months),
        month_cards_html=month_cards_html,
        chart_labels_json=chart_labels_json,
        chart_costs_json=chart_costs_json,
        chart_values_json=chart_values_json,
        chart_roas_json=chart_roas_json,
        js_data=js_data,
    )
