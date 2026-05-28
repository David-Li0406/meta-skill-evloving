---
name: code-review-evaluation
description: Evaluate external PR suggestions (Gemini, CodeRabbit) against project conventions. Use when asked to review or agree with external code review comments.
---

# Code Review Evaluation Skill

## Purpose

Evaluate external code review suggestions (Gemini, CodeRabbit, etc.) against project conventions. These tools have access to our codebase and often make valid suggestions - but they don't know our **project-specific conventions**.

## What External Reviewers ARE Good At

CodeRabbit, Gemini, etc. **can see your code** and are excellent at catching:

- ✅ **Missing fields** in examples/docs (like missing `geoScope` in docstring)
- ✅ **Type mismatches** and inconsistencies
- ✅ **Unused imports/variables**
- ✅ **Potential null/undefined errors**
- ✅ **Security vulnerabilities** (generic patterns)
- ✅ **Documentation gaps**
- ✅ **Test coverage suggestions**
- ✅ **General best practices** (accessibility, performance)

**These suggestions are usually VALID - agree with them!**

## What External Reviewers DON'T Know

They lack context about our **project-specific conventions**:

- ❌ Our `@i18n/routing` Link requirement
- ❌ Our `/types` directory governance
- ❌ Our three-layer API proxy pattern
- ❌ Our design system semantic classes
- ❌ Our env variable 4-location rule
- ❌ Our $300 searchParams incident history

**Only check skills when suggestion involves these patterns.**

## Evaluation Framework

When user asks "Do you agree with this suggestion?":

### Step 1: Categorize the Suggestion

| Category            | Examples                                   | Default Response  |
| ------------------- | ------------------------------------------ | ----------------- |
| **Bug/Error fix**   | Missing field, type error, null check      | Usually **AGREE** |
| **Documentation**   | Missing JSDoc, outdated example            | Usually **AGREE** |
| **Code quality**    | Unused code, simplification                | Usually **AGREE** |
| **Code complexity** | >100 lines/function, >10 props, >3 nesting | Usually **AGREE** |
| **Pattern change**  | Different import, new abstraction          | **CHECK SKILLS**  |
| **Architecture**    | Component structure, API calls             | **CHECK SKILLS**  |

### Step 2: If Pattern/Architecture → Cross-Reference Skills

Only check skills if the suggestion involves patterns we have rules for:

| Skill                          | Check For                                           |
| ------------------------------ | --------------------------------------------------- |
| `pre-implementation-checklist` | Does suggestion duplicate existing code?            |
| `type-system-governance`       | Does it create types outside `/types`?              |
| `react-nextjs-patterns`        | Does it violate server-first pattern?               |
| `api-layer-patterns`           | Does it bypass three-layer proxy?                   |
| `url-canonicalization`         | Does it add `searchParams` to listing pages?        |
| `i18n-best-practices`          | Does it use `next/link` instead of `@i18n/routing`? |
| `design-system-conventions`    | Does it use `gray-*` or arbitrary utilities?        |
| `env-variable-management`      | Does it add env var without all 4 locations?        |
| `data-validation-patterns`     | Does it skip Zod validation?                        |
| `security-headers-csp`         | Does it use raw `fetch()` without wrappers?         |

### Step 3: Provide Structured Response

## Response Template

```markdown
## Evaluation: [Suggestion Title/Topic]

### Summary

[1-2 sentence summary of the suggestion]

### Category

[Bug fix / Documentation / Code quality / Pattern change / Architecture]

### Skill Check (if pattern/architecture)

- [ ] [Relevant skill] - [Pass/Conflict: reason]

### Recommendation

**[AGREE / DISAGREE / PARTIAL]**

[Explanation]
```

## Example: Valid Suggestion (AGREE)

**CodeRabbit says**: "Docstring example missing geoScope field"

```markdown
## Evaluation: Missing geoScope in docstring

### Summary

Example in JSDoc is missing a required field from the type.

### Category

Documentation - external reviewer caught a real inconsistency.

### Skill Check

Not needed - this is a documentation fix, not a pattern change.

### Recommendation

**AGREE** - The docstring example should match the actual type definition.
```

