**核心假說：「SHFE 銅庫存快速回補，且水位處於高檔」→「短線價格更可能出現局部高點」**

這個假說基於以下邏輯：
1. 庫存快速回補代表下游需求可能已經前置完成
2. 庫存處於高檔代表潛在拋售壓力
3. 兩者同時發生時，價格上漲動能可能減弱

**注意**：這是概率訊號，非確定性預測。

---

## 數據來源架構

本技能使用以下數據，分別扮演不同角色：

| 數據         | 來源                 | 頻率 | 角色               |
|--------------|----------------------|------|--------------------|
| SHFE 銅庫存  | MacroMicro (CDP)     | 週   | **主要訊號源**     |
| COMEX 銅庫存 | MacroMicro (CDP)     | 日   | **輔助驗證**       |
| 銅期貨價格   | Yahoo Finance (HG=F) | 日   | **長期分位數判讀** |

### 為什麼使用雙庫存來源？

**SHFE（上海期貨交易所）**：
- 中國消費全球約 50% 的精煉銅
- 反映中國銅需求的即時變化
- 作為**主要訊號來源**

**COMEX（芝加哥商品交易所）**：
- 反映北美/西方市場庫存
- 作為**輔助驗證來源**
- 與 SHFE 同向時，訊號更可靠

**總庫存（SHFE + COMEX）**：
- 反映全球可見庫存趨勢
- 用於判斷整體供需格局

---

## 回補速度 Z-Score 計算

將主觀「回補很快」轉化為客觀可比較的標準化指標。

### Step 1: 計算 W 週累積回補量

```
rebuild_W(t) = inventory(t) - inventory(t - W)
```

- W = 4 週（預設）
- 正值代表「回補」
- 負值代表「去庫存」

**注意**：SHFE 和 COMEX 各自獨立計算，不混合。

### Step 2: 計算滾動均值與標準差

```
μ = rolling_mean(rebuild_W, window=156)   # 3 年滾動
σ = rolling_std(rebuild_W, window=156)
```

### Step 3: 計算 Z-Score

```
z(t) = (rebuild_W(t) - μ) / σ
```

**Z-Score 解讀**：

| Z-Score 範圍 | 解讀               | 短期訊號貢獻  |
|--------------|--------------------|---------------|
| > 2.0        | 回補速度「極端快」 | 強 CAUTION    |
| 1.5 ~ 2.0    | 回補速度「異常快」 | CAUTION       |
| -1.5 ~ 1.5   | 正常範圍           | NEUTRAL       |
| -2.0 ~ -1.5  | 去庫存「異常快」   | SUPPORTIVE    |
| < -2.0       | 去庫存「極端快」   | 強 SUPPORTIVE |

### 為什麼用 3 年滾動？

1. 庫存行為會隨市場結構變化（期貨持倉規模、套利策略）
2. 3 年足夠捕捉近期特性，又有足夠樣本（~156 週）
3. 避免遠期極端值過度影響
4. **SHFE 和 COMEX 各自計算**，保持獨立的基準線

### 代碼範例

```python
W = 4  # 4 週窗口
baseline_weeks = 156  # 3 年滾動

# SHFE z-score
shfe_df['rebuild_W'] = shfe_df['inventory_tonnes'] - shfe_df['inventory_tonnes'].shift(W)
mu = shfe_df['rebuild_W'].rolling(baseline_weeks, min_periods=52).mean()
sigma = shfe_df['rebuild_W'].rolling(baseline_weeks, min_periods=52).std()
shfe_df['rebuild_z'] = (shfe_df['rebuild_W'] - mu) / sigma

# COMEX z-score（獨立計算）
comex_df['rebuild_W'] = comex_df['inventory_tonnes'] - comex_df['inventory_tonnes'].shift(W)
mu_c = comex_df['rebuild_W'].rolling(baseline_weeks, min_periods=52).mean()
sigma_c = comex_df['rebuild_W'].rolling(baseline_weeks, min_periods=52).std()
comex_df['rebuild_z'] = (comex_df['rebuild_W'] - mu_c) / sigma_c
```

---

## 庫存水位分位數

判斷當前庫存水位在歷史分布中的位置。

### 計算方法

```
percentile(t) = (inventory(t) - min) / (max - min)
```

