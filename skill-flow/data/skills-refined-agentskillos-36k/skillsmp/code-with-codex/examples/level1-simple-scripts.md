# Level 1: Simple Scripts Examples

Quick utilities, single-file scripts, simple automation tasks using `codex-mini` or `codex` models.

---

## Example 1: Batch File Rename

Add date prefix to all files in a directory.

### Command

```bash
memex-cli run --backend codex --stdin <<'EOF'
---TASK---
id: batch-rename
backend: codex
workdir: /home/user/scripts
model: gpt-5.1-codex-mini
stream-format: text
---CONTENT---
Python脚本：批量重命名文件，添加日期前缀（格式：YYYYMMDD_filename）
---END---
EOF
```

### Expected Output

```
▶ batch-rename (codex/gpt-5.1-codex-mini)

```python
import os
from datetime import datetime

def batch_rename(directory: str):
    """批量重命名文件，添加日期前缀"""
    today = datetime.now().strftime("%Y%m%d")

    for filename in os.listdir(directory):
        if not filename.startswith(today):
            new_name = f"{today}_{filename}"
            os.rename(
                os.path.join(directory, filename),
                os.path.join(directory, new_name)
            )
            print(f"Renamed: {filename} -> {new_name}")

if __name__ == "__main__":
    batch_rename("./files")
```

» 写入 batch_rename.py
✓ batch-rename 1.8s
```

### Usage

```bash
python batch_rename.py
# Renames all files in ./files/ with YYYYMMDD_ prefix
```

### Customization Tips

- Modify date format: `.strftime("%Y-%m-%d")` for `2026-01-10_`
- Add file type filter: `if filename.endswith('.txt')`
- Add dry-run mode: `print(f"Would rename: {filename}")` without actual `os.rename()`

---

## Example 2: CSV Statistics

Calculate null value counts for each column in a CSV file.

### Command

```bash
memex-cli run --backend codex --stdin <<'EOF'
---TASK---
id: csv-stats
backend: codex
workdir: /home/user/scripts
model: gpt-5.1-codex-mini
stream-format: text
---CONTENT---
读取CSV文件，统计每列的空值数量，生成报告
---END---
EOF
```

### Expected Output

```
▶ csv-stats (codex/gpt-5.1-codex-mini)

```python
import csv
from collections import defaultdict

def analyze_csv(filepath: str):
    """分析CSV文件的空值统计"""
    null_counts = defaultdict(int)
    total_rows = 0

    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames

        for row in reader:
            total_rows += 1
            for header in headers:
                if not row[header] or row[header].strip() == '':
                    null_counts[header] += 1

    # 生成报告
    print(f"Total rows: {total_rows}\n")
    print("Null value counts:")
    for col, count in sorted(null_counts.items()):
        percentage = (count / total_rows) * 100
        print(f"  {col}: {count} ({percentage:.1f}%)")

if __name__ == "__main__":
    analyze_csv("data.csv")
```

» 写入 csv_stats.py
✓ csv-stats 2.1s
```

### Usage

```bash
python csv_stats.py
# Outputs null value statistics for data.csv
```

### Customization Tips

- Support multiple files: `for f in sys.argv[1:]`
- Export to JSON: `json.dump(null_counts, open('stats.json', 'w'))`
- Add visualizations: Use `matplotlib` to plot bar charts

---

## Example 3: Disk Space Monitor

Monitor disk usage and send alerts when threshold exceeded.

### Command

```bash
memex-cli run --backend codex --stdin <<'EOF'
---TASK---
id: disk-monitor
backend: codex
workdir: /home/user/scripts
model: gpt-5.1-codex-mini
stream-format: text
---CONTENT---
Bash脚本：监控磁盘空间，超过80%发送告警（支持Linux/macOS）
---END---
EOF
```

### Expected Output

```
▶ disk-monitor (codex/gpt-5.1-codex-mini)

```bash
#!/bin/bash

THRESHOLD=80

check_disk_usage() {
    df -h | awk 'NR>1 {print $5 " " $6}' | while read usage mount; do
        usage_percent=${usage%\%}

        if [ "$usage_percent" -gt "$THRESHOLD" ]; then
            echo "⚠️  ALERT: $mount is at ${usage} (threshold: ${THRESHOLD}%)"
            # 可选：发送邮件或通知
            # echo "Disk $mount at ${usage}" | mail -s "Disk Alert" admin@example.com
        else
            echo "✓ $mount: ${usage}"
        fi
    done
}

check_disk_usage
```

» 写入 disk_monitor.sh
✓ disk-monitor 1.5s
```

### Usage

```bash
chmod +x disk_monitor.sh
./disk_monitor.sh
# Or add to crontab for periodic checks:
# */30 * * * * /path/to/disk_monitor.sh
```

### Customization Tips

- Adjust threshold: `THRESHOLD=90`
- Email alerts: Uncomment `mail` command and configure SMTP
- Log to file: `>> /var/log/disk_monitor.log`
- Add Slack/webhook notifications

---

## Common Level 1 Task Patterns

### File Operations
- Batch rename/move/copy
- Directory cleanup (delete old files)
- File type conversion (txt → csv, jpg → png)

### Data Processing
- CSV/JSON parsing and filtering
- Log file analysis (extract errors, count events)
- Text search and replace

### System Monitoring
- Disk/memory/CPU usage checks
- Process monitoring (check if service running)
- Network connectivity tests

### Automation
- Backup scripts (compress and archive)
- Scheduled cleanup tasks
- Notification triggers

---

## Model Selection for Level 1

| Task Complexity | Model | Reason |
|----------------|-------|--------|
| Very simple (< 30 lines) | `gpt-5.1-codex-mini` | Fastest, lowest cost |
| Standard scripts (30-80 lines) | `gpt-5.1-codex-mini` | Good quality, fast generation |
| Edge cases (80-100 lines) | `gpt-5.2-codex` | Better error handling |

**When to upgrade to Level 2**:
- Need reusable functions (not just scripts)
- Require input validation or type checking
- Code will be imported by other modules

---

## Tips for Level 1 Tasks

1. **Keep prompts simple**: Specify language, task, basic requirements
2. **Use stdlib only**: Avoid external dependencies for portability
3. **Add basic docs**: Include usage examples in docstrings
4. **Test interactively**: Run generated scripts immediately to verify
5. **Iterate quickly**: Use `codex-mini` for rapid prototyping

---

## Related Resources

- [references/complexity-guide.md](../references/complexity-guide.md) - Detailed complexity selection guide
- [examples/level2-utilities.md](./level2-utilities.md) - Upgrade to reusable functions
- [skills/memex-cli/SKILL.md](../../memex-cli/SKILL.md) - Memex CLI usage details
