---
name: notebooklm
description: Use this skill to query your Google NotebookLM notebooks directly from Claude Code for source-grounded, citation-backed answers from Gemini.
---

# NotebookLM Research Assistant Skill

Interact with Google NotebookLM to query documentation with Gemini's source-grounded answers. Each question opens a fresh browser session, retrieves the answer exclusively from your uploaded documents, and closes.

## When to Use This Skill

Trigger when user:
- Mentions NotebookLM explicitly
- Shares NotebookLM URL (`https://notebooklm.google.com/notebook/...`)
- Asks to query their notebooks/documentation
- Wants to add documentation to NotebookLM library
- Uses phrases like "ask my NotebookLM", "check my docs", "query my notebook"

## ⚠️ CRITICAL: Add Command - Smart Discovery

When user wants to add a notebook without providing details:

**SMART ADD (Recommended)**: Query the notebook first to discover its content:
```bash
# Step 1: Query the notebook about its content
python scripts/run.py ask_question.py --question "What is the content of this notebook? What topics are covered? Provide a complete overview briefly and concisely" --notebook-url "[URL]"

# Step 2: Use the discovered information to add it
python scripts/run.py notebook_manager.py add --url "[URL]" --name "[Based on content]" --description "[Based on content]" --topics "[Based on content]"
```

**MANUAL ADD**: If user provides all details:
- `--url` - The NotebookLM URL
- `--name` - A descriptive name
- `--description` - What the notebook contains (REQUIRED!)
- `--topics` - Comma-separated topics (REQUIRED!)

NEVER guess or use generic descriptions! If details are missing, use Smart Add to discover them.

## Critical: Always Use run.py Wrapper

**NEVER call scripts directly. ALWAYS use `python scripts/run.py [script]`:**

```bash
# ✅ CORRECT - Always use run.py:
python scripts/run.py auth_manager.py status
python scripts/run.py notebook_manager.py list
python scripts/run.py ask_question.py --question "..."

# ❌ WRONG - Never call directly:
python scripts/auth_manager.py status  # Fails without venv!
```

The `run.py` wrapper automatically:
1. Creates `.venv` if needed
2. Installs all dependencies
3. Activates environment
4. Executes script properly

## Core Workflow

### Step 1: Check Authentication Status
```bash
python scripts/run.py auth_manager.py status
```