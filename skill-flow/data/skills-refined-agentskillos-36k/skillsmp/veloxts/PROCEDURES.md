# VeloxTS Procedures API Reference

Procedures are the core abstraction for defining type-safe API endpoints. They combine validation, handlers, and routing in a fluent builder pattern.

## Basic Structure

```typescript
import { procedure, procedures, z } from '@veloxts/velox';

export const userProcedures = procedures('users', {
  getUser: procedure()
    .input(z.object({ id: z.string().uuid() }))
    .output(UserSchema)
    .query(async ({ input, ctx }) => {
      return ctx.db.user.findUnique({ where: { id: input.id } });
    }),

  createUser: procedure()
    .input(CreateUserSchema)
    .output(UserSchema)
    .mutation(async ({ input, ctx }) => {
      return ctx.db.user.create({ data: input });
    }),
});
```

## Procedure Methods

### `.input(schema)`

Validates incoming request data with Zod.

```typescript
.input(z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  age: z.number().min(0).max(150).optional(),
}))
```

**Important**: Input is validated before the handler runs. Invalid input returns 400.

### `.output(schema)`

Validates and types the response.

```typescript
.output(z.object({
  id: z.string(),
  name: z.string(),
  createdAt: z.coerce.date(),
}))
```

**Tip**: Use `.output()` for type inference and runtime validation of responses.

### `.query(handler)` vs `.mutation(handler)`

- **Query**: Read operations (GET requests)
- **Mutation**: Write operations (POST, PUT, PATCH, DELETE)

```typescript
// Query - for reading data
listUsers: procedure()
  .output(z.array(UserSchema))
  .query(async ({ ctx }) => {
    return ctx.db.user.findMany();
  }),

// Mutation - for writing data
createUser: procedure()
  .input(CreateUserSchema)
  .output(UserSchema)
  .mutation(async ({ input, ctx }) => {
    return ctx.db.user.create({ data: input });
  }),
```

### `.guard(guardFn)`

Protects procedures with authentication/authorization.

```typescript
import { authenticated, hasRole, hasPermission } from '@veloxts/auth';

// Require authentication
getProfile: procedure()
  .guard(authenticated)
  .query(({ ctx }) => ctx.user),

// Require specific role
adminPanel: procedure()
  .guard(hasRole('admin'))
  .query(() => ({ admin: true })),

// Require permission
deletePost: procedure()
  .guard(hasPermission('posts.delete'))
  .input(z.object({ id: z.string() }))
  .mutation(async ({ ctx, input }) => {
    await ctx.db.post.delete({ where: { id: input.id } });
  }),

// Custom guard
isOwner: procedure()
  .guard(async ({ ctx, input }) => {
    const post = await ctx.db.post.findUnique({ where: { id: input.id } });
    if (post?.authorId !== ctx.user?.id) {
      throw new Error('Not authorized');
    }
  })
  .input(z.object({ id: z.string() }))
  .mutation(async ({ ctx, input }) => { /* ... */ }),
```

### `.rest(options)`

Override automatic REST route inference.

```typescript
// Custom path
publishPost: procedure()
  .input(z.object({ id: z.string() }))
  .rest({ method: 'POST', path: '/posts/:id/publish' })
  .mutation(/* ... */),

// Custom method
archivePost: procedure()
  .rest({ method: 'PATCH', path: '/posts/:id/archive' })
  .mutation(/* ... */),
```

**Warning**: Don't include `/api` prefix - it's added automatically.

### `.use(middleware)`

Add procedure-specific middleware.

```typescript
import { rateLimit, cache } from '@veloxts/velox';

// Rate limiting
createComment: procedure()
  .use(rateLimit({ max: 10, window: '1m' }))
  .input(CommentSchema)
  .mutation(/* ... */),

// Caching
getPopularPosts: procedure()
  .use(cache({ ttl: '5m' }))
  .output(z.array(PostSchema))
  .query(/* ... */),
```

## REST Route Inference

VeloxTS automatically maps procedure names to HTTP routes:

### Query Procedures (GET)

| Prefix | HTTP | Route Pattern | Example |
|--------|------|---------------|---------|
| `get*` | GET | `/{namespace}/:id` | `getUser` → `GET /users/:id` |
| `list*` | GET | `/{namespace}` | `listUsers` → `GET /users` |
| `find*` | GET | `/{namespace}` | `findUsers` → `GET /users` |

