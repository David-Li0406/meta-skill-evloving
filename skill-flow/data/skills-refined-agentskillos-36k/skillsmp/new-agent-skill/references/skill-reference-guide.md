# Skill `master` guide

**`GOAL`**: provide a single source of truth for creating and updating
agent skills.

**`NOTE`**: this guide targets agent consumption. It contains zero
fluff. Agents must strictly adhere to these rules.

---

## 1. Core Protocol

### 1.1 Status codes

**Rule**: the first line of output must contain `STATUS: message`.

| Status    | Meaning                | Exit Code | Usage                                       |
| :-------- | :--------------------- | :-------- | :------------------------------------------ |
| `SUCCESS` | Completed with changes | 0         | Work done, proceed to next step.            |
| `WARN`    | Completed, no changes  | 0         | Nothing to do, skip cleanup/optional steps. |
| `ERROR`   | Failed                 | 1         | Critical failure, halt immediately.         |

**Extended codes** (Domain-specific): `APPROVED`, `REJECTED_EDIT`,
`REJECTED_ABORT` (for example, for user interaction).

---

## 2. Skill structure template

**File**: `skills/<skill-name>/SKILL.md`

```markdown
---
name: skill-name
description: Brief description (1-3 sentences). Use when [context].
---

# [Readable Title]

**`GOAL`**: [What the skill accomplishes]

**`WHEN`**: [When to invoke this skill]

**`NOTE`**: [Key constraint] (optional)

## Efficiency directives

[Insert Template 3.1]

## Task management

[Insert Template 3.2]

## Workflow

[Insert Pattern from Section 4]

## Output

**Files created/modified:**

- `filename` - Description

**Status communication:** [Describe status reporting behavior]
```

---

## 3. Component templates

### 3.1 Efficiency directives

```markdown
## Efficiency directives

- Batch operations on file groups, avoid individual file processing
- Use parallel execution when possible
- Target only relevant files
- Reduce token usage
```

### 3.2 Task management

```markdown
## Task management

Use your task management tool to break down, plan, and optimize
workflow.
```

---

## 4. Orchestration patterns

### 4.1 `Simple` skill (linear)

**Use when**: single responsibility, no sub-skills, 3-5 steps.

```markdown
## Workflow

- Step 1 action
- Step 2 action
- Step 3 action
- **`DONE`**
```

### 4.2 Sequential orchestration (looping)

**Use when**: fixed order, status capture, automatic loop control.

```markdown
## Workflow

Follow these steps in sequence:

### Step 1: [Action]

- Check [prerequisite]. If [condition], skip to Step N.

### Step 2: [Sub-skill]

- Invoke `sub-skill-1`.
- Capture status (`SUCCESS`, `WARN`, `ERROR`).
- Handle status:
  - `ERROR`: Halt and report.
  - `WARN`: [Action].
  - `SUCCESS`: Continue.

### Step 3: [Loop Control]

- Check for remaining work.
- If work remains: automatically loop back to Step 2.
- If done: Continue to Step 4.

### Step 4: Final Status

- Report summary.
- **`DONE`**
```

### 4.3 Conditional orchestration (branching)

**Use when**: dependencies, optional steps, smart initialization.

```markdown
## Workflow

### Step 1: Prerequisite Check

- Check if [resource] exists.
- If missing: Invoke `init-skill`.
  - `ERROR`: Halt.
  - `SUCCESS`/`WARN`: Continue.

### Step 2: Main Operation

- Invoke `main-skill`.
- Capture status.
- `WARN` (no work): Skip Step 3, go to Step 4.
- `SUCCESS`: Continue to Step 3.

### Step 3: Cleanup (Conditional)

- Only run if Step 2 was `SUCCESS`.
- Invoke `cleanup-skill`.

### Step 4: Completion

- Report summary.
- **`DONE`**
```

---

## 5. Scripting standards

### 5.1 Portability and compliance

- **`POSIX` compliance**: Ensure scripts remain portable across
  `POSIX`-compliant systems.
- **Shell selection**: Use `#!/bin/sh` for portability. Use
  `#!/bin/bash` only when specific features (for example, associative
  arrays) require it.
- **Best practices**:
  - Use `set -e` to exit on error (or handle errors explicitly).
  - Use `set -u` to treat unset variables as errors.
  - Quote all variables to prevent word splitting and `globbing`.
  - Use `$(...)` instead of backticks for command substitution.
  - Use `mktemp` for secure temporary file creation.

---

## 6. Anti-patterns (strict prohibitions)

1.  **`God` skill**: Doing >1 verb (for example, "Stage and commit").
    **Fix**: Split into sub-skills.
2.  **Implicit dependencies**: Assuming files exist. **Fix**: Explicit
    checks with `ERROR` exit.
3.  **Silent failures**: Exiting 0 without status. **Fix**: Always
    `echo "STATUS: msg"`.
4.  **Format chaos**: Mixing headers. **Fix**: Use `GOAL`.
5.  **Duplication**: Copying directives. **Fix**: Use templates from
    Section 3.
6.  **Inefficient loops**: Processing files individually. **Fix**: Batch
    operations.
7.  **Blind orchestration**: Ignoring sub-skill status. **Fix**: Capture
    and handle `SUCCESS`/`WARN`/`ERROR`.

```

```
