# Personal Preferences

Personal preferences for writing tests that complement the Better Tests guidelines.

## Use `it` Instead of `test`

Use `it` instead of `test` for individual test cases.

```typescript
// Bad
test("returns a 200 status code", () => {
  expect(response.status).toBe(200);
});

// Good
it("returns a 200 status code", () => {
  expect(response.status).toBe(200);
});
```

## Articles and Linking Verbs

Use proper articles ('a', 'an', 'the') and linking verbs ('is', 'are', 'has', 'does') in test descriptions. When testing a subject directly, start descriptions with linking verbs like "is", "are", "has", or "does".

```typescript
// Bad (missing articles)
describe("when template includes partial");
describe("when URI is preceded by @");

// Good (includes articles)
describe("when the template includes a partial");
describe("when the URI is preceded by an @");

// Bad (missing linking verbs for direct subject testing)
it("valid");
it("not saved");

// Good (starts with linking verbs)
it("is valid");
it("is not saved");
```

## When to Mock

Use mocks sparingly, typically only when simulating external APIs or when calling something would have a side effect that can't be easily reverted in a test context. Test real behavior when possible.

```typescript
// Good (mocking external API)
beforeEach(() => {
  jest.spyOn(weatherService, "getCurrentTemperature").mockResolvedValue(72);
});

// Good (mocking side effects)
beforeEach(() => {
  jest.spyOn(fs, "unlinkSync").mockImplementation(() => {});
});
```

## Test Data Guidelines

When creating lists of undifferentiated records, 3 is usually the right number.

## Context Setup

Put test setup in `beforeEach` blocks within the context, not inside individual tests. This keeps tests focused and makes adding new tests to the context simpler.

```typescript
// Bad
describe("when a package.json exists in the directory", () => {
  it("returns true", async () => {
    await writeFile(join(tempDirectory, "package.json"), "{}");

    expect(await isJavaScriptProject()).toBe(true);
  });
});

// Good
describe("when a package.json exists in the directory", () => {
  beforeEach(async () => {
    await writeFile(join(tempDirectory, "package.json"), "{}");
  });

  it("returns true", async () => {
    expect(await isJavaScriptProject()).toBe(true);
  });
});
```
