---
name: test-design
version: 1.0.0
description: Use to design test strategies and create test specifications. Documents testing approaches for stories.
---
<!-- Powered by PRISMâ„¢ Core -->

# test-design

Create comprehensive E2E integration test scenarios with complete user journey validation for story implementation.

## When to Use

- When designing test strategy for a new story
- Before implementing tests to plan coverage
- When documenting test specifications for QA
- When applying test level framework decisions

## Quick Start

1. Analyze story requirements and acceptance criteria
2. Apply test level framework (integration primary, unit supporting)
3. Assign priorities using test priorities matrix
4. Create test scenarios with Given-When-Then documentation
5. Generate test specification document

## Inputs

```yaml
required:
  - story_id: '{epic}.{story}' # e.g., "1.3"
  - story_path: '{devStoryLocation}/{epic}.{story}.*.md' # Path from core-config.yaml
  - story_title: '{title}' # If missing, derive from story file H1
  - story_slug: '{slug}' # If missing, derive from title (lowercase, hyphenated)
```

## Purpose

Design a comprehensive E2E integration test strategy that validates complete user journeys and system interactions. Primary focus on integration tests using WebApplicationFactory patterns with containerized dependencies to ensure realistic production-like scenarios while maintaining fast feedback loops.

## Dependencies

```yaml
data:
  - test-levels-framework.md # Unit/Integration/E2E decision criteria
  - test-priorities-matrix.md # P0/P1/P2/P3 classification system
```

## Process

### 1. Analyze Story Requirements

Break down each acceptance criterion into testable scenarios. For each AC:

- Identify the core functionality to test
- Determine data variations needed
- Consider error conditions
- Note edge cases

### 2. Apply Test Level Framework

**Reference:** Load `test-levels-framework.md` for detailed criteria

**Primary Strategy - E2E Integration Tests:**

- **Integration (Primary)**: Complete user journeys with WebApplicationFactory, real database connections via Testcontainers, API endpoints with authentication flows
- **Unit (Supporting)**: Pure logic, calculations, validation rules - only when business logic is complex enough to warrant isolation
- **E2E (Selective)**: Browser-based tests for critical UI workflows - sparingly used due to maintenance overhead

### 3. Assign Priorities

**Reference:** Load `test-priorities-matrix.md` for classification

Quick priority assignment:

- **P0**: Revenue-critical, security, compliance
- **P1**: Core user journeys, frequently used
- **P2**: Secondary features, admin functions
- **P3**: Nice-to-have, rarely used

### 4. Design E2E Integration Test Scenarios

For each identified test need, create comprehensive integration scenarios:

```yaml
test_scenario:
  id: '{epic}.{story}-{LEVEL}-{SEQ}'
  requirement: 'AC reference'
  priority: P0|P1|P2|P3
  level: unit|integration|e2e
  description: 'Complete user journey being tested'
  justification: 'Why this level provides optimal coverage'
  test_pattern: 'WebApplicationFactory|TestContainers|Fixture-based'
  authentication: 'Bearer token|Keycloak|Anonymous'
  database_state: 'Required test data setup'
  api_endpoints: ['endpoints covered in journey']
  arrange_act_assert: 'Clear AAA structure with Shouldly assertions'
  mitigates_risks: ['RISK-001'] # If risk profile exists
```

**Integration Test Design Patterns:**

- **WebApplicationFactory**: Primary test harness for API testing with full application bootstrap
- **Test Fixtures**: Shared resource management (DatabaseFixture, SmtpFixture) via ICollectionFixture
- **Testcontainers**: Real database dependencies (MSSQL) for realistic data operations  
- **Authentication Flows**: Bearer token patterns with test data seeding
- **Arrange-Act-Assert**: Clear structure with Shouldly assertions for readable test validation
- **JSON Serialization**: Consistent patterns for request/response handling

### 5. Validate Integration Coverage

Ensure comprehensive E2E integration coverage:

- Every AC has at least one integration test covering the complete user journey
- Critical authentication flows are validated with real token handling
- Database operations tested against containerized dependencies
- API endpoint interactions verified end-to-end
- Error scenarios include proper HTTP status code validation
- Happy path and edge cases covered within the same integration context
- Test fixtures properly isolate test data while sharing expensive resources

## Outputs

### Output 1: Test Design Document

**Save to:** `qa.qaLocation/assessments/{epic}.{story}-test-design-{YYYYMMDD}.md`

```markdown
# E2E Integration Test Design: Story {epic}.{story}

Date: {date}
Designer: Quinn (Test Architect)

## Test Strategy Overview

- **Primary Approach**: E2E Integration tests with WebApplicationFactory
- **Test Infrastructure**: Testcontainers (MSSQL) + Fixture-based resource sharing
- **Authentication**: Bearer token flows with seeded test data
- **Assertion Framework**: Shouldly for readable validation
- Total test scenarios: X
- Integration tests: Z (85%+ target)
- Unit tests: Y (10-15% for complex business logic only)
- Browser E2E tests: W (<5% for critical UI flows)
- Priority distribution: P0: X, P1: Y, P2: Z

## Integration Test Scenarios by Acceptance Criteria

### AC1: {description}

#### Test Scenarios

| ID           | Level       | Priority | User Journey                           | Test Pattern              | Endpoints Covered           |
| ------------ | ----------- | -------- | -------------------------------------- | ------------------------- | --------------------------- |
| 1.3-INT-001  | Integration | P0       | User authenticates and {core action}   | WebApplicationFactory     | /api/auth, /api/{resource}  |
| 1.3-INT-002  | Integration | P0       | System validates {business rules}      | DatabaseFixture + TestDB  | /api/{validation-endpoint}  |
| 1.3-INT-003  | Integration | P1       | Error handling for {edge case}        | Full container stack      | /api/{resource}             |

#### Test Implementation Pattern

```csharp
[Collection(nameof(DefaultWebApplicationCollection))]
public class {FeatureEndpointTests}
{
    private readonly ActionsApiFactory application;
    
