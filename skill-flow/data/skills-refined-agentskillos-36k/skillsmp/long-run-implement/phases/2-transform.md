# Phase 2: Prepare Plans

## Purpose
Validate, optimize, and split tasks into executable plan files by delegating to the plan-fixer skill.

## Inputs (from Phase 1)
- `spec_path`: Path to spec folder
- `state_path`: Path to .long-run/ directory
- `is_resume`: Boolean indicating resume state
- `resume_from`: Plan number to resume from (if applicable)

## Workflow

### Step 1: Detect Input State

```
IF {spec_path}/.long-run/plans/ contains NN-PLAN.md files:
  # Already prepared - skip to execution
  Log: "Plan files already exist, skipping preparation"
  GOTO Phase 3

IF {spec_path}/PLAN.md exists:
  # Unified plan exists - needs splitting only
  input_mode = "split_only"
  input_file = PLAN.md

ELSE IF {spec_path}/tasks.md exists:
  # Raw tasks - needs full processing
  input_mode = "full"
  input_file = tasks.md

ELSE:
  ERROR "No tasks.md or PLAN.md found in spec folder"
```

### Step 2: Run Plan-Fixer

```
IF input_mode == "full":
  # Run all phases (0-4)
  # Invoke plan-fixer skill with source file

  Use Skill tool:
    skill: "plan-fixer"
    args: "{spec_path}/tasks.md"

  # Plan-fixer will:
  #   Phase 0: Structure & format
  #   Phase 1: Claude review
  #   Phase 2: Codex validation
  #   Phase 3: Final polish
  #   Phase 4: Split into .long-run/plans/

IF input_mode == "split_only":
  # Run Phase 4 only (plan already optimized)
  # Use "split only" trigger phrase to activate split-only mode

  Use Skill tool:
    skill: "plan-fixer"
    args: "{spec_path}/PLAN.md split only"

  # The "split only" phrase triggers split-only mode which:
  #   - Skips Phases 0-3 (structure, Claude review, Codex, polish)
  #   - Runs Phase 4 only (split & initialize)
  #   - Creates .long-run/ structure from existing PLAN.md
  #   - Requires input file to already have <task> blocks
```

### Step 2.5: Handle Single Task Group

```
IF plan-fixer reports "Single task group detected":
  # Still have one plan file to execute
  plans = ["{spec_path}/.long-run/plans/01-PLAN.md"]
  Log: "Single task group - will execute as one plan"
  # Continue normally to Step 3
```

**Note:** Single task group handling is now done IN plan-fixer (Phase 4). It creates the `.long-run/` structure with a single `01-PLAN.md` file. This ensures consistent directory structure regardless of task count.

### Step 3: Verify Output

```
Verify .long-run/plans/ contains expected files:
  - At least one NN-PLAN.md file
  - STATE.md exists in .long-run/
  - Each plan has required sections (<task>, <action>, <verify>, <done>)

IF verification fails:
  Report error with details
  STOP with status "preparation_failed"
```

### Step 4: Handle --prepare-only Flag

```
IF --prepare-only flag is set:
  Output to user:
    "✅ Plan preparation complete (--prepare-only mode)

     Plans created: {count}
     Location: {spec_path}/.long-run/plans/

     Review the plans and run again without --prepare-only to execute."
  STOP (do not proceed to Phase 3)
```

### Step 5: Output

```
Pass to Phase 3:
  - plans: Array of paths to .long-run/plans/*.md
  - state_path: {spec_path}/.long-run
  - dependencies: Dependency graph (extracted from STATE.md)
```

## Backward Compatibility

**Preserve manually created plans:** If someone has manually created `.long-run/plans/` files, do not overwrite them. The existence check in Step 1 ensures this.

**Legacy tasks.md support:** The full plan-fixer pipeline (Phases 0-4) handles tasks.md files that haven't been pre-processed.

## Plan File Format

Each split plan file in `.long-run/plans/{NN}-PLAN.md` should be self-contained:

```markdown
<objective>
{shared objective from unified plan}
</objective>

<context>
{shared context from unified plan}
</context>

<constraints>
{shared constraints from unified plan}
</constraints>

<tasks>
<task type="auto">
  <name>Task N: {task_name}</name>
  <files>{files to stage for commit}</files>
  <action>
  {specific action steps for this task}
  </action>
  <verify>{verification command}</verify>
  <done>{completion criteria}</done>
</task>
</tasks>
```

**Note:** Each split plan contains only ONE task inside the `<tasks>` wrapper. The `<name>` is a child element, not an attribute. The `type="auto"` indicates autonomous execution (no user approval needed).

## Error Handling

```
ON plan-fixer failure:
  Log detailed error from plan-fixer output
  Report to user: "Plan preparation failed: {error}"
  Preserve any partial state for debugging
  STOP with status "preparation_failed"

ON verification failure:
  Report specific missing elements:
    - "Missing NN-PLAN.md files"
    - "STATE.md not found"
    - "Plan {N} missing <verify> section"
  Offer options:
    1. Re-run plan-fixer
    2. Manually fix and retry
    3. Abort
```
