<overview>
穀物類 (Grains) 是 WASDE 報告的核心內容，包含小麥、玉米、稻米、大麥、高粱、燕麥。本文件詳細說明各穀物的表格結構、欄位映射與解析規則。
</overview>

<wheat>
**小麥 (Wheat)**

**表格名稱搜尋：**
```yaml
us_tables:
  - "U.S. Wheat Supply and Use"
  - "Wheat: U.S. Supply and Use"
  - "U.S. Wheat Supply and Disappearance"

us_by_class_tables:
  - "U.S. Wheat Supply and Use by Class"
  - "Wheat by Class: U.S. Supply and Use"

world_tables:
  - "World Wheat Supply and Use"
  - "Wheat: World Supply and Use"
```

**US 欄位映射：**
```yaml
fields_map:
  beginning_stocks: ["Beginning Stocks", "Beg. Stocks"]
  production: ["Production"]
  imports: ["Imports"]
  supply_total: ["Supply, Total", "Total Supply"]
  food: ["Food"]
  seed: ["Seed"]
  feed_and_residual: ["Feed and Residual", "Feed & Residual"]
  domestic_total: ["Domestic, Total", "Total Domestic"]
  exports: ["Exports"]
  use_total: ["Use, Total", "Total Use"]
  ending_stocks: ["Ending Stocks"]
  avg_farm_price: ["Avg. Farm Price", "Season-Average Farm Price"]
```

**US by-class 欄位：**
```yaml
wheat_classes:
  - hard_red_winter: ["Hard Red Winter", "HRW"]
  - hard_red_spring: ["Hard Red Spring", "HRS"]
  - soft_red_winter: ["Soft Red Winter", "SRW"]
  - white: ["White"]
  - durum: ["Durum"]

by_class_fields:
  beginning_stocks: ["Beginning Stocks"]
  production: ["Production"]
  imports: ["Imports"]
  food: ["Food"]
  seed: ["Seed"]
  feed_and_residual: ["Feed and Residual"]
  exports: ["Exports"]
  ending_stocks: ["Ending Stocks"]
```

**World 欄位映射：**
```yaml
fields_map:
  beginning_stocks: ["Beginning Stocks"]
  production: ["Production"]
  imports: ["Imports"]
  supply_total: ["Supply"]
  domestic_use: ["Domestic Use", "Dom. Consumption"]
  exports: ["Exports"]
  use_total: ["Use, Total"]
  ending_stocks: ["Ending Stocks"]

major_exporters:
  - united_states
  - canada
  - european_union
  - australia
  - argentina
  - russia
  - ukraine
  - kazakhstan

major_importers:
  - egypt
  - indonesia
  - algeria
  - philippines
  - japan
  - china
```

**單位：**
- US: million bushels
- World: million metric tons
- Price: $/bushel

**行銷年度：**
- US: June 1 - May 31
- World: July 1 - June 30
</wheat>

<corn>
**玉米 (Corn)**

**表格名稱搜尋：**
```yaml
us_tables:
  - "U.S. Feed Grain and Corn Supply and Use"
  - "Corn: U.S. Supply and Use"
  - "U.S. Corn Supply and Disappearance"

world_tables:
  - "World Corn Supply and Use"
  - "Corn: World Supply and Use"
  - "Coarse Grains: World Supply and Use"
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
  supply_total: ["Supply, Total"]
  feed_and_residual: ["Feed and Residual"]
  food_seed_industrial: ["Food, Seed, and Industrial", "FSI"]
  ethanol: ["Ethanol and by-products", "Ethanol"]
  domestic_total: ["Domestic, Total"]
  exports: ["Exports"]
  use_total: ["Use, Total"]
  ending_stocks: ["Ending Stocks"]
  avg_farm_price: ["Avg. Farm Price"]
```

**World 欄位映射：**
```yaml
fields_map:
  beginning_stocks: ["Beginning Stocks"]
  production: ["Production"]
  imports: ["Imports"]
  domestic_use: ["Domestic Use", "Feed Dom. Consumption"]
  exports: ["Exports"]
  ending_stocks: ["Ending Stocks"]

major_producers:
  - united_states
  - china
  - brazil
  - european_union
  - argentina
  - ukraine
  - mexico
```

**單位：**
- US: million bushels
- World: million metric tons
- Yield: bushels/acre
- Price: $/bushel

**行銷年度：**
- US: September 1 - August 31
- World: October 1 - September 30
</corn>

<rice>
**稻米 (Rice)**

