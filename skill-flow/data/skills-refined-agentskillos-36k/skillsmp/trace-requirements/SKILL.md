---
name: trace-requirements
description: Use to trace requirements through implementation. Maps acceptance criteria to code and tests.
---
<!-- Powered by PRISMâ„¢ Core -->

# trace-requirements

Map story requirements to E2E integration test cases for comprehensive end-to-end traceability and workflow validation.

## When to Use

- When mapping acceptance criteria to test cases
- During QA review to verify coverage
- When creating traceability matrix for stories
- When validating all requirements have tests

## Quick Start

1. Extract testable requirements from acceptance criteria
2. Map each requirement to E2E integration tests
3. Create traceability matrix with test file references
4. Calculate coverage percentage
5. Identify and document any coverage gaps

## Purpose

Create a requirements traceability matrix that ensures every acceptance criterion has corresponding E2E integration test coverage. This task prioritizes integration tests as the source of truth for requirement validation, ensuring complete workflow traceability from user input to system response.

**FOCUS**: E2E integration tests are the PRIMARY mechanism for requirements traceability. Unit tests supplement but integration tests validate complete requirement fulfillment.

**IMPORTANT**: Given-When-Then is used here for documenting the mapping between requirements and tests, NOT for writing the actual test code. Tests should follow your project's testing standards (no BDD syntax in test code).

## Prerequisites

- Story file with clear acceptance criteria
- Access to E2E integration test suite
- Understanding of complete system workflows
- Endpoint-to-test mapping documentation
- Multi-tenant and authentication requirements

## Traceability Process

### 1. Extract Requirements

Identify all testable requirements from:

- Acceptance Criteria (primary source for E2E validation)
- Complete user workflows and journeys
- API endpoint behaviors and responses
- Authentication/authorization requirements
- Multi-tenant isolation requirements
- Non-functional requirements (performance, security)
- Edge cases and error scenarios
- Integration touchpoints between components

### 2. Map to E2E Integration Tests

