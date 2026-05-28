# Testing Automation

## Patterns


---
  #### **Name**
Testing Pyramid Structure
  #### **Description**
Balanced test distribution for speed and confidence
  #### **When**
Setting up testing strategy for any project
  #### **Example**
    # Testing Pyramid Distribution
    #
    #         /\
    #        /  \     E2E Tests (5-10%)
    #       /----\    - Critical user journeys only
    #      /      \   - Login, checkout, core flows
    #     /--------\  Integration Tests (20-30%)
    #    /          \ - API endpoints
    #   /------------\- Database operations
    #  /              \- Service interactions
    # /----------------\ Unit Tests (60-70%)
    #                   - Business logic
    #                   - Utilities, helpers
    #                   - Pure functions
    
    # Example test counts for 1000 total tests:
    # - Unit tests: 650
    # - Integration tests: 280
    # - E2E tests: 70
    
    # Benefits:
    # - Fast feedback (unit tests run in seconds)
    # - High confidence (integration catches real bugs)
    # - Stable CI (fewer flaky e2e tests)
    

---
  #### **Name**
Unit Test Best Practices
  #### **Description**
Fast, isolated tests for business logic
  #### **When**
Testing pure functions, business logic, utilities
  #### **Example**
    // Jest/Vitest example
    
    // Good: Test behavior, not implementation
    describe('calculateDiscount', () => {
      it('applies 10% discount for orders over $100', () => {
        const order = { total: 150 };
        expect(calculateDiscount(order)).toBe(15);
      });
    
      it('applies no discount for orders under $100', () => {
        const order = { total: 50 };
        expect(calculateDiscount(order)).toBe(0);
      });
    
      it('applies maximum discount cap of $50', () => {
        const order = { total: 1000 };
        expect(calculateDiscount(order)).toBe(50);
      });
    });
    
    // Good: Arrange-Act-Assert pattern
    describe('UserService', () => {
      it('creates user with hashed password', async () => {
        // Arrange
        const userData = { email: 'test@example.com', password: 'secret' };
        const mockHasher = { hash: jest.fn().mockResolvedValue('hashed') };
        const service = new UserService(mockHasher);
    
        // Act
        const user = await service.create(userData);
    
        // Assert
        expect(user.password).toBe('hashed');
        expect(mockHasher.hash).toHaveBeenCalledWith('secret');
      });
    });
    
    // Good: Descriptive test names
    it('throws ValidationError when email format is invalid', () => {
      expect(() => validateEmail('not-an-email')).toThrow(ValidationError);
    });
    

---
  #### **Name**
Integration Test Patterns
  #### **Description**
Test component interactions with real dependencies
  #### **When**
Testing APIs, database operations, service interactions
  #### **Example**
    // Supertest for API testing
    import request from 'supertest';
    import { app } from '../app';
    import { db } from '../db';
    
    describe('POST /api/users', () => {
      beforeEach(async () => {
        await db.migrate.latest();
        await db.seed.run();
      });
    
      afterEach(async () => {
        await db('users').truncate();
      });
    
      it('creates user and returns 201', async () => {
        const response = await request(app)
          .post('/api/users')
          .send({ email: 'new@example.com', name: 'Test User' })
          .expect(201);
    
        expect(response.body).toMatchObject({
          email: 'new@example.com',
          name: 'Test User',
        });
    
        // Verify in database
        const user = await db('users').where({ email: 'new@example.com' }).first();
        expect(user).toBeDefined();
      });
    
      it('returns 400 for duplicate email', async () => {
        await db('users').insert({ email: 'existing@example.com', name: 'Existing' });
    
        await request(app)
          .post('/api/users')
          .send({ email: 'existing@example.com', name: 'Duplicate' })
          .expect(400);
      });
    });
    
    // Use test containers for real database
    import { PostgreSqlContainer } from '@testcontainers/postgresql';
    
    let container;
    beforeAll(async () => {
      container = await new PostgreSqlContainer().start();
      process.env.DATABASE_URL = container.getConnectionUri();
    });
    
    afterAll(async () => {
      await container.stop();
    });
    

---
  #### **Name**
E2E Test Strategy
  #### **Description**
Test critical user journeys end-to-end
  #### **When**
Validating complete user workflows
  #### **Example**
    // Playwright example
    import { test, expect } from '@playwright/test';
    
    test.describe('Checkout Flow', () => {
      test.beforeEach(async ({ page }) => {
        // Setup: logged in user with items in cart
        await page.goto('/login');
        await page.fill('[data-testid="email"]', 'test@example.com');
        await page.fill('[data-testid="password"]', 'password');
        await page.click('[data-testid="login-button"]');
        await expect(page).toHaveURL('/dashboard');
      });
    
      test('completes purchase with valid payment', async ({ page }) => {
        // Navigate to checkout
        await page.goto('/cart');
        await page.click('[data-testid="checkout-button"]');
    
        // Fill payment details
        await page.fill('[data-testid="card-number"]', '4242424242424242');
        await page.fill('[data-testid="card-expiry"]', '12/25');
        await page.fill('[data-testid="card-cvc"]', '123');
    
        // Complete purchase
        await page.click('[data-testid="pay-button"]');
    
        // Verify success
        await expect(page).toHaveURL(/\/order\/\w+/);
        await expect(page.locator('[data-testid="success-message"]'))
          .toContainText('Order confirmed');
      });
    
      test('shows error for declined card', async ({ page }) => {
        await page.goto('/cart');
        await page.click('[data-testid="checkout-button"]');
    
        // Use test card that declines
        await page.fill('[data-testid="card-number"]', '4000000000000002');
        await page.fill('[data-testid="card-expiry"]', '12/25');
        await page.fill('[data-testid="card-cvc"]', '123');
        await page.click('[data-testid="pay-button"]');
    
        await expect(page.locator('[data-testid="error-message"]'))
          .toContainText('Card declined');
      });
    });
    

