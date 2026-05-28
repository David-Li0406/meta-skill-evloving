---
name: [PROJECT]-testing-strategies
description: [PROJECT] testing patterns and quality assurance strategies
globs: ["**/*.{test,spec}.{ts,js,java,py,rb}", "**/test/**/*", "**/tests/**/*"]
---

# Testing Strategies

> **Template for project-specific testing strategies skill**
> Fill in [CUSTOMIZE] sections with your project's testing stack and patterns

**Project**: [PROJECT NAME]
**Last Updated**: [DATE]

---

## Testing Philosophy

**Coverage Target**: [CUSTOMIZE: 80% / 85% / 90%]

**Testing Pyramid**:
```
[CUSTOMIZE: Adjust ratios for your project]

        /\
       /E2E\      <- [5-10%] Critical flows
      /------\
     /Integr.\   <- [20%] API endpoints, DB
    /----------\
   /   Unit     \ <- [70%] Functions, components
  /--------------\
```

---

## Unit Testing (Backend)

### Framework

**Test Framework**: [CUSTOMIZE: JUnit 5 / Jest / Pytest / RSpec / Go testing]

**Mocking Library**: [CUSTOMIZE: Mockito / sinon / unittest.mock / RSpec mocks / gomock]

**Assertion Library**: [CUSTOMIZE: JUnit assertions / expect / assert / should]

### Test Structure

**Pattern**: [CUSTOMIZE: AAA / Given-When-Then / Arrange-Act-Assert]

**Example - Service Test**:
```[language]
[CUSTOMIZE: Show service unit test pattern]

Examples:
- JUnit 5:
  @Test
  void getUserById_ExistingId_ReturnsUser() {
    // Arrange
    when(repository.findById(1L)).thenReturn(Optional.of(user));
    // Act
    UserDTO result = service.getUserById(1L);
    // Assert
    assertEquals("John", result.name());
  }

- Jest:
  it('getUserById returns user when exists', async () => {
    repository.findById.mockResolvedValue(user)
    const result = await service.getUserById(1)
    expect(result.name).toBe('John')
  })
```

### What to Test

**Service Layer**:
- [ ] Happy path (successful operations)
- [ ] Error cases (not found, validation errors)
- [ ] Business rule validations
- [ ] Edge cases (null, empty, boundary values)
- [ ] [PROJECT-SPECIFIC REQUIREMENT]

**Repository Layer**:
- [ ] Custom query methods
- [ ] [Only if complex logic, otherwise integration test]

---

## Unit Testing (Frontend)

### Framework

**Test Framework**: [CUSTOMIZE: Jest / Vitest / Jasmine/Karma]

**Component Testing**: [CUSTOMIZE: React Testing Library / Angular Testing Library / Vue Test Utils]

**User Interaction**: [CUSTOMIZE: @testing-library/user-event / Jasmine click() / @testing-library/vue]

### Test Pattern

**Philosophy**: [CUSTOMIZE: Test user behavior / Test implementation / Test contracts]

**Example - Component Test**:
```[language]
[CUSTOMIZE: Show component test pattern]

Examples:
- React Testing Library:
  it('renders user list and handles click', async () => {
    render(<UserList users={mockUsers} onSelect={mockFn} />)
    await userEvent.click(screen.getByText('John'))
    expect(mockFn).toHaveBeenCalledWith(mockUsers[0])
  })
```

### What to Test

**Components**:
- [ ] Renders with props
- [ ] Loading state displays
- [ ] Error state displays
- [ ] Empty state displays
- [ ] User interactions (clicks, typing, navigation)
- [ ] Callbacks invoked correctly
- [ ] [PROJECT-SPECIFIC REQUIREMENT]

---

## Integration Testing

### Backend Integration Tests

**Framework**: [CUSTOMIZE: Spring Test / Supertest / TestClient / request specs]

**Database**: [CUSTOMIZE: TestContainers / In-memory H2 / Rollback / Test database]

**Example - API Endpoint Test**:
```[language]
[CUSTOMIZE: Show API integration test]

Examples:
- Spring Boot:
  @Test
  void createUser_ValidData_Returns201() {
    ResponseEntity<UserDTO> response = restTemplate.postForEntity(
      "/api/users", request, UserDTO.class
    );
    assertEquals(HttpStatus.CREATED, response.getStatusCode());
  }

- Supertest:
  it('POST /api/users creates user', async () => {
    const res = await request(app).post('/api/users').send(data)
    expect(res.status).toBe(201)
  })
```

### What to Test

**API Endpoints**:
- [ ] All CRUD operations (GET, POST, PUT, DELETE)
- [ ] Success cases (200, 201, 204)
- [ ] Error cases (400, 404, 409, 500)
- [ ] Validation errors
- [ ] Authentication/Authorization (if applicable)
- [ ] [PROJECT-SPECIFIC ENDPOINT]

---

## E2E Testing

### Framework

**E2E Framework**: [CUSTOMIZE: Playwright / Cypress / Selenium / Puppeteer]

