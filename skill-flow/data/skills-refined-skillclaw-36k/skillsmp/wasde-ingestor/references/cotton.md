<overview>
棉花 (Cotton) 是 WASDE 報告涵蓋的重要纖維作物。本文件詳細說明 US 與 World 棉花表格的結構、欄位映射與解析規則。
</overview>

<cotton_types>
**棉花類型**

| 類型 | 英文 | 說明 |
|------|------|------|
| 陸地棉 | Upland Cotton | 占美國產量 97%，主要短纖維棉 |
| 匹馬棉 | Pima / ELS Cotton | Extra Long Staple，高品質長纖維棉 |
| 全棉花 | All Cotton | Upland + Pima 合計 |
</cotton_types>

<us_cotton>
**US 棉花供需**

**表格名稱搜尋：**
```yaml
us_tables:
  - "U.S. Cotton Supply and Use"
  - "Cotton: U.S. Supply and Use"
  - "U.S. Upland Cotton Supply and Use"
  - "U.S. All Cotton Supply and Use"

us_pima_tables:
  - "U.S. Pima Cotton Supply and Use"
  - "U.S. Extra-Long Staple Cotton Supply and Use"
```

**US 欄位映射：**
```yaml
fields_map:
  area_planted: ["Area Planted"]
  area_harvested: ["Area Harvested"]
  yield: ["Yield per Harvested Acre"]
  beginning_stocks: ["Beginning Stocks"]
  production: ["Production"]
  imports: ["Imports"]
  supply_total: ["Supply, Total", "Total Supply"]
  mill_use: ["Mill Use", "Domestic Mill Use"]
  exports: ["Exports"]
  use_total: ["Use, Total", "Total Use"]
  unaccounted: ["Unaccounted"]
  ending_stocks: ["Ending Stocks"]
  avg_farm_price: ["Avg. Farm Price", "Upland Farm Price"]
  a_index: ["A Index", "Cotlook A Index"]
```

**區域細分（可選）：**
```yaml
regions:
  southeast: ["Southeast", "GA", "NC", "SC", "VA", "AL"]
  delta: ["Delta", "MS", "AR", "LA", "TN", "MO"]
  southwest: ["Southwest", "TX", "OK", "KS"]
  west: ["West", "CA", "AZ", "NM"]
```

**單位：**
- 面積: million acres
- 產量: million 480-lb bales
- 單產: pounds/acre
- 價格: cents/pound

**行銷年度：** August 1 - July 31
</us_cotton>

<world_cotton>
**World 棉花供需**

**表格名稱搜尋：**
```yaml
world_tables:
  - "World Cotton Supply and Use"
  - "Cotton: World Supply and Use"
  - "World Cotton Supply and Distribution"
```

**World 欄位映射：**
```yaml
fields_map:
  beginning_stocks: ["Beginning Stocks"]
  production: ["Production"]
  imports: ["Imports"]
  mill_use: ["Mill Use", "Mill Consumption"]
  exports: ["Exports"]
  loss_adjustment: ["Loss Adjustment", "Statistical Discrepancy"]
  ending_stocks: ["Ending Stocks"]
  stocks_to_use: ["Stocks-to-Use Ratio"]
```

**主要生產國：**
```yaml
major_producers:
  - india: ["India"]
  - china: ["China"]
  - united_states: ["United States", "USA"]
  - brazil: ["Brazil"]
  - pakistan: ["Pakistan"]
  - australia: ["Australia"]
  - turkey: ["Turkey"]
  - uzbekistan: ["Uzbekistan"]
```

**主要消費國（Mill Use）：**
```yaml
major_consumers:
  - china: ["China"]  # 全球最大
  - india: ["India"]
  - pakistan: ["Pakistan"]
  - bangladesh: ["Bangladesh"]
  - vietnam: ["Vietnam"]
  - turkey: ["Turkey"]
```

**主要出口國：**
```yaml
major_exporters:
  - united_states: ["United States"]
  - brazil: ["Brazil"]
  - australia: ["Australia"]
  - india: ["India"]
```

**單位：**
- 產量/消費/庫存: million 480-lb bales
- Stocks-to-Use: percentage

**行銷年度：** August 1 - July 31 (全球統一)
</world_cotton>

<price_indices>
**棉花價格指標**

| 指標 | 說明 | 單位 |
|------|------|------|
| Upland Farm Price | 美國陸地棉農場價格 | cents/lb |
| Cotlook A Index | 全球遠東交貨價格指標 | cents/lb |
| ICE Cotton #2 | 紐約棉花期貨 | cents/lb |
| CC Index | 中國棉花指數 | CNY/ton |

**A Index 與 Farm Price 關係：**
- A Index 通常高於 Farm Price
- 價差反映運輸、品質溢價
</price_indices>

<validation_rules>
**棉花驗證規則**

**平衡公式：**
```
Ending Stocks = Beginning Stocks + Production + Imports - Mill Use - Exports - Loss
```

**US 合理性範圍 (million 480-lb bales)：**
```yaml
upland:
  production: [10, 20]
  mill_use: [2, 4]
  exports: [10, 18]
  ending_stocks: [2, 8]

pima:
  production: [0.3, 1.0]
  mill_use: [0.1, 0.3]
  exports: [0.3, 0.8]
```

**World 合理性範圍 (million 480-lb bales)：**
```yaml
world:
  production: [100, 130]
  mill_use: [100, 130]
  ending_stocks: [70, 110]
  stocks_to_use: [60, 100]  # percentage

china:
  production: [25, 35]
  mill_use: [35, 45]
  imports: [5, 15]
  ending_stocks: [30, 50]

india:
  production: [25, 35]
  mill_use: [20, 30]
```

**特殊檢查：**
- World Mill Use ≈ World Production (長期)
- China Imports ≈ China Mill Use - China Production
- US Exports 占 World Trade 約 30-40%
</validation_rules>

<seasonal_patterns>
**棉花季節性模式**

| 月份 | 北半球 | 南半球 |
|------|--------|--------|
| 1-3月 | 淡季 | 收成 (Brazil, Australia) |
| 4-6月 | 種植 | 淡季 |
| 7-9月 | 生長 | 淡季 |
| 10-12月 | 收成 (US) | 種植 |

**關鍵報告月份：**
- 5月 WASDE: 首次發布新年度預測
- 8月 WASDE: 首次產量預估
- 1月 WASDE: 最終產量確認
</seasonal_patterns>
