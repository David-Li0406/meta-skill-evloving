---
name: repository-pattern
description: Provides general guidance for implementing data access layers in backend applications. This skill should be used when designing repositories, implementing query methods, or managing database access patterns.
---

# Repository Pattern Skill

Provides general guidelines for implementing repository (data access) layers in backend applications.

## Core Responsibilities

Repositories act as data access abstraction. They should:

1. **Encapsulate queries** - All database operations go through repositories
2. **Hide database details** - Services don't know SQL or ORM specifics
3. **Provide typed interfaces** - Strong typing for queries and results
4. **Handle errors** - Low-level errors are handled here
5. **Implement soft deletes** - Consistent deletion strategy
6. **Support common patterns** - Find, create, update, delete operations
7. **Optimize queries** - Eager loading, indexes, pagination

## Repository Architecture

**Layered Pattern**:

```
Service (Business logic)
    ↓
Repository (Data access)
    ├── Find operations
    ├── Create/Update operations
    ├── Delete operations
    ├── Bulk operations
    └── Count operations
    ↓
Database (PostgreSQL, MongoDB, etc.)
```

## Core Operations

### Find Operations

```
findById(id) → Entity | null
findBy*(key) → Entity | null
findMany(params) → Entity[]
findOne(criteria) → Entity | null
findFirstOrThrow(criteria) → Entity | throws
```

**Key Patterns**:
- ✅ Always include soft delete filter (deletedAt: null)
- ✅ Support multiple find methods (by id, by uid, by email, etc.)
- ✅ Return null when not found (or throw if OrThrow variant)
- ✅ Support filtering and ordering
- ✅ Support eager loading (includes/relations)

### Create Operations

```
create(data) → Entity
createMany(data[]) → BatchPayload
```

**Key Patterns**:
- ✅ Validate data before creating
- ✅ Return created entity with all fields
- ✅ Use bulk operations for multiple creates
- ✅ Handle unique constraint violations
- ✅ Generate required fields (id, timestamps)

### Update Operations

```
update(where, data) → Entity
updateMany(where, data) → BatchPayload
```

**Key Patterns**:
- ✅ Only update specified fields
- ✅ Return updated entity
- ✅ Use bulk operations for multiple updates
- ✅ Handle concurrent updates (optimistic locking)
- ✅ Update timestamps automatically

### Delete Operations

```
softDelete(where) → void
hardDelete(where) → void (rarely used)
```

**Key Patterns**:
- ✅ Use soft delete by default (set deletedAt)
- ✅ Never expose hard delete publicly
- ✅ Preserve data for audit trails
- ✅ Create separate method for permanent deletion (if needed)

### Bulk Operations

```
createMany(data[]) → BatchPayload
updateMany(where, data) → BatchPayload
deleteMany(where) → BatchPayload
```

**Key Patterns**:
- ✅ Handle multiple records in single operation
- ✅ Support partial success (skipDuplicates)
- ✅ Return operation results
- ✅ Use for performance-critical operations

## Soft Delete Pattern

**Always filter out deleted records by default**:

```
✅ CORRECT: Filter deleted
findMany({ where: { deletedAt: null } })

✅ CORRECT: Soft delete (set timestamp)
softDelete({ uid: 'user_123' })

✅ CORRECT: Query deleted (explicit)
findMany({ where: { deletedAt: { not: null } } })

❌ WRONG: No soft delete filter
findMany() // Includes deleted records

❌ WRONG: Hard delete
delete({ uid: 'user_123' }) // Loses data
```

**Key Rules**:
- ✅ All find operations include `deletedAt: null`
- ✅ Use soft delete (update deletedAt) instead of hard delete
- ✅ Create separate methods for querying deleted records
- ❌ Never expose hard delete without careful consideration
- ❌ Never forget the soft delete filter in queries

## Query Patterns

### Finding by Single Identifier

```
Common patterns:
- findById(id) - By database ID
- findByUid(uid) - By external UID
- findByEmail(email) - By email
- findByUsername(username) - By username
- findByExternalId(extId) - By external system ID
```

**Implementation**:
- ✅ Create specialized methods for common lookups
- ✅ Include soft delete filter
- ✅ Return null if not found (or throw)
- ✅ Type-safe return values

### Finding Multiple Records

