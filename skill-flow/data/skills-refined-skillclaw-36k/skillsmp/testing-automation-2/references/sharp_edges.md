# Testing Automation - Sharp Edges

## Flaky Test Timing Dependency

### **Id**
flaky-test-timing-dependency
### **Summary**
Test passes locally, fails in CI due to timing assumptions
### **Severity**
high
### **Situation**
Test depends on setTimeout, setInterval, or implicit timing
### **Why**
  Test waits 100ms for async operation. Works on your machine (fast SSD, idle CPU).
  CI runner under load, operation takes 150ms. Test fails. You add 200ms wait.
  Passes for a while. CI gets busier. Fails again. Team starts ignoring failures.
  "Just re-run it" becomes the solution. Eventually real bugs slip through.
  
### **Solution**
  // WRONG: Fixed timing assumptions
  it('shows loading then content', async () => {
    render(<DataLoader />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
    await new Promise(r => setTimeout(r, 100));  // Race condition!
    expect(screen.getByText('Data loaded')).toBeInTheDocument();
  });
  
  // RIGHT: Wait for actual state change
  it('shows loading then content', async () => {
    render(<DataLoader />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
    await waitFor(() => {
      expect(screen.getByText('Data loaded')).toBeInTheDocument();
    });
  });
  
  // RIGHT: Use fake timers for time-dependent code
  it('debounces search input', () => {
    jest.useFakeTimers();
    render(<SearchBox onSearch={mockSearch} />);
  
    fireEvent.change(input, { target: { value: 'test' } });
    expect(mockSearch).not.toHaveBeenCalled();
  
    jest.advanceTimersByTime(300);
    expect(mockSearch).toHaveBeenCalledWith('test');
  });
  
  // RIGHT: For Playwright/Cypress, use built-in waiting
  await expect(page.locator('[data-testid="content"]')).toBeVisible();
  // NOT: await page.waitForTimeout(1000);
  
### **Symptoms**
  - Test passes locally, fails in CI
  - setTimeout/sleep in test code
  - "Just re-run it" as common response
  - Inconsistent test results
### **Detection Pattern**
setTimeout|sleep|waitForTimeout|new Promise.*setTimeout

## Test Order Dependency

### **Id**
test-order-dependency
### **Summary**
Tests pass when run together, fail when run in isolation or different order
### **Severity**
high
### **Situation**
Test depends on state from previous test
### **Why**
  Test A creates user in database. Test B assumes user exists. Run together, passes.
  Run Test B alone, fails. Run in parallel, fails. Run in random order, sometimes fails.
  Root cause hidden until CI parallelizes tests for speed. Then everything breaks.
  Hours wasted debugging "the tests worked yesterday."
  
### **Solution**
  // WRONG: Shared mutable state between tests
  let testUser;
  
  describe('User operations', () => {
    it('creates user', async () => {
      testUser = await createUser({ name: 'Test' });
      expect(testUser.id).toBeDefined();
    });
  
    it('updates user', async () => {
      await updateUser(testUser.id, { name: 'Updated' });  // Depends on previous test!
      const user = await getUser(testUser.id);
      expect(user.name).toBe('Updated');
    });
  });
  
  // RIGHT: Each test sets up its own state
  describe('User operations', () => {
    it('creates user', async () => {
      const user = await createUser({ name: 'Test' });
      expect(user.id).toBeDefined();
    });
  
    it('updates user', async () => {
      // Arrange: Create user for THIS test
      const user = await createUser({ name: 'Test' });
  
      // Act
      await updateUser(user.id, { name: 'Updated' });
  
      // Assert
      const updated = await getUser(user.id);
      expect(updated.name).toBe('Updated');
    });
  });
  
  // RIGHT: Use beforeEach for consistent setup
  describe('User operations', () => {
    let user;
  
    beforeEach(async () => {
      user = await createUser({ name: 'Test' });
    });
  
    afterEach(async () => {
      await deleteUser(user.id);
    });
  
    it('updates user', async () => {
      await updateUser(user.id, { name: 'Updated' });
      const updated = await getUser(user.id);
      expect(updated.name).toBe('Updated');
    });
  });
  
### **Symptoms**
  - Tests pass together, fail in isolation
  - CI parallel mode breaks tests
  - Random test order causes failures
  - Shared variables across tests
### **Detection Pattern**
let\s+\w+;\s*\n\s*describe|beforeAll.*create.*\n.*it\(

## Mock Implementation Not Behavior

### **Id**
mock-implementation-not-behavior
### **Summary**
Mock returns happy path, real implementation has edge cases that cause production bugs
### **Severity**
high
### **Situation**
Mocking external service but not its real behavior
### **Why**
  Mock Stripe: `mockStripe.charge.mockResolvedValue({ success: true })`.
  All tests pass. Ship to production. Real Stripe returns `{ status: 'pending' }`
  for some transactions. Code doesn't handle it. Customers charged, orders not created.
  100% test coverage, production bug. Mock was testing your fantasy, not reality.
  
### **Solution**
  // WRONG: Mock only happy path
  const mockPayment = {
    charge: jest.fn().mockResolvedValue({ success: true, id: 'ch_123' }),
  };
  
  it('processes payment', async () => {
    const result = await processOrder(order, mockPayment);
    expect(result.status).toBe('completed');
  });
  // But what about declined cards? Network errors? Rate limits?
  
  // RIGHT: Mock realistic scenarios including failures
  describe('Payment processing', () => {
    it('handles successful payment', async () => {
      mockPayment.charge.mockResolvedValue({
        status: 'succeeded',
        id: 'ch_123'
      });
      const result = await processOrder(order, mockPayment);
      expect(result.status).toBe('completed');
    });
  
    it('handles declined card', async () => {
      mockPayment.charge.mockRejectedValue(
        new PaymentError('card_declined', 'Your card was declined')
      );
      await expect(processOrder(order, mockPayment))
        .rejects.toThrow('Payment failed');
    });
  
    it('handles pending status (3D Secure)', async () => {
      mockPayment.charge.mockResolvedValue({
        status: 'requires_action',
        client_secret: 'pi_xxx_secret_yyy'
      });
      const result = await processOrder(order, mockPayment);
      expect(result.status).toBe('pending_confirmation');
    });
  
    it('handles network timeout', async () => {
      mockPayment.charge.mockRejectedValue(new Error('ETIMEDOUT'));
      // Should retry or fail gracefully, not crash
      const result = await processOrder(order, mockPayment);
      expect(result.status).toBe('payment_pending');
    });
  });
  
  // BEST: Use contract tests against real API in staging
  // Or use Stripe's test mode with test card numbers
  
### **Symptoms**
  - Tests all pass but production fails
  - Mocks only return success
  - No error scenario tests
  - Edge cases discovered in production
### **Detection Pattern**
mockResolvedValue.*success|mockReturnValue.*true

## Database State Pollution

### **Id**
database-state-pollution
### **Summary**
Tests interfere with each other through shared database state
### **Severity**
high
### **Situation**
Multiple tests write to the same database without proper isolation
### **Why**
  Test A inserts user with email "test@example.com". Test B expects unique constraint
  to work, also uses "test@example.com". Tests run in order: passes. Run in parallel:
  one fails with "duplicate key" error. Or worse: Test A doesn't clean up, Test B
  finds unexpected data and fails mysteriously. Database becomes polluted over time.
  
### **Solution**
  // WRONG: Shared database state, no cleanup
  it('creates user', async () => {
    await db('users').insert({ email: 'test@example.com' });
    // Never cleaned up!
  });
  
  it('enforces unique email', async () => {
    await db('users').insert({ email: 'test@example.com' });
    // Fails if previous test ran first
  });
  
  // RIGHT: Transaction rollback for each test
  describe('User operations', () => {
    let trx;
  
    beforeEach(async () => {
      trx = await db.transaction();
    });
  
    afterEach(async () => {
      await trx.rollback();  // Undo all changes
    });
  
    it('creates user', async () => {
      await trx('users').insert({ email: 'test@example.com' });
      const user = await trx('users').where({ email: 'test@example.com' }).first();
      expect(user).toBeDefined();
    });
  });
  
  // RIGHT: Unique data per test with factories
  import { faker } from '@faker-js/faker';
  
  const createTestUser = (overrides = {}) => ({
    email: faker.internet.email(),
    name: faker.person.fullName(),
    ...overrides,
  });
  
  it('creates user with unique email', async () => {
    const userData = createTestUser();
    await db('users').insert(userData);
    // Each test gets unique email, no conflicts
  });
  
  // RIGHT: Database reset between test files
  beforeAll(async () => {
    await db.migrate.latest();
  });
  
  beforeEach(async () => {
    await db.raw('TRUNCATE users, orders, products RESTART IDENTITY CASCADE');
  });
  
### **Symptoms**
  - Tests fail when run in parallel
  - Unique constraint violations
  - Data "left over" from previous tests
  - Tests pass individually, fail together
### **Detection Pattern**
test@example\.com|insert.*hardcoded

## Mock Never Restored

### **Id**
mock-never-restored
### **Summary**
Mock from one test affects subsequent tests
### **Severity**
medium
### **Situation**
Global mock or spy not restored after test
### **Why**
  Test A mocks `Date.now()` to test time-based logic. Forgets to restore.
  All subsequent tests have frozen time. Test B tests "created 5 minutes ago"
  logic, uses real time comparison, fails mysteriously. Hours debugging to find
  the mock from 50 tests ago that poisoned everything.
  
### **Solution**
  // WRONG: Mock not restored
  it('shows relative time', () => {
    jest.spyOn(Date, 'now').mockReturnValue(1000000);
    expect(formatTime(999000)).toBe('1 second ago');
    // Date.now still mocked for all future tests!
  });
  
  // RIGHT: Always restore mocks
  it('shows relative time', () => {
    const spy = jest.spyOn(Date, 'now').mockReturnValue(1000000);
    try {
      expect(formatTime(999000)).toBe('1 second ago');
    } finally {
      spy.mockRestore();  // Always restore
    }
  });
  
  // RIGHT: Use Jest's automatic cleanup
  afterEach(() => {
    jest.restoreAllMocks();
  });
  
  // Or in jest.config.js:
  // restoreMocks: true
  
  // RIGHT: For module mocks, reset between tests
  jest.mock('./api');
  import { fetchData } from './api';
  
  beforeEach(() => {
    jest.resetAllMocks();  // Clear mock state
  });
  
  // RIGHT: Scope mocks to test blocks
  describe('with mocked time', () => {
    beforeAll(() => {
      jest.useFakeTimers();
      jest.setSystemTime(new Date('2024-01-01'));
    });
  
    afterAll(() => {
      jest.useRealTimers();
    });
  
    it('test with fake time', () => { ... });
  });
  
  describe('with real time', () => {
    it('test with real time', () => { ... });  // Not affected
  });
  
### **Symptoms**
  - Tests fail depending on order
  - Date/time tests affect other tests
  - "Works when I run it alone"
  - Mock values from other tests appear
### **Detection Pattern**
spyOn|jest\.mock(?!.*restore)|mockImplementation

## E2E Brittle Selectors

### **Id**
e2e-brittle-selectors
### **Summary**
E2E tests break on every UI change due to fragile selectors
### **Severity**
medium
### **Situation**
Tests select elements by CSS class, position, or generated IDs
### **Why**
  Test finds button by `.css-1234xyz` (generated class). Design change regenerates
  classes. All E2E tests fail. Or select by `div > div > button:first-child`.
  Add a loading indicator, position changes, test fails. Team spends more time
  fixing tests than shipping features. Eventually tests are deleted.
  
### **Solution**
  // WRONG: Brittle selectors
  await page.click('.MuiButton-root');  // Material UI generated class
  await page.click('button:nth-child(2)');  // Position-dependent
  await page.click('#submit-btn-12345');  // Generated ID
  
  // RIGHT: Use data-testid attributes
  await page.click('[data-testid="submit-button"]');
  await page.click('[data-testid="user-profile-menu"]');
  
  // RIGHT: Use accessible selectors (better for a11y too)
  await page.getByRole('button', { name: 'Submit' }).click();
  await page.getByLabel('Email address').fill('test@example.com');
  await page.getByText('Welcome back').isVisible();
  
  // RIGHT: Use Playwright's recommended selectors
  // Priority: role > label > placeholder > text > testid > css
  await page.getByRole('link', { name: 'Sign up' }).click();
  await page.getByPlaceholder('Enter your email').fill('test@example.com');
  
  // Component side: Add stable test IDs
  <button data-testid="checkout-button" className={styles.button}>
    Checkout
  </button>
  
  // RIGHT: Create page objects for maintainability
  class CheckoutPage {
    constructor(page) {
      this.page = page;
      this.submitButton = page.getByRole('button', { name: 'Complete purchase' });
      this.emailInput = page.getByLabel('Email');
    }
  
    async fillEmail(email) {
      await this.emailInput.fill(email);
    }
  
    async submit() {
      await this.submitButton.click();
    }
  }
  
### **Symptoms**
  - Tests break on CSS changes
  - Position-based selectors
  - Generated class names in selectors
  - Frequent test maintenance
### **Detection Pattern**
nth-child|:first-child|css-[a-z0-9]+|MuiButton

## Snapshot Test Blindness

### **Id**
snapshot-test-blindness
### **Summary**
Snapshot tests auto-approved without review, mask real changes
### **Severity**
medium
### **Situation**
Large snapshot diffs routinely updated with `--updateSnapshot`
### **Why**
  Component renders 500-line HTML. Snapshot test captures it all. Small change
  creates 200-line diff. Reviewer can't tell if intentional. Developer runs
  `jest --updateSnapshot`. PR approved. Weeks later: "Why is this text wrong?"
  Snapshot showed it, but no one read 200 lines of HTML diff.
  
### **Solution**
  // WRONG: Giant snapshots nobody reads
  it('renders correctly', () => {
    const component = render(<ComplexDashboard user={mockUser} />);
    expect(component).toMatchSnapshot();  // 500+ lines
  });
  
  // RIGHT: Targeted inline snapshots
  it('renders user greeting', () => {
    render(<Dashboard user={{ name: 'Alice' }} />);
    expect(screen.getByTestId('greeting').textContent).toMatchInlineSnapshot(
      `"Welcome back, Alice!"`
    );
  });
  
  // RIGHT: Test behavior, not structure
  it('shows user name in header', () => {
    render(<Dashboard user={{ name: 'Alice' }} />);
    expect(screen.getByText('Welcome back, Alice!')).toBeInTheDocument();
  });
  
  // RIGHT: If snapshots needed, keep them small and focused
  it('renders menu items correctly', () => {
    const { container } = render(<NavigationMenu items={menuItems} />);
    expect(container.querySelector('nav')).toMatchSnapshot();
    // Snapshot only the nav, not entire page
  });
  
  // RIGHT: Visual regression for styling (with tools)
  // Use Percy, Chromatic, or Playwright visual comparisons
  // These highlight actual visual differences, not DOM changes
  
  // Config: Warn on large snapshot updates
  // In CI: fail if snapshot changes without explicit flag
  // Require separate PR for snapshot updates with screenshot
  
### **Symptoms**
  - "Update snapshot" in every PR
  - 100+ line snapshot files
  - Nobody reads snapshot diffs
  - Visual bugs slip through
### **Detection Pattern**
toMatchSnapshot\(\)$|\.snap.*lines

## Testing Private Implementation

### **Id**
testing-private-implementation
### **Summary**
Tests break on refactoring because they test internal implementation, not behavior
### **Severity**
medium
### **Situation**
Tests mock private methods or assert on internal state
### **Why**
  Test mocks `_calculateDiscount()` private method. Refactor to `computeDiscount()`.
  20 tests break. Or test asserts `component.state.isLoading === true`. Refactor
  to use hook. All tests break. Code behavior unchanged, tests still fail.
  Team fears refactoring. Code rots because changing it breaks too many tests.
  
### **Solution**
  // WRONG: Testing implementation details
  it('calculates discount', () => {
    const service = new OrderService();
    jest.spyOn(service, '_calculateDiscount');  // Private method
  
    service.processOrder(order);
  
    expect(service._calculateDiscount).toHaveBeenCalledWith(100);
  });
  
  // WRONG: Testing React internal state
  it('shows loading state', () => {
    const wrapper = shallow(<DataLoader />);
    expect(wrapper.state('isLoading')).toBe(true);  // Internal state!
  });
  
  // RIGHT: Test observable behavior
  it('applies 10% discount for orders over $100', () => {
    const service = new OrderService();
    const result = service.processOrder({ items: [{ price: 150 }] });
    expect(result.discount).toBe(15);  // Test the output, not how
  });
  
  // RIGHT: Test what user sees
  it('shows loading indicator while fetching', async () => {
    render(<DataLoader />);
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  
    await waitForElementToBeRemoved(() => screen.queryByRole('progressbar'));
    expect(screen.getByText('Data loaded')).toBeInTheDocument();
  });
  
  // RIGHT: Test public API contracts
  describe('OrderService', () => {
    it('returns order with calculated total', () => {
      const result = service.processOrder(order);
      expect(result).toMatchObject({
        total: expect.any(Number),
        discount: expect.any(Number),
        status: 'pending',
      });
    });
  });
  
  // The "what", not the "how":
  // - Given this input, expect this output
  // - When user clicks, expect this visible change
  // - After action, expect this API call
  
### **Symptoms**
  - Tests break on refactoring
  - Mocking private methods
  - Accessing component state directly
  - Tests tied to implementation
### **Detection Pattern**
\.state\(|_[a-zA-Z]+.*mock|spyOn.*_

## Async Test Not Awaited

### **Id**
async-test-not-awaited
### **Summary**
Test completes before async operation, passes incorrectly
### **Severity**
high
### **Situation**
Assertion runs before async code finishes
### **Why**
  Test calls async function, forgets `await`. Function returns promise.
  Assertion runs immediately (before promise resolves). Test passes because
  no assertion failed yet. Promise rejects later, outside test scope.
  "All tests green" but feature is broken. Discovered in production.
  
### **Solution**
  // WRONG: Missing await
  it('creates user', () => {
    const user = createUser({ email: 'test@example.com' });  // Missing await!
    expect(user.id).toBeDefined();  // user is a Promise, not a user object!
    // This passes because Promise object has properties
  });
  
  // WRONG: Callback not waited
  it('handles callback', () => {
    fetchData((err, data) => {
      expect(err).toBeNull();  // Never runs before test ends
      expect(data).toBeDefined();
    });
    // Test ends immediately, callback ignored
  });
  
  // RIGHT: Always await async operations
  it('creates user', async () => {
    const user = await createUser({ email: 'test@example.com' });
    expect(user.id).toBeDefined();
  });
  
  // RIGHT: Return promise for non-async/await
  it('fetches data', () => {
    return fetchData().then(data => {
      expect(data).toBeDefined();
    });
  });
  
  // RIGHT: Use done callback correctly
  it('handles callback', (done) => {
    fetchData((err, data) => {
      expect(err).toBeNull();
      expect(data).toBeDefined();
      done();  // Signal test completion
    });
  });
  
  // RIGHT: Configure Jest to detect unhandled rejections
  // jest.config.js
  // testEnvironmentOptions: { customExportConditions: ['node'] }
  // Also: --detectOpenHandles flag
  
  // RIGHT: ESLint rule to catch this
  // 'jest/no-done-callback': 'error'
  // '@typescript-eslint/no-floating-promises': 'error'
  
### **Symptoms**
  - Tests pass but feature broken
  - Unhandled promise rejection warnings
  - Inconsistent test results
  - Missing await in test code
### **Detection Pattern**
it\([^)]+\)\s*{\s*(?!.*await|return)

## Coverage Worship

### **Id**
coverage-worship
### **Summary**
High coverage with low-value tests - bugs still slip through
### **Severity**
medium
### **Situation**
Tests written just to increase coverage percentage
### **Why**
  Manager mandates 80% coverage. Team writes tests for getters, setters, trivial
  functions. Coverage at 85%! But complex business logic has one test for happy path.
  Edge cases uncovered. Mutation testing shows 40% of mutations survive. High coverage,
  low confidence. Bugs in the hard parts, fully tested trivial parts.
  
### **Solution**
  // WRONG: Tests for coverage, not confidence
  it('gets name', () => {
    const user = new User({ name: 'Alice' });
    expect(user.getName()).toBe('Alice');
  });
  
  it('sets name', () => {
    const user = new User({});
    user.setName('Bob');
    expect(user.getName()).toBe('Bob');
  });
  // 100% coverage on User class, 0% value
  
  // RIGHT: Test complex logic thoroughly
  describe('OrderPricing', () => {
    it('applies member discount before tax', () => { ... });
    it('caps discount at $50', () => { ... });
    it('handles multiple discount codes', () => { ... });
    it('rejects expired coupons', () => { ... });
    it('calculates tax after discount', () => { ... });
    it('rounds to 2 decimal places', () => { ... });
    // Lower overall coverage, higher confidence in critical code
  });
  
  // RIGHT: Use mutation testing to find weak tests
  // npm run test:mutation (Stryker for JS)
  // If mutating code doesn't fail tests, tests are weak
  
  // RIGHT: Focus coverage on critical paths
  // jest.config.js
  coverageThreshold: {
    './src/billing/**': { branches: 90, functions: 90 },
    './src/utils/**': { branches: 50 },  // Less critical
  }
  
  // RIGHT: Coverage as a metric, not a goal
  // Use coverage to FIND untested code, not to prove code is tested
  // Look for: 0% coverage in critical files
  // Ignore: 70% vs 80% overall number
  
### **Symptoms**
  - High coverage, bugs still ship
  - Tests for trivial code
  - Complex functions with 1 test
  - Mutation testing shows weak tests
### **Detection Pattern**
get[A-Z]|set[A-Z]|\.name\)\.toBe

## Integration Test External Service

### **Id**
integration-test-external-service
### **Summary**
Integration tests call real external services - flaky and slow
### **Severity**
medium
### **Situation**
Tests hit production APIs, third-party services
### **Why**
  Test calls real Stripe API. Stripe has outage. All tests fail. Or test creates
  real AWS resources. Resource limit hit. Tests fail. Or third-party API rate
  limits. Tests flaky during high usage periods. Slow (network calls) and
  unreliable (external dependencies). CI becomes lottery.
  
### **Solution**
  // WRONG: Real external service calls
  it('charges credit card', async () => {
    const result = await stripe.charges.create({
      amount: 1000,
      currency: 'usd',
      source: 'tok_visa',  // Real API call!
    });
    expect(result.status).toBe('succeeded');
  });
  
  // RIGHT: Use service sandboxes/test modes
  it('charges credit card', async () => {
    const stripe = new Stripe(process.env.STRIPE_TEST_KEY);
    const result = await stripe.charges.create({
      amount: 1000,
      currency: 'usd',
      source: 'tok_visa',  // Stripe test mode - no real charge
    });
    expect(result.status).toBe('succeeded');
  });
  
  // RIGHT: Mock at integration boundaries
  import nock from 'nock';
  
  beforeEach(() => {
    nock('https://api.stripe.com')
      .post('/v1/charges')
      .reply(200, { id: 'ch_123', status: 'succeeded' });
  });
  
  afterEach(() => {
    nock.cleanAll();
  });
  
  // RIGHT: Use WireMock or similar for complex scenarios
  // Record real responses, replay in tests
  
  // RIGHT: Contract tests instead of integration tests
  // Test that YOUR code sends correct requests
  // Separate contract tests verify API compatibility
  
  // RIGHT: Use test containers for databases, queues
  import { PostgreSqlContainer } from '@testcontainers/postgresql';
  
  let container;
  beforeAll(async () => {
    container = await new PostgreSqlContainer().start();
    process.env.DATABASE_URL = container.getConnectionUri();
  });
  
### **Symptoms**
  - Tests fail on external service outage
  - Slow test suite (network calls)
  - Rate limit errors in CI
  - Tests depend on external state
### **Detection Pattern**
stripe\.|aws\.|http[s]?://api\.