# Phase 8: Test Development

## Objective

Write comprehensive tests before implementation using Test-Driven Development (TDD) approach.

## Step 1: Test Strategy Definition

```markdown
### Decision: Test Strategy

**Test Pyramid Distribution**:

```
            /\
           /  \      E2E Tests (10%)
          /----\     - Critical user journeys
         /      \    - Smoke tests
        /--------\   Integration Tests (20%)
       /          \  - API contracts
      /            \ - Database interactions
     /--------------\
    /                \ Unit Tests (70%)
   /                  \ - Business logic
  /____________________\ - Pure functions
```

| Level | Count Target | Focus | Tools |
|-------|--------------|-------|-------|
| Unit | ~70% | Business logic, utilities | [Jest/Pytest/etc.] |
| Integration | ~20% | API, Database, Services | [Supertest/etc.] |
| E2E | ~10% | User journeys | [Playwright/Cypress/etc.] |

**Test Naming Convention**:
```
[unit|integration|e2e]/[feature]/[component].[test|spec].{ext}
```
```

## Step 2: Unit Test Development

For each component/module:

```markdown
### Unit Tests: [Component Name]

**Path**: `tests/unit/[feature]/[component].test.{ext}`

**Test Cases from Requirements**:

| Requirement | Test Case | Input | Expected Output |
|-------------|-----------|-------|-----------------|
| [TR-001] | should create valid resource | valid input | resource object |
| [TR-001] | should reject invalid input | invalid input | validation error |
| [TR-002] | should calculate correctly | known values | expected result |
```

**Test Implementation Template**:
```typescript
describe('[ComponentName]', () => {
  // Setup
  let component: ComponentType;

  beforeEach(() => {
    // Fresh instance for each test
    component = createComponent(testConfig);
  });

  describe('[methodName]', () => {
    // Happy path
    it('should [expected behavior] when [condition]', () => {
      // Arrange
      const input = { /* test data */ };

      // Act
      const result = component.methodName(input);

      // Assert
      expect(result).toEqual(expectedOutput);
    });

    // Edge cases
    it('should handle empty input', () => {
      expect(() => component.methodName(null)).toThrow('Input required');
    });

    it('should handle boundary values', () => {
      const result = component.methodName(maxValue);
      expect(result).toBeDefined();
    });

    // Error cases
    it('should throw ValidationError for invalid input', () => {
      const invalidInput = { /* invalid data */ };
      expect(() => component.methodName(invalidInput))
        .toThrow(ValidationError);
    });
  });
});
```

### Unit Test Coverage Requirements

| Category | Minimum Coverage | Notes |
|----------|-----------------|-------|
| Business Logic | 90% | Core domain must be well tested |
| Utilities | 80% | Common functions |
| Models | 70% | Data transformations |
| Overall | 80% | Project-wide target |
```

## Step 3: Integration Test Development

```markdown
### Integration Tests: [API/Service Name]

**Path**: `tests/integration/[feature]/[endpoint].test.{ext}`

**Test Cases from Interface Contracts**:

| Contract | Test Case | Preconditions | Expected |
|----------|-----------|---------------|----------|
| POST /resources | should create resource | valid auth | 201 + resource |
| POST /resources | should reject unauthorized | no auth | 401 |
| GET /resources/:id | should return resource | exists | 200 + resource |
| GET /resources/:id | should return 404 | not exists | 404 |
```

**Integration Test Template**:
```typescript
describe('[API Feature] Integration', () => {
  let app: Application;
  let db: Database;

  beforeAll(async () => {
    // Start test database
    db = await createTestDatabase();
    // Start application
    app = await createApp({ database: db });
  });

  afterAll(async () => {
    await db.close();
    await app.close();
  });

  beforeEach(async () => {
    // Reset database state
    await db.reset();
  });

  describe('POST /api/v1/resources', () => {
    it('should create resource with valid input', async () => {
      // Arrange
      const input = { name: 'Test Resource' };
      const token = await getTestToken();

      // Act
      const response = await request(app)
        .post('/api/v1/resources')
        .set('Authorization', `Bearer ${token}`)
        .send(input);

      // Assert
      expect(response.status).toBe(201);
      expect(response.body).toMatchObject({
        id: expect.any(String),
        name: 'Test Resource',
        createdAt: expect.any(String)
      });

      // Verify side effects
      const saved = await db.resources.findById(response.body.id);
      expect(saved).toBeDefined();
    });

    it('should return 401 without authentication', async () => {
      const response = await request(app)
        .post('/api/v1/resources')
        .send({ name: 'Test' });

      expect(response.status).toBe(401);
      expect(response.body.code).toBe('UNAUTHORIZED');
    });
  });
});
```

### Contract Test Template (for API consumers)

```typescript
describe('[External Service] Contract', () => {
  it('should match expected response schema', async () => {
    const response = await client.getResource('id');

    expect(response).toMatchSchema({
      type: 'object',
      required: ['id', 'name', 'status'],
      properties: {
        id: { type: 'string' },
        name: { type: 'string' },
        status: { enum: ['active', 'inactive'] }
      }
    });
  });
});
```
```

