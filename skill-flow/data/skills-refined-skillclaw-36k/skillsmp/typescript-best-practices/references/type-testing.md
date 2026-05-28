# Type Testing

Use `*.test-d.ts` files for type-level tests:

```typescript
// myGeneric.test-d.ts
import type { MyGenericType } from './MyGenericType';

const anyObj: any = {};

// Test 1: Extracts correct keys with basic types
(() => {
  type Input = {
    key1: string;
    key2: number;
    other: boolean;
  };
  type Expected = {
    key1: string;
    key2: number;
  };
  type Result = MyGenericType<Input, 'key1' | 'key2'>;

  // Bidirectional satisfies ensures strict equality
  (anyObj as Result satisfies Expected);
  (anyObj as Expected satisfies Result);
})();

// Test 2: Preserves optional modifiers
(() => {
  type Input = {
    required: string;
    optional?: number;
  };
  type Expected = {
    required: string;
    optional?: number;
  };
  type Result = MyGenericType<Input>;

  (anyObj as Result satisfies Expected);
  (anyObj as Expected satisfies Result);
})();

// Test 3: Handles nested objects
(() => {
  type Expected = {
    user: { id: string; name: string };
  };
  type Result = MyGenericType<typeof anyObj, 'user'>;

  (anyObj as Result satisfies Expected);
  (anyObj as Expected satisfies Result);
})();

// Test 4: Handles union types in values
(() => {
  type Expected = {
    status: 'active' | 'inactive';
  };
  type Result = MyGenericType<typeof anyObj, 'status'>;

  (anyObj as Result satisfies Expected);
  (anyObj as Expected satisfies Result);
})();

// Test 5: Empty keys returns empty object
(() => {
  type Expected = Record<string, never>;
  type Result = MyGenericType<typeof anyObj, never>;

  (anyObj as Result satisfies Expected);
  (anyObj as Expected satisfies Result);
})();

// Add more test cases as needed to cover edge cases
```

## Testing Negative Cases

When a type is designed to **reject** certain inputs, test those rejections explicitly using `@ts-expect-error`:

```typescript
// navigate.test-d.ts
import { navigate } from './navigate';

// Test: Valid paths work
navigate('/home');
navigate('/about');

// Test: Invalid paths should cause type errors
// @ts-expect-error invalid path should cause a type error
navigate('/path/not/exist');

// @ts-expect-error numbers are not valid paths
navigate(123);

// @ts-expect-error empty string is not a valid path
navigate('');
```

If the `@ts-expect-error` line does NOT produce an error, TypeScript will report an "Unused '@ts-expect-error' directive" error — this catches regressions where invalid inputs accidentally become valid.

## Best Practices

1. **Use IIFE for test isolation** — Each test case in its own `(() => { ... })()` block prevents type leakage
2. **Bidirectional satisfies** — Test both `Result satisfies Expected` AND `Expected satisfies Result` for strict equality
3. **Test edge cases** — Empty inputs, union types, optional properties, nested objects
4. **Test negative cases** — Use `@ts-expect-error` to verify type rejections
5. **Descriptive comments** — Name each test case clearly

Write as many test cases as needed to thoroughly verify the generic type behavior. Each IIFE isolates the test scope and makes failures easy to locate.
