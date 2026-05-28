---
name: task-breakdown
description: (opencode-project - Skill) Template and guidelines for breaking features into implementation tasks
---

# Task Breakdown Skill

Use this skill when breaking down a feature into implementation tasks. This follows the Kiro spec-driven development format with checkbox-style task tracking and requirement traceability.

## Directory Structure

The tasks document lives in the feature directory:

```
specs/
├── <feature-name>/
│   ├── requirements.md    # Requirements (created by /dev/spec)
│   ├── design.md          # Technical design (created by /dev/design)
│   └── tasks.md           # This document
```

**Feature Name Format (CRITICAL)**: Feature names MUST be lowercase with dashes (kebab-case):
- ✅ `user-authentication`
- ✅ `api-rate-limiting`
- ✅ `budget-owner-implementation`
- ❌ `User Authentication`
- ❌ `API_Rate_Limiting`
- ❌ `BudgetOwnerImplementation`

## Tasks Document Template

Create the document at `specs/<feature-name>/tasks.md` with this structure:

```markdown
# Implementation Plan: <Feature Name>

## Overview

<Brief description of the implementation plan and how tasks are organized (by layer, phase, etc.)>

## Tasks

- [ ] 1. <Major Task Category>
  - <Brief description of what this category covers>
  - _Requirements: <X.Y, X.Z>_

- [ ] 1.1 <Subtask Title>
  - <Detailed description of what to implement>
  - _Requirements: <X.Y>_

- [ ] 1.2 <Subtask Title>
  - <Detailed description of what to implement>
  - _Requirements: <X.Y>_

- [ ] 1.3 <Subtask Title>
  - **Property: <Property Name>**
  - **Validates: Requirements <X.Y>**

- [ ] 2. <Major Task Category>
  - <Brief description>
  - _Requirements: <X.Y>_

- [ ] 2.1 <Subtask Title>
  - <Description>
  - _Requirements: <X.Y>_

- [ ] 2.2 <Subtask Title>
  - <Description>
  - _Requirements: <X.Y>_

- [-] 3. <Major Task Category> (Partially Complete)
  - <Description>
  - _Requirements: <X.Y>_

- [x] 3.1 <Completed Subtask>
  - <Description>
  - _Requirements: <X.Y>_

- [!] 3.2 <Failed/Blocked Subtask>
  - <Description>
  - **Failure Details**: <What went wrong>
  - **Root Cause**: <Why it failed>
  - **Fix Required**: <What needs to be done>

- [ ] 4. Checkpoint - <Milestone Description>
  - <What should be verified at this checkpoint>
  - Ask the user if questions arise

## Notes

- All tasks are required for comprehensive implementation
- Each task references specific requirements for traceability
- Property tests validate universal correctness properties
- Integration tests validate API endpoints with real infrastructure
- Checkpoints ensure incremental validation

## Estimated Timeline

- Week 1: Tasks 1-X (<Description>)
- Week 2: Tasks X-Y (<Description>)
- Week 3: Tasks Y-Z (<Description>)

Total: <N> weeks for complete implementation
```

## Task Status Markers

Use these checkbox markers for task status:

| Marker | Status | Meaning |
|--------|--------|---------|
| `- [ ]` | Pending | Task not yet started |
| `- [x]` | Completed | Task finished successfully |
| `- [-]` | In Progress / Partial | Task started or partially complete |
| `- [!]` | Failed / Blocked | Task failed, needs attention |

## Task Naming Conventions

### Major Tasks (Numbered)
```markdown
- [ ] 1. Database Schema and Migrations
- [ ] 2. Domain Entity Implementation
- [ ] 3. Repository Implementation
- [ ] 4. Command Handler Implementation
```

### Subtasks (Decimal Numbered)
```markdown
- [ ] 1.1 Create budget_owners table migration
- [ ] 1.2 Create audit_logs table migration
- [ ] 1.3 Test migrations in development environment
```

### Property Test Tasks
```markdown
- [ ] 4.12 Write property test for cost center code uniqueness
  - **Property 2: Cost Center Code Uniqueness**
  - **Validates: Requirements 11.2, 11.3**
```

### Checkpoint Tasks
```markdown
- [ ] 16. Checkpoint - Ensure all tests pass
  - Run all unit tests
  - Run all property tests
  - Run all integration tests
  - Fix any failing tests
  - Ensure test coverage meets goals (80%+ for business logic)
  - Ask the user if questions arise
```

## Requirement Traceability

Every task MUST reference the requirements it implements:

```markdown
- [ ] 5.2 Implement HandleCreateBudgetOwner
  - Validate input command
  - Check cost center code uniqueness
  - Create budget owner entity
  - Persist to database
  - Log audit event
  - Return created budget owner ID
  - _Requirements: 1.1, 10.1_
```

## Handling Failures

When a task fails, document it clearly:

```markdown
- [!] 12.9 Write property test for transfer atomicity
  - **Property 13: Transfer Atomicity**
  - **Validates: Requirements 6.5**
  - **Failure Details**: Transfer should fail when attempting to transfer 
    non-existent resources, but it succeeds
  - **Root Cause**: Missing validation in Transfer method - needs to verify 
    all resourceIDs exist before transfer
  - **Fix Required**: Add validation to ensure count of existing assignments 
    matches count of requested resourceIDs
```

## Task Organization by Architecture Layer

Organize tasks following CLEAN architecture layers:

1. **Database/Infrastructure** (Tasks 1.x)
   - Migrations, schemas, indexes

2. **Domain Entities** (Tasks 2.x)
   - Entity structures, validation

