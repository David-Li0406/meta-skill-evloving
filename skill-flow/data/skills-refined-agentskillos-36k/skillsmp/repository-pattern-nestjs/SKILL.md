---
name: repository-pattern-nestjs
description: Provides Prisma-specific repository implementation patterns for NestJS. This skill should be used when implementing repositories that extend BaseRepository or use Prisma delegates.
---

# Repository Pattern - Prisma/NestJS Implementation

**Implementation guide for NestJS Repositories using Prisma.**

For core database concepts (Soft Delete, Bulk Ops, Transactions), see **[Database Patterns](database-patterns/SKILL.md)**.
For general repository theory, see **[Repository Pattern](repository-pattern/SKILL.md)**.

## BaseRepository Extension

**All repositories MUST extend `BaseRepository<T, C, U, W>`**.

```typescript
import { BaseRepository, IBaseModel } from '@/lib/repositories/base.repository';

// 1. Define Wrapper (bridges BaseRepo generics to Prisma Delegate)
class UserModelWrapper implements IBaseModel<User, Prisma.UserCreateInput, Prisma.UserUpdateInput, Prisma.UserWhereInput> {
  constructor(private readonly delegate: Prisma.UserDelegate) {}
  create(args: any) { return this.delegate.create(args); }
  findFirst(args: any) { return this.delegate.findFirst(args); }
  findMany(args: any) { return this.delegate.findMany(args); }
  update(args: any) { return this.delegate.update(args); }
  delete(args: any) { return this.delegate.delete(args); }
  count(args: any) { return this.delegate.count(args); }
}

// 2. Implement Repository
@Injectable()
export class UserRepository extends BaseRepository<
  User,
  Prisma.UserCreateInput,
  Prisma.UserUpdateInput,
  Prisma.UserWhereInput
> {
  constructor(private readonly prisma: PrismaService) {
    super(new UserModelWrapper(prisma.user));
  }
}
```

## Specialized Find Methods

**Implement domain-specific queries here (not in Service).**

```typescript
// Find by UID (Standard)
async findByUid(uid: string): Promise<User | null> {
  return this.model.findFirst({
    where: { uid, deletedAt: null },
  });
}

// Find or Throw (Let Prisma throw P2025 -> converted to 404 by Global Filter)
async findByUidOrThrow(uid: string): Promise<User> {
  return this.model.findFirstOrThrow({
    where: { uid, deletedAt: null },
  });
}
```

## Type-Safe Includes

**Return typed payloads based on includes.**

```typescript
async findWithRelations<T extends Prisma.UserInclude>(
  include: T,
): Promise<Prisma.UserGetPayload<{ include: T }>[]> {
  return this.model.findMany({
    where: { deletedAt: null },
    include,
  });
}
```

## Implementation of Database Patterns

**Refer to [Database Patterns](database-patterns/SKILL.md) for the "Why". Here is the "How".**

### Soft Delete
**The BaseRepository handles this for standard methods.** If bypassing base methods:

```typescript
async softDelete(where: Prisma.UserWhereInput): Promise<void> {
  await this.model.updateMany({
    where: { ...where, deletedAt: null },
    data: { deletedAt: new Date() },
  });
}
```

### Bulk Create
```typescript
async createMany(data: Prisma.UserCreateInput[]): Promise<Prisma.BatchPayload> {
  return this.model.createMany({
    data,
    skipDuplicates: true,
  });
}
```

### Pagination
```typescript
async findPaginated(params: PaginationParams): Promise<PaginatedResult<User>> {
  const [data, total] = await Promise.all([
    this.model.findMany({ 
      where: { ...params.where, deletedAt: null },
      skip: params.skip,
      take: params.take 
    }),
    this.model.count({ where: { ...params.where, deletedAt: null } }),
  ]);
  return { data, total, page: params.page, limit: params.limit };
}
```

## Module Registration

```typescript
@Module({
  imports: [PrismaModule],
  providers: [UserRepository],
  exports: [UserRepository], // Export for Services to use!
})
export class UserModule {}
```

## Testing

**Integration Tests with Real Database (Recommended)**

```typescript
it('should not find soft-deleted user', async () => {
  await prisma.user.create({ data: { uid: 'u_del', deletedAt: new Date() } });
  const user = await repository.findByUid('u_del');
  expect(user).toBeNull();
});
```

## Best Practices Checklist

- [ ] Extend `BaseRepository`
- [ ] Implement `findByUid` and `findByUidOrThrow`
- [ ] **Always** filter `deletedAt: null` in custom queries
- [ ] Use `Promise.all` for pagination (count + data)
- [ ] Return `null` for not found (unless `OrThrow`)
- [ ] **Never** throw HTTP Exceptions (leave that to Service/Controller)
- [ ] Use `Prisma.GetPayload` for typed relations