**表格名稱搜尋：**
```yaml
us_tables:
  - "U.S. Rice Supply and Use"
  - "Rice: U.S. Supply and Use"

us_by_type_tables:
  - "U.S. Long-grain Rice Supply and Use"
  - "U.S. Medium/Short-grain Rice Supply and Use"

world_tables:
  - "World Rice Supply and Use"
  - "Rice: World Supply and Use"
```

**US 欄位映射：**
```yaml
fields_map:
  area_planted: ["Area Planted"]
  area_harvested: ["Area Harvested"]
  yield: ["Yield"]
  beginning_stocks: ["Beginning Stocks"]
  production: ["Production"]
  imports: ["Imports"]
  imports_long_grain: ["Long-grain Imports"]
  imports_med_short: ["Med./Short-grain Imports"]
  supply_total: ["Total Supply"]
  domestic_and_residual: ["Domestic and Residual"]
  exports: ["Exports"]
  use_total: ["Total Use"]
  ending_stocks: ["Ending Stocks"]
  avg_farm_price: ["Avg. Farm Price"]

rice_types:
  - long_grain: ["Long-grain", "Long Grain"]
  - medium_short_grain: ["Medium/Short-grain", "Med./Short-grain", "Medium and Short Grain"]
```

**World 欄位映射：**
```yaml
fields_map:
  beginning_stocks: ["Beginning Stocks"]
  production: ["Production"]
  imports: ["Imports"]
  domestic_use: ["Domestic Use", "Domestic Consumption"]
  exports: ["Exports"]
  ending_stocks: ["Ending Stocks"]

major_producers:
  - china
  - india
  - indonesia
  - bangladesh
  - vietnam
  - thailand
  - united_states
```

**單位：**
- US: million cwt (hundredweight)
- World: million metric tons (milled basis)
- Price: $/cwt

**行銷年度：**
- US: August 1 - July 31
- World: Calendar Year (January - December)
</rice>

<other_grains>
**其他穀物 (Barley, Sorghum, Oats)**

**大麥 (Barley):**
```yaml
tables:
  - "U.S. Barley Supply and Use"
  - "Barley: U.S. Supply and Use"

marketing_year: Jun-May
unit: million bushels

fields_map:
  beginning_stocks: ["Beginning Stocks"]
  production: ["Production"]
  imports: ["Imports"]
  food_alcohol_industrial: ["Food, Alcohol, and Industrial"]
  seed: ["Seed"]
  feed_and_residual: ["Feed and Residual"]
  exports: ["Exports"]
  ending_stocks: ["Ending Stocks"]
```

**高粱 (Sorghum):**
```yaml
tables:
  - "U.S. Sorghum Supply and Use"
  - "Sorghum: U.S. Supply and Use"

marketing_year: Sep-Aug
unit: million bushels

fields_map:
  beginning_stocks: ["Beginning Stocks"]
  production: ["Production"]
  imports: ["Imports"]
  feed_and_residual: ["Feed and Residual"]
  food_alcohol_industrial: ["Food, Alcohol, and Industrial"]
  exports: ["Exports"]
  ending_stocks: ["Ending Stocks"]
```

**燕麥 (Oats):**
```yaml
tables:
  - "U.S. Oats Supply and Use"
  - "Oats: U.S. Supply and Use"

marketing_year: Jun-May
unit: million bushels

fields_map:
  beginning_stocks: ["Beginning Stocks"]
  production: ["Production"]
  imports: ["Imports"]
  feed_and_residual: ["Feed and Residual"]
  food_and_industrial: ["Food and Industrial"]
  exports: ["Exports"]
  ending_stocks: ["Ending Stocks"]
```
</other_grains>

<validation_rules>
**穀物類驗證規則**

**平衡公式：**
```
Supply Total = Beginning Stocks + Production + Imports
Use Total = Domestic Total + Exports
Ending Stocks = Supply Total - Use Total
```

**合理性範圍 (US, million bushels)：**
```yaml
wheat:
  production: [1000, 3000]
  ending_stocks: [300, 1500]
  exports: [500, 1500]

corn:
  production: [10000, 18000]
  ending_stocks: [500, 3000]
  exports: [1500, 3000]
  ethanol: [4000, 6000]

rice:  # cwt
  production: [100, 300]
  ending_stocks: [20, 80]
```

**World 合理性範圍 (million metric tons)：**
```yaml
wheat:
  production: [700, 850]
  ending_stocks: [200, 350]

corn:
  production: [1000, 1300]
  ending_stocks: [200, 400]
```
</validation_rules>
