# Markdown 輸出模板 (Output Markdown Template)

## 完整報告模板

```markdown
# 投資時鐘分析報告

**分析日期**：{as_of}
**市場**：{market}
**分析區間**：{start_date} 至 {end_date}

---

## 當前位置

| 指標 | 數值 | 狀態 |
|------|------|------|
| 時鐘點位 | {clock_hour} 點 | {quadrant_name} |
| 獲利成長 | {y_value:.1%} | {earnings_status} |
| 金融環境 Z-score | {x_value:.2f} | {fci_status} |

### 象限判定

**當前象限**：{quadrant_name}（{quadrant}）

{interpretation}

### 配置建議

{quadrant_implication}

---

## 旋轉分析

| 項目 | 數值 |
|------|------|
| 起始點位 | {from_hour} 點（{from_quadrant_name}） |
| 目前點位 | {to_hour} 點（{to_quadrant_name}） |
| 旋轉方向 | {direction_cn} |
| 旋轉幅度 | {magnitude_degrees}° |

### 旋轉解讀

{magnitude_note}

---

## 象限時間分布

| 象限 | 期數 | 佔比 |
|------|------|------|
| 理想象限（Q1） | {q1_periods} | {q1_pct:.1%} |
| 好壞混合（Q2） | {q2_periods} | {q2_pct:.1%} |
| 修復過渡（Q3） | {q3_periods} | {q3_pct:.1%} |
| 最差象限（Q4） | {q4_periods} | {q4_pct:.1%} |

---

## 風險監控

### 需關注的因素

{risk_factors_list}

### 監控指標

{monitoring_points_list}

---

## 資料來源

| 指標 | 系列 ID | 最新日期 | 最新值 |
|------|---------|----------|--------|
| 獲利成長 | {earnings_series_id} | {earnings_latest_date} | {earnings_latest_value} |
| 金融環境 | {fci_series_id} | {fci_latest_date} | {fci_latest_value} |

### 注意事項

{notes_list}

---

*報告生成時間：{generated_at}*
*技能版本：{skill_version}*
```

---

## 循環比較模板

```markdown
# 投資時鐘循環比較報告

**分析日期**：{as_of}

---

## 循環概覽

### 當前循環

| 項目 | 數值 |
|------|------|
| 期間 | {current_start} 至 {current_end} |
| 起始點位 | {current_from_hour} 點 |
| 目前點位 | {current_to_hour} 點 |
| 旋轉幅度 | {current_magnitude}° |
| 路徑特徵 | {current_character} |

### 前一輪循環（{previous_name}）

| 項目 | 數值 |
|------|------|
| 期間 | {previous_start} 至 {previous_end} |
| 起始點位 | {previous_from_hour} 點 |
| 終點點位 | {previous_to_hour} 點 |
| 旋轉幅度 | {previous_magnitude}° |
| 路徑特徵 | {previous_character} |

---

## 比較分析

| 比較項目 | 當前循環 | 前一輪循環 |
|----------|----------|------------|
| 旋轉幅度 | {current_magnitude}° | {previous_magnitude}° |
| 旋轉方向 | {current_direction} | {previous_direction} |
| 主要路徑 | {current_path} | {previous_path} |

### 同質性判斷

**判定結果**：{homogeneity}

{homogeneity_explanation}

---

## 結論與建議

{comparison_implications}

### 注意事項

{caveats_list}

---

*報告生成時間：{generated_at}*
```

---

## 快速報告模板

```markdown
## 投資時鐘快速檢查

**截至**：{as_of}

### 當前位置

- **時鐘點位**：{clock_hour} 點
- **象限**：{quadrant_name}
- **獲利成長**：{y_value:.1%}
- **金融環境**：{x_value:.2f}（{fci_status}）

### 解讀

{interpretation}

### 配置建議

{implication}
```

---

## 表格格式模板

用於終端顯示：

```
投資時鐘分析結果（數據截至 {as_of}）

┌────────────────────────────┬────────┬──────────────────────────┐
│            指標            │  數值  │           狀態           │
├────────────────────────────┼────────┼──────────────────────────┤
│ 時鐘點位                   │ {hour} │ {quadrant_name}          │
├────────────────────────────┼────────┼──────────────────────────┤
│ 獲利成長 (Earnings Growth) │ {y}%   │ {earnings_status}        │
├────────────────────────────┼────────┼──────────────────────────┤
│ 金融環境 (FCI Z-score)     │ {x}    │ {fci_status}             │
└────────────────────────────┴────────┴──────────────────────────┘

旋轉分析
┌──────────┬───────────┬──────────────────────────┐
│   項目   │   數值    │           說明           │
├──────────┼───────────┼──────────────────────────┤
│ 起始點位 │ {from} 點 │ {from_quadrant}          │
├──────────┼───────────┼──────────────────────────┤
│ 目前點位 │ {to} 點   │ {to_quadrant}            │
├──────────┼───────────┼──────────────────────────┤
│ 旋轉方向 │ {dir}     │ {dir_explanation}        │
├──────────┼───────────┼──────────────────────────┤
│ 旋轉幅度 │ {mag}°    │ {mag_note}               │
└──────────┴───────────┴──────────────────────────┘

配置建議
{implication}

注意事項
{caveats}
```

---

## 變數說明

| 變數 | 說明 | 範例 |
|------|------|------|
| {as_of} | 資料截止日 | 2026-01-19 |
| {clock_hour} | 時鐘點位 | 10 |
| {quadrant} | 象限代碼 | Q1_ideal |
| {quadrant_name} | 象限中文名 | 理想象限 |
| {x_value} | X 軸數值 | -0.35 |
| {y_value} | Y 軸數值 | 0.052 |
| {direction_cn} | 旋轉方向中文 | 順時針 |
| {magnitude_degrees} | 旋轉度數 | 240 |
| {earnings_status} | 獲利狀態 | 正成長 |
| {fci_status} | 金融環境狀態 | 偏寬鬆 |
