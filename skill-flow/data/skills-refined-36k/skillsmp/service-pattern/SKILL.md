---
name: service-pattern
description: Provides general guidance for implementing service layers in backend applications. This skill should be used when designing service architectures, implementing CRUD operations, or organizing orchestration services.
---

# Service Pattern Skill

Provides general guidelines for implementing service layers in backend applications.

## Core Responsibilities

Services act as the business logic layer. They should:

1. **Implement business logic** - Handle domain rules and operations
2. **Coordinate data access** - Call repositories to fetch/persist data
3. **Validate input** - Check data before persistence
4. **Handle errors** - Transform low-level errors to domain errors
5. **Coordinate operations** - Orchestrate multi-entity workflows
6. **Manage transactions** - Ensure data consistency

## Service Architecture

**Layered Pattern**:

```
Controller (HTTP boundary)
    ↓
Service (Business logic)
    ├─ Model Services (single entity)
    └─ Orchestration Services (multiple entities)
    ↓
Repository (Data access)
    ↓
Database
```

### Model Services

Handle CRUD operations for a single entity:

```
UserService
├── createUser(data) → User
├── getUserById(id) → User
├── listUsers(params) → User[]
├── updateUser(id, data) → User
└── deleteUser(id) → void
```

**Characteristics**:
- ✅ Focused on single entity
- ✅ Simple CRUD operations
- ✅ Dependency: one or more repositories
- ✅ Injected into controllers and other services

### Orchestration Services

Coordinate multiple entities for complex workflows:

```
ShowOrchestrationService
├── createShowWithAssignments(data)
│   ├─ Validate input
│   ├─ Create show
│   ├─ Create MC assignments
│   ├─ Create platform assignments
│   └─ Return with relations
└── publishSchedule(scheduleId)
    ├─ Validate schedule
    ├─ Delete old shows
    ├─ Create new shows
    └─ Update schedule status
```

**Characteristics**:
- ✅ Coordinate multiple services/repositories
- ✅ Handle complex business workflows
- ✅ Use transactions for atomicity
- ✅ Injected into controllers
- ✅ May call other orchestration services (rare)

## CRUD Operations Pattern

### Create

```
1. Receive data from controller
2. Validate input
3. Generate unique identifiers (if needed)
4. Call repository to create
5. Handle errors
6. Return created entity
```

**Key Rules**:
- ✅ Validate all input
- ✅ Generate IDs in service (not controller)
- ✅ Handle duplicate key errors
- ✅ Return created entity with all fields

### Read

```
1. Receive identifier from controller
2. Call repository to fetch
3. Handle not-found error (404)
4. Return entity
```

**Key Rules**:
- ✅ Always check if entity exists
- ✅ Throw not-found error if missing
- ✅ Support filtering and pagination
- ✅ Load relations when needed

### Update

```
1. Receive id and data from controller
2. Verify entity exists (not-found check)
3. Validate input data
4. Call repository to update
5. Handle version conflicts
6. Return updated entity
```

**Key Rules**:
- ✅ Always verify resource exists before updating
- ✅ Validate update data
- ✅ Handle concurrent updates (optimistic locking)
- ✅ Return updated entity

### Delete

```
1. Receive id from controller
2. Verify entity exists
3. Call repository to delete
4. Handle foreign key constraints
5. Return success
```

**Key Rules**:
- ✅ Always verify resource exists
- ✅ Handle cascade delete or soft delete
- ✅ Check for referential integrity
- ✅ Log deletion for audit trail

## Error Handling in Services

**Pattern**: Service layer throws domain errors, controller/filter converts to HTTP

```
Service throws:
  HttpError.notFound('User', id)
  HttpError.badRequest('Invalid email')
  HttpError.conflict('Duplicate entry')

↓

Global error filter converts to HTTP:
  {
    "statusCode": 404,
    "message": "User not found: user_123",
    "error": "NotFound"
  }
```

**Error Levels**:

