---
name: requirements-framework-usage
description: This skill should be used when the user asks about "using requirements framework", "how to configure requirements", "add requirement checklist", "customize requirements", "requirements not working", "bypass requirements", "satisfy requirements", or needs help with the requirements framework CLI (req command). Also triggers on questions about requirement scopes, session management, or troubleshooting hooks.
git_hash: 7953a43
---

# Requirements Framework Usage

Help users configure, customize, and troubleshoot the **Claude Code Requirements Framework** - a hook-based system that enforces development workflow practices.

**Repository**: https://github.com/HarmAalbers/claude-requirements-framework
**Documentation**: `~/.claude/hooks/README-REQUIREMENTS-FRAMEWORK.md`

## Core Capabilities

1. **Configuration Guidance** - Help set up global, project, and local configs
2. **Checklist Customization** - Add/modify checklists for requirements
3. **CLI Usage** - Explain `req` command and session management
4. **Troubleshooting** - Debug hooks, permissions, and sync issues
5. **Best Practices** - Recommend workflows and patterns

## Quick Reference

### Essential CLI Commands

```bash
req status                  # Check requirement status
req satisfy commit_plan     # Mark requirement satisfied
req clear commit_plan       # Clear a requirement
req list                    # List all requirements
req sessions                # View active sessions
req init                    # Interactive project setup
req config commit_plan      # View/modify configuration
req doctor                  # Verify installation
```

**→ Full CLI reference**: See `references/cli-reference.md`

### Configuration Locations

1. **Global** (`~/.claude/requirements.yaml`) - Defaults for all projects
2. **Project** (`.claude/requirements.yaml`) - Shared team config (committed)
3. **Local** (`.claude/requirements.local.yaml`) - Personal overrides (gitignored)

### Requirement Scopes

| Scope | Lifetime | Use Case |
|-------|----------|----------|
| `session` | Until Claude session ends | Daily planning, ADR review |
| `branch` | Persists across sessions | GitHub ticket linking |
| `permanent` | Never auto-cleared | Project setup |
| `single_use` | Cleared after action | Pre-commit review (each commit) |

## Common Tasks

### Task: Add Checklist to Requirement

```yaml
# In .claude/requirements.yaml
requirements:
  commit_plan:
    enabled: true
    scope: session
    checklist:
      - "Plan created via EnterPlanMode"
      - "Atomic commits identified"
      - "TDD approach documented"
```

### Task: Create Custom Requirement

```yaml
requirements:
  my_requirement:
    enabled: true
    scope: session
    trigger_tools:
      - Edit
      - Write
    message: |
      🎯 **Custom Requirement**

      Explain what needs to be done.

      **To satisfy**: `req satisfy my_requirement`
    checklist:
      - "First step"
      - "Second step"
```

**→ More examples**: See `examples/custom-requirement.yaml`

### Task: Block Specific Bash Commands

```yaml
requirements:
  pre_commit_review:
    enabled: true
    scope: single_use
    trigger_tools:
      - tool: Bash
        command_pattern: "git\\s+commit"
    message: "Review required before commit"
```

**Pattern Tips**:
- `\\s+` matches whitespace
- `|` for OR: `git\\s+(commit|push)`
- Case-insensitive by default

**→ More patterns**: See `examples/bash-command-trigger.yaml`

### Task: Temporarily Disable Requirements

**Option 1**: Local override
```yaml
# .claude/requirements.local.yaml
enabled: false
```

**Option 2**: Environment variable
```bash
export CLAUDE_SKIP_REQUIREMENTS=1
```

**Option 3**: Disable specific requirement
```bash
req config commit_plan --disable --local
```

## Interactive Setup

Use `req init` for guided project setup:

```bash
req init                    # Interactive wizard
req init --preset strict    # Use preset (non-interactive)
req init --yes              # Non-interactive with defaults
```

**Presets**:
- `strict` - All requirements, session scope (teams)
- `relaxed` - Basic requirements, branch scope
- `minimal` - Only commit_plan (learning)
- `advanced` - All features + branch limits + guards
- `inherit` - Inherit from global config

## Configuration Management

View and modify settings without editing YAML:

```bash
# View
req config                   # All requirements
req config commit_plan       # Specific requirement

# Modify
req config commit_plan --enable
req config commit_plan --disable
req config commit_plan --scope branch
req config adr_reviewed --set adr_path=/custom/path
```

