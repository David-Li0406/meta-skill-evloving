---
name: prompt-builder
description: Use this skill to build complete agent prompts deterministically via a Python script, right before spawning any BAZINGA agent (Developer, QA, Tech Lead, PM, etc.).
---

# Prompt Builder Skill

You are the prompt-builder skill. Your role is to build complete agent prompts by calling `prompt_builder.py`, which handles everything deterministically.

## Overview

This skill builds complete agent prompts by calling a Python script that:
- Reads specializations from the database (task_groups.specializations)
- Reads context from the database (context_packages, error_patterns, reasoning)
- Reads full agent definition files from the filesystem
- Applies token budgets per model
- Validates required markers are present
- Saves the prompt to a file and returns a JSON result

## Prerequisites

- Database must be initialized (`bazinga/bazinga.db` exists)
- Config must be seeded (run `config-seeder` skill first at session start)
- Agent files must exist in the `agents/` directory

## When to Invoke This Skill

- **RIGHT BEFORE** spawning any BAZINGA agent
- When the orchestrator needs a complete prompt for Developer, QA Expert, Tech Lead, PM, Investigator, or Requirements Engineer
- Called ON-DEMAND to get the latest context from the database

## Your Task

When invoked, you must:

### Step 1: Read Parameters File

The orchestrator writes a params JSON file before invoking this skill. Look for it at:

```
bazinga/prompts/{session_id}/params_{agent_type}_{group_id}.json
```

Example: `bazinga/prompts/bazinga_20251217_120000/params_developer_CALC.json`

**Params file format:**
```json
{
  "agent_type": "developer",
  "session_id": "bazinga_20251217_120000",
  "group_id": "CALC",
  "task_title": "Implement calculator",
  "task_requirements": "Create add/subtract functions",
  "branch": "main",
  "mode": "simple",
  "testing_mode": "full",
  "model": "haiku",
  "output_file": "bazinga/prompts/bazinga_20251217_120000/developer_CALC.md"
}
```

**Additional fields for retries:**
```json
{
  "qa_feedback": "Tests failed: test_add expected 4, got 5",
  "tl_feedback": "Error handling needs improvement"
}
```

**Additional fields for CRP (Compact Return Protocol):**
```json
{
  "prior_handoff_file": "bazinga/artifacts/bazinga_20251217_120000/CALC/handoff_developer.json"
}
```

**Additional fields for PM spawns:**
```json
{
  "pm_state": "{...json...}",
  "resume_context": "Resuming after ..."
}
```