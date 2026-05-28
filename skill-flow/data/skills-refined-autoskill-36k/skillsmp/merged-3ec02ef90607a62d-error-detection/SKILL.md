---
name: error-detection
description: Use this skill to search logs and codebases for error patterns, stack traces, and anomalies, helping to identify root causes and correlations across systems.
---

# Error Detection

Find and analyze errors across logs and code.

## When to use

- Investigating production errors
- Analyzing log patterns
- Finding error root causes
- Correlating errors across systems
- Proactively debugging issues

## Log Analysis

### Find Errors

```bash
# Recent errors
grep -i "error\|exception\|fatal" <log_file> | tail -100

# Errors with context
grep -B 5 -A 10 "ERROR" <log_file>

# Count by error type
grep -oE "Error: [^:]*" <log_file> | sort | uniq -c | sort -rn

# Errors in time range
awk '/<start_time>/ && /ERROR/' <log_file>
```

### Pattern Detection

```bash
# Find repeated errors
grep "ERROR" <log_file> | cut -d']' -f2 | sort | uniq -c | sort -rn | head -20

# Correlate request IDs
grep "<request_id>" <log_files> | sort -t' ' -k1,2

# Find error spikes
grep "ERROR" <log_file> | cut -d' ' -f1-2 | uniq -c | sort -rn
```

## Stack Trace Analysis

### Parse Stack Traces

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

### Common Patterns

| Pattern            | Indicates          | Action                   |
| ------------------ | ------------------ | ------------------------ |
| NullPointer        | Missing null check | Add validation           |
| Timeout            | Slow dependency    | Add timeout, retry       |
| Connection refused | Service down       | Check health, retry      |
| OOM                | Memory leak        | Profile, increase limits |
| Rate limit         | Too many requests  | Add backoff, queue       |

## Investigation Checklist

1. **Capture** - Get full error message and stack trace
2. **Timestamp** - When did it start?
3. **Frequency** - How often? Increasing?
4. **Scope** - All users or specific?
5. **Changes** - Recent deployments?
6. **Dependencies** - External services affected?

## Correlation Queries

```sql
-- Errors by endpoint
SELECT endpoint, count(*) as errors
FROM logs
WHERE level = 'ERROR' AND time > NOW() - INTERVAL '1 hour'
GROUP BY endpoint ORDER BY errors DESC;

-- Error rate over time
SELECT
  date_trunc('minute', time) as minute,
  count(*) filter (where level = 'ERROR') as errors,
  count(*) as total
FROM logs
WHERE time > NOW() - INTERVAL '1 hour'
GROUP BY minute ORDER BY minute;
```

## Examples

**Input:** "Find why API is returning 500 errors"  
**Action:** Search logs for 500 status, find stack traces, identify root cause.

**Input:** "Analyze error patterns from last hour"  
**Action:** Aggregate errors by type, find spikes, correlate with events.

## Focus Areas

- Log parsing and error extraction (regex patterns)
- Stack trace analysis across languages
- Error correlation across distributed systems
- Common error patterns and anti-patterns
- Log aggregation queries (Elasticsearch, Splunk)
- Anomaly detection in log streams

## Approach

1. Start with error symptoms, work backward to cause.
2. Look for patterns across time windows.
3. Correlate errors with deployments/changes.
4. Check for cascading failures.
5. Identify error rate changes and spikes.

## Output

- Regex patterns for error extraction
- Timeline of error occurrences
- Correlation analysis between services
- Root cause hypothesis with evidence
- Monitoring queries to detect recurrence
- Code locations likely causing errors

Focus on actionable findings. Include both immediate fixes and prevention strategies.