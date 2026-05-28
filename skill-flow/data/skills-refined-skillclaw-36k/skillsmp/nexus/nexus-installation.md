---
name: nexus-installation
description: "Nexus installation and setup. Use when asking 'install nexus', 'nexus setup', or 'nexus requirements'."
---

# Nexus Installation Guide

> **Skill Metadata**
> Category: `nexus`
> Priority: `HIGH`
> SDK Version: `0.9.25+`
> Related Skills: [`nexus-specialist`](nexus-specialist.md), [`nexus-quickstart`](nexus-quickstart.md)

## Installation

```bash
# Install Nexus
pip install kailash-nexus

# Verify installation
python -c "from nexus import Nexus; print('Nexus installed successfully')"
```

## Requirements

- Python 3.9+
- kailash SDK 0.9.25+
- FastAPI (for API mode)
- Click (for CLI mode)

## Quick Setup

```python
from nexus import Nexus
from kailash.workflow.builder import WorkflowBuilder

# Create workflow
workflow = WorkflowBuilder()
workflow.add_node("LLMNode", "chat", {
    "provider": "openai",
    "model": "gpt-4",
    "prompt": "{{input.message}}"
})

# Create Nexus app
app = Nexus(workflow.build(), name="ChatApp")

# Run all channels
if __name__ == "__main__":
    app.run()
```

## Running Modes

```bash
# API mode (default)
python app.py --mode api --port 8000

# CLI mode
python app.py --mode cli

# MCP mode (for Claude Desktop)
python app.py --mode mcp
```

## Documentation

- **Installation**: [`sdk-users/apps/nexus/01-installation.md`](../../../../sdk-users/apps/nexus/01-installation.md)

<!-- Trigger Keywords: install nexus, nexus setup, nexus requirements, nexus installation -->
