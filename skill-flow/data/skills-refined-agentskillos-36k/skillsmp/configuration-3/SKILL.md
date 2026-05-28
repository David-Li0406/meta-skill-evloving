---
name: configuration
description: Guidelines for consuming and storing configuration.
---

# Configuration

## Consume Configuration
Configuration parameters should be accessible via:
1.  **Command Line Flag**: Use dot notation to match file structure (e.g., `--slack.api.key="abcde"`).
2.  **Environment Variable**: With a prefix (e.g., `ANNOUNCE_SLACK_API_KEY="abcde"`).
3.  **File**: See below.

Use [spf13/viper](https://github.com/spf13/viper) for implementation.

## Store Configuration Files
Store configuration in a path that follows the **XDG standards**.
Use [ardg/xdg](https://github.com/ardg/xdg) for finding or writing to those files.
