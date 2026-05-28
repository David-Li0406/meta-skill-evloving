# Resolve Workflow Modes

<context>
This document defines the different execution modes for the /resolve command
and their behaviors. Each mode determines which steps are executed and how
user interaction is handled.
</context>

## Mode Overview

| Mode | Flag | Description | User Interaction |
|------|------|-------------|------------------|
| INIT | `--init` | Configure project only | Minimal |
| CONTINUE | `--continue` | Resume from validated plan | None until implement |
| REFINE | `--refine-plan` | Refine existing plan | High |
| AUTO | `--auto` | Complete workflow automatically | None |
| PLAN-ONLY | `--auto --plan-only` | Stop after plan creation | None |
| INTERACTIVE | (default) | User validates each step | High |

---

## INIT Mode

<mode name="INIT">

**Flag**: `--init`

**Purpose**: Configure project settings without processing a ticket.

**Steps Executed**:
1. 00-initialization (config only)
2. STOP

**Behavior**:
- Apply init-project skill
- Create/update `.claude/ticket-config.json`
- No ticket required

</mode>

---

## CONTINUE Mode

<mode name="CONTINUE">

**Flag**: `--continue`

**Purpose**: Resume workflow from a previously validated plan.

**Prerequisites**:
- `.claude/feature/{ticket-id}/status.json` must exist
- `state` must be `plan_validated`
- `.claude/feature/{ticket-id}/plan.md` must exist

**Steps Executed**:
1. Verify status (skip 00-05)
2. Execute /compact
3. 06-implement
4. 07-simplify
5. 08-review
6. 09-finalize

**Behavior**:
- Skip fetch, analyze, explore, plan, validation
- Load existing plan directly
- Clear context with /compact before implementation

</mode>

---

## REFINE Mode

<mode name="REFINE">

**Flag**: `--refine-plan`

**Purpose**: Interactively refine an existing plan before implementation.

**Prerequisites**:
- `.claude/feature/{ticket-id}/plan.md` must exist

**Steps Executed**:
1. Load context (ticket, analysis, plan)
2. 05-plan-validation (refine loop)
3. If validated: 06-implement → 07-simplify → 08-review → 09-finalize

**Behavior**:
- Display plan summary and context
- Extended validation options:
  - Poser des questions
  - Challenger le plan
  - Modifier le plan
  - Regenerer le plan
- Exit options:
  - Valider et implementer
  - Valider et arreter

</mode>

---

## AUTO Mode

<mode name="AUTO">

**Flag**: `--auto`

**Purpose**: Complete workflow automatically without user interaction.

**Prerequisites**:
- User must create branch/worktree BEFORE running

**Steps Executed**:
1. 00-initialization
2. 01-fetch-ticket
3. 02-analyze-complexity
4. 03-exploration
5. 04-create-plan
6. 05-plan-validation (auto-validate)
7. Execute /compact
8. 06-implement
9. 07-simplify
10. 08-review
11. 09-finalize (push + PR)

**Behavior**:
- No user prompts
- Auto-validate plan
- Create draft PR at end
- Log warnings for PR body instead of prompting

</mode>

---

## PLAN-ONLY Mode

<mode name="PLAN-ONLY">

**Flags**: `--auto --plan-only`

**Purpose**: Generate plan only, for epics that need separate implementation sessions.

**Steps Executed**:
1. 00-initialization
2. 01-fetch-ticket
3. 02-analyze-complexity
4. 03-exploration
5. 04-create-plan
6. 05-plan-validation (auto-validate)
7. STOP (display plan + next steps)

**Behavior**:
- Auto workflow up to plan validation
- Display full plan content
- Suggest next steps:
  - `/resolve {ticket-id} --refine-plan` for refinement
  - `solo-implement.sh --feature {ticket-id}` for implementation

**Use Case**: Large epics where implementation should run in separate Claude sessions.

</mode>

---

## INTERACTIVE Mode

<mode name="INTERACTIVE">

**Flag**: (default, no flag)

**Purpose**: User-guided workflow with validation at each decision point.

**Prerequisites**:
- User must create branch/worktree BEFORE running

**Steps Executed**:
1. 00-initialization (with resume prompt)
2. 01-fetch-ticket (with Figma/context prompts)
3. 02-analyze-complexity (with workflow confirmation)
4. 03-exploration
5. 04-create-plan
6. 05-plan-validation (interactive loop)
7. If "Valider et implementer": /compact → 06-implement → 07-simplify → 08-review
8. STOP (user manages push/PR)

**Behavior**:
- Prompt for resume if previous workflow exists
- Prompt for Figma URLs if not found
- Prompt for user context
- Confirm workflow type
- Interactive plan validation loop
- Prompt on visual verification issues
- Prompt on review issues
- Stop before push/PR (use `--pr` to include)

</mode>

---

## Mode Comparison

| Aspect | INTERACTIVE | AUTO | PLAN-ONLY | CONTINUE | REFINE |
|--------|-------------|------|-----------|----------|--------|
| Ticket fetch | Yes | Yes | Yes | No | No |
| Analysis | Yes | Yes | Yes | No | No |
| Exploration | Yes | Yes | Yes | No | No |
| Plan creation | Yes | Yes | Yes | No | No |
| Plan validation | Loop | Auto | Auto | No | Loop |
| Implementation | Yes | Yes | No | Yes | If validated |
| Simplify | Yes | Yes | No | Yes | If validated |
| Review | Yes | Yes | No | Yes | If validated |
| Push/PR | Manual | Auto | No | Auto | Manual |

---

## Typical Workflows

### Quick Fix (INTERACTIVE)

```bash
git checkout -b fix/PROJ-123
/resolve PROJ-123
# → Interactive validation
# → "Valider et implementer"
# → Implementation runs
# → User pushes and creates PR manually
```

### Full Automation (AUTO)

```bash
git checkout -b feat/PROJ-456
/resolve PROJ-456 --auto
# → Complete workflow runs
# → Draft PR created automatically
```

### Epic Planning (PLAN-ONLY + REFINE)

```bash
git checkout -b feat/PROJ-789
/resolve PROJ-789 --auto --plan-only
# → Plan generated and saved
# Review plan...
/resolve PROJ-789 --refine-plan
# → Refine and validate plan
# → "Valider et arreter"
solo-implement.sh --feature PROJ-789
# → Implement in separate sessions
```

### Resume After Interruption (CONTINUE)

```bash
# Previous session stopped after plan validation
/resolve PROJ-123 --continue
# → Skips to implementation
# → Completes workflow
```
