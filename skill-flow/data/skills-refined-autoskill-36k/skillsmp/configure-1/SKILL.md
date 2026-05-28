---
name: configure
description: Configure Inference Confidenz settings
argument-hint: "[enable|disable|display minimal|display detailed|log on|log off]"
allowed-tools: Bash
user-invocable: true
---

# Configure Inference Confidenz

Configure the Inference Confidenz plugin settings.

```!
"${CLAUDE_PLUGIN_ROOT}/scripts/configure.sh" $ARGUMENTS
```

## Usage

- `/inference-confidenz:configure enable` - Enable confidence display
- `/inference-confidenz:configure disable` - Disable confidence display
- `/inference-confidenz:configure display minimal` - Minimal display format
- `/inference-confidenz:configure display detailed` - Detailed display with level
- `/inference-confidenz:configure log on` - Enable history logging
- `/inference-confidenz:configure log off` - Disable history logging
- `/inference-confidenz:configure status` - Show current configuration

The configuration is saved to `.claude/confidenz.config.json` in your project.
