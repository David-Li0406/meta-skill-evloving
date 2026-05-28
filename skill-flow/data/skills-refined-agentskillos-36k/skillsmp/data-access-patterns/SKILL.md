---
name: data-access-patterns
description: |
  This skill provides guidance on accessing session data efficiently in ultrawork.
  Covers JSON vs Markdown rules, token efficiency rationale, and common patterns.
  Required knowledge for all ultrawork agents (explorer, planner, worker, verifier, reviewer).
---

# Data Access Patterns

## IMPORTANT: Placeholder Notation

This document uses placeholder syntax to indicate values that must be substituted from your agent prompt:

- `{SCRIPTS_PATH}` - Replace with the actual SCRIPTS_PATH value from your prompt
- `${CLAUDE_SESSION_ID}` - Replace with the actual session ID from your prompt

**These are NOT bash environment variables.** They are text placeholders documenting what values you should use.

**Example:**
- Documentation shows: `bun "{SCRIPTS_PATH}/task-get.js" --session ${CLAUDE_SESSION_ID}`
- Your prompt provides: `SCRIPTS_PATH: /Users/name/.claude/plugins/.../scripts` and `CLAUDE_SESSION_ID: abc-123`
- You should execute: `bun "/Users/name/.claude/plugins/.../scripts/task-get.js" --session abc-123`

## Core Rule: JSON via Scripts, Markdown via Read

**Always use scripts for JSON data. Never use Read tool directly on JSON files.**

