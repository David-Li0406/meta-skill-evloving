---
name: flaky-fix
description: Use this skill when you need to suggest and apply fixes for flaky tests identified by flaky-detect, ensuring reliable test execution.
---

# Flaky Fix Skill

## Purpose

Analyze flaky test patterns and suggest or auto-apply fixes. This skill leverages research indicating that LLMs can effectively repair flaky tests through targeted prompts.

## Research Foundation

| Finding | Source | Reference |
|---------|--------|-----------|
| LLM Auto-repair | FlakyFix (2023) | [arXiv:2307.00012](https://arxiv.org/html/2307.00012v4) - 70%+ success rate |
| Flaky Taxonomy | Google (2016) | [Flaky Tests Study](https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html) |
| Pattern-based Fixes | FlaKat (2024) | [arXiv:2403.01003](https://arxiv.org/abs/2403.01003) |

## When This Skill Applies

- After `flaky-detect` identifies flaky tests.
- When a user requests to "fix flaky test" or "make test reliable."
- If CI is failing intermittently on specific tests.
- When a test marked as flaky needs repair.

## Trigger Phrases

| Natural Language | Action |
|------------------|--------|
| "Fix this flaky test" | Analyze and suggest fix |
| "Make this test reliable" | Apply deterministic patterns |
| "Why is this test flaky?" | Root cause analysis + fix |
| "Auto-fix flaky tests" | Batch fix safe patterns |
| "Remove timing dependency" | Specific timing fix |

## Fix Patterns by Category

### 1. Timing Issues (45% of flaky tests)

#### Problem: Uses Real Time
```typescript
// FLAKY: Time-dependent
it('should expire after 1 hour', () => {
  const token = createToken();
  expect(token.expiresAt).toBeGreaterThan(Date.now());
});
```

#### Fix: Mock Time
```typescript
// FIXED: Mocked time
it('should expire after 1 hour', () => {
  const fixedTime = new Date('2024-01-01T00:00:00Z');
  vi.setSystemTime(fixedTime);

  const token = createToken();

  expect(token.expiresAt).toBe(fixedTime.getTime() + 3600000);
  vi.useRealTimers();
});
```

#### Problem: Explicit Sleep/Delay
```typescript
// FLAKY: Arbitrary delay
it('should complete async operation', async () => {
  startAsyncOperation();
  await sleep(100);  // Race condition!
  expect(result).toBeDefined();
});
```

#### Fix: Proper Async Handling
```typescript
// FIXED: Wait for actual completion
it('should complete async operation', async () => {
  const result = await startAsyncOperation();
  expect(result).toBeDefined();
});

// Or use waitFor for DOM
it('should show loading state', async () => {
  // Implementation here...
});
```