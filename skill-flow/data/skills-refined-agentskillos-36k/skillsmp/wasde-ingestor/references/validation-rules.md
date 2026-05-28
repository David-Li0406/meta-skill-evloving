<overview>
本文件定義 WASDE 數據解析的通用驗證規則，包含平衡公式檢查、數值合理性範圍、跨表一致性驗證等。
</overview>

<balance_formula>
**供需平衡公式**

所有供需表遵循相同的基本平衡公式：

```
Supply = Beginning Stocks + Production + Imports
Use = Domestic Use + Exports
Ending Stocks = Supply - Use
```

**驗證方式：**
```python
def validate_balance(row, tolerance=1.0):
    supply = row['beginning_stocks'] + row['production'] + row['imports']
    use = row['domestic_total'] + row['exports']
    calculated_ending = supply - use

    actual_ending = row['ending_stocks']
    diff = abs(calculated_ending - actual_ending)

    return diff <= tolerance
```

**容許誤差：**
| 商品類別 | US 容許誤差 | World 容許誤差 |
|----------|------------|---------------|
| Grains | 5.0 (million bu) | 1.0 (mmt) |
| Oilseeds | 5.0 (million bu) | 1.0 (mmt) |
| Cotton | 0.1 (million bales) | 0.5 (million bales) |
| Livestock | 50.0 (million lbs) | N/A |
| Sugar | 50.0 (1000 st) | N/A |

**誤差來源：**
- 四捨五入
- Residual / Unaccounted 項目
- Statistical discrepancy
</balance_formula>

<numeric_sanity>
**數值合理性檢查**

**原則：**
1. 數值必須為非負數（除特定例外）
2. 數值必須在歷史合理範圍內
3. 年度變化幅度不應異常

**允許負值的欄位：**
```yaml
allow_negative:
  - feed_and_residual  # 統計殘差可能為負
  - unaccounted        # 統計殘差
  - loss_adjustment    # 損失調整
  - residual           # 殘差項
```

**異常值檢測：**
```python
def check_anomaly(value, historical_mean, historical_std, threshold=3.0):
    """檢測是否超過 3 個標準差"""
    z_score = abs(value - historical_mean) / historical_std
    return z_score > threshold
```

**年度變化限制：**
```yaml
max_yoy_change:
  production: 30%      # 產量年變化不超過 30%
  ending_stocks: 100%  # 庫存可能大幅波動
  exports: 50%         # 出口變化較大
  domestic_use: 20%    # 國內消費較穩定
```
</numeric_sanity>

<cross_table_validation>
**跨表一致性驗證**

**World 加總驗證：**
```python
def validate_world_total(country_data, world_total, tolerance_pct=2.0):
    """各國加總應等於 World Total"""
    calculated_total = sum(country_data.values())
    diff_pct = abs(calculated_total - world_total) / world_total * 100
    return diff_pct <= tolerance_pct
```

**油籽壓榨關係：**
```python
def validate_crush_relationship(soybean_crush, meal_production, oil_production):
    """壓榨量與產品產量的對應關係"""
    # 1 bushel = 60 lbs → 48 lbs meal + 11 lbs oil
    expected_meal = soybean_crush * 60 * 0.80 / 2000  # thousand short tons
    expected_oil = soybean_crush * 60 * 0.183  # million pounds

    meal_diff = abs(meal_production - expected_meal) / expected_meal
    oil_diff = abs(oil_production - expected_oil) / expected_oil

    return meal_diff < 0.10 and oil_diff < 0.10  # 10% 容許
```

**US-Mexico 糖貿易對賬：**
```python
def validate_sugar_trade(us_imports_from_mexico, mexico_exports_to_us):
    """US 進口 ≈ Mexico 出口（單位換算後）"""
    # US: 1000 short tons → Mexico: 1000 metric tons
    us_in_mt = us_imports_from_mexico * 0.9072
    diff_pct = abs(us_in_mt - mexico_exports_to_us) / mexico_exports_to_us * 100
    return diff_pct < 5.0
```
</cross_table_validation>

<schema_validation>
**Schema 驗證**

