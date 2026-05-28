---
name: error-detective
description: Use this skill when debugging issues, analyzing logs, or investigating production errors to identify error patterns, stack traces, and anomalies.
---

# Skill body

## When to use
- Investigating production errors
- Analyzing log patterns
- Finding error root causes
- Correlating errors across systems
- Proactively monitoring for anomalies

## Log analysis

### Find errors

```bash
# Recent errors
grep -i "error\|exception\|fatal" /var/log/app.log | tail -100

# Errors with context
grep -B 5 -A 10 "ERROR" /var/log/app.log

# Count by error type
grep -oE "Error: [^:]*" app.log | sort | uniq -c | sort -rn

# Errors in time range
awk '/2024-01-15 14:/ && /ERROR/' app.log
```

### Pattern detection

```bash
# Find repeated errors
grep "ERROR" app.log | cut -d']' -f2 | sort | uniq -c | sort -rn | head -20

# Correlate request IDs
grep "req-12345" *.log | sort -t' ' -k1,2

# Find error spikes
grep "ERROR" app.log | cut -d' ' -f1-2 | uniq -c | sort -rn
```

## Stack trace analysis

### Parse stack traces

```python
import re

def parse_stack_trace(log_content: str) -> list[dict]:
    pattern = r'(?P<exception>\w+Error|\w+Exception): (?P<message>.*?)\n(?P<trace>(?:\s+at .+\n)+)'

    traces = []
    for match in re.finditer(pattern, log_content):
        traces.append({
            'type': match.group('exception'),
            'message': match.group('message'),
            'trace': match.group('trace').strip().split('\n')
        })
    return traces
```

### Common patterns

| Pattern            | Indicates          | Action                   |
| ------------------ | ------------------ | ------------------------ |
| NullPointer        | Missing null check | Add validation           |
| Timeout            | Slow dependency    | Add timeout, retry       |
| Connection refused | Service down       | Check health, retry      |
| OOM                | Memory leak        | Profile, increase limits |
| Rate limit         | Too many requests  | Add backoff, queue       |

## Investigation checklist

1. **Capture** - Get full error message and stack trace
2. **Timestamp** - When did it start?
3. **Frequency** - How often? Increasing?
4. **Scope** - All users or specific?
5. **Changes** - Recent deployments?
6. **Dependencies** - External services affected?

## Correlation queries

```sql
-- Errors by endpoint
SELECT endpoint, count(*) as errors
FROM logs
WHERE level = 'ERROR' AND time > NOW() - INTERVAL '1 hour'
```

## Output
- Regex patterns for error extraction
- Timeline of error occurrences
- Correlation analysis between services
- Root cause hypothesis with evidence
- Monitoring queries to detect recurrence
- Code locations likely causing errors

Focus on actionable findings. Include both immediate fixes and prevention strategies.