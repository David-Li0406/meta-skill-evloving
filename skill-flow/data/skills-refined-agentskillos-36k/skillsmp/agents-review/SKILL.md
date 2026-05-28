---
name: agents-review
description: Review code changes using src.agents.scripts.review after edits. Use when you need multi-provider feedback on diffs, staged changes, or the last commit, or when focusing on a review theme like security.
---

# Agents Review

## Overview

Use this skill to run multi-provider review after changes, especially before finalizing or committing.

## Quick start

Review all changes in the working tree.

```bash
uv run python -m src.agents.scripts.review
```

## Common scopes

Review only staged changes.

```bash
uv run python -m src.agents.scripts.review review.scope=staged
```

Review the last commit.

```bash
uv run python -m src.agents.scripts.review review.scope=head
```

Focus the review on a theme like security.

```bash
uv run python -m src.agents.scripts.review 'review.focus=security'
```
