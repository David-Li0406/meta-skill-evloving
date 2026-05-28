<overview>
油籽類 (Oilseeds) 包含大豆、豆油、豆粕，是 WASDE 報告的重要組成部分。本文件詳細說明表格結構、欄位映射與解析規則。
</overview>

<soybeans>
**大豆 (Soybeans)**

**表格名稱搜尋：**
```yaml
us_tables:
  - "U.S. Soybeans Supply and Use"
  - "Soybeans: U.S. Supply and Use"
  - "U.S. Soybeans and Products Supply and Use"

world_tables:
  - "World Soybean Supply and Use"
  - "Soybeans: World Supply and Use"
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
  crushings: ["Crushings", "Crush"]
  exports: ["Exports"]
  seed: ["Seed"]
  residual: ["Residual"]
  use_total: ["Use, Total", "Total Use"]
  ending_stocks: ["Ending Stocks"]
  avg_farm_price: ["Avg. Farm Price", "Season-Average Farm Price"]
```

**World 欄位映射：**
```yaml
fields_map:
  beginning_stocks: ["Beginning Stocks"]
  production: ["Production"]
  imports: ["Imports"]
  crush: ["Crush", "Domestic Crush"]
  exports: ["Exports"]
  ending_stocks: ["Ending Stocks"]

major_producers:
  - united_states
  - brazil
  - argentina
  - china
  - india
  - paraguay

major_exporters:
  - brazil
  - united_states
  - argentina
  - paraguay
  - canada

major_importers:
  - china  # 占全球進口 60%+
  - european_union
  - mexico
  - japan
  - egypt
```

**單位：**
- US: million bushels
- World: million metric tons
- Yield: bushels/acre
- Price: $/bushel

**行銷年度：**
- US: September 1 - August 31
- World: October 1 - September 30

**特殊注意：**
- 中國進口量是關鍵觀察指標
- Brazil 與 US 的出口競爭關係
- 南美收成季（3-5月）影響 World 供需
</soybeans>

<soybean_oil>
**豆油 (Soybean Oil)**

**表格名稱搜尋：**
```yaml
us_tables:
  - "U.S. Soybean Oil Supply and Use"
  - "Soybean Oil: U.S. Supply and Use"
  - "U.S. Soybean Oil Supply and Disappearance"

world_tables:
  - "World Soybean Oil Supply and Use"
  - "Soybean Oil: World Supply and Use"
```

**US 欄位映射：**
```yaml
fields_map:
  beginning_stocks: ["Beginning Stocks"]
  production: ["Production"]
  imports: ["Imports"]
  supply_total: ["Supply, Total"]
  domestic_disappearance: ["Domestic Disappearance", "Domestic Use"]
  biofuel: ["Biofuel", "Biodiesel"]  # 2021 年後改名
  food_feed_other: ["Food, Feed, and Other Industrial"]
  exports: ["Exports"]
  use_total: ["Use, Total"]
  ending_stocks: ["Ending Stocks"]
  price: ["Price", "Avg. Price"]
```

**World 欄位映射：**
```yaml
fields_map:
  beginning_stocks: ["Beginning Stocks"]
  production: ["Production"]
  imports: ["Imports"]
  domestic_use: ["Domestic Use", "Dom. Consumption"]
  exports: ["Exports"]
  ending_stocks: ["Ending Stocks"]
```

**單位：**
- US: million pounds
- World: million metric tons
- Price: cents/pound

**行銷年度：** October 1 - September 30

**特殊注意：**
- Biofuel 需求是重要驅動因素
- 2021 年後 "Biodiesel" 改為 "Biofuel"
</soybean_oil>

<soybean_meal>
**豆粕 (Soybean Meal)**

**表格名稱搜尋：**
```yaml
us_tables:
  - "U.S. Soybean Meal Supply and Use"
  - "Soybean Meal: U.S. Supply and Use"

world_tables:
  - "World Soybean Meal Supply and Use"
  - "Soybean Meal: World Supply and Use"
```

**US 欄位映射：**
```yaml
fields_map:
  beginning_stocks: ["Beginning Stocks"]
  production: ["Production"]
  imports: ["Imports"]
  supply_total: ["Supply, Total"]
  domestic_disappearance: ["Domestic Disappearance"]
  exports: ["Exports"]
  use_total: ["Use, Total"]
  ending_stocks: ["Ending Stocks"]
  price: ["Price", "Avg. Price"]
```

**World 欄位映射：**
```yaml
fields_map:
  beginning_stocks: ["Beginning Stocks"]
  production: ["Production"]
  imports: ["Imports"]
  domestic_use: ["Domestic Use"]
  exports: ["Exports"]
  ending_stocks: ["Ending Stocks"]

# 2021 年後 China 單獨列出
major_countries:
  - china  # 單獨列出
  - argentina
  - brazil
  - united_states
  - european_union
```

**單位：**
- US: thousand short tons
- World: million metric tons
- Price: $/short ton

**行銷年度：** October 1 - September 30
</soybean_meal>

<crush_relationship>
**壓榨關係 (Crush Relationship)**

大豆壓榨產出豆油與豆粕，有固定的產出比例：

```
1 bushel soybeans (60 lbs) ≈
  - 11 lbs soybean oil (18.3%)
  - 48 lbs soybean meal (80%)
  - 1 lb hulls & loss (1.7%)
```

**換算公式：**
```python
# US 單位換算
soybean_bushels_crushed = soybean_meal_production_tons * 2000 / 48 / 60
# 或
soybean_bushels_crushed = soybean_oil_production_lbs / 11 / 60
```

**驗證規則：**
- 豆粕產量 ≈ 壓榨量 * 0.80
- 豆油產量 ≈ 壓榨量 * 0.183
- 容許 5% 誤差（不同大豆品種含油量不同）
</crush_relationship>

<validation_rules>
**油籽類驗證規則**

**平衡公式：**
```
Supply Total = Beginning Stocks + Production + Imports
Use Total = Crush + Exports + Seed + Residual
Ending Stocks = Supply Total - Use Total
```

**合理性範圍 (US)：**
```yaml
soybeans:  # million bushels
  production: [3500, 5000]
  crush: [2000, 2500]
  exports: [1500, 2500]
  ending_stocks: [100, 600]

soybean_oil:  # million pounds
  production: [20000, 28000]
  biofuel: [8000, 14000]
  exports: [500, 2000]

soybean_meal:  # thousand short tons
  production: [45000, 60000]
  exports: [10000, 16000]
```

**World 合理性範圍 (million metric tons)：**
```yaml
soybeans:
  production: [350, 450]
  crush: [300, 400]
  ending_stocks: [80, 150]
  china_imports: [90, 120]  # 關鍵指標
```

**跨表驗證：**
- US Soybean Crush ≈ 計算自 Soybean Meal Production
- World 各國加總 ≈ World Total
</validation_rules>
