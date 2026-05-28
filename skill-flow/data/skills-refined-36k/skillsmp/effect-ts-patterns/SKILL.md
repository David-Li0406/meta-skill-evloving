---
name: effect-ts-patterns
description: Patterns and best practices for Effect-TS in the Nuclom codebase. Use when writing API routes, services, or any code using Effect-TS. Covers Effect.gen, error handling, services, layers, and common pitfalls.
---

# Effect-TS Patterns for Nuclom

This skill documents the Effect-TS patterns used throughout the Nuclom codebase. Effect-TS provides type-safe error handling and dependency injection.

## Quick Reference

### API Route Template

```typescript
import { Effect } from "effect";
import type { NextRequest } from "next/server";
import { createFullLayer, handleEffectExit } from "@/lib/api-handler";
import { Auth } from "@/lib/effect/services/auth";

export async function GET(request: NextRequest) {
  const effect = Effect.gen(function* () {
    // 1. Authenticate
    const auth = yield* Auth;
    const { user } = yield* auth.getSession(request.headers);

    // 2. Use repository services
    const repo = yield* VideoRepository;
    return yield* repo.findByUserId(user.id);
  });

  // 3. Provide layer and run
  const runnable = Effect.provide(effect, createFullLayer());
  const exit = await Effect.runPromiseExit(runnable);

  // 4. Handle exit
  return handleEffectExit(exit);
}
```

## Core Patterns

### 1. Effect.gen for Sequential Code

Always use `Effect.gen` for sequential async operations:

```typescript
// ✅ CORRECT: Use Effect.gen with yield*
const program = Effect.gen(function* () {
  const user = yield* getUser(id);
  const videos = yield* getVideosForUser(user.id);
  return { user, videos };
});

// ❌ WRONG: Don't use flatMap chains
const program = getUser(id).pipe(
  Effect.flatMap(user => getVideosForUser(user.id).pipe(
    Effect.map(videos => ({ user, videos }))
  ))
);
```

### 2. Error Handling with Data.TaggedError

```typescript
import { Data, Effect } from "effect";

// Define tagged errors
class NotFoundError extends Data.TaggedError("NotFoundError")<{
  readonly message: string;
  readonly entity: string;
}> {}

class ValidationError extends Data.TaggedError("ValidationError")<{
  readonly message: string;
  readonly field: string;
}> {}

// Use in effects
const findVideo = (id: string) => Effect.gen(function* () {
  const video = yield* repo.findById(id);
  if (!video) {
    return yield* Effect.fail(new NotFoundError({
      message: `Video ${id} not found`,
      entity: "video"
    }));
  }
  return video;
});
```

### 3. Error Recovery with catchTag

Handle errors close to where they occur:

```typescript
const program = Effect.gen(function* () {
  const video = yield* findVideo(id);
  return video;
}).pipe(
  Effect.catchTag("NotFoundError", () => Effect.succeed(null)),
  Effect.catchTag("ValidationError", (e) =>
    Effect.fail(new BadRequestError({ message: e.message }))
  )
);
```

### 4. Repository Services

Always use repository services, never direct `db` access:

```typescript
// ✅ CORRECT: Use repository service
const effect = Effect.gen(function* () {
  const repo = yield* VideoRepository;
  return yield* repo.findById(id);
});

// ❌ WRONG: Direct db access in route
const effect = Effect.gen(function* () {
  return await db.query.videos.findFirst({...}); // Don't do this!
});
```

### 5. Layer Provision

Always provide layers before execution:

```typescript
// For authenticated routes
const runnable = Effect.provide(effect, createFullLayer());

// For public routes
const runnable = Effect.provide(effect, createPublicLayer());
```

## Common Pitfalls

### ❌ await inside Effect.gen

```typescript
// ❌ WRONG: Never await inside Effect.gen
const program = Effect.gen(function* () {
  const result = await Effect.runPromise(someEffect); // NO!
  return result;
});

// ✅ CORRECT: Use yield*
const program = Effect.gen(function* () {
  const result = yield* someEffect;
  return result;
});
```

### ❌ Forgetting to provide layers

```typescript
// ❌ WRONG: Running without layer
const result = await Effect.runPromise(effect);

// ✅ CORRECT: Provide layer first
const runnable = Effect.provide(effect, createFullLayer());
const result = await Effect.runPromise(runnable);
```

### ❌ Creating effects without executing

```typescript
// ❌ WRONG: Effect created but never run
Effect.gen(function* () {
  yield* doSomething();
}); // This does nothing!

// ✅ CORRECT: Execute the effect
const effect = Effect.gen(function* () {
  yield* doSomething();
});
await Effect.runPromise(Effect.provide(effect, layer));
```

## API Route Checklist

Before completing an API route, verify:

- [ ] Uses `Effect.gen` for business logic
- [ ] Authenticates with `Auth` service (if needed)
- [ ] Uses repository services (not direct `db`)
- [ ] Custom errors extend `Data.TaggedError`
- [ ] Errors handled with `catchTag`
- [ ] Layer provided with `createFullLayer()` or `createPublicLayer()`
- [ ] Exit handled with `handleEffectExit()` or `handleEffectExitWithStatus()`
- [ ] No `await Effect.runPromise()` inside `Effect.gen`

## Service Pattern

```typescript
import { Context, Effect, Layer } from "effect";

// Define service interface
interface VideoService {
  findById(id: string): Effect.Effect<Video | null, NotFoundError>;
  create(data: CreateVideoInput): Effect.Effect<Video, ValidationError>;
}

// Create tag
export class VideoService extends Context.Tag("VideoService")<
  VideoService,
  VideoService
>() {}

// Implement service
export const VideoServiceLive = Layer.succeed(VideoService, {
  findById: (id) => Effect.gen(function* () {
    // implementation
  }),
  create: (data) => Effect.gen(function* () {
    // implementation
  }),
});
```

## See Also

- `CLAUDE.md` - Project-wide patterns
- `content/docs/internal/architecture/effect-best-practices.mdx` - Full documentation
- `src/lib/effect/services/` - Existing service implementations