**→ Full config options**: See `references/cli-reference.md`

## Session Management

Sessions are auto-detected. Manual override when needed:

```bash
req sessions                           # List active sessions
req satisfy commit_plan --session ID   # Explicit session
```

## Troubleshooting Quick Guide

### Hook Not Triggering?

1. Check if on main/master (skipped by design)
2. Verify config enabled: `req config`
3. Check hook registration: `req doctor`
4. Check permissions: `ls -la ~/.claude/hooks/*.py`
5. Verify no skip flag: `echo $CLAUDE_SKIP_REQUIREMENTS`

### Session Not Found?

```bash
req sessions                # Find session ID
req satisfy NAME --session ID
req prune                   # Clean stale sessions
```

**→ Full troubleshooting guide**: See `references/troubleshooting.md`

## Advanced Features

### Auto-Satisfaction via Skills

Skills can automatically satisfy requirements:

```
1. git commit → Blocked by pre_commit_review
2. /requirements-framework:pre-commit runs
3. Auto-satisfies pre_commit_review
4. git commit → Success!
5. single_use clears → Next commit requires review again
```

**Built-in mappings**:
- `requirements-framework:pre-commit` → `pre_commit_review`
- `requirements-framework:quality-check` → `pre_pr_review`
- `requirements-framework:codex-review` → `codex_reviewer`

### Single-Use Scope

Requires satisfaction before EACH action:

```yaml
pre_commit_review:
  scope: single_use  # Must satisfy before EVERY commit
```

### Dynamic Requirements

Auto-calculated conditions (e.g., branch size):

```yaml
branch_size_limit:
  type: dynamic
  threshold: 400
```

### Guard Requirements

Condition checks (e.g., protected branches):

```yaml
protected_branch:
  type: guard
  branches: [main, master]
```

**→ Advanced features details**: See `references/advanced-features.md`

## Checklist Best Practices

1. **Keep items concise** - 5-10 words per item
2. **Make actionable** - Each item verifiable
3. **Order logically** - Steps flow naturally
4. **Limit quantity** - 5-10 items maximum

**Good**:
```yaml
checklist:
  - "Plan created via EnterPlanMode"
  - "Atomic commits identified"
  - "Tests written (TDD)"
```

**Bad**:
```yaml
checklist:
  - "Think about what you're going to do and write it down"
  - "Various commit-related activities"
```

## Configuration Patterns

### Pattern: Team Config with Personal Overrides

```yaml
# .claude/requirements.yaml (team - committed)
requirements:
  commit_plan:
    enabled: true
    scope: session

# .claude/requirements.local.yaml (personal - gitignored)
requirements:
  commit_plan:
    enabled: false  # I opt-out
```

### Pattern: Inheritance

```yaml
# Project inherits and extends global
version: "1.0"
inherit: true

requirements:
  commit_plan:
    checklist:
      - "Project-specific checklist item"
```

**→ More patterns**: See `references/configuration-patterns.md`

## Diagnostics

```bash
req doctor   # Full installation check
req verify   # Quick verification
```

`req doctor` checks:
- Python version (3.9+)
- Hook registration
- File permissions
- Sync status (repo vs deployed)
- Library imports
- Test suite status

## Key Principles

1. **Fail open** - Errors don't block Claude
2. **Skip protected** - Main/master often skipped
3. **User override** - Local settings always win
4. **Session-isolated** - Requirements don't leak
5. **Team configurable** - Projects control workflow

## Resources

- **README**: `~/.claude/hooks/README-REQUIREMENTS-FRAMEWORK.md`
- **GitHub**: https://github.com/HarmAalbers/claude-requirements-framework
- **Dev Guide**: `~/Tools/claude-requirements-framework/DEVELOPMENT.md`
- **Sync Tool**: `~/Tools/claude-requirements-framework/sync.sh`
- **Tests**: `~/.claude/hooks/test_requirements.py`

## Reference Files

- `references/cli-reference.md` - Complete CLI command documentation
- `references/configuration-patterns.md` - Common configuration patterns
- `references/advanced-features.md` - Auto-satisfy, dynamic, guards
- `references/troubleshooting.md` - Error messages, debugging
- `examples/project-requirements.yaml` - Full project config
- `examples/custom-requirement.yaml` - Custom requirement template
- `examples/bash-command-trigger.yaml` - Bash command patterns
