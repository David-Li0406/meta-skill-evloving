# 輸入參數定義 (Input Schema)

## 必要參數

### etf_ticker

| 屬性 | 值 |
|------|---|
| 類型 | string |
| 必要 | 是 |
| 說明 | 實物型 ETF/信託代碼 |
| 範例 | "SLV", "PSLV", "GLD", "PHYS" |

**支援的 ETF**：

| 代碼 | 名稱 | 商品 | 官網 |
|------|------|------|------|
| SLV | iShares Silver Trust | 白銀 | ishares.com |
| PSLV | Sprott Physical Silver Trust | 白銀 | sprott.com |
| GLD | SPDR Gold Shares | 黃金 | spdrgoldshares.com |
| PHYS | Sprott Physical Gold Trust | 黃金 | sprott.com |
| IAU | iShares Gold Trust | 黃金 | ishares.com |
| SIVR | Aberdeen Standard Physical Silver | 白銀 | abrdn.com |

### commodity_price_symbol

| 屬性 | 值 |
|------|---|
| 類型 | string |
| 必要 | 是 |
| 說明 | 商品現貨或近月期貨價格代碼 |
| 範例 | "XAGUSD=X", "XAUUSD=X", "SI=F", "GC=F" |

**建議配對**：

| ETF | 建議價格代碼 | 說明 |
|-----|-------------|------|
| SLV, PSLV, SIVR | XAGUSD=X | 白銀現貨 |
| SLV, PSLV, SIVR | SI=F | 白銀期貨近月 |
| GLD, PHYS, IAU | XAUUSD=X | 黃金現貨 |
| GLD, PHYS, IAU | GC=F | 黃金期貨近月 |

## 可選參數

### start_date

| 屬性 | 值 |
|------|---|
| 類型 | string (ISO date) |
| 必要 | 否 |
| 預設 | 10 年前 |
| 格式 | "YYYY-MM-DD" |
| 範例 | "2010-01-01" |
| 說明 | 分析起始日期 |

### end_date

| 屬性 | 值 |
|------|---|
| 類型 | string (ISO date) |
| 必要 | 否 |
| 預設 | 今天 |
| 格式 | "YYYY-MM-DD" |
| 範例 | "2026-01-16" |
| 說明 | 分析結束日期 |

### inventory_field

| 屬性 | 值 |
|------|---|
| 類型 | string |
| 必要 | 否 |
| 預設 | "auto" |
| 可選值 | "auto", "silver_held_tonnes", "oz_held", "shares_outstanding" |
| 說明 | 庫存欄位名稱，auto 會自動偵測 |

**欄位說明**：

| 值 | 說明 |
|---|------|
| auto | 自動偵測，優先使用實物持倉量 |
| silver_held_tonnes | 白銀持倉量（噸） |
| oz_held | 持倉量（盎司） |
| shares_outstanding | 流通股數（可換算為持倉量） |

### decade_low_window_days

| 屬性 | 值 |
|------|---|
| 類型 | int |
| 必要 | 否 |
| 預設 | 3650 |
| 範圍 | 365 - 7300 |
| 說明 | 計算歷史低點的滾動視窗天數 |

**建議值**：
- 3650（10 年）：標準設定
- 1825（5 年）：較短期視角
- 5475（15 年）：更長期視角

### divergence_window_days

| 屬性 | 值 |
|------|---|
| 類型 | int |
| 必要 | 否 |
| 預設 | 180 |
| 範圍 | 30 - 365 |
| 說明 | 計算背離的視窗天數 |

**建議值**：
- 30：短期監控
- 90：季度視角
- 180：半年視角（推薦）
- 365：年度視角

### min_price_return_pct

| 屬性 | 值 |
|------|---|
| 類型 | float |
| 必要 | 否 |
| 預設 | 0.15 |
| 範圍 | 0.05 - 0.50 |
| 說明 | 視窗內價格上漲至少多少才算「上漲期」 |

**建議值**：
- 0.10（10%）：較敏感
- 0.15（15%）：標準
- 0.20（20%）：較保守

### min_inventory_drawdown_pct

| 屬性 | 值 |
|------|---|
| 類型 | float |
| 必要 | 否 |
| 預設 | 0.10 |
| 範圍 | 0.05 - 0.30 |
| 說明 | 視窗內庫存下滑至少多少才算「庫存被抽走」 |

**建議值**：
- 0.05（5%）：較敏感
- 0.10（10%）：標準
- 0.15（15%）：較保守

### confirm_signals

| 屬性 | 值 |
|------|---|
| 類型 | array[string] |
| 必要 | 否 |
| 預設 | [] |
| 說明 | 交叉驗證訊號清單 |

**可用訊號**：

| 訊號 | 說明 | 數據來源 |
|------|------|----------|
| comex_inventory | COMEX 庫存變化 | CME Group |
| lbma_vault | LBMA 金庫存量 | LBMA |
| lease_rates | 借貸利率 | 需要付費數據 |
| futures_backwardation | 期貨曲線結構 | Yahoo Finance |
| retail_premiums | 零售溢價 | 零售商網站 |

### output_format

| 屬性 | 值 |
|------|---|
| 類型 | string |
| 必要 | 否 |
| 預設 | "json" |
| 可選值 | "json", "markdown", "csv" |
| 說明 | 輸出格式 |

### output_file

| 屬性 | 值 |
|------|---|
| 類型 | string |
| 必要 | 否 |
| 預設 | stdout |
| 說明 | 輸出檔案路徑 |

## 完整範例

### 最簡配置

```json
{
  "etf_ticker": "SLV",
  "commodity_price_symbol": "XAGUSD=X"
}
```

### 完整配置

```json
{
  "etf_ticker": "SLV",
  "commodity_price_symbol": "XAGUSD=X",
  "start_date": "2010-01-01",
  "end_date": "2026-01-16",
  "inventory_field": "auto",
  "decade_low_window_days": 3650,
  "divergence_window_days": 180,
  "min_price_return_pct": 0.15,
  "min_inventory_drawdown_pct": 0.10,
  "confirm_signals": [
    "comex_inventory",
    "futures_backwardation",
    "retail_premiums"
  ],
  "output_format": "json",
  "output_file": "result.json"
}
```

### 命令列範例

**快速檢查**：
```bash
python scripts/divergence_detector.py \
  --etf SLV \
  --commodity XAGUSD=X \
  --quick
```

**完整分析**：
```bash
python scripts/divergence_detector.py \
  --etf SLV \
  --commodity XAGUSD=X \
  --start 2010-01-01 \
  --end 2026-01-16 \
  --divergence-window 180 \
  --price-threshold 0.15 \
  --inventory-threshold 0.10 \
  --output result.json
```

**多 ETF 監控**：
```bash
python scripts/divergence_detector.py \
  --etf SLV,PSLV,GLD \
  --commodity XAGUSD=X,XAGUSD=X,XAUUSD=X \
  --quick \
  --output monitor_report.json
```

## 參數驗證

腳本會自動驗證參數：

1. **etf_ticker**：必須是支援的代碼
2. **commodity_price_symbol**：必須是有效的 Yahoo Finance 代碼
3. **日期範圍**：start_date 必須早於 end_date
4. **百分比門檻**：必須在 0-1 之間
5. **視窗天數**：必須為正整數

無效參數會回傳錯誤訊息並列出可用選項。
