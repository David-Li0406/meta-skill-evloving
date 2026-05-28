---
name: agents-consult
description: Consult multiple LLM providers via src.agents.scripts.consult to get approach suggestions before implementing changes. Use when you need design options, risk checks, or alternative solutions for a task in this repo, especially before complex work.
---

# Agents Consult

## Overview

Use this skill to ask multiple LLM providers for implementation approaches before you start coding.

## Quick start

Run the consult script with a clear prompt.

```bash
uv run python -m src.agents.scripts.consult 'task.prompt=Propose improvements for BLCS generate_dataset.'
```

## Common options

Use the approach-oriented system prompt when you want structured design guidance.

```bash
uv run python -m src.agents.scripts.consult system_prompt=approach 'task.prompt=...'
```

Disable a provider to avoid specific models.

```bash
uv run python -m src.agents.scripts.consult claude.enable=false 'task.prompt=...'
```

## Output

Expect a multi-provider summary with sections like:

```
Sub-agent Consultation Results
[CLAUDE] ...
[CODEX] ...
```
