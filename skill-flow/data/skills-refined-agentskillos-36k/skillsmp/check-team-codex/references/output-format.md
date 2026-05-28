# Output Format

> **SoT 참조**: 검증 항목과 Severity Levels는 `semo-core/TEAM_RULES.md` 섹션 2에서 관리됩니다.

## Full Report Example

```markdown
# Team Codex Compliance Report

## ✅ Commit Messages (10/10 valid)

Recent commits:

1. feat(posts): Add comment functionality ✅
2. fix(auth): Resolve login redirect ✅
3. test(v0.2.x): Add repository tests ✅
   ...

## ✅ ESLint

✓ 0 errors
✓ 0 warnings
All files pass linting

## ✅ TypeScript

✓ No type errors found
Strict mode: enabled

## ⚠️ Debug Code (2 instances found)

src/app/posts/_hooks/usePosts.ts:15
console.log('Debug: fetching posts');

src/app/posts/_components/PostsList.tsx:42
// TODO: implement pagination

**Action**: Remove before PR

## ⚠️ 'any' Types (3 instances found)

src/app/posts/_api-clients/post.client.ts:23
return response.json() as any;

src/app/posts/_hooks/usePosts.ts:18
params: any

**Action**: Use explicit types

## ✅ Pre-commit Hook

No bypass detected ✅

## ✅ Architecture Compliance

- Repository files: ✅ No 'use client'
- Components: ✅ No direct Supabase imports
- API Clients: ✅ Factory Pattern used
- Layer separation: ✅ Proper boundaries

---

## Summary

**Status**: ⚠️ WARNINGS (Fix before PR)

**Critical Issues**: 0
**Warnings**: 5 (2 debug code, 3 'any' types)
**Passed Checks**: 5/7

**Next Steps**:
1. Remove console.log statements
2. Replace 'any' with explicit types
3. Re-run check before committing
```

## Return Values

```javascript
{
  status: "PASSED" | "WARNINGS" | "FAILED",
  criticalIssues: number,
  warnings: number,
  checks: {
    commits: { passed: true, count: "10/10" },
    eslint: { passed: true, errors: 0, warnings: 0 },
    typescript: { passed: true, errors: 0 },
    debugCode: { passed: false, instances: 2 },
    anyTypes: { passed: false, instances: 3 },
    precommitHook: { passed: true },
    architecture: { passed: true }
  },
  report: "markdown string",
  nextSteps: ["action 1", "action 2"]
}
```

## Quick Fix Suggestions

### Remove Debug Code

```bash
# Find all console.log
grep -r "console\.log" src/

# Find debugger statements
grep -r "debugger" src/
```

### Fix 'any' Types

```typescript
// Before
const data: any = await fetch(...);

// After
const data: GetPostsResponse = await fetch(...);
```

### Fix Commit Message

```bash
# Bad
git commit -m "fixed bug"

# Good
git commit -m "fix(posts): Resolve pagination offset bug"
```
