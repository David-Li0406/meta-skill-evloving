---
name: cli-mastery
description: **Tags:** #tools #cli #railway #github #env
---

# CLI Mastery & Environment Protocol

**Tags:** #tools #cli #railway #github #env

## 🚨 Environment Variable Protocol (CRITICAL)

**Core Rule:** Do NOT look for `.env` files.
**Automation:** Use the `run` command wrapper.

### The `run` Command
We have installed a smart wrapper called `run`. It automatically detects if you need Railway secrets and injects them.

**Usage:**
Always prefix your execution commands with `run`.

*   ❌ `python main.py`
*   ✅ `run python main.py` (Automatically becomes `railway run python main.py`)
*   ✅ `run pytest`
*   ✅ `run make dev`

**Verification:**
If `run env | grep DATABASE_URL` returns nothing, then the project is not configured correctly.

---

## 🚅 Railway CLI (`railway`)

### 1. Context
*   **Check Environment:** `railway environment`
*   **List Services:** `railway service`

### 2. Diagnosis
Don't guess. Check the logs.
```bash
# Get the last 50 lines of logs
run railway logs -n 50
```

---

## 🐙 GitHub CLI (`gh`)

### 1. Reading State (JSON is King)
Always use `--json` to get structured data.

```bash
# List open PRs
gh pr list --json number,title,author,state
```

### 2. Actions
```bash
# Create a PR
gh pr create --fill
```
