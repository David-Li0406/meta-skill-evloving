# TDD Workflow with Claude Code

Complete patterns for test-driven development using Claude Code as your pair programming partner.

## The TDD Cycle

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                      │
│    ┌─────────┐      ┌─────────┐      ┌──────────┐                   │
│    │   RED   │ ───► │  GREEN  │ ───► │ REFACTOR │ ──┐               │
│    │  Write  │      │  Make   │      │ Improve  │   │               │
│    │  Test   │      │  Pass   │      │  Code    │   │               │
│    └─────────┘      └─────────┘      └──────────┘   │               │
│         ▲                                           │               │
│         └───────────────────────────────────────────┘               │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Workflow: Feature Development with TDD

### Phase 1: Red (Write Failing Test)

**You drive this phase.** Describe what you want to build.

#### Prompt Template

```
Write a failing test for a function called [name] that:

Purpose: [what it does]

Inputs:
- param1: [type] - [description]
- param2: [type] - [description]

Outputs:
- Returns [type] when [condition]
- Returns [type] when [other condition]

Errors:
- Throws [ErrorType] when [condition]
- Throws [ErrorType] when [other condition]

Use [Jest/Vitest/pytest] with [TypeScript/JavaScript/Python].
Do NOT implement the function yet.
```

#### Example: Email Validator

```
Write a failing test for a function called validateEmail that:

Purpose: Validate email addresses according to RFC 5322

Inputs:
- email: string - the email address to validate

Outputs:
- Returns true for valid email addresses
- Returns false for invalid email addresses

Test cases to include:
- Valid: user@domain.com, user.name@domain.co.uk
- Invalid: missing @, missing domain, special characters
- Edge cases: empty string, null/undefined

Use Vitest with TypeScript.
Do NOT implement the function yet.
```

#### Claude's Response (Example)

```typescript
import { describe, it, expect } from 'vitest';
import { validateEmail } from './email';

describe('validateEmail', () => {
  describe('valid emails', () => {
    it('should return true for simple email', () => {
      expect(validateEmail('user@domain.com')).toBe(true);
    });

    it('should return true for email with subdomain', () => {
      expect(validateEmail('user@mail.domain.com')).toBe(true);
    });

    it('should return true for email with dots in local part', () => {
      expect(validateEmail('user.name@domain.com')).toBe(true);
    });

    it('should return true for email with plus sign', () => {
      expect(validateEmail('user+tag@domain.com')).toBe(true);
    });
  });

  describe('invalid emails', () => {
    it('should return false for email without @', () => {
      expect(validateEmail('userdomain.com')).toBe(false);
    });

    it('should return false for email without domain', () => {
      expect(validateEmail('user@')).toBe(false);
    });

    it('should return false for email without local part', () => {
      expect(validateEmail('@domain.com')).toBe(false);
    });

    it('should return false for email with spaces', () => {
      expect(validateEmail('user @domain.com')).toBe(false);
    });
  });

  describe('edge cases', () => {
    it('should return false for empty string', () => {
      expect(validateEmail('')).toBe(false);
    });

    it('should handle null gracefully', () => {
      expect(validateEmail(null as unknown as string)).toBe(false);
    });

    it('should handle undefined gracefully', () => {
      expect(validateEmail(undefined as unknown as string)).toBe(false);
    });
  });
});
```

### Phase 2: Green (Make Test Pass)

**Claude implements.** Ask for minimum code to pass tests.

#### Prompt Template

```
Now implement the minimum code to make these tests pass.
Keep it simple - no premature optimization.
```

#### Claude's Response (Example)

```typescript
export function validateEmail(email: string): boolean {
  if (!email || typeof email !== 'string') {
    return false;
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}
```

### Phase 3: Refactor (Improve Code)

**Collaborative phase.** Both review and improve.

#### Prompt Template

```
Review this implementation for:
1. Code quality and readability
2. Performance considerations
3. Edge cases we might have missed
4. Better approaches

Suggest refactoring if needed, keeping all tests passing.
```

#### Refactoring Considerations

```
Consider refactoring:
- Extract magic values to constants
- Add JSDoc documentation
- Improve error messages
- Handle additional edge cases
- Optimize regex if needed
```

## TDD Patterns by Scenario

### Pattern: Building a Service

```
I'm building a UserService that needs to:
1. Create users (with validation)
2. Find users by ID
3. Update user profiles
4. Delete users (soft delete)

Let's use TDD. Start with the create method.

Write failing tests for UserService.create that:
- Accepts { email, name, password }
- Validates email format
- Hashes password before storing
- Returns created user without password
- Throws ValidationError for invalid input
- Throws ConflictError for duplicate email

Use Vitest with TypeScript.
Mock the database calls.
```

### Pattern: Building an API Endpoint

