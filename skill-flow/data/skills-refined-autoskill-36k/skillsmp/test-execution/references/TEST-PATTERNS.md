# Test Patterns Reference

Common testing patterns and best practices.

## Test Structure (AAA Pattern)

```javascript
describe('Calculator', () => {
  it('should add two numbers', () => {
    // Arrange
    const calculator = new Calculator();

    // Act
    const result = calculator.add(2, 3);

    // Assert
    expect(result).toBe(5);
  });
});
```

## Unit Test Patterns

### Testing Pure Functions

```javascript
describe('formatDate', () => {
  it('should format date as YYYY-MM-DD', () => {
    const date = new Date('2024-03-15');
    expect(formatDate(date)).toBe('2024-03-15');
  });

  it('should handle invalid date', () => {
    expect(formatDate(null)).toBe('Invalid Date');
  });
});
```

### Testing with Mocks

```javascript
describe('UserService', () => {
  it('should fetch user by ID', async () => {
    // Mock the API
    const mockApi = {
      get: vi.fn().mockResolvedValue({ id: 1, name: 'John' })
    };

    const service = new UserService(mockApi);
    const user = await service.getUser(1);

    expect(mockApi.get).toHaveBeenCalledWith('/users/1');
    expect(user.name).toBe('John');
  });
});
```

### Testing Async Code

```javascript
describe('AsyncOperations', () => {
  // Using async/await
  it('should resolve with data', async () => {
    const data = await fetchData();
    expect(data).toBeDefined();
  });

  // Testing rejection
  it('should reject on error', async () => {
    await expect(fetchInvalidData()).rejects.toThrow('Not found');
  });
});
```

### Testing Error Handling

```javascript
describe('ErrorHandling', () => {
  it('should throw on invalid input', () => {
    expect(() => validateEmail('')).toThrow('Email required');
  });

  it('should not throw on valid input', () => {
    expect(() => validateEmail('test@example.com')).not.toThrow();
  });
});
```

## Integration Test Patterns

### Database Integration

```javascript
describe('UserRepository', () => {
  let db;

  beforeAll(async () => {
    db = await createTestDatabase();
  });

  afterAll(async () => {
    await db.close();
  });

  beforeEach(async () => {
    await db.clear();
  });

  it('should save and retrieve user', async () => {
    const repo = new UserRepository(db);

    await repo.save({ name: 'John', email: 'john@test.com' });
    const user = await repo.findByEmail('john@test.com');

    expect(user.name).toBe('John');
  });
});
```

### API Integration

```javascript
describe('API Integration', () => {
  let server;

  beforeAll(() => {
    server = createTestServer();
  });

  afterAll(() => {
    server.close();
  });

  it('should return 200 for valid request', async () => {
    const response = await fetch(`${server.url}/api/health`);
    expect(response.status).toBe(200);
  });
});
```

## Test Doubles

| Type | Purpose | Example |
|------|---------|---------|
| **Stub** | Returns predefined values | `getUser: () => ({ id: 1 })` |
| **Mock** | Verifies interactions | `expect(mock).toHaveBeenCalled()` |
| **Spy** | Wraps real implementation | `vi.spyOn(obj, 'method')` |
| **Fake** | Simplified implementation | In-memory database |

## Common Assertions

```javascript
// Equality
expect(value).toBe(expected);           // Strict equality
expect(value).toEqual(expected);        // Deep equality

// Truthiness
expect(value).toBeTruthy();
expect(value).toBeFalsy();
expect(value).toBeNull();
expect(value).toBeDefined();

// Numbers
expect(value).toBeGreaterThan(3);
expect(value).toBeLessThanOrEqual(10);
expect(value).toBeCloseTo(0.3, 5);

// Strings
expect(value).toMatch(/pattern/);
expect(value).toContain('substring');

// Arrays
expect(array).toContain(item);
expect(array).toHaveLength(3);

// Objects
expect(object).toHaveProperty('key');
expect(object).toMatchObject({ a: 1 });

// Exceptions
expect(() => fn()).toThrow();
expect(() => fn()).toThrow('message');
```

## Test Organization

```
tests/
├── unit/
│   ├── services/
│   │   └── user.service.test.ts
│   └── utils/
│       └── format.test.ts
├── integration/
│   ├── api/
│   │   └── users.api.test.ts
│   └── db/
│       └── user.repo.test.ts
└── e2e/
    └── user-flow.test.ts
```

## Naming Conventions

```javascript
// File naming
user.service.test.ts    // Unit test
users.api.test.ts       // Integration test
login.e2e.test.ts       // E2E test

// Test naming
it('should [action] when [condition]')
it('should return null when user not found')
it('should throw error when email is invalid')
```
