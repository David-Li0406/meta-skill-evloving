# Instrumentation Templates by Language

Language-specific logging patterns for hypothesis-based debugging. All templates use `#region agent log` markers for easy cleanup.

## JavaScript / TypeScript (HTTP-based)

Uses HTTP POST to local debug server. Best for browser and Node.js environments.

### Basic Log

```javascript
// #region agent log - Hypothesis A
fetch('http://127.0.0.1:3947/debug', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    location: 'filename.js:15',
    message: 'Function entry',
    data: { param1, param2, types: { p1: typeof param1, p2: typeof param2 } },
    timestamp: Date.now(),
    sessionId: 'SESSION_ID',
    runId: 'initial',
    hypothesisId: 'A'
  })
}).catch(() => {});
// #endregion
```

### Async Function Entry/Exit

```javascript
async function processData(input) {
  // #region agent log - Hypothesis B
  fetch('http://127.0.0.1:3947/debug', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      location: 'processor.js:10',
      message: 'processData entry',
      data: { input, inputType: typeof input },
      timestamp: Date.now(),
      sessionId: 'SESSION_ID',
      runId: 'initial',
      hypothesisId: 'B'
    })
  }).catch(() => {});
  // #endregion

  const result = await doWork(input);

  // #region agent log - Hypothesis B
  fetch('http://127.0.0.1:3947/debug', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      location: 'processor.js:25',
      message: 'processData exit',
      data: { input, result, resultType: typeof result },
      timestamp: Date.now(),
      sessionId: 'SESSION_ID',
      runId: 'initial',
      hypothesisId: 'B'
    })
  }).catch(() => {});
  // #endregion

  return result;
}
```

### Conditional Branch

```javascript
// #region agent log - Hypothesis C
fetch('http://127.0.0.1:3947/debug', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    location: 'logic.js:42',
    message: 'Before condition check',
    data: { value, condition: 'value > threshold', threshold, willBranch: value > threshold },
    timestamp: Date.now(),
    sessionId: 'SESSION_ID',
    runId: 'initial',
    hypothesisId: 'C'
  })
}).catch(() => {});
// #endregion

if (value > threshold) {
  // #region agent log - Hypothesis C
  fetch('http://127.0.0.1:3947/debug', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      location: 'logic.js:45',
      message: 'Entered TRUE branch',
      data: { value, threshold },
      timestamp: Date.now(),
      sessionId: 'SESSION_ID',
      runId: 'initial',
      hypothesisId: 'C'
    })
  }).catch(() => {});
  // #endregion
}
```

---

## Python (File-based)

Uses direct file append. Works in any Python environment.

### Setup Helper (optional)

```python
# #region agent log setup
import json
import time
import os

DEBUG_FILE = '.claude-logs/debug.ndjson'
os.makedirs('.claude-logs', exist_ok=True)

def debug_log(location, message, data, hypothesis_id, run_id='initial', session_id='SESSION_ID'):
    with open(DEBUG_FILE, 'a') as f:
        f.write(json.dumps({
            'location': location,
            'message': message,
            'data': data,
            'timestamp': int(time.time() * 1000),
            'sessionId': session_id,
            'runId': run_id,
            'hypothesisId': hypothesis_id
        }) + '\n')
# #endregion
```

### Inline Log (no helper)

```python
# #region agent log - Hypothesis A
import json, time
with open('.claude-logs/debug.ndjson', 'a') as f:
    f.write(json.dumps({
        'location': 'processor.py:15',
        'message': 'Function entry',
        'data': {'param': param, 'param_type': str(type(param))},
        'timestamp': int(time.time() * 1000),
        'sessionId': 'SESSION_ID',
        'runId': 'initial',
        'hypothesisId': 'A'
    }) + '\n')
# #endregion
```

### Function Entry/Exit

```python
def process_order(order_id, items):
    # #region agent log - Hypothesis B
    debug_log('orders.py:20', 'process_order entry', {
        'order_id': order_id,
        'items': items,
        'item_count': len(items)
    }, 'B')
    # #endregion

    result = calculate_total(items)

    # #region agent log - Hypothesis B
    debug_log('orders.py:35', 'process_order exit', {
        'order_id': order_id,
        'result': result
    }, 'B')
    # #endregion

    return result
```

---

## Go (File-based)

Uses file append with mutex for thread safety.

### Setup Helper

