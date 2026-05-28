<required_reading>
**執行此工作流程前，請先閱讀：**
1. references/validation-rules.md - 了解驗證規則
2. references/failure-modes.md - 了解錯誤處理
</required_reading>

<objective>
驗證現有 WASDE 數據的一致性，識別數據修正，並與最新報告進行比對。
</objective>

<process>
**Step 1: 確認驗證模式**

```yaml
validation_modes:
  integrity:
    description: "檢查現有數據的完整性與一致性"
    checks:
      - balance_formula
      - value_range
      - schema_compliance
      - no_duplicates

  revision:
    description: "識別 USDA 數據修正"
    checks:
      - compare_with_latest
      - flag_revisions
      - track_changes

  freshness:
    description: "檢查數據是否為最新"
    checks:
      - latest_release_available
      - missing_releases
```

**Step 2: 載入現有數據**

```python
import pandas as pd
import os

def load_existing_data(data_dir, commodity=None):
    """載入現有的 curated 數據"""

    curated_dir = f"{data_dir}/curated"
    data = {}

    if commodity:
        parquet_path = f"{curated_dir}/{commodity}_balance.parquet"
        if os.path.exists(parquet_path):
            data[commodity] = pd.read_parquet(parquet_path)
    else:
        # 載入所有商品
        for f in os.listdir(curated_dir):
            if f.endswith('_balance.parquet'):
                commodity_name = f.replace('_balance.parquet', '')
                data[commodity_name] = pd.read_parquet(f"{curated_dir}/{f}")

    return data
```

**Step 3: 完整性驗證**

```python
from scripts.validate_data import (
    validate_balance,
    validate_range,
    check_duplicates
)

def run_integrity_check(df, commodity):
    """執行完整性檢查"""

    results = {
        "commodity": commodity,
        "total_rows": len(df),
        "issues": []
    }

    # 平衡公式檢查
    for idx, row in df.iterrows():
        balance_ok, diff = validate_balance(row.to_dict())
        if not balance_ok:
            results['issues'].append({
                "row_index": idx,
                "release_date": row['release_date'],
                "marketing_year": row['marketing_year'],
                "type": "balance_error",
                "details": f"Balance diff: {diff}"
            })

    # 數值範圍檢查
    for idx, row in df.iterrows():
        range_issues = validate_range(row.to_dict(), commodity)
        for issue in range_issues:
            results['issues'].append({
                "row_index": idx,
                "release_date": row['release_date'],
                "marketing_year": row['marketing_year'],
                "type": "range_warning",
                "details": issue
            })

    # 重複檢查
    duplicates = check_duplicates(df, ['release_date', 'marketing_year', 'commodity'])
    for dup in duplicates:
        results['issues'].append({
            "type": "duplicate",
            "details": dup
        })

    results['valid_rows'] = results['total_rows'] - len([
        i for i in results['issues'] if i['type'] == 'balance_error'
    ])
    results['integrity_score'] = results['valid_rows'] / results['total_rows'] * 100

    return results
```

**Step 4: 修正值識別**

```python
def detect_revisions(existing_data, latest_data, commodity):
    """比對現有數據與最新數據，識別修正值"""

    revisions = []

    # 找出重疊的 marketing years
    existing_mys = set(existing_data['marketing_year'].unique())
    latest_mys = set(latest_data['marketing_year'].unique())
    overlap_mys = existing_mys & latest_mys

    for my in overlap_mys:
        existing_row = existing_data[existing_data['marketing_year'] == my].iloc[-1]
        latest_row = latest_data[latest_data['marketing_year'] == my].iloc[0]

        # 比較數值欄位
        numeric_fields = [
            'beginning_stocks', 'production', 'imports',
            'exports', 'ending_stocks', 'total_use'
        ]

        for field in numeric_fields:
            if field not in existing_row or field not in latest_row:
                continue

            old_val = existing_row.get(field)
            new_val = latest_row.get(field)

            if pd.isna(old_val) or pd.isna(new_val):
                continue

            if abs(old_val - new_val) > 0.001:  # 有差異
                revisions.append({
                    "marketing_year": my,
                    "field": field,
                    "old_value": old_val,
                    "new_value": new_val,
                    "change": new_val - old_val,
                    "change_pct": (new_val - old_val) / old_val * 100 if old_val != 0 else None,
                    "old_release": existing_row['release_date'],
                    "new_release": latest_row['release_date']
                })

    return revisions
```

**Step 5: 新鮮度檢查**

