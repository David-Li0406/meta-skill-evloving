# 方法論：貴金屬礦業毛利率代理值

## 核心概念

### 毛利率代理值 (Gross Margin Proxy)

本 skill 使用的「毛利率代理值」是一個簡化公式，用於快速估算礦業的邊際盈利能力：

```
gross_margin_proxy = (metal_price - unit_cost) / metal_price
```

**重要說明**：
- 此指標**不等同會計報表的毛利率 (GAAP Gross Margin)**
- 會計毛利率需考慮副產品收入、非現金項目、會計準則差異
- 本代理值的優點是**可快速計算、跨公司可比、便於時序分析**

### 與會計毛利率的差異

| 項目       | Margin Proxy           | GAAP Gross Margin          |
|------------|------------------------|----------------------------|
| 計算方式   | (Price - AISC) / Price | (Revenue - COGS) / Revenue |
| 副產品處理 | AISC 已扣除副產品收入  | 需單獨調整                 |
| 非現金項目 | 不含                   | 含折舊/攤銷                |
| 可比性     | 高（標準化公式）       | 低（會計政策差異）         |
| 即時性     | 可用即時金價估算       | 需等財報披露               |

---

## 成本指標口徑

### Cost Metric 層次

```
┌─────────────────────────────────────────────────────────┐
│                    All-In Cost (AIC)                    │
│  ┌───────────────────────────────────────────────────┐  │
│  │               AISC (All-In Sustaining Cost)       │  │
│  │  ┌─────────────────────────────────────────────┐  │  │
│  │  │              Cash Cost (C1)                 │  │  │
│  │  │  - 採掘成本                                 │  │  │
│  │  │  - 加工成本                                 │  │  │
│  │  │  - 場內一般行政                             │  │  │
│  │  └─────────────────────────────────────────────┘  │  │
│  │  + 維持資本開支 (Sustaining CapEx)               │  │
│  │  + 勘探費用                                       │  │
│  │  + 一般行政費用                                   │  │
│  └───────────────────────────────────────────────────┘  │
│  + 成長資本開支 (Growth CapEx)                          │
│  + 併購相關費用                                          │
└─────────────────────────────────────────────────────────┘
```

### 各口徑比較

| 口徑           | 定義            | 典型值 (Gold)   | 適用場景                 |
|----------------|-----------------|-----------------|--------------------------|
| Cash Cost (C1) | 直接現場成本    | $800-1,200/oz   | 現金流壓力測試           |
| AISC           | C1 + 維持開支   | $1,100-1,500/oz | **行業標準**（WGC 定義） |
| All-In Cost    | AISC + 成長開支 | $1,300-1,800/oz | 完整經濟成本             |

**建議**：優先使用 **AISC**，因其：
- 由 World Gold Council 標準化定義（2013 年起）
- 跨公司可比性最佳
- 多數公司在季報中揭露

---

## 聚合方法

### 籃子聚合邏輯

當分析多家礦業時，需將個別毛利率聚合為「籃子毛利率」：

**1. Equal Weight（等權重）**
```python
basket_margin = Σ margin_i / N
```
- 每家公司貢獻相同
- 適用於：關注「典型礦業」表現

**2. Production Weighted（產量加權）**
```python
basket_margin = Σ (margin_i × prod_i) / Σ prod_i
```
- 大型生產商貢獻較大
- 適用於：反映「產業整體毛利」
- **建議使用此方法**

**3. Market Cap Weighted（市值加權）**
```python
basket_margin = Σ (margin_i × mcap_i) / Σ mcap_i
```
- 與 GDX/GDXJ 等 ETF 曝險結構接近
- 適用於：分析「股權曝險」毛利

---

## 歷史分位數計算

### 方法

使用滾動視窗計算當前毛利率在歷史分布中的位置：

```python
def percentile_rank(series, window_years=20):
    window = window_years * 4  # 季度
    ranks = series.rolling(window, min_periods=4).apply(
        lambda x: (x.iloc[-1] > x[:-1]).mean()
    )
    return ranks
```

### 區間標記

