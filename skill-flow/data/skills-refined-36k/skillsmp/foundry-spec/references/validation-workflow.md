# Validation Workflow

This reference describes how to validate and fix SDD JSON specification files.

## Overview

Spec validation checks for structural consistency, auto-fixes common issues, and analyzes dependencies. Use validation after creating a spec or before running other SDD skills.

**Key capabilities:**
- Validate JSON spec structure and hierarchy integrity
- Auto-fix 13 common issue types with preview and backup support
- Calculate comprehensive spec statistics
- Analyze dependencies (cycles, orphans, deadlocks, bottlenecks)
- Check completeness and detect duplicates

## Understanding Exit Codes

Exit codes indicate the **state of your spec**, not command success/failure:

- **Exit 0**: Spec is valid (no errors)
- **Exit 1**: Spec has warnings (usable but improvable)
- **Exit 2**: Spec has errors (needs fixing) - expected for new specs
- **Exit 3**: File not found or access error (actual command failure)

**Important:** Exit code 2 means "I found errors in your spec" not "I failed to validate".

## MCP Tooling

| Router | Key Actions |
|--------|-------------|
| `spec` | `validate`, `fix`, `stats`, `analyze-deps`, `diff`, `history`, `completeness-check`, `duplicate-detection` |

## Core Workflow

### Step 1: Validate

```bash
mcp__plugin_foundry_foundry-mcp__spec action="validate" spec_id="{spec-id}"
```

Check exit code:
- Exit 0 → Valid, done
- Exit 3 → File error, check path
- Exit 1-2 → Continue to fix

### Step 2: Fix

```bash
# Preview fixes first
mcp__plugin_foundry_foundry-mcp__spec action="fix" spec_id="{spec-id}" dry_run=true

# Apply fixes (backup created automatically)
mcp__plugin_foundry_foundry-mcp__spec action="fix" spec_id="{spec-id}"
```

### Step 3: Re-validate

Always re-validate after fixing - fixing often reveals new issues.

Track error count progression:
- **Decreasing** (88 → 23 → 4) - Continue auto-fixing
- **Plateau** (4 → 4 → 4) - Switch to manual fixes

### Step 4: Manual Fixes (if needed)

Switch to manual intervention when:
- Error count unchanged for 2+ passes
- Fix reports "skipped issues requiring manual intervention"
- Remaining issues need context or human judgment

See `validation-fixes.md` for manual fix patterns.

## Typical Fix Cycles

**Most specs (2-3 passes):**
```
Pass 1: 47 errors → fix → 8 errors
Pass 2: 8 errors → fix → 2 errors
Pass 3: 2 errors → fix → 0 errors
```

**Complex specs with circular deps (4-5 passes):**
```
Pass 1: 88 errors → fix → 23 errors
Pass 2: 23 errors → fix → 4 errors
Pass 3: 4 errors → fix → 4 errors (plateau)
→ Manual: Remove circular dependencies
Pass 4: Validate → 0 errors
```

## Additional Commands

### stats

Calculate comprehensive spec statistics:

```bash
mcp__plugin_foundry_foundry-mcp__spec action="stats" spec_id="{spec-id}"
```

Shows node counts, status breakdown, hierarchy depth, average tasks per phase, verification coverage, and progress percentage.

### analyze-deps

Analyze dependencies for cycles, orphans, deadlocks, and bottlenecks:

```bash
mcp__plugin_foundry_foundry-mcp__spec action="analyze-deps" spec_id="{spec-id}" bottleneck_threshold=3
```

### completeness-check

Analyze spec completeness with scoring (structure, metadata, dependencies, verification):

```bash
mcp__plugin_foundry_foundry-mcp__spec action="completeness-check" spec_id="{spec-id}"
```

### duplicate-detection

Detect duplicate or near-duplicate tasks:

```bash
mcp__plugin_foundry_foundry-mcp__spec action="duplicate-detection" spec_id="{spec-id}"
```

Detects exact title matches, similar descriptions (fuzzy matching), overlapping acceptance criteria, and redundant verification tasks.

### diff

Compare two versions of a spec:

```bash
mcp__plugin_foundry_foundry-mcp__spec action="diff" spec_id="{spec-id}" compare_to="{backup-path-or-version}"
```

### history

View modification history:

```bash
mcp__plugin_foundry_foundry-mcp__spec action="history" spec_id="{spec-id}" limit=10
```

## Input Format

All validation commands accept both spec names and paths:

**Spec name (recommended):**
```bash
mcp__plugin_foundry_foundry-mcp__spec action="validate" spec_id="my-spec-001"
```

**Path:**
```bash
mcp__plugin_foundry_foundry-mcp__spec action="validate" path="specs/pending/my-spec-001.json"
```
