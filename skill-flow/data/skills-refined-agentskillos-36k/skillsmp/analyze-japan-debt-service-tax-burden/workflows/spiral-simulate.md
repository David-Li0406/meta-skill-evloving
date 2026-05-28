# 債務螺旋模擬工作流

模擬多年累積效應，視覺化展示 Interest/Tax Ratio 如何在持續高利率環境下逐年惡化。

## 核心概念

**債務螺旋邏輯**：
```
Year N: cumulative_pass_through = min(N × 0.15, 1.0)
        additional_interest = debt_stock × cumulative_pass_through × delta_yield
        ratio = (base_interest + additional_interest) / (tax × tax_growth^N)
```

隨著時間推移，越來越多存量債務以新高利率再融資，利息負擔逐年累積上升。

## 快速執行

### 完整多情境 Dashboard

```bash
cd skills/analyze-japan-debt-service-tax-burden
python scripts/generate_spiral_chart.py --all --output-dir ../../../output
```

輸出包含 4 種情境：
- 基準（維持現狀）
- +200bp（利率正常化）
- +200bp + 衰退（稅收 -3%/年）
- +300bp 嚴重衝擊

### 單一壓力情境

```bash
# +200bp 衝擊
python scripts/generate_spiral_chart.py --stress 200 --output-dir ../../../output

# +300bp 衝擊
python scripts/generate_spiral_chart.py --stress 300 --output-dir ../../../output
```

### 自定義模擬年數

```bash
# 15 年模擬
python scripts/generate_spiral_chart.py --years 15 --output-dir ../../../output
```

## 輸出圖表說明

### 1. 螺旋比較圖（主圖）

- **X 軸**：模擬年數（0-10 年）
- **Y 軸**：Interest/Tax Ratio（0-70%）
- **背景區間**：綠/黃/橙/紅風險區
- **曲線**：各情境 Ratio 演變軌跡
- **終點標註**：最終 Ratio 與風險等級

### 2. 利息分解圖

- 堆疊柱狀圖展示「原始利息 + 新增利息」
- 清晰顯示利率上升帶來的增量負擔

### 3. 摘要統計

- 初始財政數據
- 各情境 Year 10 結果與風險等級

## 情境設計參考

### 保守情境

```python
{
    "name": "温和升息",
    "delta_yield_bp": 100,
    "tax_growth": 0.02,  # 經濟成長 2%
}
```

### 壓力情境

```python
{
    "name": "+200bp + 經濟停滯",
    "delta_yield_bp": 200,
    "tax_growth": 0.0,  # 稅收不變
}
```

### 嚴重情境

```python
{
    "name": "+300bp + 衰退",
    "delta_yield_bp": 300,
    "tax_growth": -0.05,  # 稅收年減 5%
}
```

## 解讀指引

### 風險區間含義

| 區間 | Ratio | 含義 |
|------|-------|------|
| GREEN | <25% | 財政彈性充足 |
| YELLOW | 25-40% | 政策空間開始受限 |
| ORANGE | 40-55% | 需要政策調整 |
| RED | >55% | 接近「利息吃掉 2/3 稅收」敘事區 |

### 關鍵觀察點

1. **曲線斜率**：斜率越陡，惡化速度越快
2. **交叉點**：何時從綠區進入黃區？從黃區進入橙區？
3. **收斂性**：是否在某年後趨於穩定（pass_through 達到 100%）
4. **情境差異**：稅收成長/衰退對結果的影響有多大？

## 與其他工作流搭配

1. **先執行快速檢查**（quick-check.md）了解當前狀態
2. **再執行螺旋模擬**了解長期風險
3. **最後生成完整 Dashboard**（generate-chart.md）綜合報告
