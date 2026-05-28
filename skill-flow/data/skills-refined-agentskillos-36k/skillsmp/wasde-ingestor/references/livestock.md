<overview>
畜產品 (Livestock) 僅涵蓋美國市場，包含牛肉、豬肉、禽肉、雞蛋、乳製品。本文件詳細說明表格結構、欄位映射與解析規則。
</overview>

<livestock_overview>
**畜產品總覽**

| 商品 | 英文 | 單位 | 年度 |
|------|------|------|------|
| 牛肉 | Beef | million lbs (carcass weight) | Calendar Year |
| 豬肉 | Pork | million lbs (carcass weight) | Calendar Year |
| 禽肉 | Broiler | million lbs (ready-to-cook) | Calendar Year |
| 火雞 | Turkey | million lbs (ready-to-cook) | Calendar Year |
| 雞蛋 | Eggs | million dozen | Calendar Year |
| 乳製品 | Dairy/Milk | billion lbs | Calendar Year |

**注意：** 畜產品僅有 US 數據，無 World 數據。
</livestock_overview>

<beef>
**牛肉 (Beef)**

**表格名稱搜尋：**
```yaml
tables:
  - "U.S. Beef Supply and Use"
  - "Beef: U.S. Supply and Use"
  - "U.S. Red Meat Supply and Use"  # 可能與豬肉合併
```

**欄位映射：**
```yaml
fields_map:
  beginning_stocks: ["Beginning Stocks", "Beg. Stocks"]
  commercial_production: ["Commercial Production", "Comm. Prod."]
  farm_production: ["Farm Production"]
  production_total: ["Production, Total", "Total Production"]
  imports: ["Imports"]
  supply_total: ["Supply, Total", "Total Supply"]
  exports: ["Exports"]
  domestic_use: ["Domestic Use", "Dom. Disappearance"]
  ending_stocks: ["Ending Stocks"]
  per_capita: ["Per Capita Disappearance", "Per Capita"]
  price_choice: ["Price, Choice", "Choice Beef Price"]
  price_all_fresh: ["Price, All Fresh", "All Fresh Beef"]
```

**單位：**
- 產量/庫存: million pounds (carcass weight)
- Per Capita: pounds/person
- Price: $/cwt

**特殊指標：**
- Cattle on Feed (存欄)
- Cattle Slaughter (屠宰)
- Average Carcass Weight
</beef>

<pork>
**豬肉 (Pork)**

**表格名稱搜尋：**
```yaml
tables:
  - "U.S. Pork Supply and Use"
  - "Pork: U.S. Supply and Use"
  - "U.S. Red Meat Supply and Use"
```

**欄位映射：**
```yaml
fields_map:
  beginning_stocks: ["Beginning Stocks"]
  commercial_production: ["Commercial Production"]
  farm_production: ["Farm Production"]
  production_total: ["Production, Total"]
  imports: ["Imports"]
  supply_total: ["Supply, Total"]
  exports: ["Exports"]
  domestic_use: ["Domestic Use"]
  ending_stocks: ["Ending Stocks"]
  per_capita: ["Per Capita Disappearance"]
  price_51_52: ["Price, 51-52%", "51-52% Lean"]
  price_national_base: ["National Base", "National Base Price"]
```

**單位：**
- 產量/庫存: million pounds (carcass weight)
- Per Capita: pounds/person
- Price: $/cwt

**特殊指標：**
- Hog Slaughter
- Average Carcass Weight
- Pigs per Litter
</pork>

<poultry>
**禽肉 (Poultry)**

**表格名稱搜尋：**
```yaml
broiler_tables:
  - "U.S. Broiler Supply and Use"
  - "Broiler: U.S. Supply and Use"

turkey_tables:
  - "U.S. Turkey Supply and Use"
  - "Turkey: U.S. Supply and Use"
```

**Broiler 欄位映射：**
```yaml
fields_map:
  beginning_stocks: ["Beginning Stocks"]
  production: ["Production"]
  imports: ["Imports"]
  supply_total: ["Supply, Total"]
  exports: ["Exports"]
  domestic_use: ["Domestic Use", "Ending Stocks + Domestic"]
  ending_stocks: ["Ending Stocks"]
  per_capita: ["Per Capita Disappearance"]
  price_wholesale: ["Price, Wholesale", "Wholesale Price"]
```

