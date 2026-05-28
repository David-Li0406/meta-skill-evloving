# Execution Phases

Detailed instructions for each phase of the build-update-tests workflow.

## Phase 1: Code Analysis & Risk Assessment

**Objective**: Understand what needs to be tested and assess risk level

### Step 1.1: Read and Analyze Target File

Identify file type:
- React component (.tsx)
- React hook (use*.ts)
- Service (.service.ts)
- Utility function (.ts in utils/)
- Page component (pages/*.tsx)
- API route handler

Analyze complexity indicators:
- Lines of code
- Dependencies (imports, hooks, contexts, services)

For React components:
- Props interface and types
- State management (useState, useForm, etc.)
- User interactions (buttons, forms, inputs, checkboxes)
- Conditional rendering logic
- Side effects (useEffect, callbacks)

For services:
- Function signatures and return types
- External API calls
- Error handling patterns
- Data mutations (create/update/delete)

For utilities:
- Pure functions vs impure functions
- Input/output contracts

### Step 1.2: Apply Risk Matrix

| Risk Level | Characteristics | Required Tests |
|------------|-----------------|----------------|
| **High** | Complex business logic, data mutations, user-facing forms, auth, payments, email automation, multi-step workflows | Unit + Integration + E2E |
| **Medium** | Data fetching/display, filtering/search, validation logic, data transformations, hooks with side effects | Unit + Integration OR Unit + E2E |
| **Low** | Pure utility functions, simple formatters, type guards, constants/enums, display-only components | Unit only |

### Step 1.3: Identify Critical Paths

- Main user flows (P0)
- Edge cases (P1)
- Error scenarios (P0 for critical, P1 for others)
- State transitions
- Integration points

### Step 1.4: Check Requirements Documentation

If user provided requirements doc:
- Read it
- Extract must-test scenarios
- Map requirements to code sections

### Step 1.5: Required Test Levels Matrix

| Code Type | Complexity | Required Tests |
|-----------|-----------|----------------|
| User-facing component | Any | Unit + E2E |
| Form component | Any | Unit + E2E |
| Service with mutations | Any | Unit + Integration + E2E |
| Service read-only | Simple | Unit |
| Service read-only | Complex | Unit + Integration |
| Pure utility | Any | Unit |
| React hook | Simple | Unit |
| React hook | Complex | Unit + Integration |
| Page component | Any | E2E |

---

## Phase 2: Existing Test Discovery & Pattern Compliance

**Objective**: Find all existing tests and validate pattern compliance

### Step 2.1: Search for Test Files

**Unit tests**:
- Pattern: `src/**/__tests__/[filename].test.{ts,tsx}`
- Pattern: `src/**/[filename].test.{ts,tsx}`

**Integration tests**:
- Pattern: `src/**/*.integration.test.{ts,tsx}`

**E2E tests**:
- Pattern: `playwright/tests/*.spec.ts`

### Step 2.2: Analyze Existing Tests

If tests exist:
- Count existing test cases
- Identify coverage: rendering, interaction, state change, edge cases, error handling
- Document test file locations

### Step 2.3: Pattern Compliance Check (CRITICAL)

Read relevant pattern documentation:
- `claude-patterns/testing-patterns.md` (React component unit tests)
- `claude-patterns/vitest-testing-patterns.md` (Service/utility unit tests)
- `claude-patterns/playwright-best-practices.md` (E2E tests)

**Unit Test Patterns**:

Pattern #1 - Async elements:
```typescript
// GOOD
const element = await screen.findByText('Success');

// BAD
const element = screen.getByText('Success'); // May not exist yet
```

Pattern #2 - Await userEvent:
```typescript
// GOOD
await userEvent.type(input, 'text');
await userEvent.click(button);

// BAD
userEvent.type(input, 'text'); // Missing await
```

Pattern #3 - Behavior over implementation:
```typescript
// GOOD
expect(screen.getByText('Welcome John')).toBeInTheDocument();

// BAD
expect(component.state.name).toBe('John'); // Implementation detail
```

**E2E Test Patterns**:

Pattern #1 - ONE test per user journey:
```typescript
// GOOD: One comprehensive test
test('complete contact workflow', async ({ page }) => {
  await test.step('Add contact', ...);
  await test.step('Verify automation', ...);
});

// BAD: Split interdependent steps
test('1. add contact', ...);
test('2. verify automation', ...); // Depends on test 1
```

Pattern #2 - Real services, NOT direct INSERTs:
```typescript
// GOOD
const session = await sessionsService.createSession({ ... });

// BAD: Direct database bypass
await supabase.from('sessions').insert({ ... });
```

Pattern #3 - Wait for automation worker
Pattern #4 - Worker health check present
Pattern #5 - Cleanup in finally blocks

### Step 2.4: Create Gap Analysis

Document:
- What's Tested (checkmarks)
- What's Missing (with priority)
- Pattern Violations (with references)
- What Needs Improvement

---

## Phase 3: Test Design

**Objective**: Plan the test structure

### Step 3.1: Review Project Conventions

Search for 2-3 existing test files to understand:
- Test file structure
- Mock patterns
- Helper utilities (custom render functions)
- Assertion style

### Step 3.2: Design Test Structure

```typescript
describe('[ComponentName/ModuleName]', () => {
  // Setup section
  const mockData = ...;
  const renderComponent = () => ...;

  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('[Feature Area 1]', () => {
    it('test case 1');
    it('test case 2');
  });

  describe('[Feature Area 2]', () => {
    it('test case 3');
  });
});
```

### Step 3.3: Plan Test Cases by Priority

**P0 Critical** (must have):
- Happy path for main functionality
- Critical user flows
- Data integrity (forms submit correct data)

**P1 Important** (should have):
- Edge cases
- Error handling
- Conditional logic branches

**P2 Nice-to-Have**:
- Accessibility
- Performance
- Rarely-used features

### Step 3.4: Identify Mock Requirements

- External services/APIs
- React hooks (useAuth, useQuery, custom hooks)
- Context providers
- Third-party libraries
- Browser APIs (localStorage, fetch)

---

## Phase 4: Test Implementation

**Objective**: Write or update test code

### If NO Tests Exist

1. Create new test file at appropriate location
2. Set up test infrastructure:
   - Imports (testing-library, vitest, etc.)
   - Mock declarations
   - Helper functions (render wrappers, etc.)
3. Implement P0 tests first
4. Add P1 tests
5. Add P2 tests if applicable

### If Tests EXIST But Incomplete

1. Preserve existing working tests
2. Add missing test cases
3. Improve existing tests if needed:
   - Add missing assertions
   - Fix improper mocks
   - Update for current code structure

### Best Practices

**Arrange-Act-Assert pattern**:
```typescript
it('submits form with correct data', async () => {
  // Arrange
  const mockSubmit = vi.fn();
  render(<MyForm onSubmit={mockSubmit} />);

  // Act
  await userEvent.type(screen.getByLabelText('Name'), 'John');
  await userEvent.click(screen.getByRole('button', { name: 'Submit' }));

  // Assert
  expect(mockSubmit).toHaveBeenCalledWith({ name: 'John' });
});
```

**Test behavior, not implementation**:
- Use accessible queries (getByRole, getByLabelText)
- Focus on user-visible outcomes
- Avoid testing internal state directly

**Comprehensive assertions**:
- Don't just check element exists
- Verify correct content, attributes, behavior
- Test negative cases (element NOT present)

**Proper async handling**:
- Use `waitFor` for async operations
- Use `findBy` queries for async elements
- Properly await user interactions with userEvent

**Mock external dependencies**:
```typescript
vi.mock('@/hooks/useAuth');
vi.mock('@/hooks/useQuery');

beforeEach(() => {
  vi.mocked(useAuth).mockReturnValue({
    user: { id: '1', email: 'test@example.com' }
  });
});
```

---

## Phase 5: Validation

**Objective**: Ensure tests work correctly

### Step 5.1: Run Tests

```bash
npm run test:unit -- [test-file-name]
```

### Step 5.2: Handle Failures

If tests FAIL, analyze error messages. Determine cause:
- Incorrect test code → Fix test
- Bug in source code → Report to user
- Missing mock → Add mock

Fix and re-run until all tests pass.

### Step 5.3: Verify Stability

If tests PASS:
- Run in watch mode to verify stability
- Check for any console warnings
- Ensure no flaky tests (run multiple times if needed)

---

## Phase 6: Reporting

**Objective**: Document evaluation findings and implementation results

Use the report template from [references/report-template.md](report-template.md) to provide a comprehensive summary including:
- Evaluation phase findings (risk, gaps, violations)
- Implementation phase results (tests created/updated)
- Validation results
- Recommendations
