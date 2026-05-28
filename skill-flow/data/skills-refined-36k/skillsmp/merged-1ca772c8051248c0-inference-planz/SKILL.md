---
name: inference-planz
description: Use this skill to manage and configure the inference-planz plugin for multi-agent intelligence workflows.
---

# Inference Planz

The **Inference Planz** plugin assists in creating structured workflows for AI tasks by analyzing prompts, clarifying requirements, and generating actionable plans.

## Overview

### Key Features
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
| `/inference-planz:configure <arguments>` | Modify plugin settings. |

## Quick Start

To run a planning pipeline, use:
```
/inference-planz:run <your_prompt>
```
This will initiate the process of researching, clarifying, and planning based on your input.

## Pipeline Stages

### Stage 1: Input Normalization
- Trims whitespace.
- Detects language and tone.
- Extracts entities, constraints, and objectives.

### Stage 2: Research Agent
- Analyzes user intent.
- Identifies missing details and risks.
- Recommends implementation approaches.

### Stage 3: Survey Agent
- Generates multiple-choice questions covering various aspects of the task.

### Stage 4: Plan Agent
- Creates a production-grade roadmap with phases, checkpoints, and deliverables.

## Configuration

### Configuration Commands
You can modify the plugin settings using the following commands:

- **Enable/Disable**: `enable` or `disable`
- **Debug Mode**: `debug on` or `debug off`
- **Timeouts**: `timeout research <seconds>`, `timeout survey <seconds>`, `timeout plan <seconds>`, `timeout total <seconds>`
- **Survey Settings**: `survey questions <min> <max>`, `survey options <min> <max>`, `survey other on|off`
- **Reset**: `reset` to default configuration
- **Show**: `show` to display current configuration

### Configuration File
Settings are saved in `.claude/planz.config.json`. You can specify a different path using:
```
config path <path>
```

### Example Commands
```
/inference-planz:configure debug on
/inference-planz:configure timeout research 90
/inference-planz:configure survey questions 5 12
/inference-planz:configure reset
/inference-planz:configure show
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `INFERENCE_PLANZ_ENABLED` | Enable/disable plugin | true |
| `INFERENCE_PLANZ_DEBUG` | Enable debug output | false |
| `INFERENCE_PLANZ_TIMEOUT` | Total pipeline timeout (seconds) | 180 |

## Integration with Other Plugins
Works seamlessly with:
- **inference-confidenz**: Confidence scoring for responses.
- **inference-continuez**: Auto-continuation based on confidence.

## Troubleshooting
- **Pipeline timeout**: Increase `INFERENCE_PLANZ_TIMEOUT` or individual agent timeouts.
- **Agent failures**: Check logs for details.
- **Empty output**: Ensure your prompt is not empty.

## Links
- Repository: [GitHub](https://github.com/Blerbz/blerbz-plugins)
- Issues: [GitHub Issues](https://github.com/Blerbz/blerbz-plugins/issues)