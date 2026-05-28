---
name: code-review
description: Senior frontend code review for Vue/TypeScript. Use when reviewing PRs, checking code quality, or validating against project conventions.
license: MIT
metadata:
  author: shipitsmarter
  version: "1.0"
---

# Code Review Skill

Senior frontend tech lead code review for Vue 3 / TypeScript projects. Clear, concise, actionable feedback.

---

## Trigger

Use this skill when:
- Reviewing a PR or code changes
- Checking code quality before committing
- Validating component structure against conventions
- Deciding if tests are needed

For **full PR workflow** (checklist verification, release notes, GitHub updates), use the **pr-review** skill instead.

---

## Review Principles

### Be Direct
Lead with the verdict, explain why, suggest how to fix.

### Be Proportional
- **Blocking issues**: Must fix before merge
- **Suggestions**: Nice to have, not required
- **Nits**: One line max, or skip entirely

### Be Helpful
Don't just criticize - show the correct pattern.

---

## Review Process

### Step 1: Run Automated Checks

```bash
npm run lint && npm run type-check
```

Any errors here are **blocking issues**. Report them first.

### Step 2: Check Component Structure

For each changed `.vue` file, verify script order:

1. Types & interfaces
2. Composables
3. Constants
4. Services
5. Props & emits
6. Models
7. Refs & reactives
8. Computed
9. Functions
10. Watchers
11. Lifecycle hooks (always last)

**Common violations:**
- Lifecycle hooks before functions
- Watchers before functions
- Refs defined before composables

### Step 3: Check Conventions

| Convention | Correct | Wrong |
|------------|---------|-------|
| Imports | `@/components/X.vue` | `../../components/X` |
| Types | `unknown` + type guard | `any` |
| Templates | `@click="fn"` | `@click="fn()"` |
| v-for keys | `:key="item.id"` | `:key="index"` |
| Styling | Tailwind classes | `<style>` blocks |
| Functions | Arrow functions | `function` declarations |

### Step 4: Check for Debug Code

```bash
# Console statements (remove before merge)
rg "console\.(log|warn|debug)" --type vue --type ts

# Debugger statements
rg "debugger" --type vue --type ts
```

**Exceptions:**
- `console.error` in error handlers is OK
- `TODO(VIYA-123)` with ticket reference is OK

### Step 5: Evaluate Test Coverage

Use the Test Decision Framework below.

---

## Test Decision Framework

```
Is this a critical business workflow? (payments, shipments, rates)
  YES -> E2E test required

Does the feature cross multiple pages/routes?
  YES -> E2E test required

Is this a new composable or utility function?
  YES -> Unit test required

Is this a bug fix?
  YES -> Test that reproduces the bug

Is this pure refactoring?
  YES -> Existing tests should pass, no new tests

Is this a simple UI/styling change?
  YES -> No tests required
```

### Test Locations

| Code | Location | Example |
|------|----------|---------|
| Component | `src/components/{feature}/__tests__/` | `Button.spec.ts` |
| Composable | `src/composables/__tests__/` | `useFilter.spec.ts` |
| Utility | `src/utils/__tests__/` | `format.spec.ts` |
| E2E | `playwright/tests/app-tests/{feature}/` | `shipment.spec.ts` |

---

## Review Output Format

```markdown
## Review Summary

**Verdict**: [APPROVE / CHANGES REQUESTED / NEEDS DISCUSSION]

### Blocking Issues
- [Issue 1 with file:line]
- [Issue 2 with file:line]
- Or: None

### Suggestions
- [Optional improvement]

### Good Patterns
[One line noting what was done well, or omit]
```

---

## Common Issue Templates

### Script Order Violation

```markdown
**Script order** `ComponentName.vue:89`

Watchers appear before functions. Move to correct position.

Order: Types -> Composables -> Constants -> Services -> Props -> Models -> Refs -> Computed -> Functions -> **Watchers** -> Lifecycle
```

### Missing Type

```markdown
**Add typing** `useData.ts:45`

```typescript
// Before
const data: any = await response.json();

// After  
const data: ShipmentResponse = await response.json();
```
```

### Missing Tests

```markdown
**Missing tests** `useShipmentBulk.ts`

New composable with business logic needs unit tests.

Create: `src/composables/__tests__/useShipmentBulk.spec.ts`
```

### Debug Code

```markdown
**Remove console.log** `ShipmentPage.vue:123`
```

---

## Quick Commands

```bash
# Full check
npm run lint && npm run type-check && npm run build-only:prod

# Changed files only
git diff --name-only origin/main...HEAD | grep -E '\.(vue|ts)$'

# Run specific test
npm run test:unit -- --grep "ComponentName"
```

---

## When to Escalate

Request discussion (not just changes) when:
- Architecture changes affect multiple features
- New patterns that could set precedent
- Security or performance concerns
- Breaking changes to shared components

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| **pr-review** | Full PR workflow with checklist and release notes |
| **vue-component** | Detailed component conventions |
| **unit-testing** | Vitest patterns and mocking |
| **playwright-test** | E2E test structure |
