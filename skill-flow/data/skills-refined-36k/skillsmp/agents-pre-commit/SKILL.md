---
name: agents-pre-commit
description: Run pre-commit checks using src.agents.scripts.pre_commit after editing code. Use when you need automated lint/format hooks on changed files or before running tests and review.
---

# Agents Pre Commit

## Overview

Use this skill to run the repo's pre-commit hooks on files changed since HEAD.

## Quick start

```bash
uv run python -m src.agents.scripts.pre_commit
```

## Notes

The script runs pre-commit on `git diff --name-only HEAD` and may delegate fixes to sub-agents.
Logs are saved under `agents_workspace/sub_agents/logs/`.

If `uv` cache permissions fail, use a workspace cache:

```bash
uv --cache-dir agents_workspace/tmp_cache/uv_cache run python -m src.agents.scripts.pre_commit
```