### Mutation Procedures

| Prefix | HTTP | Route Pattern | Example |
|--------|------|---------------|---------|
| `create*` | POST | `/{namespace}` (201) | `createUser` → `POST /users` |
| `add*` | POST | `/{namespace}` (201) | `addUser` → `POST /users` |
| `update*` | PUT | `/{namespace}/:id` | `updateUser` → `PUT /users/:id` |
| `edit*` | PUT | `/{namespace}/:id` | `editUser` → `PUT /users/:id` |
| `patch*` | PATCH | `/{namespace}/:id` | `patchUser` → `PATCH /users/:id` |
| `delete*` | DELETE | `/{namespace}/:id` | `deleteUser` → `DELETE /users/:id` |
| `remove*` | DELETE | `/{namespace}/:id` | `removeUser` → `DELETE /users/:id` |

### React Query Hook Mapping

Naming also determines which React Query hooks are available:

**Query prefixes** (`get*`, `list*`, `find*`):
```typescript
api.users.getUser.useQuery({ id })
api.users.listUsers.useSuspenseQuery({})
api.posts.findPosts.useQuery({ search: 'hello' })
```

**Mutation prefixes** (everything else):
```typescript
api.users.createUser.useMutation()
api.posts.updatePost.useMutation()
api.comments.deleteComment.useMutation()
```

**Warning**: Non-standard names like `fetchUsers` are treated as mutations!

## Context Object

The `ctx` parameter provides request-scoped data:

```typescript
.query(async ({ input, ctx }) => {
  // Database client
  const user = await ctx.db.user.findUnique({ where: { id: input.id } });

  // Current authenticated user (if using auth)
  const currentUser = ctx.user;

  // Raw Fastify request/reply
  const ip = ctx.request.ip;
  ctx.reply.header('X-Custom', 'value');

  // Cache (if configured)
  const cached = await ctx.cache.get('key');

  // Queue (if configured)
  await ctx.queue.dispatch(SendEmailJob, { to: user.email });
})
```

### Available Context Properties

| Property | Type | Description |
|----------|------|-------------|
| `ctx.db` | `PrismaClient` | Database client |
| `ctx.user` | `User \| undefined` | Authenticated user |
| `ctx.request` | `FastifyRequest` | Raw HTTP request |
| `ctx.reply` | `FastifyReply` | Raw HTTP response |
| `ctx.cache` | `CacheManager` | Cache operations (if enabled) |
| `ctx.queue` | `QueueManager` | Job queue (if enabled) |
| `ctx.storage` | `StorageManager` | File storage (if enabled) |

## Validation Patterns

### Input Schemas

```typescript
// Required fields
const CreateUserInput = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(255),
  password: z.string().min(8),
});

// Optional fields with defaults
const ListUsersInput = z.object({
  page: z.number().min(1).default(1),
  limit: z.number().min(1).max(100).default(10),
  search: z.string().optional(),
});

// Enum fields
const UpdateStatusInput = z.object({
  status: z.enum(['draft', 'published', 'archived']),
});

// Nested objects
const CreateOrderInput = z.object({
  items: z.array(z.object({
    productId: z.string().uuid(),
    quantity: z.number().min(1),
  })).min(1),
  shippingAddress: AddressSchema,
});
```

### Output Schemas

```typescript
// Handle Prisma types
const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string(),
  name: z.string(),
  // Prisma returns Date objects
  createdAt: z.coerce.date(),
  updatedAt: z.coerce.date(),
  // Prisma Decimal → number
  balance: z.any().transform((val) => Number(val)),
});

// Nullable response
.output(UserSchema.nullable())

// Array response
.output(z.array(UserSchema))

// Paginated response
.output(z.object({
  data: z.array(UserSchema),
  meta: z.object({
    page: z.number(),
    limit: z.number(),
    total: z.number(),
    totalPages: z.number(),
  }),
}))
```

## Error Handling

### VeloxError

```typescript
import { VeloxError } from '@veloxts/core';

getUser: procedure()
  .input(z.object({ id: z.string().uuid() }))
  .query(async ({ input, ctx }) => {
    const user = await ctx.db.user.findUnique({ where: { id: input.id } });

    if (!user) {
      throw VeloxError.notFound('User', input.id);
    }

    return user;
  }),
```

