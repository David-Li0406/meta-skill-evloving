---
name: nodejs-best-practices
description: Use this skill when you need to make informed decisions about Node.js development, including framework selection, async patterns, security, and architecture.
---

# Node.js Best Practices

> Principles and decision-making for Node.js development in 2025.
> **Learn to THINK, not memorize code patterns.**

## ⚠️ How to Use This Skill

This skill teaches **decision-making principles**, not fixed code to copy.

- ASK user for preferences when unclear.
- Choose framework/pattern based on CONTEXT.
- Don't default to the same solution every time.

## 1. Framework Selection (2025)

### Decision Tree

```
What are you building?
│
├── Edge/Serverless (Cloudflare, Vercel)
│   └── Hono (zero-dependency, ultra-fast cold starts)
│
├── High Performance API
│   └── Fastify (2-3x faster than Express)
│
├── Enterprise/Team familiarity
│   └── NestJS (structured, DI, decorators)
│
├── Legacy/Stable/Maximum ecosystem
│   └── Express (mature, most middleware)
│
└── Full-stack with frontend
    └── Next.js API Routes or tRPC
```

### Comparison Principles

| Factor             | Hono             | Fastify     | Express          |
| ------------------ | ---------------- | ----------- | ---------------- |
| **Best for**       | Edge, serverless | Performance | Legacy, learning |
| **Cold start**     | Fastest          | Fast        | Moderate         |
| **Ecosystem**      | Growing          | Good        | Largest          |
| **TypeScript**     | Native           | Excellent   | Good             |
| **Learning curve** | Low              | Medium      | Low              |

### Selection Questions to Ask

1. What's the deployment target?
2. Is cold start time critical?
3. Does the team have existing experience?
4. Is there legacy code to maintain?

## 2. Runtime Considerations (2025)

### Native TypeScript

```
Node.js 22+: --experimental-strip-types
├── Run .ts files directly
├── No build step needed for simple projects
└── Consider for: scripts, simple APIs
```

### Module System Decision

```
ESM (import/export)
├── Modern standard
├── Better tree-shaking
├── Async module loading
└── Use for: new projects

CommonJS (require)
├── Legacy compatibility
├── More npm packages support
└── Use for: existing codebases, some edge cases
```

### Runtime Selection

| Runtime     | Best For                            |
| ----------- | ----------------------------------- |
| **Node.js** | General purpose, largest ecosystem   |
| **Bun**     | Performance, built-in bundler       |
| **Deno**    | Security-first, built-in TypeScript  |

## 3. Architecture Principles

### Layered Structure Concept

```
Request Flow:
│
├── Controller/Route Layer
│   ├── Handles HTTP specifics
```