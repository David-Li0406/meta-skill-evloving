---
name: cloudflare-workers-development
description: Comprehensive Cloudflare Workers development guidance for building serverless functions with TypeScript, Hono, and Workers Runtime API
---

## What I Cover

- Setting up Cloudflare Workers with TypeScript and Wrangler configuration
- Building REST APIs using Hono framework with middleware (CORS, authentication)
- Creating OpenAPI-documented endpoints with chanfana and Zod validation
- Managing environment variables and runtime bindings
- Implementing authentication patterns (JWT tokens, OTP login)
- Integrating with external APIs (client factories, error handling)
- Deploying Workers with Wrangler CLI and observability features

## Common Patterns

### Hono App Setup with Middleware
```typescript
const app = new Hono<{ Bindings: Env }>();

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

### Chanfana OpenAPI Route Classes
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
    return new GoPayClientMock(apiUrl, token);
  }
  return new GoPayClient(apiUrl, token);
};
```

## Best Practices

- **Type Safety**: Use TypeScript interfaces for request/response types and environment bindings
- **Security**: Implement proper CORS policies and validate all inputs with Zod schemas
- **Authentication**: Use Bearer token authentication for protected routes, exclude public endpoints
- **Configuration**: Store API URLs and feature flags in environment variables via wrangler.jsonc
- **API Documentation**: Define comprehensive OpenAPI schemas with examples and error responses
- **Error Handling**: Return appropriate HTTP status codes and structured error responses
- **Testing**: Use mock clients during development to avoid external API dependencies
- **Performance**: Set appropriate cache headers and use observability for monitoring
- **Deployment**: Use Wrangler for local development and production deployment with compatibility dates

## Related Skills

- `sveltekit-development`: For frontend integration with Workers APIs
- `frontend-developer`: For building client applications that consume Worker endpoints
- `deployment-specialist`: For advanced deployment strategies and CI/CD with Cloudflare
- `backend-developer`: For general API design and server-side development patterns</content>
<parameter name="filePath">D:\Git\GoPayShortcuts\.opencode\skill\cloudflare-workers-development\SKILL.md