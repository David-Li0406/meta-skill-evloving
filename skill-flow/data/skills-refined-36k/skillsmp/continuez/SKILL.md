---
name: continuez
description: Manage inference-continuez auto-continuation settings
allowed-tools: Read, Write, Bash
user-invocable: true
---

# Inference Continuez Settings

Manage the inference-continuez plugin settings for auto-continuation.

## Current Settings

Show the current configuration by reading the settings file and displaying it to the user.

If "$ARGUMENTS" contains:
- "threshold <number>": Set the confidence threshold to that number (0-99)
- "enable": Enable auto-continuation
- "disable": Disable auto-continuation
- "show" or empty: Display current settings

After making any changes, confirm the new settings to the user.

## Settings Reference

- **confidence_threshold** (0-99): Minimum confidence score to auto-continue. Default: 80
- **enabled** (true/false): Whether auto-continuation is active. Default: true
- **log_decisions** (true/false): Log decisions to stderr. Default: true
- **excluded_patterns**: Patterns that prevent auto-continuation regardless of confidence
