# Vitest (JavaScript/TypeScript)

Use for JS/TS projects using Vitest. Load when targeting Vitest. Keep async tests with `async/await`, prefer explicit expectations, and use JSDoc-style doc comments for helper utilities.

```typescript
/** Example Vitest tests */
import { describe, it, expect, beforeEach, afterEach } from 'vitest';

describe('[ModuleName]', () => {
  beforeEach(() => {
  });

  afterEach(() => {
  });

  describe('[functionName]', () => {
    it('returns expected result for valid input', async () => {
      const input: InputType = /* test data */;
      const result: OutputType = await functionUnderTest(input);
      expect(result).toEqual(expectedOutput);
    });

    it('returns default value for empty input', () => {
      expect(functionUnderTest([] as InputType[])).toEqual(defaultValue);
    });

    it('throws for invalid input', () => {
      expect(() => functionUnderTest(invalidInput as InputType)).toThrow(ExpectedError);
    });
  });
});
```