| 分位數 | 標記                | 解讀                         |
|--------|---------------------|------------------------------|
| ≥ 90%  | extreme_high_margin | 毛利極端高，均值回歸風險     |
| 70-90% | high_margin         | 毛利較高，礦業盈利良好       |
| 30-70% | neutral             | 毛利中等                     |
| 10-30% | low_margin          | 毛利較低，部分礦業壓力       |
| < 10%  | extreme_low_margin  | 毛利極端低，可能觸及成本支撐 |

### 視窗選擇考量

| 視窗  | 覆蓋週期  | 優點   | 缺點             |
|-------|-----------|--------|------------------|
| 10 年 | ~2 個週期 | 較敏感 | 樣本較少         |
| 15 年 | ~3 個週期 | 平衡   | -                |
| 20 年 | ~4 個週期 | 穩健   | 可能錯過結構變化 |

**建議**：使用 **15-20 年**，覆蓋 2-4 個完整商品週期。

---

## 驅動拆解

### 毛利變化分解

毛利率變化可歸因於價格或成本：

```
Δmargin ≈ f(Δprice, Δcost)
```

展開（一階近似）：
```
Δmargin ≈ (1/P) × ΔP - (1/P) × ΔC + O(...)
         = (ΔP - ΔC) / P
```

### 驅動判斷規則

```python
if abs(price_change) > abs(cost_change) * 2:
    driver = "PRICE_DRIVEN"
elif abs(cost_change) > abs(price_change) * 2:
    driver = "COST_DRIVEN"
else:
    driver = "MIXED"
```

### 驅動類型與含義

| 驅動類型       | 毛利變化 | 解讀                                  |
|----------------|----------|---------------------------------------|
| PRICE_RALLY    | ↑        | 金價上漲帶動，可持續性取決於金價      |
| COST_DECLINE   | ↑        | 成本下降帶動，可能是暫時（油價/匯率） |
| COST_INFLATION | ↓        | 成本通膨壓力，需關注趨勢              |
| PRICE_DROP     | ↓        | 金價下跌帶動，需關注支撐位            |
| MIXED          | -        | 價格與成本同向或幅度相近              |

---

## 數據對齊

### 頻率處理

金屬價格為日頻，成本數據為季頻，需要對齊：

**方法 1：Forward Fill（建議）**
```python
cost_quarterly.reindex(daily_index, method="ffill")
```
- 季度成本值延續到下一季報發布
- 優點：簡單、避免前視偏誤

**方法 2：同季均價**
```python
price_quarterly = price_daily.resample('Q').mean()
```
- 將價格也降到季頻
- 優點：數據乾淨、避免假精度

**建議**：使用**季度頻率**作為基準，以 Method 2 對齊。

### 缺值處理

| 情況               | 處理方式                        |
|--------------------|---------------------------------|
| 某季成本缺失       | 前一季 forward-fill，或該季降權 |
| 連續多季缺失       | 從籃子中剔除該公司              |
| 成本異常（如重組） | Winsorize 或標記排除            |

---

## 離群處理

### Winsorize 方法

將極端值縮至指定分位數：

```python
def winsorize(series, lower=0.01, upper=0.99):
    low = series.quantile(lower)
    high = series.quantile(upper)
    return series.clip(low, high)
```

### 適用場景

- **一次性減記**：成本異常飆高
- **資產出售**：成本異常降低
- **會計變更**：口徑不連續

**建議**：使用 **winsorize_1_99**（1-99 分位數），保留 98% 數據。

---

## 模型限制

1. **非會計毛利率**：不可直接與財報比較
2. **成本滯後**：季報發布滯後 1-2 個月
3. **口徑差異**：不同公司的 AISC 定義可能略有差異
4. **副產品複雜**：白銀礦常有黃金/銅副產品，AISC 處理方式各異
5. **串流公司除外**：FNV、WPM 等串流公司的成本結構不同，不適用本模型

---

## 參考文獻

- World Gold Council (2013). "Guidance Note on Non-GAAP Metrics – All-In Sustaining Costs and All-In Costs"
- VanEck (2024). "The Case for Gold Mining Stocks"
- Kitco News. "AISC Tracking Reports"
