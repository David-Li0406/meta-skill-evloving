---
name: pinpoint-testing
description: Use this skill when writing tests, debugging test failures, or when user mentions testing/test/spec/E2E.
---

# PinPoint Testing Guide

## When to Use This Skill

Use this skill when:
- Writing new tests (unit, integration, or E2E)
- Debugging test failures
- Setting up test infrastructure
- Understanding test patterns and organization
- User mentions: "test", "testing", "spec", "E2E", "Playwright", "Vitest", "coverage"

## Quick Reference

### Test Distribution (100-150 tests total)
- **70% Unit (~70-100)**: Pure functions, utilities, validation
- **25% Integration (~25-35)**: DB queries with worker-scoped PGlite
- **5% E2E (~5-10)**: Critical flows (Playwright)

### Commands
```bash
pnpm run check          # Quick: types + lint + unit (~5s)
pnpm test               # Unit tests only
pnpm test -- path/to/file.test.ts  # Targeted unit test
pnpm run test:integration          # DB integration tests (requires supabase start)
pnpm run smoke                     # E2E smoke tests (Playwright)
pnpm run preflight                 # Full suite (~60s) - run before commit
```

### Critical Rules
1. **Worker-scoped PGlite only**: Per-test instances cause lockups
2. **No testing Server Components directly**: Use E2E instead
3. **Test behavior, not implementation**: Focus on outcomes
4. **Integration tests location**: `src/test/integration/supabase/*.test.ts`

## Detailed Documentation

Read these files for comprehensive testing guidance:

```bash
# Full testing strategy and patterns
cat docs/TESTING_PLAN.md

# E2E-specific patterns with Playwright
cat docs/E2E_BEST_PRACTICES.md

# Testing-related non-negotiables
cat docs/NON_NEGOTIABLES.md | grep -A 10 "## Testing"
```

## Code Examples

### Unit Test Pattern
```typescript
// Pure function testing
import { describe, it, expect } from "vitest";
import { calculateSeverityScore } from "~/lib/utils";

describe("calculateSeverityScore", () => {
  it("returns 10 for unplayable", () => {
    expect(calculateSeverityScore("unplayable")).toBe(10);
  });

  it("returns 5 for playable", () => {
    expect(calculateSeverityScore("playable")).toBe(5);
  });

  it("returns 1 for minor", () => {
    expect(calculateSeverityScore("minor")).toBe(1);
  });
});
```

### Integration Test with PGlite (Worker-Scoped)
```typescript
import { describe, it, expect, beforeAll } from "vitest";
import { getPGlite } from "~/lib/db"; // Example import

describe("Integration Test with PGlite", () => {
  beforeAll(async () => {
    // Setup code here
  });

  it("should perform a database query", async () => {
    const result = await getPGlite("some query");
    expect(result).toBeDefined();
  });
});
```