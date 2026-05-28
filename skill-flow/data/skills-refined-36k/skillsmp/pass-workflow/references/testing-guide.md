# Testing Guide for unmangleJS Passes

## Test Structure

```
tests/
├── passes/
│   └── <pass-name>.test.ts
├── utils/
│   └── <util-name>.test.ts
└── unmangle.ts (test helper)
```

## Basic Test

```typescript
import { describe, it, expect } from "vitest";
import { yourPass } from "../../src/passes";
import { unmangle } from "../unmangle";

describe("your-pass", () => {
  it("should transform pattern", async () => {
    const input = "const x = 1 + 2;";
    const { code } = await unmangle(input, [yourPass]);
    expect(code).toContain("const x = 3;");
  });
});
```

**Test helper features:** debug logging, silent mode, custom passes, fixpoint iteration, no Prettier

## Test Patterns

```typescript
// Basic transformation
it("should fold constants", async () => {
  const { code } = await unmangle("const x = 1 + 2;", [yourPass]);
  expect(code).toContain("const x = 3;");
});

// Multiple variants
describe("binary expressions", () => {
  it("should handle +", async () => {
    const { code } = await unmangle("const x = 1 + 2;", [yourPass]);
    expect(code).toContain("const x = 3;");
  });
  it("should handle -", async () => {
    const { code } = await unmangle("const x = 10 - 5;", [yourPass]);
    expect(code).toContain("const x = 5;");
  });
});

// Edge cases
describe("edge cases", () => {
  it("should handle division by zero", async () => {
    const { code } = await unmangle("const x = 5 / 0;", [yourPass]);
    expect(code).toBeDefined();
  });
  it("should preserve non-constants", async () => {
    const { code } = await unmangle("const x = y + 5;", [yourPass]);
    expect(code).toContain("const x = y + 5;");
  });
});

// Negative cases
it("should not transform function calls", async () => {
  const { code } = await unmangle("const x = Math.random();", [yourPass]);
  expect(code).toContain("Math.random()");
});
```

## Assertion Strategies

```typescript
expect(code).toContain("const x = 3;"); // Containment (preferred)
expect(code).toBe("const x = 3;"); // Exact match (brittle)
expect(code).toMatch(/const x = \d+;/); // Regex pattern
expect(code).toBeDefined(); // Just verify valid
```

## Test Organization

```typescript
describe("my-pass pass", () => {
  describe("binary expressions", () => {
    it("should handle +");
    it("should handle -");
  });

  describe("unary expressions", () => {
    it("should handle !");
    it("should handle -");
  });

  describe("edge cases", () => {
    it("should handle division by zero");
    it("should handle NaN");
  });
});
```

## Vitest Features

```typescript
// Timeout for individual tests
it("slow test", async () => {
  const { code } = await unmangle(largeInput, [yourPass]);
  expect(code).toBeDefined();
}, 4000); // 4 second timeout for this test

// Only/Skip
it.only("run only this", async () => {
  /* ... */
});
it.skip("skip temporarily", async () => {
  /* ... */
});

// Each - test multiple inputs
it.each([
  ["1 + 2", "3"],
  ["5 - 3", "2"],
])("should fold %s to %s", async (input, expected) => {
  const { code } = await unmangle(`const x = ${input};`, [yourPass]);
  expect(code).toContain(`const x = ${expected};`);
});
```

**⚠️ IMPORTANT:** All tests combined must complete within 10 seconds. If total test time exceeds 10 seconds, there may be a bug (possibly infinite loop in test or pass).

## Debugging Tests

```typescript
// Console logging
it("debug example", async () => {
  const input = "const x = 1 + 2;";
  const { code } = await unmangle(input, [yourPass]);
  console.log("Input:", input);
  console.log("Output:", code);
  expect(code).toContain("const x = 3;");
});

// Temporary test scripts (tmp/test-my-pass.ts)
import { unmangle } from "../tests/unmangle";
import { myPass } from "../src/passes";

async function main() {
  const { code } = await unmangle("const x = 1 + 2;", [myPass]);
  console.log("Output:", code);
}
main();

// Run with: npm run ts -- tmp/test-my-pass.ts
```

## Test Coverage

Cover: all operators, all node types, edge cases (null, undefined), type coercion, nesting, special values (NaN, Infinity), negative cases

```typescript
describe("comprehensive", () => {
  it("should handle + - * /");
  it("should handle NaN");
  it("should handle Infinity");
  it("should handle string + number");
  it("should handle division by zero");
  it("should not transform non-constants");
  it("should not transform function calls");
});
```

## Common Mistakes

```typescript
// ❌ WRONG - Missing async/await
it("should transform", () => {
  const { code } = unmangle(input, [pass]); // Missing await
  expect(code).toContain("output");
});

// ✅ CORRECT
it("should transform", async () => {
  const { code } = await unmangle(input, [pass]);
  expect(code).toContain("output");
});

// ❌ WRONG - Brittle exact match
expect(code).toBe("const x=3;");

// ✅ CORRECT - Flexible containment
expect(code).toContain("const x = 3;");
```

## Performance & Integration

```typescript
// Individual test timeout
it("should handle large input", async () => {
  const { code } = await unmangle(largeInput, [yourPass]);
  expect(code).toBeDefined();
}, 4000); // 4 second timeout for this specific test

// Multiple passes
it("should work with other passes", async () => {
  const { code } = await unmangle(input, [pass1, pass2, pass3]);
  expect(code).toBeDefined();
});

// Fixpoint iteration
it("should converge to fixpoint", async () => {
  const { code } = await unmangle(input, [yourPass], { fixpoint: true });
  expect(code).toContain("const x = true;");
});
```

**⚠️ CRITICAL:** All tests combined must run within 10 seconds. Exceeding this indicates a bug (likely infinite loop).

## Running Tests

```bash
npm test                           # All tests
npm test tests/passes/xxx.test.ts  # Single file
npm run test:watch                 # Watch mode
npm test -t "test name"            # Specific test
```

## Best Practices

1. One assertion per test (usually)
2. Descriptive names: "should transform X to Y"
3. Test in isolation
4. Use describe blocks to organize
5. Cover edge cases and negative cases
6. **All tests combined must complete within 10 seconds** (exceeding indicates a bug/infinite loop)
7. Use `it.only` for development, remove before committing
