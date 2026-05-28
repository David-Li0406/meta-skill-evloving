---
name: flow-example
description: Example skill demonstrating Flow-Next path resolution strategy and Factory skill format. Use this as a template for creating new Factory skills that integrate with flowctl.
---

# Flow Example Skill

This is a template skill demonstrating the correct path resolution strategy for Factory/Droid skills that use flowctl.

## Path Resolution Strategy

All Factory skills must use dynamic repo root resolution with proper fallback handling:

```bash
REPO_ROOT="${REPO_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || true)}"
if [ -z "$REPO_ROOT" ]; then
  echo "Error: Set REPO_ROOT=/absolute/path/to/repo (git rev-parse failed; cwd may be outside repo)."
  exit 1
fi
"$REPO_ROOT/.flow/bin/flowctl" <command>
```

**Rules:**
- If `git rev-parse` fails (cwd is outside repo), output a clear error and exit
- Never silently fail - always provide actionable error messages
- Support explicit REPO_ROOT override for edge cases

## Usage

This skill serves as documentation and verification for the Factory skills directory structure.

To list epics and tasks:
```bash
REPO_ROOT="${REPO_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || true)}"
"$REPO_ROOT/.flow/bin/flowctl" list
```

## Verification

````bash
REPO_ROOT="${REPO_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || true)}"
if [ -z "$REPO_ROOT" ]; then
  echo "Error: Set REPO_ROOT=/absolute/path/to/repo"
  exit 1
fi

# Verify skill file exists
ls "$REPO_ROOT/.factory/skills/flow-example/SKILL.md"
# Expected: file exists, exit code 0

# Verify flowctl is callable
"$REPO_ROOT/.flow/bin/flowctl" --help >/dev/null 2>&1 && echo "flowctl OK"
# Expected: outputs "flowctl OK", exit code 0
````
