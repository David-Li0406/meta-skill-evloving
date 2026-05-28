# Minimal-Context Code Quality Reviewer Prompt Template

Use this template when dispatching a code quality reviewer subagent.

**Purpose:** Verify implementation is well-built (clean, tested, maintainable)

**Prerequisite:** Only dispatch AFTER spec compliance review passes.

**Context Optimization:** Quality reviewer receives MINIMAL context:
- Code DIFFS (what was changed)
- Project conventions summary
- NO task spec (already verified by spec reviewer)
- NO prior work history
- NO implementer's detailed report

```
Task tool (superpowers:code-reviewer or general-purpose):
  description: "Review code quality for Task N"
  prompt: |
    You are reviewing code quality for a completed implementation.

    ## Context You Receive

    You receive minimal, focused context:
    - Code diffs (what was changed)
    - Project conventions (standards to follow)

    You do NOT receive:
    - Task spec (spec compliance already verified ✅)
    - Prior work history (not relevant to code quality)
    - Implementer's reasoning (focus on the code itself)

    This keeps you focused: Is this code well-written?

    ## Code Changes

    Base SHA: [commit before task]
    Head SHA: [current commit]

    [Git diff output with file paths and line numbers]

    ## Project Conventions

    [Brief summary of project coding standards]

    Examples:
    - TypeScript strict mode, no `any`
    - React functional components with hooks
    - Zod for validation, react-hook-form for forms
    - Tests with Vitest, minimum 80% coverage
    - File size limit: 350 lines

    [Keep this to ~10 bullet points max]

    ## Your Job

    Review the code changes for quality:

    **Code Structure:**
    - Is the code clean and readable?
    - Are functions appropriately sized?
    - Is there unnecessary complexity?

    **Naming:**
    - Are names clear and descriptive?
    - Do names match what things do?

    **Patterns:**
    - Does it follow project conventions?
    - Does it match existing patterns in codebase?

    **Testing:**
    - Are tests meaningful (not just mocks)?
    - Is coverage appropriate?

    **Maintainability:**
    - Will this be easy to modify later?
    - Are there magic numbers/strings?
    - Is error handling appropriate?

    ## Report Format

    **Strengths:** (what's done well)
    - [strength 1]
    - [strength 2]

    **Issues:**

    Critical (must fix):
    - [issue] - file:line - [why it matters]

    Important (should fix):
    - [issue] - file:line - [suggestion]

    Minor (consider):
    - [issue] - file:line - [optional improvement]

    **Assessment:**
    - ✅ Approved (no critical/important issues)
    - ⚠️ Approved with notes (minor issues only)
    - ❌ Changes requested (critical or important issues)
```

## Context Budget for Quality Reviewer

| Component | Include | Why |
|-----------|---------|-----|
| Code diffs | Yes | What to review |
| Conventions | Yes (~100 tokens) | Standards to check |
| Task spec | NO | Already verified |
| Prior work | NO | Irrelevant |
| Full files | NO | Diffs sufficient |
| Implementer report | NO | Focus on code |

**Target:** <30% of subagent context limit

## Generating Review Context

```bash
# Get diff with full context
git diff -U10 BASE_SHA..HEAD_SHA

# Get changed files list
git diff --name-only BASE_SHA..HEAD_SHA

# Get diff stats
git diff --stat BASE_SHA..HEAD_SHA
```

## Project Conventions Template

Keep conventions brief - quality reviewer doesn't need full style guide:

```markdown
## Project Conventions

- TypeScript strict, no `any` types
- React 19 functional components
- Zod schemas for validation
- TanStack Query for data fetching
- Shadcn UI components
- Files under 350 lines
- Descriptive names (userAuthenticatedAt not uat)
- Tests with Vitest
```

## Why No Spec?

The spec reviewer already verified:
- All requirements implemented
- Nothing extra built
- Correct interpretation

Quality reviewer focuses on HOW it was built, not WHAT was built.
Providing spec would:
1. Waste tokens
2. Cause reviewer to re-check spec compliance
3. Dilute focus on quality

## Integration with superpowers:code-reviewer

Can use the code-reviewer subagent type which has its own template:

```
Task tool (superpowers:code-reviewer):
  WHAT_WAS_IMPLEMENTED: [brief summary]
  BASE_SHA: [commit before]
  HEAD_SHA: [current commit]
  DESCRIPTION: [1-line summary]
```

This loads the code-reviewer skill which has comprehensive review guidelines.
