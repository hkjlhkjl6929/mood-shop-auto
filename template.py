"""HTML template for Mood Shop monthly dashboard. Built from a known-good rendering."""

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<meta name="robots" content="noindex,nofollow,noarchive">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" type="image/png" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAIUElEQVR42u2a349dVRXHP2uf3/dOpx2GdminWBp+VSoIUsEgBDDaIKBiQAJqDL744pMvPvNf8K6JGhOjlpigEOChIiSg0FKBllIov/pjZjqduT/OPT/28mHfO3Nv587cYSb6IOckN5O5d9199v7stb5rrX2PnH/yEeXzeKlFohqGz/lVAagAVAAqABWACkAFoAJQAagAVAAqABWACkAFoAJQAagAVAA2e8nan4mMsOk379l/1vus//JHmyhYBbNOVrYcMnEBLd04at1nftAdXlcu2lr3UnX39wN3f2u797Du/b4pYgSMN3zMjQNQN2gUou0WMgqCCCQJFIV7GQNl6caJa0gYQxRBnmFnzoIIEsVuQSIOTl5AHEOUIGGMoJSz5yBtI0nd2SR1xA9A1WEQIM/Q5iIiAmG0DGtzISCotSQPPUHywONolg53SWPQTpvwtnupPf5zB00E8hySGrJrD9TqYAxiPLyrbyD57o/xdu1BW01nX5YgBpneA1u2gee7iJmaJrn/MYKbbkfTZndfLFoWqC0Ra8EPMTt24d96J7J9J9psrBE6g5f3y3tueHL19RskS9HGAvVvP0Z57hPKTz9AwmiFm1lV4v0HCCa2k778PGJL5PKdeFfvw546Do1FSFvo4jzl6ZOgUPv+T9G0RXn6BFIbw7vpq9gzH8OF85C2obmI/eQ0dvYstfsexdsxTf7OG4gq5Nnyq91E52fQtEV01/2YbZOUp95BgnBN7xY/GOEBaiFOKI4fpX34GWoPPI6MjTv37idsDOL50ElRVed+cUJ4xzcp3zkKWQq+73Y1CJH6GPmxV0mf+T1jDz2B+cI1BLfdg16YRWfOQBA6+yBA6mPYmbM0fvcU4S1fJ7rzPrTTHc8Y9/J9CCN0dob0L78hOnAX0Z0H0XZrpHaNVjZrkTgmffFptN0iOfgDN4EeAGshrrmdQFw4pC3CA3e7HZ87B1G8LGiqUJaY8QnyY6+SvfUvxn/yC7ztOylP/hup1ZcFsGsrtTo6d5b0xUMkdz+ATO5w4dWbQxe6JAm0m7Sf/SPJvQ9hrtgNWWfNcBgNwBgYn4CsQ/PQrwlvvB3/i7c4uiJut4yH5JlbvLUQhgTX3Uj56Ydu160OF1gxpK+/hDe2FebnoMiHT9a63/GyN18Dawn33YzmQxZWlkicUHxwHNtqEN18B5pnmwCgLv1JfRyJYsr33yZ9+TnqD/7Q7VSeQ30LpK1Bj0jqeFsm0LXoq4tBe+ZjysX5gaw2dB6e5/Tj/Bm8HdOrm4uBrIPOz+BN7XYbsEZaNOspAyjLbijUSF84hGYZ8Te+h/U9ZzCMsudhtmzt5v3V4WqnhW03MePb3OTXSLFaFmhjHvF9ZFSqV3W3lc1Wgspy0WEMkmc0D/2K6Ct3Eey/FZ07D543GDJpC20sEOy+en3Vni3xdl4JcbJm/naLNpTzsw7sat7iB8jWSYqZM1CUm9QA6ausuupefnCC1gt/RmfPu5S0xKq7q3lO9vbrBNfdiIxPrMwafQs39XEQgzexHX/PtU5gjTdEBxTCEI1j8hNHXYq71LWNh3ZS/N17MePb6Lzxj6WCaVO9gJTFQIxLnJD9/Vnsx++7qqv/BmoxUUznlefRLCW++0Fsc9G5dz8EETRt4++/ldaLT5MeeZnawUecTZEPpi9j0HYTf+8+ik9PU55+F8J48L7GQN4B4xF/62HSl/6K/eg9V3luTgMUrW8ZVGhVJAxXCkyvhu+GweJvnyK4/iaiex5EmwtOK3o2nRRv7z40bVEceYX0b3+gbDdIHv0Zai2atl1fYS1kHWTictixk+zwM4gXgC2Wx+rakNSJv/Mj8hNvkj73J1c6jyiJV68ERdCsg3/NfpKDD5OfeBM66XChEkGLgvDLX8O7/Ao6rx1GfB+9OEf+9usEXzqA2XUVNu32E0GITGwHz8Me77pzWZAdeQVvatppS9ZxRVUQwvhWZOtl2HePuTkkdfd+ECBB4PqGqWn8q66nfO8t8n8eRpLaiKbIZSFZ6xkhVYu5bAoztoVy9jw0Lq5ZWcnkFBKE2Jkzbrc9zzUpRYGZmobaGHRaaJq6haSt5a6w2wVq2sJMTiHbJtG84zwh60Cr6e4t4gqrfu/rdorauLhUC4xshrrPCMnIh6SKArWFE5Nh4jRgm6Pd/L4ULr2/ebaU+ly73C1jVwiZceFWFMtNlYiD2bNVe0nd0P3H89ffDncBjD4PCAKEYH2DBqFLuwOiqEufrUitw8a0FowPkT84Rr/tkqBqX6LXz3QOsP4DkfUMKjI4yX61Vx2Sh3Xwe0unRfT1DP15WAZT8sD3NveUn7/hb/bU3lqn1v3ummWogPSOwLRcFk9rnasag2Yd10WKLKt6b5xeOJTF4CKNQfNiOcxsuVQD/O8AKMi1tyDdhkaNgeZFaDWQsXEkGUPL0glcGHdPejpuGcZD1GLfPYp35XXYcx8ikzuRrZOupb04BwsXMNt3UX50ErN3H2CQMsfmGaIWCUK0yMFabHMBievoqWODOvHfBWDRtImmDfAjJIrRhTlEFdtJMaVC4KNlDo0FN7HeDgeRA+Z56OIFJ5xpE4lqaKuBtBtoGLlus8igsYjaAorcHXf5AZql6MK86zeiBHvh3MaPcDf8qGxZdA877VK31g3S7jngJfrQ60zUunDwfDdGL531XN10x+mNWRYrdERVEc8bDH/P+8ybuL4ssKrvBKuIpSyno1Hi2qvnRcCLBjVS+mxGHYjrxsVw4wBWjTVd/1yGpctLEsVGUlv1y1AFoAJQAagAVAAqABWACkAFoAJQAagAVAAqABWAtS5/1Z+Z/98vtaAWX6La5xSAIlGN/wAyfgVHY7WOmAAAAABJRU5ErkJggg==">
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