### Error Types

| Method | HTTP | Use Case |
|--------|------|----------|
| `VeloxError.notFound(entity, id)` | 404 | Resource not found |
| `VeloxError.unauthorized(message)` | 401 | Not authenticated |
| `VeloxError.forbidden(message)` | 403 | Not authorized |
| `VeloxError.badRequest(message)` | 400 | Invalid input |
| `VeloxError.conflict(message)` | 409 | Duplicate resource |
| `VeloxError.internal(message)` | 500 | Server error |

## Complete Example

```typescript
import { procedure, procedures, paginationInputSchema, z } from '@veloxts/velox';
import { authenticated, hasRole } from '@veloxts/auth';
import { VeloxError } from '@veloxts/core';

// Schemas
const PostSchema = z.object({
  id: z.string().uuid(),
  title: z.string(),
  content: z.string(),
  authorId: z.string().uuid(),
  publishedAt: z.coerce.date().nullable(),
  createdAt: z.coerce.date(),
  updatedAt: z.coerce.date(),
});

const CreatePostInput = z.object({
  title: z.string().min(1).max(255),
  content: z.string().min(1),
});

const UpdatePostInput = CreatePostInput.partial();

// Procedures
export const postProcedures = procedures('posts', {
  // Public: list published posts
  listPosts: procedure()
    .input(paginationInputSchema.optional())
    .output(z.object({
      data: z.array(PostSchema),
      meta: z.object({
        page: z.number(),
        limit: z.number(),
        total: z.number(),
        totalPages: z.number(),
      }),
    }))
    .query(async ({ input, ctx }) => {
      const page = input?.page ?? 1;
      const limit = input?.limit ?? 10;
      const skip = (page - 1) * limit;

      const where = { publishedAt: { not: null } };

      const [data, total] = await Promise.all([
        ctx.db.post.findMany({ where, skip, take: limit }),
        ctx.db.post.count({ where }),
      ]);

      return {
        data,
        meta: { page, limit, total, totalPages: Math.ceil(total / limit) },
      };
    }),

  // Public: get single post
  getPost: procedure()
    .input(z.object({ id: z.string().uuid() }))
    .output(PostSchema.nullable())
    .query(async ({ input, ctx }) => {
      return ctx.db.post.findUnique({ where: { id: input.id } });
    }),

  // Auth required: create post
  createPost: procedure()
    .guard(authenticated)
    .input(CreatePostInput)
    .output(PostSchema)
    .mutation(async ({ input, ctx }) => {
      return ctx.db.post.create({
        data: {
          ...input,
          authorId: ctx.user!.id,
        },
      });
    }),

  // Auth required: update own post
  updatePost: procedure()
    .guard(authenticated)
    .input(z.object({ id: z.string().uuid() }).merge(UpdatePostInput))
    .output(PostSchema)
    .mutation(async ({ input, ctx }) => {
      const { id, ...data } = input;

      const post = await ctx.db.post.findUnique({ where: { id } });

      if (!post) {
        throw VeloxError.notFound('Post', id);
      }

      if (post.authorId !== ctx.user!.id) {
        throw VeloxError.forbidden('You can only edit your own posts');
      }

      return ctx.db.post.update({ where: { id }, data });
    }),

  // Admin only: delete any post
  deletePost: procedure()
    .guard(hasRole('admin'))
    .input(z.object({ id: z.string().uuid() }))
    .output(z.object({ success: z.boolean() }))
    .mutation(async ({ input, ctx }) => {
      await ctx.db.post.delete({ where: { id: input.id } });
      return { success: true };
    }),

  // Custom route: publish post
  publishPost: procedure()
    .guard(authenticated)
    .input(z.object({ id: z.string().uuid() }))
    .output(PostSchema)
    .rest({ method: 'POST', path: '/posts/:id/publish' })
    .mutation(async ({ input, ctx }) => {
      const post = await ctx.db.post.findUnique({ where: { id: input.id } });

      if (!post) {
        throw VeloxError.notFound('Post', input.id);
      }

      if (post.authorId !== ctx.user!.id) {
        throw VeloxError.forbidden('You can only publish your own posts');
      }

      return ctx.db.post.update({
        where: { id: input.id },
        data: { publishedAt: new Date() },
      });
    }),
});
```
