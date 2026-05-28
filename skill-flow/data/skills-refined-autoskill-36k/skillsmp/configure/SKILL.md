---
name: configure
description: Configure inference-planz plugin settings
allowed-tools: Read, Write
user-invocable: true
---

# Inference Planz - Configure

Modify plugin configuration based on "$ARGUMENTS".

## Supported Configuration Commands

Parse "$ARGUMENTS" for these commands:

### Enable/Disable
- `enable` - Enable the plugin
- `disable` - Disable the plugin

### Debug Mode
- `debug on` - Enable debug mode (shows internal context)
- `debug off` - Disable debug mode

### Timeouts
- `timeout research <seconds>` - Set Research Agent timeout
- `timeout survey <seconds>` - Set Survey Agent timeout
- `timeout plan <seconds>` - Set Plan Agent timeout
- `timeout total <seconds>` - Set total pipeline timeout

### Survey Settings
- `survey questions <min> <max>` - Set question count range
- `survey options <min> <max>` - Set options per question range
- `survey other on|off` - Enable/disable "Other" option

### Reset
- `reset` - Reset to default configuration

### Show
- `show` or empty - Display current configuration

## Configuration File

Settings are saved to project-level `.claude/planz.config.json` by default.

To specify a different location:
- `config path <path>` - Set custom config path

## Examples

```
/inference-planz:configure debug on
/inference-planz:configure timeout research 90
/inference-planz:configure survey questions 5 12
/inference-planz:configure reset
/inference-planz:configure show
```

## Configuration Schema

```json
{
  "enabled": true,
  "debug_mode": false,
  "log_decisions": true,
  "timeouts": {
    "research_agent": 60,
    "survey_agent": 45,
    "plan_agent": 60,
    "total_pipeline": 180
  },
  "fallback": {
    "enabled": true,
    "min_survey_questions": 5,
    "use_heuristics_on_failure": true
  },
  "output": {
    "format": "markdown",
    "show_timing": true,
    "show_agent_names": true
  },
  "agents": {
    "research": {
      "max_tokens": 4000,
      "temperature": 0.3
    },
    "survey": {
      "max_questions": 10,
      "min_options_per_question": 3,
      "max_options_per_question": 7,
      "include_other_option": true
    },
    "plan": {
      "max_tokens": 6000,
      "include_provisional_branches": true
    }
  }
}
```

## Output

After applying changes, confirm the new configuration to the user:

```
## Configuration Updated

Changed:
- debug_mode: false -> true

Current configuration saved to: .claude/planz.config.json

Use `/inference-planz:status` to see full settings.
```
