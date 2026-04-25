"""HTML template for Mood Shop monthly dashboard. Built from a known-good rendering."""

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<meta name="robots" content="noindex,nofollow,noarchive">
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