```
I'm building a REST API endpoint POST /api/users.

Write failing tests that verify:
- Returns 201 with user data on success
- Returns 400 with validation errors for bad input
- Returns 409 for duplicate email
- Returns 500 for database errors
- Sets correct content-type header
- Does not expose password in response

Use supertest with Jest.
```

### Pattern: Building a React Component

```
I'm building a LoginForm component that:
- Has email and password inputs
- Has a submit button
- Shows validation errors inline
- Disables button during submission
- Calls onSubmit with credentials on success
- Shows error message on failure

Write failing tests using React Testing Library.
Test user interactions, not implementation.
```

### Pattern: Building a CLI Tool

```
I'm building a CLI command 'process-files' that:
- Accepts --input and --output flags
- Processes all .txt files in input dir
- Writes results to output dir
- Shows progress bar
- Exits with code 0 on success
- Exits with code 1 on error

Write failing tests for the CLI behavior.
Mock filesystem operations.
```

## TDD Best Practices

### Write Meaningful Test Names

```typescript
// Good - describes behavior
it('should throw ValidationError when email format is invalid', ...)

// Avoid - describes implementation
it('should call regex.test', ...)
```

### One Assertion Per Behavior

```typescript
// Good - focused tests
it('should return user id', () => {
  const result = createUser(data);
  expect(result.id).toBeDefined();
});

it('should hash password', () => {
  const result = createUser(data);
  expect(result.password).not.toBe(data.password);
});

// Avoid - multiple behaviors
it('should create user correctly', () => {
  const result = createUser(data);
  expect(result.id).toBeDefined();
  expect(result.password).not.toBe(data.password);
  expect(result.createdAt).toBeDefined();
  // ... more assertions
});
```

### Test Behavior, Not Implementation

```typescript
// Good - tests outcome
it('should store user in database', async () => {
  await userService.create(data);
  const user = await db.users.findByEmail(data.email);
  expect(user).toBeDefined();
});

// Avoid - tests internals
it('should call db.users.insert once', async () => {
  await userService.create(data);
  expect(db.users.insert).toHaveBeenCalledTimes(1);
});
```

### Arrange-Act-Assert Pattern

```typescript
it('should update user name', async () => {
  // Arrange
  const user = await createTestUser();
  const newName = 'Updated Name';

  // Act
  await userService.update(user.id, { name: newName });

  // Assert
  const updated = await userService.findById(user.id);
  expect(updated.name).toBe(newName);
});
```

## Prompts for TDD Phases

### Starting a Feature

```
I want to build [feature description].

Let's use TDD. First, help me identify:
1. What are the main behaviors to test?
2. What edge cases should we consider?
3. What errors should we handle?

Then write the first failing test.
```

### When Test Passes

```
The test passes. Let's check:
1. Is the implementation as simple as possible?
2. Did we hardcode anything that should be dynamic?
3. Should we add more test cases?

If the code is good, move to the next behavior.
```

### Adding a Test Case

```
Add a test case for [scenario].
The test should verify [expected behavior].
Run the test to confirm it fails for the right reason.
```

### Refactoring Phase

```
All tests pass. Let's refactor:
1. Extract [repeated code] into [function/constant]
2. Rename [unclear name] to [clearer name]
3. Add documentation for public API
4. Review error messages for clarity

Keep all tests passing.
```

## Handling Complex Features

### Break Down Large Features

```
The feature is too large for one TDD cycle.
Break it into smaller, testable units:

1. [First unit] - basic functionality
2. [Second unit] - error handling
3. [Third unit] - edge cases
4. [Fourth unit] - integration

Start TDD with [first unit].
```

### Incremental Complexity

```
Start with the simplest case:
1. Happy path only
2. Add validation
3. Add error handling
4. Add edge cases
5. Add performance optimizations

Each step should have failing tests first.
```

## TDD Workflow Checklist

### Before Writing Tests

- [ ] Feature requirements are clear
- [ ] Test framework is set up
- [ ] Dependencies are mocked as needed
- [ ] Test file is created

### During Red Phase

- [ ] Test describes desired behavior
- [ ] Test name is descriptive
- [ ] Test uses Arrange-Act-Assert
- [ ] Test runs and fails

### During Green Phase

- [ ] Implementation is minimal
- [ ] No premature optimization
- [ ] All tests pass
- [ ] No new test failures

### During Refactor Phase

- [ ] Code is readable
- [ ] No duplication
- [ ] Names are clear
- [ ] Documentation added
- [ ] All tests still pass

## Common TDD Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Writing too many tests at once | Overwhelming, hard to focus | One test at a time |
| Implementing before test fails | Defeats TDD purpose | Always see red first |
| Testing implementation details | Brittle tests | Test behavior only |
| Skipping refactor phase | Technical debt | Allocate refactor time |
| Making tests pass with hacks | False confidence | Clean implementation |
| Not running tests frequently | Late feedback | Run after every change |
