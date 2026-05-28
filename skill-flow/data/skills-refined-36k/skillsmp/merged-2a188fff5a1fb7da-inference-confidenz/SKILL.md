---
name: inference-confidenz
description: Use this skill to display help documentation and current status for the Inference Confidenz plugin.
---

# Inference Confidenz Help and Status

## Overview

**Inference Confidenz** displays a confidence percentage (0-99%) alongside every Claude Code response, analyzing response quality, task completion certainty, and more.

## Commands

| Command | Description |
|---------|-------------|
| `/inference-confidenz:help` | Show help documentation |
| `/inference-confidenz:configure` | Configure settings |
| `/inference-confidenz:status` | Show current status |

## Confidence Levels

- **High (75-99%)**: Strong completion, definitive language, no errors
- **Medium (40-74%)**: Partial completion, some uncertainty
- **Low (0-39%)**: Hedging language, errors present, incomplete

## Configuration

Create `.claude/confidenz.config.json`:

```json
{
  "enabled": true,
  "display": "minimal",
  "logHistory": false,
  "thresholds": {
    "high": 75,
    "medium": 40
  }
}
```

## Display Formats

- `minimal`: `CZ 87%`
- `detailed`: `CZ 87% [high]`

## Environment Variables

- `CONFIDENZ_ENABLED`: Set to `false` to disable
- `CONFIDENZ_DISPLAY`: Set display format

## Status Check

To display the current status and recent confidence history, run the following command:

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/status.sh"
```

This will show:
- Whether Confidenz is enabled
- Current display format
- Recent confidence scores (if logging is enabled)
- Configuration file location

## Links

- GitHub: [Blerbz Plugins](https://github.com/Blerbz/blerbz-plugins)
- Issues: [Blerbz Issues](https://github.com/Blerbz/blerbz-plugins/issues)