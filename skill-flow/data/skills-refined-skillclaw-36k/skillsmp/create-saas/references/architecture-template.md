# Architecture Template & Guidelines

Reference for designing technical architecture.

---

## Architecture Philosophy

**Good architecture is:**

- Simple (minimum complexity for requirements)
- Documented (decisions and rationale)
- Cost-aware (solo dev budget reality)
- Practical (uses proven patterns)

**Over-engineering signs:**

- Tools you don't need yet
- "Future-proofing" for unknown requirements
- Complex patterns for simple problems
- More than 2 weeks to MVP

---

## Architecture Document Structure

````markdown
# Technical Architecture: {Product Name}

## Overview

**Stack Summary:**

- Framework: Next.js 15 with App Router
- Database: {choice} + Prisma
- Auth: Better Auth with {method}
- Deployment: Vercel

## Frontend Architecture

### Core Stack

| Tool         | Purpose     |
| ------------ | ----------- |
| Next.js 15   | Framework   |
| TypeScript   | Type safety |
| Tailwind CSS | Styling     |
| shadcn/ui    | Components  |

### State Management

| Type         | Solution              |
| ------------ | --------------------- |
| Server state | TanStack Query        |
| URL state    | nuqs                  |
| Form state   | React Hook Form + Zod |
| Client state | Zustand (if needed)   |

### Data Fetching

- Default: Server Components
- Dynamic: TanStack Query
- Mutations: Server Actions

## Backend Architecture

### API Layer

- Server Actions via next-safe-action
- Validation with Zod v4
- Rate limiting: {approach}

### Database

- ORM: Prisma
- Database: {Neon/Supabase}
- Migrations: Prisma Migrate

### Schema Overview

```prisma
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  createdAt DateTime @default(now())
}

// Feature-specific models...
```
````

## Infrastructure

### Deployment

- Platform: Vercel
- Environments: dev, preview, production

### External Services

| Service | Purpose  | When to add         |
| ------- | -------- | ------------------- |
| Resend  | Email    | When sending emails |
| Stripe  | Payments | When monetizing     |

## Folder Structure

```
/
├── app/
│   ├── (auth)/
│   ├── (dashboard)/
│   └── api/
├── src/
│   ├── components/
│   ├── lib/
│   ├── actions/
│   └── hooks/
└── prisma/
```

## Feature Implementation Map

| PRD Feature | How to Build              |
| ----------- | ------------------------- |
| {Feature 1} | {Implementation approach} |
| {Feature 2} | {Implementation approach} |

## Architecture Decisions

### ADR-001: {Decision Title}

- **Context**: {Why needed}
- **Decision**: {What we chose}
- **Rationale**: {Why this choice}
- **Trade-offs**: {What we give up}

## Cost Estimation

| Service   | Monthly Cost |
| --------- | ------------ |
| Vercel    | $0-20        |
| Database  | $0-19        |
| Email     | $0           |
| **Total** | ~$0-40       |

```

---

## Common Patterns

### Authentication Pattern
```

User → Login Page → Better Auth → Session Cookie → Protected Routes

```

### Data Mutation Pattern
```

Form Submit → Server Action → Zod Validation → Prisma → Revalidate → UI Update

```

### API Route Pattern
```

Request → Route Handler → Zod Validation → Business Logic → Response

```

---

## Folder Structure Explained

```

app/
├── (auth)/ # Public auth pages
│ ├── login/
│ └── signup/
├── (dashboard)/ # Protected pages (layout with auth check)
│ ├── dashboard/
│ ├── settings/
│ └── [feature]/
├── (marketing)/ # Public marketing pages
│ └── page.tsx # Landing page
└── api/ # API routes (if needed)
└── webhooks/

src/
├── components/
│ ├── ui/ # shadcn components
│ ├── forms/ # Form components
│ └── [feature]/ # Feature-specific components
├── lib/
│ ├── auth.ts # Auth configuration
│ ├── prisma.ts # Prisma client
│ └── utils.ts # Utility functions
├── actions/ # Server actions
│ ├── auth.ts
│ └── [feature].ts
└── hooks/ # Custom React hooks

```

---

## Decision Checklist

Before adding any tool, ask:

1. **Does the PRD require this?**
   - If no, don't add it

2. **What's the simplest solution?**
   - Built-in > Library > Service

3. **What's the cost?**
   - Free tier limits?
   - Scaling costs?

4. **What's the trade-off?**
   - Complexity added?
   - Vendor lock-in?

---

## Plans & Limits Architecture (Better-Auth)

**🚨 CRITICAL: Keep it simple - NO extra abstraction layers!**

### Data Model

```

Organization → Resources (projects, files, etc.)
Organization → Subscription → Plan → Limits

````

**❌ NEVER add:**
- Workspace level
- Team level (separate from Organization)
- Project-level plans
- Any other abstraction layer

### Implementation Pattern

**File: `src/lib/auth/stripe/auth-plans.ts`**

