"""
透過 Netlify API 部署 site/ 資料夾到指定 site
文件：https://docs.netlify.com/api/get-started/#deploy-a-zip-file
"""
import os
import zipfile
import requests

NETLIFY_TOKEN = os.environ["NETLIFY_TOKEN"]
SITE_ID = os.environ["NETLIFY_SITE_ID"]

ZIP_PATH = "site.zip"
SITE_DIR = "site"

# 1) 把 site/ 打包成 zip
with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as z:
    for root, _, files in os.walk(SITE_DIR):
        for f in files:
            full = os.path.join(root, f)
            rel = os.path.relpath(full, SITE_DIR)
            z.write(full, rel)
            print(f"  zipped {rel}")

# 2) POST 到 Netlify
url = f"https://api.netlify.com/api/v1/sites/{SITE_ID}/deploys"
headers = {
    "Authorization": f"Bearer {NETLIFY_TOKEN}",
    "Content-Type": "application/zip",
}
with open(ZIP_PATH, "rb") as f:
    data = f.read()

print(f"\nUploading {len(data):,} bytes to Netlify site {SITE_ID}...")
r = requests.post(url, headers=headers, data=data, timeout=120)
r.raise_for_status()
result = r.json()

print(f"\n[OK] Deploy created: {result.get('id')}")
print(f"State: {result.get('state')}")
print(f"URL: {result.get('ssl_url') or result.get('url')}")