其中 min, max 為過去 N 年（預設 10 年）的最小/最大值。

### 門檻判定

| 分位數      | 解讀         | 短期訊號貢獻     |
|-------------|--------------|------------------|
| ≥ 0.85      | 庫存「偏高」 | CAUTION 前提條件 |
| 0.35 ~ 0.85 | 庫存「正常」 | 中性             |
| ≤ 0.35      | 庫存「偏低」 | 潛在支撐         |

### 也可用絕對門檻

```python
# 絕對門檻模式
if high_inventory_mode == "absolute":
    high_inventory = inventory >= 250000  # 噸
```

---

## 雙庫存同步性分析

### 同步情境（SHFE 與 COMEX 同向）

當兩個庫存來源呈現相同趨勢時：
- 訊號**可信度較高**
- 反映全球銅需求的真實變化
- 可增加訊號權重

**判定方式**：
```python
is_sync = (shfe_rebuild_z > 0 and comex_rebuild_z > 0) or \
          (shfe_rebuild_z < 0 and comex_rebuild_z < 0)
```

### 背離情境（SHFE 與 COMEX 反向）

當兩個庫存來源呈現相反趨勢時：
- 需**謹慎解讀**單一庫存訊號
- 可能為區域性套利或調倉
- 應降低訊號權重

**背離情境解讀**：

| SHFE     | COMEX    | 可能原因                 | 建議                   |
|----------|----------|--------------------------|------------------------|
| 回補 ↑   | 去庫存 ↓ | 中國進口增加導致庫存轉移 | 關注進口數據與價差變化 |
| 去庫存 ↓ | 回補 ↑   | 中國出口增加或需求減弱   | 觀察是否為季節性因素   |

### 總庫存觀察

```python
total_inventory = shfe_inventory + comex_inventory
```

總庫存趨勢用於判斷：
- 全球可見庫存是否在累積或消耗
- 單一交易所的變化是否為「轉移」還是「真實供需」

---

## 價格分位數（長期判讀）

判斷當前銅價在歷史分布中的位置，用於長期便宜/昂貴判讀。

### 計算方法

```
price_percentile(t) = (price(t) - min) / (max - min)
```

其中 min, max 為過去 10 年（520 週）的最小/最大值。

### 門檻判定

| 分位數      | 解讀           | 長期訊號 |
|-------------|----------------|----------|
| ≤ 0.35      | 長期「偏便宜」 | CHEAP    |
| 0.35 ~ 0.65 | 長期「中性」   | FAIR     |
| ≥ 0.65      | 長期「偏貴」   | RICH     |

### 進階：通膨調整（可選）

```python
# 用 CPI 調整為實質價格
real_price = nominal_price / cpi * 100
price_percentile = calculate_percentile(real_price)
```

### 銅價數據注意事項

- HG=F 為 COMEX 銅期貨連續近月合約
- 換倉日可能有價格跳躍
- 建議使用週收盤價減少噪音

---

## 訊號生成邏輯

### 短期訊號（Near-term Signal）

**主訊號基於 SHFE**（中國消費全球 50% 銅）：

```python
if shfe_high_inventory and shfe_fast_rebuild:
    signal = "CAUTION"
elif shfe_low_inventory or shfe_fast_destocking:
    signal = "SUPPORTIVE"
else:
    signal = "NEUTRAL"
```

**COMEX 輔助驗證**：

```python
# 若 COMEX 同步，增強訊號
if signal == "CAUTION" and comex_rebuild_z > 1.0:
    confidence = "HIGH"
elif signal == "CAUTION" and comex_rebuild_z < 0:
    confidence = "LOW"  # 背離，降低信心
else:
    confidence = "MEDIUM"
```

### 完整條件表

| SHFE 庫存水位 | SHFE 回補 z-score | COMEX 同步 | 短期訊號    | 信心 |
|---------------|-------------------|------------|-------------|------|
| ≥ 0.85 分位   | ≥ 1.5             | 是         | **CAUTION** | 高   |
| ≥ 0.85 分位   | ≥ 1.5             | 否         | **CAUTION** | 中   |
| ≥ 0.85 分位   | < 1.5             | -          | NEUTRAL     | -    |
| 正常          | ≥ 1.5             | -          | NEUTRAL     | -    |
| 正常          | 正常              | -          | NEUTRAL     | -    |
| ≤ 0.35 分位   | ≤ -1.5            | 是         | SUPPORTIVE  | 高   |
| 任意          | ≤ -1.5            | 否         | SUPPORTIVE  | 中   |

