---
name: foundry-agent
description: Call Foundry agents. Use when user asks to rate a task, prioritize work, or call ratemytask agent.
license: MIT
---

# Foundry Agent Skill

## Setup (one time)

```bash
pip install azure-ai-projects azure-identity
az login
export PROJECT_ENDPOINT="your-endpoint-here"
```

## Usage

```bash
python call_agent_simple.py "Rate my task: fix the bug"
```