## Step 4: End-to-End Test Development

```markdown
### E2E Tests: [User Journey]

**Path**: `tests/e2e/[journey].test.{ext}`

**Mapped from User Flows**:

| User Flow | E2E Test | Priority |
|-----------|----------|----------|
| [Flow 1: User Registration] | Complete registration flow | Critical |
| [Flow 2: Create Resource] | Create and view resource | Critical |
| [Flow 3: Error Recovery] | Handle and recover from error | High |
```

**E2E Test Template** (Web):
```typescript
describe('User Journey: [Journey Name]', () => {
  beforeEach(async () => {
    // Reset application state
    await resetTestData();
  });

  it('should complete [journey] successfully', async () => {
    // Step 1: Start at entry point
    await page.goto('/');
    await expect(page).toHaveTitle('App Name');

    // Step 2: Perform action
    await page.click('[data-testid="start-button"]');
    await page.fill('[data-testid="name-input"]', 'Test User');
    await page.click('[data-testid="submit-button"]');

    // Step 3: Verify result
    await expect(page.locator('[data-testid="success-message"]'))
      .toBeVisible();
    await expect(page).toHaveURL('/dashboard');

    // Step 4: Verify data persisted
    await page.reload();
    await expect(page.locator('[data-testid="user-name"]'))
      .toHaveText('Test User');
  });

  it('should handle errors gracefully', async () => {
    // Simulate error condition
    await mockApiError('/api/resource', 500);

    await page.goto('/create');
    await page.fill('[data-testid="name-input"]', 'Test');
    await page.click('[data-testid="submit-button"]');

    // Verify error handling
    await expect(page.locator('[data-testid="error-message"]'))
      .toBeVisible();
    await expect(page.locator('[data-testid="retry-button"]'))
      .toBeEnabled();
  });
});
```

**E2E Test Template** (CLI):
```typescript
describe('CLI Journey: [Journey Name]', () => {
  it('should complete [command flow] successfully', async () => {
    // Execute command
    const result = await exec('myapp create --name "Test"');

    // Verify output
    expect(result.exitCode).toBe(0);
    expect(result.stdout).toContain('Created successfully');

    // Verify effect
    const listResult = await exec('myapp list');
    expect(listResult.stdout).toContain('Test');
  });
});
```
```

## Step 5: Test Data Management

```markdown
### Test Data Strategy

**Factories/Fixtures**:
```typescript
// tests/factories/resource.factory.ts
export const resourceFactory = {
  build(overrides = {}): Resource {
    return {
      id: faker.string.uuid(),
      name: faker.commerce.productName(),
      status: 'active',
      createdAt: new Date(),
      ...overrides
    };
  },

  async create(db: Database, overrides = {}): Promise<Resource> {
    const resource = this.build(overrides);
    await db.resources.insert(resource);
    return resource;
  }
};
```

**Test Database Seeding**:
```typescript
// tests/seeds/index.ts
export async function seedTestData(db: Database) {
  // Create test users
  const users = await Promise.all([
    userFactory.create(db, { role: 'admin' }),
    userFactory.create(db, { role: 'user' })
  ]);

  // Create test resources
  await Promise.all([
    resourceFactory.create(db, { userId: users[0].id }),
    resourceFactory.create(db, { userId: users[1].id })
  ]);

  return { users };
}
```
```

## Step 6: Test Coverage Requirements

```markdown
### Coverage Targets

| Module | Line | Branch | Function | Rationale |
|--------|------|--------|----------|-----------|
| Core Domain | 90% | 85% | 95% | Critical business logic |
| API Handlers | 80% | 75% | 90% | Request handling |
| Utilities | 85% | 80% | 90% | Shared functions |
| Config | 70% | 70% | 80% | Configuration loading |

**Uncovered Code Justification**:
| File/Line | Reason Not Covered |
|-----------|-------------------|
| error-handler.ts:45 | Catastrophic failure path |
| logger.ts:12 | Third-party wrapper |
```

## Phase 8 Approval Gate

```markdown
## Phase 8 Summary: Test Development

### Test Coverage
| Level | Tests Written | Target | Status |
|-------|---------------|--------|--------|
| Unit | [X] | 70% of logic | [Met/Not Met] |
| Integration | [Y] | All endpoints | [Met/Not Met] |
| E2E | [Z] | Critical paths | [Met/Not Met] |

### Tests by Feature
| Feature | Unit | Integration | E2E |
|---------|------|-------------|-----|
| Auth | [X] | [Y] | [Z] |
| Users | [X] | [Y] | [Z] |

### Test Status
```
All tests: FAILING (expected - no implementation yet)
Test count: [N] tests
Coverage: 0% (scaffolding only)
```

### Test Data
- [ ] Factories created
- [ ] Fixtures defined
- [ ] Seed scripts ready

### Verified
- [ ] Test suite runs (all fail)
- [ ] Coverage reporting works
- [ ] CI runs tests

---

**Do you approve Phase 8? Ready to proceed to Implementation?**
```
