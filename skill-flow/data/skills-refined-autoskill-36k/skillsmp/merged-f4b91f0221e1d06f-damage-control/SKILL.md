---
name: damage-control
description: Use this skill to install, configure, and manage security hooks that block dangerous commands and protect sensitive files in Claude Code.
---

# Damage Control Skill

This skill provides a defense-in-depth protection system for Claude Code, utilizing PreToolUse hooks to intercept and validate tool calls before execution, blocking dangerous commands and protecting sensitive files.

## Overview

The Damage Control skill helps users deploy and manage a security system that includes:

- **Command Pattern Blocking**: Blocks dangerous bash commands (e.g., `rm -rf`, `git reset --hard`).
- **Ask Patterns**: Triggers confirmation dialogs for risky operations (e.g., `git checkout -- .`).
- **Path Protection Levels**:
  - `zeroAccessPaths`: No access at all (e.g., secrets, credentials).
  - `readOnlyPaths`: Read allowed, modifications blocked (e.g., system configs).
  - `noDeletePaths`: All operations except delete (e.g., important project files).

## Skill Structure

```
.claude/skills/damage-control/
├── SKILL.md                     # This file
├── patterns.yaml                # Shared security patterns
├── cookbook/
│   ├── install_damage_control_ag_workflow.md
│   ├── modify_damage_control_ag_workflow.md
│   ├── manual_control_damage_control_ag_workflow.md
│   ├── list_damage_controls.md
│   ├── test_damage_control.md
│   └── build_for_windows.md
├── hooks/
│   ├── damage-control-python/   # Python implementation
│   │   ├── bash-tool-damage-control.py
│   │   ├── edit-tool-damage-control.py
│   │   ├── write-tool-damage-control.py
│   │   └── test-damage-control.py
│   └── damage-control-typescript/  # TypeScript implementation
│       ├── bash-tool-damage-control.ts
│       ├── edit-tool-damage-control.ts
│       ├── write-tool-damage-control.ts
│       └── test-damage-control.ts
└── test-prompts/                # Test prompts for validation
    ├── sentient_v1.md
    ├── sentient_v2.md
    ├── sentient_v3.md
    └── sentient_v4.md
```

## After Installation

The installation workflow copies hooks and creates settings based on the chosen level:

### Global Hooks
```
~/.claude/
├── settings.json                      # Hook configuration
└── hooks/
    └── damage-control/
        ├── patterns.yaml
        ├── bash-tool-damage-control.py (or .ts)
        ├── edit-tool-damage-control.py
        └── write-tool-damage-control.py
```

### Project Hooks
```
<agents current working directory>/
└── .claude/
    ├── settings.json                  # Hook configuration (shared)
    └── hooks/
        └── damage-control/
            ├── patterns.yaml
            ├── bash-tool-damage-control.py (or .ts)
            ├── edit-tool-damage-control.py
            └── write-tool-damage-control.py
```

### Project Personal Hooks
```
<agents current working directory>/
└── .claude/
    ├── settings.local.json            # Personal overrides (gitignored)
    └── hooks/
        └── damage-control/
            ├── patterns.yaml
            ├── bash-tool-damage-control.py (or .ts)
            ├── edit-tool-damage-control.py
            └── write-tool-damage-control.py
```

## Quick Reference

### Settings File Locations

| Level            | Path                          | Scope                      |
| ---------------- | ----------------------------- | -------------------------- |
| Global           | `~/.claude/settings.json`     | All projects               |
| Project          | `.claude/settings.json`       | Current project (shared)   |
| Project Personal | `.claude/settings.local.json` | Current project (personal) |

### Path Protection Levels

| Type              | Read | Write | Edit | Delete | Use Case                |
| ----------------- | ---- | ----- | ---- | ------ | ----------------------- |
| `zeroAccessPaths` | No   | No    | No   | No     | Secrets, credentials    |
| `readOnlyPaths`   | Yes  | No    | No   | No     | System configs, history |
| `noDeletePaths`   | Yes  | Yes  | Yes  | No     | Important project files |

### Runtime Requirements

| Implementation | Runtime     | Install Command                                             |
| -------------- | ----------- | ----------------------------------------------------------- |
| Python         | UV (Astral) | `curl -LsSf https://astral.sh/uv/install.sh \| sh`          |
| TypeScript     | Bun         | `curl -fsSL https://bun.sh/install \| bash && bun add yaml` |

### Exit Codes

| Code | Meaning                              |
| ---- | ------------------------------------ |
| 0    | Allow operation                      |
| 0    | Ask (JSON output triggers dialog)    |
| 2    | Block operation                      |

## Testing

Use the test prompts in [test-prompts/](test-prompts/) to validate the hooks:

- `sentient_v1.md` - Tests `rm -rf` blocking
- `sentient_v2.md` - Tests `find -delete` blocking
- `sentient_v3.md` - Tests ask patterns
- `sentient_v4.md` - Tests simple command blocking

Run a test:
```
/project:test-prompts/sentient_v1
```

## Related Workflows

| Workflow | Purpose |
|----------|---------|
| [cookbook/install_damage_control_ag_workflow.md](cookbook/install_damage_control_ag_workflow.md) | Installation workflow |
| [cookbook/modify_damage_control_ag_workflow.md](cookbook/modify_damage_control_ag_workflow.md) | Modification workflow |
| [cookbook/test_damage_control.md](cookbook/test_damage_control.md) | Test all hooks |
| [cookbook/list_damage_controls.md](cookbook/list_damage_controls.md) | List all configurations |
| [cookbook/build_for_windows.md](cookbook/build_for_windows.md) | Add Windows patterns |

## Critical Reminder

**IMPORTANT:** After any installation or modification, restart your agent for changes to take effect. Hooks are only loaded at agent startup. Run `/hooks` after restart to verify.