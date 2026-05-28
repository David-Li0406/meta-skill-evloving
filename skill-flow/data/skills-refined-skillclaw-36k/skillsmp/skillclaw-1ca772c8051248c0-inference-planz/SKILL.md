---
name: inference-planz
description: Use this skill to configure and display help for the inference-planz plugin, which assists in planning and executing multi-agent intelligence workflows.
---

# Skill body

## Overview

**Inference Planz** is a multi-agent intelligence workflow plugin for Claude Code that helps you:

1. **Understand Prompts Deeply**: Research agent analyzes your intent.
2. **Clarify Requirements**: Survey agent generates targeted questions.
3. **Plan Execution**: Plan agent creates actionable roadmaps.

## Commands

| Command | Description |
|---------|-------------|
| `/inference-planz:run <prompt>` | Execute the full planning pipeline. |
| `/inference-planz:planz <prompt>` | Alias for run. |
| `/inference-planz:help` | Show help documentation. |
| `/inference-planz:status` | Show current session status. |
| `/inference-planz:configure` | Configure plugin settings. |

## Quick Start

To run the planning pipeline, use the following command:

```
/inference-planz:run Build a REST API for user authentication with JWT tokens
```

This will:
1. Research what authentication patterns are best.
2. Ask clarifying questions about your requirements.
3. Generate a detailed implementation plan.

## Configuration

Modify plugin configuration using the following commands:

### Enable/Disable
- `enable` - Enable the plugin.
- `disable` - Disable the plugin.

### Debug Mode
- `debug on` - Enable debug mode (shows internal context).
- `debug off` - Disable debug mode.

### Timeouts
- `timeout research <seconds>` - Set Research Agent timeout.
- `timeout survey <seconds>` - Set Survey Agent timeout.
- `timeout plan <seconds>` - Set Plan Agent timeout.
- `timeout total <seconds>` - Set total pipeline timeout.

### Survey Settings
- `survey questions <min> <max>` - Set question count range.
- `survey options <min> <max>` - Set options per question range.
- `survey other on|off` - Enable/disable "Other" option.

### Reset
- `reset` - Reset to default configuration.

### Show
- `show` or empty - Display current configuration.

## Configuration File

Settings are saved to project-level `.claude/planz.config.json` by default. To specify a different location, use:

- `config path <path>` - Set custom config path.

## Configuration Schema

```json
{
  "enabled": true,
  "debug_mode": false,
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