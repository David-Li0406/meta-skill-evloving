# Test Quality Checklist

Complete checklist for assessing test quality and regression protection.

---

## Critical Path Coverage

### Authentication & Authorization

- [ ] **Login success** - Valid credentials authenticate user
- [ ] **Login failure** - Invalid credentials rejected with proper error
- [ ] **Session expiry** - Expired sessions handled correctly
- [ ] **Token refresh** - Token refresh works before/after expiry
- [ ] **Logout** - Session properly invalidated
- [ ] **Permission checks** - Unauthorized access rejected
- [ ] **Role-based access** - Each role has correct permissions
- [ ] **Multi-tenant isolation** - Users can't access other tenants' data

### Core Business Logic

- [ ] **Happy path** - Main success scenario works
- [ ] **Input validation** - Invalid inputs rejected with clear errors
- [ ] **Boundary conditions** - Min/max/zero values handled
- [ ] **State transitions** - Valid state changes work, invalid blocked
- [ ] **Calculations** - Financial/math operations are precise
- [ ] **Idempotency** - Duplicate operations handled safely

### Data Operations

- [ ] **Create** - New records created correctly
- [ ] **Read** - Data retrieved accurately
- [ ] **Update** - Updates applied correctly, partial updates work
- [ ] **Delete** - Soft/hard delete works, cascades correct
- [ ] **Transactions** - Atomic operations are atomic
- [ ] **Concurrent writes** - Race conditions handled

### External Integrations

- [ ] **API calls succeed** - Happy path with external services
- [ ] **API calls fail** - Timeouts, errors handled gracefully
- [ ] **Retry logic** - Transient failures retried correctly
- [ ] **Circuit breaker** - Failing services isolated
- [ ] **Webhook handling** - Incoming webhooks processed correctly
- [ ] **Event publishing** - Events published with correct payload

---

## Failure Case Coverage

### Error Handling

- [ ] **Network failures** - Connection refused, timeout, DNS failure
- [ ] **Database failures** - Connection lost, query timeout, deadlock
- [ ] **External API failures** - 4xx, 5xx, malformed responses
- [ ] **Validation errors** - Clear error messages returned
- [ ] **Business rule violations** - Domain errors handled properly
- [ ] **Unexpected exceptions** - Caught and logged appropriately

### Resource Exhaustion

- [ ] **Memory limits** - Behavior under memory pressure
- [ ] **Connection pool exhausted** - Graceful handling
- [ ] **Rate limit hit** - Backoff and retry behavior
- [ ] **Disk full** - Write failures handled
- [ ] **Queue full** - Backpressure behavior

### Partial Failures

- [ ] **Partial success** - Some operations succeed, others fail
- [ ] **Rollback** - Failed transactions rolled back completely
- [ ] **Compensation** - Saga rollback works correctly
- [ ] **Recovery** - System recovers after failure

---

## Edge Case Coverage

### Input Edge Cases

- [ ] **Empty input** - Empty strings, arrays, objects
- [ ] **Null/undefined** - Null values handled
- [ ] **Maximum length** - Max string length, array size
- [ ] **Special characters** - Unicode, emojis, control characters
- [ ] **Whitespace** - Leading/trailing spaces, tabs, newlines
- [ ] **Negative numbers** - Where applicable
- [ ] **Zero** - Zero quantities, zero amounts
- [ ] **Decimal precision** - Floating point edge cases

### Boundary Conditions

- [ ] **Off-by-one** - First/last item, N vs N-1 vs N+1
- [ ] **Pagination boundaries** - First page, last page, empty page
- [ ] **Date boundaries** - Midnight, month end, year end, DST
- [ ] **Timezone edge cases** - UTC conversion, DST transitions
- [ ] **Integer overflow** - Large numbers near limits

### Timing Edge Cases

- [ ] **Concurrent requests** - Same resource modified simultaneously
- [ ] **Race conditions** - Order-dependent operations
- [ ] **Stale data** - Reading during writes
- [ ] **Clock skew** - Different server times
- [ ] **Timeout edge cases** - Request times out mid-operation

---

## Flaky Test Prevention

### Test Isolation

- [ ] **No shared state** - Tests don't depend on other tests
- [ ] **Database cleanup** - Each test starts clean
- [ ] **No global mocks** - Mocks scoped to individual tests
- [ ] **Deterministic order** - Tests pass in any order

### Timing Reliability

- [ ] **No real delays** - Don't use `sleep()` or real timers
- [ ] **Mock time** - Use fake timers for time-dependent logic
- [ ] **Async handling** - Proper await/promise handling
- [ ] **Retry not needed** - Tests don't need retry to pass

### External Dependencies

- [ ] **No network calls** - External services mocked
- [ ] **No file system** - Or uses temp directories
- [ ] **No environment dependency** - Works on any machine
- [ ] **Seeded randomness** - Random values are reproducible

