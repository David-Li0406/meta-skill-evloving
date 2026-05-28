# Output Format

## Full Report Example

```markdown
# Quality Verification Report

**Feature**: Add comment functionality
**Branch**: feature/posts-comments
**Date**: 2025-01-20

---

## Executive Summary

**Overall Status**: ✅ APPROVED

**Critical Issues**: 0
**Warnings**: 2
**Suggestions**: 3

---

## Detailed Results

### 1. Spec Compliance ✅

**spec.md ↔ plan.md**:

- ✅ All requirements mapped
- ✅ Technical approach complete
- ✅ No orphaned requirements

**plan.md ↔ tasks.md**:

- ✅ All components have tasks
- ✅ DDD layers properly mapped
- ✅ Dependency order correct

**tasks.md ↔ code**:

- ✅ All tasks completed
- ✅ Implementation follows plan
- ✅ No architectural deviations

**Acceptance Criteria**:

- ✅ 100% coverage (10/10 criteria)
- ✅ All testable
- ✅ All implemented

### 2. Team Codex ✅

- Commit Messages: 10/10 valid ✅
- ESLint: ✅ 0 errors, 0 warnings
- TypeScript: ✅ No errors
- Debug Code: ✅ Clean
- 'any' Types: ⚠️ Found 2 instances
  - `app/posts/_hooks/usePosts.ts:23`
  - `app/posts/_hooks/usePosts.ts:45`

### 3. DDD Architecture ✅

- 4-layer structure: ✅ Complete
- Pattern compliance: ✅ No violations
- SSR rules: ✅ No 'use client' in Repository
- Import validation: ✅ Proper Supabase client usage

### 4. Supabase Integration ✅

- Server client usage: ✅
- RPC patterns: ✅ Matches core-supabase
- Type assertions: ✅ Proper `as unknown as` usage
- Error handling: ✅ Consistent pattern

### 5. Testing ✅

- Total: 15 tests
- Passing: 15 (100%)
- Coverage:
  - Repositories: 92% ✅ (>80%)
  - Hooks: 88% ✅ (>80%)
  - Components: 75% ✅ (>70%)

### 5.5. Browser Testing ✅ (Optional)

- Page Load: ✅ 1.8s
- UI Rendering: ✅ All components visible
- Interactions: ✅ Buttons, forms working
- Console Errors: ✅ None
- MCP Used: playwright

### 6. Constitution ✅

- ✅ Principle I: DDD Architecture
- ✅ Principle II: SSR-First
- ✅ Principle III: Test-Driven Quality
- ✅ Principle IV: Performance Excellence
- ✅ Principle V: API Mode Flexibility
- ✅ Principle VI: Atomic Design System
- ⚠️ Principle VII: Type Safety (2 'any' types)
- ✅ Principle VIII: Spec-Driven Development
- ✅ Principle IX: Agent-Driven Collaboration

**Score**: 8/9 principles satisfied

---

## 🟡 Warnings

1. **Type Safety**: 2 'any' types found
   - File: `app/posts/_hooks/usePosts.ts`
   - Lines: 23, 45
   - Fix: Replace with proper TypeScript types

2. **Documentation**: Missing JSDoc for 3 public methods
   - `PostsRepository.getPosts()`
   - `PostsRepository.createPost()`
   - `PostsRepository.updatePost()`

## 🟢 Suggestions

1. **Performance**: Memoize expensive calculations in `PostsList` component
2. **Accessibility**: Add aria-labels to interactive elements
3. **Testing**: Add edge case tests for empty states

---

## Next Steps

**Status**: ✅ APPROVED WITH WARNINGS

✅ **Can Proceed to PR**

**Recommended Before Merge**:

1. Fix 'any' types (5 minutes)
2. Add JSDoc comments (10 minutes)

**Optional Improvements**:

- Performance optimizations
- Accessibility enhancements
- Additional edge case tests
```

## Return Values

```typescript
{
  status: "APPROVED" | "APPROVED_WITH_WARNINGS" | "REJECTED",
  criticalIssues: number,
  warnings: number,
  suggestions: number,
  report: string, // Markdown formatted
  layers: {
    spec: { passed: boolean, issues: string[] },
    codex: { passed: boolean, issues: string[] },
    architecture: { passed: boolean, issues: string[] },
    supabase: { passed: boolean, issues: string[] },
    tests: { passed: boolean, coverage: object },
    browserTest: {
      passed: boolean,
      skipped: boolean,
      mcp: "playwright" | "chrome-devtools" | null,
      issues: string[]
    },
    constitution: { passed: boolean, score: string }
  }
}
```
