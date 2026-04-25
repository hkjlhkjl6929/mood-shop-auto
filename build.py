"""
Mood Shop 廣告成效自動化建置腳本
透過 Facebook Marketing API 抓取資料，生成所有月份的 HTML 報表。
v2: 改用 Python 端過濾，避開 FB API STARTS_WITH 限制。
"""
import os
import re
import json
import time
import requests
from datetime import datetime, timedelta
from collections import defaultdict
from calendar import monthrange

# ===== 從環境變數讀取機密 =====
FB_TOKEN = os.environ["FB_ACCESS_TOKEN"]
FB_ACCOUNT_ID = os.environ.get("FB_ACCOUNT_ID", "act_3518918538334496")
# 自動修正：如果忘了加 act_ 前綴，自動補上
if not FB_ACCOUNT_ID.startswith("act_"):
    FB_ACCOUNT_ID = "act_" + FB_ACCOUNT_ID

API_VERSION = "v21.0"
BASE = f"https://graph.facebook.com/{API_VERSION}"

TODAY = datetime.utcnow() + timedelta(hours=8)
CURRENT_YEAR = TODAY.year
CURRENT_MONTH = TODAY.month
MONTHS = list(range(1, CURRENT_MONTH + 1))

OUT_DIR = "site"
os.makedirs(OUT_DIR, exist_ok=True)


def parse_budget(name):
    m = re.search(r'\$([0-9,]+)', name)
    return int(m.group(1).replace(',', '')) if m else 0


def parse_day(name):
    m = re.match(r'(\d+)/(\d+)', name)
    return int(m.group(2)) if m else 0


def classify(name):
    after_date = re.sub(r'^\d+/\d+\s*', '', name)
    return "apparel" if "服飾" in after_date else "other"


def fb_request(url, params=None, what=""):
    """Wrapper that prints real FB error messages."""
    try:
        r = requests.get(url, params=params, timeout=60)
        if not r.ok:
            try:
                err = r.json()
            except Exception:
                err = {"raw": r.text}
            print(f"[FB API ERROR on {what}]")
            print(f"  Status: {r.status_code}")
            print(f"  Body: {json.dumps(err, ensure_ascii=False, indent=2)}")
            r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        print(f"[Request failed on {what}]: {e}")
        raise


def fetch_all_campaigns(year):
    """抓取整個帳號所有 campaign（一次拿，後面在 Python 過濾）"""
    url = f"{BASE}/{FB_ACCOUNT_ID}/campaigns"
    params = {
        "access_token": FB_TOKEN,
        "fields": "id,name,created_time",
        "limit": 200,
    }
    all_camps = []
    while url:
        data = fb_request(url, params, "list campaigns")
        all_camps.extend(data.get("data", []))
        next_url = data.get("paging", {}).get("next")
        url, params = next_url, None
    print(f"  Total campaigns in account: {len(all_camps)}")
    return all_camps


def fetch_insights(month, year, end_date):
    """抓 insights，不用 API filter，後面 Python 過濾"""
    since = f"{year}-{month:02d}-01"
    until = end_date.strftime("%Y-%m-%d")
    url = f"{BASE}/{FB_ACCOUNT_ID}/insights"
    params = {
        "access_token": FB_TOKEN,
        "level": "adset",
        "fields": "campaign_name,adset_name,spend,actions,action_values",
        "time_range": json.dumps({"since": since, "until": until}),
        "action_attribution_windows": json.dumps(["7d_click", "1d_view"]),
        "limit": 500,
    }
    rows = []
    while url:
        data = fb_request(url, params, f"insights {since}..{until}")
        rows.extend(data.get("data", []))
        next_url = data.get("paging", {}).get("next")
        url, params = next_url, None
    return rows


def extract_omni(actions, key="omni_purchase"):
    if not actions:
        return 0
    for a in actions:
        if a.get("action_type") == key:
            return float(a.get("value", 0) or 0)
    return 0


def merge_key(name):
    """為合併互動/轉換用的 key：拿掉「互動」「轉換」字樣 + 拿掉預算"""
    cleaned = re.sub(r'\s*(?:互動|轉換)\s*', ' ', name)
    cleaned = re.sub(r'\s*\$[\d,]+\s*$', '', cleaned)
    return re.sub(r'\s+', ' ', cleaned).strip()


def aggregate_to_campaigns(rows, month_prefix):
    """把 adset rows 聚合，並過濾出指定月份開頭的活動。
    同一天同場次（互動 vs 轉換差異）合併為一檔。"""
    # Step 1: aggregate by raw campaign name first
    by_campaign = defaultdict(list)
    for row in rows:
        c_name = row.get("campaign_name", "")
        if not c_name.startswith(month_prefix):
            continue
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

    # Step 2: build raw campaign list
    raw_campaigns = []
    for c_name, adsets in by_campaign.items():
        raw_campaigns.append({
            "name": c_name,
            "budget": parse_budget(c_name),
            "day": parse_day(c_name),
            "category": classify(c_name),
            "adsets": adsets,
        })

    # Step 3: merge by key (date + session, ignore 互動/轉換)
    merged = {}
    for c in raw_campaigns:
        key = merge_key(c["name"])
        if key not in merged:
            merged[key] = {
                "name": key,
                "budget": 0,
                "day": c["day"],
                "category": c["category"],
                "adsets": [],
                "_source_names": [],
            }
        merged[key]["budget"] += c["budget"]
        merged[key]["_source_names"].append(c["name"])
        # apparel takes precedence
        if c["category"] == "apparel":
            merged[key]["category"] = "apparel"
        # merge adsets by adset name
        for a in c["adsets"]:
            existing = next((x for x in merged[key]["adsets"] if x["name"] == a["name"]), None)
            if existing:
                existing["cost"] += a["cost"]
                existing["value"] += a["value"]
                existing["purchases"] += a["purchases"]
            else:
                merged[key]["adsets"].append(dict(a))

    # Step 4: finalize names with combined budget at the end
    campaigns = []
    for key, c in merged.items():
        if len(c["_source_names"]) > 1:
            c["name"] = f'{key} ${c["budget"]:,}'
        else:
            # single source: keep original name
            c["name"] = c["_source_names"][0]
        del c["_source_names"]
        campaigns.append(c)

    campaigns.sort(key=lambda c: (c["day"], c["name"]))
    return campaigns


