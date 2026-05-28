---
name: monitoring
description: How to monitor agent performance and system health
tags: [monitoring, metrics, observability, debugging]
---

# Monitoring Skill

Use this skill to monitor KOR agent performance and system health.

## Commands

- `/metrics` - View current metrics summary
- `/sessions` - List active sessions

## Tracked Metrics

- **Agent lifecycle**: starts, ends, errors
- **Tool calls**: invocations, latency, success rate
- **Sessions**: duration, message count

## Viewing Metrics

Run the collector script directly:

```bash
python3 ${KOR_PLUGIN_ROOT}/scripts/collector.py summary
```

## Best Practices

1. **Review daily**: Check metrics summary to identify issues
2. **Track errors**: Low success rates indicate problems
3. **Monitor latency**: High tool duration may need optimization