---

## Missing Invariants

### Business Invariants

- [ ] **Balance never negative** - Account balances, inventory counts
- [ ] **Total matches sum** - Aggregates match detail records
- [ ] **Unique constraints** - No duplicate IDs, emails, etc.
- [ ] **Foreign key integrity** - References point to existing records
- [ ] **State consistency** - Related fields stay in sync

### Security Invariants

- [ ] **No unauthorized access** - Every endpoint checked
- [ ] **No data leakage** - Sensitive data not exposed
- [ ] **Audit trail complete** - All changes logged
- [ ] **Encryption applied** - Sensitive data encrypted

### System Invariants

- [ ] **Idempotency** - Duplicate requests safe
- [ ] **Ordering preserved** - Where order matters
- [ ] **No data loss** - Operations don't lose data
- [ ] **Recovery works** - Can recover from any state

---

## Contract Tests (Service-to-Service)

### API Contracts

- [ ] **Request schema** - All required fields present
- [ ] **Response schema** - Response matches expected shape
- [ ] **Status codes** - Correct codes for each scenario
- [ ] **Error format** - Errors follow contract
- [ ] **Versioning** - Version compatibility tested

### Event Contracts

- [ ] **Event schema** - Events match expected format
- [ ] **Required fields** - All required fields present
- [ ] **Event ordering** - Order assumptions tested
- [ ] **Idempotency** - Duplicate events handled

### Database Contracts

- [ ] **Schema compatibility** - Queries work with schema
- [ ] **Migration tested** - Up and down migrations work
- [ ] **Data format** - Data stored in expected format

---

## Frontend Regression Protection

### Component Tests

- [ ] **Render correctly** - Components render without error
- [ ] **Props handling** - All prop combinations work
- [ ] **User interactions** - Click, input, submit work
- [ ] **Loading states** - Loading UI displayed correctly
- [ ] **Error states** - Error UI displayed correctly
- [ ] **Empty states** - Empty UI displayed correctly

### Integration Tests

- [ ] **Page navigation** - Routes work correctly
- [ ] **Form submission** - Forms submit and validate
- [ ] **API integration** - Data fetched and displayed
- [ ] **State management** - State updates correctly

### Visual Regression

- [ ] **Screenshot tests** - Key screens captured
- [ ] **Responsive layouts** - Different screen sizes tested
- [ ] **Theme variants** - Light/dark mode tested

### Accessibility Tests

- [ ] **Keyboard navigation** - All interactive elements reachable
- [ ] **Screen reader** - Proper ARIA labels
- [ ] **Color contrast** - Meets WCAG standards

---

## Smart Contract Coverage

### Functional Tests

- [ ] **All functions tested** - Every public function
- [ ] **Access control** - Only authorized callers succeed
- [ ] **State changes** - State updated correctly
- [ ] **Events emitted** - Correct events with correct data
- [ ] **Return values** - Functions return expected values

### Security Tests

- [ ] **Reentrancy** - Reentrancy attacks fail
- [ ] **Integer overflow** - Overflow/underflow handled
- [ ] **Access control bypass** - No privilege escalation
- [ ] **Front-running** - MEV attacks mitigated
- [ ] **Oracle manipulation** - Price manipulation handled

### Invariant Tests

- [ ] **Total supply invariant** - Tokens can't be created from nothing
- [ ] **Balance invariant** - Sum of balances equals total
- [ ] **State machine invariant** - Only valid state transitions
- [ ] **Time-lock invariant** - Timelocks can't be bypassed

### Fuzz Testing

- [ ] **Random inputs** - Functions handle random valid inputs
- [ ] **Random sequences** - Random call sequences don't break invariants
- [ ] **Property-based** - Key properties hold for all inputs
- [ ] **Stateful fuzzing** - System invariants hold across operations

---

## Test Quality Signals

### Green Flags ✅

- Tests fail when code is broken
- Tests are readable and maintainable
- Test names describe behavior, not implementation
- Setup/teardown is minimal and clear
- Assertions are specific and meaningful

### Red Flags 🚩

- Tests only pass because they're skipped
- Tests require specific timing to pass
- Tests have no assertions
- Tests mock everything
- Tests test implementation details
- Tests are copy-pasted with minor changes
- Tests take minutes to run
- Tests require manual setup

---

## Severity Classification

| Gap Type | Severity | Action |
|----------|----------|--------|
| Critical path untested | CRITICAL | Block release |
| Failure case not tested | HIGH | Fix this sprint |
| Edge case not covered | MEDIUM | Add to backlog |
| Flaky test exists | HIGH | Fix or delete |
| False confidence test | MEDIUM | Rewrite |
| Missing contract test | HIGH | Add before integration |
| No invariant tests | MEDIUM | Add for critical logic |
