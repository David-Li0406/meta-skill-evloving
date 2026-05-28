# memex-cli Output Formats Reference

This document provides detailed specifications for memex-cli output formats.

## Overview

memex-cli supports two output formats:
1. **Text Format** (default) - Human-readable with status markers
2. **JSONL Format** - Machine-readable JSON Lines for programmatic parsing

## Text Format (Default)

### Status Markers

Human-readable output uses Unicode markers to indicate task status and actions:

| Marker | Meaning | Usage |
|--------|---------|-------|
| `▶` | Task start | Indicates beginning of task execution |
| `✓` | Success | Task completed successfully |
| `✗` | Failed | Task failed or error occurred |
| `⟳` | Retrying | Task is being retried after failure |
| `»` | Action | File write, command execution, or other action |
| `⚠` | Warning | Warning message or timeout alert |
| `📄` | File loaded | File has been loaded into context |

### Single Task Output Example

```
▶ code-gen-20260109100000 (codex/gpt-5.2)

```python
def authenticate(username: str, password: str) -> bool:
    """用户认证函数"""
    user = db.query(User).filter_by(username=username).first()
    if not user:
        return False
    return verify_password(password, user.password_hash)
```

» 写入 auth.py
✓ code-gen-20260109100000 3.5s
```

**Breakdown:**
- `▶ code-gen-20260109100000 (codex/gpt-5.2)` - Task starts with ID and backend
- AI-generated output content appears next
- `» 写入 auth.py` - Action marker shows file write
- `✓ code-gen-20260109100000 3.5s` - Success with duration

### Multi-Task Sequential Output (DAG)

```
▶ design (gemini)

设计 REST API...

✓ design 4.2s

▶ implement (codex/gpt-5.2) ← design

实现代码...

» 写入 main.py
✓ implement 6.8s

▶ test (codex) ← implement

编写测试...

» 写入 test_main.py
» 运行 pytest
✓ test 3.1s

───────────────────────────
✓ 完成 3/3 任务 (14.1s)
```

**Key Features:**
- `← design` notation shows task dependency
- Tasks execute sequentially respecting dependencies
- Final summary shows total tasks and time

### Parallel Tasks Output

```
▶ 并行执行 3 个任务...

  ▶ task-a (codex)
  ▶ task-b (codex)
  ▶ task-c (codex)

  ✓ task-a 2.1s
  ✓ task-b 2.5s
  ✓ task-c 2.8s

───────────────────────────
✓ 完成 3/3 任务 (2.8s, 并行加速 2.6x)
```

**Parallel Indicators:**
- Header: `▶ 并行执行 N 个任务...`
- Indented task markers show parallel execution
- Summary includes speedup factor (2.6x)

### Error and Retry Output

```
▶ unstable-task (codex)

⚠ 即将超时 (8s/10s)
✗ 超时

⟳ 重试 1/2

处理完成！

✓ unstable-task 4.2s (重试1次)
```

**Error Handling Features:**
- `⚠` warns before timeout
- `✗` marks failure
- `⟳` indicates retry attempt with count
- Final success includes retry count

### File Loading Output

When files are loaded with `files:` parameter:

```
▶ review-task (gemini)

📄 加载 design.md (2.3 KB)
📄 加载 mockup.png (145 KB, base64)

分析设计稿...

✓ review-task 5.1s
```

## JSONL Format

### Enabling JSONL Output

```bash
memex-cli run --stdin --stream-format jsonl < tasks.md
```

### JSONL Structure

Each line is a valid JSON object with consistent schema:

```jsonl
{"v":1,"type":"<event_type>","ts":"<ISO8601>","run_id":"<id>","task_id":"<id>","..."}
```

**Common Fields:**
- `v` (integer) - Protocol version (currently 1)
- `type` (string) - Event type identifier
- `ts` (string) - ISO 8601 timestamp
- `run_id` (string) - Unique run identifier
- `task_id` (string, optional) - Task identifier (absent for run-level events)

### Event Types

#### Run Lifecycle Events

**run.start** - Run begins
```json
{
  "v": 1,
  "type": "run.start",
  "ts": "2026-01-09T10:00:00.000Z",
  "run_id": "abc123",
  "metadata": {
    "total_tasks": 3,
    "execution_mode": "parallel"
  }
}
```

**run.end** - Run completes
```json
{
  "v": 1,
  "type": "run.end",
  "ts": "2026-01-09T10:00:03.600Z",
  "run_id": "abc123",
  "metadata": {
    "status": "success",
    "completed": 3,
    "failed": 0,
    "duration_ms": 3600
  }
}
```

#### Task Lifecycle Events

**task.start** - Task execution begins
```json
{
  "v": 1,
  "type": "task.start",
  "ts": "2026-01-09T10:00:00.100Z",
  "run_id": "abc123",
  "task_id": "code-gen",
  "metadata": {
    "backend": "codex",
    "model": "gpt-5.2"
  }
}
```

**task.end** - Task execution completes
```json
{
  "v": 1,
  "type": "task.end",
  "ts": "2026-01-09T10:00:03.500Z",
  "run_id": "abc123",
  "task_id": "code-gen",
  "metadata": {
    "status": "success",
    "duration_ms": 3400,
    "retries": 0
  }
}
```

#### Content Events

**assistant.output** - AI generates output
```json
{
  "v": 1,
  "type": "assistant.output",
  "ts": "2026-01-09T10:00:01.000Z",
  "run_id": "abc123",
  "task_id": "code-gen",
  "output": "def authenticate(username: str, password: str) -> bool:\n    ..."
}
```

