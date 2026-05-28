---
name: agents-test
description: Run targeted tests using src.agents.scripts.test after code changes. Use when you need to execute only affected tests, pass a custom pytest command, or collect JSON test summaries with sub-agent fixes.
---

# Agents Test

## Overview

Use this skill to run only the affected tests and capture a JSON summary.

## Quick start

Run the default test command (pytest with `-q -n auto`) through the sub-agent.

```bash
uv run python -m src.agents.scripts.test
```

## Targeted tests (required by repo policy)

Always pass a narrowed `task.test_cmd` for affected files.

```bash
uv run python -m src.agents.scripts.test \
  'task.test_cmd=uv run --no-sync pytest -q -n auto tests/unit/test_affected.py'
```

Use a specific test case when needed.

```bash
uv run python -m src.agents.scripts.test \
  'task.test_cmd=uv run --no-sync pytest -q tests/test_example.py::test_case'
```

## Output and logs

The script prints a single-line JSON summary and stores logs under
`agents_workspace/sub_agents/logs/pytest_*.log`.

## Cache workaround

If `uv` cache permissions fail, use a workspace cache:

```bash
uv run python -m src.agents.scripts.test \
  'task.test_cmd=uv --cache-dir agents_workspace/tmp_cache/uv_cache run --no-sync pytest -q tests/...'
```
