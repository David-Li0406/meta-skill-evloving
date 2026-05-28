---
name: julien-cmd-routing-stats
description: Display routing correlation statistics - how well the skill router predicts actual skill usage
author: Julien
version: 1.0.0
category: infrastructure
type: command
triggers:
  - routing stats
  - routing statistics
  - show routing stats
  - correlation stats
  - routing accuracy
  - skill routing stats
  - analyse routing
  - statistiques routing
  - router performance
---

# Routing Statistics

Display routing correlation statistics to measure how well the skill router predicts actual skill usage.

## Action

Run the analyze-routing-correlation script:

```bash
node ~/.claude/scripts/analyze-routing-correlation.js --verbose
```

## What It Shows

- **Total invocations**: How many skills were invoked in the time period
- **Routing matched**: Router correctly predicted the skill used
- **Routing mismatch**: Router suggested a different skill
- **No routing**: Direct invocation without routing suggestion

## Verbose Output

With `--verbose`, shows:
- Top 10 most used skills with routing accuracy
- Common mismatches (router suggested X but Y was used)

## Options

- `--days N`: Analyze last N days (default: 7)
- `--verbose` or `-v`: Show detailed breakdown

## Example

```bash
# Last 7 days, verbose
node ~/.claude/scripts/analyze-routing-correlation.js --verbose

# Last 30 days
node ~/.claude/scripts/analyze-routing-correlation.js --days 30 --verbose
```
