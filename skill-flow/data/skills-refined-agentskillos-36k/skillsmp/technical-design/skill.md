---
name: technical-design
description: (opencode-project - Skill) Template and guidelines for creating technical design documents
---

# Technical Design Skill

Use this skill when creating technical design documents based on requirements. This follows the Kiro spec-driven development format with emphasis on correctness properties.

## Directory Structure

The design document lives in the feature directory:

```
specs/
├── <feature-name>/
│   ├── requirements.md    # Requirements (created by /dev/spec)
│   ├── design.md          # This document
│   └── tasks.md           # Implementation tasks (created by /dev/tasks)
```

**Feature Name Format (CRITICAL)**: Feature names MUST be lowercase with dashes (kebab-case):
- ✅ `user-authentication`
- ✅ `api-rate-limiting`
- ✅ `budget-owner-implementation`
- ❌ `User Authentication`
- ❌ `API_Rate_Limiting`
- ❌ `BudgetOwnerImplementation`

## Design Document Template

Create the document at `specs/<feature-name>/design.md` with this structure:

```markdown
# Design Document: <Feature Name>

## Overview

<2-4 paragraphs describing the technical approach, how it implements the requirements, and key design principles being followed.>

The implementation follows <project>'s established patterns:
- **<Pattern 1>**: <Brief description>
- **<Pattern 2>**: <Brief description>
- **<Pattern 3>**: <Brief description>

## Architecture

### Layer Organization

```
<directory-structure-showing-where-code-lives>
```

### Data Flow

**<Operation Name>**:
1. <Step 1> -> <Component A>
2. <Component A> -> <Component B>
3. <Component B> -> <Component C>
4. Response flows back through layers

### Key Design Decisions

1. **<Decision 1>**: <Rationale>
2. **<Decision 2>**: <Rationale>
3. **<Decision 3>**: <Rationale>

## Components and Interfaces

### <Component Name> (<file path>)

```<language>
<interface or struct definition>
```

### <Component Name> (<file path>)

```<language>
<interface or struct definition>
```

## Data Models

### <Model Name> (<file path>)

```<language>
<struct/type definition with field comments>
```

### Database Schema (if applicable)

```sql
CREATE TABLE <table_name> (
    <column definitions>
);
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: <Property Name>

*For any* <input domain>, <operation> should <expected invariant>.

**Validates: Requirements <X.Y>**

### Property 2: <Property Name>

*For any* <input domain>, <operation> should <expected invariant>.

**Validates: Requirements <X.Y>**

### Property 3: <Property Name>

*For any* <condition>, <system behavior> must <guarantee>.

**Validates: Requirements <X.Y>**

## Error Handling

### Error Types

```<language>
<error type definitions>
```

### HTTP Status Code Mapping

- 200 OK: <When returned>
- 201 Created: <When returned>
- 400 Bad Request: <When returned>
- 404 Not Found: <When returned>
- 409 Conflict: <When returned>
- 500 Internal Server Error: <When returned>

## Testing Strategy

### Test Layer Assignment (MANDATORY)

*Each correctness property MUST be assigned to a test layer. Use the decision tree from AGENTS.md.*

| Property | Test Layer | Test File | Rationale |
|----------|------------|-----------|-----------|
| Property 1: <Name> | <Unit/Property/Integration/E2E> | `<path>_test.go` | <Why this layer> |
| Property 2: <Name> | <Unit/Property/Integration/E2E> | `<path>_test.go` | <Why this layer> |
| Property 3: <Name> | <Unit/Property/Integration/E2E> | `<path>_test.go` | <Why this layer> |

### Unit Tests (Standard Go Testing)

Test pure business logic and validation (NO infrastructure):
- <Test category 1>: `<file>_test.go`
- <Test category 2>: `<file>_test.go`

### Property-Based Tests (gopter)

Test universal properties across random inputs:

**Property Test 1: <Name>**
- **File**: `<path>_property_test.go`
- Generate random valid <inputs>
- Perform <operation>
- Assert <invariant>
- **Validates: Property 1 (<Property Name>), Requirements <X.Y>**

