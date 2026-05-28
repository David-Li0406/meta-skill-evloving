---
title: Monitor Slow Commands with SLOWLOG
impact: HIGH
impactDescription: identifies performance bottlenecks and problematic commands
tags: performance, slowlog, monitoring, debugging
---

## Monitor Slow Commands with SLOWLOG

Use Redis SLOWLOG to identify slow commands that impact performance. SLOWLOG captures commands exceeding a configurable threshold, helping identify anti-patterns, missing indexes, or unexpected load.

**What SLOWLOG Captures:**
- Commands taking longer than threshold (default 10ms)
- Timestamp, duration, command, and arguments
- Last N slow commands (configurable)

**Common Slow Command Causes:**
- KEYS with many matches
- Operations on large collections
- Blocking commands timing out
- Complex Lua scripts
- Cross-slot operations in cluster

**Incorrect (not monitoring slow commands):**

```python
import redis
r = redis.Redis()

# Anti-pattern 1: No slow log monitoring
# Problems go undetected until outage

# Anti-pattern 2: SLOWLOG threshold too high
# redis.conf: slowlog-log-slower-than 1000000 (1 second)
# Missing commands that take 100-999ms

# Anti-pattern 3: SLOWLOG buffer too small
# redis.conf: slowlog-max-len 32
# Slow commands get evicted before review
```

**Correct (proper SLOWLOG configuration and monitoring):**

```bash
# Correct 1: Configure SLOWLOG appropriately
# redis.conf

# Log commands slower than 10ms (10000 microseconds)
slowlog-log-slower-than 10000

# Keep last 1000 slow commands
slowlog-max-len 1000

# For production debugging, consider lower threshold
# slowlog-log-slower-than 5000  # 5ms
```

```python
import redis
from datetime import datetime

r = redis.Redis()

# Correct 2: Get and analyze slow log
def get_slow_log(count=100):
    """Retrieve slow log entries"""
    entries = r.slowlog_get(count)
    parsed = []

    for entry in entries:
        parsed.append({
            'id': entry['id'],
            'timestamp': datetime.fromtimestamp(entry['start_time']),
            'duration_ms': entry['duration'] / 1000,
            'command': entry['command'].decode() if isinstance(entry['command'], bytes) else entry['command'],
            'client_addr': entry.get('client_address', b'').decode() if entry.get('client_address') else None,
            'client_name': entry.get('client_name', b'').decode() if entry.get('client_name') else None,
        })

    return parsed

def print_slow_log():
    """Print slow log in readable format"""
    entries = get_slow_log()
    print(f"{'ID':<8} {'Duration':<12} {'Command':<50} {'Time'}")
    print("-" * 100)
    for e in entries:
        cmd = e['command'][:47] + '...' if len(e['command']) > 50 else e['command']
        print(f"{e['id']:<8} {e['duration_ms']:>8.2f}ms   {cmd:<50} {e['timestamp']}")

# Correct 3: Alert on slow commands
def check_slow_log_alerts(duration_threshold_ms=100):
    """Alert if there are very slow commands"""
    entries = get_slow_log(50)
    alerts = [e for e in entries if e['duration_ms'] > duration_threshold_ms]

    if alerts:
        return {
            'alert': True,
            'count': len(alerts),
            'slowest': max(alerts, key=lambda x: x['duration_ms']),
            'commands': [e['command'] for e in alerts]
        }
    return {'alert': False}

# Correct 4: Analyze slow log patterns
def analyze_slow_commands():
    """Identify patterns in slow commands"""
    entries = get_slow_log(500)
    analysis = {
        'total_entries': len(entries),
        'by_command': {},
        'by_duration': {
            '10-50ms': 0,
            '50-100ms': 0,
            '100-500ms': 0,
            '500ms+': 0
        }
    }

    for entry in entries:
        # Extract command type (first word)
        cmd_type = entry['command'].split()[0].upper()
        if cmd_type not in analysis['by_command']:
            analysis['by_command'][cmd_type] = {
                'count': 0,
                'total_ms': 0,
                'max_ms': 0
            }

        analysis['by_command'][cmd_type]['count'] += 1
        analysis['by_command'][cmd_type]['total_ms'] += entry['duration_ms']
        analysis['by_command'][cmd_type]['max_ms'] = max(
            analysis['by_command'][cmd_type]['max_ms'],
            entry['duration_ms']
        )

        # Duration buckets
        if entry['duration_ms'] < 50:
            analysis['by_duration']['10-50ms'] += 1
        elif entry['duration_ms'] < 100:
            analysis['by_duration']['50-100ms'] += 1
        elif entry['duration_ms'] < 500:
            analysis['by_duration']['100-500ms'] += 1
        else:
            analysis['by_duration']['500ms+'] += 1

    # Calculate averages
    for cmd, data in analysis['by_command'].items():
        data['avg_ms'] = data['total_ms'] / data['count'] if data['count'] > 0 else 0

    return analysis
```

