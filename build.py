"""
Mood Shop 廣告成效自動化建置腳本
每天透過 Facebook Marketing API 抓取資料，生成所有月份的 HTML 報表。
"""
import os
import re
import json
import time
import requests
from datetime import datetime, timedelta
from collections import defaultdict

# ===== 從環境變數讀取機密 =====
FB_TOKEN = os.environ["FB_ACCESS_TOKEN"]
FB_ACCOUNT_ID = os.environ.get("FB_ACCOUNT_ID", "act_3518918538334496")
API_VERSION = "v21.0"
BASE = f"https://graph.facebook.com/{API_VERSION}"

# 哪幾個月要建立報表（依當下日期動態決定：當年的 1 月到當月）
TODAY = datetime.utcnow() + timedelta(hours=8)  # 台灣時區
CURRENT_YEAR = TODAY.year
CURRENT_MONTH = TODAY.month
MONTHS = list(range(1, CURRENT_MONTH + 1))  # [1, 2, ..., 當月]

OUT_DIR = "site"
os.makedirs(OUT_DIR, exist_ok=True)


# ===== 工具函式 =====
def parse_budget(name):
    """從活動名稱尾端 $X,XXX 解析預算"""
    m = re.search(r'\$([0-9,]+)', name)
    return int(m.group(1).replace(',', '')) if m else 0


def parse_day(name):
    """從活動名稱開頭 M/D 解析日"""
    m = re.match(r'(\d+)/(\d+)', name)
    return int(m.group(2)) if m else 0


def classify(name):
    """日期後若含「服飾」→ apparel，其餘 → other"""
    after_date = re.sub(r'^\d+/\d+\s*', '', name)
    return "apparel" if "服飾" in after_date else "other"


def get_last_live_day(month, year):
    """找出該月最後一場直播的日期（campaign create_time 的最後一筆）"""
    url = f"{BASE}/{FB_ACCOUNT_ID}/campaigns"
    params = {
        "access_token": FB_TOKEN,
        "fields": "name,created_time",
        "filtering": json.dumps([{
            "field": "name",
            "operator": "STARTS_WITH",
            "value": f"{month}/"
        }]),
        "limit": 200,
    }
    last_day = 0
    while True:
        r = requests.get(url, params=params)
        r.raise_for_status()
        data = r.json()
        for c in data.get("data", []):
            d = parse_day(c["name"])
            if d > last_day:
                last_day = d
        next_url = data.get("paging", {}).get("next")
        if not next_url:
            break
        url, params = next_url, {}
    return last_day


def fetch_adset_insights(month, year, end_date):
    """抓取該月所有「M/」開頭活動的 adset 層級資料"""
    since = f"{year}-{month:02d}-01"
    until = end_date.strftime("%Y-%m-%d")
    url = f"{BASE}/{FB_ACCOUNT_ID}/insights"
    params = {
        "access_token": FB_TOKEN,
        "level": "adset",
        "fields": "campaign_name,adset_name,spend,actions,action_values",
        "time_range": json.dumps({"since": since, "until": until}),
        "filtering": json.dumps([{
            "field": "campaign.name",
            "operator": "STARTS_WITH",
            "value": f"{month}/"
        }]),
        "action_attribution_windows": json.dumps(["7d_click", "1d_view"]),
        "limit": 500,
    }
    rows = []
    while True:
        r = requests.get(url, params=params)
        r.raise_for_status()
        data = r.json()
        rows.extend(data.get("data", []))
        next_url = data.get("paging", {}).get("next")
        if not next_url:
            break
        url, params = next_url, {}
    return rows


def extract_omni(actions, key="omni_purchase"):
    """從 actions / action_values 陣列中找出 omni_purchase 的數字"""
    if not actions:
        return 0
    for a in actions:
        if a.get("action_type") == key:
            return float(a.get("value", 0) or 0)
    return 0


def aggregate_to_campaigns(rows):
    """把 adset rows 聚合成 campaign 結構"""
    by_campaign = defaultdict(list)
    for row in rows:
        c_name = row.get("campaign_name", "")
        a_name = row.get("adset_name", "")
        cost = float(row.get("spend", 0) or 0)
        purchases = int(extract_omni(row.get("actions", [])))
        value = extract_omni(row.get("action_values", []))
        by_campaign[c_name].append({
            "name": a_name,
            "cost": round(cost),
            "value": round(value),
            "purchases": purchases,
        })

    campaigns = []
    for c_name, adsets in by_campaign.items():
        campaigns.append({
            "name": c_name,
            "budget": parse_budget(c_name),
            "day": parse_day(c_name),
            "category": classify(c_name),
            "adsets": adsets,
        })
    # 依日期排序
    campaigns.sort(key=lambda c: (c["day"], c["name"]))
    return campaigns


