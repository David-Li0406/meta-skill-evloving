# Testing Strategies

## Patterns


---
  #### **Name**
Testing Pyramid
  #### **Description**
Balance of test types
  #### **When**
Planning test strategy
  #### **Example**
    # TESTING PYRAMID:
    
    """
    The pyramid guides quantity, not importance.
    More unit tests (fast, cheap)
    Fewer integration tests (medium)
    Even fewer E2E tests (slow, expensive)
    """
    
    # UNIT TESTS (70%)
    # - Test pure functions, utilities
    # - Test individual components in isolation
    # - Fast, no external dependencies
    # - Run on every save
    
    test('formatDate returns readable date', () => {
      expect(formatDate(new Date('2024-01-15'))).toBe('Jan 15, 2024');
    });
    
    
    # INTEGRATION TESTS (20%)
    # - Test component interactions
    # - Test API endpoints with database
    # - Test service combinations
    # - Run on commit
    
    test('user can sign up and receive welcome email', async () => {
      const user = await createUser({ email: 'test@test.com' });
      expect(user.id).toBeDefined();
      expect(emailQueue.jobs).toContainEqual(
        expect.objectContaining({ to: 'test@test.com' })
      );
    });
    
    
    # E2E TESTS (10%)
    # - Test complete user flows
    # - Test in real browser
    # - Run before deploy
    # - Keep minimal and critical
    
    test('user can complete checkout', async ({ page }) => {
      await page.goto('/');
      await page.click('[data-testid="add-to-cart"]');
      await page.click('[data-testid="checkout"]');
      await page.fill('#email', 'test@test.com');
      await page.click('[data-testid="submit"]');
      await expect(page.locator('.confirmation')).toBeVisible();
    });
    

---
  #### **Name**
React Component Testing
  #### **Description**
Testing React with Testing Library
  #### **When**
Testing React components
  #### **Example**
    # REACT COMPONENT TESTING:
    
    """
    Test behavior, not implementation.
    Query like users (by role, text, label).
    Don't test internal state.
    """
    
    import { render, screen, waitFor } from '@testing-library/react';
    import userEvent from '@testing-library/user-event';
    import { LoginForm } from './LoginForm';
    
    describe('LoginForm', () => {
      it('submits email and password', async () => {
        const onSubmit = vi.fn();
        const user = userEvent.setup();
    
        render(<LoginForm onSubmit={onSubmit} />);
    
        // Query by role/label - how users find elements
        await user.type(screen.getByLabelText(/email/i), 'test@test.com');
        await user.type(screen.getByLabelText(/password/i), 'password123');
        await user.click(screen.getByRole('button', { name: /sign in/i }));
    
        expect(onSubmit).toHaveBeenCalledWith({
          email: 'test@test.com',
          password: 'password123',
        });
      });
    
      it('shows error for invalid email', async () => {
        const user = userEvent.setup();
        render(<LoginForm onSubmit={vi.fn()} />);
    
        await user.type(screen.getByLabelText(/email/i), 'invalid');
        await user.click(screen.getByRole('button', { name: /sign in/i }));
    
        expect(screen.getByText(/invalid email/i)).toBeInTheDocument();
      });
    
      it('disables submit while loading', async () => {
        render(<LoginForm onSubmit={vi.fn()} isLoading />);
    
        expect(screen.getByRole('button')).toBeDisabled();
        expect(screen.getByText(/signing in/i)).toBeInTheDocument();
      });
    });
    
    
    // Testing hooks
    import { renderHook, act } from '@testing-library/react';
    import { useCounter } from './useCounter';
    
    test('useCounter increments', () => {
      const { result } = renderHook(() => useCounter());
    
      act(() => {
        result.current.increment();
      });
    
      expect(result.current.count).toBe(1);
    });
    

---
  #### **Name**
API Testing
  #### **Description**
Testing backend APIs
  #### **When**
Testing API endpoints
  #### **Example**
    # API TESTING:
    
    """
    Test the HTTP contract.
    Use real database (test instance).
    Test error cases explicitly.
    """
    
    // Jest + Supertest (Express)
    import request from 'supertest';
    import { app } from '../app';
    import { prisma } from '../db';
    
    describe('POST /users', () => {
      beforeEach(async () => {
        await prisma.user.deleteMany();
      });
    
      it('creates a user', async () => {
        const response = await request(app)
          .post('/users')
          .send({ email: 'test@test.com', name: 'Test User' })
          .expect(201);
    
        expect(response.body).toMatchObject({
          id: expect.any(Number),
          email: 'test@test.com',
          name: 'Test User',
        });
    
        // Verify in database
        const user = await prisma.user.findUnique({
          where: { email: 'test@test.com' },
        });
        expect(user).not.toBeNull();
      });
    
      it('returns 400 for invalid email', async () => {
        const response = await request(app)
          .post('/users')
          .send({ email: 'invalid', name: 'Test' })
          .expect(400);
    
        expect(response.body.error).toContain('email');
      });
    
      it('returns 409 for duplicate email', async () => {
        await prisma.user.create({
          data: { email: 'test@test.com', name: 'Existing' },
        });
    
        await request(app)
          .post('/users')
          .send({ email: 'test@test.com', name: 'New' })
          .expect(409);
      });
    });
    
    
    // FastAPI + pytest
    import pytest
    from httpx import AsyncClient
    from app.main import app
    
    @pytest.mark.asyncio
    async def test_create_user():
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/users",
                json={"email": "test@test.com", "name": "Test User"}
            )
            assert response.status_code == 201
            assert response.json()["email"] == "test@test.com"
    