def assign_groups(campaigns, month_prefix):
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
            label = f"{month_prefix}{g[0]} 小計"
        else:
            label = f"{month_prefix}{g[0]}–{month_prefix}{g[-1]} 小計"
        for d in g:
            day_to_group[d] = (i + 1, label)
    for c in campaigns:
        gnum, glabel = day_to_group.get(c["day"], (1, ""))
        c["group"] = gnum
        c["groupLabel"] = glabel
    return campaigns


def build_dashboard(title, campaigns, date_range_note, year_month):
    campaigns_json = json.dumps(campaigns, ensure_ascii=False)
    total_cost = sum(sum(a["cost"] for a in c["adsets"]) for c in campaigns)
    total_value = sum(sum(a["value"] for a in c["adsets"]) for c in campaigns)
    total_purchases = sum(sum(a["purchases"] for a in c["adsets"]) for c in campaigns)
    total_roas = total_value / total_cost if total_cost > 0 else 0
    total_cpp = total_cost / total_purchases if total_purchases > 0 else 0
    apparel_count = sum(1 for c in campaigns if c["category"] == "apparel")
    other_count = sum(1 for c in campaigns if c["category"] == "other")
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


from template import TEMPLATE, build_index


def main():
    print(f"=== Mood Shop Auto-Build {TODAY.strftime('%Y-%m-%d %H:%M')} ===")
    print(f"FB_ACCOUNT_ID: {FB_ACCOUNT_ID}")
    print(f"Months to build: {MONTHS}\n")

    # 一次抓所有 campaigns，找出每月最後一場直播日
    all_campaigns = fetch_all_campaigns(CURRENT_YEAR)
    last_day_per_month = {}
    for c in all_campaigns:
        n = c.get("name", "")
        m_match = re.match(r'(\d+)/(\d+)', n)
        if not m_match:
            continue
        mm, dd = int(m_match.group(1)), int(m_match.group(2))
        if mm in MONTHS and dd > last_day_per_month.get(mm, 0):
            last_day_per_month[mm] = dd

    totals_by_month = {}

    for month in MONTHS:
        print(f"\n--- {CURRENT_YEAR}/{month:02d} ---")
        last_day = last_day_per_month.get(month, 0)
        if last_day == 0:
            print(f"  No campaigns starting with '{month}/', skip")
            continue

        month_end_day = monthrange(CURRENT_YEAR, month)[1]
        attribution_end_day = min(last_day + 7, month_end_day)
        end_date = datetime(CURRENT_YEAR, month, attribution_end_day)
        if end_date > TODAY:
            end_date = TODAY

        print(f"  Last live: {month}/{last_day}, attribution end: {end_date.strftime('%Y-%m-%d')}")

        rows = fetch_insights(month, CURRENT_YEAR, end_date)
        print(f"  Got {len(rows)} adset rows (whole account)")

        month_prefix = f"{month}/"
        campaigns = aggregate_to_campaigns(rows, month_prefix)
        campaigns = assign_groups(campaigns, month_prefix)
        print(f"  Filtered to {len(campaigns)} campaigns starting with '{month_prefix}'")

        if not campaigns:
            print(f"  No campaigns to build for {month}, skip")
            continue

        title = f"Mood Shop {month}月廣告成效"
        note = f"歸因窗 7 天（{CURRENT_YEAR}-{month:02d}-01 ~ {end_date.strftime('%Y-%m-%d')}）。"
        if last_day + 7 > month_end_day and month == CURRENT_MONTH:
            note += f" {month}/{last_day} 場次的歸因窗尚未結束，數據仍在累積。"

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
        time.sleep(2)

    if not totals_by_month:
        print("\nERROR: No data built for any month. Check FB token and account.")
        raise SystemExit(1)

    index_html = build_index(totals_by_month, MONTHS, CURRENT_YEAR, CURRENT_MONTH)
    with open(f"{OUT_DIR}/index.html", "w", encoding="utf-8") as f:
        f.write(index_html)

    # Privacy: prevent search engine indexing
    with open(f"{OUT_DIR}/robots.txt", "w", encoding="utf-8") as f:
        f.write("User-agent: *\nDisallow: /\n")
    with open(f"{OUT_DIR}/_headers", "w", encoding="utf-8") as f:
        f.write("/*\n  X-Robots-Tag: noindex, nofollow, noarchive\n")
    print("[OK] robots.txt + _headers written (noindex protection)")
    print(f"\n[OK] index.html with {len(totals_by_month)} months")
    print("\nFiles in site/:")
    for f in sorted(os.listdir(OUT_DIR)):
        print(f"  {f}")


if __name__ == "__main__":
    main()