3. **Repository/Data Access** (Tasks 3.x-4.x)
   - Interface definitions, implementations

4. **Application Layer** (Tasks 5.x-7.x)
   - Commands, queries, services

5. **Interface Layer** (Tasks 8.x-9.x)
   - HTTP handlers, adapters

6. **Cross-Cutting** (Tasks 10.x-15.x)
   - Middleware, notifications, jobs

7. **Testing** (Tasks 16.x-18.x) - **MANDATORY**
   - Unit tests for validation logic
   - Property tests for correctness properties
   - Integration tests for API endpoints
   - E2E tests for Kubernetes features (if applicable)

8. **Verification** (Tasks 19.x+)
   - Checkpoints, documentation, deployment

## Mandatory Test Tasks

**Every task breakdown MUST include test tasks for each correctness property from the design document.**

### Test Task Structure

For each correctness property in `design.md`, create a corresponding test task:

```markdown
## Phase N: Testing

- [ ] N.1 <Test Type> Tests for <Domain>
  - Create test file `<path>_test.go`
  - _Requirements: <X.Y>_

- [ ] N.1.1 Write <test type> test for <Property Name>
  - **Property**: <Property N from design.md>
  - **Test Layer**: <Unit/Property/Integration/E2E>
  - **Test File**: `<path>_<type>_test.go`
  - **Validates**: Requirements <X.Y>

- [ ] N.1.2 Write <test type> test for <Property Name>
  - **Property**: <Property M from design.md>
  - **Test Layer**: <Unit/Property/Integration/E2E>
  - **Test File**: `<path>_<type>_test.go`
  - **Validates**: Requirements <X.Y>
```

### Test Task Naming by Layer

| Test Layer | Task Naming Pattern | File Pattern |
|------------|---------------------|--------------|
| Unit | "Write unit test for X" | `*_test.go` |
| Property | "Write property test for X" | `*_property_test.go` |
| Integration | "Write integration test for X" | `*_integration_test.go` |
| E2E | "Write E2E test for X" | `test/e2e/*_test.go` |

### Example: Test Tasks from Design Properties

If `design.md` has these correctness properties:

```markdown
### Property 1: Budget Owner Creation Round Trip
*For any* valid budget owner data, creating and retrieving should return equivalent data.
**Validates: Requirements 1.1, 1.3**

### Property 2: Cost Center Code Uniqueness  
*For any* two budget owners, their cost center codes must be unique.
**Validates: Requirements 11.2, 11.3**

### Property 3: API Response Format
*For any* GET request to /budget-owners/{id}, response matches BudgetOwner schema.
**Validates: Requirements 1.3, 23.7**
```

Then `tasks.md` MUST include:

```markdown
## Phase X: Testing

- [ ] X.1 Property Tests for Budget Owner
  - _Requirements: 1.1, 1.3, 11.2, 11.3_

- [ ] X.1.1 Write property test for creation round trip
  - **Property**: Property 1 (Budget Owner Creation Round Trip)
  - **Test Layer**: Property Test (gopter)
  - **Test File**: `internal/entities/budget/budget_owner_property_test.go`
  - **Validates**: Requirements 1.1, 1.3

- [ ] X.1.2 Write property test for cost center uniqueness
  - **Property**: Property 2 (Cost Center Code Uniqueness)
  - **Test Layer**: Property Test (gopter)
  - **Test File**: `internal/entities/budget/budget_owner_property_test.go`
  - **Validates**: Requirements 11.2, 11.3

- [ ] X.2 Integration Tests for Budget Owner API
  - _Requirements: 1.3, 23.7_

- [ ] X.2.1 Write integration test for GET /budget-owners/{id}
  - **Property**: Property 3 (API Response Format)
  - **Test Layer**: Integration Test (Ginkgo + testcontainers)
  - **Test File**: `internal/adapters/handlers/management/budget_owner_integration_test.go`
  - **Validates**: Requirements 1.3, 23.7
```

### Test Coverage Verification Checkpoint

Include a test verification checkpoint:

```markdown
- [ ] N. Checkpoint - Test Coverage Verification
  - [ ] All correctness properties from design.md have test tasks
  - [ ] Each test task specifies: Property, Test Layer, Test File, Requirements
  - [ ] Test file paths follow naming conventions
  - [ ] Run `mage test:unit` - all pass
  - [ ] Run `mage test:property` - all pass  
  - [ ] Run `mage test:integration` - all pass (if applicable)
  - [ ] Test coverage meets 80%+ for business logic
  - Ask the user if questions arise
```

## Task Size Guidelines

### Subtasks Should Be:
- **Atomic**: One clear deliverable
- **Testable**: Has clear acceptance criteria
- **Small**: Completable in 1-4 hours
- **Independent**: Minimal blocking dependencies

### If a Task is Too Large:
Break it into subtasks. A major task category should have 3-10 subtasks.

## Best Practices

1. **Reference Requirements**: Every task links to requirements
2. **MANDATORY Test Tasks**: Every correctness property from design.md MUST have a test task
3. **Specify Test Layer**: Each test task must specify Unit/Property/Integration/E2E
4. **Include Test Files**: Each test task must specify the target test file path
5. **Add Checkpoints**: Include verification checkpoints every 3-5 major tasks
6. **Track Failures**: Use `[!]` marker with failure details
7. **Estimate Timeline**: Include week-by-week breakdown
8. **Follow Order**: Tasks should be in dependency order (implementation before tests)

## Example: Budget Owner Tasks (Reference)

See `specs/` for comprehensive examples with subtasks organized by layer, including mandatory test phases.
