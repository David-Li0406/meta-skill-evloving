# Jest (JavaScript/TypeScript)

Use for JS/TS projects using Jest (examples shown in JavaScript). Load when targeting Jest. Keep async tests with `async/await`, prefer explicit expectations, and use JSDoc-style doc comments for helper utilities.

```typescript
/** Builds sample input */
const makeInput = () => ({ /* ... */ });

/** Example Jest tests (JavaScript) */
describe('[ModuleName]', () => {
  beforeEach(() => {
  });

  afterEach(() => {
  });

  describe('[functionName]', () => {
    it('returns expected result for valid input', () => {
      const input = makeInput();
      const result = functionUnderTest(input);
      expect(result).toEqual(expectedOutput);
    });

    it('returns default value for empty input', () => {
      expect(functionUnderTest([])).toEqual(defaultValue);
    });

    it('throws for invalid input', () => {
      expect(() => functionUnderTest(invalidInput)).toThrow(ExpectedError);
    });
  });
});
```
