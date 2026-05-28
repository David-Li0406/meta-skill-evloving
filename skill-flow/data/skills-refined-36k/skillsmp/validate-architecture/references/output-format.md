# Output Format

## Report Example

```markdown
# Architecture Validation Report

**Domain**: posts
**Layers**: 4/4 present ✅

---

## Layer Structure ✅

app/posts/
├── _repositories/
│   ├── __tests__/ ✅
│   ├── PostsRepository.ts ✅
│   └── index.ts ✅
├── _api-clients/
│   ├── posts.client.ts ✅
│   └── index.ts ✅
├── _hooks/
│   ├── __tests__/ ✅
│   ├── usePosts.ts ✅
│   └── index.ts ✅
└── _components/
    ├── __tests__/ ✅
    ├── PostsHeader.tsx ✅
    └── index.ts ✅

---

## Pattern Compliance

### Repository Layer ✅
- Server-side only: ✅
- Uses createServerSupabaseClient: ✅
- No 'use client': ✅
- Proper error handling: ✅

### API Client Layer ✅
- Factory Pattern: ✅
- Singleton exported: ✅
- Registered globally: ✅

### Hooks Layer ✅
- Uses React Query: ✅
- Calls API client: ✅
- No direct fetch: ✅

### Components Layer ⚠️
- Uses hooks: ✅
- No direct API access: ✅
- SSR-first: ⚠️ (1 unnecessary 'use client' found)

---

## Summary

**Overall Status**: ⚠️ PASS WITH WARNINGS

**Violations**: 0 critical, 1 warning
**Constitution Compliance**:
- Principle I (DDD Architecture): ✅
- Principle II (SSR-First): ⚠️ (1 issue)

**Next Steps**:
1. Remove unnecessary 'use client' from PostsHeader.tsx
2. Re-run validation after fix
```

## Return Values

```javascript
{
  status: "PASSED" | "PASSED_WITH_WARNINGS" | "FAILED",
  domain: "posts",
  layersPresent: 4,
  violations: {
    critical: 0,
    warnings: 1,
    info: 0
  },
  checks: {
    structure: { passed: true },
    patterns: { passed: true },
    ssr: { passed: false, issues: 1 },
    supabase: { passed: true },
    imports: { passed: true },
    tests: { passed: true }
  },
  report: "markdown string",
  nextSteps: ["action 1", "action 2"]
}
```

## Violation Severity

### 🔴 CRITICAL (Blocks PR)

- Missing required layers
- Repository with 'use client'
- Direct Supabase access in components/hooks
- No Factory Pattern in API clients
- Missing error handling in Repository

### 🟡 WARNING (Should fix)

- Unnecessary 'use client'
- Missing test files
- Suboptimal import patterns
- Missing index.ts exports

### 🟢 INFO (Nice to have)

- Naming convention improvements
- Code organization suggestions

## Quick Fix Examples

### Add Factory Pattern

```typescript
// Before
export class PostsApiClient {}

// After
export class PostsApiClient {}
export const postsClient = new PostsApiClient();
```

### Fix Supabase Pattern

```typescript
// Before
const { data } = await supabase.rpc("posts_read", {});
return data;

// After
const { data, error } = await supabase.rpc("posts_read", {});
if (error) throw new Error(`Failed: ${error.message}`);
return data as unknown as Post[];
```

## Reference Implementations

Points to gold standard implementations:

- **posts domain**: Complete DDD (all patterns correct)
- **dashboard domain**: Activity features example
- **profile domain**: CRUD operations example

## Related Skills

- `verify` - Uses this skill for architecture validation
- `scaffold-domain` - Creates validated structure
- `implement` - Ensures compliance during implementation

## Constitution Compliance

- **Principle I**: DDD Architecture (NON-NEGOTIABLE)
- **Principle II**: SSR-First Development
- Enforces 4-layer separation
- Validates pattern adherence

## Critical Rules

1. **All 4 Layers Required**: Never allow partial structure
2. **No SSR Violations**: Repository MUST be server-side
3. **Factory Pattern**: API clients MUST export singletons
4. **Supabase Patterns**: MUST use RPC functions with error handling
5. **Layer Boundaries**: MUST respect separation of concerns
