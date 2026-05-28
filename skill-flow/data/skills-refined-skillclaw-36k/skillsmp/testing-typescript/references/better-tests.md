# Better Tests

Testing best practices for TypeScript/JavaScript frameworks like Jest, Vitest, and Bun, adapted from [betterspecs.org](https://www.betterspecs.org/).

## Keep Descriptions Short

When testing classes, use `.` for static methods and `#` for instance methods. For standalone functions, use the function name. When testing multiple functions, use top-level describe blocks for each function.

```typescript
// Bad
describe("the authenticate method for User");
describe("if the user is an admin");

// Good (class methods)
describe("User", () => {
  describe(".authenticate");
  describe("#isAdmin");
});

// Good (standalone functions)
describe("calculateTax");
describe("formatCurrency");
```

## Use Contexts (With `describe`)

Use contexts to organize related tests. Start context descriptions with 'when', 'with', or 'without'. JavaScript frameworks lack a dedicated `context` function, so use `describe` for contexts instead.

```typescript
// Bad
it("has 200 status code if logged in", () => {
  expect(response.status).toEqual(200);
});

it("has 401 status code if not logged in", () => {
  expect(response.status).toEqual(401);
});

// Good
describe("when logged in", () => {
  it("returns a 200 status code", () => {
    expect(response.status).toEqual(200);
  });
});

describe("when logged out", () => {
  it("returns a 401 status code", () => {
    expect(response.status).toEqual(401);
  });
});
```

## Keep `it` Descriptions Short

```typescript
// Bad
it("has 422 status code if an unexpected params will be added", () => {
  expect(response.status).toEqual(422);
});

// Good
describe("when the parameters are invalid", () => {
  it("responds with a 422 status code", () => {
    expect(response.status).toEqual(422);
  });
});
```

## Single Expectations

Prefer one assertion per test. Multiple assertions are acceptable when test setup is expensive, such as in integration tests.

```typescript
// Good (isolated)
it("returns a JSON content type", () => {
  expect(response.headers["content-type"]).toContain("application/json");
});

it("assigns the resource", () => {
  expect(response.data.resource).toBeDefined();
});

// Good (not isolated)
it("creates a resource", () => {
  expect(response.headers["content-type"]).toContain("application/json");
  expect(response.data.resource).toBeDefined();
});
```

## Test All Cases

Test valid, edge, and invalid cases, not just the happy path.

```typescript
// Bad
it("shows the resource");

// Good
describe("#delete", () => {
  describe("when resource is found", () => {
    it("responds with a 200 status");
    it("shows the resource");
  });

  describe("when the resource is not found", () => {
    it("responds with a 404 status");
  });

  describe("when the resource is not owned", () => {
    it("responds with a 404 status");
  });
});
```

## Mocks

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

## Minimal Data

Create only the test data you need. When creating lists of undifferentiated records, 3 is usually the right number.

## Factories

Use factory functions instead of inline object creation. Avoid complex data setup when possible.

```typescript
// Bad
const user = { id: 1, name: "John", email: "john@example.com", ... };

// Good
const user = userFactory.build({ name: "John" });

// Good (for database persistence)
const user = await userFactory.create({ name: "John" });
```

## Avoid "should"

Avoid "should" in test descriptions. Use present tense, third person.

```typescript
// Bad
it("should not update the user's email", () => {
  expect(user.email).toEqual(originalEmail);
});

// Good
it("does not update the user's email", () => {
  expect(user.email).toEqual(originalEmail);
});
```
