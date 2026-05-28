# Step 3: Test Planning

**Duration**: ~2 minutes
**Purpose**: Generate comprehensive test plan with scenarios.

---

## Actions

### 1. Analyze Requirements

Spawn test-planner agent to analyze:
- Feature requirements from ticket
- Acceptance criteria
- Edge cases and error scenarios
- Test data requirements

### 2. Determine Playwright Project

| Project Type | Workers | Use Case |
|--------------|---------|----------|
| **Serial** | 1 | Shared state, authentication flows |
| **Parallel** | 4 | Independent tests, data-isolated |

**Decision Criteria**:
- Tests share user state → Serial
- Tests modify shared data → Serial
- Tests are completely independent → Parallel

### 3. Generate Test Scenarios

#### Happy Path Scenarios
```markdown
- User can complete primary action successfully
- Expected UI feedback is displayed
- Data is persisted correctly
```

#### Edge Cases
```markdown
- Empty/null input handling
- Boundary values (max length, special characters)
- Concurrent user actions
```

#### Error Handling
```markdown
- API failure responses (500, 502)
- Network timeout scenarios
- Invalid session/authentication
```

---

## Output

Generate test plan: `docs/test-plans/{ticket-id}-test-plan.md`

**Document Structure**:
```markdown
# Test Plan: {TICKET-ID}

## Overview
- **Feature**: {feature name}
- **Test Type**: {E2E UI|API Integration}
- **Project**: {serial|parallel}
- **Estimated Tests**: {count}

## Prerequisites
- [ ] Test user accounts available
- [ ] Test data seeded
- [ ] API endpoints accessible

## Test Scenarios

### Happy Path
| ID | Scenario | Priority |
|----|----------|----------|
| HP-1 | User can login successfully | P0 |
| HP-2 | User can complete checkout | P0 |

### Edge Cases
| ID | Scenario | Priority |
|----|----------|----------|
| EC-1 | Empty form submission | P1 |
| EC-2 | Special characters in input | P2 |

### Error Handling
| ID | Scenario | Priority |
|----|----------|----------|
| EH-1 | API returns 500 error | P1 |
| EH-2 | Network timeout | P2 |

## Test Data Requirements
- Test buyer account: `buyer@test.com`
- Test seller account: `seller@test.com`
- Mock case data: See `fixtures/cases.json`

## Dependencies
- Linear MCP for ticket details
- Existing page objects: {list}
- Helper utilities: {list}
```

---

## Scenario Prioritization

| Priority | Description | Coverage Target |
|----------|-------------|-----------------|
| **P0** | Critical path, must pass | 100% |
| **P1** | Important edge cases | 80% |
| **P2** | Nice-to-have coverage | Best effort |

---

## Test Data Strategy

### Approach 1: Fixture-Based
```typescript
// Use static fixtures
import { testCases } from '../fixtures/cases.json'
```

### Approach 2: API-Generated
```typescript
// Create data via API before tests
test.beforeAll(async () => {
  await createTestCase({ title: 'Test Case', ... })
})
```

### Approach 3: UI-Generated
```typescript
// Create data through UI in setup
test.beforeAll(async ({ page }) => {
  await createCaseViaUI(page, testData)
})
```

**Preference**: Fixture-based > API-generated > UI-generated
