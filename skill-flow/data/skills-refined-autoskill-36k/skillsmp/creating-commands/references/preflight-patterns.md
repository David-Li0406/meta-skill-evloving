---
title: Preflight Check Patterns
description: Bash command patterns for validating command prerequisites before execution. Includes file existence checks, git repository validation, dependency checks, and state validation patterns.
keywords: preflight checks, validation, bash patterns, git checks, dependency checks, state validation, file existence
file-type: reference
skill: creating-commands
---

# Preflight Check Patterns

Preflight checks validate that the command can execute successfully. Use bash commands with the `!` prefix in your command's `## Preflight Checks` section.

## File Existence Checks

```markdown
- Target file exists: !`test -f $1 && echo "exists" || echo "missing"`
- Directory exists: !`test -d .claude/commands && echo "yes" || echo "no"`
- Project structure: !`ls -la src/ tests/ 2>/dev/null || echo "not found"`
```

## Git Repository Checks

```markdown
- Git repository: !`git rev-parse --git-dir 2>/dev/null && echo "yes" || echo "no"`
- Clean working tree: !`git status --short`
- Current branch: !`git branch --show-current`
- Branch is pushed: !`git rev-parse --abbrev-ref @{upstream} 2>/dev/null || echo "not pushed"`
```

## Dependency Checks

```markdown
- Node.js installed: !`which node || echo "not found"`
- Package installed: !`npm list package-name --depth=0 2>/dev/null || echo "not installed"`
- Python available: !`which python3 || echo "not found"`
- Command available: !`which docker || echo "not found"`
```

## State Validation Checks

```markdown
- Uncommitted changes exist: !`git diff --stat || echo "none"`
- Tests directory exists: !`test -d tests && echo "yes" || echo "no"`
- Build artifacts present: !`test -f dist/main.js && echo "yes" || echo "no"`
```

## Skill Context Loading Checks

Force-load complete skill context to ensure full visibility of SKILL.md, reference files, and available resources.

**Use case**: Commands that need to deeply understand and apply patterns from a specific skill before execution.

### Basic Skill Context Loading

```markdown
- Load creating-commands skill context: !`python3 ~/.claude/skills/creating-commands/scripts/load_skill_context.py ~/.claude/skills/creating-commands`
```

### Loading Any Skill Context

```markdown
- Load skill context: !`python3 ~/.claude/skills/$SKILL_NAME/scripts/load_skill_context.py ~/.claude/skills/$SKILL_NAME`
```

**Script outputs**:
- Full SKILL.md content
- Complete frontmatter (all YAML fields) from each reference file
- All markdown headers (H1, H2, H3+) from each reference file
- All directories and files with type indicators (scripts, templates, assets, configs, etc.)

### Example Usage in Command

```markdown
---
allowed-tools: Bash, Read, Edit, Write
---

## Preflight Checks

- creating-skills context: !`python3 ~/.claude/skills/creating-skills/scripts/load_skill_context.py ~/.claude/skills/creating-skills`

## Task Instructions

Now that the complete creating-skills context is loaded:

1. Review the full SKILL.md content for workflow patterns
2. Examine reference file headers to understand available guidance
3. Apply the patterns from the skill to create the new artifact
```

## Usage in Commands

Copy these patterns into your command's `## Preflight Checks` section. Customize the checks based on your command's requirements.

**Example:**
```markdown
## Preflight Checks

- Git repository: !`git rev-parse --git-dir 2>/dev/null && echo "yes" || echo "no"`
- Has changes: !`git status --short`
- Not on main: !`git branch --show-current | grep -v '^main$' && echo "safe" || echo "on main"`
```