```python
from scripts.discover_releases import discover_latest_release
from datetime import datetime, timedelta

def check_freshness(existing_data, commodity):
    """檢查數據新鮮度"""

    # 獲取最新可用的 release
    latest_available = discover_latest_release()

    # 獲取現有數據的最新 release
    latest_in_data = existing_data['release_date'].max()

    is_current = str(latest_in_data) == latest_available['release_date']

    # 計算缺失的 releases
    missing_releases = []
    if not is_current:
        # 列出從 latest_in_data 到 latest_available 之間的所有 releases
        from scripts.discover_releases import get_release_calendar
        all_releases = get_release_calendar(
            start=datetime.strptime(str(latest_in_data), "%Y-%m-%d"),
            end=datetime.strptime(latest_available['release_date'], "%Y-%m-%d")
        )
        existing_dates = set(existing_data['release_date'].astype(str).unique())
        missing_releases = [
            r['release_date'] for r in all_releases
            if r['release_date'] not in existing_dates
        ]

    return {
        "commodity": commodity,
        "latest_available": latest_available['release_date'],
        "latest_in_data": str(latest_in_data),
        "is_current": is_current,
        "missing_releases": missing_releases,
        "days_behind": (
            datetime.strptime(latest_available['release_date'], "%Y-%m-%d") -
            datetime.strptime(str(latest_in_data), "%Y-%m-%d")
        ).days if not is_current else 0
    }
```

**Step 6: 生成驗證報告**

```python
def generate_validation_report(
    integrity_results,
    revision_results,
    freshness_results,
    output_dir
):
    """生成完整的驗證報告"""

    report = {
        "validation_timestamp": datetime.now().isoformat(),
        "summary": {
            "commodities_validated": len(integrity_results),
            "overall_integrity_score": sum(
                r['integrity_score'] for r in integrity_results.values()
            ) / len(integrity_results),
            "total_issues": sum(
                len(r['issues']) for r in integrity_results.values()
            ),
            "revisions_detected": sum(
                len(r) for r in revision_results.values()
            ),
            "commodities_current": sum(
                1 for r in freshness_results.values() if r['is_current']
            )
        },
        "integrity": integrity_results,
        "revisions": revision_results,
        "freshness": freshness_results,
        "recommendations": generate_recommendations(
            integrity_results,
            revision_results,
            freshness_results
        )
    }

    # 寫入報告
    report_path = f"{output_dir}/validation_report_{datetime.now():%Y%m%d_%H%M%S}.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2, default=str)

    return report

def generate_recommendations(integrity, revisions, freshness):
    """生成建議操作"""

    recommendations = []

    # 完整性問題
    for commodity, result in integrity.items():
        if result['integrity_score'] < 95:
            recommendations.append({
                "priority": "high",
                "commodity": commodity,
                "action": "re-ingest",
                "reason": f"Integrity score {result['integrity_score']:.1f}% below threshold"
            })

    # 修正值處理
    for commodity, revs in revisions.items():
        significant_revs = [r for r in revs if abs(r.get('change_pct', 0) or 0) > 5]
        if significant_revs:
            recommendations.append({
                "priority": "medium",
                "commodity": commodity,
                "action": "update_historical",
                "reason": f"{len(significant_revs)} significant revisions detected"
            })

    # 新鮮度問題
    for commodity, result in freshness.items():
        if result['days_behind'] > 30:
            recommendations.append({
                "priority": "high",
                "commodity": commodity,
                "action": "ingest_latest",
                "reason": f"Data is {result['days_behind']} days behind"
            })
        elif result['missing_releases']:
            recommendations.append({
                "priority": "medium",
                "commodity": commodity,
                "action": "backfill",
                "reason": f"{len(result['missing_releases'])} missing releases"
            })

    return sorted(recommendations, key=lambda x: {"high": 0, "medium": 1, "low": 2}[x['priority']])
```

**Step 7: 執行修復（可選）**

```python
def apply_fixes(recommendations, config):
    """根據建議執行修復"""

    for rec in recommendations:
        if rec['action'] == 'ingest_latest':
            # 執行最新 ingest
            from workflows.ingest import run_single_ingest
            run_single_ingest(
                release_info="latest",
                commodities=[rec['commodity']],
                scope=config.scope,
                output_dir=config.output_dir
            )

        elif rec['action'] == 'backfill':
            # 執行 backfill
            from workflows.backfill import run_backfill
            # ... backfill missing releases

        elif rec['action'] == 're-ingest':
            # 重新 ingest 有問題的數據
            # ... re-ingest with force=True
            pass
```
</process>

<success_criteria>
此工作流程成功完成時：
- [ ] 完成所有指定商品的完整性檢查
- [ ] 識別並記錄所有數據修正
- [ ] 檢查數據新鮮度
- [ ] 生成完整的 validation_report.json
- [ ] 提供可操作的修復建議
</success_criteria>

<scheduled_validation>
**建議定期執行：**

```yaml
schedule:
  integrity_check:
    frequency: "weekly"
    day: "Sunday"

  revision_check:
    frequency: "monthly"
    trigger: "after WASDE release"

  freshness_check:
    frequency: "daily"
    alert_if_behind: 7  # days
```
</scheduled_validation>