| Error Type | Status | Use Case |
|-----------|--------|----------|
| Not Found | 404 | Resource doesn't exist |
| Bad Request | 400 | Invalid input validation |
| Conflict | 409 | Version mismatch, duplicates |
| Unauthorized | 401 | Authentication required |
| Forbidden | 403 | User not authorized |
| Unprocessable Entity | 422 | Invalid data format |

**Key Rules**:
- ✅ Throw domain-level errors in services
- ✅ Include context (resource name, identifier)
- ✅ Never expose implementation details
- ❌ Never throw low-level database errors directly
- ❌ Never expose SQL or internal structure

## Dependency Injection

**Services depend on repositories and utilities**:

```
Service
├── Repository (data access)
├── OtherService (domain logic)
├── UtilityService (helpers)
└── Configuration
```

**Characteristics**:
- ✅ Inject dependencies in constructor
- ✅ Use dependency injection containers
- ✅ Keep circular dependencies to minimum
- ✅ Prefer explicit over implicit dependencies

## Bulk Operations

**Pattern**: Use batch operations, not loops

```
❌ WRONG:
for (user of users) {
  await service.createUser(user)
}

✅ CORRECT:
await repository.createMany(users)
```

**Benefits**:
- ✅ Fewer database calls
- ✅ Better performance
- ✅ Atomic operations
- ✅ Reduced network overhead

## Transaction Management

**Pattern**: Wrap multi-step operations in transactions

```
1. Start transaction
2. Operation A (create show)
3. Operation B (create assignments)
4. Operation C (update schedule)
5. Commit or Rollback
```

**Key Rules**:
- ✅ Use transactions for multi-step operations
- ✅ Roll back on any failure
- ✅ Minimize transaction scope (only data operations)
- ❌ Never include external API calls in transactions
- ❌ Never do long-running operations in transactions

## Pagination Implementation

**Pattern**: Support pagination in list services

```
Input:
{
  page: 1,
  limit: 10,
  filters: {...}
}

Processing:
skip = (page - 1) * limit
take = limit

Output:
{
  data: [...],
  meta: {
    page: 1,
    limit: 10,
    total: 150
  }
}
```

**Key Rules**:
- ✅ Support page and limit parameters
- ✅ Calculate skip correctly
- ✅ Query data and count in parallel
- ✅ Return metadata with total count

## Testing Services

**Unit Tests**: Mock repositories, test business logic

```
✅ Test data validation
✅ Test error handling
✅ Test business rules
✅ Test transaction rollback
✅ Mock repository calls
```

**Integration Tests**: Real repositories, test with data

```
✅ Test with real database
✅ Test transaction behavior
✅ Test soft delete patterns
✅ Test pagination
```

## Best Practices Checklist

- [ ] Single responsibility: One service per entity (or orchestration)
- [ ] All input validated before database operations
- [ ] Resource existence verified before update/delete
- [ ] All errors properly typed and contextualized
- [ ] Pagination supported on list operations
- [ ] Bulk operations used instead of loops
- [ ] Transactions used for multi-step operations
- [ ] Dependencies injected in constructor
- [ ] No circular dependencies
- [ ] Services testable with mocked repositories
- [ ] Error messages include context (resource, identifier)
- [ ] No exposure of internal database structure

## Related Skills

- **repository-pattern/SKILL.md** - Data access layer
- **backend-controller-pattern/SKILL.md** - Service consumption
- **data-validation/SKILL.md** - Validation patterns
- **authentication-authorization-backend/SKILL.md** - Auth in services

## Decision Tree

**Implementing CRUD for single entity?**
→ Create Model Service
- Extend base service class if available
- Inject repository
- Implement create/read/update/delete
- Use utility service for ID generation

**Coordinating multiple entities?**
→ Create Orchestration Service
- Inject multiple repositories/services
- Use transactions for atomicity
- Call multiple repositories in sequence
- Validate before multi-step operations

**Unsure about approach?**
→ Check related services in codebase
- Look for similar patterns
- Follow existing conventions
- Consult team guidelines
- Ask in code review
