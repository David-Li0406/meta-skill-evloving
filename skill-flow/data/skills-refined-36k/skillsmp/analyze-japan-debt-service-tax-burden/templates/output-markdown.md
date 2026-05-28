# Markdown 報告模板

## 標準報告格式

```markdown
# 分析日本債務利息負擔報告

> 分析日期：{as_of}

## 摘要

**{headline}**

## 殖利率狀態

| 指標           | 數值          |
|----------------|---------------|
| {tenor} 殖利率 | {latest}%     |
| 百分位數       | {percentile}% |
| Z-Score        | {zscore}      |

{interpretation}

## 財政利息負擔

| 指標               | 數值                            |
|--------------------|---------------------------------|
| 稅收               | ¥{tax_revenue_jpy/1e12}兆       |
| 利息支出           | ¥{interest_payments_jpy/1e12}兆 |
| 債務存量           | ¥{debt_stock_jpy/1e12}兆        |
| Interest/Tax Ratio | {interest_tax_ratio}%           |
| 風險分級           | {risk_band_emoji} {risk_band}   |

**口徑說明**：
- 稅收：{tax_revenue_series}
- 利息：{interest_payment_series}
- 財政年度：{fiscal_year}

## 壓力測試結果

| 情境 | Year 1 Ratio | Year 2 Ratio | 風險分級 |
|------|--------------|--------------|----------|
{stress_test_rows}

## 外溢通道（日本對美資產）

- 估計總規模：${us_assets_estimate_usd/1e12}兆
- 美債持有：${ust_holdings_usd/1e12}兆

> {spillover_note}

## 要點摘要

{headline_takeaways}

---

*報告由 analyze-japan-debt-service-tax-burden skill 自動生成*
```

## 範例輸出

```markdown
# 分析日本債務利息負擔報告

> 分析日期：2026-01-20

## 摘要

**利息支出佔稅收 33.3%，處於🟡 YELLOW 區**

## 殖利率狀態

| 指標       | 數值  |
|------------|-------|
| 10Y 殖利率 | 1.23% |
| 百分位數   | 97%   |
| Z-Score    | 2.10  |

分位數 97%，處於極端高位區

## 財政利息負擔

| 指標               | 數值       |
|--------------------|------------|
| 稅收               | ¥72.0兆    |
| 利息支出           | ¥24.0兆    |
| 債務存量           | ¥1,200.0兆 |
| Interest/Tax Ratio | 33.3%      |
| 風險分級           | 🟡 YELLOW  |

**口徑說明**：
- 稅收：general_account_tax
- 利息：interest_only
- 財政年度：FY2024

## 壓力測試結果

| 情境                         | Year 1 Ratio | Year 2 Ratio | 風險分級  |
|------------------------------|--------------|--------------|-----------|
| +100bp baseline              | 35.8%        | 38.3%        | 🟡 YELLOW |
| +200bp baseline              | 38.3%        | 43.3%        | 🟠 ORANGE |
| +200bp + recession (-5% tax) | 40.4%        | 45.6%        | 🟠 ORANGE |
| +300bp severe stress         | 43.3%        | 53.3%        | 🟠 ORANGE |

## 外溢通道（日本對美資產）

- 估計總規模：$3.0兆
- 美債持有：$1.1兆

> 僅標示潛在通道與量級；是否『會拋售』屬行為假設，需搭配資金流/政策約束判讀

## 要點摘要

- 當前 interest/tax ratio 為 33.3%，處於 YELLOW 區
- 10Y JGB 殖利率 1.23% 處於 97% 分位，接近近期極值
- 最嚴重壓測情境下，兩年後 ratio 可能升至 53.3%，進入 ORANGE 區
- 注意：不同口徑會產生不同數值，本分析已標示使用口徑

---

*報告由 analyze-japan-debt-service-tax-burden skill 自動生成*
```

## 格式化規則

### 數值格式

| 類型       | 格式                | 範例    |
|------------|---------------------|---------|
| 百分比     | {value:.1%}         | 33.3%   |
| 金額（兆） | ¥{value/1e12:.1f}兆 | ¥72.0兆 |
| 殖利率     | {value:.2f}%        | 1.23%   |
| 分位數     | {value:.0%}         | 97%     |

### 風險分級 Emoji

| 分級   | Emoji |
|--------|-------|
| green  | 🟢    |
| yellow | 🟡    |
| orange | 🟠    |
| red    | 🔴    |