**assistant.action** - AI performs action
```json
{
  "v": 1,
  "type": "assistant.action",
  "ts": "2026-01-09T10:00:03.000Z",
  "run_id": "abc123",
  "task_id": "code-gen",
  "action": "write_file",
  "args": {
    "path": "auth.py",
    "content": "def authenticate..."
  }
}
```

#### Tool Events

**tool.call** - Tool invocation
```json
{
  "v": 1,
  "type": "tool.call",
  "ts": "2026-01-09T10:00:02.000Z",
  "run_id": "abc123",
  "task_id": "test",
  "tool": "bash",
  "args": {
    "command": "pytest tests/"
  }
}
```

**tool.result** - Tool execution result
```json
{
  "v": 1,
  "type": "tool.result",
  "ts": "2026-01-09T10:00:02.500Z",
  "run_id": "abc123",
  "task_id": "test",
  "tool": "bash",
  "result": {
    "exit_code": 0,
    "stdout": "========== 5 passed in 0.12s ==========",
    "stderr": ""
  }
}
```

#### Message Events

**error** - Error occurred
```json
{
  "v": 1,
  "type": "error",
  "ts": "2026-01-09T10:00:04.000Z",
  "run_id": "abc123",
  "task_id": "failing-task",
  "message": "Timeout after 10 seconds",
  "error_code": "TIMEOUT"
}
```

**warning** - Warning message
```json
{
  "v": 1,
  "type": "warning",
  "ts": "2026-01-09T10:00:03.800Z",
  "run_id": "abc123",
  "task_id": "slow-task",
  "message": "Task approaching timeout (8s/10s)"
}
```

**info** - Informational message
```json
{
  "v": 1,
  "type": "info",
  "ts": "2026-01-09T10:00:01.500Z",
  "run_id": "abc123",
  "task_id": "data-task",
  "message": "Loaded design.md (2.3 KB)"
}
```

### Complete JSONL Example

Single task execution from start to finish:

```jsonl
{"v":1,"type":"run.start","ts":"2026-01-09T10:00:00.000Z","run_id":"abc123","metadata":{"total_tasks":1}}
{"v":1,"type":"task.start","ts":"2026-01-09T10:00:00.100Z","run_id":"abc123","task_id":"code-gen","metadata":{"backend":"codex","model":"gpt-5.2"}}
{"v":1,"type":"assistant.output","ts":"2026-01-09T10:00:01.000Z","run_id":"abc123","task_id":"code-gen","output":"def authenticate(username: str, password: str) -> bool:\n    ..."}
{"v":1,"type":"assistant.action","ts":"2026-01-09T10:00:03.000Z","run_id":"abc123","task_id":"code-gen","action":"write_file","args":{"path":"auth.py"}}
{"v":1,"type":"task.end","ts":"2026-01-09T10:00:03.500Z","run_id":"abc123","task_id":"code-gen","metadata":{"status":"success","duration_ms":3400}}
{"v":1,"type":"run.end","ts":"2026-01-09T10:00:03.600Z","run_id":"abc123","metadata":{"status":"success","completed":1,"failed":0}}
```

### Parsing JSONL Output

**Python Example:**

```python
import json

with open('output.jsonl') as f:
    for line in f:
        event = json.loads(line)

        if event['type'] == 'assistant.output':
            print(f"Output: {event['output'][:50]}...")

        elif event['type'] == 'assistant.action':
            print(f"Action: {event['action']} - {event['args']}")

        elif event['type'] == 'task.end':
            status = event['metadata']['status']
            duration = event['metadata']['duration_ms']
            print(f"Task {event['task_id']} {status} in {duration}ms")
```

**JavaScript Example:**

```javascript
const fs = require('fs');
const readline = require('readline');

const rl = readline.createInterface({
  input: fs.createReadStream('output.jsonl'),
  crlfDelay: Infinity
});

rl.on('line', (line) => {
  const event = JSON.parse(line);

  if (event.type === 'run.end') {
    console.log(`Completed ${event.metadata.completed} tasks`);
  }
});
```

## Format Selection Guidelines

**Use Text Format when:**
- Running tasks interactively in terminal
- Human monitoring of task progress
- Debugging or exploring memex-cli features
- One-off task executions

**Use JSONL Format when:**
- Integrating memex-cli into automation pipelines
- Logging task execution for analysis
- Building dashboards or monitoring systems
- Programmatic parsing of task results

## Advanced Output Features

### Streaming Behavior

Both formats stream output in real-time:
- Text format shows output as it's generated
- JSONL emits events immediately as they occur

### Output Redirection

```bash
# Save text output
memex-cli run --stdin < tasks.md > output.log 2>&1

# Save JSONL output
memex-cli run --stdin --stream-format jsonl < tasks.md > events.jsonl

# Filter specific events (JSONL)
memex-cli run --stdin --stream-format jsonl < tasks.md | \
  jq 'select(.type == "assistant.action")'
```

### Combining with Tools

```bash
# Watch task progress
memex-cli run --stdin < tasks.md | tee execution.log

# Parse and analyze JSONL
memex-cli run --stdin --stream-format jsonl < tasks.md | \
  jq -r 'select(.type == "task.end") | "\(.task_id): \(.metadata.duration_ms)ms"'
```

## Summary

- **Text format**: Human-friendly, status markers, real-time progress
- **JSONL format**: Machine-readable, structured events, programmatic parsing
- Both formats support streaming output
- Choose format based on use case (interactive vs. automation)
