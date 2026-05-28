---
name: testing-strategies
description: Build comprehensive test suites using the testing pyramid, TDD/BDD methodologies, proper mocking strategies, and effective test coverage. Write tests that catch bugs and survive refactoring.
---

# Testing Strategies

Complete framework for building effective, maintainable test suites that give you confidence to ship.

## When to Use

- Setting up testing for new projects
- Improving existing test coverage
- Practicing Test-Driven Development (TDD)
- Debugging flaky tests
- Deciding what to test (and what not to)
- Organizing test files and structure

## Core Testing Principles

**Test Behavior, Not Implementation:**
- Test what the code does, not how
- Tests should survive refactoring
- Focus on public interfaces

**Testing Pyramid:**
```
         /\
        /  \         E2E (Few, slow, comprehensive)
       /----\
      /      \       Integration (Some, medium)
     /--------\
    /          \     Unit (Many, fast, isolated)
   /------------\
```

**Write Tests That Fail Usefully:**
- Clear error messages
- Pinpoint failure location
- Show expected vs actual

---

## Workflow

### Step 1: Choose the Right Test Level

**Unit Tests (70% of tests):**
```
WHEN TO USE:
- Business logic
- Data transformations
- Validation rules
- Pure functions
- Edge cases

CHARACTERISTICS:
- Fast (<100ms each)
- Isolated (no external dependencies)
- Many tests
- Run on every commit
```

**Integration Tests (20% of tests):**
```
WHEN TO USE:
- API endpoints
- Database operations
- External service integration
- Multiple components working together

CHARACTERISTICS:
- Medium speed (100ms-1s each)
- Real dependencies (test DB, APIs)
- Fewer than unit tests
- Run before merge
```

**E2E Tests (10% of tests):**
```
WHEN TO USE:
- Critical user journeys
- Complete workflows
- Cross-browser compatibility

CHARACTERISTICS:
- Slow (seconds per test)
- Full application stack
- Fewest tests
- Run before release
```

### Step 2: Write Unit Tests (AAA Pattern)

**Arrange-Act-Assert:**
```javascript
describe('UserService', () => {
  describe('createUser', () => {
    it('creates a user with valid data', async () => {
      // ARRANGE: Set up test data and dependencies
      const userData = {
        email: 'test@example.com',
        name: 'Test User'
      };
      const mockRepo = {
        save: jest.fn().mockResolvedValue({ id: '1', ...userData })
      };
      const service = new UserService(mockRepo);

      // ACT: Execute the code under test
      const result = await service.createUser(userData);

      // ASSERT: Verify the outcome
      expect(result).toEqual({ id: '1', ...userData });
      expect(mockRepo.save).toHaveBeenCalledWith(userData);
    });

    it('throws validation error for invalid email', async () => {
      // ARRANGE
      const userData = { email: 'invalid', name: 'Test' };
      const service = new UserService(mockRepo);

      // ACT & ASSERT
      await expect(service.createUser(userData))
        .rejects.toThrow('Invalid email format');
    });
  });
});
```

**What to Unit Test:**
```markdown
✅ DO TEST:
- Business logic
- Data transformations
- Validation rules
- Edge cases (null, empty, max values)
- Error conditions
- Pure functions

❌ DON'T TEST:
- Third-party libraries
- Simple getters/setters
- Framework code
- Configuration
- Trivial code
```

**Mocking Guidelines:**
```javascript
// ✅ GOOD: Mock external dependencies
const mockEmailService = {
  send: jest.fn().mockResolvedValue(true)
};

const mockDatabase = {
  query: jest.fn().mockResolvedValue([{ id: 1 }])
};

// ✅ GOOD: Use dependency injection
class UserService {
  constructor(private db: Database, private email: EmailService) {}

  async createUser(data) {
    const user = await this.db.save(data);
    await this.email.send(user.email, 'Welcome!');
    return user;
  }
}

// In test:
const service = new UserService(mockDb, mockEmail);

// ❌ BAD: Mocking internal implementation details
// This couples tests to implementation
```

### Step 3: Write Integration Tests

