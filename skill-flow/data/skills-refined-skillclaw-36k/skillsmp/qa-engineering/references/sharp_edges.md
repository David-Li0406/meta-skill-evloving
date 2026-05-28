# Qa Engineering - Sharp Edges

## Flaky Test Infestation

### **Id**
flaky-test-infestation
### **Summary**
Test suite with intermittent failures that pass on retry
### **Severity**
critical
### **Situation**
Tests that sometimes pass and sometimes fail with no code change
### **Why**
  Team ignores test failures. Real bugs slip through. "Just re-run" becomes culture.
  Flaky tests are worse than no tests - they train the team to ignore failures.
  When real bugs fail, they get dismissed as flakiness.
  
### **Solution**
  # Zero tolerance policy
  1. Flaky test = broken test
  2. Fix or delete immediately
  3. Never just re-run
  
  # Quarantine flaky tests
  Move to quarantine suite
  Don't block CI
  Track and fix with deadline
  
  # Find root causes
  Race conditions → Add proper waits
  Shared state → Isolate tests
  Timing issues → Deterministic waits
  Order dependency → Independent tests
  
  # Test infrastructure
  beforeEach(async () => {
    jest.useFakeTimers()
  })
  
  // Retry once in CI (flag as flaky)
  // Track flakiness metrics
  // Prioritize fixing
  
### **Symptoms**
  - Tests fail intermittently
  - "Just re-run" culture
  - Team ignores failures
  - Different results on same code
### **Detection Pattern**
retry|flaky|intermittent|sometimes fails

## E2E Test Addiction

### **Id**
e2e-test-addiction
### **Summary**
Over-reliance on end-to-end tests at the expense of unit/integration tests
### **Severity**
high
### **Situation**
Test pyramid inverted with most tests being slow E2E tests
### **Why**
  Slow CI (45+ minutes), hard to debug, expensive to maintain. Most bugs can
  be caught cheaper and earlier with unit/integration tests.
  
### **Solution**
  # Follow the test pyramid
  Unit tests: 70% (fast, isolated)
  Integration tests: 20% (module boundaries)
  E2E tests: 10% (critical paths only)
  
  # E2E for critical paths only
  - User can sign up
  - User can complete core action
  - User can purchase/subscribe
  - Critical integrations work
  
  # Push tests down
  Can unit test catch this? → Unit test
  Need to test integration? → Integration test
  Critical user journey? → E2E test
  
  # NOT every form validation, error state, or edge case
  
### **Symptoms**
  - CI takes 30+ minutes
  - Hard to debug failures
  - Many E2E tests, few unit tests
  - Test maintenance is painful
### **Detection Pattern**
describe.*e2e|test.*e2e|playwright|cypress|selenium

## Hardcoded Wait Nightmare

### **Id**
hardcoded-wait-nightmare
### **Summary**
Using fixed time delays instead of condition-based waits
### **Severity**
high
### **Situation**
Tests use sleep() or setTimeout instead of waiting for conditions
### **Why**
  Fixed waits are guesses. Too short = flaky. Too long = slow. Both = broken tests.
  Fast server waits too long, slow server still fails.
  
### **Solution**
  # WRONG: Hardcoded wait
  await page.click('.submit')
  await page.waitForTimeout(5000)  // Hope it's loaded
  expect(page.locator('.result')).toBeVisible()
  
  # RIGHT: Wait for conditions
  await page.click('.submit')
  await page.waitForSelector('.result', { state: 'visible' })
  expect(page.locator('.result')).toBeVisible()
  
  # Custom wait helpers
  async function waitForApi(path) {
    await page.waitForResponse(
      response => response.url().includes(path)
    )
  }
  
  # Network idle when appropriate
  await page.waitForLoadState('networkidle')
  
### **Symptoms**
  - Tests with sleep/delay calls
  - Flaky tests on slower systems
  - CI significantly slower than local
  - waitForTimeout in test code
### **Detection Pattern**
waitForTimeout|sleep|setTimeout.*test|delay.*ms

## Test Data Nightmare

### **Id**
test-data-nightmare
### **Summary**
Tests sharing or depending on data created by other tests
### **Severity**
high
### **Situation**
Test order matters because tests depend on shared database state
### **Why**
  Order-dependent tests can't run in parallel, fail in different environments,
  and create hidden dependencies that make debugging impossible.
  
### **Solution**
  # Test isolation - each test creates and cleans its own data
  beforeEach(async () => {
    testUser = await createTestUser({ email: `test-${uuid()}@test.com` })
  })
  
  afterEach(async () => {
    await cleanupTestUser(testUser.id)
  })
  
  # Unique identifiers prevent collisions
  const email = `test-${uuid()}@test.com`
  
  # Database isolation strategies
  # - Transactions: Roll back after test
  # - Truncation: Clear tables before suite
  # - Containers: Fresh DB per suite
  
  # Tests can run in any order, in parallel
  
