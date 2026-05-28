---
name: codex
description: |
  Use Codex CLI (OpenAI) for code consultation and review.
  Triggers: "codex", "ask codex", "code review", "review this"
  Use cases: (1) Message/copy review, (2) Code review, (3) Design consultation, (4) Bug investigation, (5) Complex problem research
---

# Codex

Skill for running code review and analysis using Codex CLI.

## Command

codex exec --full-auto --sandbox read-only --cd <project_directory> "<request>"

## Parameters

| Parameter             | Description                         |
| --------------------- | ----------------------------------- |
| `--full-auto`         | Run in fully automatic mode         |
| `--sandbox read-only` | Read-only sandbox for safe analysis |
| `--cd <dir>`          | Target project directory            |
| `"<request>"`         | Request content                     |

## Examples

### Code Review

codex exec --full-auto --sandbox read-only --cd /path/to/project "Review this project's code and point out improvements"

### Bug Investigation

codex exec --full-auto --sandbox read-only --cd /path/to/project "Investigate the cause of authentication errors"

## Execution Steps

1. Receive request from user
2. Identify target project directory
3. Execute Codex with the command format above
4. Report results to user
