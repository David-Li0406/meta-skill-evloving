---
name: implement-plan
description: Execute an existing implementation plan with step-by-step confirmations
---

# Implement Plan

Execute an existing plan with user confirmations at each step.

**Usage**: "implement plan `<id>`"

---

## Instructions

When the user asks to implement a plan:

### 1. Find the Plan

```bash
ls plan/<id>-*.md
```

Read the plan file and parse all steps.

### 2. Pre-Implementation Checks

Verify git state:

```bash
git status
git branch --show-current
```

- Working directory should be clean (no uncommitted changes)
- Note current branch

### 3. Create/Checkout Feature Branch

If not already on the feature branch:

```bash
git checkout -b feature/<id>-<title>
# or if branch exists:
git checkout feature/<id>-<title>
```

### 4. Ask User Which Steps to Implement

**CRITICAL**: Present the steps and ASK before implementing:

```
Found plan: <id>-<title>

Steps:
1. <Step 1 name> - <brief description>
2. <Step 2 name> - <brief description>
3. <Step 3 name> - <brief description>

Which step(s) would you like me to implement?
- Enter step number (e.g., "1")
- Enter range (e.g., "1-2")
- Enter "all" for all steps
```

**WAIT for user response before proceeding.**

### 5. Implement Each Confirmed Step

For each step the user confirms:

1. **Implement** all tasks in the step
2. **Mark complete** in plan file: `- [ ]` → `- [x]`
3. **Validate** before commit:
   ```bash
   cargo fmt && cargo clippy && cargo test
   ```
4. **Commit** using the message from the plan:
   ```bash
   git add -A
   git commit -m "<commit message from plan>"
   ```

### 6. Update Plan Status

After implementing any steps, update the plan file:
- Change `**Status**: planning` to `**Status**: in-progress`

---

## Example Interaction

**User**: "implement plan 001"

**Assistant**:
```
Found plan: 001-qr-code

Steps:
1. Add QR Code Library - Add qrcode crate and create generation module
2. Template Integration - Add QrCode element and rendering
3. Documentation - Add usage examples and API docs

Which step(s) would you like me to implement?
```

**User**: "1"

**Assistant**: Implements step 1, marks tasks complete, runs validation, commits.

---

## Important Rules

1. **Always ask first** - Never assume which steps to implement
2. **One step at a time** - Complete and commit each step before moving to next
3. **Validate before commit** - Run `cargo fmt && cargo clippy && cargo test`
4. **Update plan file** - Mark tasks `[x]` as you complete them
5. **Use exact commit messages** - Use the commit message specified in the plan

---

## Handling Failures

If validation fails:
1. Fix the issues
2. Re-run validation
3. Only commit when all checks pass

If user wants to stop mid-implementation:
1. Commit completed steps
2. Leave remaining tasks unchecked
3. Status stays `in-progress`

---

## Checklist

For each step implemented:
- [ ] Tasks completed
- [ ] Plan file updated with `[x]` marks
- [ ] `cargo fmt` passes
- [ ] `cargo clippy` passes
- [ ] `cargo test` passes
- [ ] Changes committed with correct message
