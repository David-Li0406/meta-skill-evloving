# Reflect Phase

Reflect on what went wrong with the tackle process and improve the skill.

## Purpose

This step runs **immediately after PR submission** (not after merge). Capture friction and errors while fresh.

**CRITICAL**: The reflect step is how tackle learns and improves. Skipping evaluation or writing "Clean run" without review loses valuable learning data. Take this step seriously.

---

## Reflect Checklist (EVALUATE BEFORE CLOSING)

**Do not write "Clean run" until you've reviewed each category:**

### 1. Skill/Formula Issues?
- Were any instructions wrong or unclear?
- Did any commands fail due to wrong flags?
- Were steps missing or in wrong order?
- Did gates work correctly?

### 2. Research Issues?
- Did we miss existing work (closed issues, open PRs)?
- Was upstream research stale or incomplete?
- Did we duplicate someone else's effort?

### 3. Agent Behavior Issues?
- Did I jump to conclusions without investigating?
- Did I propose a fix that turned out to be wrong?
- Did I forget any steps?
- Did I need user correction?

### 4. Molecule Cleanup?
- Are ALL steps closed (not just reflect)?
- Is the ROOT MOLECULE closed?
- Did I record issues in close_reason for pattern detection?

**Only write "Clean run - no issues" if you've reviewed ALL categories and found nothing.**

---

## What to Log

**IMPORTANT**: Only log issues that tackle could help prevent in future runs.

### IN SCOPE: Tackle skill issues
- Command failures due to wrong flags in instructions
- Missing `--no-daemon` or other required flags
- Confusing workflow steps or unclear instructions
- Missing guidance that applies to ALL tackle runs
- State management issues (handoff, molecule attachment)
- Gate workflow problems

### IN SCOPE: Systemic issues tackle could address
- Working in wrong directory/git clone
- Forgetting to check for existing work before starting
- Common agent mistakes that guardrails could prevent
- Environment assumptions that should be verified

### OUT OF SCOPE (task-specific issues)
- Test failures in the code being submitted
- Upstream codebase quirks or conventions
- Merge conflicts or rebasing issues
- PR review feedback about the code

**Rule of thumb**: Could tackle reasonably add guidance/checks to prevent this? If yes, log it. If it's inherent to the specific task, don't.

## Pattern Detection via Molecule History

Tackle molecules are labeled `formula:tackle` for querying. Molecules with friction are also labeled `tackle:friction`. Use past molecules to detect patterns:

```bash
source "$SKILL_DIR/resources/scripts/query-friction.sh"
# Or run directly: bash "$SKILL_DIR/resources/scripts/query-friction.sh"
```

Check notes and close_reason fields for recurring issues before proposing fixes.

## When to Fix

### Fix Immediately (no pattern needed)
Objective errors that will always fail:
- Wrong command flags (`--silent` doesn't exist)
- Missing required flags (`--no-daemon` required but not in instructions)
- Syntax errors in example commands
- Incorrect command names or paths

Predictable inefficiencies that will always waste effort:
- Design flaws that cause redundant work every run
- Missing state tracking that forces unnecessary re-fetches
- Logic errors that produce correct but wasteful behavior

These are bugs or design flaws, not patterns. Fix them now.

### Note and Check for Patterns (2+ occurrences)
Subjective issues that need validation:
- "Instructions were confusing" - might be context-specific
- "Would be nice to have X" - suggestions need confirmation
- "Step took multiple attempts" - might be user error

**Rules:**
- 1 occurrence: Note in molecule close_reason, wait for pattern
- 2+ occurrences: Propose fix
- 3+ occurrences: Definitely fix

## Recording Issues

When there are issues, record them in the close_reason using this format:

```
Issues found:
- ERROR: Used --silent flag (doesn't exist, should be -q)
- FRICTION: Molecule attachment instructions unclear

Clean areas:
- Gate flow worked smoothly
- Validation steps clear
```

This becomes queryable history for pattern detection.

## Proposing Skill Improvements

For persistent problems (2+ occurrences across molecules), propose changes:

```
## Tackle Skill Improvement

Issue: <description of persistent problem>
Occurrences: Found in molecules <list>
Affected resource: <RESEARCH.md | IMPLEMENT.md | etc.>

Signal: "<exact error or friction point>"

Current text:
> existing instruction

Proposed text:
> improved instruction

Rationale: <why this helps>
```

Present for review. Only apply with explicit approval.

## Completing Reflect

### If the run was smooth

```bash
bd close <reflect-step-id> --reason "Clean run - no issues"
```

### If there were issues

Add the friction label (for pattern detection) and close with the format from "Recording Issues":

```bash
bd update <molecule-id> --add-label "tackle:friction"
bd close <reflect-step-id> --reason "$(cat <<'EOF'
Issues found:
- <issue 1>
- <issue 2>
EOF
)"
```

### IMPORTANT: Close the Root Molecule

**Molecules do NOT auto-close.** After closing the reflect step, you must explicitly close the root molecule and unhook:

```bash
source "$SKILL_DIR/resources/scripts/complete-tackle.sh"
```

This script:
1. Closes the root molecule
2. Verifies molecule closure
3. Unhooks the issue

**Why this matters**: Open molecules pollute future queries. Pattern detection depends on closed molecules with proper close_reason fields.

## Example

```
## Tackle Reflect: gt-mol-xxxxx

Reviewed tackle process for worktree health check PR.

### Issues Found

1. **ERROR**: Used `--silent` flag (doesn't exist)
   - Should be `-q` or `--quiet`
   - Fixing immediately in RESEARCH.md

2. **FRICTION**: Molecule attachment confusion
   - Instructions unclear about "pinned bead" concept
   - Checking molecule history for pattern...
   - Found similar note in gt-mol-yyyyy - 2nd occurrence
   - Proposing clearer instructions

### Pattern Check
Queried closed tackle molecules for similar issues.
Found 1 prior occurrence of molecule attachment confusion.

### Actions
- Fixed: --silent -> -q in RESEARCH.md (objective error)
- Proposed: Clearer molecule attachment instructions (2nd occurrence)
```
