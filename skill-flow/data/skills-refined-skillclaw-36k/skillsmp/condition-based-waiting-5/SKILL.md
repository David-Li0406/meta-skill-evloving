---
name: condition-based-waiting
description: This skill should be used when the user mentions "flaky tests", "race condition", "timing issues", "wait for", "test sometimes fails", or when tests have inconsistent pass/fail behavior. Replaces arbitrary timeouts with condition polling.
allowed-tools: Read, Bash, mcp__plugin_serena_serena, mcp__plugin_serena_serena_*
---

# Condition-Based Waiting

Flaky tests often guess at timing with arbitrary delays.

**Core principle:** Wait for the actual condition that matters, not a guess about how long it takes.

## Core Pattern

```typescript
// ❌ BEFORE: Guessing at timing
await new Promise((r) => setTimeout(r, 50));
const result = getResult();
expect(result).toBeDefined();

// ✅ AFTER: Waiting for condition
await waitFor(() => getResult() !== undefined);
const result = getResult();
expect(result).toBeDefined();
```

## Quick Patterns

| Scenario       | Pattern                                              |
| -------------- | ---------------------------------------------------- |
| Wait for event | `waitFor(() => events.find(e => e.type === 'DONE'))` |
| Wait for state | `waitFor(() => machine.state === 'ready')`           |
| Wait for count | `waitFor(() => items.length >= 5)`                   |
| Wait for file  | `waitFor(() => fs.existsSync(path))`                 |

## Implementation

```typescript
async function waitFor<T>(
  condition: () => T | undefined | null | false,
  description: string,
  timeoutMs = 5000
): Promise<T> {
  const startTime = Date.now();

  while (true) {
    const result = condition();
    if (result) return result;

    if (Date.now() - startTime > timeoutMs) {
      throw new Error(
        `Timeout waiting for ${description} after ${timeoutMs}ms`
      );
    }

    await new Promise((r) => setTimeout(r, 10)); // Poll every 10ms
  }
}
```

See `examples/example.ts` for domain-specific helpers (waitForEvent, waitForEventCount, waitForEventMatch).

## Common Mistakes

| Mistake                | Fix                                     |
| ---------------------- | --------------------------------------- |
| Polling too fast (1ms) | Poll every 10ms                         |
| No timeout             | Always include timeout with clear error |
| Stale data             | Call getter inside loop for fresh data  |

## When Arbitrary Timeout IS Correct

When testing actual timing behavior:

```typescript
// Tool ticks every 100ms - need 2 ticks
await waitForEvent(manager, "TOOL_STARTED"); // First: wait for condition
await new Promise((r) => setTimeout(r, 200)); // Then: wait for known timing
// 200ms = 2 ticks at 100ms - documented and justified
```

Requirements:

1. First wait for triggering condition
2. Based on known timing (not guessing)
3. Comment explaining WHY

## Integration

Referenced by **systematic-debugging** when flaky tests are identified.