**Turkey 欄位映射：**
```yaml
fields_map:
  beginning_stocks: ["Beginning Stocks"]
  production: ["Production"]
  imports: ["Imports"]
  supply_total: ["Supply, Total"]
  exports: ["Exports"]
  domestic_use: ["Domestic Use"]
  ending_stocks: ["Ending Stocks"]
  per_capita: ["Per Capita Disappearance"]
  price_wholesale: ["Price, Wholesale"]
```

**單位：**
- 產量/庫存: million pounds (ready-to-cook weight)
- Per Capita: pounds/person
- Price: cents/lb

**特殊注意：**
- Broiler 生產週期短（6-7 週）
- 季節性：感恩節、聖誕節前需求高
</poultry>

<eggs>
**雞蛋 (Eggs)**

**表格名稱搜尋：**
```yaml
tables:
  - "U.S. Egg Supply and Use"
  - "Eggs: U.S. Supply and Use"
```

**欄位映射：**
```yaml
fields_map:
  production: ["Production"]
  imports: ["Imports"]
  supply_total: ["Supply, Total"]
  hatching_use: ["Hatching Use"]
  exports: ["Exports"]
  domestic_food: ["Domestic Food Use", "Food Use"]
  ending_stocks: ["Ending Stocks"]
  per_capita: ["Per Capita Disappearance"]
  price_ny: ["Price, New York", "NY Price"]
  price_midwest: ["Price, Midwest"]
```

**單位：**
- 產量: million dozen
- Per Capita: number of eggs/person
- Price: cents/dozen

**特殊分類：**
- Table Eggs (食用蛋)
- Hatching Eggs (孵化蛋)
- Breaking Stock (加工用蛋)
</eggs>

<dairy>
**乳製品 (Dairy/Milk)**

**表格名稱搜尋：**
```yaml
tables:
  - "U.S. Dairy Supply and Use"
  - "Milk: U.S. Supply and Use"
  - "U.S. Milk Production and Supply"
```

**欄位映射：**
```yaml
fields_map:
  milk_cows: ["Milk Cows", "Number of Cows"]
  milk_per_cow: ["Milk per Cow", "Production per Cow"]
  milk_production: ["Milk Production", "Total Production"]
  beginning_stocks: ["Beginning Stocks"]
  imports: ["Imports"]
  supply_total: ["Supply, Total"]
  domestic_use: ["Domestic Use", "Commercial Disappearance"]
  exports: ["Exports"]
  ending_stocks: ["Ending Stocks"]
  all_milk_price: ["All Milk Price"]
  class_iii_price: ["Class III Price"]
  class_iv_price: ["Class IV Price"]
```

**乳製品細分：**
```yaml
products:
  - butter: ["Butter"]
  - cheese: ["Cheese", "American Cheese", "Other Cheese"]
  - nonfat_dry_milk: ["Nonfat Dry Milk", "NDM"]
  - dry_whey: ["Dry Whey"]
```

**單位：**
- 牛奶產量: billion pounds
- 乳製品: million pounds
- Per Cow: pounds/year
- Price: $/cwt

**特殊指標：**
- Milk-Feed Price Ratio
- Class III/IV Prices (FMMO pricing)
</dairy>

<validation_rules>
**畜產品驗證規則**

**平衡公式：**
```
Supply Total = Beginning Stocks + Production + Imports
Use Total = Domestic Use + Exports
Ending Stocks = Supply Total - Use Total
```

**合理性範圍 (million pounds)：**
```yaml
beef:
  production: [25000, 30000]
  imports: [2000, 4000]
  exports: [2500, 4000]
  per_capita: [55, 62]

pork:
  production: [25000, 30000]
  imports: [500, 1000]
  exports: [6000, 8000]
  per_capita: [45, 55]

broiler:
  production: [42000, 50000]
  exports: [6000, 8000]
  per_capita: [90, 105]

eggs:  # million dozen
  production: [8000, 9500]
  per_capita: [275, 295]  # eggs per person

dairy:  # billion pounds milk
  production: [215, 235]
  milk_per_cow: [23000, 26000]  # pounds/year
```

**價格合理性：**
```yaml
beef_choice: [100, 250]  # $/cwt
pork_51_52: [40, 120]    # $/cwt
broiler_wholesale: [60, 150]  # cents/lb
egg_ny: [50, 300]        # cents/dozen
all_milk: [15, 30]       # $/cwt
```
</validation_rules>
