# QA Engineering

## Patterns


---
  #### **Name**
Test Pyramid
  #### **Description**
Many fast unit tests, fewer integration tests, fewest E2E tests
  #### **When**
Designing test strategy, balancing coverage vs speed
  #### **Example**
    Test distribution target:
    - Unit tests: 70% (fast, isolated, many)
    - Integration tests: 20% (module boundaries)
    - E2E tests: 10% (critical user journeys only)
    
    E2E tests should cover:
    - User can sign up
    - User can complete core action
    - User can purchase/subscribe
    - Critical integrations work
    
    NOT every form validation or edge case.
    

---
  #### **Name**
Arrange-Act-Assert
  #### **Description**
Structure tests with clear setup, action, and verification phases
  #### **When**
Writing any test for clarity and maintainability
  #### **Example**
    test('user can add item to cart', async () => {
      // Arrange - Setup
      const user = await createTestUser()
      const product = await createTestProduct()
    
      // Act - Execute
      await cartService.addItem(user.id, product.id)
    
      // Assert - Verify
      const cart = await cartService.getCart(user.id)
      expect(cart.items).toHaveLength(1)
      expect(cart.items[0].productId).toBe(product.id)
    })
    

---
  #### **Name**
Test Isolation
  #### **Description**
Each test creates its own data and cleans up after itself
  #### **When**
Tests share a database, preventing order-dependent failures
  #### **Example**
    beforeEach(async () => {
      // Create fresh data for this test
      testUser = await createTestUser({ email: `test-${uuid()}@test.com` })
    })
    
    afterEach(async () => {
      // Clean up test data
      await cleanupTestUser(testUser.id)
    })
    
    // Tests can run in any order, in parallel
    

---
  #### **Name**
Page Object Model
  #### **Description**
Encapsulate page interactions in reusable objects
  #### **When**
E2E tests need to interact with UI elements across multiple tests
  #### **Example**
    class LoginPage {
      constructor(page) { this.page = page }
    
      async login(email, password) {
        await this.page.fill('[data-testid="email"]', email)
        await this.page.fill('[data-testid="password"]', password)
        await this.page.click('[data-testid="submit"]')
      }
    
      async getError() {
        return this.page.textContent('[data-testid="error"]')
      }
    }
    
    // Tests use page objects
    test('shows error on invalid credentials', async () => {
      const loginPage = new LoginPage(page)
      await loginPage.login('wrong@email.com', 'wrong')
      expect(await loginPage.getError()).toContain('Invalid credentials')
    })
    

---
  #### **Name**
Contract Testing
  #### **Description**
Test that API provider and consumer agree on interface
  #### **When**
Frontend and backend developed separately, microservices
  #### **Example**
    // Consumer test (frontend)
    const provider = new PactV3({ consumer: 'Frontend', provider: 'UserAPI' })
    provider.addInteraction({
      uponReceiving: 'a request for user',
      withRequest: { method: 'GET', path: '/users/1' },
      willRespondWith: {
        status: 200,
        body: { id: 1, name: string(), email: email() }
      }
    })
    
    // Provider verifies it meets the contract
    

## Anti-Patterns


---
  #### **Name**
Flaky Tests
  #### **Description**
Tests that sometimes pass and sometimes fail with no code change
  #### **Why**
Team ignores failures, real bugs slip through, "just re-run" becomes culture.
  #### **Instead**
Zero tolerance. Fix or quarantine immediately. Track flakiness metrics.

---
  #### **Name**
E2E Test Addiction
  #### **Description**
Over-reliance on slow end-to-end tests for everything
  #### **Why**
Slow CI, hard to debug, expensive to maintain. Most bugs can be caught earlier.
  #### **Instead**
Follow the pyramid. Push tests down. E2E for critical paths only.

---
  #### **Name**
Hardcoded Waits
  #### **Description**
Using sleep() or fixed timeouts instead of condition-based waits
  #### **Why**
Too short = flaky, too long = slow, both = broken.
  #### **Instead**
Wait for conditions (element visible, API response, state change).

---
  #### **Name**
Shared Test Data
  #### **Description**
Tests depending on data created by other tests
  #### **Why**
Order-dependent, can't parallelize, environment-specific failures.
  #### **Instead**
Each test creates and cleans up its own data.

---
  #### **Name**
Testing Implementation
  #### **Description**
Tests that know and verify internal implementation details
  #### **Why**
Tests break when you refactor, even if behavior is unchanged.
  #### **Instead**
Test behavior and outcomes, not how code is structured.

---
  #### **Name**
Assertion-Free Tests
  #### **Description**
Tests that execute code but don't verify anything
  #### **Why**
Test passes even when code is broken. "No error" is not success.
  #### **Instead**
Every test must have meaningful assertions about expected outcomes.