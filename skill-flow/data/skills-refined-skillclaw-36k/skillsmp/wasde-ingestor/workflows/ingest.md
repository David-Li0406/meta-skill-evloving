<required_reading>
**執行此工作流程前，請先閱讀：**
1. references/commodities-overview.md - 了解商品範圍與單位
2. references/validation-rules.md - 了解驗證規則
3. references/failure-modes.md - 了解失敗處理
4. 根據指定商品，閱讀對應的參考文件（grains.md, oilseeds.md 等）
</required_reading>

<objective>
抓取並解析最新或指定月份的 WASDE 報告，提取指定商品的供需數據。
</objective>

<process>
**Step 1: 確認參數**

詢問或確認以下參數：

```yaml
parameters:
  commodities:
    description: "要抓取的商品"
    options:
      - all          # 所有商品
      - grains       # Wheat, Corn, Rice, Barley, Sorghum, Oats
      - oilseeds     # Soybeans, Soybean Oil, Soybean Meal
      - cotton       # Cotton
      - livestock    # Beef, Pork, Broiler, Turkey, Eggs, Dairy
      - sugar        # US & Mexico Sugar
      - [specific]   # 指定單一商品，如 "corn", "soybeans"
    default: "all"

  scope:
    description: "數據範圍"
    options: ["us", "world", "us,world"]
    default: "us,world"

  release_date:
    description: "報告發布日期"
    format: "YYYY-MM-DD"
    default: "latest"  # 抓取最新

  output_dir:
    description: "輸出目錄"
    default: "./data/wasde"
```

**Step 2: 發現報告 URL**

```python
# 使用 scripts/discover_releases.py
from scripts.discover_releases import discover_latest_release, discover_by_date

if release_date == "latest":
    release_info = discover_latest_release()
else:
    release_info = discover_by_date(release_date)

# release_info 包含:
# - release_date: "2025-01-10"
# - pdf_url: "https://www.usda.gov/oce/commodity/wasde/wasde0125.pdf"
# - html_url: "https://www.usda.gov/oce/commodity/wasde/"
```

**Step 3: 下載報告**

```python
# 使用 scripts/fetch_report.py
from scripts.fetch_report import fetch_pdf, fetch_html

# 嘗試下載 PDF
pdf_path = fetch_pdf(
    url=release_info['pdf_url'],
    output_dir=f"{output_dir}/raw/{release_info['release_date']}",
    retry_config={
        "max_attempts": 5,
        "backoff": [1, 2, 4, 8, 16]
    }
)

# 如果 PDF 失敗，嘗試 HTML
if not pdf_path and config.allow_fallback:
    html_content = fetch_html(release_info['html_url'])
```

**Step 4: 解析表格**

```python
# 使用 scripts/parse_tables.py
from scripts.parse_tables import parse_wasde_pdf, parse_wasde_html

# 根據商品配置決定要解析的表格
tables_to_parse = get_tables_for_commodities(commodities, scope)

# 解析
if pdf_path:
    parsed_data = parse_wasde_pdf(
        pdf_path=pdf_path,
        tables=tables_to_parse,
        fuzzy_match=True,
        fuzzy_threshold=0.8
    )
else:
    parsed_data = parse_wasde_html(
        html_content=html_content,
        tables=tables_to_parse
    )
```

**Step 5: 標準化數據**

```python
# 標準化欄位名稱
def normalize_fields(raw_data, commodity):
    """使用欄位映射標準化"""
    field_map = load_field_map(commodity)  # 從 references 載入

    normalized = {}
    for raw_field, value in raw_data.items():
        standard_field = map_field(raw_field, field_map)
        if standard_field:
            normalized[standard_field] = value

    return normalized

# 標準化單位
def normalize_units(data, commodity, scope):
    """確保單位一致"""
    expected_unit = get_expected_unit(commodity, scope)
    data['unit'] = expected_unit
    return data

# 計算衍生欄位
def compute_derived_fields(data):
    """計算 stocks_to_use 等衍生欄位"""
    if data.get('ending_stocks') and data.get('total_use'):
        data['stocks_to_use'] = data['ending_stocks'] / data['total_use']
    return data
```

