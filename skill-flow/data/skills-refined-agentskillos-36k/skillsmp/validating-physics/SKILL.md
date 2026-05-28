---
name: validating-physics
description: Validate component compliance with Sigil physics - audit for violations before they harm users
allowed-tools:
  - Read
  - Glob
  - Grep
---

# Validating Physics Skill

Protective barrier check — reveals physics violations before they harm users.

---

## Core Principle

```
Scan → Detect → Report → Fix
```

An audit reveals the gap between intent and implementation. Every finding is an opportunity to align.

---

## Severity Levels

| Level | Meaning | Action |
|-------|---------|--------|
| 🔴 CRITICAL | User harm possible | Fix immediately |
| 🟡 WARNING | Physics mismatch | Fix soon |
| 🟢 INFO | Optimization opportunity | Consider |

---

## Audit Categories

### 1. Physics Audit
- Sync strategy matches effect (pessimistic for financial/destructive)
- Timing values align with physics table
- Confirmation patterns present where required

### 2. Performance Audit
- Async waterfalls (sequential awaits)
- Barrel imports from heavy packages
- Missing Suspense boundaries
- Re-render issues

### 3. Protected Audit
- Touch targets ≥ 44px
- Focus rings visible
- Cancel always reachable
- Error recovery paths

### 4. Material Audit
- Shadow layers ≤ 1
- Gradient stops ≤ 2
- Border radius ≤ 16px
- Contrast ratio ≥ 4.5:1

### 5. Animation Audit
- High-frequency = 0ms animation
- Financial/destructive use ease-out
- Reduced motion respected
- SVGs wrapped for GPU

---

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

**Effect Detection**:
- Financial: `claim|withdraw|deposit|transfer|stake|mint|burn`
- Destructive: `delete|remove|destroy|revoke`
- Type patterns: `Currency|Money|Balance|Wei|Token`

**Physics Check**:
- Is `onMutate` present? (bad for financial)
- Check transition/duration values
- Is there a confirm step?

**Protected Check**:
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
│                                                           │
├─ Critical Issues ─────────────────────────────────────────┤
│                                                           │
│  🔴 [Category]: [Message]                                 │
│     File: [path]:[line]                                   │
│     Expected: [expected behavior]                         │
│     Found: [actual behavior]                              │
│     Fix: [how to fix]                                     │
│                                                           │
├─ Warnings ────────────────────────────────────────────────┤
│                                                           │
│  🟡 [Category]: [Message]                                 │
│     File: [path]:[line]                                   │
│     Fix: [how to fix]                                     │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

Save to `grimoires/sigil/ward-report.md`.

### Step 4: Offer Fixes

> "Would you like me to fix any of these issues?"
> - Fix all critical issues
> - Fix specific issue by number
> - Skip

---

## Critical Violations

| Issue | Why Critical |
|-------|--------------|
| Financial + optimistic | Money can't roll back |
| Cancel hidden | User trapped |
| No error recovery | Dead end |
| Focus ring missing | Accessibility |

---

## Detection Patterns

**Financial with optimistic (VIOLATION)**:
```typescript
const { mutate } = useMutation({
  mutationFn: () => claimRewards(amount),
  onMutate: async () => { /* BAD */ }
})
```

**Cancel hidden (VIOLATION)**:
```typescript
{!isPending && <CancelButton />}
```

**No recovery (VIOLATION)**:
```typescript
{isError && <p>Error</p>}
```

---

## Visual Validation

When URL provided, use agent-browser:
1. Open URL
2. Snapshot interactive elements
3. Check touch targets (≥44px)
4. Test focus visibility
5. Capture screenshot

---

## When to Use /ward

- Before a release
- After refactoring
- Periodic health checks
- After adding new components

**Not for**:
- Generating new code → `/craft`
- Single known issue → Edit
- Security audit → `/audit`

---

## Batch Validation: /ward-all

For validating all components in the codebase at once, use `/ward-all`:

```
/ward-all              # Scan default path (src/components)
/ward-all --path src   # Scan custom path
/ward-all --fix        # Auto-fix issues where possible
/ward-all --report     # Generate detailed report file
```

**Auto-fix capabilities**:
| Check | Auto-fixable |
|-------|--------------|
| Touch target < 44px | ✓ Yes |
| Missing focus ring | ✓ Yes |
| Missing physics attribute | ✓ Yes |
| Optimistic for Financial | ✗ No (requires manual review) |
| Missing confirmation | ✗ No (requires manual review) |

See `/ward-all` command documentation for full details.

---

## CI Integration

Add to CI pipeline for continuous physics validation:

```yaml
- name: Physics Validation
  run: /ward-all --severity error
```

Exit codes:
- 0: All checks pass
- 1: Errors found
- 2: Scan failed
