# Mood Shop 廣告成效自動化部署

## 這個 repo 做什麼？
每天台灣時間早上 9 點，自動：
1. 從 Facebook Marketing API 抓取 Mood Shop.連線（act_3518918538334496）的廣告資料
2. 用 7 天歸因窗 + Omni 購買欄位生成當年所有月份的 HTML 報表
3. 透過 Netlify API 部署到你的 Netlify site

## 設定步驟

### 1. 把所有檔案放進新建的 GitHub repo

```
mood-shop-auto/
├── build.py
├── deploy.py
├── template.py
├── requirements.txt
├── README.md
└── .github/workflows/daily.yml
```

### 2. 在 Settings → Secrets and variables → Actions 加入 4 個 Secrets

| Secret 名稱 | 內容 |
|---|---|
| `FB_ACCESS_TOKEN` | Facebook Marketing API long-lived token |
| `FB_ACCOUNT_ID` | `act_3518918538334496` |
| `NETLIFY_TOKEN` | Netlify Personal Access Token |
| `NETLIFY_SITE_ID` | 從 Netlify Site Settings → General 找 Site ID |

### 3. 手動觸發測試

到 Actions 分頁 → 點 "Daily Mood Shop Dashboard Update" → "Run workflow" 按鈕 → 等 2 分鐘看結果

### 4. 確認排程已啟用

排程是 `cron: '0 1 * * *'`（UTC 1:00 = 台灣時間 9:00）。確認後就會每天自動跑。

## 故障排查

**Q: workflow 紅燈、build.py 失敗？**
A: 通常是 FB token 過期。重新產生 long-lived token 後更新 secret 即可。

**Q: 改了排程時間？**
A: 編輯 `.github/workflows/daily.yml` 的 `cron` 行：
- 每天台灣早上 9:00 → `0 1 * * *`
- 每週一台灣 9:00 → `0 1 * * 1`
- 每天台灣 9:00 + 21:00 → `0 1,13 * * *`

**Q: 想要本地測試？**
```bash
export FB_ACCESS_TOKEN=...
export FB_ACCOUNT_ID=act_3518918538334496
export NETLIFY_TOKEN=...
export NETLIFY_SITE_ID=...
pip install -r requirements.txt
python build.py
python deploy.py
```