```typescript
// 1. Define default limits
const DEFAULT_LIMIT = {
  projects: 5,
  storage: 10,      // in GB
  members: 3,
  aiCredits: 20,    // $ worth
};

export type PlanLimit = typeof DEFAULT_LIMIT;
export type OverrideLimits = Partial<PlanLimit>;

// 2. Define plans with Better-Auth structure
export type AppAuthPlan = {
  priceId?: string;
  annualDiscountPriceId?: string;
  name: string;
  limits: PlanLimit;
  description: string;
  isPopular?: boolean;
  price: number;
  yearlyPrice?: number;
  currency: string;
  freeTrial?: {
    days: number;
    onTrialStart?: (subscription, ctx) => Promise<void>;
    onTrialEnd?: (data, ctx) => Promise<void>;
    onTrialExpired?: (subscription, ctx) => Promise<void>;
  };
  onSubscriptionCanceled?: (subscription, ctx) => Promise<void>;
};

// 3. Define your plans
export const AUTH_PLANS: AppAuthPlan[] = [
  {
    name: "free",
    description: "For individuals and small projects",
    limits: DEFAULT_LIMIT,
    price: 0,
    currency: "USD",
  },
  {
    name: "pro",
    isPopular: true,
    description: "For growing teams",
    priceId: process.env.STRIPE_PRO_PLAN_ID ?? "",
    annualDiscountPriceId: process.env.STRIPE_PRO_YEARLY_PLAN_ID ?? "",
    limits: {
      projects: 20,
      storage: 50,
      members: 10,
      aiCredits: 50,
    },
    freeTrial: { days: 14 },
    price: 49,
    yearlyPrice: 400,
    currency: "USD",
  },
  {
    name: "ultra",
    description: "Enterprise-grade",
    priceId: process.env.STRIPE_ULTRA_PLAN_ID ?? "",
    annualDiscountPriceId: process.env.STRIPE_ULTRA_YEARLY_PLAN_ID ?? "",
    limits: {
      projects: 100,
      storage: 1000,
      members: 100,
      aiCredits: 200,
    },
    freeTrial: { days: 14 },
    price: 100,
    yearlyPrice: 1000,
    currency: "USD",
  },
];

// 4. Helper to get plan limits (with override support)
export const getPlanLimits = (
  plan = "free",
  overrideLimits?: OverrideLimits | null,
): PlanLimit => {
  const planLimits = AUTH_PLANS.find((p) => p.name === plan)?.limits;
  const baseLimits = planLimits ?? DEFAULT_LIMIT;

  if (!overrideLimits) return baseLimits;

  return { ...baseLimits, ...overrideLimits };
};
````

### UI Configuration for Limits

```typescript
// Display config for pricing page
export const LIMITS_CONFIG: Record<
  keyof PlanLimit,
  {
    icon: React.ElementType;
    getLabel: (value: number) => string;
    description: string;
  }
> = {
  projects: {
    icon: FolderArchive,
    getLabel: (value) => `${value} ${value === 1 ? "Project" : "Projects"}`,
    description: "Create and manage projects",
  },
  storage: {
    icon: HardDrive,
    getLabel: (value) => `${value} GB Storage`,
    description: "Cloud storage for your files",
  },
  members: {
    icon: Users,
    getLabel: (value) => `${value} Team ${value === 1 ? "Member" : "Members"}`,
    description: "Invite team members",
  },
  aiCredits: {
    icon: Bot,
    getLabel: (value) => `$${value} AI Credits`,
    description: "AI-powered features",
  },
};
```

### Checking Limits in Code

```typescript
// In server action or API route
import { getPlanLimits } from "@/lib/auth/stripe/auth-plans";

export async function createProject(orgId: string) {
  const org = await prisma.organization.findUnique({
    where: { id: orgId },
    include: { subscription: true },
  });

  const limits = getPlanLimits(
    org?.subscription?.plan ?? "free",
    org?.subscription?.overrideLimits,
  );

  const projectCount = await prisma.project.count({
    where: { organizationId: orgId },
  });

  if (projectCount >= limits.projects) {
    throw new Error("Project limit reached. Please upgrade your plan.");
  }

  // Create project...
}
```

### Key Principles

1. **Organization is the billing entity** - Plans are tied to Organizations, not Users
2. **Limits are in Better-Auth config** - Centralized in `auth-plans.ts`
3. **Override support** - Allow per-organization limit overrides (for enterprise deals)
4. **No extra layers** - Organization → Resources, that's it

---

## Anti-Patterns

❌ **Microservices for MVP** - Monolith is fine
❌ **Kubernetes** - Vercel handles scaling
❌ **Custom auth** - Use Better Auth or Clerk
❌ **GraphQL** - REST/Server Actions are simpler
❌ **Redis for everything** - Start without caching
❌ **Message queues** - Direct calls are fine initially
❌ **Workspace abstraction** - Organization is enough, don't add layers
❌ **User-level plans** - Plans belong to Organizations, not Users
❌ **1-1 relationships** - Don't create separate tables just to "organize data". Put fields directly on the parent model

### 1-1 Relationships Anti-Pattern

**❌ BAD - Separate table for no reason:**

```prisma
model User {
  id       String       @id
  profile  UserProfile?
}

model UserProfile {
  id     String @id
  bio    String?
  avatar String?
  userId String @unique
  user   User   @relation(fields: [userId], references: [id])
}
```

**✅ GOOD - Fields directly on User:**

```prisma
model User {
  id     String  @id
  bio    String?
  avatar String?
}
```

**When 1-1 is acceptable:**

- External system integration (e.g., StripeCustomer linked to User)
- Better-Auth managed tables (Session, Account, etc.)
- Genuinely optional large data that's rarely loaded
