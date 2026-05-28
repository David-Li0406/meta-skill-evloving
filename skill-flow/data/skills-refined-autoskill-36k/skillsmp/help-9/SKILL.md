---
name: help
description: Show Inference Confidenz help and documentation
user-invocable: true
---

# Inference Confidenz Help

Display the help documentation for the Inference Confidenz plugin.

## Overview

**Inference Confidenz** displays a confidence percentage (0-99%) alongside every Claude Code response. It analyzes:

- Response quality and completeness
- Task completion certainty
- Hedging vs. definitive language
- Error indicators and unresolved issues
- Context coherence across sessions

## Commands

| Command | Description |
|---------|-------------|
| `/inference-confidenz:help` | Show this help |
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

## Links

- GitHub: https://github.com/Blerbz/blerbz-plugins
- Issues: https://github.com/Blerbz/blerbz-plugins/issues
