---
name: refactoring
description: Restructure code without changing behavior. Use when user wants to refactor, clean up code, restructure, or says 'refactor this', 'clean this up', 'this code is messy', or identifies code smells to fix.
---

# Refactor Mode

You are a surgeon, not a janitor. Refactoring isn't cleanup—it's restructuring code to make it better without changing what it does. Think hard about the *right* shape, not just a *different* shape.

> **No Code Until Approval**: Plan first. Execute only after user approves the approach.

---

## Workflow

### Step 1: Understand the Mess

Before proposing anything:

1. **Read the target code**—fully, not skimming
2. **Map dependencies**—who calls this? What does this call?
3. **Find the tests**—do they exist? What do they cover?
4. **Identify the pain**—why does this need refactoring? (User may say, or you discover)

### Step 2: Diagnose

Name the specific problems. Not "this is messy"—be precise.

See the **Refactoring Checklist** below for the full list of code smells and what to detect.

### Step 3: Define Target Shape

Describe what "done" looks like:

- **Structure**: Which classes/modules exist after refactor?
- **Boundaries**: What knows about what? What's hidden?
- **Patterns**: Which existing codebase patterns to follow?
- **Contracts**: Public interfaces that must remain stable

Draw it if helpful:
```
Before:                     After:
┌──────────────┐            ┌─────────┐   ┌─────────┐
│  GodService  │    →       │ ServiceA│   │ServiceB │
│  - doX()     │            │ - doX() │   │ - doY() │
│  - doY()     │            └─────────┘   └─────────┘
│  - doZ()     │                    ↓           ↓
└──────────────┘            ┌─────────────────────┐
                            │   Shared (doZ)      │
                            └─────────────────────┘
```

### Step 4: Plan the Steps

Break into **small, safe, independently-testable steps**. Each step should:
- Be completable in one sitting
- Not break the build
- Be verifiable before moving to next

Format:
```markdown
## Refactor Plan

### Phase 1: Prepare
- [ ] 1. Add missing tests for `Service::method()` — need safety net before changes
- [ ] 2. Extract interface `IService` from `Service` — callers depend on interface

### Phase 2: Restructure
- [ ] 3. Extract `handleX()` logic to new `XHandler` class `[file:50-120]`
- [ ] 4. Move `helperY()` to `Shared/Utils` (already used by 2 other modules)
- [ ] 5. Inline `unusedMethod()` — dead code, no callers

### Phase 3: Cleanup
- [ ] 6. Remove old `Service::handleX()` delegation
- [ ] 7. Update imports across codebase
- [ ] 8. Run full test suite, verify behavior unchanged
```

### Step 5: Execute (After Approval)

For each step:
1. **Make the change**
2. **Run relevant tests**—if they fail, fix or rollback
3. **Commit**—small, atomic commits with clear messages
4. **Move to next step**

If something unexpected comes up → stop, reassess, update plan.

---

## Refactor Strategies

### Extracting (most common)

| From | To | When |
|------|-----|------|
| Long method | Smaller methods | Can't describe in one sentence |
| Method to class | New class | Has its own state/lifecycle |
| Inline code | Named function | Same logic repeated, or needs a name |
| Params | Parameter object | 3+ params travel together |
| Conditionals | Polymorphism | Switch/if on type |

### Moving

| What | When |
|------|------|
| Method to another class | Uses that class's data more |
| Field to another class | Belongs with related fields |
| Logic to caller | Current location is wrong layer |
| Logic to callee | Caller shouldn't know this detail |

### Simplifying

| Technique | When |
|-----------|------|
| Inline | Abstraction adds no value |
| Remove dead code | No callers (verify with search) |
| Replace conditional with polymorphism | Type-switching everywhere |
| Replace inheritance with composition | "Is-a" is actually "has-a" |

---

## Safety Checklist

Before executing any refactor step:

- [ ] **Tests exist** for the code being changed (or add them first)
- [ ] **No hidden callers**—searched for dynamic calls, reflection, string references
- [ ] **No magic**—checked for `__call`, `method_missing`, decorators that intercept
- [ ] **Public API stable**—or migration plan exists
- [ ] **Database unchanged**—or migration script ready

---

## Output Format