```python
# Correct 5: Reset and monitor continuously
def reset_slow_log():
    """Reset slow log for fresh measurement period"""
    r.slowlog_reset()
    print("Slow log reset")

def monitor_slow_log_continuous(interval_seconds=60):
    """Continuously monitor and report slow log"""
    import time

    last_id = 0
    while True:
        entries = get_slow_log(100)
        new_entries = [e for e in entries if e['id'] > last_id]

        if new_entries:
            print(f"\n--- {len(new_entries)} new slow commands ---")
            for e in new_entries:
                print(f"  [{e['duration_ms']:.1f}ms] {e['command'][:80]}")

            last_id = max(e['id'] for e in new_entries)

        time.sleep(interval_seconds)

# Correct 6: Configure SLOWLOG at runtime
def configure_slowlog(threshold_microseconds=10000, max_len=1000):
    """Configure SLOWLOG settings"""
    r.config_set('slowlog-log-slower-than', threshold_microseconds)
    r.config_set('slowlog-max-len', max_len)

    current = {
        'threshold_us': r.config_get('slowlog-log-slower-than'),
        'max_len': r.config_get('slowlog-max-len')
    }
    return current
```

```bash
# CLI commands for SLOWLOG

# Get slow log entries
redis-cli SLOWLOG GET 20

# Get slow log length
redis-cli SLOWLOG LEN

# Reset slow log
redis-cli SLOWLOG RESET

# Get current settings
redis-cli CONFIG GET slowlog-*

# Set threshold to 5ms
redis-cli CONFIG SET slowlog-log-slower-than 5000

# Example output:
# 1) 1) (integer) 14               # ID
#    2) (integer) 1309448221       # Timestamp
#    3) (integer) 15               # Duration in microseconds
#    4) 1) "ping"                  # Command
#    5) "127.0.0.1:58217"         # Client address
#    6) ""                         # Client name
```

```javascript
// Node.js - SLOWLOG monitoring
const Redis = require('ioredis');
const redis = new Redis();

async function getSlowLog(count = 100) {
    const entries = await redis.slowlog('GET', count);
    return entries.map(entry => ({
        id: entry[0],
        timestamp: new Date(entry[1] * 1000),
        durationMs: entry[2] / 1000,
        command: entry[3].join(' '),
        clientAddr: entry[4],
        clientName: entry[5]
    }));
}

async function analyzeSlowLog() {
    const entries = await getSlowLog(500);
    const byCommand = {};

    entries.forEach(entry => {
        const cmdType = entry.command.split(' ')[0].toUpperCase();
        if (!byCommand[cmdType]) {
            byCommand[cmdType] = { count: 0, totalMs: 0 };
        }
        byCommand[cmdType].count++;
        byCommand[cmdType].totalMs += entry.durationMs;
    });

    return { totalEntries: entries.length, byCommand };
}
```

Reference: [Redis SLOWLOG](https://redis.io/commands/slowlog/)