**必要欄位檢查：**
```yaml
required_fields:
  all_balance_tables:
    - release_date
    - marketing_year
    - commodity
    - unit
    - beginning_stocks
    - production
    - imports
    - exports
    - ending_stocks
    - content_hash

  grains_us:
    - area_planted
    - area_harvested
    - yield
    - avg_farm_price

  oilseeds_us:
    - crushings
    - seed
    - residual

  cotton_us:
    - mill_use
    - unaccounted

  livestock_us:
    - commercial_production
    - per_capita
```

**資料類型驗證：**
```yaml
field_types:
  release_date: date
  marketing_year: string  # "2024/25" format
  commodity: string
  unit: string
  numeric_fields: float
  content_hash: string (SHA256)
```

**Marketing Year 格式：**
```python
import re

def validate_marketing_year(my_str):
    """驗證行銷年度格式"""
    pattern = r'^\d{4}/\d{2}$'  # "2024/25"
    return bool(re.match(pattern, my_str))
```
</schema_validation>

<drift_detection>
**Schema Drift 檢測**

**表格結構變化檢測：**
```python
def detect_schema_drift(current_columns, baseline_columns):
    """檢測表格結構是否變化"""
    added = set(current_columns) - set(baseline_columns)
    removed = set(baseline_columns) - set(current_columns)

    if added or removed:
        return {
            "drift_detected": True,
            "added_columns": list(added),
            "removed_columns": list(removed)
        }
    return {"drift_detected": False}
```

**Schema Hash：**
```python
import hashlib
import json

def compute_schema_hash(columns, dtypes):
    """計算 schema 的 hash 值"""
    schema_str = json.dumps({
        "columns": sorted(columns),
        "dtypes": {k: str(v) for k, v in sorted(dtypes.items())}
    }, sort_keys=True)
    return hashlib.sha256(schema_str.encode()).hexdigest()[:16]
```

**Drift 處理策略：**
```yaml
on_drift:
  minor:  # 新增欄位
    action: "warn_and_continue"
    log_level: "warning"

  major:  # 刪除欄位或重命名
    action: "fail_with_report"
    log_level: "error"
    output: "drift_report.json"
```
</drift_detection>

<content_hash>
**Content Hash 計算**

**目的：**
- 追蹤數據變化
- 識別修正值
- 確保冪等性

**計算方式：**
```python
import hashlib
import json

def compute_content_hash(row_dict, exclude_fields=None):
    """計算行數據的 content hash"""
    exclude = exclude_fields or ['content_hash', 'created_at', 'updated_at']

    # 只包含數據欄位
    data = {k: v for k, v in sorted(row_dict.items()) if k not in exclude}

    # 處理浮點數精度
    for k, v in data.items():
        if isinstance(v, float):
            data[k] = round(v, 6)

    content_str = json.dumps(data, sort_keys=True, default=str)
    return hashlib.sha256(content_str.encode()).hexdigest()[:32]
```

**修正值識別：**
```python
def detect_revision(new_hash, old_hash, release_date, old_release_date):
    """識別數據修正"""
    if new_hash != old_hash:
        return {
            "is_revision": True,
            "new_release": release_date,
            "old_release": old_release_date,
            "new_hash": new_hash,
            "old_hash": old_hash
        }
    return {"is_revision": False}
```
</content_hash>

<quality_metrics>
**數據品質指標**

```yaml
quality_metrics:
  completeness:
    description: "必要欄位的填充率"
    threshold: 0.95  # 95% 以上

  accuracy:
    description: "平衡公式驗證通過率"
    threshold: 0.99  # 99% 以上

  consistency:
    description: "跨表數據一致性"
    threshold: 0.95

  timeliness:
    description: "數據更新及時性"
    threshold: "release_date + 1 day"

  uniqueness:
    description: "無重複記錄"
    threshold: 1.0  # 100%
```

**品質報告輸出：**
```python
def generate_quality_report(df, checks):
    """生成數據品質報告"""
    return {
        "total_rows": len(df),
        "valid_rows": sum(checks),
        "quality_score": sum(checks) / len(checks) * 100,
        "issues": [
            {"row": i, "reason": "balance_check_failed"}
            for i, passed in enumerate(checks) if not passed
        ]
    }
```
</quality_metrics>
