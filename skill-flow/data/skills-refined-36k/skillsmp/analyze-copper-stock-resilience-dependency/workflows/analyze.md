# Workflow: 完整分析

<required_reading>
**執行前請閱讀：**
1. references/methodology.md - 跨資產依賴方法論
2. references/data-sources.md - 數據來源與爬蟲說明
3. references/input-schema.md - 完整參數定義
</required_reading>

<process>

## Step 1: 資料擷取 (Data Ingestion)

抓取三條核心序列：

### 1.1 銅期貨價格（月K）

```python
# 使用 yfinance 抓取 COMEX Copper
python scripts/fetch_data.py --series HG=F --start 2020-01-01 --end 2026-01-20 --freq 1mo
```

**注意**：HG=F 為 $/lb，需轉換為 $/ton：
```python
copper_usd_per_ton = copper_usd_per_lb * 2204.62262
```

### 1.2 全球股市韌性代理

```python
# 使用 yfinance 抓取 ACWI
python scripts/fetch_data.py --series ACWI --start 2020-01-01 --end 2026-01-20 --freq 1mo
```

### 1.3 中國10年公債殖利率

```python
# 使用 Selenium 爬取 TradingEconomics
python scripts/fetch_china_10y.py --start 2020-01-01 --end 2026-01-20
```

**快取策略**：爬蟲數據建議快取 12 小時，避免頻繁請求。

### 1.4 資料對齊

```python
# 統一轉成月頻、對齊時間索引
df = align_monthly({
    "copper": copper,
    "equity": equity,
    "cny10y": cny10y
}).dropna()
```

## Step 2: 趨勢與關卡分析 (Trend & Round Levels)

### 2.1 計算移動平均與趨勢

```python
# 計算 60 期（月）SMA
df["copper_sma"] = df["copper"].rolling(ma_window).mean()
df["copper_sma_slope"] = df["copper_sma"].diff()

# 定義趨勢狀態
df["copper_trend"] = np.where(
    (df["copper"] > df["copper_sma"]) & (df["copper_sma_slope"] > 0), "up",
    np.where(
        (df["copper"] < df["copper_sma"]) & (df["copper_sma_slope"] < 0), "down",
        "range"
    )
)
```

### 2.2 關卡判定

```python
# 設定關卡（如 10,000 / 13,000）
round_levels = [10000, 13000]
threshold = 0.05  # 5% 容忍範圍

# 判斷接近哪個關卡
near_resistance = [lv for lv in round_levels if abs(price - lv)/lv < threshold and price < lv]
near_support = [lv for lv in round_levels if abs(price - lv)/lv < threshold and price > lv]
```

## Step 3: 股市韌性評分 (Equity Resilience Score)

### 3.1 計算三個因子

```python
# 12 個月動能
df["equity_12m_ret"] = df["equity"].pct_change(12)

# 是否站上 12 月均線
df["equity_sma12"] = df["equity"].rolling(12).mean()
df["above_sma"] = (df["equity"] > df["equity_sma12"]).astype(int)

# 近 3 個月回撤
df["equity_3m_max"] = df["equity"].rolling(3).max()
df["equity_drawdown_3m"] = (df["equity_3m_max"] - df["equity"]) / df["equity_3m_max"]
```

### 3.2 計算加權評分

```python
# 分位數函數
def percentile_rank(series):
    return series.rank(pct=True) * 100

# 計算韌性評分
df["equity_resilience_score"] = (
    0.4 * percentile_rank(df["equity_12m_ret"]) +
    0.4 * df["above_sma"] * 100 +
    0.2 * (1 - np.clip(df["equity_drawdown_3m"] / 0.15, 0, 1)) * 100
)
```

## Step 4: 滾動迴歸 (Rolling Regression)

### 4.1 計算報酬率

```python
ret = pd.DataFrame({
    "dcopper": df["copper"].pct_change(),
    "dequity": df["equity"].pct_change(),
    "dyield": df["cny10y"].diff()
}).dropna()
```

### 4.2 執行滾動迴歸

