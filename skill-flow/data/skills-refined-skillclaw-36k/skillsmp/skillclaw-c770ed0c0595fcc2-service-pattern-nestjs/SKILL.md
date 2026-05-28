---
name: service-pattern-nestjs
description: Use this skill when implementing Model Services, Orchestration Services, or business logic with NestJS decorators.
---

# Service Pattern - NestJS Implementation

**Implementation guide for NestJS Services in Eridu.**

For core database concepts (Transactions, Bulk Ops), see **[Database Patterns](database-patterns/SKILL.md)**. For general service architecture, see **[Service Pattern](service-pattern/SKILL.md)**.

## Model Service Structure

**Extend `BaseModelService<T>` for standard CRUD.**

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

**Use `HttpError` utility, NEVER NestJS exceptions directly.** This ensures consistent error responses and logging.

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

**Coordinate multiple services/repositories.**