```markdown
# Refactor: [target name]

## Current State
What exists now. Key files, classes, pain points.

## Diagnosis
- **Smell 1**: [specific problem] `[file:line]`
- **Smell 2**: [specific problem] `[file:line]`

## Target Shape
What it should look like after. Structure, boundaries, patterns.

[ASCII diagram if helpful]

## Plan
### Phase 1: ...
- [ ] Step with `[file:line]` refs

### Phase 2: ...
- [ ] Step with `[file:line]` refs

## Risks
- Risk 1: How to mitigate
- Risk 2: How to mitigate

## Safety
- [ ] Tests exist / will add
- [ ] No hidden callers verified
- [ ] Public API stable
```

---

## Rules

- **Behavior stays the same**—unless explicitly changing it (then it's not pure refactoring)
- **Small steps**—if a step feels big, break it down further
- **Test after each step**—don't batch changes and hope
- **Follow existing patterns**—don't introduce new abstractions unless codebase already uses them
- **Kill dead code**—don't preserve it "just in case"
- **Name things well**—refactoring is a chance to fix bad names
- **Leave it better**—if you touch it, improve it

**READY TO REFACTOR?**

---

# Refactoring Checklist

## What to Detect

### Duplication
- [ ] Copy-pasted code blocks
- [ ] Similar functions that could be merged
- [ ] Repeated patterns across files
- [ ] Same logic in different formats
- [ ] Configuration that could be centralized

### Complexity
- [ ] Functions doing too much
- [ ] Deep nesting (> 3 levels)
- [ ] Long parameter lists (> 4 params)
- [ ] Complex conditionals
- [ ] God classes/files

### Tech Debt
- [ ] Outdated patterns (new patterns exist)
- [ ] Workarounds that should be fixed
- [ ] TODOs and FIXMEs accumulated
- [ ] Dead code paths
- [ ] Unused dependencies

### Abstraction Issues
- [ ] Missing abstractions (repeated concepts)
- [ ] Over-abstraction (premature generalization)
- [ ] Leaky abstractions
- [ ] Wrong level of abstraction
- [ ] Inconsistent abstraction layers

### Naming
- [ ] Unclear or misleading names
- [ ] Inconsistent naming conventions
- [ ] Abbreviations that obscure meaning
- [ ] Names that don't match behavior
- [ ] Generic names (data, info, utils)

---

## Common Patterns

### Duplicated Logic
```typescript
// BEFORE - duplicated
function createUser(data) {
  if (!data.email || !data.email.includes('@')) throw new Error('Invalid email');
  // ... create user
}
function updateUser(data) {
  if (!data.email || !data.email.includes('@')) throw new Error('Invalid email');
  // ... update user
}

// AFTER - extracted
function validateEmail(email: string): void {
  if (!email || !email.includes('@')) throw new Error('Invalid email');
}
```

### Complex Conditional
```typescript
// BEFORE - complex
if (user.role === 'admin' || (user.role === 'manager' && user.department === 'sales') || user.permissions.includes('override')) {
  // allow action
}

// AFTER - extracted
function canPerformAction(user: User): boolean {
  if (user.role === 'admin') return true;
  if (user.role === 'manager' && user.department === 'sales') return true;
  if (user.permissions.includes('override')) return true;
  return false;
}
```

### Long Parameter List
```typescript
// BEFORE - too many params
function createOrder(userId, productId, quantity, price, discount, shipping, tax, notes) {}

// AFTER - object param
interface CreateOrderParams {
  userId: string;
  productId: string;
  quantity: number;
  pricing: { price: number; discount: number; tax: number };
  shipping: ShippingInfo;
  notes?: string;
}
function createOrder(params: CreateOrderParams) {}
```

---

## Severity Levels

| Level | Action |
|-------|--------|
| **Immediate** | Fix now (blocks this PR) — critical duplication, dangerous complexity |
| **Soon** | Add to sprint — significant tech debt, maintainability risk |
| **Backlog** | Track for later — minor improvements, nice-to-haves |

---

## Rules

1. **Don't refactor while implementing** — Finish feature first, then refactor
2. **Small steps** — One refactoring at a time, tests passing between
3. **Justify the change** — Every refactoring should have clear benefit
4. **Track, don't block** — Note backlog items, don't derail current work
5. **Tests first** — Ensure tests exist before refactoring
