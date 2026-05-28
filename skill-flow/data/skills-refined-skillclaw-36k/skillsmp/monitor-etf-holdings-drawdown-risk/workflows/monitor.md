# Workflow: 持續監控模式

<required_reading>
**執行前請先閱讀：**
1. references/input-schema.md - 完整參數定義
2. references/data-sources.md - 數據來源與抓取方式
</required_reading>

<process>

## Step 1: 配置監控參數

設定監控的 ETF 清單與警報門檻：

```python
monitor_config = {
    "etfs": [
        {"ticker": "SLV", "commodity": "XAGUSD", "name": "iShares Silver Trust"},
        {"ticker": "PSLV", "commodity": "XAGUSD", "name": "Sprott Physical Silver"},
        {"ticker": "GLD", "commodity": "XAUUSD", "name": "SPDR Gold Shares"},
        {"ticker": "PHYS", "commodity": "XAUUSD", "name": "Sprott Physical Gold"}
    ],
    "alert_thresholds": {
        "stress_score_warning": 50,    # 警告門檻
        "stress_score_critical": 75,   # 嚴重門檻
        "divergence_trigger": True      # 背離觸發警報
    },
    "check_interval_hours": 24,        # 檢查間隔（小時）
    "output_dir": "output/monitor/"
}
```

## Step 2: 執行單次監控檢查

對每個 ETF 執行快速檢查：

```bash
python scripts/divergence_detector.py \
  --etf SLV --commodity XAGUSD --quick \
  --output output/monitor/SLV_latest.json

python scripts/divergence_detector.py \
  --etf PSLV --commodity XAGUSD --quick \
  --output output/monitor/PSLV_latest.json

python scripts/divergence_detector.py \
  --etf GLD --commodity XAUUSD --quick \
  --output output/monitor/GLD_latest.json
```

## Step 3: 彙總監控結果

```python
import json
from pathlib import Path

results = []
for etf in monitor_config["etfs"]:
    result_file = Path(f"output/monitor/{etf['ticker']}_latest.json")
    if result_file.exists():
        with open(result_file) as f:
            result = json.load(f)
            result["etf_name"] = etf["name"]
            results.append(result)
```

## Step 4: 判定警報等級

```python
def get_alert_level(result, thresholds):
    stress = result.get("stress_score_0_100", 0)
    divergence = result.get("divergence", False)

    if stress >= thresholds["stress_score_critical"]:
        return "CRITICAL"
    elif stress >= thresholds["stress_score_warning"] or divergence:
        return "WARNING"
    else:
        return "NORMAL"

alerts = []
for result in results:
    level = get_alert_level(result, monitor_config["alert_thresholds"])
    if level != "NORMAL":
        alerts.append({
            "etf": result.get("etf_ticker"),
            "level": level,
            "stress_score": result.get("stress_score_0_100"),
            "divergence": result.get("divergence"),
            "message": f"{result['etf_name']}: stress={result.get('stress_score_0_100'):.1f}, divergence={result.get('divergence')}"
        })
```

## Step 5: 產出監控報告

```python
report = {
    "timestamp": datetime.now().isoformat(),
    "summary": {
        "total_monitored": len(results),
        "critical_alerts": len([a for a in alerts if a["level"] == "CRITICAL"]),
        "warning_alerts": len([a for a in alerts if a["level"] == "WARNING"]),
        "normal": len(results) - len(alerts)
    },
    "alerts": alerts,
    "details": results
}

# 輸出報告
with open("output/monitor/report.json", "w") as f:
    json.dump(report, f, indent=2)
```

## Step 6: 設定定時任務（可選）

使用 APScheduler 設定定時檢查：

```python
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
import random

scheduler = BlockingScheduler()

def run_monitor_check():
    # 隨機延遲 0-15 分鐘（避免固定時間爬取）
    jitter = random.uniform(0, 15 * 60)
    time.sleep(jitter)

    # 執行監控檢查
    check_all_etfs()

scheduler.add_job(
    run_monitor_check,
    trigger=IntervalTrigger(hours=monitor_config["check_interval_hours"]),
    id='etf_monitor'
)

scheduler.start()
```

**注意**：定時任務需要額外安裝 `apscheduler`：
```bash
pip install apscheduler
```

## Step 7: 歷史趨勢追蹤（可選）

記錄每次檢查結果以追蹤趨勢：

```python
import csv
from datetime import datetime

def log_check_result(result):
    log_file = f"output/monitor/{result['etf_ticker']}_history.csv"

    with open(log_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().isoformat(),
            result.get("stress_score_0_100"),
            result.get("divergence"),
            result.get("price_return_window"),
            result.get("inventory_change_window"),
            result.get("inventory_decade_low")
        ])
```

</process>

<success_criteria>
監控設定完成時應：

- [ ] 配置監控 ETF 清單
- [ ] 設定警報門檻
- [ ] 執行單次監控檢查
- [ ] 產出彙總報告
- [ ] 識別需要關注的警報
- [ ] （可選）設定定時任務
- [ ] （可選）記錄歷史趨勢
</success_criteria>