```go
// #region agent log setup
package main

import (
    "encoding/json"
    "os"
    "sync"
    "time"
)

var debugMu sync.Mutex
const debugFile = ".claude-logs/debug.ndjson"

func init() {
    os.MkdirAll(".claude-logs", 0755)
}

type DebugLog struct {
    Location     string                 `json:"location"`
    Message      string                 `json:"message"`
    Data         map[string]interface{} `json:"data"`
    Timestamp    int64                  `json:"timestamp"`
    SessionID    string                 `json:"sessionId"`
    RunID        string                 `json:"runId"`
    HypothesisID string                 `json:"hypothesisId"`
}

func debugLog(location, message string, data map[string]interface{}, hypothesisID string) {
    debugMu.Lock()
    defer debugMu.Unlock()

    entry := DebugLog{
        Location:     location,
        Message:      message,
        Data:         data,
        Timestamp:    time.Now().UnixMilli(),
        SessionID:    "SESSION_ID",
        RunID:        "initial",
        HypothesisID: hypothesisID,
    }

    f, _ := os.OpenFile(debugFile, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
    defer f.Close()
    json.NewEncoder(f).Encode(entry)
}
// #endregion
```

### Usage

```go
func ProcessRequest(req *Request) (*Response, error) {
    // #region agent log - Hypothesis A
    debugLog("handler.go:45", "ProcessRequest entry", map[string]interface{}{
        "requestID": req.ID,
        "method":    req.Method,
    }, "A")
    // #endregion

    result, err := doWork(req)

    // #region agent log - Hypothesis A
    debugLog("handler.go:55", "ProcessRequest exit", map[string]interface{}{
        "requestID": req.ID,
        "hasError":  err != nil,
        "result":    result,
    }, "A")
    // #endregion

    return result, err
}
```

---

## Rust (File-based)

Uses file append with mutex.

### Setup Helper

```rust
// #region agent log setup
use std::fs::{OpenOptions, create_dir_all};
use std::io::Write;
use std::sync::Mutex;
use std::time::{SystemTime, UNIX_EPOCH};
use serde_json::json;

lazy_static::lazy_static! {
    static ref DEBUG_MUTEX: Mutex<()> = Mutex::new(());
}

fn debug_log(location: &str, message: &str, data: serde_json::Value, hypothesis_id: &str) {
    let _lock = DEBUG_MUTEX.lock().unwrap();
    create_dir_all(".claude-logs").ok();

    let timestamp = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_millis();

    let entry = json!({
        "location": location,
        "message": message,
        "data": data,
        "timestamp": timestamp,
        "sessionId": "SESSION_ID",
        "runId": "initial",
        "hypothesisId": hypothesis_id
    });

    let mut file = OpenOptions::new()
        .create(true)
        .append(true)
        .open(".claude-logs/debug.ndjson")
        .unwrap();

    writeln!(file, "{}", entry).ok();
}
// #endregion
```

### Usage

```rust
fn process_data(input: &str) -> Result<String, Error> {
    // #region agent log - Hypothesis A
    debug_log("processor.rs:20", "process_data entry", json!({
        "input": input,
        "input_len": input.len()
    }), "A");
    // #endregion

    let result = transform(input)?;

    // #region agent log - Hypothesis A
    debug_log("processor.rs:30", "process_data exit", json!({
        "result": result,
        "result_len": result.len()
    }), "A");
    // #endregion

    Ok(result)
}
```

---

## Shell / Bash (File-based)

For debugging shell scripts.

```bash
# #region agent log - Hypothesis A
echo "{\"location\":\"script.sh:15\",\"message\":\"Before loop\",\"data\":{\"count\":$COUNT,\"file\":\"$FILE\"},\"timestamp\":$(date +%s%3N),\"sessionId\":\"SESSION_ID\",\"runId\":\"initial\",\"hypothesisId\":\"A\"}" >> .claude-logs/debug.ndjson
# #endregion
```

---

## Region Marker Reference

| Language | Start Marker | End Marker |
|----------|-------------|------------|
| JavaScript/TypeScript | `// #region agent log` | `// #endregion` |
| Python | `# #region agent log` | `# #endregion` |
| Go | `// #region agent log` | `// #endregion` |
| Rust | `// #region agent log` | `// #endregion` |
| Bash | `# #region agent log` | `# #endregion` |

Always include the hypothesis ID in the marker: `// #region agent log - Hypothesis A`