---
  #### **Name**
Mocking Strategies
  #### **Description**
When and how to mock
  #### **When**
Dealing with external dependencies
  #### **Example**
    # MOCKING STRATEGIES:
    
    """
    Mock at boundaries (APIs, databases, time).
    Don't mock what you own.
    Prefer dependency injection over mocking.
    """
    
    // MOCK EXTERNAL APIS
    // Use MSW (Mock Service Worker) for network mocking
    import { rest } from 'msw';
    import { setupServer } from 'msw/node';
    
    const server = setupServer(
      rest.get('https://api.example.com/users/:id', (req, res, ctx) => {
        return res(ctx.json({ id: req.params.id, name: 'Test User' }));
      })
    );
    
    beforeAll(() => server.listen());
    afterEach(() => server.resetHandlers());
    afterAll(() => server.close());
    
    test('fetches user data', async () => {
      const user = await fetchUser('123');
      expect(user.name).toBe('Test User');
    });
    
    
    // MOCK TIME
    beforeEach(() => {
      vi.useFakeTimers();
      vi.setSystemTime(new Date('2024-01-15'));
    });
    
    afterEach(() => {
      vi.useRealTimers();
    });
    
    test('shows relative time', () => {
      const oneHourAgo = new Date('2024-01-15T09:00:00');
      expect(formatRelativeTime(oneHourAgo)).toBe('1 hour ago');
    });
    
    
    // DEPENDENCY INJECTION OVER MOCKING
    // Instead of mocking internal functions:
    // WRONG:
    jest.mock('./sendEmail');
    const { sendEmail } = require('./sendEmail');
    sendEmail.mockResolvedValue();
    
    // RIGHT: Inject dependency
    function createUserService(emailService) {
      return {
        async createUser(data) {
          const user = await db.create(data);
          await emailService.send(user.email, 'Welcome!');
          return user;
        }
      };
    }
    
    test('sends welcome email', async () => {
      const mockEmailService = { send: vi.fn() };
      const service = createUserService(mockEmailService);
    
      await service.createUser({ email: 'test@test.com' });
    
      expect(mockEmailService.send).toHaveBeenCalledWith(
        'test@test.com',
        'Welcome!'
      );
    });
    

---
  #### **Name**
E2E Testing with Playwright
  #### **Description**
End-to-end browser testing
  #### **When**
Testing complete user flows
  #### **Example**
    # PLAYWRIGHT E2E:
    
    """
    Test critical user journeys.
    Use Page Object Model for maintainability.
    Run in CI before deploy.
    """
    
    // playwright.config.ts
    import { defineConfig } from '@playwright/test';
    
    export default defineConfig({
      testDir: './e2e',
      fullyParallel: true,
      forbidOnly: !!process.env.CI,
      retries: process.env.CI ? 2 : 0,
      workers: process.env.CI ? 1 : undefined,
      use: {
        baseURL: 'http://localhost:3000',
        trace: 'on-first-retry',
      },
    });
    
    
    // e2e/checkout.spec.ts
    import { test, expect } from '@playwright/test';
    
    test.describe('Checkout', () => {
      test.beforeEach(async ({ page }) => {
        // Seed test data
        await page.request.post('/api/test/seed');
      });
    
      test('user can complete purchase', async ({ page }) => {
        // Browse to product
        await page.goto('/products');
        await page.click('[data-testid="product-1"]');
    
        // Add to cart
        await page.click('[data-testid="add-to-cart"]');
        await expect(page.locator('.cart-count')).toHaveText('1');
    
        // Go to checkout
        await page.click('[data-testid="checkout"]');
    
        // Fill shipping
        await page.fill('#email', 'test@test.com');
        await page.fill('#address', '123 Test St');
        await page.click('[data-testid="continue"]');
    
        // Payment (use test card)
        await page.fill('#card', '4242424242424242');
        await page.fill('#expiry', '12/25');
        await page.fill('#cvc', '123');
    
        // Submit
        await page.click('[data-testid="submit"]');
    
        // Verify confirmation
        await expect(page.locator('.confirmation')).toBeVisible();
        await expect(page.locator('.order-number')).toContainText(/ORD-/);
      });
    
      test('shows error for invalid payment', async ({ page }) => {
        // ... setup
        await page.fill('#card', '4000000000000002'); // Declined card
        await page.click('[data-testid="submit"]');
    
        await expect(page.locator('.error')).toContainText('declined');
      });
    });
    
    
    // Page Object Model
    // pages/CheckoutPage.ts
    export class CheckoutPage {
      constructor(private page: Page) {}
    
      async fillShipping(email: string, address: string) {
        await this.page.fill('#email', email);
        await this.page.fill('#address', address);
        await this.page.click('[data-testid="continue"]');
      }
    
      async fillPayment(card: string, expiry: string, cvc: string) {
        await this.page.fill('#card', card);
        await this.page.fill('#expiry', expiry);
        await this.page.fill('#cvc', cvc);
      }
    
      async submit() {
        await this.page.click('[data-testid="submit"]');
      }
    }
    

