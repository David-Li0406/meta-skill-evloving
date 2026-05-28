---
name: validating-physics
description: Use this skill to validate component compliance with Sigil physics, auditing for violations that could harm users before they occur.
---

# Skill body

## Core Principle

```
Scan → Detect → Report → Fix
```

An audit reveals the gap between intent and implementation. Every finding is an opportunity to align.

## Severity Levels

| Level | Meaning | Action |
|-------|---------|--------|
| 🔴 CRITICAL | User harm possible | Fix immediately |
| 🟡 WARNING | Physics mismatch | Fix soon |
| 🟢 INFO | Optimization opportunity | Consider |

## Audit Categories

1. **Physics Audit**
   - Sync strategy matches effect (pessimistic for financial/destructive)
   - Timing values align with physics table
   - Confirmation patterns present where required

2. **Performance Audit**
   - Async waterfalls (sequential awaits)
   - Barrel imports from heavy packages
   - Missing Suspense boundaries
   - Re-render issues

3. **Protected Audit**
   - Touch targets ≥ 44px
   - Focus rings visible
   - Cancel always reachable
   - Error recovery paths

4. **Material Audit**
   - Shadow layers ≤ 1
   - Gradient stops ≤ 2
   - Border radius ≤ 16px
   - Contrast ratio ≥ 4.5:1

5. **Animation Audit**
   - High-frequency = 0ms animation
   - Financial/destructive use ease-out
   - Reduced motion respected
   - SVGs wrapped for GPU

## Workflow

### Step 1: Discover Scope

**If scope is "all"**:
```
Glob: src/**/*.tsx, src/**/*.jsx
Exclude: *.test.*, *.spec.*, *.stories.*
```

**If scope is "file:path"**:
Audit only that file.

### Step 2: Run Detection Passes

For each file:

- **Effect Detection**:
  - Financial: `claim|withdraw|deposit|transfer|stake|mint|burn`
  - Destructive: `delete|remove|destroy|revoke`
  - Type patterns: `Currency|Money|Balance|Wei|Token`

- **Physics Check**:
  - Is `onMutate` present? (bad for financial)
  - Check transition/duration values
  - Is there a confirm step?

- **Protected Check**:
  - `{!isPending && <Cancel` pattern (violation)
  - Missing `focus:ring` or `focus-visible`
  - Error states without retry buttons

### Step 3: Generate Report

```
┌─ Ward Report ─────────────────────────────────────────────┐
│                                                           │
│  Scanned:    [N] components                               │
│  Passed:     [M] ([%])                                    │
│  Critical:   [X]                                          │
│  Warnings:   [Y]                                          │
└───────────────────────────────────────────────────────────┘
```