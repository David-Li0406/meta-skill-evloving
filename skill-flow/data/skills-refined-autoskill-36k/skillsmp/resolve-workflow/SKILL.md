---
name: resolve-workflow
description: Modular ticket resolution workflow orchestrator. Loads steps dynamically based on mode and current state.
---

# Resolve - Modular Workflow Orchestrator

<context>
This skill orchestrates the complete ticket resolution workflow by loading and executing
individual step files. Each step is a separate file containing focused instructions,
loaded only when needed to minimize context usage.
</context>

## Input

Arguments passed from command: `$ARGUMENTS`

## Step 1: Parse Arguments

<instructions>
Extract from arguments:
- `ticket_id`: Required (except with --init)
- Flags: `--init`, `--auto`, `--continue`, `--refine-plan`, `--plan-only`
- Options: `--source`, `--target`, `--skip-simplify`, `--skip-review`, `--skip-visual-verify`, `--pr`, `--draft`
</instructions>

## Step 2: Determine Mode

<mode_detection>
| Flag              | Mode        | Starting Step            |
|-------------------|-------------|--------------------------|
| `--init`          | INIT        | 00-initialization (config only) |
| `--continue`      | CONTINUE    | 06-implement             |
| `--refine-plan`   | REFINE      | 05-plan-validation       |
| `--auto`          | AUTO        | 00-initialization        |
| (default)         | INTERACTIVE | 00-initialization        |
</mode_detection>

## Step 3: Load Current Step

<workflow>
1. Check mode to determine starting point
2. If CONTINUE or REFINE: verify status.json exists and is valid
3. Read step file: `~/.claude/skills/resolve-workflow/steps/{step-number}-{step-name}.md`
4. Execute step instructions
5. Read step frontmatter for `next` directive
6. Continue to next step or STOP
</workflow>

## Step Execution Flow

<step_flow>
### Standard Flow (INTERACTIVE/AUTO)
```
00-initialization → 01-fetch-ticket → 02-analyze-complexity → 03-exploration
→ 04-create-plan → 05-plan-validation → 06-implement → 07-simplify
→ 08-review → 09-finalize
```

### CONTINUE Flow
```
(verify status) → 06-implement → 07-simplify → 08-review → 09-finalize
```

### REFINE Flow
```
(load context) → 05-plan-validation (refine loop) → 06-implement → ...
```

### INIT Flow
```
00-initialization (config only) → STOP
```

### PLAN-ONLY Flow
```
00-initialization → ... → 05-plan-validation → STOP (display plan + next steps)
```
</step_flow>

## Mode Reference

See `~/.claude/skills/resolve-workflow/references/modes.md` for detailed mode behaviors.

## Step Files

| Step | File | Description |
|------|------|-------------|
| 00 | `steps/00-initialization.md` | Setup, config loading, feature directory |
| 01 | `steps/01-fetch-ticket.md` | Retrieve ticket, extract Figma URLs, user context |
| 02 | `steps/02-analyze-complexity.md` | Score complexity, determine workflow type |
| 03 | `steps/03-exploration.md` | Explore codebase based on complexity |
| 04 | `steps/04-create-plan.md` | Generate implementation plan |
| 05 | `steps/05-plan-validation.md` | Validate/refine plan interactively |
| 06 | `steps/06-implement.md` | Execute plan, visual verification |
| 07 | `steps/07-simplify.md` | Code simplification pass |
| 08 | `steps/08-review.md` | Code review |
| 09 | `steps/09-finalize.md` | Push and create PR |

## Error Handling

<constraints>
- If step file not found: ERROR with clear message
- If status.json invalid for CONTINUE: ERROR "Plan not validated"
- If ticket not found: ERROR with troubleshooting hints
- Always update status.json after each step completion
</constraints>

## Language

All user communication in French.
Technical output (git, code, files) in English.

## NOW

<instructions>
1. Parse the arguments provided
2. Determine the execution mode
3. Load and execute the appropriate starting step
4. Follow the step's `next` directive until STOP or completion
</instructions>

Begin workflow for: `$ARGUMENTS`
