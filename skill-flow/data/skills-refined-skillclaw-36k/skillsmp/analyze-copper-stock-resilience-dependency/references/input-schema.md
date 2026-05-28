# 輸入參數定義

## 完整參數表

### 核心參數

| 參數 | 類型 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `start_date` | string | ✅ | - | 分析起始日期（YYYY-MM-DD） |
| `end_date` | string | ✅ | - | 分析結束日期（YYYY-MM-DD） |
| `freq` | string | ❌ | `1mo` | 資料頻率（1mo = 月） |
| `copper_series` | string | ✅ | - | 銅價序列代碼（如 HG=F） |
| `equity_proxy_series` | string | ✅ | - | 股市代理序列（如 ACWI） |
| `china_10y_yield_series` | string | ✅ | - | 中國10Y殖利率來源 |

### 模型參數

| 參數 | 類型 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `ma_window` | int | ❌ | `60` | 移動平均視窗（期數） |
| `rolling_window` | int | ❌ | `24` | 滾動迴歸視窗（月數） |
| `round_levels` | list[float] | ❌ | `[10000, 13000]` | 關卡位置（USD/ton） |
| `backfill_max_drawdown` | float | ❌ | `0.25` | 回補幅度上限（25%） |
| `level_threshold` | float | ❌ | `0.05` | 關卡判定容忍範圍（5%） |

### 股市韌性權重

| 參數 | 類型 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `resilience_weight_momentum` | float | ❌ | `0.4` | 12m 動能權重 |
| `resilience_weight_sma` | float | ❌ | `0.4` | 均線位置權重 |
| `resilience_weight_drawdown` | float | ❌ | `0.2` | 近期回撤權重 |
| `resilience_sma_period` | int | ❌ | `12` | 韌性用均線期數 |
| `resilience_drawdown_period` | int | ❌ | `3` | 回撤計算期數 |

### 輸出參數

| 參數 | 類型 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `output` | string | ❌ | `stdout` | 輸出檔案路徑 |
| `format` | string | ❌ | `json` | 輸出格式（json / markdown） |
| `verbose` | bool | ❌ | `false` | 是否輸出詳細日誌 |

---

## 參數詳細說明

### start_date / end_date

分析的時間範圍。

```python
# 範例
start_date = "2020-01-01"
end_date = "2026-01-20"
```

**建議**：至少包含 5 年歷史，確保有足夠樣本計算回補機率。

### freq

資料頻率，對應 yfinance 的 interval 參數。

| 值 | 說明 |
|----|------|
| `1mo` | 月頻（預設，對應圖中 monthly candle） |
| `1wk` | 週頻 |
| `1d` | 日頻 |

**注意**：頻率越高，計算量越大且雜訊越多。

### copper_series

銅價序列代碼。

| 代碼 | 來源 | 單位 | 說明 |
|------|------|------|------|
| `HG=F` | Yahoo Finance | USD/lb | COMEX Copper futures |
| `custom` | 自定義 | 視情況 | 需提供 CSV 路徑 |

**重要**：若使用 HG=F，腳本會自動轉換為 USD/ton。

### equity_proxy_series

全球股市韌性代理序列。

| 代碼 | 名稱 | 涵蓋範圍 |
|------|------|----------|
| `ACWI` | iShares MSCI ACWI ETF | 全球（預設推薦） |
| `VT` | Vanguard Total World Stock | 全球 |
| `URTH` | iShares MSCI World ETF | 已開發市場 |

### china_10y_yield_series

中國10Y殖利率來源。

| 值 | 說明 |
|----|------|
| `tradingeconomics` | 從 TradingEconomics 爬取（預設） |
| `csv:path/to/file.csv` | 使用本地 CSV 檔案 |
| `manual` | 手動輸入（互動模式） |

### ma_window

移動平均視窗，用於判定趨勢狀態。

```python
# 預設 60 期（月），對應圖中長期均線
ma_window = 60
```

**調整建議**：
- 更短期觀點：20-30
- 更長期觀點：90-120

### rolling_window

滾動迴歸視窗，用於計算 β 係數。

```python
# 預設 24 個月
rolling_window = 24
```

**調整建議**：
- 更反應性：12-18
- 更穩定：30-36

### round_levels

關卡位置列表，單位 USD/ton。

```python
# 預設關卡
round_levels = [10000, 13000]

# 自定義
round_levels = [8000, 10000, 13000, 15000]
```

### backfill_max_drawdown

用於判定「典型回補」的幅度上限。

```python
# 預設 25%
backfill_max_drawdown = 0.25
```

若觸及高關卡後的回撤在 10%-25% 範圍內，視為典型 back-and-fill。

---

## 命令列介面

### 基本用法

```bash
python scripts/copper_stock_analyzer.py \
    --start 2020-01-01 \
    --end 2026-01-20 \
    --copper HG=F \
    --equity ACWI
```

### 完整參數

```bash
python scripts/copper_stock_analyzer.py \
    --start 2020-01-01 \
    --end 2026-01-20 \
    --copper HG=F \
    --equity ACWI \
    --yield tradingeconomics \
    --ma-window 60 \
    --rolling-window 24 \
    --levels 10000,13000 \
    --output result.json \
    --format json \
    --verbose
```

### 快速檢查模式

```bash
python scripts/copper_stock_analyzer.py --quick
```

等同於：
```bash
python scripts/copper_stock_analyzer.py \
    --start $(date -d "3 years ago" +%Y-%m-%d) \
    --end $(date +%Y-%m-%d) \
    --copper HG=F \
    --equity ACWI \
    --yield tradingeconomics
```

---

## JSON 配置檔（可選）

除了命令列參數，也可使用 JSON 配置檔：

```json
{
  "start_date": "2020-01-01",
  "end_date": "2026-01-20",
  "freq": "1mo",
  "copper_series": "HG=F",
  "equity_proxy_series": "ACWI",
  "china_10y_yield_series": "tradingeconomics",
  "ma_window": 60,
  "rolling_window": 24,
  "round_levels": [10000, 13000],
  "backfill_max_drawdown": 0.25,
  "resilience_weights": {
    "momentum": 0.4,
    "sma": 0.4,
    "drawdown": 0.2
  },
  "output": {
    "path": "result.json",
    "format": "json"
  }
}
```

使用配置檔：
```bash
python scripts/copper_stock_analyzer.py --config config.json
```

---

## 參數驗證

腳本會驗證以下條件：

1. `start_date` < `end_date`
2. `ma_window` >= 1
3. `rolling_window` >= 12
4. `round_levels` 至少包含 2 個值
5. `backfill_max_drawdown` 在 (0, 1) 範圍內
6. 權重總和 = 1.0

驗證失敗時會輸出錯誤訊息並退出。
