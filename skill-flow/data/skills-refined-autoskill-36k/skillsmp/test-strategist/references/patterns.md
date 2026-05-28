# Test Strategist

## Patterns


---
  #### **Name**
The Pragmatic Test Pyramid
  #### **Description**
Layer tests appropriately for fast feedback and confidence
  #### **When**
Designing test strategy for any project
  #### **Example**
    # The classic pyramid (Mike Cohn):
    #
    #        /\
    #       /E2E\        Few, slow, high confidence
    #      /------\
    #     /Integr- \     Some, medium speed
    #    /  ation   \
    #   /------------\
    #  /    Unit      \  Many, fast, low confidence per test
    # /________________\
    
    # Modern rebalancing (Kent C. Dodds):
    #
    #       /\
    #      /E2E\         Still few (critical paths only)
    #     /------\
    #    / Integr-\      MORE than traditional pyramid
    #   /  ation   \     (catches most real bugs)
    #  /------------\
    # /     Unit     \   Fewer than traditional
    #/________________\  (complex logic only)
    
    # WHEN TO USE WHICH:
    
    ## Unit Tests: Complex logic in isolation
    - Pure functions with many edge cases
    - Algorithms and calculations
    - State machines
    - Input validation
    
    ## Integration Tests: Components working together
    - API endpoints with database
    - Service interactions
    - Real HTTP requests (to local services)
    - File system operations
    
    ## E2E Tests: Critical user journeys
    - Signup → first action → conversion
    - Payment flows
    - Authentication
    - Top 5 most important user paths
    
    # Golden rule: If the test shape matches the bug shape, you'll catch it.
    # Most bugs are integration bugs, not unit logic bugs.
    

---
  #### **Name**
Test Behavior, Not Implementation
  #### **Description**
Tests that survive refactoring
  #### **When**
Writing any test
  #### **Example**
    # BAD: Testing implementation details
    describe('UserService', () => {
      it('calls database.query with correct SQL', () => {
        const db = mock(Database);
        const service = new UserService(db);
    
        service.getUser(123);
    
        // Breaks if you change query structure
        expect(db.query).toHaveBeenCalledWith(
          'SELECT * FROM users WHERE id = ?', [123]
        );
      });
    });
    
    # GOOD: Testing behavior
    describe('UserService', () => {
      it('returns user by id', async () => {
        const service = new UserService(testDb);
        await testDb.insert({ id: 123, name: 'Alice' });
    
        const user = await service.getUser(123);
    
        // Survives query refactoring
        expect(user.name).toBe('Alice');
      });
    
      it('returns null for non-existent user', async () => {
        const service = new UserService(testDb);
    
        const user = await service.getUser(999);
    
        expect(user).toBeNull();
      });
    });
    
    # The rule: Test the contract (what the function promises),
    # not the implementation (how it fulfills that promise).
    

---
  #### **Name**
The Arrange-Act-Assert Pattern
  #### **Description**
Clear test structure for readability
  #### **When**
Writing any test
  #### **Example**
    describe('OrderCalculator', () => {
      it('applies percentage discount to order total', () => {
        // ARRANGE: Set up the scenario
        const items = [
          { name: 'Widget', price: 100 },
          { name: 'Gadget', price: 200 },
        ];
        const discount = { type: 'percentage', value: 10 };
        const calculator = new OrderCalculator();
    
        // ACT: Do the thing being tested
        const total = calculator.calculate(items, discount);
    
        // ASSERT: Verify the result
        expect(total).toBe(270); // 300 - 10%
      });
    });
    
    # Variations for complex scenarios:
    
    # Given-When-Then (same thing, BDD style):
    describe('given items totaling $300', () => {
      describe('when 10% discount is applied', () => {
        it('then total is $270', () => {
          // ...
        });
      });
    });
    
    # Multiple assertions on same result (OK):
    it('returns complete user profile', () => {
      const profile = getProfile(userId);
    
      expect(profile.name).toBe('Alice');
      expect(profile.email).toContain('@');
      expect(profile.createdAt).toBeInstanceOf(Date);
    });
    

---
  #### **Name**
Strategic Test Coverage
  #### **Description**
Focus testing effort where bugs hide
  #### **When**
Deciding what to test
  #### **Example**
    # HIGH PRIORITY (test thoroughly):
    - Money calculations (off-by-one cents add up)
    - Authentication and authorization (security critical)
    - Data transformations (where input → output logic lives)
    - Edge cases in core business logic
    - Integration points with external systems
    - Code that has broken before (regression prone)
    
    # MEDIUM PRIORITY (test key paths):
    - API endpoint contracts
    - Database queries (especially complex ones)
    - State management
    - Error handling paths
    
    # LOW PRIORITY (test sparingly or skip):
    - Simple getters/setters
    - Configuration objects
    - Thin wrappers around libraries
    - Code that will be deleted soon
    - Highly stable, rarely changed code
    
    # Coverage metrics are a tool, not a goal:
    """
    90% coverage with:
    - All edge cases tested
    - Integration points verified
    - No flaky tests
    = Good suite
    
    90% coverage with:
    - Only happy paths
    - Lots of mocking
    - Several flaky tests
    = False confidence
    """
    

---
  #### **Name**
