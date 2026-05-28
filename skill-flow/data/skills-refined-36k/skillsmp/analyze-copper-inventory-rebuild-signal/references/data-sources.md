<overview>
此參考文件列出銅庫存回補訊號分析所需的資料來源，包括 SHFE/COMEX 庫存的 MacroMicro 爬蟲說明與銅價來源。

**資料來源（三類數據）**：
- **SHFE 銅庫存**：MacroMicro Highcharts 圖表
- **COMEX 銅庫存**：MacroMicro Highcharts 圖表
- **銅期貨價格**：Yahoo Finance HG=F

**推薦方法**：Chrome CDP（繞過 Cloudflare）
</overview>

<shfe_inventory>

**SHFE 銅庫存數據**

| 屬性 | 值 |
|------|-----|
| 名稱 | SHFE Copper Warehouse Stock |
| URL | https://en.macromicro.me/series/8743/copper-shfe-warehouse-stock |
| 頻率 | 週（每週五公布） |
| 單位 | 噸 (tonnes) |
| 歷史 | 2003 年起 |
| 更新延遲 | ~1 週 |

**欄位說明**：

| 欄位 | 說明 |
|------|------|
| date | 數據日期 |
| inventory_tonnes | SHFE 可交割銅庫存量（噸） |

**抓取方法**：Chrome CDP（推薦）

詳見 [Chrome CDP 數據爬取 SOP](../../../thoughts/shared/guide/chrome-cdp-scraping-sop.md)

</shfe_inventory>

<comex_inventory>

**COMEX 銅庫存數據**

| 屬性 | 值 |
|------|-----|
| 名稱 | COMEX Copper Warehouse Stock |
| URL | https://www.macromicro.me/series/8742/copper-comex-warehouse-stock |
| 頻率 | 日（可轉週） |
| 單位 | 噸 (tonnes) |
| 歷史 | 1990 年代起 |
| 更新延遲 | ~1-2 天 |

**欄位說明**：

| 欄位 | 說明 |
|------|------|
| date | 數據日期 |
| inventory_tonnes | COMEX 可交割銅庫存量（噸） |

**抓取方法**：Chrome CDP（推薦）

與 SHFE 使用相同的抓取流程，由 `fetch_copper_data.py` 統一處理。

</comex_inventory>

<copper_price>

**銅期貨價格數據**

| 屬性 | 值 |
|------|-----|
| 名稱 | COMEX Copper Futures (HG=F) |
| 來源 | Yahoo Finance |
| 頻率 | 日（可轉週） |
| 單位 | USD/lb |
| 歷史 | 2000 年起 |

**抓取方法**：yfinance Python 套件

```python
import yfinance as yf

data = yf.download("HG=F", start="2015-01-01", end="2026-01-26")
```

**注意事項**：
- HG=F 為連續近月合約
- 存在換倉日的價格跳躍
- 建議使用週收盤價減少噪音

</copper_price>

<cdp_method>

**Chrome CDP 方法（推薦）**

透過 Chrome DevTools Protocol 連接到已開啟的 Chrome 瀏覽器，完全繞過 Cloudflare 和反爬蟲偵測。

**原理**：
```
┌─────────────────┐     WebSocket      ┌─────────────────┐
│  Python Script  │ ◄────────────────► │  Chrome Browser │
│  (CDP Client)   │    Port 9222       │  (你的 Profile) │
└─────────────────┘                    └─────────────────┘
        │                                      │
        │ Runtime.evaluate()                   │
        ▼                                      ▼
   執行 JavaScript ──────────────────► 提取 Highcharts 數據
```

**自動化流程**：

本技能的 `fetch_shfe_inventory.py` 腳本實現全自動流程：

1. 檢查是否已有 Chrome 調試實例
2. 若無，自動啟動 Chrome（帶調試端口）
3. 等待頁面載入（~40 秒）
4. 透過 CDP 執行 JavaScript 提取 Highcharts 數據
5. 關閉 Chrome（若是本次啟動的）

