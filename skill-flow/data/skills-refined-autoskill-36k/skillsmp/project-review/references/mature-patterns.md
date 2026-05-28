# mature patterns

patterns extracted from mature projects. use for comparison during audits.

## source projects

| project | maturity | strengths |
|---------|----------|-----------|
| arbor | high | TDD, convex patterns, turborepo |
| webs | high | web agents, playwright, TDD |
| kumori | medium | notifications, AI queues |
| koto | medium | pipedream, onboarding |
| sine | medium | iOS integration |

## file structure patterns

### turborepo layout

```
project/
├── apps/
│   ├── web/           # Next.js app
│   └── api/           # API server (if separate)
├── packages/
│   ├── backend/       # @repo/backend (convex)
│   ├── ui/            # @repo/ui (shared components)
│   └── shared/        # @repo/shared (utilities)
├── turbo.json
├── package.json       # workspace root
└── pnpm-workspace.yaml
```

**audit:** does project follow apps/packages split?

### convex directory

```
packages/backend/convex/
├── _generated/        # auto-generated
├── schema.ts          # data schema
├── auth.ts            # authentication
├── http.ts            # HTTP endpoints
├── crons.ts           # scheduled jobs
├── functions/         # organized by domain
│   ├── users/
│   ├── messages/
│   └── ...
└── lib/               # shared utilities
```

**audit:** are convex functions organized by domain?

## test patterns

### colocation

```
src/
├── components/
│   ├── Button.tsx
│   └── Button.test.tsx    # colocated
├── hooks/
│   ├── useAuth.ts
│   └── useAuth.test.ts    # colocated
```

**audit:** are tests next to source files?

### naming

| pattern | convention |
|---------|------------|
| unit tests | `*.test.ts` |
| integration | `*.integration.test.ts` |
| e2e | `*.e2e.ts` or `e2e/*.spec.ts` |

### convex-test patterns

```typescript
import { convexTest } from "convex-test";
import schema from "./schema";
import { api } from "./_generated/api";

describe("users", () => {
  const t = convexTest(schema);

  test("create user", async () => {
    const userId = await t.mutation(api.users.create, {
      name: "Test User",
    });
    expect(userId).toBeDefined();
  });
});
```

**audit:** are convex functions tested with convex-test?

### playwright patterns

```typescript
import { test, expect } from "@playwright/test";

test("user flow", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading")).toContainText("Welcome");
});
```

**audit:** are critical user flows covered by e2e tests?

## schema patterns

### convex schema

```typescript
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  users: defineTable({
    name: v.string(),
    email: v.string(),
    clerkId: v.string(),
    createdAt: v.number(),
  })
    .index("by_clerk_id", ["clerkId"])
    .index("by_email", ["email"]),
});
```

**audit:** are indexes defined for query patterns?

### validator patterns

```typescript
import { v } from "convex/values";

// define validators separately for reuse
export const userValidator = v.object({
  name: v.string(),
  email: v.string(),
});

// use in functions
export const createUser = mutation({
  args: userValidator,
  handler: async (ctx, args) => { ... }
});
```

**audit:** are validators defined and reused?

## import patterns

### path aliases

```typescript
// tsconfig.json paths
{
  "paths": {
    "@/*": ["./src/*"],
    "@/components/*": ["./src/components/*"],
    "@repo/backend": ["../../packages/backend"],
    "@repo/ui": ["../../packages/ui"]
  }
}
```

**audit:** are path aliases configured and used consistently?

### barrel exports

```typescript
// components/index.ts
export { Button } from "./Button";
export { Card } from "./Card";
export { Modal } from "./Modal";

// usage
import { Button, Card } from "@/components";
```

**audit:** are barrel exports used for cleaner imports?

## commit patterns

### conventional commits

```
feat(ARB-123): add user authentication flow
fix(ARB-124): resolve race condition in sync
refactor(ARB-125): extract shared validation logic
test(ARB-126): add e2e tests for checkout
```

**audit:** do commits follow conventional format with issue refs?

## env patterns

### env files

```
.env.local           # local overrides (gitignored)
.env.example         # template (committed)
.env.development     # development defaults
.env.production      # production defaults
```

**audit:** does .env.example exist with all required vars?

## gap checklist

when auditing against mature patterns:

- [ ] turborepo: apps/packages structure?
- [ ] convex: domain-organized functions?
- [ ] tests: colocated with source?
- [ ] tests: convex-test for backend?
- [ ] tests: playwright for e2e?
- [ ] schema: proper indexes?
- [ ] validators: defined and reused?
- [ ] imports: path aliases configured?
- [ ] commits: conventional with issue refs?
- [ ] env: .env.example exists?