Test-Driven Development (When Appropriate)
  #### **Description**
Write tests first when it makes sense
  #### **When**
Clear requirements, well-understood domain
  #### **Example**
    # TDD Cycle:
    # 1. RED: Write a failing test
    # 2. GREEN: Write minimal code to pass
    # 3. REFACTOR: Clean up while keeping tests green
    
    # Example: Building a validator
    
    # Step 1: RED - Write failing test
    it('rejects emails without @', () => {
      expect(isValidEmail('notanemail')).toBe(false);
    });
    // Run: FAIL (isValidEmail doesn't exist)
    
    # Step 2: GREEN - Minimal implementation
    function isValidEmail(email) {
      return email.includes('@');
    }
    // Run: PASS
    
    # Step 3: RED - Next requirement
    it('rejects emails without domain', () => {
      expect(isValidEmail('user@')).toBe(false);
    });
    // Run: FAIL
    
    # Step 4: GREEN - Extend implementation
    function isValidEmail(email) {
      const parts = email.split('@');
      return parts.length === 2 && parts[1].length > 0;
    }
    // Run: PASS
    
    # WHEN TDD WORKS:
    - Requirements are clear
    - Building library/utility code
    - Complex logic with many cases
    - Working on well-understood domain
    
    # WHEN TO SKIP TDD:
    - Exploratory/spike code
    - UI prototyping
    - Learning new framework
    - Uncertain requirements (test after)
    

---
  #### **Name**
Integration Test Design
  #### **Description**
Testing components working together with real dependencies
  #### **When**
Testing API endpoints, database operations, or service interactions
  #### **Example**
    # Integration test with real database
    
    describe('OrderAPI', () => {
      let app;
      let db;
    
      beforeAll(async () => {
        db = await createTestDatabase();
        app = createApp({ db });
      });
    
      beforeEach(async () => {
        await db.truncate(['orders', 'order_items']);
      });
    
      afterAll(async () => {
        await db.close();
      });
    
      it('creates order and returns with generated id', async () => {
        const response = await request(app)
          .post('/orders')
          .send({
            userId: 'user-1',
            items: [{ productId: 'prod-1', quantity: 2 }]
          });
    
        expect(response.status).toBe(201);
        expect(response.body.id).toMatch(/^order-/);
    
        // Verify in database
        const order = await db.orders.findById(response.body.id);
        expect(order.userId).toBe('user-1');
        expect(order.items).toHaveLength(1);
      });
    
      it('returns 400 for invalid order', async () => {
        const response = await request(app)
          .post('/orders')
          .send({ userId: 'user-1' }); // Missing items
    
        expect(response.status).toBe(400);
        expect(response.body.error).toContain('items');
      });
    });
    
    # Key principles:
    # - Use real database (in-memory or container)
    # - Clean state between tests (truncate, not recreate)
    # - Test full request/response cycle
    # - Verify side effects (database state)
    

## Anti-Patterns


---
  #### **Name**
The Liar
  #### **Description**
Test that passes but doesn't test what it claims
  #### **Why**
    Test has a descriptive name but the assertions don't match. "should reject
    invalid email" but actually just checks the function doesn't throw. Gives
    false confidence while bugs slip through.
    
  #### **Instead**
Make sure assertions match the test name. Review tests for what they actually verify.

---
  #### **Name**
Excessive Mocking
  #### **Description**
Test that mocks so much it tests nothing real
  #### **Why**
    Ten mocks, three stubs, two spies. The test passes, but what did it prove?
    You tested that your mocks work, not that your code works. When you change
    implementation, tests break even though behavior is correct.
    
  #### **Instead**
Use real dependencies where practical. Mock only external systems and slow operations.

---
  #### **Name**
The Slow Poke
  #### **Description**
Test suite that takes too long to run
  #### **Why**
    Tests take 20 minutes. Developers run them before lunch, not after each change.
    When tests are slow, they're not part of the development feedback loop. Bugs
    accumulate until the delayed test run.
    
  #### **Instead**
Aim for full unit suite < 30 seconds, integration suite < 5 minutes. Parallelize. Use in-memory databases.

---
  #### **Name**
Flaky Tests
  #### **Description**
Tests that sometimes pass and sometimes fail
  #### **Why**
    Flaky tests train developers to ignore failures. "Oh, that test is just flaky,
    retry it." Eventually real bugs hide behind "flakiness." The test suite becomes
    meaningless.
    
  #### **Instead**
Delete or fix flaky tests immediately. Common causes: timing dependencies, shared state, random data.

---
  #### **Name**
Testing Implementation Details
  #### **Description**
Tests that break when you refactor working code
  #### **Why**
    You refactor a function, behavior unchanged, but 15 tests break because they
    asserted on internal details. Now refactoring is scary because it means
    rewriting tests. Tests that should enable refactoring now prevent it.
    
  #### **Instead**
Test observable behavior. Assert on outputs, not on how you got there.

---
  #### **Name**
The Giant Test
  #### **Description**
Single test that verifies everything
  #### **Why**
    One test method with 50 assertions. When it fails, you don't know which part
    broke. When requirements change, you have to understand the entire test to
    modify any part. It's a test-shaped monolith.
    
  #### **Instead**
One logical assertion per test. Test name should describe the specific behavior.