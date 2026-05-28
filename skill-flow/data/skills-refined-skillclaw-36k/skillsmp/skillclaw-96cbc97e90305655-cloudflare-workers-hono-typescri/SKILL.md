---
name: cloudflare-workers-hono-typescript-development
description: Use this skill when you need to build high-performance, edge-first APIs with Hono and TypeScript for Cloudflare Workers, Deno, Bun, and Node.js.
---

# Skill body

## Overview

This skill provides comprehensive guidelines for developing serverless functions and APIs using Hono and TypeScript, specifically tailored for Cloudflare Workers and similar environments.

## TypeScript General Guidelines

### Basic Principles

- Use English for all code and documentation.
- Always declare types for variables and functions (parameters and return values).
- Avoid using `any` type; create necessary types instead.
- Use JSDoc to document public classes and methods.
- Write concise, maintainable, and technically accurate code.
- Use functional and declarative programming patterns; avoid classes.
- Prefer iteration and modularization to adhere to DRY principles.

### Nomenclature

- Use PascalCase for types and interfaces.
- Use camelCase for variables, functions, and methods.
- Use kebab-case for file and directory names.
- Use UPPERCASE for environment variables.
- Use descriptive variable names with auxiliary verbs: `isLoading`, `hasError`, `canDelete`.
- Start each function with a verb.

### Functions

- Write short functions with a single purpose.
- Use arrow functions for handlers and middleware.
- Prefer the RO-RO pattern: Receive an Object, Return an Object.
- Use default parameters instead of null checks.

### Types and Interfaces

- Prefer interfaces over types for object shapes.
- Avoid enums; use maps or const objects instead for better type safety.
- Use Zod for runtime validation with inferred types.
- Use `readonly` for immutable properties.
- Use `import type` for type-only imports.

## Hono-Specific Guidelines

### Project Structure

```
src/
  routes/
    {resource}/
      index.ts
      handlers.ts
      validators.ts
  middleware/
    auth.ts
    cors.ts
    logger.ts
  services/
    {domain}Service.ts
  types/
    index.ts
  utils/
  config/
  index.ts
```

### App Initialization

```typescript
import { Hono } from 'hono';

// Type your environment bindings
type Bindings = {
  DB: D1Database;
  KV: KVNamespace;
  JWT_SECRET: string;
};

type Variables = {
  user: User;
};

const app = new Hono<{ Bindings: Bindings; Variables: Variables }>();
```

### Middleware Setup

```typescript
app.use("*", cors({
  origin: ["http://localhost:5173", "https://tobbe3108.github.io"],
  allowMethods: ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
  allowHeaders: ["Content-Type", "Authorization"],
  credentials: true,
}));
```

### Global Authentication Middleware

```typescript
app.use("/api/*", async (c, next) => {
  const path = c.req.path;
  if (path === "/api/login" || path === "/api/menu") {
    await next();
    return;
  }

  const token = c.req.header("Authorization");
  if (!token?.startsWith("Bearer")) {
    return c.text("Missing or invalid Authorization header", 401);
  }

  await next();
});
```

### Routing

- Use method chaining for clean route definitions.
- Group related routes with `app.route()`.
- Use route parameters with proper typing.

### Example Route Class

```typescript
export class Login extends OpenAPIRoute {
  schema = {
    tags: ["Auth"],
    summary: "Login with one-time password (OTP)",
    request: {
      body: contentJson(z.object({
        otp: z.string().describe("One-time password (OTP) received via email"),
      })),
    },
    responses: {
      "200": contentJson(z.object({
        token: Str({ example: "eyJhbGciOi..." }).describe("JWT authentication token"),
      })),
    },
  };

  async handle(c: AppContext) {
    const data = await this.getValidatedData<typeof this.schema>();
    const client = createGoPayClient(c);
    const response = await client.login(data.body.otp);
    return { token: response.authentication.token };
  }
}
```

### Client Factory Pattern

```typescript
export const createGoPayClient = (context: AppContext): GoPayClient => {
  const apiUrl = context.env.GOPAY_API_URL;
  const token = context.req.header("Authorization")?.replace("Bearer", "").trim();

  if (context.env.USE_LOCAL_MOCK_CLIENTS === true) {
    return new GoPayClientMock(apiUrl);
  }
  return new GoPayClient(apiUrl, token);
};
```

## Deployment

- Deploy Workers with Wrangler CLI and utilize observability features for monitoring and debugging.
```bash
wrangler publish
```