**使用方式**：
```bash
cd scripts
python fetch_shfe_inventory.py
```

**強制更新**：
```bash
python fetch_shfe_inventory.py --force-refresh
```

</cdp_method>

<cache_strategy>

**快取策略**

| 參數 | 值 | 說明 |
|------|-----|------|
| 快取目錄 | `./cache` | 預設 |
| 最大有效期 | 12 小時 | 庫存為週數據 |
| SHFE 快取 | `shfe_inventory.csv` | SHFE 庫存數據 |
| COMEX 快取 | `comex_inventory.csv` | COMEX 庫存數據 |
| 價格快取 | `copper_price.csv` | 銅期貨價格 |

**使用快取**：
```bash
python scripts/fetch_copper_data.py  # 自動使用快取
```

**強制更新**：
```bash
python scripts/fetch_copper_data.py --force-refresh
```

**只更新特定數據**：
```bash
python scripts/fetch_copper_data.py --source shfe      # 只抓 SHFE
python scripts/fetch_copper_data.py --source comex     # 只抓 COMEX
python scripts/fetch_copper_data.py --source price     # 只抓價格
```

</cache_strategy>

<update_schedule>

**資料更新時程**

| 資料 | 來源 | 更新頻率 | 延遲 | 建議抓取時機 |
|------|------|---------|------|-------------|
| SHFE 庫存 | MacroMicro | 週 | ~7 天 | 每週一 |
| COMEX 庫存 | MacroMicro | 日 | ~1-2 天 | 每日 |
| 銅期貨價格 | Yahoo Finance | 日 | ~1 天 | 每日 |

**監控建議**：
- 每週一檢查 SHFE 庫存更新
- COMEX 庫存每日可更新
- 設定快取有效期為 12 小時
- 重大經濟事件後可手動更新

</update_schedule>

<fallback_sources>

**備用數據源**

若 MacroMicro 無法存取：

1. **上海期貨交易所官網**
   - http://www.shfe.com.cn/
   - 需手動查詢日報/週報

2. **其他庫存來源**
   | 來源 | 庫存類型 | 取得難度 |
   |------|----------|----------|
   | CME Group | COMEX 倉庫庫存 | 需爬蟲 |
   | LME | LME 倉庫庫存 | 需訂閱 |
   | 中國海關 | 進出口數據 | 月度滯後 |

</fallback_sources>

<troubleshooting>

**常見問題排解**

**Q1: WebSocket 連線被拒絕 (403 Forbidden)**

確認啟動 Chrome 時有加上 `--remote-allow-origins=*` 參數。

**Q2: 無法連接到 Chrome 調試端口**

1. 確保所有 Chrome 視窗都已關閉
2. 確認使用了非預設的 `--user-data-dir`
3. 檢查端口 9222 是否被佔用：`curl -s http://127.0.0.1:9222/json`

**Q3: Highcharts not found**

1. 確認頁面已完全載入（圖表已顯示）
2. 在瀏覽器 Console 中執行 `typeof Highcharts` 確認
3. 可能需要登入 MacroMicro 帳號

**Q4: 被 Cloudflare 擋住**

1. 使用 CDP 方法而非 Selenium
2. 在 Chrome 中手動完成 Cloudflare 驗證
3. 登入 MacroMicro 帳號後再執行

**Q5: yfinance 無法取得數據**

1. 確認網路連線正常
2. 嘗試更新 yfinance：`pip install --upgrade yfinance`
3. 檢查 ticker symbol 是否正確（HG=F）

</troubleshooting>

<related_guides>

**相關指南**

- [Chrome CDP 數據爬取 SOP](../../../thoughts/shared/guide/chrome-cdp-scraping-sop.md)
- [MacroMicro Highcharts 爬蟲指南](../../../thoughts/shared/guide/macromicro-highcharts-crawler.md)

</related_guides>
