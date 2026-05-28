# Markdown 輸出模板 (Output Markdown Template)

## 完整報告模板

```markdown
# {ETF_TICKER} 價格-庫存背離分析報告

**生成時間**：{GENERATED_AT}
**分析期間**：{START_DATE} 至 {END_DATE}

---

## 摘要

| 指標 | 數值 | 狀態 |
|------|------|------|
| 背離判定 | {DIVERGENCE} | {DIVERGENCE_STATUS} |
| {WINDOW_DAYS} 日價格變化 | {PRICE_RETURN_PCT}% | {PRICE_DIRECTION} |
| {WINDOW_DAYS} 日庫存變化 | {INVENTORY_CHANGE_PCT}% | {INVENTORY_DIRECTION} |
| 庫存十年低點 | {DECADE_LOW} | {DECADE_LOW_STATUS} |
| 庫存/價格比值 Z | {RATIO_Z} | {RATIO_Z_STATUS} |
| **壓力分數** | **{STRESS_SCORE}/100** | **{STRESS_LEVEL}** |

---

## 背離狀態詳情

### 價格與庫存

| 項目 | 最新值 | 日期 |
|------|--------|------|
| {COMMODITY} 價格 | ${PRICE} | {PRICE_DATE} |
| {ETF_TICKER} 持倉 | {INVENTORY_OZ:,} oz | {INVENTORY_DATE} |
| 持倉（噸） | {INVENTORY_TONNES:.1f} tonnes | - |

### 歷史背景

| 項目 | 數值 |
|------|------|
| 十年最低庫存 | {DECADE_MIN:,} oz |
| 十年最高庫存 | {DECADE_MAX:,} oz |
| 當前百分位數 | {PERCENTILE:.1f}% |

---

## 壓力分數計算

```
stress_score = 100 × min(1.0,
    0.6 × {DIVERGENCE_SEVERITY:.3f} +    # 背離嚴重度
    0.2 × {DECADE_LOW_BONUS:.1f} +       # 十年低點加成
    0.2 × {RATIO_EXTREME_BONUS:.1f}      # 比值極端加成
)
= {STRESS_SCORE:.1f}
```

| 分數區間 | 等級 | 當前 |
|----------|------|------|
| 0-30 | 正常 | {LEVEL_LOW} |
| 30-60 | 輕度 | {LEVEL_MEDIUM} |
| 60-80 | 中度 | {LEVEL_HIGH} |
| 80-100 | 重度 | {LEVEL_CRITICAL} |

---

## 雙重假設解釋

### 假設 A：實物緊張 (Physical Tightness)

**支持條件**：
- 交易所/金庫庫存同步下降
- 期貨 backwardation 變強
- Lease rates 上升
- 零售溢價擴大

**解讀**：這才比較接近社群敘事所說的「實物吃緊/被抽走」。

### 假設 B：ETF 資金流 (ETF Flow / Redemption)

**支持條件**：
- 其他實物緊張指標不跟
- 期貨結構平穩
- 零售溢價穩定

**解讀**：ETF 持倉下降不必然等同「銀行搶銀條」，可能是投資人資金外流。

---

## 下一步驗證建議

1. {NEXT_CHECK_1}
2. {NEXT_CHECK_2}
3. {NEXT_CHECK_3}
4. {NEXT_CHECK_4}

---

## 附錄：數據來源

| 數據 | 來源 | 更新頻率 |
|------|------|----------|
| 價格 | Yahoo Finance | 即時 |
| ETF 持倉 | {ETF_ISSUER} 官網 | 每日 |
| 交叉驗證 | 各交易所/公開數據 | 不定 |

---

*本報告由 monitor-etf-holdings-drawdown-risk skill 自動生成*
*僅供參考，不構成投資建議*
```

## 簡化報告模板（快速檢查）

```markdown
# {ETF_TICKER} 背離快速檢查

**截至**：{ASOF}

## 結果

| 指標 | 數值 |
|------|------|
| 背離 | {DIVERGENCE_EMOJI} {DIVERGENCE} |
| 壓力分數 | {STRESS_SCORE}/100 ({STRESS_LEVEL}) |
| 價格變化 | {PRICE_RETURN_PCT:+.1f}% |
| 庫存變化 | {INVENTORY_CHANGE_PCT:+.1f}% |
| 十年低點 | {DECADE_LOW_EMOJI} {DECADE_LOW} |

## 建議

{RECOMMENDATION}

## 下一步

- {NEXT_CHECK_1}
- {NEXT_CHECK_2}
```

## 監控報告模板

```markdown
# ETF 持倉背離監控報告

**時間**：{TIMESTAMP}

## 警報摘要

| 等級 | 數量 |
|------|------|
| 嚴重 (CRITICAL) | {CRITICAL_COUNT} |
| 警告 (WARNING) | {WARNING_COUNT} |
| 正常 (NORMAL) | {NORMAL_COUNT} |

## 警報詳情

{#each ALERTS}
### {ALERT_EMOJI} {ETF_NAME} ({ETF_TICKER})

- **等級**：{ALERT_LEVEL}
- **壓力分數**：{STRESS_SCORE}/100
- **背離**：{DIVERGENCE}

{/each}

## 所有監控 ETF

| ETF | 壓力分數 | 背離 | 狀態 |
|-----|----------|------|------|
{#each DETAILS}
| {ETF_TICKER} | {STRESS_SCORE} | {DIVERGENCE} | {STATUS_EMOJI} |
{/each}

---

*下次檢查：{NEXT_CHECK_TIME}*
```

## 占位符說明

| 占位符 | 類型 | 說明 |
|--------|------|------|
| {ETF_TICKER} | string | ETF 代碼 |
| {COMMODITY} | string | 商品名稱 |
| {DIVERGENCE} | boolean | 背離判定 |
| {DIVERGENCE_EMOJI} | string | 背離表情符號（true: ⚠️, false: ✅） |
| {PRICE_RETURN_PCT} | float | 價格變化百分比 |
| {INVENTORY_CHANGE_PCT} | float | 庫存變化百分比 |
| {STRESS_SCORE} | float | 壓力分數 |
| {STRESS_LEVEL} | string | 壓力等級 |
| {DECADE_LOW} | boolean | 十年低點判定 |
| {DECADE_LOW_EMOJI} | string | 十年低點表情符號 |
| {RATIO_Z} | float | 比值 Z 分數 |
| {NEXT_CHECK_N} | string | 下一步驗證建議 |

## 表情符號對照

| 狀態 | 表情符號 |
|------|----------|
| 背離成立 | ⚠️ |
| 無背離 | ✅ |
| 十年低點 | 📉 |
| 非十年低點 | ➖ |
| 壓力：LOW | 🟢 |
| 壓力：MEDIUM | 🟡 |
| 壓力：HIGH | 🟠 |
| 壓力：CRITICAL | 🔴 |