### **Symptoms**
  - Tests fail when run in different order
  - Can't run tests in parallel
  - Tests fail in CI but pass locally
  - Shared test data files
### **Detection Pattern**
beforeAll.*insert|shared.*data|global.*test

## Missing Error Path

### **Id**
missing-error-path
### **Summary**
Only testing the happy path, ignoring error states
### **Severity**
high
### **Situation**
Tests only verify successful scenarios, not failures
### **Why**
  Happy paths are easy. Error paths are where bugs hide. Users will find every
  error path. Untested error handling is unpredictable in production.
  
### **Solution**
  # For each feature, test:
  - Invalid input
  - Network failure
  - Server error (500)
  - Timeout
  - Unauthorized (401, 403)
  
  # Boundary testing
  - Empty inputs
  - Maximum lengths
  - Special characters
  - Unexpected types
  
  # Failure injection
  test('handles API error', async () => {
    server.use(
      rest.post('/api/submit', (req, res, ctx) => {
        return res(ctx.status(500))
      })
    )
    await user.click(submitButton)
    expect(screen.getByText(/error/i)).toBeVisible()
  })
  
### **Symptoms**
  - Only happy path tests
  - No error message assertions
  - Missing mock error responses
  - Untested catch blocks
### **Detection Pattern**
expect.*success|expect.*200(?!.*error|.*fail)

## Screenshot Comparison Trap

### **Id**
screenshot-comparison-trap
### **Summary**
Over-relying on visual regression tests
### **Severity**
medium
### **Situation**
Excessive visual regression tests cause noise and maintenance burden
### **Why**
  1000s of screenshots to maintain. Tiny changes break everything. False positives
  overwhelm real bugs. Team starts approving blindly.
  
### **Solution**
  # Selective visual testing
  Key pages only
  Design system components
  Not every permutation
  
  # Component-level testing
  Test components in isolation (Storybook)
  Not full pages
  
  # Threshold settings
  Allow small differences (< 0.1%)
  Focus on structural changes
  Not pixel-perfect
  
  # Keep visual tests under control
  Under 50 for most apps
  Under 200 for large apps
  Above 500 = maintenance hell
  
### **Symptoms**
  - Thousands of visual snapshots
  - Frequent false positive failures
  - Team auto-approves visual diffs
  - Long snapshot review times
### **Detection Pattern**
toMatchSnapshot|toMatchImageSnapshot|percy|chromatic

## Works In Isolation Blindspot

### **Id**
works-in-isolation-blindspot
### **Summary**
Components pass unit tests but fail when integrated
### **Severity**
high
### **Situation**
All unit tests pass but integrated system fails
### **Why**
  Unit tests test units, not integration. Interfaces are where bugs hide.
  Form submits wrong format, service expects different structure, confirmation
  shows wrong data - but all unit tests passed.
  
### **Solution**
  # Integration tests for seams
  test('payment flow integration', async () => {
    const form = new PaymentForm()
    const service = new PaymentService()
  
    form.fill({ card: '4242...' })
    const result = await service.process(form.getData())
  
    expect(result.status).toBe('success')
  })
  
  # Contract testing
  const provider = new PactV3({ consumer: 'Frontend', provider: 'UserAPI' })
  provider.addInteraction({
    uponReceiving: 'a request for user',
    withRequest: { method: 'GET', path: '/users/1' },
    willRespondWith: {
      status: 200,
      body: { id: 1, name: string(), email: email() }
    }
  })
  
  # Test the boundaries between components
  
### **Symptoms**
  - Unit tests pass, integration fails
  - API contract mismatches
  - Data transformation bugs
  - Module interface issues
### **Detection Pattern**
mock.*service|jest\\.mock.*repository

## Test What You Built Trap

### **Id**
test-what-you-built-trap
### **Summary**
Developer writes tests for their implementation, not requirements
### **Severity**
high
### **Situation**
Tests validate how code works, not what it should do
### **Why**
  Tests pass, but requirements aren't met. Testing exact match when requirements
  say "search products" means partial match, case insensitive, and typo tolerance
  go untested.
  
### **Solution**
  # Test requirements, not implementation
  
  # BAD: Tests what was built
  test('search finds exact match', () => {
    expect(search('iPhone')).toContain('iPhone')
  })
  
  # GOOD: Tests requirements
  describe('product search', () => {
    test('finds case insensitive matches', () => {
      expect(search('iphone')).toContain('iPhone')
    })
    test('finds partial matches', () => {
      expect(search('phone')).toContain('iPhone')
    })
    test('handles empty results gracefully', () => {
      expect(search('zzz')).toEqual([])
    })
  })
  
  # Write tests from requirements before code (TDD)
  # Get independent review of tests
  # Test as user would use it
  
### **Symptoms**
  - Tests mirror implementation exactly
  - Edge cases not in tests
  - Tests break on refactor
  - Requirements not covered
### **Detection Pattern**