For each requirement, document E2E integration tests that validate complete workflows. Use Given-When-Then to describe what the test validates (not how it's written):

```yaml
requirement: 'AC1: User can authenticate and access tenant-specific resources'
test_mappings:
  # PRIMARY: E2E Integration Test (Source of Truth)
  - test_file: 'Integration.Tests/Endpoints/AuthEndpointTests.cs'
    test_case: 'RegisterComponent_ShouldReturn_Ok'
    endpoint: 'POST /api/Auth/registerComponent/{tenantId}'
    given: 'Valid tenant with master authentication token'
    when: 'Component registration request submitted'
    then: 'Returns OK with encrypted RemoteAccessToken for tenant isolation'
    coverage: e2e_integration
    auth_pattern: 'Bearer token with tenant context'
    multi_tenant: true

  # SUPPLEMENTAL: Validation scenarios
  - test_file: 'Integration.Tests/Endpoints/AuthEndpointTests.cs'  
    test_case: 'RegisterComponent_ShouldValidateRequest'
    test_attribute: '[Theory] with [InlineData] scenarios'
    given: 'Invalid tenant ID or missing parameters'
    when: 'Component registration attempted'
    then: 'Returns appropriate error messages and status codes'
    coverage: e2e_validation
    scenarios_tested: ['invalid_tenant', 'validation_errors']

requirement: 'AC2: Multi-tenant data isolation enforced'
test_mappings:
  # PRIMARY: Complete tenant lifecycle validation  
  - test_file: 'Integration.Tests/Endpoints/TenantEndpointTests.cs'
    test_case: 'CreateAndDeleteNewTenant_ShouldReturn_Ok'
    endpoint: 'POST /api/Tenant/createNewTenant, DELETE /api/Tenant/deleteTenant'
    given: 'Master authentication and tenant creation request'
    when: 'Complete tenant lifecycle executed (create, validate, delete)'
    then: 'Tenant created with isolated database, license validated, clean deletion'
    coverage: e2e_integration
    workflow_validation: 'Complete tenant management workflow'
    database_validation: 'Tenant-specific database connection verified'
    license_validation: 'Tenant license status compliance checked'
```

### 3. E2E Integration Coverage Analysis

Evaluate coverage for each requirement with emphasis on complete workflow validation:

**Coverage Levels (Priority Order):**

- `e2e_integration`: Complete end-to-end workflow tested with full system integration (HIGHEST PRIORITY)
- `e2e_validation`: Edge cases and validation scenarios covered in integration tests
- `integration_with_unit`: Integration tests backed by supporting unit tests
- `integration_only`: Covered in integration tests but lacks unit test support
- `unit_only`: Only unit tests exist - INSUFFICIENT for requirement validation
- `none`: No test coverage found - CRITICAL GAP

**E2E Integration Test Patterns:**

- **Endpoint Testing**: Direct API endpoint validation with realistic payloads
- **Authentication Flow**: Complete auth workflows with tenant context
- **Multi-Tenant Validation**: Tenant isolation and data segregation testing
- **Database Integration**: Real database operations and transaction validation
- **Service Integration**: Cross-service communication and dependency validation
- **Error Scenario Testing**: Complete error handling workflows

### 4. E2E Integration Gap Identification

Document gaps with focus on missing end-to-end workflow validation:

```yaml
e2e_coverage_gaps:
  - requirement: 'AC3: Secret key lifecycle management'
    gap: 'No complete workflow test from creation through update to deletion'
    severity: high
    current_coverage: 'unit_only'
    missing_e2e_test:
      type: e2e_integration
      suggested_file: 'Integration.Tests/Endpoints/SecretKeysEndpointTests.cs'
      workflow: 'CreateSecretKey -> UpdateSecretKey -> GetSecretKeyById -> DeleteSecretKey'
      authentication: 'JWT Bearer token validation throughout lifecycle'
      database_validation: 'Verify persistence and state transitions'

  - requirement: 'AC4: Multi-tenant data isolation under concurrent access'
    gap: 'No concurrent multi-tenant access validation'
    severity: critical
    current_coverage: 'integration_only'
    missing_e2e_test:
      type: e2e_integration
      suggested_file: 'Integration.Tests/Infrastructure/Services/MultiTenantConcurrencyTests.cs'
      workflow: 'Simultaneous tenant operations with isolation verification'
      auth_pattern: 'Multiple tenant tokens in parallel requests'
      database_validation: 'Verify no cross-tenant data leakage'

  - requirement: 'AC5: Host registration with remote access validation'
    gap: 'Missing end-to-end host lifecycle with actual remote connectivity'
    severity: medium
    current_coverage: 'e2e_validation'
    missing_e2e_test:
      type: e2e_integration
      enhancement: 'Extend HostEndpointTests to include connectivity validation'
      workflow: 'RegisterRemoteHost -> ValidateConnection -> DeregisterHost'
```

## Outputs

### Output 1: E2E Integration Gate YAML Block

**Generate for pasting into gate file under `trace`:**

```yaml
trace:
  totals:
    requirements: X
    e2e_integration: Y    # PRIMARY: Complete workflow validation
    e2e_validation: Z     # Validation scenarios covered
    integration_with_unit: A # Integration + unit test coverage
    integration_only: B   # Integration tests without unit support
    unit_only: C          # INSUFFICIENT: Unit tests only
    none: W               # CRITICAL: No coverage
  e2e_priority: 'Integration tests are source of truth for requirement validation'
  planning_ref: 'qa.qaLocation/assessments/{epic}.{story}-test-design-{YYYYMMDD}.md'
  critical_gaps:
    - ac: 'AC4'
      gap: 'Missing concurrent multi-tenant validation'
      severity: 'critical'
      test_type: 'e2e_integration'
  workflow_coverage:
    - endpoint_to_test_mapping: 'verified'
    - authentication_flows: 'validated'
    - multi_tenant_isolation: 'tested'
    - database_integration: 'verified'
  notes: 'See qa.qaLocation/assessments/{epic}.{story}-trace-{YYYYMMDD}.md'
```

### Output 2: E2E Integration Traceability Report

**Save to:** `qa.qaLocation/assessments/{epic}.{story}-trace-{YYYYMMDD}.md`

Create an E2E integration-focused traceability report with:

```markdown
# E2E Integration Requirements Traceability Matrix

## Story: {epic}.{story} - {title}

### E2E Integration Coverage Summary

- Total Requirements: X
- **E2E Integration Validated**: Y (Z%) - PRIMARY COVERAGE
- **E2E Validation Scenarios**: A (B%) - Edge case coverage  
- **Integration with Unit Support**: C (D%) - Comprehensive coverage
- **Integration Only**: E (F%) - Adequate but missing unit support
- **Unit Only**: G (H%) - INSUFFICIENT for requirement validation
- **Not Covered**: I (J%) - CRITICAL GAPS

### E2E Integration Test Mappings

#### AC1: {Acceptance Criterion 1}

**Coverage: E2E_INTEGRATION** âœ…

E2E Integration Tests (Source of Truth):

- **Endpoint Test**: `Integration.Tests/Endpoints/AuthEndpointTests.cs::RegisterComponent_ShouldReturn_Ok`
  - **Endpoint**: `POST /api/Auth/registerComponent/{tenantId}`
  - **Given**: Valid tenant with master authentication token
  - **When**: Component registration API called with tenant context
  - **Then**: Returns HTTP 200 with encrypted RemoteAccessToken, validates tenant isolation
  - **Authentication**: Bearer token with master privileges
  - **Multi-tenant**: Validates tenant-specific token generation
  - **Database**: Verifies tenant context in database operations

- **Validation Test**: `Integration.Tests/Endpoints/AuthEndpointTests.cs::RegisterComponent_ShouldValidateRequest`
  - **Test Pattern**: [Theory] with [InlineData] for multiple scenarios
  - **Given**: Invalid tenant IDs and malformed requests
  - **When**: Registration attempted with invalid data
  - **Then**: Returns appropriate HTTP error codes and descriptive error messages
  - **Scenarios**: Invalid tenant, missing parameters, validation failures

#### AC2: {Acceptance Criterion 2}

**Coverage: E2E_INTEGRATION** âœ…

E2E Integration Tests:

- **Complete Workflow**: `Integration.Tests/Endpoints/TenantEndpointTests.cs::CreateAndDeleteNewTenant_ShouldReturn_Ok`
  - **Endpoints**: `POST /api/Tenant/createNewTenant`, `DELETE /api/Tenant/deleteTenant`
  - **Given**: Master authentication and tenant creation parameters
  - **When**: Complete tenant lifecycle executed (create â†’ validate â†’ delete)
  - **Then**: Tenant created with isolated database, license verified, clean deletion confirmed
  - **Database Integration**: Validates tenant-specific database connection
  - **License Validation**: Confirms tenant license compliance
  - **Multi-tenant**: Ensures proper tenant isolation throughout lifecycle

[Continue for all ACs...]

### Critical E2E Integration Gaps

1. **Multi-Tenant Concurrency Requirements**
   - **Gap**: No concurrent multi-tenant access validation in integration tests
   - **Risk**: Critical - Data isolation could fail under concurrent load
   - **Current Coverage**: Integration tests exist but lack concurrency validation
   - **Required E2E Test**: `Integration.Tests/Infrastructure/Services/MultiTenantConcurrencyTests.cs`
   - **Workflow**: Simultaneous tenant operations with cross-tenant isolation verification
   - **Authentication**: Multiple tenant tokens in parallel requests

2. **Complete Workflow Validation**
   - **Gap**: Secret key lifecycle not fully tested end-to-end
   - **Risk**: High - Partial workflow failures not caught
   - **Current Coverage**: Individual endpoint tests exist but not linked workflows
   - **Required E2E Test**: Extend `Integration.Tests/Endpoints/SecretKeysEndpointTests.cs`
   - **Workflow**: Create â†’ Update â†’ Retrieve â†’ Delete with authentication throughout

3. **Cross-Service Integration**
   - **Gap**: Service-to-service communication not validated in integration tests
   - **Risk**: Medium - Integration points could fail silently
   - **Required E2E Test**: Service interaction workflows with database and external services

### E2E Integration Test Design Recommendations

Based on E2E gaps identified, prioritize:

1. **Complete Workflow Coverage**: Test entire user journeys, not just individual endpoints
2. **Multi-Tenant Validation**: Every test should validate tenant isolation where applicable
3. **Authentication Flow Integration**: Include authentication context in all relevant tests
4. **Database Transaction Validation**: Verify data persistence and consistency
5. **Error Scenario Integration**: Test complete error handling workflows
6. **Performance Integration**: Basic performance validation within integration tests

### Risk Assessment (E2E Integration Focus)

- **Critical Risk**: Requirements with no E2E integration coverage (unit_only or none)
- **High Risk**: Requirements with integration tests but missing complete workflow validation
- **Medium Risk**: Requirements with E2E integration but missing edge case validation  
- **Low Risk**: Requirements with comprehensive E2E integration plus supporting unit tests
```

## E2E Integration Traceability Best Practices

### E2E Integration Test Patterns

**Endpoint-to-Test Mapping:**
- Each API endpoint should have corresponding integration test
- Test file organization: `Integration.Tests/Endpoints/{FeatureArea}EndpointTests.cs`
- Test method naming: `{Operation}_{ExpectedResult}` (e.g., `CreateTenant_ShouldReturn_Ok`)

**Authentication Flow Integration:**
- Every test validates authentication context where applicable
- Bearer token patterns: Master tokens vs tenant-specific tokens
- Multi-tenant authentication validation in every relevant test

**Complete Workflow Testing:**
- Test entire business workflows, not just individual operations
- Link related operations: Create â†’ Read â†’ Update â†’ Delete sequences
- Validate state transitions and data consistency throughout workflow

**Database Integration Validation:**
- Real database operations with transaction verification
- Tenant-specific database connection validation
- Data persistence and retrieval verification

### Given-When-Then for E2E Integration Mapping

Use Given-When-Then to document complete E2E workflow validation:

**Given**: The complete system context and authentication setup

- Authentication tokens and tenant context
- Database state and test data preparation
- Multi-tenant isolation preconditions
- External service mock/stub configurations

**When**: The complete workflow or API interaction

- Full API request with realistic payloads
- Multi-step workflow execution
- Cross-service integration calls
- Error scenario triggering

**Then**: Complete system response and state validation

- HTTP response codes and payload validation
- Database state changes verified
- Multi-tenant isolation maintained
- Authentication context preserved
- Service integration confirmed

**Note**: This documents E2E integration validation, not test code implementation.

### E2E Coverage Priority (Source of Truth)

Prioritize E2E integration coverage based on:

1. **Critical Multi-Tenant Workflows** (HIGHEST)
2. **Authentication/Authorization Flows**
3. **Complete Business Process Workflows**
4. **Database Integration Operations**
5. **Cross-Service Communication**
6. **Error Handling Workflows**
7. **Performance-Critical Paths**

### Test Granularity (E2E Focus)

Map requirements with E2E integration as primary validation:

- **E2E Integration tests**: PRIMARY - Complete workflow validation (source of truth)
- **Unit tests**: SUPPLEMENTAL - Support E2E coverage with isolated logic testing
- **Performance tests**: SPECIALIZED - For non-functional requirements
- **Manual tests**: LAST RESORT - Only for scenarios impossible to automate

## E2E Integration Quality Indicators

Good E2E integration traceability shows:

- Every AC has E2E integration test coverage (PRIMARY requirement)
- Critical workflows tested end-to-end with complete system integration
- Authentication flows validated throughout complete user journeys
- Multi-tenant isolation verified in all applicable scenarios
- Database integration validated with real persistence operations
- Error scenarios tested with complete error handling workflows
- Clear endpoint-to-test mapping with realistic test data

## E2E Integration Red Flags

Critical issues to watch for:

- **ACs with only unit test coverage** - INSUFFICIENT for requirement validation
- **Missing complete workflow validation** - Tests individual operations but not linked workflows
- **Authentication not validated in integration context** - Tests functionality but ignores auth requirements
- **Multi-tenant isolation not verified** - Tests work but don't validate tenant data segregation
- **Database integration mocked or stubbed** - Tests logic but not actual data operations
- **Missing error scenario E2E validation** - Tests happy path but not complete error workflows
- **Vague integration test descriptions** - Tests exist but purpose unclear
- **Tests that don't map to actual API endpoints** - Test coverage doesn't reflect real system behavior

## Integration with E2E Quality Gates

E2E integration traceability feeds into quality gates with strict standards:

- **Requirements with no E2E integration coverage** â†’ FAIL
- **Critical workflows missing complete E2E validation** â†’ FAIL  
- **Multi-tenant requirements without isolation validation** â†’ FAIL
- **Authentication flows not validated in integration context** â†’ CONCERNS
- **Missing complete workflow E2E coverage** â†’ CONCERNS
- **Unit-only coverage for integration-dependent requirements** â†’ CONCERNS

### Gate Priorities (E2E Focus)

1. **FAIL Conditions**: E2E integration gaps for critical requirements
2. **CONCERNS**: Missing workflow completion or validation scenarios
3. **PASS Contribution**: Comprehensive E2E integration coverage with supporting unit tests

### Output 3: E2E Integration Story Hook Line

**Print this line for review task to quote:**

```text
E2E Integration Trace Matrix: qa.qaLocation/assessments/{epic}.{story}-trace-{YYYYMMDD}.md
```

## Key E2E Integration Principles

- **E2E integration tests are the source of truth** for requirement validation
- **Complete workflows take precedence** over individual operation testing
- **Multi-tenant validation is mandatory** for all applicable requirements
- **Authentication context must be preserved** throughout integration testing
- **Database integration must be real**, not mocked, for true validation
- **Error scenarios require complete workflow validation**, not just unit-level testing
- **Use Given-When-Then to document complete system behavior**, not just isolated logic
- **Prioritize based on system integration risk**, not just functional complexity

