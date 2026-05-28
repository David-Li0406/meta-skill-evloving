---
name: implement
description: Execute implementation plan phase by phase with visual verification
order: 6

next:
  default: simplify
  conditions:
    - if: "flag == '--skip-simplify'"
      then: review

tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
  - AskUserQuestion
  - mcp__figma-screenshot__figma_screenshot
---

# Step: Implement

<context>
This step executes the implementation plan phase by phase. Each phase includes
code changes, validation, and optional visual verification against Figma designs.
</context>

## Instructions

<instructions>

### 1. Execute /compact (if not already done)

Clear context before implementation to maximize available context for code changes.

### 2. Load Plan

Read `.claude/feature/{ticket-id}/plan.md`

Parse frontmatter for:
- `total_phases`
- `ticket_id`

### 3. Implement Each Phase

For each phase in the plan:

#### 3.1 Read Phase Details

- Goal
- Files to modify/create
- Implementation details
- Validation command
- Commit message

#### 3.2 Implement Changes

Execute the implementation as described in the phase.

#### 3.3 Run Validation

Execute the validation command if specified:
```bash
{validation command from plan}
```

#### 3.4 Visual Verification (if applicable)

**Conditions to trigger**:
- `--skip-visual-verify` NOT set
- `figma_urls` exist in status.json
- Phase modified frontend files (`.vue`, `.tsx`, `.jsx`, `.css`, `.scss`, etc.)

**Check for frontend changes**:
```bash
git diff --name-only HEAD~1 | grep -E '\.(vue|tsx|jsx|css|scss|less|html)$'
```

**If frontend files modified AND Figma URLs available**:

```yaml
Task:
  subagent_type: visual-verify
  prompt: |
    Compare Figma designs with browser render.
    Figma URLs: {figma_urls from status.json}
    Base URL: {config.visual_verify.base_url}
    Context: Phase {N} - {phase description}
    Ticket: {ticket-id}
```

**Handle results**:

| Status | AUTO Mode | INTERACTIVE Mode |
|--------|-----------|------------------|
| pass | Continue | Continue |
| needs_attention | Log warning, continue | Ask user |
| fail | Log warning in PR | Ask user to fix |
| skipped | Continue | Continue |

**INTERACTIVE - on needs_attention or fail**:

```yaml
AskUserQuestion:
  question: "Des ecarts visuels detectes (score: {score}/5). Que faire ?"
  header: "Visual"
  options:
    - label: "Voir le rapport"
      description: "Afficher le rapport detaille"
    - label: "Corriger maintenant"
      description: "Appliquer les corrections"
    - label: "Ignorer et continuer"
      description: "Sera note dans la PR"
```

#### 3.5 Commit Changes (if configured)

Using the commit message from the plan (unless user manages commits manually).

#### 3.6 Store Visual Warnings

If visual issues found, store in status.json for PR body:
```json
{
  "visual_warnings": [
    { "screen": "...", "score": 3, "report": "path/to/report" }
  ]
}
```

### 4. Update Status

After all phases complete:
- `phases.implement = "completed"`
- `state = "implemented"`

</instructions>

## Output

<output>
- Code changes implemented according to plan
- Commits created (if configured)
- Status: `phases.implement = "completed"`, `state = "implemented"`
- Optional: `visual_warnings[]` in status.json
</output>

## Auto Behavior

<auto_behavior>
- Implement all phases without user interaction
- Log visual warnings for PR body
- Continue on non-critical issues
</auto_behavior>

## Interactive Behavior

<interactive_behavior>
- Show progress for each phase
- Prompt on visual verification issues
- Allow user to decide on corrections
</interactive_behavior>

## Large Epic Note

<constraints>
For very large epics with many phases, use `--plan-only` flag and run
`solo-implement.sh` separately. This launches each phase in its own
Claude session with fresh context.
</constraints>
