# Verification Layers Detail

## Layer 1: Spec Compliance (Integrated speckit.analyze)

**Purpose**: Cross-artifact consistency validation

**Checks**:

- ✅ spec.md ↔ plan.md alignment
  - All requirements mapped to plan sections
  - No orphaned requirements
  - Technical approach addresses all scenarios

- ✅ plan.md ↔ tasks.md alignment
  - All plan components have corresponding tasks
  - DDD layers properly mapped
  - No missing implementation tasks

- ✅ tasks.md ↔ code alignment
  - All tasks completed or in-progress
  - Code follows plan architecture
  - No deviation from technical approach

- ✅ Acceptance criteria coverage
  - All criteria testable
  - All criteria implemented
  - Edge cases handled

**Process**:

1. Parse spec.md, plan.md, tasks.md
2. Build dependency graph
3. Cross-reference implementation
4. Report gaps and inconsistencies

**Note**: This replaces `/speckit.analyze` command - analysis is fully integrated

## Layer 2: Team Codex Compliance

**Invokes**: `skill:check-team-codex`

**Checks**:

- ✅ Commit message format (last 10 commits)
  - Format: `type(scope): subject`
  - Valid types: feat, fix, docs, test, refactor, style, chore
  - Gitmoji usage (recommended)

- ✅ ESLint (zero errors/warnings expected)

  ```bash
  npm run lint
  ```

- ✅ TypeScript (zero type errors expected)

  ```bash
  npx tsc --noEmit
  ```

- ✅ Debug code detection
  - Search for `console.log`, `console.debug`, `debugger`
  - Check for commented-out code blocks

- ✅ 'any' type detection
  - Scan for TypeScript `any` usage
  - Report file/line references

- ✅ Hook bypass detection
  - Verify no `--no-verify` in commit history
  - Check for hook circumvention patterns

## Layer 3: DDD Architecture Compliance

**Invokes**: `skill:validate-architecture`

**Checks**:

- ✅ 4-layer structure exists

  ```text
  app/{domain}/_repositories/
  app/{domain}/_api-clients/
  app/{domain}/_hooks/
  app/{domain}/_components/
  ```

- ✅ Layer pattern compliance
  - Repository: `createServerSupabaseClient`, no 'use client'
  - API Client: Factory Pattern, registered in lib/api-clients/
  - Hooks: React Query patterns, no direct DB access
  - Components: Proper separation of concerns

- ✅ SSR rules validation
  - No 'use client' in Repository layer
  - No browser APIs in server components
  - Proper client boundary markers

- ✅ Import validation
  - No direct `@supabase/supabase-js` imports in components
  - Proper use of client/server Supabase instances

## Layer 4: Supabase Pattern Verification

**Checks**:

- ✅ Repository uses `createServerSupabaseClient`

  ```typescript
  const supabase = await createServerSupabaseClient();
  ```

- ✅ RPC function naming (core-supabase patterns)
  - Check against core-supabase repository
  - Verify parameter structure matches
  - Confirm return type handling

- ✅ Type assertions pattern

  ```typescript
  return data as unknown as Type;
  ```

- ✅ Error handling implementation

  ```typescript
  if (error) throw new Error(error.message);
  ```

## Layer 5: Test Coverage and Quality

**Checks**:

- ✅ Run all tests

  ```bash
  npm test
  ```

- ✅ Generate coverage report

  ```bash
  npm run test:coverage
  ```

- ✅ Validate coverage thresholds:
  - Repositories: >80%
  - Hooks: >80%
  - Components: >70%

- ✅ Test quality patterns
  - Repository tests: Proper Supabase mocking
  - Hook tests: React Query testing patterns
  - Component tests: User interaction testing
  - No skipped tests (`it.skip`, `describe.skip`)

## Layer 6: Constitution Principles Validation

**Checks all 9 principles**:

1. ✅ **DDD Architecture** (Principle I)
   - 4-layer structure complete
   - Domain boundaries clear

2. ✅ **SSR-First** (Principle II)
   - Server Components by default
   - Minimal client boundaries

3. ✅ **Test-Driven Quality** (Principle III)
   - Tests written before implementation
   - Coverage thresholds met

4. ✅ **Performance Excellence** (Principle IV)
   - Bundle size targets met
   - No obvious performance issues

5. ✅ **API Mode Flexibility** (Principle V)
   - Factory Pattern implemented
   - Environment variable configuration

6. ✅ **Atomic Design System** (Principle VI)
   - Components in correct atomic layer
   - No architectural mixing

7. ✅ **Type Safety** (Principle VII)
   - No 'any' types
   - Proper Supabase type generation

8. ✅ **Spec-Driven Development** (Principle VIII)
   - spec.md → plan.md → tasks.md exists
   - Cross-artifact alignment

9. ✅ **Agent-Driven Collaboration** (Principle IX)
   - Phase-gated approvals received
   - Documentation complete
