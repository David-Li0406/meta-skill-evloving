# JSON 輸出模板

## 完整輸出結構

```json
{
  "skill": "analyze_japan_debt_service_tax_burden",
  "mode": "full_analysis",
  "as_of": "2026-01-20",

  "yield_stats": {
    "tenor": "10Y",
    "latest": 1.23,
    "zscore": 2.10,
    "percentile": 0.97,
    "window_days": 504,
    "min": 0.65,
    "max": 1.25,
    "mean": 0.92,
    "interpretation": "分位數 97%，處於極端高位區"
  },

  "fiscal": {
    "tax_revenue_jpy": 72000000000000,
    "interest_payments_jpy": 24000000000000,
    "debt_stock_jpy": 1200000000000000,
    "interest_tax_ratio": 0.3333,
    "risk_band": "yellow",
    "risk_band_emoji": "🟡",
    "definition": {
      "tax_revenue_series": "general_account_tax",
      "interest_payment_series": "interest_only",
      "fiscal_year": "FY2024"
    }
  },

  "stress_tests": [
    {
      "name": "+100bp baseline",
      "assumptions": {
        "delta_yield_bp": 100,
        "pass_through_year1": 0.15,
        "pass_through_year2": 0.15,
        "tax_shock": 0.0
      },
      "results": {
        "year1_interest_tax_ratio": 0.3583,
        "year2_interest_tax_ratio": 0.3833
      },
      "risk_band_year1": "yellow",
      "risk_band_year2": "yellow"
    },
    {
      "name": "+200bp baseline",
      "assumptions": {
        "delta_yield_bp": 200,
        "pass_through_year1": 0.15,
        "pass_through_year2": 0.15,
        "tax_shock": 0.0
      },
      "results": {
        "year1_interest_tax_ratio": 0.3833,
        "year2_interest_tax_ratio": 0.4333
      },
      "risk_band_year1": "yellow",
      "risk_band_year2": "orange"
    },
    {
      "name": "+200bp + recession (-5% tax)",
      "assumptions": {
        "delta_yield_bp": 200,
        "pass_through_year1": 0.15,
        "pass_through_year2": 0.15,
        "tax_shock": -0.05
      },
      "results": {
        "year1_interest_tax_ratio": 0.4035,
        "year2_interest_tax_ratio": 0.4561
      },
      "risk_band_year1": "orange",
      "risk_band_year2": "orange"
    }
  ],

  "spillover_channel": {
    "enabled": true,
    "us_assets_estimate_usd": 3000000000000,
    "ust_holdings_usd": 1100000000000,
    "components": [
      "UST holdings (TIC)",
      "Agency securities",
      "Corporate bonds",
      "Equities"
    ],
    "note": "僅標示潛在通道與量級；是否『會拋售』屬行為假設，需搭配資金流/政策約束判讀"
  },

  "headline_takeaways": [
    "當前 interest/tax ratio 為 33.3%，處於 YELLOW 區",
    "10Y JGB 殖利率 1.23% 處於 97% 分位，接近近期極值",
    "最嚴重壓測情境下，兩年後 ratio 可能升至 45.6%，進入 ORANGE 區",
    "注意：不同口徑（國稅 vs 一般會計 vs 總收入）會產生不同數值，本分析已標示使用口徑"
  ]
}
```

## 快速檢查輸出

```json
{
  "mode": "quick_check",
  "as_of": "2026-01-20",
  "yield_stats": {
    "tenor": "10Y",
    "latest": 1.23,
    "percentile": 0.97
  },
  "fiscal": {
    "interest_tax_ratio": 0.333,
    "risk_band": "yellow",
    "risk_band_emoji": "🟡"
  },
  "headline": "利息支出佔稅收 33.3%，處於🟡 YELLOW 區"
}
```

## 欄位說明

### yield_stats

| 欄位 | 類型 | 說明 |
|------|------|------|
| tenor | string | 觀察期限（如 10Y） |
| latest | float | 最新殖利率（%） |
| zscore | float | Z-score（標準差距離） |
| percentile | float | 百分位數（0-1） |
| window_days | int | 分析視窗（交易日） |
| interpretation | string | 人類可讀解讀 |

### fiscal

| 欄位 | 類型 | 說明 |
|------|------|------|
| tax_revenue_jpy | int | 稅收（日圓） |
| interest_payments_jpy | int | 利息支出（日圓） |
| debt_stock_jpy | int | 債務存量（日圓） |
| interest_tax_ratio | float | 利息/稅收比 |
| risk_band | string | 風險分級（green/yellow/orange/red） |
| definition | object | 口徑定義 |

### stress_tests

| 欄位 | 類型 | 說明 |
|------|------|------|
| name | string | 情境名稱 |
| assumptions | object | 假設參數 |
| results | object | 壓測結果 |
| risk_band_year1 | string | Year 1 風險分級 |
| risk_band_year2 | string | Year 2 風險分級 |
