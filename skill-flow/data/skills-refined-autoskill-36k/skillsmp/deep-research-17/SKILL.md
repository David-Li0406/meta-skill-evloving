---
name: deep-research
description: Use this to perform in-depth research tasks using the Gemini Deep Research API.
---

# Deep Research Skill

This skill provides access to the Gemini Deep Research API, allowing you to perform in-depth research tasks.

## Commands

### `start`

Starts a new research session.

**Usage:** `node deep-research.js start <filename> [--model <model>] <prompt...>`

- `<filename>`: The file where the interaction ID (and later the result) will be stored.
- `--model <model>`: Optional. The model to use for research (default: `deep-research-pro-preview-12-2025`).
- `<prompt>`: The research query.

**Example:**

```bash
node deep-research.js start my-research.md "Research the impact of quantum computing on cryptography"
```

**Example with custom model:**

```bash
node deep-research.js start my-research.md --model deep-research-pro-preview-01-2026 "Research future trends in AI"
```

### `check`

Checks the status of a research session. If completed, it updates the file with the result.

**Usage:** `node deep-research.js check <filename>`

**Example:**

```bash
node deep-research.js check my-research.md
```

### `poll`

Polls the research session status periodically until it completes.

**Usage:** `node deep-research.js poll <filename> [interval_seconds]`

- `[interval_seconds]`: Optional. Polling interval in seconds (default: 10).

**Example:**

```bash
node deep-research.js poll my-research.md 30
```