## Project-Specific Blind Spots (CHECK SKILLS)

Only disagree when suggestion conflicts with our conventions:

### 1. "Use `next/link` directly"

**Our rule**: Always use `Link` from `@i18n/routing`
**Response**: Disagree - breaks locale handling

### 2. "Add types inline in component"

**Our rule**: All types in `/types` directory
**Response**: Disagree - violates type governance

### 3. "Use `gray-500` for text"

**Our rule**: Use semantic tokens (`text-foreground/80`)
**Response**: Disagree - violates design system

### 4. "Add searchParams to page component for filtering"

**Our rule**: NEVER in listing pages (causes $300+ cost spikes)
**Response**: Disagree - violates url-canonicalization (CRITICAL)

### 5. "Use raw fetch() for this API call"

**Our rule**: Use `fetchWithHmac` or `safeFetch`
**Response**: Disagree - violates security patterns

### 6. "Create a helper function here"

**Our rule**: Search for existing patterns first
**Response**: Partial - check if pattern exists before creating

### 7. "Use axios instead of fetch"

**Our rule**: Use `fetchWithHmac` (internal) or `safeFetch` (external)
**Response**: Disagree - we have standardized fetch wrappers

### 8. "Prefer @types/\* path alias over bare types/ path"

**Our rule**: Use `types/*` not `@types/*`
**Response**: Disagree - `@types/*` conflicts with TypeScript's convention for type definition packages (e.g., `@types/react`, `@types/node`). We intentionally use `types/*` to avoid this collision.

## Quick Decision Tree

```text
Is the suggestion about...?
│
├─ Bug/error fix → Usually AGREE ✅
├─ Missing docs/fields → Usually AGREE ✅
├─ Unused code cleanup → Usually AGREE ✅
├─ Test coverage → Usually AGREE ✅
│
├─ Types/interfaces → Check type-system-governance
├─ Components → Check react-nextjs-patterns
├─ Styling → Check design-system-conventions
├─ API calls → Check api-layer-patterns
├─ URLs/routing → Check url-canonicalization
├─ Links → Check i18n-best-practices
├─ Env vars → Check env-variable-management
├─ Validation → Check data-validation-patterns
├─ Security → Check security-headers-csp
├─ New utility → Check pre-implementation-checklist
```

## More Examples

### Example: Missing Field in Docstring (AGREE)

**Suggestion**: "Docstring example missing geoScope field"

**Response**: **AGREE** - External reviewer correctly identified inconsistency between example and type.

### Example: Suggestion to use `useMemo` (PARTIAL)

**Suggestion**: "Wrap this computation in useMemo for performance"

**Response**: **PARTIAL** - Only if profiling shows actual bottleneck. Don't prematurely optimize.

### Example: Suggestion to inline styles (DISAGREE)

**Suggestion**: "Use inline className with Tailwind utilities"

**Response**: **DISAGREE** - `design-system-conventions` requires semantic classes.

## When to AGREE (Most Cases)

External reviewers are usually right about:

- Missing fields in docs/examples
- Type inconsistencies
- Unused imports/variables
- Null/undefined safety
- Documentation improvements
- Test coverage gaps
- Accessibility issues
- General security issues

## When to DISAGREE (Project-Specific)

Only disagree when suggestion conflicts with our skills:

- Uses `next/link` instead of `@i18n/routing`
- Creates types outside `/types`
- Uses `gray-*` instead of semantic tokens
- Adds `searchParams` to listing pages
- Uses raw `fetch()` instead of our wrappers
- Bypasses three-layer API pattern
- Adds env var without 4-location update

## Checklist

- [ ] What category is this? (Bug fix / Docs / Code quality / Pattern)
- [ ] If pattern change → check relevant skills
- [ ] Does it conflict with project conventions?
- [ ] Provide clear AGREE / DISAGREE / PARTIAL response