**Browser Coverage**: [CUSTOMIZE: Chrome / Chrome + Firefox + Safari / Chrome only]

### Test Pattern

**Organization**: [CUSTOMIZE: Page Object Model / Direct interaction / Custom abstraction]

**Example - E2E Test**:
```[language]
[CUSTOMIZE: Show E2E test pattern]

Examples:
- Playwright:
  test('user can create account', async ({ page }) => {
    await page.goto('/signup')
    await page.fill('[name="email"]', 'test@example.com')
    await page.fill('[name="password"]', 'password123')
    await page.click('button:has-text("Sign Up")')
    await expect(page.locator('text=Welcome')).toBeVisible()
  })
```

### Critical Flows

**[CUSTOMIZE - LIST PROJECT CRITICAL FLOWS]**

1. **[Flow Name]**: [Description]
   - Start: [Where user starts]
   - Actions: [Key steps]
   - Success: [Expected result]

2. **[Flow Name]**: [Description]

---

## Test Data Management

### Fixtures / Seeds

**Location**: [CUSTOMIZE: src/test/resources / tests/fixtures / test/fixtures]

**Format**: [CUSTOMIZE: JSON / YAML / SQL / Code]

**Example**:
```[format]
[CUSTOMIZE: Show test data structure]
```

### Database State

**Strategy**: [CUSTOMIZE: Rollback / Clean + Seed / Snapshot + Restore]

**Example**:
```[language]
[CUSTOMIZE: Show database setup/teardown]
```

---

## Mocking Strategy

### When to Mock

**[CUSTOMIZE WITH PROJECT GUIDELINES]**

**Always Mock**:
- [ ] External APIs (third-party services)
- [ ] File system operations
- [ ] Time-dependent functions
- [ ] [PROJECT-SPECIFIC]

**Never Mock** (use real):
- [ ] Internal services (integration test)
- [ ] Database (use test database)
- [ ] [PROJECT-SPECIFIC]

### Mock Patterns

**Backend**:
```[language]
[CUSTOMIZE: Show mocking pattern]

Examples:
- Mockito: when(service.getUser()).thenReturn(user)
- Jest: service.getUser = jest.fn().mockResolvedValue(user)
```

**Frontend API Mocking**:
```[language]
[CUSTOMIZE: MSW / nock / HttpClientTestingModule / fetch-mock]
```

---

## Coverage Requirements

### Targets

**Overall**: [CUSTOMIZE: 80% / 85% / 90%]

**Per Component Type**:
- Services/Business Logic: [CUSTOMIZE: 90%+]
- Controllers/Routes: [CUSTOMIZE: 80%+]
- Components: [CUSTOMIZE: 80%+]
- Utils: [CUSTOMIZE: 90%+]

### What NOT to Cover

**[CUSTOMIZE - AREAS TO SKIP]**

Skip coverage for:
- [ ] Generated code (if any)
- [ ] Third-party integrations (mock instead)
- [ ] Simple getters/setters (if trivial)
- [ ] [PROJECT-SPECIFIC SKIP]

---

## Test Execution

### Commands

**Backend Unit Tests**:
```bash
[CUSTOMIZE: mvn test / npm test / pytest / rspec / go test]
```

**Frontend Unit Tests**:
```bash
[CUSTOMIZE: npm test / ng test / vitest]
```

**Integration Tests**:
```bash
[CUSTOMIZE: mvn verify / npm run test:integration / pytest tests/integration]
```

**E2E Tests**:
```bash
[CUSTOMIZE: npx playwright test / npm run e2e / cypress run]
```

**Coverage Report**:
```bash
[CUSTOMIZE: mvn jacoco:report / npm run test:coverage / pytest --cov]
```

---

## Quality Gates

**[CUSTOMIZE WITH PROJECT GATES]**

Before deployment:
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] All E2E tests pass (critical flows)
- [ ] Coverage >= [80]%
- [ ] Build succeeds
- [ ] No linting errors
- [ ] [PROJECT-SPECIFIC GATE]

---

## CI/CD Integration

### Test Execution in Pipeline

**Where Tests Run**: [CUSTOMIZE: GitHub Actions / GitLab CI / Jenkins]

**Parallelization**:
```yaml
[CUSTOMIZE: Show how tests run in parallel in CI]

Example:
jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps: [...]
  frontend-tests:
    runs-on: ubuntu-latest
    steps: [...]
```

### Failure Handling

**Strategy**: [CUSTOMIZE: Fail fast / Retry / Notify]

---

## Project-Specific Testing Patterns

**[CUSTOMIZE - ADD DETECTED OR CHOSEN PATTERNS]**

### Flaky Test Handling
- [CUSTOMIZE: Retry policy / Investigation process]

### Test Performance
- [CUSTOMIZE: Timeout thresholds / Parallel execution]

### Custom Assertions
- [CUSTOMIZE: Project-specific assertions or matchers]

---

**Customization Complete**: Replace all [CUSTOMIZE] sections with project-detected or chosen patterns.

**Auto-generated by**: `/add-skill testing-strategies` command
