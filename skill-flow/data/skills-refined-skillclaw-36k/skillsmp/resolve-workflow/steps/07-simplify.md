---
name: simplify
description: Apply code simplification pass to implementation
order: 7

skip_if:
  - flag: "--skip-simplify"
  - config: "simplify.enabled == false"

next:
  default: review
  conditions:
    - if: "flag == '--skip-review'"
      then: finalize

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

# Step: Simplify

<context>
This step applies a code simplification pass to the implementation.
A specialized simplifier agent reviews the modified files and suggests
improvements for readability, maintainability, and code quality.
</context>

## Instructions

<instructions>

### 1. Check Skip Conditions

Skip this step if:
- `--skip-simplify` flag is set
- Config `simplify.enabled = false`

### 2. Detect Simplifier Agent

Auto-detect based on project:

| Detection | Agent |
|-----------|-------|
| `composer.json` with symfony | symfony-simplifier |
| `composer.json` with laravel | laravel-simplifier |
| `package.json` | js-simplifier |
| Default | generic-simplifier |

Agent path: `~/.claude/agents/{agent}-simplifier.md`

### 3. Get Modified Files

```bash
git diff --name-only {base-branch}...HEAD
```

Filter for relevant code files (exclude tests, configs, etc. unless specifically changed).

### 4. Apply Simplifier Agent

```yaml
Task:
  subagent_type: general-purpose
  prompt: |
    Apply simplification to these files:
    {list of modified files}

    Using agent: ~/.claude/agents/{agent}-simplifier.md

    Focus on:
    - Code readability
    - Removing duplication
    - Simplifying complex logic
    - Following project conventions
```

### 5. Review Suggestions (INTERACTIVE)

```yaml
AskUserQuestion:
  question: "Le simplifier suggere ces modifications. Appliquer ?"
  header: "Simplify"
  options:
    - label: "Appliquer tout"
      description: "Accepter toutes les suggestions"
    - label: "Revoir une par une"
      description: "Valider chaque modification"
    - label: "Ignorer"
      description: "Ne pas appliquer les simplifications"
```

### 6. Apply Changes (if accepted)

If changes applied, commit:

```bash
git add -A
git commit -m "refactor: simplify code ({agent}-simplifier)"
```

### 7. Update Status

Update status: `phases.simplify = "completed"`

</instructions>

## Output

<output>
- Code simplified (if changes applied)
- Commit: "refactor: simplify code ({agent}-simplifier)"
- Status: `phases.simplify = "completed"`
</output>

## Auto Behavior

<auto_behavior>
- Apply simplifications if `simplify.auto_apply = true` in config
- Otherwise: log suggestions without applying
</auto_behavior>

## Interactive Behavior

<interactive_behavior>
- Present suggestions before applying
- Allow selective application
- Allow skipping entirely
</interactive_behavior>