---
  #### **Name**
Mocking Strategies
  #### **Description**
Isolate dependencies without hiding bugs
  #### **When**
Unit testing with external dependencies
  #### **Example**
    // Good: Mock at boundaries, not everywhere
    describe('OrderService', () => {
      // Mock external payment gateway
      const mockPaymentGateway = {
        charge: jest.fn(),
      };
    
      // Use real order calculator (internal logic)
      const orderCalculator = new OrderCalculator();
    
      const service = new OrderService(mockPaymentGateway, orderCalculator);
    
      it('charges correct amount after discount', async () => {
        mockPaymentGateway.charge.mockResolvedValue({ id: 'ch_123' });
    
        const order = { items: [{ price: 100, qty: 2 }], discountCode: 'SAVE10' };
        await service.processOrder(order);
    
        // Real calculation happened, only payment was mocked
        expect(mockPaymentGateway.charge).toHaveBeenCalledWith(180); // 200 - 10%
      });
    });
    
    // Good: Use dependency injection for testability
    class UserService {
      constructor(
        private userRepo: UserRepository,
        private emailService: EmailService,
        private hasher: PasswordHasher
      ) {}
    }
    
    // In tests, inject mocks
    const service = new UserService(mockRepo, mockEmail, mockHasher);
    
    // Bad: Mocking implementation details
    // Don't mock: array methods, Date, Math, internal private methods
    // Do mock: databases, APIs, file systems, email services
    

---
  #### **Name**
Test Data Management
  #### **Description**
Reliable, isolated test data
  #### **When**
Tests need consistent starting state
  #### **Example**
    // Factory pattern for test data
    const userFactory = {
      build: (overrides = {}) => ({
        id: faker.string.uuid(),
        email: faker.internet.email(),
        name: faker.person.fullName(),
        createdAt: new Date(),
        ...overrides,
      }),
    
      create: async (overrides = {}) => {
        const user = userFactory.build(overrides);
        await db('users').insert(user);
        return user;
      },
    
      createMany: async (count, overrides = {}) => {
        const users = Array.from({ length: count }, () => userFactory.build(overrides));
        await db('users').insert(users);
        return users;
      },
    };
    
    // Usage in tests
    describe('UserList', () => {
      it('paginates users correctly', async () => {
        await userFactory.createMany(25);
    
        const response = await request(app)
          .get('/api/users?page=2&limit=10');
    
        expect(response.body.data).toHaveLength(10);
        expect(response.body.pagination.page).toBe(2);
      });
    });
    
    // Database cleanup strategies
    beforeEach(async () => {
      // Option 1: Truncate tables
      await db.raw('TRUNCATE users, orders, products CASCADE');
    
      // Option 2: Transaction rollback
      await db.transaction(async (trx) => {
        // Test runs here
      }); // Auto-rollback
    });
    

## Anti-Patterns


---
  #### **Name**
Ice Cream Cone
  #### **Description**
Inverted pyramid with many e2e tests, few unit tests
  #### **Why**
E2E tests are slow (minutes vs milliseconds), flaky (browser timing issues), and expensive (infrastructure). CI takes 30+ minutes. Team waits hours for feedback. Flaky tests get ignored.
  #### **Instead**
Follow testing pyramid. Unit tests for logic, integration for APIs, e2e only for critical paths. Target 70% unit, 20% integration, 10% e2e.

---
  #### **Name**
Flaky Tests Ignored
  #### **Description**
Tests that sometimes pass, sometimes fail
  #### **Why**
Team reruns until green. Real failures get missed. "The tests are flaky" becomes excuse for merging broken code. Eventually all tests are untrusted.
  #### **Instead**
Quarantine flaky tests immediately. Fix root causes (timing, state, external dependencies). Never merge with flaky failures.

---
  #### **Name**
Testing Implementation Details
  #### **Description**
Tests that break when code is refactored
  #### **Why**
Test mocks internal methods. Rename private method, test breaks. 50 tests to update for one refactor. Team fears refactoring. Code rots.
  #### **Instead**
Test behavior, not implementation. "When I do X, Y happens" not "Method A calls method B". Tests should survive refactoring.

---
  #### **Name**
Over-Mocking
  #### **Description**
Mocking everything including the code under test
  #### **Why**
All collaborators mocked. Test passes but production fails. Mock returns happy path, real code has bugs. 100% coverage, 0% confidence.
  #### **Instead**
Mock only external boundaries (databases, APIs, file systems). Use real implementations for internal collaborators. Prefer integration tests over heavily mocked unit tests.

---
  #### **Name**
Slow Test Suite
  #### **Description**
Tests that take 30+ minutes to run
  #### **Why**
Developers don't run tests locally. Push and pray. CI queue backs up. Feedback loop is hours instead of minutes. Bugs caught days later.
  #### **Instead**
Unit tests should run in seconds. Integration tests in minutes. Parallelize. Use test containers. Only run affected tests on PR.

---
  #### **Name**
Coverage Worship
  #### **Description**
Chasing 100% coverage as a goal
  #### **Why**
Tests added just to hit coverage. Tests that assert nothing. Tests that verify implementation. High coverage, low confidence. Trivial getters tested, complex logic ignored.
  #### **Instead**
Coverage is a metric, not a goal. Focus on critical paths. Mutation testing to find weak tests. Quality over quantity.