### Integration Tests (Ginkgo + testcontainers)

Test API endpoints with real database/cache:

| Endpoint | Test File | Scenarios |
|----------|-----------|-----------|
| `POST /api/v1/<resource>` | `<path>_integration_test.go` | Create success, validation failure |
| `GET /api/v1/<resource>/{id}` | `<path>_integration_test.go` | Found, not found |

### E2E Tests (Ginkgo + KIND) - Only if Kubernetes Required

Test Kubernetes-specific features (operators, webhooks, CRDs):
- <K8s scenario 1>: `test/e2e/<name>_test.go`
- <K8s scenario 2>: `test/e2e/<name>_test.go`

*If no Kubernetes features, write "N/A - No Kubernetes-specific features"*

## Database Migrations

### Migration 001: <Description>

```sql
<SQL migration>
```

## Implementation Notes

### Configuration

All configuration via environment variables (12-factor principles):

```bash
<ENV_VAR_1>=<value>
<ENV_VAR_2>=<value>
```

### Security Considerations

- <Security consideration 1>
- <Security consideration 2>

### Performance Considerations

- <Performance consideration 1>
- <Performance consideration 2>

## Dependencies

### External Libraries
- <Library 1>: <Purpose>
- <Library 2>: <Purpose>

### Internal Dependencies
- <Package 1>: <Purpose>
- <Package 2>: <Purpose>

```

## Correctness Properties Guidelines

Properties are the key differentiator in this design format. They bridge requirements to tests.

### Property Types

| Type | Pattern | Example |
|------|---------|---------|
| **Round-Trip** | *For any* valid X, serialize(deserialize(X)) == X | Creation round trip |
| **Uniqueness** | *For any* two entities, their <field> must be unique | Cost center code uniqueness |
| **Atomicity** | *For any* concurrent operations, final state == sum of operations | Utilization increment atomicity |
| **Completeness** | *For any* set, paginating returns all items exactly once | Pagination completeness |
| **Enforcement** | *For any* X with condition Y, system must Z | Hard enforcement blocks |
| **Validation** | *For any* invalid input, system rejects with error | Alert threshold validation |

### Writing Good Properties

1. **Start with "For any"**: This signals property-based testing
2. **Reference Requirements**: Every property validates specific acceptance criteria
3. **Be Testable**: Property should translate directly to property-based test
4. **Be Universal**: Property must hold for ALL valid inputs, not just examples

### Example Properties (from Budget Owner)

```markdown
### Property 1: Budget Owner Creation Round Trip

*For any* valid budget owner data, creating a budget owner and then 
retrieving it by ID should return equivalent data with all fields preserved.

**Validates: Requirements 1.1, 1.3**

### Property 3: Utilization Increment Atomicity

*For any* sequence of concurrent utilization increments to the same budget 
owner, the final utilization should equal the sum of all increments (no lost updates).

**Validates: Requirements 3.2, 14.4**
```

## Design Checklist

Before finalizing the design, verify:

- [ ] Overview explains the technical approach
- [ ] All requirements are addressed
- [ ] Follows existing code patterns (reference actual patterns)
- [ ] Data models are complete with types
- [ ] Interfaces are well-defined
- [ ] **Correctness properties are defined** (minimum 5)
- [ ] Each property references requirements
- [ ] **Each property has assigned test layer** (Unit/Property/Integration/E2E)
- [ ] **Test Layer Assignment table is complete**
- [ ] Testing strategy covers ALL properties
- [ ] Test file paths are specified for each test category
- [ ] Error handling is comprehensive
- [ ] Security is considered
- [ ] Performance is considered
- [ ] Migration path is defined (if applicable)

## Best Practices

1. **Reference the Requirements**: Link properties back to acceptance criteria
2. **Follow Existing Patterns**: Study `specs/` examples and AGENTS.md
3. **Be Specific**: Include actual code interfaces, not pseudocode
4. **Define Properties First**: They guide the implementation
5. **Plan for Failure**: Include error handling and rollback strategies
6. **Think About Testing**: Design should enable property-based testing
