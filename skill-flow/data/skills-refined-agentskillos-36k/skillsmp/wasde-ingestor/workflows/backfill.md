<required_reading>
**執行此工作流程前，請先閱讀：**
1. references/commodities-overview.md - 了解商品範圍與行銷年度
2. references/validation-rules.md - 了解驗證規則
3. workflows/ingest.md - 了解單次 ingest 流程
</required_reading>

<objective>
批量回補歷史 WASDE 數據，從指定起始日期開始，抓取並解析多個月份的報告。
</objective>

<process>
**Step 1: 確認參數**

```yaml
parameters:
  commodities:
    description: "要回補的商品"
    default: "all"

  scope:
    description: "數據範圍"
    default: "us,world"

  months_back:
    description: "回補多少個月"
    default: 24
    min: 1
    max: 240  # 最多 20 年

  start_date:
    description: "起始日期（優先於 months_back）"
    format: "YYYY-MM-DD"
    optional: true

  end_date:
    description: "結束日期"
    format: "YYYY-MM-DD"
    default: "today"

  output_dir:
    description: "輸出目錄"
    default: "./data/wasde"

  parallel:
    description: "並行處理數量"
    default: 3
    max: 5

  skip_existing:
    description: "跳過已存在的數據"
    default: true
```

**Step 2: 生成報告日期列表**

```python
from datetime import datetime, timedelta
from scripts.discover_releases import get_release_calendar

def generate_release_dates(months_back=None, start_date=None, end_date=None):
    """生成要處理的 release dates 列表"""

    if end_date is None:
        end_date = datetime.today()
    elif isinstance(end_date, str):
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

    if start_date:
        start = datetime.strptime(start_date, "%Y-%m-%d")
    else:
        # WASDE 每月發布一次
        start = end_date - timedelta(days=months_back * 31)

    # 獲取實際發布日曆
    release_calendar = get_release_calendar(start, end_date)

    return release_calendar

# 範例輸出
# [
#   {"release_date": "2024-12-10", "pdf_url": "..."},
#   {"release_date": "2024-11-08", "pdf_url": "..."},
#   ...
# ]
```

**Step 3: 檢查已存在數據**

```python
import pandas as pd
import os

def get_existing_releases(output_dir, commodity):
    """獲取已存在的 release dates"""
    parquet_path = f"{output_dir}/curated/{commodity}_balance.parquet"

    if not os.path.exists(parquet_path):
        return set()

    df = pd.read_parquet(parquet_path)
    return set(df['release_date'].astype(str).unique())

def filter_missing_releases(all_releases, existing_releases, skip_existing=True):
    """過濾出需要處理的 releases"""
    if not skip_existing:
        return all_releases

    return [r for r in all_releases if r['release_date'] not in existing_releases]
```

**Step 4: 批量處理**

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
from workflows.ingest import run_single_ingest
import time

def run_backfill(releases, config, parallel=3):
    """批量執行 ingest"""

    results = []
    failed = []

    with ThreadPoolExecutor(max_workers=parallel) as executor:
        # 提交所有任務
        future_to_release = {
            executor.submit(
                run_single_ingest,
                release_info=release,
                commodities=config.commodities,
                scope=config.scope,
                output_dir=config.output_dir
            ): release
            for release in releases
        }

        # 處理完成的任務
        for future in as_completed(future_to_release):
            release = future_to_release[future]
            try:
                result = future.result()
                results.append({
                    "release_date": release['release_date'],
                    "status": "success",
                    "result": result
                })
                print(f"✓ {release['release_date']} completed")

            except Exception as e:
                failed.append({
                    "release_date": release['release_date'],
                    "status": "failed",
                    "error": str(e)
                })
                print(f"✗ {release['release_date']} failed: {e}")

            # 避免過度請求
            time.sleep(0.5)

    return results, failed
```

**Step 5: 合併數據**

```python
def consolidate_parquet_files(output_dir, commodity):
    """合併所有 parquet 文件，去重並排序"""

    parquet_path = f"{output_dir}/curated/{commodity}_balance.parquet"

    if not os.path.exists(parquet_path):
        return

    df = pd.read_parquet(parquet_path)

    # 去重：保留最新的 content_hash
    df = df.sort_values('release_date')
    df = df.drop_duplicates(
        subset=['release_date', 'marketing_year', 'commodity'],
        keep='last'
    )

    # 排序
    df = df.sort_values(['marketing_year', 'release_date'])

    # 重新寫入
    df.to_parquet(parquet_path, index=False)

    return len(df)
```

**Step 6: 生成回補報告**

```python
def generate_backfill_report(results, failed, config):
    """生成回補總結報告"""

    report = {
        "backfill_config": {
            "commodities": config.commodities,
            "scope": config.scope,
            "months_back": config.months_back,
            "start_date": config.start_date,
            "end_date": config.end_date
        },
        "summary": {
            "total_releases": len(results) + len(failed),
            "successful": len(results),
            "failed": len(failed),
            "success_rate": len(results) / (len(results) + len(failed)) * 100
        },
        "successful_releases": [r['release_date'] for r in results],
        "failed_releases": [
            {"release_date": f['release_date'], "error": f['error']}
            for f in failed
        ],
        "data_coverage": {
            commodity: get_coverage_stats(config.output_dir, commodity)
            for commodity in get_commodity_list(config.commodities)
        }
    }

    # 寫入報告
    report_path = f"{config.output_dir}/backfill_report_{datetime.now():%Y%m%d_%H%M%S}.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)

    return report

def get_coverage_stats(output_dir, commodity):
    """獲取數據覆蓋統計"""
    parquet_path = f"{output_dir}/curated/{commodity}_balance.parquet"

    if not os.path.exists(parquet_path):
        return {"rows": 0, "date_range": None}

    df = pd.read_parquet(parquet_path)
    return {
        "rows": len(df),
        "date_range": {
            "min": df['release_date'].min(),
            "max": df['release_date'].max()
        },
        "marketing_years": df['marketing_year'].unique().tolist()
    }
```

**Step 7: 處理失敗重試**

```python
def retry_failed_releases(failed, config, max_retries=2):
    """重試失敗的 releases"""

    remaining_failed = failed
    retry_count = 0

    while remaining_failed and retry_count < max_retries:
        retry_count += 1
        print(f"\n--- Retry attempt {retry_count} ---")

        # 等待一段時間
        time.sleep(30)

        results, still_failed = run_backfill(
            releases=remaining_failed,
            config=config,
            parallel=1  # 重試時使用單線程
        )

        remaining_failed = still_failed

    return remaining_failed
```
</process>

<success_criteria>
此工作流程成功完成時：
- [ ] 成功識別所有要處理的 release dates
- [ ] 成功處理 90% 以上的 releases（允許部分失敗）
- [ ] 所有成功的數據已合併到 curated parquet
- [ ] 生成完整的 backfill_report.json
- [ ] 失敗的 releases 已記錄並嘗試重試
</success_criteria>

<performance_notes>
**效能建議：**

1. **並行度**
   - 建議 parallel=3，避免過度請求 USDA 伺服器
   - 每次請求間隔至少 0.5 秒

2. **記憶體管理**
   - 每處理 10 個 releases 後執行一次 gc
   - 大量回補時建議分批處理

3. **斷點續傳**
   - 使用 skip_existing=true 可以從失敗處繼續
   - 每個 release 處理完立即寫入

4. **預估時間**
   - 單個 release 約 10-30 秒
   - 24 個月約需 10-15 分鐘
   - 240 個月約需 2-3 小時
</performance_notes>
