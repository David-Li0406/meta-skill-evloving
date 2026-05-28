# API Package Agent Reference

Reference to `.claude/agent/api.md` for packages/api development.

## When to Use API Agent

Use the api agent when working on:
- REST API endpoints
- Database schema and migrations
- Business logic services
- Repository pattern implementation
- Authentication and authorization
- API validation with Zod

## Critical Rules Summary

### 1. Table Names - SINGULAR
```typescript
// ✅ CORRECT
import { profile, asset, socialLink } from "../../db/schema"

// ❌ WRONG
import { profiles, assets } from "../../db/schema"
```

### 2. Service Registration - MUST register in plugins/services.ts
```typescript
export const servicesPlugin = new Elysia({ name: "services" }).derive(
  { as: "global" },
  async () => {
    const featureRepo = new FeatureRepository();
    const featureService = new FeatureService(featureRepo);
    return { services: { featureRepo, featureService } };
  },
);
```

### 3. Repository Pattern
```typescript
export class FeatureRepository {
  async findOne(ctx: RequestContext, id: string) {
    return db.query.feature.findFirst({
      where: and(eq(feature.id, id), eq(feature.userId, ctx.userId)),
    });
  }

  async create(ctx: RequestContext, data: NewFeature) {
    const [result] = await db.insert(feature)
      .values({ ...data, userId: ctx.userId })
      .returning();
    return result;
  }
}
```

### 4. Business Service
```typescript
export class FeatureService {
  constructor(private repo: FeatureRepository) {}

  async getOne(ctx: RequestContext, id: string) {
    const item = await this.repo.findOne(ctx, id);
    if (!item) throw new NotFoundException("Not found");
    return item;
  }
}
```

### 5. Route Handler
```typescript
export const featureRoutes = new Elysia({ prefix: "/feature" })
  .use(errorMiddleware)
  .use(servicesPlugin)
  .use(authGuard)
  .get("/", ({ ctx, services }) => services.featureService.getAll(ctx!))
  .post("/", ({ body, ctx, services, set }) => {
    set.status = 201;
    return services.featureService.create(ctx!, body);
  }, { body: t.Object({ name: t.String() }) });
```

### 6. Relations - Access via name
```typescript
// ✅ CORRECT
const platform = click.socialLink.platform;

// ❌ WRONG
const platform = click.platform;
```

### 7. HTTP Exceptions
```typescript
throw new NotFoundException("Profile not found");     // 404
throw new ConflictException("Username exists");       // 409
throw new BadRequestException("Invalid data");        // 400
```

### 8. Type Callbacks
```typescript
// ✅ CORRECT
items.reduce((sum: number, item: Item) => sum + item.value, 0);

// ❌ WRONG
items.reduce((sum, item) => sum + item.value, 0);
```

## Full Agent Documentation

See `.claude/agent/api.md` for complete reference.