**API Integration Tests:**
```javascript
describe('POST /api/users', () => {
  let db: Database;

  beforeAll(async () => {
    db = await createTestDatabase();
  });

  afterAll(async () => {
    await db.close();
  });

  beforeEach(async () => {
    await db.query('DELETE FROM users');
  });

  it('creates a user and returns 201', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'test@example.com', name: 'Test' })
      .expect(201);

    expect(response.body).toMatchObject({
      id: expect.any(String),
      email: 'test@example.com'
    });

    // Verify in database
    const user = await db.users.findOne({ email: 'test@example.com' });
    expect(user).toBeDefined();
  });

  it('returns 400 for invalid data', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'invalid' })
      .expect(400);

    expect(response.body.error).toBe('Invalid email format');
  });

  it('returns 409 for duplicate email', async () => {
    await createUser({ email: 'test@example.com' });

    await request(app)
      .post('/api/users')
      .send({ email: 'test@example.com', name: 'Test' })
      .expect(409);
  });
});
```

### Step 4: Write E2E Tests (Page Object Pattern)

**Page Object:**
```javascript
// pages/LoginPage.ts
class LoginPage {
  constructor(private page: Page) {}

  async navigate() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.page.fill('[data-testid="email"]', email);
    await this.page.fill('[data-testid="password"]', password);
    await this.page.click('[data-testid="submit"]');
  }

  async getErrorMessage() {
    return this.page.textContent('[data-testid="error"]');
  }
}

// tests/login.spec.ts
describe('Login', () => {
  it('logs in successfully with valid credentials', async () => {
    const loginPage = new LoginPage(page);
    await loginPage.navigate();
    await loginPage.login('user@example.com', 'password');

    await expect(page).toHaveURL('/dashboard');
  });

  it('shows error for invalid credentials', async () => {
    const loginPage = new LoginPage(page);
    await loginPage.navigate();
    await loginPage.login('user@example.com', 'wrong');

    const error = await loginPage.getErrorMessage();
    expect(error).toBe('Invalid credentials');
  });
});
```

**E2E Best Practices:**
```markdown
✅ DO:
- Use data-testid attributes
- Test user journeys, not features
- Run in realistic environment
- Handle async properly
- Clean up test data

❌ DON'T:
- Test every edge case with E2E
- Use brittle selectors (.class-name-xyz)
- Share state between tests
- Skip cleanup
- Run E2E on every commit (too slow)
```

### Step 5: Test-Driven Development (TDD)

**Red-Green-Refactor Cycle:**

```
1. RED: Write a failing test
   └── Test describes desired behavior

2. GREEN: Write minimal code to pass
   └── Just enough to make test pass

3. REFACTOR: Clean up
   └── Improve code while tests pass
```

**TDD Example:**
```javascript
// Step 1: RED - Write failing test
describe('Cart', () => {
  it('calculates total price with discount', () => {
    const cart = new Cart();
    cart.addItem({ price: 100, quantity: 2 });
    cart.applyDiscount(10); // 10%

    expect(cart.total).toBe(180); // (100 * 2) - 10%
  });
});

// Run test: FAILS (Cart doesn't exist yet)

// Step 2: GREEN - Minimal implementation
class Cart {
  items = [];
  discount = 0;

  addItem(item) {
    this.items.push(item);
  }

  applyDiscount(percent) {
    this.discount = percent;
  }

  get total() {
    const subtotal = this.items.reduce(
      (sum, i) => sum + i.price * i.quantity,
      0
    );
    return subtotal * (1 - this.discount / 100);
  }
}

// Run test: PASSES

// Step 3: REFACTOR - Clean up
class Cart {
  private items: CartItem[] = [];
  private discountPercent: number = 0;

  addItem(item: CartItem): void {
    this.items.push(item);
  }

  applyDiscount(percent: number): void {
    this.discountPercent = percent;
  }

  get total(): number {
    const subtotal = this.calculateSubtotal();
    return this.applyDiscountToSubtotal(subtotal);
  }

  private calculateSubtotal(): number {
    return this.items.reduce(
      (sum, item) => sum + item.price * item.quantity,
      0
    );
  }

  private applyDiscountToSubtotal(subtotal: number): number {
    return subtotal * (1 - this.discountPercent / 100);
  }
}

// Run test: STILL PASSES (refactoring didn't break anything)
```

