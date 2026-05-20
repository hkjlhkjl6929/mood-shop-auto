"""
Mood Shop 廣告成效自動化建置腳本
透過 Facebook Marketing API 抓取資料，生成所有月份的 HTML 報表。
v2: 改用 Python 端過濾，避開 FB API STARTS_WITH 限制。
v3: CSV-based billing + retry + sidebar layout.
"""
import sys
print("[BOOT] build.py started, Python", sys.version.split()[0], flush=True)
import os
import re
import json
import time
import shutil
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

# 過濾規則（兩種，二擇一即可）：
# A) MY_CARD_LAST4：白名單，只列出自己的卡（多張用逗號分隔）
# B) EXCLUDE_CARD_LAST4：黑名單，只列出要排除的卡（如客戶的卡）
# 推薦用 B（黑名單），自己新辦卡時不用每次更新
MY_CARD_LAST4 = [s.strip() for s in os.environ.get("MY_CARD_LAST4", "").split(",") if s.strip()]
EXCLUDE_CARD_LAST4 = [s.strip() for s in os.environ.get("EXCLUDE_CARD_LAST4", "").split(",") if s.strip()]

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


def fb_request(url, params=None, what="", max_retries=4):
    """Wrapper with retry for transient errors (rate limit, etc.)"""
    delay = 5
    for attempt in range(max_retries):
        try:
            r = requests.get(url, params=params, timeout=60)
            if r.ok:
                return r.json()
            # Try parse error
            try:
                err = r.json()
            except Exception:
                err = {"raw": r.text}
            err_obj = err.get("error", {}) if isinstance(err, dict) else {}
            is_transient = (
                err_obj.get("is_transient") or
                err_obj.get("code") in (4, 17, 32, 613, 80004) or
                r.status_code in (429, 500, 502, 503, 504)
            )
            if is_transient and attempt < max_retries - 1:
                print(f"  [RETRY {attempt+1}/{max_retries}] {what}: transient error (code={err_obj.get('code')}), wait {delay}s...")
                time.sleep(delay)
                delay *= 2  # exponential backoff
                continue
            print(f"[FB API ERROR on {what}]")
            print(f"  Status: {r.status_code}")
            print(f"  Body: {json.dumps(err, ensure_ascii=False, indent=2)}")
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                print(f"  [RETRY {attempt+1}/{max_retries}] {what}: connection error, wait {delay}s...")
                time.sleep(delay)
                delay *= 2
                continue
            print(f"[Request failed on {what}]: {e}")
            raise


def fetch_all_campaigns(year):
    """抓取整個帳號所有 campaign（一次拿，後面在 Python 過濾）"""
    url = f"{BASE}/{FB_ACCOUNT_ID}/campaigns"