def assign_groups(campaigns):
    """依連續日期分小計群組"""
    if not campaigns:
        return campaigns
    days = sorted(set(c["day"] for c in campaigns if c["day"]))
    groups = []
    cur = [days[0]]
    for d in days[1:]:
        if d == cur[-1] + 1:
            cur.append(d)
        else:
            groups.append(cur)
            cur = [d]
    groups.append(cur)
    day_to_group = {}
    for i, g in enumerate(groups):
        if len(g) == 1:
            label = f"{campaigns[0]['name'][0]}/{g[0]} 小計"  # use month from first campaign
        else:
            month_prefix = campaigns[0]['name'].split('/')[0]
            label = f"{month_prefix}/{g[0]}–{month_prefix}/{g[-1]} 小計"
        for d in g:
            day_to_group[d] = (i + 1, label)
    for c in campaigns:
        gnum, glabel = day_to_group.get(c["day"], (1, ""))
        c["group"] = gnum
        c["groupLabel"] = glabel
    return campaigns


def build_dashboard(title, campaigns, date_range_note, year_month):
    """生成單月 HTML 報表"""
    campaigns_json = json.dumps(campaigns, ensure_ascii=False)
    total_cost = sum(sum(a["cost"] for a in c["adsets"]) for c in campaigns)
    total_value = sum(sum(a["value"] for a in c["adsets"]) for c in campaigns)
    total_purchases = sum(sum(a["purchases"] for a in c["adsets"]) for c in campaigns)
    total_roas = total_value / total_cost if total_cost > 0 else 0
    total_cpp = total_cost / total_purchases if total_purchases > 0 else 0
    apparel_count = sum(1 for c in campaigns if c["category"] == "apparel")
    other_count = sum(1 for c in campaigns if c["category"] == "other")

    # 動態建立月份導覽列
    month_links = "".join(
        f'<a href="2026-{m:02d}.html">{m}月</a>\n  ' for m in MONTHS
    )

    return TEMPLATE.format(
        title=title, campaigns_json=campaigns_json,
        total_cost=total_cost, total_value=total_value,
        total_roas=total_roas, total_purchases=total_purchases,
        total_cpp=round(total_cpp), apparel_count=apparel_count,
        other_count=other_count, date_range_note=date_range_note,
        month_links=month_links,
    )


# ===== TEMPLATE 從 template.py 載入（同層級檔案，避免 build.py 太長）=====
from template import TEMPLATE, build_index


def main():
    print(f"=== Mood Shop Auto-Build {TODAY.strftime('%Y-%m-%d %H:%M')} ===")
    totals_by_month = {}

    for month in MONTHS:
        print(f"\n--- {CURRENT_YEAR}/{month:02d} ---")
        # 找最後一場直播日 + 7 天歸因窗
        last_day = get_last_live_day(month, CURRENT_YEAR)
        if last_day == 0:
            print(f"  No campaigns for month {month}, skip")
            continue

        # 結算日 = min(月底, 最後直播日 +7, 今天)
        from calendar import monthrange
        month_end_day = monthrange(CURRENT_YEAR, month)[1]
        attribution_end_day = min(last_day + 7, month_end_day)
        end_date = datetime(CURRENT_YEAR, month, attribution_end_day)
        if end_date > TODAY:
            end_date = TODAY

        print(f"  Last live: {month}/{last_day}, attribution end: {end_date.strftime('%Y-%m-%d')}")

        rows = fetch_adset_insights(month, CURRENT_YEAR, end_date)
        print(f"  Got {len(rows)} adset rows")

        campaigns = aggregate_to_campaigns(rows)
        campaigns = assign_groups(campaigns)
        print(f"  Aggregated to {len(campaigns)} campaigns")

        title = f"Mood Shop {month}月廣告成效"
        note = f"歸因窗 7 天（{CURRENT_YEAR}-{month:02d}-01 ~ {end_date.strftime('%Y-%m-%d')}）。"
        if last_day + 7 > month_end_day and month == CURRENT_MONTH:
            note += f" {month}/{last_day} 場次的歸因窗尚未結束（需至 {month}/{last_day + 7}），數據仍在累積。"

        ym = f"{CURRENT_YEAR}-{month:02d}"
        html = build_dashboard(title, campaigns, note, ym)
        with open(f"{OUT_DIR}/{ym}.html", "w", encoding="utf-8") as f:
            f.write(html)

        cost = sum(sum(a["cost"] for a in c["adsets"]) for c in campaigns)
        value = sum(sum(a["value"] for a in c["adsets"]) for c in campaigns)
        purchases = sum(sum(a["purchases"] for a in c["adsets"]) for c in campaigns)
        totals_by_month[ym] = {
            "cost": cost, "value": value, "purchases": purchases,
            "roas": value / cost if cost > 0 else 0,
            "cpp": cost / purchases if purchases > 0 else 0,
            "count": len(campaigns),
        }
        print(f"  [OK] {ym}.html (cost={cost:,}, value={value:,}, ROAS={value/cost if cost>0 else 0:.2f}x)")

        # 避免被 FB API rate limit
        time.sleep(2)

    # 生成總覽頁
    index_html = build_index(totals_by_month, MONTHS, CURRENT_YEAR, CURRENT_MONTH)
    with open(f"{OUT_DIR}/index.html", "w", encoding="utf-8") as f:
        f.write(index_html)
    print(f"\n[OK] index.html with {len(MONTHS)} months")
    print("\nFiles in site/:")
    for f in sorted(os.listdir(OUT_DIR)):
        print(f"  {f}")


if __name__ == "__main__":
    main()
