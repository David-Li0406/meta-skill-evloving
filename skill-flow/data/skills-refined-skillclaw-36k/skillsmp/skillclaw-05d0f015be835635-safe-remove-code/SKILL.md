---
name: safe-remove-code
description: Use this skill when you need to safely remove code patterns from multiple files while ensuring validation and rollback to prevent accidental data loss.
---

# Safe Code Removal Skill

**Purpose**: Safely remove code patterns (instrumentation, debugging code, deprecated patterns) from multiple files with strict validation to prevent accidentally gutting files.

**Created**: 2025-11-07 after accidentally gutting 7 hooks during timing code removal.

**Performance**: Prevents catastrophic file damage through per-file validation, syntax checks, and functional testing.

## The Problem

When removing instrumentation, debugging code, or other patterns from multiple files, aggressive removal scripts can accidentally delete functional code, leaving only boilerplate (shebang, set commands).

**Real Example** (2025-11-07):
- **Task**: Remove timing instrumentation from 47 hooks.
- **Mistake**: Removal script was too aggressive.
- **Impact**: 7 hooks reduced to 3 lines (only `#!/bin/bash` and `set -euo pipefail`).
- **Hooks destroyed**: auto-learn-from-mistakes.sh, block-data-loss.sh, detect-worktree-violation.sh, enforce-requirements-release.sh, load-todo.sh, detect-assistant-giving-up.sh, verify-convergence-entry.sh.
- **Recovery**: Restored from backups.
- **Root cause**: Didn't validate hooks after removal, declared task complete too early.

## When to Use This Skill

### ✅ Use safe-remove-code When:
- Removing instrumentation code from multiple files.
- Cleaning up debugging statements across the codebase.
- Removing deprecated patterns systematically.
- Need validation that files remain functional after removal.
- Pattern removal affects 5+ files.

### ❌ Use Edit Tool Instead When:
- Removing code from a single file (Edit tool is simpler).
- Changes are complex refactoring (not simple removal).
- Pattern varies significantly across files.
- Need to preserve some instances of the pattern.
- Pattern removal is part of a larger refactoring task.

## ⚠️ Critical Safety Rules
- **MANDATORY BACKUP**: Always create a timestamped backup before any removal.
- **PER-FILE VALIDATION**: Validate each file individually (syntax, size, integrity).
- **FUNCTIONAL TESTING**: Run build and tests after all removals.
- **IMMEDIATE VERIFICATION**: Don't declare complete without verification.
- **AUTOMATIC CLEANUP**: Remove backups only after ALL validation passes.
- **PRECISE PATTERNS**: Use specific patterns, not vague regex.

## Prerequisites
Before using this skill, verify:
- [ ] Working directory is clean.