| Data Type | Access Method | Tool |
|-----------|---------------|------|
| session.json | `session-get.js` | Bash |
| context.json | `context-get.js` | Bash |
| tasks/*.json | `task-get.js`, `task-list.js` | Bash |
| exploration/*.md | Direct file read | Read |
| docs/plans/*.md | Direct file read | Read |

## Why Scripts for JSON?

### 1. Token Efficiency

JSON structure wastes significant context tokens:

```json
{
  "version": "6.1",
  "session_id": "abc-123",
  "working_dir": "/path/to/project",
  "phase": "PLANNING",
  "exploration_stage": "overview",
  ...
}
```

Every brace, quote, comma, and key name consumes tokens. For large session files with evidence arrays, this can waste thousands of tokens.

**Script output with `--field` flag**:
```bash
bun "{SCRIPTS_PATH}/session-get.js" --session ${CLAUDE_SESSION_ID} --field phase
# Output: PLANNING
```

Returns only the value you need—no JSON structure overhead.

### 2. Field Extraction

Scripts support precise data extraction:

```bash
# Single field
bun "{SCRIPTS_PATH}/session-get.js" --session ${CLAUDE_SESSION_ID} --field phase

# Nested field (dot notation)
bun "{SCRIPTS_PATH}/session-field.js" --session ${CLAUDE_SESSION_ID} --field options.auto_mode

# AI-friendly summary
bun "{SCRIPTS_PATH}/context-get.js" --session ${CLAUDE_SESSION_ID} --summary
```

**Benefits**:
- Extract only needed data
- Support for nested field access
- Generate AI-optimized markdown summaries

### 3. Error Handling

Scripts provide consistent validation:

```bash
# Missing session
bun "{SCRIPTS_PATH}/session-get.js" --session invalid-id
# Error: Session not found: invalid-id

# Missing field
bun "{SCRIPTS_PATH}/task-get.js" --session ${CLAUDE_SESSION_ID} --id 999
# Error: Task not found: 999
```

Direct JSON reads require manual error handling for:
- File not found
- Invalid JSON
- Missing fields
- Type validation

### 4. Storage Format Abstraction

Scripts insulate agents from storage changes:
- File location moves
- Schema version updates
- Field renames
- Structure refactoring

Agents continue working with the same script interface.

### 5. Compression for AI

Scripts generate AI-friendly formats:

```bash
# Task summary (markdown, not JSON)
bun "{SCRIPTS_PATH}/task-summary.js" --session ${CLAUDE_SESSION_ID} --task 1

# Evidence index (structured for comprehension)
bun "{SCRIPTS_PATH}/evidence-summary.js" --session ${CLAUDE_SESSION_ID}
```

These formats optimize for AI understanding, not data transfer.

## Common Access Patterns

### Pattern 1: Check Current Phase

```bash
# Get phase to determine allowed operations
PHASE=$(bun "{SCRIPTS_PATH}/session-get.js" --session ${CLAUDE_SESSION_ID} --field phase)

if [ "$PHASE" = "PLANNING" ]; then
  echo "Design phase: no code edits allowed"
fi
```

### Pattern 2: List Open Tasks

```bash
# Get tasks needing work
bun "{SCRIPTS_PATH}/task-list.js" --session ${CLAUDE_SESSION_ID} \
  --status open \
  --format json
```

### Pattern 3: Read Task Details

```bash
# Get full task data
bun "{SCRIPTS_PATH}/task-get.js" --session ${CLAUDE_SESSION_ID} --id 1

# Get specific field
bun "{SCRIPTS_PATH}/task-get.js" --session ${CLAUDE_SESSION_ID} --id 1 --field status
```

### Pattern 4: Update Task with Evidence

```bash
# Add evidence to task
bun "{SCRIPTS_PATH}/task-update.js" --session ${CLAUDE_SESSION_ID} --id 1 \
  --add-evidence "npm test: 15/15 passed, exit 0"

# Mark task complete
bun "{SCRIPTS_PATH}/task-update.js" --session ${CLAUDE_SESSION_ID} --id 1 \
  --status resolved \
  --add-evidence "All criteria met"
```

### Pattern 5: Read Exploration Context

```bash
# Get AI-friendly context summary
bun "{SCRIPTS_PATH}/context-get.js" --session ${CLAUDE_SESSION_ID} --summary

# Get specific field
bun "{SCRIPTS_PATH}/context-get.js" --session ${CLAUDE_SESSION_ID} --field key_files
```

### Pattern 6: Read Exploration Details (Markdown)

```bash
# Markdown files can be read directly
SESSION_DIR=~/.claude/ultrawork/sessions/${CLAUDE_SESSION_ID}
```

Then use Read tool:
```
Read("$SESSION_DIR/exploration/overview.md")
Read("$SESSION_DIR/docs/plans/design.md")
```

### Pattern 7: Get Session Directory Path

```bash
# Session directory (use direct path, not a script)
SESSION_DIR=~/.claude/ultrawork/sessions/${CLAUDE_SESSION_ID}

# Then access files directly
ls "$SESSION_DIR/tasks/"
cat "$SESSION_DIR/exploration/overview.md"
```

### Pattern 8: Query Evidence Log

```bash
# Get recent test results
bun "{SCRIPTS_PATH}/evidence-query.js" --session ${CLAUDE_SESSION_ID} \
  --type test_result \
  --last 5

# Search evidence
bun "{SCRIPTS_PATH}/evidence-query.js" --session ${CLAUDE_SESSION_ID} \
  --search "npm test"

# Get evidence for specific task
bun "{SCRIPTS_PATH}/evidence-query.js" --session ${CLAUDE_SESSION_ID} \
  --task 1
```

## Anti-Patterns (DO NOT USE)

### ❌ Direct JSON Read

```bash
# WRONG: Wastes tokens, requires manual parsing
Read("~/.claude/ultrawork/sessions/${CLAUDE_SESSION_ID}/session.json")
```

### ❌ Manual JSON Parsing

```bash
# WRONG: Fragile, verbose, error-prone
cat session.json | grep '"phase"' | cut -d'"' -f4
```

### ❌ Hardcoded Paths

```bash
# WRONG: Breaks when paths change
cat ~/.claude/ultrawork/sessions/abc-123/tasks/1.json
```

Use scripts with `${CLAUDE_SESSION_ID}` instead.

## Quick Reference

| Need | Script | Example |
|------|--------|---------|
| Session phase | `session-get.js` | `--field phase` |
| Session directory | Direct path | `SESSION_DIR=~/.claude/ultrawork/sessions/${CLAUDE_SESSION_ID}` |
| Task details | `task-get.js` | `--id 1` |
| Task status | `task-get.js` | `--id 1 --field status` |
| Open tasks | `task-list.js` | `--status open` |
| Context summary | `context-get.js` | `--summary` |
| Exploration docs | Read tool | `Read("$SESSION_DIR/exploration/overview.md")` |
| Evidence query | `evidence-query.js` | `--type test_result --last 5` |
| Add evidence | `task-update.js` | `--id 1 --add-evidence "..."` |

## Token Savings Example

**Direct JSON read of session.json** (~500 lines):
- Tokens: ~3000 (includes all structure, unused fields)

**Script with `--field phase`**:
- Tokens: ~5 (just the value "PLANNING")

**Savings**: 99.8% token reduction for single field access.

For multiple field lookups across session lifecycle, scripts save tens of thousands of tokens in main context.