```python
from statsmodels.regression.rolling import RollingOLS

# 設定 rolling window（24 個月）
model = RollingOLS(
    ret["dcopper"],
    sm.add_constant(ret[["dequity", "dyield"]]),
    window=rolling_window
)
betas = model.fit()

# 提取係數
df["beta_equity"] = betas.params["dequity"]
df["beta_yield"] = betas.params["dyield"]
df["r_squared"] = betas.rsquared
```

## Step 5: 回補機率估計 (Backfill Probability)

### 5.1 定義回補事件

```python
def detect_backfill_events(df, level_hi=13000, level_lo=10000, lookforward=12):
    """
    偵測觸及高關卡後回補到低關卡的事件
    """
    events = []
    for i, row in df.iterrows():
        if row["copper"] >= level_hi * 0.98:  # 觸及高關卡
            future = df.loc[i:].head(lookforward)
            trough = future["copper"].min()
            if trough <= level_lo * 1.02:  # 回到低關卡
                events.append({
                    "touch_date": i,
                    "touch_price": row["copper"],
                    "trough_price": trough,
                    "backfill": True,
                    "equity_resilience": row["equity_resilience_score"]
                })
            else:
                events.append({
                    "touch_date": i,
                    "touch_price": row["copper"],
                    "trough_price": trough,
                    "backfill": False,
                    "equity_resilience": row["equity_resilience_score"]
                })
    return pd.DataFrame(events)
```

### 5.2 分組統計

```python
events_df = detect_backfill_events(df)

# 整體回補率
overall_backfill_rate = events_df["backfill"].mean()

# 依韌性分組
high_resilience = events_df[events_df["equity_resilience"] >= 70]
low_resilience = events_df[events_df["equity_resilience"] <= 30]

backfill_stats = {
    "overall": overall_backfill_rate,
    "equity_resilience_high": high_resilience["backfill"].mean(),
    "equity_resilience_low": low_resilience["backfill"].mean()
}
```

## Step 6: 情境判讀 (Insight Generation)

### 6.1 輸出診斷

回答三個核心問題：

**Q1: 現在是續航情境，還是回補情境？**
```python
if copper_trend == "up" and near_resistance and equity_resilience_score >= 70:
    scenario = "續航機率較高"
elif copper_trend == "up" and near_resistance and equity_resilience_score < 50:
    scenario = "回補風險上升"
else:
    scenario = "需持續觀察"
```

**Q2: 依賴股市有多強？**
```python
beta_percentile = percentile_rank(beta_equity)
if beta_percentile >= 75:
    dependency = "高依賴：市場正把銅當風險資產交易"
elif beta_percentile >= 50:
    dependency = "中度依賴"
else:
    dependency = "低依賴：銅有自身邏輯"
```

**Q3: 中國殖利率扮演什麼角色？**
```python
yield_change = df["cny10y"].diff(12).iloc[-1]
if yield_change < 0 and equity_resilience_score < 50:
    yield_role = "殖利率下行 + 股市不強 → 風險/成長壓力敘事（對銅不利）"
elif yield_change < 0 and equity_resilience_score >= 70:
    yield_role = "殖利率下行 + 股市強勢 → 寬鬆/流動性敘事（未必對銅不利）"
else:
    yield_role = "中性，需觀察"
```

## Step 7: 輸出結果

```python
# 執行完整分析
python scripts/copper_stock_analyzer.py \
    --start 2020-01-01 \
    --end 2026-01-20 \
    --copper HG=F \
    --equity ACWI \
    --output result.json
```

輸出結構參見 `templates/output-json.md`。

</process>

<success_criteria>
完整分析成功時應產出：

- [ ] 銅價時間序列（已轉換為 USD/ton）
- [ ] 趨勢狀態（up/down/range）
- [ ] 關卡接近判定（near_resistance/near_support）
- [ ] 股市韌性評分（0-100）
- [ ] 滾動貝塔係數（β_equity, β_yield）
- [ ] 回補機率統計（overall / high / low）
- [ ] 情境判讀敘述
- [ ] JSON 輸出檔案
</success_criteria>
