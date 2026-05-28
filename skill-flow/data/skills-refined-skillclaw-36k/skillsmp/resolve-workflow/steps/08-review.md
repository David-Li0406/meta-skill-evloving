---
name: review
description: Execute code review on implementation
order: 8

skip_if:
  - flag: "--skip-review"
  - config: "review.enabled == false"

next:
  default: finalize

tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
  - AskUserQuestion
---

# Step: Review

<context>
This step performs a code review on the implementation. A code reviewer agent
analyzes the changes for functional correctness, code quality, security,
and adherence to project conventions.
</context>

## Instructions

<instructions>

### 1. Check Skip Conditions

Skip this step if:
- `--skip-review` flag is set
- Config `review.enabled = false`

### 2. Gather Review Context

Read these files:
- `.claude/feature/{ticket-id}/ticket.md` - Original requirements
- `.claude/feature/{ticket-id}/plan.md` - Implementation plan
- Git diff of changes: `git diff {base-branch}...HEAD`

### 3. Apply Code Reviewer Agent

Apply agent: `~/.claude/agents/code-reviewer.md`

```yaml
Task:
  subagent_type: general-purpose
  prompt: |
    Perform code review on implementation for {ticket-id}.

    Context:
    - Ticket: .claude/feature/{ticket-id}/ticket.md
    - Plan: .claude/feature/{ticket-id}/plan.md
    - Changes: git diff {base-branch}...HEAD

    Review for:
    1. Functional correctness (meets requirements)
    2. Code quality (readability, maintainability)
    3. Security implications
    4. Test coverage
    5. Project conventions
```

### 4. Present Review Results

Display review findings:

```markdown
## Code Review Results

### Summary
- **Issues Found**: {count}
- **Critical**: {critical_count}
- **Warnings**: {warning_count}
- **Suggestions**: {suggestion_count}

### Critical Issues
{list of critical issues that must be fixed}

### Warnings
{list of warnings to consider}

### Suggestions
{list of optional improvements}
```

### 5. Handle Issues (INTERACTIVE)

```yaml
AskUserQuestion:
  question: "Review termine. Comment traiter les problemes ?"
  header: "Review"
  options:
    - label: "Corriger automatiquement"
      description: "Appliquer les corrections suggerees"
    - label: "Revoir manuellement"
      description: "Examiner chaque probleme"
    - label: "Ignorer et continuer"
      description: "Proceder sans corrections"
```

### 6. Apply Fixes (if requested)

If auto-fix requested:
- Apply suggested corrections
- Commit: `git commit -m "fix: address code review feedback"`

### 7. Block on Critical (if configured)

If `review.block_on_critical = true` and critical issues remain:
- **INTERACTIVE**: Require user to address before continuing
- **AUTO**: Log warning, continue with issues noted for PR

### 8. Update Status

Update status: `phases.review = "completed"`, `state = "reviewed"`

</instructions>

## Output

<output>
- Review report displayed
- Fixes applied (if requested)
- Status: `phases.review = "completed"`, `state = "reviewed"`
</output>

## Auto Behavior

<auto_behavior>
- Run review automatically
- Auto-fix if `review.auto_fix = true` in config
- Block on critical if `review.block_on_critical = true`
- Log issues for PR body if not fixed
</auto_behavior>

## Interactive Behavior

<interactive_behavior>
- Display review results
- Present fix options
- Allow manual review of each issue
- Require resolution of critical issues before continuing
</interactive_behavior>

## Review Categories

<review_categories>

### Functional Review
- Does implementation match requirements?
- Are edge cases handled?
- Is error handling appropriate?

### Technical Review
- Code quality and readability
- Performance considerations
- Security implications
- Test coverage

### Convention Review
- Project coding standards
- Naming conventions
- File organization

</review_categories>