    public {FeatureEndpointTests}(DatabaseFixture db, SmtpFixture smtp, ITestOutputHelper output)
    {
        application = new ActionsApiFactory(db, smtp, output);
        application.InitializeAuthentication();
    }
    
    [Fact]
    public async Task {UserJourney}_ShouldReturn_{ExpectedOutcome}()
    {
        // Arrange - Setup user context and test data
        var client = application.GetHttpClient();
        var bearerToken = await application.GetJwtBearerToken();
        client.DefaultRequestHeaders.Authorization = 
            new AuthenticationHeaderValue("Bearer", bearerToken);
        var requestData = new { /* test specific data */ };
        
        // Act - Execute the complete user journey
        using var response = await client.PostAsync("/api/{endpoint}", 
            CreateJsonContent(requestData));
        var result = (await response.Content.ReadAsStringAsync())
            .Deserialize<{ResponseType}>();
        
        // Assert - Validate complete response with Shouldly
        response.StatusCode.ShouldBe(HttpStatusCode.OK);
        result.ShouldNotBeNull();
        result.{Property}.ShouldBe({ExpectedValue});
    }
}
```

[Continue for all ACs...]

## Test Infrastructure Setup

**Required Fixtures:**
- `DatabaseFixture`: MSSQL Testcontainer with master/tenant databases
- `SmtpFixture`: Email testing infrastructure  
- `DefaultWebApplicationCollection`: Shared fixture orchestration

**Authentication Flow:**
- Keycloak integration for realistic token validation
- Seeded test data in both master and tenant databases
- Bearer token patterns matching production authentication

## Risk Coverage

[Map integration test scenarios to identified risks - each scenario validates complete workflows]

## Recommended Execution Strategy

1. **P0 Integration tests** (primary coverage - complete user journeys)
2. **P0 Unit tests** (complex business logic only)
3. **P1 Integration tests** (secondary workflows) 
4. **P2+ Integration tests** (edge cases and admin scenarios)
5. **Browser E2E tests** (critical UI flows - minimal set)
```

### Output 2: Gate YAML Block

Generate for inclusion in quality gate:

```yaml
integration_test_design:
  primary_strategy: "E2E Integration with WebApplicationFactory"
  test_infrastructure: 
    - "Testcontainers (MSSQL)"
    - "DatabaseFixture + SmtpFixture"
    - "Bearer token authentication"
  scenarios_total: X
  by_level:
    integration: Z # 85%+ target - primary coverage
    unit: Y # 10-15% - complex business logic only
    browser_e2e: W # <5% - critical UI flows only
  by_priority:
    p0: A # Integration-first with containerized dependencies
    p1: B # Complete user journeys with real authentication
    p2: C # Edge cases within integration context
  test_patterns:
    - "WebApplicationFactory bootstrap"
    - "Arrange-Act-Assert with Shouldly assertions"
    - "JSON serialization patterns"
    - "Real database operations via Testcontainers"
  coverage_gaps: [] # List any ACs without integration test coverage
```

### Output 3: Trace References

Print for use by trace-requirements task:

```text
E2E Integration test design matrix: qa.qaLocation/assessments/{epic}.{story}-test-design-{YYYYMMDD}.md
P0 integration tests identified: {count}
WebApplicationFactory test harness configured: YES
Testcontainer dependencies: {database_fixtures}
Authentication flows covered: {auth_patterns}
```

## Quality Checklist

Before finalizing E2E integration test design, verify:

- [ ] Every AC has integration test coverage with complete user journey validation
- [ ] WebApplicationFactory pattern used as primary test harness
- [ ] Testcontainers configured for realistic database dependencies
- [ ] Authentication flows tested with Bearer tokens and seeded test data
- [ ] Test fixtures properly shared via ICollectionFixture pattern
- [ ] Arrange-Act-Assert structure with Shouldly assertions consistently applied
- [ ] JSON serialization/deserialization patterns implemented
- [ ] API endpoints tested end-to-end within user journey context
- [ ] Error scenarios include proper HTTP status code validation
- [ ] Database operations validated against containerized MSSQL instance
- [ ] Test scenarios are atomic but cover complete business workflows
- [ ] Unit tests only created for complex business logic requiring isolation
- [ ] Browser E2E tests minimized to critical UI flows only
- [ ] Priorities align with integration-first testing strategy

## Key Principles

- **Integration-first approach**: Prioritize E2E integration tests with WebApplicationFactory for maximum confidence in complete user journeys
- **Containerized realism**: Use Testcontainers for database dependencies to ensure production-like behavior while maintaining test isolation
- **Authentication-aware testing**: Validate complete authentication flows with Bearer tokens and real Keycloak integration
- **Fixture-based efficiency**: Share expensive resources (database containers, application factories) across test collections while maintaining data isolation
- **Risk-based coverage**: Focus integration tests on business-critical paths and error scenarios that matter to users
- **Readable assertions**: Use Shouldly for clear, descriptive test validation that serves as living documentation
- **Minimal unit testing**: Only create unit tests for complex business logic that benefits from isolation - avoid testing framework code or simple operations
- **Fast feedback through smart infrastructure**: Leverage test containers and fixtures for realistic but performant test execution