```
Params:
- where: Filter criteria
- skip: Pagination offset
- take: Pagination limit
- orderBy: Sort order
- include: Relationships to load
```

**Key Patterns**:
- ✅ Support filtering (where clause)
- ✅ Support pagination (skip/take)
- ✅ Support sorting (orderBy)
- ✅ Support eager loading (include)
- ✅ Always filter out soft-deleted records

### Type-Safe Queries

```
Use framework's type system to ensure type safety:

✅ Typed includes
findMany({
  include: { studio: true, roles: true }
}) → User & { studio: Studio, roles: Role[] }

✅ Typed where clauses
findMany({
  where: { status: 'active' }
})

✅ Typed results
result.id → number
result.uid → string
result.deletedAt → Date | null
```

## Error Handling

**Repositories handle low-level errors**:

```
❌ Don't throw HTTP exceptions
throw new NotFoundException('User not found')

✅ Throw domain errors or let ORM handle
throw Prisma errors (converted by global filter)

✅ Use OrThrow variants
findFirstOrThrow() // Throws if not found
```

**Key Rules**:
- ✅ Let ORM throw low-level errors
- ✅ Global filter converts to HTTP responses
- ✅ Use `findFirstOrThrow()` for not-found cases
- ✅ Never throw HTTP exceptions in repositories
- ❌ Never expose database errors to clients

## Performance Considerations

### N+1 Query Prevention

```
❌ WRONG: N+1 queries
users.forEach(user => {
  user.studio = getStudio(user.studioId)
})

✅ CORRECT: Eager loading
findMany({
  include: { studio: true }
})
```

### Bulk Operations

```
❌ WRONG: Loop creates
users.forEach(user => create(user))

✅ CORRECT: Bulk create
createMany(users)
```

### Parallel Queries

```
❌ WRONG: Sequential
const users = findMany()
const count = count()

✅ CORRECT: Parallel
const [users, count] = Promise.all([
  findMany(),
  count()
])
```

## Pagination Implementation

```
Input:
- page: number (1-based)
- limit: number

Calculate:
- skip = (page - 1) * limit
- take = limit

Output:
- data: Entity[]
- total: number (call count() separately)
```

**Key Rules**:
- ✅ Support page and limit parameters
- ✅ Calculate skip correctly
- ✅ Query data and count in parallel (from service layer)
- ✅ Return pagination metadata from service

## Testing Repositories

**Unit Tests**: In-memory database or mocks

```
✅ Test find operations
✅ Test create/update/delete
✅ Test soft delete filtering
✅ Test bulk operations
✅ Test pagination
```

**Integration Tests**: Real database

```
✅ Test with real ORM
✅ Test transaction behavior
✅ Test constraints and relationships
✅ Test concurrent updates
```

## Best Practices Checklist

- [ ] All find operations filter `deletedAt: null`
- [ ] Soft delete used instead of hard delete
- [ ] Specialized `findBy*` methods for common queries
- [ ] Bulk operations used instead of loops
- [ ] Type-safe queries using framework's type system
- [ ] Error handling delegates to global filters
- [ ] No business logic in repositories
- [ ] No HTTP exceptions thrown
- [ ] Pagination supported
- [ ] Eager loading (includes) supported
- [ ] Repositories testable and mockable
- [ ] Clear method signatures with return types
- [ ] No N+1 query patterns
- [ ] Proper indexing on filtered columns

## Related Skills

- **service-pattern/SKILL.md** - Service layer using repositories
- **backend-controller-pattern/SKILL.md** - Repository consumption
- **database-patterns/SKILL.md** - ORM-specific patterns

## Decision Tree

**Getting single record?**
→ Use `findById()` or specialized `findBy*()` method
- Include soft delete filter
- Return null if not found
- Support eager loading via includes

**Getting multiple records?**
→ Use `findMany()` with filtering/pagination
- Include soft delete filter
- Support skip/take for pagination
- Support where clauses for filtering
- Support orderBy for sorting

**Creating/Updating multiple records?**
→ Use bulk operations
- Use `createMany()` or `updateMany()`
- Avoid loops
- Return operation results

**Unsure about approach?**
→ Check similar repositories in codebase
- Look for established patterns
- Follow existing conventions
- Ask in code review
