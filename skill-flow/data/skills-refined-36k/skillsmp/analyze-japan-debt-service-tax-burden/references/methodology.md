### 1. 計算 Interest/Tax Ratio

**定義**：
```
interest_tax_ratio = interest_payments / tax_revenue
```

**解讀**：
- 0.25 = 利息吃掉 1/4 稅收
- 0.333 = 利息吃掉 1/3 稅收
- 0.50 = 利息吃掉 1/2 稅收

### 1.1 國債費/稅收比（Debt Service Ratio）

**定義**：
```
debt_service_tax_ratio = debt_service / tax_revenue
```

其中 `debt_service` = 利息支出 + 本金償還（國債費總額）

**重要**：媒體敘事「利息吃掉 1/3 稅收」通常**誤用此口徑**，將國債費（含本金）誤稱為「interest payments alone」。

**FY2025 對照**：
| 口徑 | 分子 | 分母 | 比例 |
|------|------|------|------|
| 純利息/稅收 | 10.5 兆 | 70 兆 | **15.0%** |
| 國債費/稅收 | 28.2 兆 | 70 兆 | **40.3%** |

### 1.2 隱含平均利率（Implied Average Rate）

**定義**：
```
implied_avg_rate = interest_payments / debt_stock
```

**用途**：衡量存量債務的平均融資成本，對比當前市場利率可評估再融資壓力。

**FY2025 計算**：
```
implied_avg_rate = 10.5 兆 / 1,324 兆 = 0.79% ≈ 0.8%
```

**解讀**：
- 隱含利率 **0.8%** vs 當前 10Y 殖利率 **2.0%+**
- 差距說明大量存量債務在低利率時期（YCC/零利率）發行
- 隨著再融資，利息負擔將逐年攀升

### 1.3 「in US terms」換算邏輯

**背景**：媒體常將日本債務以「美國等效規模」表達以增強震撼效果。

**換算公式**（動態計算）：
```
debt_to_gdp = japan_debt_stock / japan_gdp
debt_in_us_terms = us_gdp × debt_to_gdp
```

**數據來源**：
- `us_gdp`：從 FRED 系列 `GDP` 實時抓取
- `japan_gdp`：從 FRED 系列 `JPNNGDP` 實時抓取，或使用配置中的 `japan_gdp_jpy`
- `japan_debt_stock`：從 `fiscal_data.json` 配置讀取

**計算範例**（數值會隨實時數據變動）：
```python
# 假設抓取到的數據
us_gdp = $30.6T（FRED 最新）
japan_gdp_jpy = ¥530 兆（配置）
japan_debt_stock = ¥1,324 兆（配置）

# 計算
debt_to_gdp = 1324 / 530 = 2.50 (250%)
debt_in_us_terms = $30.6T × 2.50 = $76.5T
```

**解讀**：
- 這是「若美國有相同債務/GDP比例，債務規模會是多少」
- 媒體稱「$70T」即來自此換算邏輯（口語化）
- 用於跨國比較時統一規模感知

### 2. 風險分級

| 區間      | 分級      | 含義                |
|-----------|-----------|---------------------|
| < 0.25    | 🟢 GREEN  | 財政彈性充足        |
| 0.25–0.40 | 🟡 YELLOW | 彈性開始下降        |
| 0.40–0.55 | 🟠 ORANGE | 政策空間明顯受限    |
| > 0.55    | 🔴 RED    | 接近敘事「2/3」區域 |

**閾值依據**：
- 0.25：一般財政健康標準
- 0.40：OECD 多數國家不超過此水平
- 0.55：接近歷史極端情況

## 壓力測試公式

### 利率衝擊映射

**核心公式**：
```
additional_interest = debt_stock × pass_through × delta_yield
```

其中：
- `debt_stock`：債務存量（日圓）
- `pass_through`：年度再定價/再融資比例
- `delta_yield`：殖利率上升幅度（小數，200bp = 0.02）

**範例**：
```
debt_stock = ¥1,200 兆
pass_through = 0.15（15%）
delta_yield = 0.02（200bp）

additional_interest = 1,200 × 0.15 × 0.02 = ¥3.6 兆
```

### 壓測後比率

```
stressed_ratio = (interest_payments + additional_interest) / (tax_revenue × (1 + tax_shock))
```

其中 `tax_shock` 為稅收衝擊（負數=下降）。

### 多年累積效應

Year 2 使用累積 pass_through：
```
cumulative_pass_through = pass_through_year1 + pass_through_year2
```

假設每年 15%，兩年累積 30% 存量債務被再定價。

## 殖利率統計分析

### Z-Score

```python
zscore = (latest - mean) / std
```

**解讀**：
- |Z| > 2.0：處於極端區域
- |Z| > 1.5：處於偏離區域

### 百分位數

```python
percentile = (series <= latest).mean()
```

**解讀**：
- > 0.95：近乎歷史最高
- > 0.80：處於高位區
- 0.20–0.80：中性區

## Pass-Through 估算

### 方法 1：平均到期年限

```
pass_through ≈ 1 / average_maturity
```

日本政府債務平均到期 ~8-9 年 → pass_through ~11-12%

### 方法 2：年度發債/到期數據

```
pass_through = (redemptions + new_issuance_at_new_rate) / debt_stock
```

若有實際發債計劃數據，此方法更精確。

### 預設假設

本 Skill 使用 15% 作為保守估計，涵蓋：
- 到期再融資 ~11%
- 新增發債 ~4%

## 敘事核對邏輯

### 「殖利率創 40 年新高」

核對方法：
1. 取 40 年歷史數據
2. 計算 percentile_rank
3. 若 > 0.99 且 latest > max(history[-40Y:]) → 敘事成立

### 「利息吃掉 1/3 稅收」

核對方法：
1. 確認口徑（哪種稅收？純利息還是國債費？）
2. 計算 interest_tax_ratio
3. 若 ≈ 0.333 且口徑對齊 → 敘事成立

### 「日本會拋售美債」

核對方法：
1. 確認日本持有美債規模（TIC）
2. 標示潛在通道與量級
3. **不做行為預測**：持有 ≠ 會拋售

## 局限性

1. **資料滯後**：財政數據通常有 1-2 年滯後
2. **口徑差異**：不同來源定義不同
3. **結構假設**：pass_through 是假設，非實際數據
4. **單一國家**：當前僅支援日本，跨國比較需調整
5. **非線性效應**：極端情況可能有非線性反應
