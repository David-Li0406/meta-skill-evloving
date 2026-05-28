---
name: nodejs-best-practices
description: Node.js development principles and decision-making for 2025+. This skill should be used when writing, reviewing, or refactoring Node.js backend code. Triggers on tasks involving API development, framework selection, async patterns, security, database access, or performance optimization.
license: MIT
metadata:
  author: mine-vibe
  version: "1.0.0"
---

# Node.js Best Practices

Comprehensive guide for Node.js development in 2025+, designed for AI agents and LLMs. Contains 40+ rules across 10 categories, prioritized by impact to guide automated code generation and refactoring.

**Philosophy:** Learn to THINK, not memorize code patterns. Every project deserves fresh consideration based on its requirements.

## When to Apply

Reference these guidelines when:
- Building new Node.js APIs or backend services
- Choosing between frameworks (Express, Fastify, Hono, NestJS)
- Implementing async operations and error handling
- Setting up validation and security measures
- Working with databases (Prisma, Drizzle)
- Deploying to Edge/Serverless environments
- Reviewing or refactoring existing Node.js code

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Framework Selection | CRITICAL | `framework-` |
| 2 | Error Handling | CRITICAL | `error-` |
| 3 | Async Patterns | CRITICAL | `async-` |
| 4 | Security | CRITICAL | `security-` |
| 5 | Runtime Considerations | HIGH | `runtime-` |
| 6 | Architecture Principles | HIGH | `architecture-` |
| 7 | Validation | HIGH | `validation-` |
| 8 | Database Access | HIGH | `database-` |
| 9 | Testing | MEDIUM | `testing-` |
| 10 | Logging & Monitoring | MEDIUM | `logging-` |

## Quick Reference

### 1. Framework Selection (CRITICAL)

- `framework-context-choice` - Choose framework based on context, not habit
- `framework-edge-hono` - Use Hono for Edge/Serverless (Cloudflare, Vercel Edge)
- `framework-performance-fastify` - Use Fastify for high-throughput APIs (>10k req/s)
- `framework-enterprise-nestjs` - Use NestJS for enterprise/structured teams
- `framework-legacy-express` - Use Express for legacy codebases only
- `framework-fullstack-nextjs` - Use Next.js API Routes or tRPC for full-stack

### 2. Error Handling (CRITICAL)

- `error-custom-classes` - Create custom error classes extending base AppError
- `error-centralized-handler` - Use centralized error handler middleware
- `error-operational-vs-programmer` - Distinguish operational vs programmer errors
- `error-no-swallow` - Never catch errors and ignore them
- `error-status-codes` - Use appropriate HTTP status codes (400, 401, 403, 404, 409, 422, 500)
- `error-no-internal-details` - Never expose internal error details to clients

### 3. Async Patterns (CRITICAL)

- `async-parallel-promise-all` - Use Promise.all() for independent operations
- `async-fault-tolerance-allsettled` - Use Promise.allSettled() when some can fail
- `async-timeout-race` - Use Promise.race() for timeout patterns
- `async-no-sync-methods` - Never use sync methods in production (readFileSync, etc.)
- `async-worker-threads` - Use worker threads for CPU-intensive work
- `async-streaming` - Use streams for large data processing

### 4. Security (CRITICAL)

- `security-input-validation` - Validate all inputs at boundaries
- `security-parameterized-queries` - Use parameterized queries, never string concatenation
- `security-password-hashing` - Use bcrypt (rounds: 12) or argon2 for passwords
- `security-jwt-verify` - Always verify JWT signature AND expiry
- `security-rate-limiting` - Implement rate limiting on all endpoints
- `security-helmet` - Use helmet.js for security headers
- `security-cors` - Configure CORS properly
- `security-secrets-env` - Store secrets in environment variables only

### 5. Runtime Considerations (HIGH)

- `runtime-node22-native-ts` - Consider Node.js 22+ native TypeScript for simple projects
- `runtime-esm-new-projects` - Use ESM (import/export) for new projects
- `runtime-commonjs-legacy` - Use CommonJS only for legacy compatibility
- `runtime-bun-performance` - Consider Bun for performance-critical applications
- `runtime-deno-security` - Consider Deno for security-first requirements

### 6. Architecture Principles (HIGH)

- `architecture-layered` - Use layered architecture (Controller → Service → Repository)
- `architecture-thin-controllers` - Keep controllers thin, business logic in services
- `architecture-framework-agnostic` - Keep services framework-agnostic
- `architecture-dependency-injection` - Use dependency injection for testability
- `architecture-single-responsibility` - Each layer has single responsibility
- `architecture-simplify-small` - Simplify structure for small projects/prototypes

### 7. Validation (HIGH)

