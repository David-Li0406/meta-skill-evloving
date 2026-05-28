---
name: discord-analyze
description: Generate a comprehensive community health report from synced Discord messages
usage: /discord-analyze [--server ID] [--days N] [--compare SERVER_ID]
---

## Persona Context

**REQUIRED:** Before executing this skill, load your configured persona:

```bash
python ${CLAUDE_PLUGIN_ROOT}/../community-agent/tools/persona_status.py --prompt
```

This outputs your persona definition. Apply it when presenting health reports:
- **Voice**: Introduce findings as the persona ("I've analyzed your community...")
- **Recommendations**: Present suggestions in the persona's communication style
- **Tone**: Use the persona's warmth when highlighting concerns or celebrations
- **Framing**: Frame metrics and insights as the persona would explain them

## Description

Analyze synced Discord data to generate a comprehensive community health report. Includes:
- Activity metrics (message volume, channel breakdown, peak times)
- Engagement metrics (reply rate, response time, reactions)
- Contributor analysis (top contributors, diversity)
- Topic clustering (automatic grouping of conversations by theme)
- Trend detection (week-over-week changes)
- Benchmark comparison (healthy/warning/critical thresholds)
- Actionable recommendations

## Prerequisites

- Discord data must be synced first (use `/discord-sync`)
- Minimum 7 days of message history recommended (30 days for trends)

## Usage Examples

```bash
# Analyze your default server
/discord-analyze

# Analyze specific server with 30 days of history
/discord-analyze --server 1196028153085296651 --days 30

# Compare two communities
/discord-analyze --server 1196028153085296651 --compare 1347066703158181888

# Show detailed progress
/discord-analyze --verbose

# Output in different formats
/discord-analyze --format yaml
/discord-analyze --format json
```

## Trigger Phrases

- "analyze Discord"
- "community health"
- "health report"
- "how is my community doing"
- "Discord metrics"
- "analyze community"
- "community analytics"

## Output

Creates two files in the server's data directory:
- `health-report.md` - Human-readable markdown report
- `health-report.yaml` - Structured data for automation

Returns a summary with:
- Overall health score (0-100)
- Key metrics summary
- Top findings and recommendations

## Arguments

| Argument | Description |
|----------|-------------|
| `--server ID` | Server ID to analyze (defaults to config) |
| `--days N` | Days of history to analyze (default: 30) |
| `--compare ID` | Server ID for comparison |
| `--format` | Output format: markdown, yaml, json |
| `--verbose` | Show detailed progress |
| `--output PATH` | Custom output path |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Configuration error |
| 2 | Data error (no synced data) |
| 3 | Analysis error |

## Tips

1. **Sync first**: Run `/discord-sync` to get latest messages
2. **More data = better trends**: Use `--days 90` for trend analysis
3. **Regular monitoring**: Run weekly to track community health
4. **Act on recommendations**: Each report includes prioritized actions

## Related Skills

- `/discord-sync` - Sync messages before analysis
- `/discord-list` - List available servers and channels
- `/discord-read` - Read specific channel messages
