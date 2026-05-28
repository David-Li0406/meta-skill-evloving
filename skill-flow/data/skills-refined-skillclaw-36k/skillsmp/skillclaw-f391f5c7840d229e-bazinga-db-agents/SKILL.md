---
name: bazinga-db-agents
description: Use this skill when logging agent interactions, saving reasoning, tracking tokens, or managing events.
---

# Skill body

You are the bazinga-db-agents skill. You manage agent interaction logs, reasoning capture, token usage, skill outputs, and events.

## When to Invoke This Skill

**Invoke when:**
- Logging agent interactions
- Saving or retrieving agent reasoning
- Tracking token usage
- Recording skill outputs
- Saving or querying events (TL issues, verdicts, etc.)

**Do NOT invoke when:**
- Managing sessions or state → Use `bazinga-db-core`
- Managing task groups or plans → Use `bazinga-db-workflow`
- Managing context packages → Use `bazinga-db-context`

## Script Location

**Path:** `.claude/skills/bazinga-db/scripts/bazinga_db.py`

All commands use this script with `--quiet` flag:
```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet <command> [args...]
```

## Commands

### log-interaction

```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet log-interaction \
  "<session_id>" "<agent_type>" "<message>" <sequence_num>
```

Logs an agent interaction in the orchestration flow.

**Parameters:**
- `agent_type`: `pm`, `developer`, `sse`, `qa_expert`, `tech_lead`, `investigator`, `requirements_engineer`
- `sequence_num`: Integer for ordering

### stream-logs

```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet stream-logs \
  "<session_id>" [limit] [offset]
```

Stream orchestration logs in markdown format. Always returns markdown (no format option).

**Parameters:**
- `limit`: Maximum number of logs to return (default: 50)
- `offset`: Number of logs to skip (default: 0)

### save-reasoning

```bash
# Recommended: Use --content-file to avoid exposing content in process table
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet save-reasoning \
  "<session_id>" "<group_id>" "<agent_type>" "<phase>" \
  --content-file /tmp/reasoning.txt [--confidence N] [--tokens N]

# Alternative: Inline content (avoid for sensitive data)
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet save-reasoning \
  "<session_id>" "<group_id>" "<agent_type>" "<phase>" "<content>" \
  [--confidence N] [--tokens N]
```

Saves agent reasoning with automatic secret redaction.

**⚠️ Security:** Prefer `--content-file` over inline content to avoid exposing reasoning in process listings.

**Phases:** `understanding`, `approach`, `decisions`, `risks`, `blockers`, `pivot`, `completion`