## Ignored Console Error

### **Id**
ignored-console-error
### **Summary**
Tests pass despite console errors and warnings
### **Severity**
high
### **Situation**
Test output has errors but tests still pass
### **Why**
  Console errors indicate problems. Ignoring them lets bugs through. Real errors
  get buried in noise. Tests become less trustworthy.
  
### **Solution**
  # Fail on console errors (Jest)
  beforeEach(() => {
    jest.spyOn(console, 'error')
      .mockImplementation((msg) => {
        throw new Error(msg)
      })
  })
  
  # Assert no errors (Playwright)
  page.on('console', msg => {
    if (msg.type() === 'error') {
      throw new Error(msg.text())
    }
  })
  
  # Clean up warnings
  Fix React key warnings
  Fix deprecation warnings
  Clean console = real signals visible
  
  # Console error policy
  Production code: Zero console.error
  Test code: Fail on console.error
  Third-party noise: Explicitly filter
  
### **Symptoms**
  - Console errors during test runs
  - React warnings in test output
  - Tests pass with errors visible
  - Unhandled promise rejections
### **Detection Pattern**
console\\.error.*ignore|suppressConsoleError

## Unmaintained Test Suite

### **Id**
unmaintained-test-suite
### **Summary**
Tests written and abandoned, not updated with code changes
### **Severity**
high
### **Situation**
Growing number of skipped, failing, or outdated tests
### **Why**
  Tests require maintenance. Unmaintained tests rot. Skipped tests become
  permanently skipped. Test debt compounds like technical debt.
  
### **Solution**
  # Tests in Definition of Done
  Feature not done until tests updated
  Code review includes tests
  No merging with failing tests
  
  # Zero skipped tests policy
  Skipped = blocked or deleted
  No indefinite skipping
  Time limit: 2 weeks max
  
  # Skipped test needs:
  - JIRA ticket
  - Owner
  - Deadline
  - Reason documented
  
  # Test health metrics
  Track passing/failing/skipped
  Trend over time
  Alert on degradation
  
  // Track test debt like code debt
  // test.skip requires comment with ticket
  
### **Symptoms**
  - Growing skip count
  - TODO Fix comments in tests
  - Tests commented out
  - Outdated test descriptions
### **Detection Pattern**
test\\.skip|it\\.skip|xit\\(|xdescribe\\(

## Missing Test Environment

### **Id**
missing-test-environment
### **Summary**
Tests only run locally, not in CI/staging-like environment
### **Severity**
high
### **Situation**
Tests pass locally but fail in CI or staging
### **Why**
  Local environment ≠ production environment. Different browser versions,
  limited resources, network latency, container restrictions all cause
  "works on my machine" failures.
  
### **Solution**
  # CI as source of truth
  If it fails in CI, it's broken
  Local passing is not enough
  CI must pass to merge
  
  # Environment parity
  CI matches production
  Same browser versions
  Same dependencies
  Same constraints
  
  # Container-based testing
  Docker for test environment
  Reproducible everywhere
  Same container as CI
  
  # Environment checklist
  □ CI runs all tests
  □ CI uses same browser versions
  □ CI has resource limits
  □ CI uses real(ish) backend
  □ Environment variables match
  □ Dependencies locked
  
### **Symptoms**
  - Works locally, fails in CI
  - Different browser behavior
  - Resource-related failures
  - Environment variable issues
### **Detection Pattern**
process\\.env\\.CI|isCI|GITHUB_ACTIONS

## Assertion Free Test

### **Id**
assertion-free-test
### **Summary**
Tests that execute code but don't assert anything meaningful
### **Severity**
high
### **Situation**
Tests run code but have no expect() or assertion statements
### **Why**
  Execution without assertion = useless test. Tests pass even when code is broken.
  "No error" is not success. You don't know if checkout succeeded, order was
  created, or confirmation was shown.
  
### **Solution**
  # WRONG: No assertion
  test('user can checkout', async () => {
    await page.goto('/cart')
    await page.click('.checkout')
    await page.fill('#email', 'test@test.com')
    await page.click('.submit')
    // No assertion!
  })
  
  # RIGHT: Assert outcomes
  test('user can checkout', async () => {
    await page.goto('/cart')
    await page.click('.checkout')
    await page.fill('#email', 'test@test.com')
    await page.click('.submit')
  
    await expect(page.locator('.confirmation')).toBeVisible()
    await expect(page.locator('.order-number')).toHaveText(/ORD-\d+/)
  })
  
  # Assertion checklist
  □ Test has at least one assertion
  □ Assertion checks outcome, not execution
  □ Assertion is specific enough
  □ Test would fail if feature broke
  
### **Symptoms**
  - Tests without expect()
  - Tests that only execute actions
  - Missing assertion libraries
  - Tests that "never fail"
### **Detection Pattern**
test\\([^)]*\\)\\s*\\{[^}]*\\}(?!.*expect)