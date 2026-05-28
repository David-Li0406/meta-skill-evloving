---
name: service-pattern-nestjs
description: Provides NestJS-specific service implementation patterns. This skill should be used when implementing Model Services, Orchestration Services, or business logic with NestJS decorators.
---

# Service Pattern - NestJS Implementation

**Implementation guide for NestJS Services in Eridu.**

For core database concepts (Transactions, Bulk Ops), see **[Database Patterns](database-patterns/SKILL.md)**.
For general service architecture, see **[Service Pattern](service-pattern/SKILL.md)**.

## Model Service Structure

**Extend `BaseModelService<T>` for standard CRUD**.

```typescript
import { Injectable } from '@nestjs/common';
import { BaseModelService } from '@/lib/services/base-model.service';
import { UtilityService } from '@/utility/utility.service';

@Injectable()
export class UserService extends BaseModelService {
  // UID_PREFIX has NO trailing underscore (e.g., 'user', not 'user_')
  static readonly UID_PREFIX = 'user';
  protected readonly uidPrefix = UserService.UID_PREFIX;

  constructor(
    private readonly userRepository: UserRepository,
    utilityService: UtilityService,
  ) {
    super(utilityService);
  }
}
```

## CRUD Operations

**Implement business logic here.**

```typescript
// Create with ID generation
async createUser(data: CreateUserDto): Promise<User> {
  return this.userRepository.create({
    uid: this.generateUid(), // Helper from BaseModelService
    email: data.email,
    name: data.name,
  });
}

// Read with verification
async getUserById(uid: string): Promise<User> {
  const user = await this.userRepository.findByUid(uid);
  if (!user) throw HttpError.notFound('User', uid);
  return user;
}

// Update (See "Verify Before Modify" pattern)
async updateUser(uid: string, data: UpdateUserDto): Promise<User> {
  await this.getUserById(uid); // Ensure exists
  return this.userRepository.update({ uid }, data);
}
```

## Error Handling

**Use `HttpError` utility, NEVER NestJS exceptions directly.**
This ensures consistent error responses and logging.

```typescript
import { HttpError } from '@/common/errors/http-error.util';

// 404 Not Found
if (!user) throw HttpError.notFound('User', uid);

// 400 Bad Request
if (invalid) throw HttpError.badRequest('Invalid state');

// 409 Conflict
if (exists) throw HttpError.conflict('User already exists');

// 403 Forbidden
if (!allowed) throw HttpError.forbidden('Access denied');
```

## Orchestration Services

**Coordinate multiple services/repositories using Transactions.**
See **[Database Patterns](database-patterns/SKILL.md)** for transaction rules.

```typescript
// Example: Creating a Show implies creating Assignments
async createShowWithAssignments(data: CreateShowDto) {
  return this.prismaService.$transaction(async (tx) => {
    // 1. Create Parent
    const show = await this.showService.createShow({ ...data, tx });
    
    // 2. Create Children
    await this.assignmentService.createAssignments(show.id, data.assignments, tx);
    
    return show;
  });
}
```

## Verify Before Modify Pattern

**Always check existence before mutating.**

```typescript
async deleteUser(uid: string): Promise<void> {
  // 1. Verify existence (throws 404 if missing)
  await this.getUserById(uid);

  // 2. Perform operation
  await this.userRepository.softDelete({ uid });
}
```

## Pagination

**Execute Count and Data queries in parallel.**

```typescript
async listUsers(params: PaginationParams) {
  const [data, total] = await Promise.all([
    this.userRepository.findMany({ ...params }),
    this.userRepository.count({ ...params }),
  ]);
  return { data, total };
}
```

### Advanced Search and Filtering

For services that require complex search logic (e.g. partial matches, date ranges, soft-delete filtering), see the **[Admin List Pattern](../admin-list-pattern/SKILL.md)**.

## Bulk Operations

**Use Repository bulk methods, DO NOT loop in Service.**

```typescript
async createManyUsers(users: CreateUserDto[]) {
  // Map DTOs to internal structure (e.g. add UIDs)
  const data = users.map(u => ({
    ...u,
    uid: this.generateUid()
  }));
  
  // Single DB Call
  return this.userRepository.createMany(data);
}
```

## Best Practices Checklist

- [ ] Extend `BaseModelService`
- [ ] Define `UID_PREFIX` static constant
- [ ] Inject `UtilityService`
- [ ] Use `this.generateUid()`
- [ ] **Verify** resource exists before Update/Delete
- [ ] Use `HttpError` for all exceptions
- [ ] Use `Promise.all` for independent async tasks
- [ ] Use `PrismaService.$transaction` for multi-step workflows
- [ ] **Never** throw `NotFoundException` directly (use `HttpError.notFound`)
