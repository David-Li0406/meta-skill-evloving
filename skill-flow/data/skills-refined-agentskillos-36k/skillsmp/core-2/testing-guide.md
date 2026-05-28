# Testing Guide

**PAI-specific testing preferences. For generic testing patterns (TDD, test pyramid, Vitest API, Playwright API), Claude knows these intrinsically.**

---

## PAI Testing Stack

| Type | Tool | Command |
|------|------|---------|
| Unit/Integration | Bun test (Vitest-compatible) | `bun test` |
| E2E | Playwright | `bun playwright test` |
| Coverage | Bun built-in | `bun test --coverage` |

---

## Key Commands

```bash
# Unit tests
bun test                    # Run all
bun test --watch            # Watch mode
bun test path/to/file.test.ts  # Specific file

# E2E tests
bun playwright test         # Run all
bun playwright test --ui    # Interactive
bunx playwright show-report # View report
```

---

## File Naming

```
src/
├── utils.ts
├── utils.test.ts          # Co-located unit tests
tests/
├── e2e/
│   └── auth.spec.ts       # E2E tests use .spec.ts
```

---

## Test Structure (AAA Pattern)

```typescript
import { describe, it, expect } from 'bun:test';

describe('feature', () => {
  it('should do something', () => {
    // Arrange
    const input = 'test';

    // Act
    const result = functionUnderTest(input);

    // Assert
    expect(result).toBe('expected');
  });
});
```

---

## Coverage Goals

- Unit: 80%+
- Integration: Cover critical paths
- E2E: Critical user journeys only (not 100%)

---

## PAI-Specific Rules

1. **Use `bun test`** - NOT jest, vitest CLI, or npm test
2. **TypeScript required** - All tests in `.test.ts` or `.spec.ts`
3. **CLI tools MUST have tests** - Per CLI-First architecture
4. **No skipped tests in commits** - Remove or fix `.skip()`

---

**For detailed patterns:** Claude knows Vitest/Playwright APIs, mocking, fixtures, async testing, etc. Just ask.