---
  #### **Name**
Test Fixtures and Factories
  #### **Description**
Reusable test data
  #### **When**
Tests need consistent data
  #### **Example**
    # TEST FIXTURES:
    
    """
    Factories create test objects.
    Fixtures provide test context.
    Both make tests readable and maintainable.
    """
    
    // Factory pattern (JavaScript)
    const userFactory = {
      build: (overrides = {}) => ({
        id: faker.string.uuid(),
        email: faker.internet.email(),
        name: faker.person.fullName(),
        createdAt: new Date(),
        ...overrides,
      }),
    
      create: async (overrides = {}) => {
        const data = userFactory.build(overrides);
        return prisma.user.create({ data });
      },
    };
    
    test('user display', () => {
      const user = userFactory.build({ name: 'John Doe' });
      render(<UserCard user={user} />);
      expect(screen.getByText('John Doe')).toBeInTheDocument();
    });
    
    
    // pytest fixtures
    import pytest
    from app.models import User
    
    @pytest.fixture
    def user(db_session):
        user = User(email="test@test.com", name="Test User")
        db_session.add(user)
        db_session.commit()
        return user
    
    @pytest.fixture
    def authenticated_client(client, user):
        client.force_login(user)
        return client
    
    def test_profile_page(authenticated_client, user):
        response = authenticated_client.get('/profile')
        assert response.status_code == 200
        assert user.name in response.text
    
    
    // Jest with beforeEach
    describe('Order', () => {
      let user: User;
      let product: Product;
    
      beforeEach(async () => {
        user = await userFactory.create();
        product = await productFactory.create({ price: 1000 });
      });
    
      it('creates order with correct total', async () => {
        const order = await createOrder(user.id, [product.id]);
        expect(order.total).toBe(1000);
      });
    });
    

## Anti-Patterns


---
  #### **Name**
Testing Implementation
  #### **Description**
Tests that break when you refactor
  #### **Why**
    If you test private methods, state changes, or specific function calls,
    your tests break when you refactor even though behavior is unchanged.
    Tests become a burden, not a safety net.
    
  #### **Instead**
    # WRONG: Testing implementation
    test('clicking button updates isLoading state', () => {
      const { result } = renderHook(() => useState(false));
      // Testing internal state...
    });
    
    # RIGHT: Testing behavior
    test('shows loading spinner when submitting', async () => {
      render(<Form />);
      await user.click(screen.getByRole('button'));
      expect(screen.getByTestId('spinner')).toBeInTheDocument();
    });
    

---
  #### **Name**
Overmocking
  #### **Description**
Mocking too much of your own code
  #### **Why**
    When you mock everything, you're testing mocks, not code. Integration
    between components is where bugs live. Your test passes but production
    fails.
    
  #### **Instead**
    # WRONG: Mock everything
    jest.mock('./userService');
    jest.mock('./emailService');
    jest.mock('./database');
    
    # RIGHT: Only mock boundaries
    // Mock: External APIs, time, randomness
    // Don't mock: Your own services, utilities
    
    # RIGHT: Use real implementations with test database
    beforeAll(() => setupTestDatabase());
    

---
  #### **Name**
Flaky Tests
  #### **Description**
Tests that sometimes pass, sometimes fail
  #### **Why**
    Flaky tests erode trust. Developers start ignoring failures. They
    re-run until it passes. Eventually, real bugs slip through because
    "it's probably just flaky."
    
  #### **Instead**
    # Common causes of flakiness:
    # 1. Race conditions - use proper waitFor
    # 2. Shared state - isolate tests
    # 3. Time-dependent - mock time
    # 4. Order-dependent - tests should be independent
    
    # WRONG: Race condition
    await user.click(button);
    expect(screen.getByText('Done')).toBeInTheDocument();
    
    # RIGHT: Wait for async updates
    await user.click(button);
    await waitFor(() => {
      expect(screen.getByText('Done')).toBeInTheDocument();
    });
    

---
  #### **Name**
Chasing Coverage
  #### **Description**
Testing trivial code to hit coverage targets
  #### **Why**
    95% coverage that tests getters, setters, and obvious code while
    missing edge cases is worse than 70% coverage of the right things.
    Coverage measures quantity, not quality.
    
  #### **Instead**
    # Focus coverage on:
    # - Business logic
    # - Edge cases
    # - Error handling
    # - Integration points
    
    # Don't waste time testing:
    # - Simple getters/setters
    # - Framework code
    # - Type definitions
    