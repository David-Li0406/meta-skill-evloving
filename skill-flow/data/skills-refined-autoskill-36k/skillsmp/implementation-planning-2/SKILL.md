---
name: Implementation Planning
description: Create detailed implementation plans with atomic tasks and verification steps
version: 1.0.0
source: Adapted from obra/superpowers
---

# Implementation Planning

## Purpose

Generate comprehensive implementation plans that:
- Break work into atomic 2-5 minute tasks
- Include exact file paths and code examples
- Follow TDD principles (test first)
- Enable parallel or sequential execution
- Allow engineers with minimal context to execute

## Plan Header Template

```markdown
# Implementation Plan: [Feature Name]

**Date**: YYYY-MM-DD
**Author**: Claude Code
**Status**: Draft | Ready | In Progress | Complete

## Goal
[1-2 sentence description of what we're building and why]

## Architecture Context
[Brief description of how this fits into the existing system]

## Tech Stack
- Framework: Next.js 14 (App Router)
- Styling: Tailwind CSS + shadcn/ui
- Testing: Vitest + Playwright
- Database: [if applicable]

## Prerequisites
- [ ] [Any setup needed before starting]
- [ ] [Dependencies to install]
- [ ] [Access/credentials required]

## Estimated Scope
- Tasks: [N] tasks
- Time: [X] hours (at 2-5 min/task average)
- Complexity: Low | Medium | High
```

## Task Structure

Each task follows the TDD cycle:

```markdown
### Task [N]: [Brief Description]

**File**: `src/path/to/file.ts`
**Type**: Test | Implementation | Refactor | Config

#### 1. Write Test (RED)
```typescript
// tests/unit/feature.test.ts
describe('featureName', () => {
  it('should [expected behavior]', () => {
    // Arrange
    const input = { ... };

    // Act
    const result = featureName(input);

    // Assert
    expect(result).toBe(expected);
  });
});
```

#### 2. Run Test - Expect Failure
```bash
npm test -- feature.test.ts
# Expected: FAIL - featureName is not defined
```

#### 3. Implement (GREEN)
```typescript
// src/lib/feature.ts
export function featureName(input: Input): Output {
  // Minimal implementation
  return result;
}
```

#### 4. Run Test - Expect Pass
```bash
npm test -- feature.test.ts
# Expected: PASS
```

#### 5. Verify No Regressions
```bash
npm test
# Expected: All tests pass
```

#### 6. Commit
```bash
git add src/lib/feature.ts tests/unit/feature.test.ts
git commit -m "feat: add featureName function with tests"
```

---
```

## Plan Organization

### For Sequential Execution

```markdown
## Tasks

### Phase 1: Foundation
1. Task 1: Create types/interfaces
2. Task 2: Write unit tests for core logic
3. Task 3: Implement core logic

### Phase 2: Integration
4. Task 4: Write API route tests
5. Task 5: Implement API route
6. Task 6: Integration test

### Phase 3: UI
7. Task 7: Write component tests
8. Task 8: Implement component
9. Task 9: E2E test

### Phase 4: Polish
10. Task 10: Error handling
11. Task 11: Loading states
12. Task 12: Documentation
```

### For Parallel Execution

```markdown
## Tasks (Parallelizable)

### Stream A: Backend (Agent 1)
- Task A1: API types
- Task A2: API tests
- Task A3: API implementation

### Stream B: Frontend (Agent 2)
- Task B1: Component types
- Task B2: Component tests
- Task B3: Component implementation

### Stream C: Infrastructure (Agent 3)
- Task C1: Database schema
- Task C2: Migration scripts
- Task C3: Seed data

### Integration Point
After A3, B3, C3 complete:
- Task I1: Integration tests
- Task I2: E2E tests
```

## Guidelines

### Task Granularity
- **Too big**: "Implement authentication" (hours)
- **Just right**: "Write test for login validation" (3 min)
- **Too small**: "Add import statement" (30 sec)

### Code Examples
- **Always provide complete code** in plans
- Never write "add validation" - show THE validation code
- Include imports, types, error handling

### File Paths
- **Always use exact paths**: `src/components/auth/LoginForm.tsx`
- Never use relative references like "the auth folder"

### Commands
- **Include exact commands** with expected output
- Show both success and failure expectations

### Dependencies
- List any skills to reference: `@test-driven-development`
- Link to related documentation

## Execution Options

After plan completion, offer:

### Option 1: Subagent-Driven
```
Spawn fresh subagent for each task within current session.
Best for: Complex tasks needing verification between steps.
```

### Option 2: Parallel Sessions
```
Execute using @parallel-agents skill.
Best for: Independent streams that don't conflict.
```

### Option 3: Manual Execution
```
Human executes tasks following the plan.
Best for: Learning, sensitive changes, production deployments.
```

## FrankX Example Plan

```markdown
# Implementation Plan: Email Signup Enhancement

**Date**: 2026-01-20
**Goal**: Add validation, rate limiting, and success animation to email signup

## Tasks

### Task 1: Add Zod Schema
**File**: `lib/validation.ts`

#### 1. Write Test
```typescript
describe('emailSignupSchema', () => {
  it('should reject invalid emails', () => {
    const result = emailSignupSchema.safeParse({ email: 'invalid' });
    expect(result.success).toBe(false);
  });

  it('should accept valid emails', () => {
    const result = emailSignupSchema.safeParse({ email: 'test@example.com' });
    expect(result.success).toBe(true);
  });
});
```

#### 2. Implement
```typescript
import { z } from 'zod';

export const emailSignupSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
});
```

---

### Task 2: Add Rate Limiting
**File**: `app/api/subscribe/route.ts`
[... continues with same structure ...]
```

## Plan Storage

Save plans to: `docs/plans/YYYY-MM-DD-feature-name.md`

```
docs/
└── plans/
    ├── 2026-01-15-email-signup.md
    ├── 2026-01-18-pdf-download.md
    └── 2026-01-20-blog-comments.md
```

## When to Use This Skill

- Before starting any multi-step feature
- When handing off work to another developer
- When breaking complex tasks into sprints
- For documentation of implementation approach

## Related Skills

- `test-driven-development` - Each task follows TDD
- `parallel-agents` - Execute streams concurrently
- `systematic-debugging` - When tasks fail