### 長期訊號（Long-term View）

```python
if price_percentile <= 0.35:
    view = "CHEAP"
elif price_percentile >= 0.65:
    view = "RICH"
else:
    view = "FAIR"
```

---

## 歷史驗證方法論

驗證「訊號觸發」與「價格局部高點」的歷史相關性。

### Step 1: 識別訊號週

找出所有滿足 CAUTION 條件的週次：
- SHFE rebuild_z ≥ 1.5
- SHFE inventory_percentile ≥ 0.85

### Step 2: 定義「局部高點」

在訊號週的 ±N 週（預設 N=2）內，若訊號週的價格為該窗口最高，則視為「命中」。

```python
window = price[t-N : t+N]
is_peak = price[t] >= max(window) * 0.99  # 容許 1% 誤差
```

### Step 3: 計算命中率

```
hit_rate = 命中次數 / 訊號觸發次數
```

### 解讀

| 命中率    | 解讀                           |
|-----------|--------------------------------|
| > 65%     | 訊號有較強參考價值             |
| 55% ~ 65% | 訊號有參考價值，需搭配其他指標 |
| < 55%     | 訊號接近隨機，參考價值低       |

### COMEX 增強驗證

```python
# 計算「SHFE + COMEX 同步」的訊號命中率
sync_signals = signals[comex_also_rebuilding]
sync_hit_rate = calculate_hit_rate(sync_signals)

# 通常同步訊號的命中率會更高
```

### 回測限制

1. 樣本量可能不足（訊號觸發次數有限）
2. 未考慮前視偏差（look-ahead bias）
3. 市場結構可能已變化
4. SHFE 和 COMEX 的歷史同步性可能隨時間變化

---

## 參數敏感度分析

不同參數設定對訊號的影響：

### 1. 回補窗口 W

| W    | 訊號特性           | 建議場景 |
|------|--------------------|----------|
| 2 週 | 更敏感，訊號更頻繁 | 短線交易 |
| 4 週 | 平衡               | 預設     |
| 8 週 | 更平滑，訊號更少   | 中期趨勢 |

### 2. Z-Score 門檻

| 門檻 | 訊號特性             |
|------|----------------------|
| 1.2  | 訊號頻繁，假陽性較多 |
| 1.5  | 平衡（預設）         |
| 2.0  | 訊號稀少，但更可靠   |

### 3. 庫存分位數門檻

| 門檻 | 訊號特性           |
|------|--------------------|
| 0.80 | 更容易觸發 CAUTION |
| 0.85 | 平衡（預設）       |
| 0.90 | 較少觸發，但更極端 |

---

## 方法限制

1. **季節性**：農曆新年前後的季節性庫存波動可能產生假訊號
2. **結構變化**：中國銅消費結構變化可能影響庫存行為
3. **雙來源限制**：僅依賴 SHFE + COMEX，未整合 LME
4. **價格因素**：未考慮價格本身的技術形態
5. **基本面**：未整合供需平衡表等基本面數據
6. **換倉跳躍**：HG=F 期貨連續合約在換倉日可能有價格不連續

### 使用建議

- 作為風險管理參考，非唯一決策依據
- 搭配其他技術/基本面指標
- 關注訊號的時間穩定性
- 定期驗證回測結果是否失效
- **優先參考 SHFE 訊號，COMEX 作為輔助驗證**
- **當 SHFE 與 COMEX 背離時，降低訊號權重**

---

## 學術與實務參考

1. **庫存與價格關係**
   - 商品期貨理論認為庫存水位影響期貨升貼水
   - 高庫存 → contango → 潛在拋售壓力

2. **動能與均值回歸**
   - z-score 極端值傾向均值回歸
   - 但非對稱：回補極端可能持續更久

3. **中國因素**
   - 中國銅消費佔全球 ~50%
   - SHFE 庫存對銅價的邊際影響顯著
   - COMEX 反映西方市場供需

4. **跨市套利**
   - SHFE 與 COMEX 價差影響實物流向
   - 庫存背離時需考慮套利因素