**Step 6: 驗證數據**

```python
# 使用 scripts/validate_data.py
from scripts.validate_data import (
    validate_balance,
    validate_range,
    validate_schema
)

validation_results = []

for commodity, data in normalized_data.items():
    # 平衡公式檢查
    balance_ok = validate_balance(data, tolerance=get_tolerance(commodity))

    # 數值範圍檢查
    range_ok = validate_range(data, commodity)

    # Schema 檢查
    schema_ok = validate_schema(data, commodity)

    validation_results.append({
        "commodity": commodity,
        "balance_check": balance_ok,
        "range_check": range_ok,
        "schema_check": schema_ok,
        "overall": balance_ok and range_ok and schema_ok
    })
```

**Step 7: 計算 Content Hash**

```python
import hashlib
import json

def compute_content_hash(row):
    """計算數據行的 content hash"""
    # 排除 metadata 欄位
    exclude = ['content_hash', 'created_at', 'updated_at']
    data = {k: v for k, v in row.items() if k not in exclude}

    # 處理浮點數精度
    for k, v in data.items():
        if isinstance(v, float):
            data[k] = round(v, 6)

    content_str = json.dumps(data, sort_keys=True, default=str)
    return hashlib.sha256(content_str.encode()).hexdigest()[:32]
```

**Step 8: 寫入輸出**

```python
import pandas as pd

# 建立輸出目錄結構
output_paths = {
    "raw": f"{output_dir}/raw/{release_date}",
    "intermediate": f"{output_dir}/intermediate/{release_date}",
    "curated": f"{output_dir}/curated"
}

# 寫入中間文件
with open(f"{output_paths['intermediate']}/tables.json", 'w') as f:
    json.dump(parsed_data, f, indent=2)

# 寫入 curated parquet
for commodity, data in curated_data.items():
    df = pd.DataFrame([data])
    df['release_date'] = release_date
    df['content_hash'] = compute_content_hash(data)

    parquet_path = f"{output_paths['curated']}/{commodity}_balance.parquet"

    # Append 或 create
    if os.path.exists(parquet_path):
        existing = pd.read_parquet(parquet_path)
        df = pd.concat([existing, df]).drop_duplicates(
            subset=['release_date', 'marketing_year', 'commodity'],
            keep='last'
        )

    df.to_parquet(parquet_path, index=False)
```

**Step 9: 生成狀態報告**

```python
# 生成 ingest_status
ingest_status = {
    "release_date": release_date,
    "success": all(v['overall'] for v in validation_results),
    "commodities_processed": list(curated_data.keys()),
    "warnings": collect_warnings(),
    "errors": collect_errors(),
    "rows_written": {c: 1 for c in curated_data.keys()},
    "timing_ms": {
        "fetch": fetch_time_ms,
        "parse": parse_time_ms,
        "validate": validate_time_ms,
        "write": write_time_ms
    }
}

# 寫入狀態文件
with open(f"{output_paths['intermediate']}/ingest_status.json", 'w') as f:
    json.dump(ingest_status, f, indent=2)
```
</process>

<success_criteria>
此工作流程成功完成時：
- [ ] 成功下載 WASDE 報告（PDF 或 HTML）
- [ ] 解析所有指定商品的表格
- [ ] 所有數據通過平衡公式驗證
- [ ] 所有數據通過數值範圍檢查
- [ ] 輸出 curated parquet 文件
- [ ] 生成 ingest_status.json 且 success=true
- [ ] 無 error 級別的日誌
</success_criteria>

<error_handling>
**錯誤處理：**

1. **網路錯誤** → 重試最多 5 次，指數退避
2. **PDF 解析失敗** → 嘗試 HTML fallback
3. **表格未找到** → 使用模糊匹配，記錄警告
4. **驗證失敗** → 根據配置決定是輸出部分數據還是完全失敗
5. **Schema Drift** → 記錄詳細報告，通知維護者

參見 references/failure-modes.md 了解完整的錯誤處理策略。
</error_handling>
