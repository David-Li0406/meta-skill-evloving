---
name: help
description: Show help and documentation for inference-planz plugin
user-invocable: true
---

# Inference Planz - Help

Display comprehensive help information for the inference-planz plugin.

## Overview

**Inference Planz** is a multi-agent intelligence workflow plugin for Claude Code that helps you:

1. **Understand Prompts Deeply**: Research agent analyzes your intent
2. **Clarify Requirements**: Survey agent generates targeted questions
3. **Plan Execution**: Plan agent creates actionable roadmaps

## Commands

| Command | Description |
|---------|-------------|
| `/inference-planz:run <prompt>` | Execute the full planning pipeline |
| `/inference-planz:planz <prompt>` | Alias for run |
| `/inference-planz:help` | Show this help documentation |
| `/inference-planz:status` | Show current session status |
| `/inference-planz:configure` | Configure plugin settings |

## Quick Start

```
/inference-planz:run Build a REST API for user authentication with JWT tokens
```

This will:
1. Research what authentication patterns are best
2. Ask clarifying questions about your requirements
3. Generate a detailed implementation plan

## Pipeline Stages

### Stage 1: Input Normalization
- Trims whitespace
- Detects language and tone
- Extracts entities, constraints, objectives

### Stage 2: Research Agent
- Deep analysis of user intent
- Identifies missing details and risks
- Recommends implementation approaches (A, B, C with tradeoffs)

### Stage 3: Survey Agent
- Generates 5-10 multiple-choice questions
- Covers goal, scope, constraints, timeline, quality
- Optimized for unblocking planning decisions

### Stage 4: Plan Agent
- Creates production-grade roadmap
- Phases with checkpoints and deliverables
- Includes file structure, interfaces, tests
- Provides relative sizing estimates

## Configuration

Create `.claude/planz.config.json` in your project:

```json
{
  "enabled": true,
  "debug_mode": false,
  "timeouts": {
    "research_agent": 60,
    "survey_agent": 45,
    "plan_agent": 60
  }
}
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `INFERENCE_PLANZ_ENABLED` | Enable/disable plugin | true |
| `INFERENCE_PLANZ_DEBUG` | Enable debug output | false |
| `INFERENCE_PLANZ_TIMEOUT` | Total pipeline timeout (seconds) | 180 |

## Integration with Other Plugins

Works seamlessly with:
- **inference-confidenz**: Confidence scoring for responses
- **inference-continuez**: Auto-continuation based on confidence

## Troubleshooting

**Pipeline timeout**: Increase `INFERENCE_PLANZ_TIMEOUT` or individual agent timeouts

**Agent failures**: Plugin includes fallback behavior - check logs for details

**Empty output**: Ensure your prompt is not empty; plugin will show domain selector

## Links

- Repository: https://github.com/Blerbz/blerbz-plugins
- Issues: https://github.com/Blerbz/blerbz-plugins/issues
