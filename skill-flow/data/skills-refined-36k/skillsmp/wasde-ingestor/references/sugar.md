<overview>
糖 (Sugar) 在 WASDE 中涵蓋美國與墨西哥市場。本文件詳細說明表格結構、欄位映射與解析規則。
</overview>

<sugar_overview>
**糖市場總覽**

| 市場 | 說明 | 單位 |
|------|------|------|
| US Sugar | 美國糖供需 | 1,000 short tons (raw value) |
| Mexico Sugar | 墨西哥糖供需 | 1,000 metric tons |

**糖類型：**
- Raw Sugar (原糖)
- Refined Sugar (精製糖)
- Beet Sugar (甜菜糖)
- Cane Sugar (甘蔗糖)
- High Fructose Corn Syrup (HFCS，玉米糖漿)
</sugar_overview>

<us_sugar>
**US 糖供需**

**表格名稱搜尋：**
```yaml
tables:
  - "U.S. Sugar Supply and Use"
  - "Sugar: U.S. Supply and Use"
  - "U.S. Sugar Supply and Use/Prices"
```

**欄位映射：**
```yaml
fields_map:
  beginning_stocks: ["Beginning Stocks"]

  # Production 細分
  beet_sugar: ["Beet Sugar"]
  cane_sugar_florida: ["Cane Sugar, Florida", "Florida Cane"]
  cane_sugar_louisiana: ["Cane Sugar, Louisiana", "Louisiana Cane"]
  cane_sugar_texas: ["Cane Sugar, Texas", "Texas Cane"]
  cane_sugar_hawaii: ["Cane Sugar, Hawaii", "Hawaii Cane"]  # 已減少
  production_total: ["Production, Total", "Total Production"]

  # Imports 細分
  imports_tariff_rate_quota: ["TRQ Imports", "Tariff-Rate Quota"]
  imports_other: ["Other Program Imports"]
  imports_high_tier: ["High-Tier Tariff Imports"]
  imports_total: ["Imports, Total", "Total Imports"]

  supply_total: ["Supply, Total"]

  exports: ["Exports"]
  deliveries_domestic: ["Deliveries, Domestic Food and Beverage"]
  deliveries_other: ["Other Deliveries"]
  miscellaneous: ["Miscellaneous"]
  use_total: ["Use, Total"]

  ending_stocks: ["Ending Stocks"]
  stocks_to_use: ["Stocks-to-Use Ratio"]

  # Prices
  raw_sugar_price: ["Raw Sugar Price", "Raw Cane Sugar Price"]
  refined_sugar_price: ["Refined Beet Sugar Price", "Refined Sugar Price"]
  world_raw_price: ["World Raw Sugar Price", "World Price"]
```

**單位：**
- 供需量: 1,000 short tons (raw value)
- Stocks-to-Use: percentage
- Price: cents/lb

**行銷年度：** October 1 - September 30

**特殊注意：**
- US 實施關稅配額 (TRQ) 制度
- Mexico 根據北美貿易協定有特殊進口待遇
</us_sugar>

<mexico_sugar>
**Mexico 糖供需**

**表格名稱搜尋：**
```yaml
tables:
  - "Mexico Sugar Supply and Use"
  - "Sugar: Mexico Supply and Use"
```

**欄位映射：**
```yaml
fields_map:
  beginning_stocks: ["Beginning Stocks"]
  production: ["Production"]
  imports: ["Imports"]
  supply_total: ["Supply, Total"]
  domestic_use: ["Domestic Consumption", "Domestic Use"]
  exports_to_us: ["Exports to United States", "Exports to US"]
  exports_other: ["Exports, Other", "Other Exports"]
  exports_total: ["Exports, Total"]
  use_total: ["Use, Total"]
  ending_stocks: ["Ending Stocks"]
```

**單位：**
- 供需量: 1,000 metric tons

**行銷年度：** October 1 - September 30

**特殊注意：**
- Mexico 是 US 最大的糖進口來源
- 受 USMCA (前 NAFTA) 貿易協定規範
</mexico_sugar>

<hfcs>
**高果糖玉米糖漿 (HFCS)**

WASDE 通常不單獨列出 HFCS 表格，但在 US Sugar 市場分析中需考慮：

```yaml
hfcs_context:
  - HFCS 是糖的主要替代品
  - 玉米價格影響 HFCS 生產成本
  - 飲料產業是主要消費者
  - 近年 HFCS 消費量下降
```
</hfcs>

<trade_policy>
**美國糖政策**

**關稅配額 (TRQ) 制度：**
```yaml
trq_system:
  description: "美國對糖進口實施二級關稅制度"

  in_quota:
    description: "配額內進口，低關稅"
    tariff: "0.625 cents/lb (raw)"

  over_quota:
    description: "超配額進口，高關稅"
    tariff: "15.36 cents/lb (raw)"

  country_allocations:
    - dominican_republic
    - brazil
    - philippines
    - australia
    - guatemala
    - others
```

**Mexico 特殊待遇：**
```yaml
mexico_access:
  description: "根據 USMCA，Mexico 有特殊進口待遇"
  provisions:
    - "Need-based access"
    - "Export limit agreements"
    - "Refined sugar restrictions"
```
</trade_policy>

<validation_rules>
**糖驗證規則**

**平衡公式：**
```
Supply Total = Beginning Stocks + Production + Imports
Use Total = Domestic Use + Exports
Ending Stocks = Supply Total - Use Total
```

**US 合理性範圍 (1,000 short tons)：**
```yaml
us_sugar:
  beet_sugar: [4000, 5500]
  cane_sugar: [3500, 4500]
  production_total: [8000, 10000]
  imports_total: [2500, 4000]
  domestic_deliveries: [11000, 13000]
  ending_stocks: [1200, 2200]
  stocks_to_use: [10, 18]  # percentage

prices:  # cents/lb
  raw_sugar: [20, 50]
  refined_sugar: [30, 70]
  world_raw: [10, 30]
```

**Mexico 合理性範圍 (1,000 metric tons)：**
```yaml
mexico_sugar:
  production: [5500, 7000]
  domestic_use: [4000, 5000]
  exports_to_us: [1000, 2000]
  ending_stocks: [500, 1500]
```

**跨表驗證：**
- US Imports from Mexico ≈ Mexico Exports to US (單位換算後)
- World Price 通常低於 US Price (因為保護政策)
</validation_rules>

<seasonal_patterns>
**糖季節性模式**

| 月份 | US 甜菜 | US 甘蔗 | Mexico |
|------|---------|---------|--------|
| 1-3月 | 淡季 | 收割 (FL, LA) | 收割 |
| 4-6月 | 種植 | 淡季 | 收割尾聲 |
| 7-9月 | 生長 | 淡季 | 淡季 |
| 10-12月 | 收割 | 開始收割 | 淡季 |

**關鍵報告月份：**
- 5月 WASDE: 新年度首次預測
- 11月 WASDE: 甜菜產量更新
- 1月 WASDE: 甘蔗產量更新
</seasonal_patterns>
