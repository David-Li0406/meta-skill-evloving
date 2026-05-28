# Workflow: 完整情境分析

<required_reading>
**執行前請先閱讀：**
1. references/methodology.md - 計算方法論
2. references/input-schema.md - 完整參數定義
3. references/data-sources.md - 數據來源
</required_reading>

<process>

## Step 1: 確認分析參數

收集以下必要參數：

| 參數        | 預設值              | 說明                    |
|-------------|---------------------|-------------------------|
| metal       | gold                | 目標金屬（gold/silver） |
| miners      | 預設籃子            | 礦業代號清單            |
| start_date  | 10 年前             | 計算起始日              |
| end_date    | today               | 計算結束日              |
| frequency   | quarterly           | 頻率                    |
| cost_metric | AISC                | 成本口徑                |
| aggregation | production_weighted | 聚合方式                |

若用戶未提供，使用預設值。

**預設籃子**：
- 黃金：NEM, GOLD, AEM, FNV, WPM
- 白銀：CDE, HL, AG, PAAS, MAG

## Step 2: 取得金屬價格序列

執行腳本取得價格數據：

```bash
python scripts/margin_calculator.py \
  --step price \
  --metal {metal} \
  --start-date {start_date} \
  --end-date {end_date} \
  --frequency {frequency}
```

或使用 Python 直接執行：

```python
import yfinance as yf
import pandas as pd

# 期貨近月合約
ticker = "GC=F" if metal == "gold" else "SI=F"
df = yf.download(ticker, start=start_date, end=end_date)

# 重採樣
if frequency == "quarterly":
    df_resampled = df['Close'].resample('Q').mean()
elif frequency == "monthly":
    df_resampled = df['Close'].resample('M').mean()
```

## Step 3: 取得礦業成本數據

成本數據通常需從以下來源取得：

1. **已建立的資料庫**：如有歷史資料庫，直接讀取
2. **公司 IR 網站**：手動或爬蟲取得
3. **使用估算值**：參考 references/data-sources.md 的估算方法

**資料格式**：
```python
cost_data = {
    "NEM": {"2024-Q3": 1380, "2024-Q4": 1350, ...},  # USD/oz
    "GOLD": {"2024-Q3": 1290, "2024-Q4": 1310, ...},
    ...
}
production_data = {
    "NEM": {"2024-Q3": 1500000, "2024-Q4": 1600000, ...},  # oz
    ...
}
```

## Step 4: 計算毛利率代理值

對齊數據並計算：

```python
def margin_proxy(price, unit_cost):
    """計算毛利率代理值"""
    return (price - unit_cost) / price

def align_cost_to_price_index(cost_quarterly, price_index):
    """將季度成本對齊到價格索引"""
    return cost_quarterly.reindex(price_index, method="ffill")

# 計算每家公司的毛利率
margins = {}
for miner in miners:
    aligned_cost = align_cost_to_price_index(cost_data[miner], price_index)
    margins[miner] = margin_proxy(price_series, aligned_cost)
```

## Step 5: 聚合籃子毛利率

根據聚合方式計算籃子毛利率：

```python
def aggregate_margins(margins_df, weights_df=None, mode="production_weighted"):
    if mode == "equal_weight" or weights_df is None:
        return margins_df.mean(axis=1)

    # 正規化權重
    w = weights_df.div(weights_df.sum(axis=1), axis=0).fillna(0.0)
    return (margins_df * w).sum(axis=1)

basket_margin = aggregate_margins(
    pd.DataFrame(margins),
    pd.DataFrame(production_data),
    mode=aggregation
)
```

## Step 6: 計算歷史分位數與區間標記

```python
def compute_percentile_rank(series, window_years=20):
    """計算滾動歷史分位數"""
    window = window_years * 4  # 季度
    ranks = series.rolling(window, min_periods=4).apply(
        lambda x: (x.iloc[-1] > x[:-1]).mean()
    )
    return ranks

def regime_label(percentile):
    """區間標記"""
    if percentile >= 0.9:
        return "extreme_high_margin"
    elif percentile >= 0.7:
        return "high_margin"
    elif percentile >= 0.3:
        return "neutral"
    elif percentile >= 0.1:
        return "low_margin"
    else:
        return "extreme_low_margin"
```

## Step 7: 驅動拆解

```python
def decompose_driver(price_series, cost_series, lookback=3):
    """拆解毛利率變化的驅動因素"""
    price_change = (price_series.iloc[-1] / price_series.iloc[-lookback-1]) - 1
    cost_change = (cost_series.iloc[-1] / cost_series.iloc[-lookback-1]) - 1

    if abs(price_change) > abs(cost_change) * 2:
        driver = "mostly_price" + ("_up" if price_change > 0 else "_down")
    elif abs(cost_change) > abs(price_change) * 2:
        driver = "mostly_cost" + ("_down" if cost_change < 0 else "_up")
    else:
        driver = "mixed"

    return {
        "price_change_pct": price_change,
        "cost_change_pct": cost_change,
        "driver": driver
    }
```

## Step 8: 輸出結果

使用 `templates/output-json.md` 格式輸出：

```bash
python scripts/margin_calculator.py \
  --metal {metal} \
  --miners {miners} \
  --start-date {start_date} \
  --frequency {frequency} \
  --cost-metric {cost_metric} \
  --aggregation {aggregation} \
  --output result.json
```

## Step 9: 生成報告

若需要 Markdown 報告：

```bash
python scripts/margin_calculator.py \
  --output result.md \
  --format markdown
```

</process>

<success_criteria>
完成分析時應產出：

- [ ] 金屬價格時序數據（已重採樣）
- [ ] 各礦業成本數據（AISC/現金成本）
- [ ] 各礦業毛利率代理值
- [ ] 產量/市值加權的籃子毛利率
- [ ] 歷史分位數排名
- [ ] 區間標記（extreme_high/high/neutral/low/extreme_low）
- [ ] 驅動拆解（價格 vs 成本）
- [ ] JSON 或 Markdown 格式的輸出
</success_criteria>