- `validation-zod-typescript` - Use Zod for TypeScript-first validation
- `validation-valibot-bundle` - Use Valibot for smaller bundle size
- `validation-boundary` - Validate at API entry points (request body/params)
- `validation-env-startup` - Validate environment variables at startup
- `validation-fail-fast` - Fail fast with clear error messages
- `validation-middleware` - Use validation middleware for routes

### 8. Database Access (HIGH)

- `database-prisma-typesafe` - Use Prisma for TypeScript-first type safety
- `database-drizzle-performance` - Use Drizzle for SQL-like syntax and performance
- `database-transactions` - Use transactions for multi-step operations
- `database-select-fields` - Select only needed fields
- `database-pagination` - Implement pagination for list queries
- `database-avoid-n-plus-1` - Avoid N+1 queries with eager loading
- `database-connection-pooling` - Use connection pooling

### 9. Testing (MEDIUM)

- `testing-node-builtin` - Use Node.js built-in test runner (node:test)
- `testing-vitest-modern` - Use Vitest for modern testing with good DX
- `testing-supertest-integration` - Use Supertest for API integration tests
- `testing-playwright-e2e` - Use Playwright for E2E tests
- `testing-critical-paths` - Prioritize testing critical paths (auth, payments)
- `testing-mock-external` - Mock external dependencies

### 10. Logging & Monitoring (MEDIUM)

- `logging-pino-structured` - Use Pino for structured JSON logging
- `logging-levels` - Use appropriate log levels (error, warn, info, debug)
- `logging-context` - Include request context (requestId, userId)
- `logging-no-sensitive` - Never log sensitive data (passwords, tokens)
- `logging-health-check` - Implement health check endpoints
- `logging-correlation-id` - Use correlation IDs for distributed tracing

---

## Decision Trees

### Framework Selection

```
What are you building?
│
├── Edge/Serverless (Cloudflare Workers, Vercel Edge)
│   └── Hono ✓ (zero-dependency, ultra-fast cold starts)
│
├── High Performance API (>10k req/s)
│   └── Fastify ✓ (2-3x faster than Express)
│
├── Enterprise/Team with Java/C# background
│   └── NestJS ✓ (structured, DI, decorators)
│
├── Legacy/Maximum ecosystem compatibility
│   └── Express ✓ (mature, most middleware)
│
└── Full-stack with frontend
    └── Next.js API Routes or tRPC ✓
```

### Module System Selection

```
What type of project?
│
├── New project
│   └── ESM (import/export) ✓
│
├── Legacy codebase
│   └── CommonJS (require) ✓
│
└── Library (publishing to npm)
    └── Dual ESM + CommonJS ✓
```

### Database ORM Selection

```
What's the priority?
│
├── Type safety + DX
│   └── Prisma ✓
│
├── Performance + SQL-like syntax
│   └── Drizzle ✓
│
├── Type-safe query builder
│   └── Kysely ✓
│
└── Decorator-based (enterprise)
    └── TypeORM ✓
```

---

## Anti-Patterns to Avoid

### ❌ DON'T:

- Use Express for new edge/serverless projects
- Use sync methods (`readFileSync`, etc.) in production
- Put business logic in controllers
- Skip input validation
- Hardcode secrets
- Trust external data without validation
- Block event loop with CPU work
- Use `any` type in TypeScript
- Catch errors and ignore them
- String concatenate SQL queries

### ✅ DO:

- Choose framework based on context
- Ask user for preferences when unclear
- Use layered architecture for growing projects
- Validate all inputs at boundaries
- Use environment variables for secrets
- Use parameterized queries
- Profile before optimizing
- Use TypeScript strict mode
- Log errors with context
- Write tests for critical paths

---

## Performance Checklist

Before shipping:

- [ ] **Framework appropriate?** Chosen based on deployment target
- [ ] **Async patterns correct?** No blocking operations
- [ ] **Error handling complete?** Centralized handler, custom errors
- [ ] **Security measures?** Validation, rate limiting, helmet
- [ ] **Database optimized?** Indexes, pagination, select fields
- [ ] **Environment validated?** Env vars checked at startup
- [ ] **Logging configured?** Structured logs, no sensitive data
- [ ] **Health checks?** Endpoint for load balancers

---

## Questions to Ask Before Implementing

1. What's the deployment target? (Edge, serverless, traditional server)
2. Is cold start time critical? (< 50ms requirement?)
3. Does the team have existing framework experience?
4. What's the expected traffic volume?
5. Is there legacy Express code to maintain?

---

## Full Compiled Document

For detailed code examples, implementation patterns, and comprehensive explanations: `AGENTS.md`

Each section in AGENTS.md contains:
- Detailed explanations of why patterns matter
- Incorrect vs Correct code comparisons
- Copy-paste ready implementations
- Framework-specific examples (Hono, Fastify, Express)
- Decision trees with detailed reasoning