### Step 6: Test Coverage

**Coverage Metrics:**
```
LINE COVERAGE: % of lines executed
├── Easy to game
├── Doesn't ensure quality

BRANCH COVERAGE: % of decision branches
├── Better than line coverage
├── Catches missing else cases

MUTATION TESTING: % of mutations caught
├── Introduces bugs, checks if tests catch them
├── High quality metric
├── Slow to run
```

**Coverage Guidelines:**
```markdown
## Coverage Targets

| Type | Target | Priority |
|------|--------|----------|
| Unit | 80% | Business logic |
| Integration | 60% | API endpoints |
| E2E | Key flows | User journeys |

### What Must Be Tested
- [ ] All public API functions
- [ ] All error handling paths
- [ ] Business rule edge cases
- [ ] Security-sensitive code

### What Can Be Skipped
- Configuration files
- Generated code
- Simple getters/setters
- Third-party wrappers
```

---

## Test Organization

**File Structure:**
```
src/
├── users/
│   ├── user.service.ts
│   ├── user.service.test.ts       # Unit tests
│   ├── user.repository.ts
│   └── user.repository.test.ts
├── __tests__/
│   └── integration/
│       └── user.api.test.ts       # Integration tests
tests/
├── e2e/
│   ├── login.spec.ts              # E2E tests
│   └── checkout.spec.ts
├── fixtures/
│   └── users.json                 # Test data
└── setup.ts                       # Test configuration
```

**Naming Conventions:**
```javascript
// Describe the unit being tested
describe('UserService', () => {
  // Describe the method
  describe('createUser', () => {
    // Describe the scenario
    describe('when email is valid', () => {
      // State what it does
      it('creates a new user', () => {});
      it('sends welcome email', () => {});
    });

    describe('when email already exists', () => {
      it('throws DuplicateEmailError', () => {});
    });
  });
});
```

---

## Test Quality Checklist

```markdown
## Test Review Checklist

### Structure
- [ ] Tests follow AAA pattern
- [ ] One assertion concept per test
- [ ] Descriptive test names
- [ ] Tests are independent
- [ ] No test interdependence

### Coverage
- [ ] Happy path tested
- [ ] Error cases tested
- [ ] Edge cases tested
- [ ] Boundary conditions tested

### Maintainability
- [ ] No flaky tests
- [ ] Setup/teardown is minimal
- [ ] Mocks are at boundaries
- [ ] Tests survive refactoring

### Performance
- [ ] Unit tests <100ms each
- [ ] Integration tests reasonable
- [ ] E2E tests focused
- [ ] Parallelization enabled
```

---

## Common Testing Mistakes

| Don't | Do |
|-------|-----|
| Test implementation details | Test public behavior |
| One assertion per test (too rigid) | One concept per test |
| Copy-paste tests | Use test helpers/factories |
| Share state between tests | Isolate each test |
| Skip edge cases | Test boundaries and errors |
| Mock everything | Mock at boundaries only |
| Ignore flaky tests | Fix or delete flaky tests |
| Write tests after code (always) | Use TDD when beneficial |

---

## Tools & Frameworks

**JavaScript/TypeScript:**
- Jest (unit + integration)
- Vitest (fast Jest alternative)
- Playwright (E2E)
- Cypress (E2E)
- Testing Library (React/Vue/etc)

**Python:**
- pytest (unit + integration)
- unittest (standard library)
- Selenium (E2E)

**Ruby:**
- RSpec (unit + integration)
- Capybara (E2E)

**Go:**
- testing package (standard library)
- testify (assertions)

---

## Related Skills

- `/code-review` - Reviewing test quality
- `/devops-cicd` - Running tests in CI/CD
- `/debugging` - Using tests to find bugs

---

**Last Updated**: 2026-01-22
