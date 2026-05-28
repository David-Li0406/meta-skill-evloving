---
name: arch
description: Architecture-first planning for complex tasks
argument-hint: "[request]"
disable-model-invocation: true
---

# /arch Skill

**Status: Active**

Generate architecture artifacts for a feature request before writing any implementation code. This skill writes only to `.claude/arch/` and does not modify any other files.

## Usage

```
/arch Add user authentication with JWT tokens
```

## Behavior

1. Gather context (read-only operations)
2. Write artifacts to `.claude/arch/`

---

## Step 1: Gather Context

Run these commands and read the output:

```bash
# Detect project type
python scripts/detect_env.py --pretty

# List top-level structure
ls -la
```

Then read relevant config files if they exist:
- `package.json` (if Node project)
- `pyproject.toml` (if Python project)
- `go.mod` (if Go project)

---

## Step 2: Generate Artifacts

Create `.claude/arch/` directory if it doesn't exist. Then write these files:

### 2.1 ARCHITECTURE.md

Structure (in this order):

```markdown
# Architecture: [Short Title]

## Summary
[1-2 paragraph overview of the proposed solution]

## Assumptions
- [Explicit assumption 1]
- [Explicit assumption 2]

## Proposed Components
- **[Component A]**: [responsibility]
- **[Component B]**: [responsibility]

## Data Flow
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Interfaces
- **Files touched**: [list]
- **APIs/functions**: [list]

## Error Handling & Edge Cases
- [Edge case 1]: [how handled]
- [Edge case 2]: [how handled]

## Verification Strategy
- [How we prove it works]
```

### 2.2 DECISIONS.md

```markdown
# Architecture Decisions

## Decision 1: [Title]
- **Decision**: [what we decided]
- **Why**: [reasoning]
- **Alternatives**: [what else we considered]
- **Tradeoffs**: [pros/cons of this choice]

## Decision 2: [Title]
...
```

### 2.3 PLAN.md

```markdown
# Implementation Plan

## Overview
[Brief summary of the plan]

## Steps

### Step 1: [step-001] [Title]
- **Goal**: [what this accomplishes]
- **Files**: [files likely touched]
- **Verification**: [how to verify]

### Step 2: [step-002] [Title]
...
```

### 2.4 TASK_GRAPH.json

Must conform to `docs/spec/TASK_GRAPH.md`:

```json
{
  "schema_version": 1,
  "request": "[the user's request]",
  "created_at": "[ISO 8601 timestamp]",
  "steps": [
    {
      "id": "step-001",
      "title": "[title]",
      "goal": "[goal]",
      "allowed_paths": ["src/path/*.ts"],
      "verification": ["npm test"],
      "success_criteria": "[what success looks like]"
    }
  ]
}
```

#### Glob Pattern Syntax for `allowed_paths`

The `allowed_paths` field uses glob patterns to specify which files can be modified during a step. These patterns are enforced by hooks during execution.

| Pattern | Matches | Example |
|---------|---------|---------|
| `src/file.py` | Exact file | Only `src/file.py` |
| `src/*.py` | Single directory | `src/main.py`, `src/utils.py` (not `src/sub/file.py`) |
| `src/**/*.py` | Recursive | `src/main.py`, `src/sub/file.py`, `src/a/b/c.py` |
| `src/` | Directory prefix | Anything under `src/` |
| `*.config.js` | Root level | `app.config.js` (not `src/app.config.js`) |
| `**/*.test.ts` | Any depth | `foo.test.ts`, `src/foo.test.ts`, `a/b/c.test.ts` |

**Key rules:**
- `*` matches any characters except `/` (single directory level)
- `**` matches any characters including `/` (recursive)
- Paths are normalized to forward slashes on all platforms
- Be specific to avoid accidentally allowing unintended files

### 2.5 state.json

Must conform to `docs/spec/STATE.md`:

```json
{
  "schema_version": 1,
  "active": true,
  "phase": "planning",
  "request": "[the user's request]",
  "created_at": "[ISO 8601 timestamp]",
  "current_step": null,
  "verify_profile": "[from detect_env.py output]"
}
```

---

## Output Confirmation

After generating all artifacts, output:

```
Architecture artifacts generated in .claude/arch/:
- ARCHITECTURE.md
- DECISIONS.md
- PLAN.md
- TASK_GRAPH.json
- state.json

Review the plan, then run /arch-start to begin execution.
```

---

## Constraints

- **Read-only outside .claude/arch/**: Do not write or edit any files except under `.claude/arch/`
- **Deterministic context**: Always run `detect_env.py` and read config files
- **Schema compliance**: TASK_GRAPH.json and state.json must match their specs
- **Step IDs**: Use `step-NNN` format (step-001, step-002, etc.)
- **allowed_paths**: Use glob patterns (see syntax table above); enforced by hooks during execution
