---
name: step-05-architecture
description: Design technical architecture based on PRD and nowts base stack
prev_step: steps/step-04-prd.md
next_step: steps/step-06-tasks.md
---

# Step 5: Technical Architecture

## MANDATORY EXECUTION RULES (READ FIRST):

- 🛑 NEVER recommend tools not in the approved stack without justification
- ✅ ALWAYS base decisions on PRD requirements
- ✅ ALWAYS respond in `{user_language}`
- 📋 YOU ARE A solutions architect, making practical decisions
- 💬 FOCUS on what the PRD requires, not hypothetical future needs
- 🚫 FORBIDDEN to over-engineer - keep it simple for solo dev

## EXECUTION PROTOCOLS:

- 🎯 Read PRD first, then map features to technical needs
- 💾 Reference nowts project and tools.md for stack decisions
- 📖 Every tool choice needs "Why" and "Trade-off"
- 🚫 FORBIDDEN to load step-06 until architecture is validated

## CONTEXT BOUNDARIES:

- Variables from previous steps: `{validated_idea}`, `{prd_content}`, `{user_language}`, `{output_dir}`, `{save_mode}`
- Base project: NOW.TS boilerplate (user provides path in step-07)

## REFERENCE:

Load `../references/tools.md` for:

- Recommended tech stack
- Tool decision matrix
- Cost estimation templates

Load `../references/architecture-template.md` for:

- Architecture document structure
- Common patterns
- Folder structure

## YOUR TASK:

Design the technical architecture that implements the PRD, using the nowts stack as a foundation.

---

## PHASE 0: RESEARCH & UNDERSTANDING

**Before making any technical decisions, research the available tools:**

### Research NOW.TS Features

NOW.TS is a complete Next.js boilerplate that provides **everything needed for a SaaS**. It saves approximately 12 days of development time by providing:

**✅ What's Already Built-In (FREE):**

**Authentication (Better Auth):**

- Password reset functionality
- Email change management
- User registration and login
- Multi-tenant support with organization invitations
- Permission and role management
- GDPR-compliant data deletion

**Payment Integration (Stripe):**

- Pre-configured webhooks
- One-time purchase support
- Subscription models (monthly/yearly)
- Usage-based billing capabilities
- Payment metadata tracking
- "Configure subscriptions in less than 3 minutes"

**Organization & Multi-Tenancy:**

- Organization creation and management
- User invitation system
- Permission and access control
- Role-based management
- Member management interface

**Admin Dashboard:**

- User management
- Payment tracking
- Subscription monitoring
- Organization oversight
- Member administration

**Developer Experience:**

- 10+ VSCode snippets for rapid component creation
- AI-optimized Cursor rules and Claude Code integration
- Automated CI/CD pipeline with GitHub
- Unit, integration, and TypeScript tests
- ESLint validation
- Vercel deployment ready

**Email System:**

- Resend integration
- Email templates with React Email
- Notification system

**Analytics:**

- PostHog integration for product analytics

**AI Features:**

- AI SDK integration ready
- Easy to add AI capabilities

**Additional:**

- Internationalization (i18n) support
- Documentation system
- Markdown support

**Tech Stack:**

- Next.js 16 with Server Components, Server Actions, App Router
- TypeScript (strict mode)
- PostgreSQL with Prisma ORM
- Tailwind CSS + shadcn/ui
- Better-Auth for authentication
- Stripe for payments
- Resend for email

**🚨 IMPORTANT: If the PRD requires auth, payments, organizations, or multi-tenant features, you DON'T need to build them - they're already in NOW.TS!**

### Research Upstash Suite (For Real-Time & Background Jobs)

If PRD requires real-time features, background jobs, or messaging, consider the Upstash suite:

**Upstash Realtime (for real-time chat, notifications, etc.):**

- 100% HTTP-based with Server-Sent Events (SSE)
- Built-in message histories
- Automatic connection management with delivery guarantee
- Type-safe with Zod schemas
- 2.6kB gzipped, zero dependencies
- Perfect for Next.js serverless
- **Use Case**: Real-time chat, live notifications, collaborative features

**Upstash QStash (for background jobs, scheduling, messaging):**

- Serverless messaging and scheduling
- Automatic retries on failure
- CRON-based scheduling
- Message delays up to 90 days
- Dead Letter Queue (DLQ) for failed messages
- Deduplication
- Rate limiting and parallelism control
- Fan-out to multiple endpoints
- **Use Cases**: Background jobs, scheduled tasks, webhooks, async processing, email queues, LLM workflows

**Upstash Redis (for caching, rate limiting):**

- Serverless Redis
- Global low latency
- Perfect for caching, sessions, rate limiting

**Upstash Vector (for AI/semantic search):**

- Vector database for embeddings
- Semantic search capabilities
- LLM integration

**When to use Upstash:**

- ✅ Real-time chat or live updates → Upstash Realtime
- ✅ Background jobs, scheduled tasks → QStash
- ✅ Rate limiting, caching → Redis
- ✅ AI semantic search → Vector

---

## BASE STACK (from NOW.TS):

**Core Framework:**

- Next.js 16 with App Router, Server Components, Server Actions
- TypeScript (strict mode)
- Tailwind CSS + shadcn/ui components

**UI & Frontend:**

- shadcn/ui components (pre-installed)
- TanStack Query for data fetching
- Zustand for client state (if needed)
- nuqs for URL state
- 10+ VSCode snippets for rapid development

**Backend:**

- Prisma ORM
- PostgreSQL (Neon recommended)
- Better Auth for authentication (fully configured)
- Next Safe Action for server actions
- Zod v4 for validation

**Authentication (Already Built-In):**

- Email + Password
- Password reset
- Email verification
- Multi-tenant organizations
- Role-based permissions
- GDPR data deletion

**Payments (Already Built-In):**

- Stripe integration with webhooks
- Subscription management
- One-time payments
- Usage-based billing

**Email (Already Built-In):**

- Resend + React Email
- Email templates
- Notification system

**Real-Time (Add if needed):**

- Upstash Realtime for SSE-based real-time features
- 2.6kB, type-safe, automatic reconnection

**Background Jobs (Add if needed):**

- Upstash QStash for scheduling, retries, async tasks

**Infrastructure:**

- Vercel deployment (ready)
- CI/CD with GitHub (configured)
- PostHog analytics (integrated)

---

## ARCHITECTURE PROCESS:

### Phase 1: PRD to Technical Requirements

**FIRST: Check what NOW.TS already provides:**

Go through the PRD feature list and mark what's already built:

| PRD Feature           | NOW.TS Status    | Additional Work Needed?     |
| --------------------- | ---------------- | --------------------------- |
| User authentication   | ✅ Built-in      | Just configure auth methods |
| Payment/subscriptions | ✅ Built-in      | Configure Stripe products   |
| Organizations/teams   | ✅ Built-in      | Customize if needed         |
| Email notifications   | ✅ Built-in      | Create email templates      |
| {custom feature}      | ❌ Need to build | {technical approach}        |

**🎯 CRITICAL: If a feature is built-in to NOW.TS, don't plan to rebuild it! Just plan to configure it.**

**SECOND: Map remaining features to technical needs:**

| PRD Feature | Technical Requirement       |
| ----------- | --------------------------- |
| {feature 1} | {what's needed technically} |
| {feature 2} | {what's needed technically} |
| {feature 3} | {what's needed technically} |

**THIRD: Identify special needs beyond NOW.TS:**

- **Real-time features?** → Consider Upstash Realtime (SSE)
  - Chat, live notifications, collaborative editing
  - Example: Real-time chat widget, live dashboard updates

- **Background jobs?** → Consider Upstash QStash
  - Scheduled tasks, async processing, retries
  - Example: Daily reports, email queues, webhook processing

- **File uploads?** → Need storage solution
  - Consider Vercel Blob Storage or S3

- **AI features?** → NOW.TS has AI SDK ready
  - Easy to integrate OpenAI, Anthropic, etc.

- **Heavy computation?** → May need background processing
  - Use QStash for async jobs

### Phase 2: Stack Decisions

**For each technical decision, ask:**

1. Is this already in NOW.TS? → Use it!
2. Does PRD require this?
3. What's the simplest solution?
4. What's the trade-off?

**🚨 IMPORTANT: Only ask about features NOT already in NOW.TS!**

**Authentication** - ✅ Already in NOW.TS with Better Auth

- Just configure which methods to enable (email/password, OAuth, magic link)
- Don't ask about auth provider - it's Better Auth

**Payments** - ✅ Already in NOW.TS with Stripe

- Just configure Stripe products and pricing
- Don't ask about payment provider - it's Stripe

**Organizations/Multi-tenant** - ✅ Already in NOW.TS

- Just customize if needed
- Don't rebuild this!

**Real-Time Features** - ❌ Need to decide

If PRD requires real-time (chat, live updates, notifications):

```yaml
questions:
  - header: "Real-time"
    question: "You need real-time features. Which approach?"
    options:
      - label: "Upstash Realtime (Recommended)"
        description: "SSE-based, 2.6kB, type-safe, perfect for Next.js serverless"
      - label: "Polling"
        description: "Simple but higher latency and server load"
      - label: "WebSockets (Custom)"
        description: "More complex, need separate server"
    multiSelect: false
```

**Background Jobs** - ❌ Need to decide

If PRD requires scheduled tasks, async processing, or retries:

```yaml
questions:
  - header: "Background Jobs"
    question: "You need background job processing. Which approach?"
    options:
      - label: "Upstash QStash (Recommended)"
        description: "Serverless, auto-retry, scheduling, perfect for Vercel"
      - label: "Vercel Cron"
        description: "Simple scheduled tasks only, no retries"
      - label: "BullMQ / Redis Queue"
        description: "Full-featured but need Redis server"
    multiSelect: false
```

**File Storage** - ❌ Need to decide

If PRD requires file uploads:

```yaml
questions:
  - header: "Storage"
    question: "Where to store uploaded files?"
    options:
      - label: "Vercel Blob (Recommended)"
        description: "Integrated with Vercel, simple API"
      - label: "AWS S3"
        description: "Most flexible, requires AWS setup"
      - label: "Cloudinary"
        description: "Great for images, auto-optimization"
    multiSelect: false
```

**Database** - Usually Neon + Prisma (already in NOW.TS)

Only ask if PRD has special requirements:

```yaml
questions:
  - header: "Database"
    question: "Special database needs detected. Which approach?"
    options:
      - label: "Neon + Prisma (Recommended)"
        description: "Standard PostgreSQL, already in NOW.TS"
      - label: "Supabase"
        description: "PostgreSQL + real-time + storage built-in"
    multiSelect: false
```

### Phase 3: Generate Architecture Document

**Create `{output_dir}/archi.md`:**

````markdown
---
project_id: { project_id }
created: { timestamp }
status: complete
stepsCompleted: [0, 1, 2, 3, 4, 5]
---

# Technical Architecture: {Product Name}

## Architecture Overview

**Philosophy**: Keep it simple. Use the nowts stack as foundation, only add what PRD requires.

**Tech Stack Summary**:

- **Framework**: Next.js 15 with App Router
- **Deployment**: Vercel
- **Database**: {choice} with {ORM}
- **Authentication**: Better Auth with {method}
- **Payments**: {choice or "Not needed for MVP"}

## Frontend Architecture

### Core Stack

| Tool         | Purpose     | Why                       |
| ------------ | ----------- | ------------------------- |
| Next.js 15   | Framework   | App Router, RSC, great DX |
| TypeScript   | Type safety | Catch errors early        |
| Tailwind CSS | Styling     | Fast, consistent          |
| shadcn/ui    | Components  | Customizable, accessible  |

### State Management

| Type         | Solution              | When to use          |
| ------------ | --------------------- | -------------------- |
| Server state | TanStack Query        | API data, caching    |
| URL state    | nuqs                  | Filters, pagination  |
| Client state | Zustand               | UI state (if needed) |
| Form state   | React Hook Form + Zod | Form validation      |

### Data Fetching Strategy

- **Default**: Server Components for initial data
- **Client**: TanStack Query for dynamic/user-specific data
- **Mutations**: Server Actions via next-safe-action

## Backend Architecture

### API Layer

| Concern        | Solution         |
| -------------- | ---------------- |
| API Routes     | next-zod-route   |
| Server Actions | next-safe-action |
| Validation     | Zod v4           |
| Rate Limiting  | {approach}       |

### Authentication

- **Provider**: Better Auth
- **Method**: {chosen method}
- **Session**: Database sessions
- **Permissions**: {RBAC if needed, otherwise simple}

### Database & ORM

- **Database**: {Neon PostgreSQL / Supabase}
- **ORM**: Prisma
- **Migrations**: Prisma Migrate

**Schema Overview:**

```prisma
// Core models for {Product Name}

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  createdAt DateTime @default(now())
  // relations...
}

// Add other models based on PRD features
{additional models}
```
````

## Infrastructure

### Deployment

- **Platform**: Vercel
- **Region**: {region recommendation}
- **Environment**: development, preview, production

### External Services

**Built-in to NOW.TS:**
| Service | Purpose | Status |
|---------|---------|--------|
| Better Auth | Authentication | ✅ Pre-configured |
| Stripe | Payments | ✅ Pre-configured |
| Resend | Email | ✅ Pre-configured |
| PostHog | Analytics | ✅ Pre-configured |

**Add if PRD requires:**
| Service | Purpose | When to add |
|---------|---------|-------------|
| Upstash Realtime | Real-time features | Chat, live updates, notifications |
| Upstash QStash | Background jobs | Scheduled tasks, async processing, retries |
| Upstash Redis | Caching, rate limiting | High-traffic apps, session storage |
| Upstash Vector | AI semantic search | Vector embeddings, AI features |
| Vercel Blob | File storage | File uploads, images, documents |
| Sentry | Error tracking | Production monitoring |

## Folder Structure

```
/
├── app/
│   ├── (auth)/           # Auth pages
│   │   ├── login/
│   │   └── signup/
│   ├── (dashboard)/      # Protected pages
│   │   └── dashboard/
│   ├── api/              # API routes
│   └── page.tsx          # Landing
├── src/
│   ├── components/       # UI components
│   │   ├── ui/           # shadcn components
│   │   └── {feature}/    # Feature components
│   ├── lib/              # Utilities
│   ├── actions/          # Server actions
│   └── hooks/            # Custom hooks
├── prisma/
│   └── schema.prisma
└── emails/               # React Email templates
```

## Feature → Implementation Map

| PRD Feature | Implementation    |
| ----------- | ----------------- |
| {Feature 1} | {How to build it} |
| {Feature 2} | {How to build it} |
| {Feature 3} | {How to build it} |

## Architecture Decision Records

### ADR-001: {Key Decision}

- **Context**: {Why decision was needed}
- **Decision**: {What was decided}
- **Alternatives**: {What else was considered}
- **Rationale**: {Why this choice}
- **Consequences**: {Trade-offs}

## Cost Estimation

### Monthly at 1,000 users

| Service        | Cost                   | Notes                              |
| -------------- | ---------------------- | ---------------------------------- |
| NOW.TS License | €200 one-time          | Lifetime, unlimited projects       |
| Vercel         | $0 (hobby) / $20 (pro) | $20 for team features              |
| Neon           | $0 (free tier) / $19   | 10GB free, then $19                |
| Resend         | $0 (3k/month free)     | 3k emails free, then pay-as-you-go |
| Stripe         | 2.9% + $0.30/txn       | Standard processing fees           |
| **Base Total** | ~$0-40/month           | Without optional services          |

### Optional Services (if PRD requires):

| Service          | Cost     | Free Tier             |
| ---------------- | -------- | --------------------- |
| Upstash Realtime | $0 - $10 | 10k events/day free   |
| Upstash QStash   | $0 - $20 | 500 messages/day free |
| Upstash Redis    | $0 - $10 | 10k commands/day free |
| Vercel Blob      | $0 - $10 | 500MB free            |

### Free Tier Limits

- **Vercel**: 100GB bandwidth, unlimited serverless calls (hobby)
- **Neon**: 10GB storage, 191.9 compute hours/month
- **Resend**: 3,000 emails/month, 100 emails/day
- **Upstash Realtime**: 10,000 events/day
- **Upstash QStash**: 500 messages/day
- **Upstash Redis**: 10,000 commands/day, 256MB storage
- **Vercel Blob**: 500MB storage

### Estimated Total Cost

- **Month 1 (development)**: €200 NOW.TS + $0 hosting = €200
- **Month 2+ (< 1000 users)**: $0-20/month (free tiers)
- **At 1000+ users**: $40-80/month

## Implementation Order

**🚀 WITH NOW.TS: Most foundation work is DONE!**

### Phase 1: Setup (Hour 1-2)

1. ✅ Clone NOW.TS boilerplate (5 minutes)
2. ✅ Database already configured (Prisma + Neon)
3. ✅ Auth already working (Better Auth)
4. ✅ Payments already integrated (Stripe)
5. ✅ Email already setup (Resend)
6. Configure your branding and colors
7. Setup environment variables

**Time saved: ~10-12 days!**

### Phase 2: Core Custom Features (Day 1-2)

Focus ONLY on features unique to your SaaS:

1. {Core feature implementation}
2. {Feature-specific database schema}
3. {Feature-specific UI components}

**If using Upstash Realtime:**

- Install `@upstash/realtime`
- Setup event schemas with Zod
- Create route handler for SSE
- Implement useRealtime hook in components

**If using Upstash QStash:**

- Install `@upstash/qstash`
- Create API endpoints for jobs
- Setup scheduled tasks
- Configure retry logic

### Phase 3: Integration & Polish (Day 3-4)

1. Connect custom features to NOW.TS auth/payments
2. Create email templates for your features
3. Landing page customization
4. Test payment flows

### Phase 4: Launch (Day 5-7)

1. Configure Stripe products/pricing
2. Setup production environment
3. Deploy to Vercel (one-click)
4. Monitor with PostHog (already integrated)

````

---

## IMPLEMENTATION EXAMPLES

### Upstash Realtime Implementation

**When to use:** Real-time chat, live notifications, collaborative features

**Setup (5 minutes):**

```typescript
// 1. Install
npm install @upstash/realtime

// 2. Define events (lib/realtime.ts)
import { Realtime } from "@upstash/realtime";
import { z } from "zod";

export const events = {
  "message.created": z.object({
    id: z.string(),
    content: z.string(),
    senderId: z.string(),
    conversationId: z.string(),
    timestamp: z.number(),
  }),
  "user.typing": z.object({
    userId: z.string(),
    conversationId: z.string(),
  }),
};

export const realtime = new Realtime(events, {
  token: process.env.UPSTASH_REALTIME_TOKEN!,
});

// 3. Route handler (app/api/realtime/route.ts)
import { realtime } from "@/lib/realtime";

export async function GET() {
  return realtime.handle();
}

// 4. Publish from Server Action (actions/messages.ts)
"use server";

import { realtime } from "@/lib/realtime";

export async function sendMessage(content: string, conversationId: string) {
  // Save to DB
  const message = await prisma.message.create({...});

  // Publish real-time event
  await realtime.publish("message.created", {
    id: message.id,
    content: message.content,
    senderId: message.senderId,
    conversationId,
    timestamp: Date.now(),
  });

  return message;
}

// 5. Subscribe from Client (components/chat.tsx)
"use client";

import { useRealtime } from "@upstash/realtime/react";

export function Chat({ conversationId }: { conversationId: string }) {
  const { data: newMessage } = useRealtime("message.created", {
    filter: (msg) => msg.conversationId === conversationId,
  });

  useEffect(() => {
    if (newMessage) {
      // Add message to UI
      setMessages((prev) => [...prev, newMessage]);
    }
  }, [newMessage]);

  return <div>{/* Chat UI */}</div>;
}
````

**Benefits:**

- ✅ SSE (Server-Sent Events) - no WebSocket needed
- ✅ Type-safe with Zod
- ✅ Automatic reconnection
- ✅ 2.6kB bundle size
- ✅ Works perfectly on Vercel serverless

---

### Upstash QStash Implementation

**When to use:** Background jobs, scheduled tasks, async processing, retries

**Setup (5 minutes):**

```typescript
// 1. Install
npm install @upstash/qstash

// 2. Create client (lib/qstash.ts)
import { Client } from "@upstash/qstash";

export const qstash = new Client({
  token: process.env.QSTASH_TOKEN!,
});

// 3. API endpoint for job processing (app/api/jobs/send-welcome-email/route.ts)
import { qstash } from "@/lib/qstash";
import { sendEmail } from "@/lib/email";

export async function POST(req: Request) {
  // Verify request is from QStash
  const signature = req.headers.get("upstash-signature");
  const isValid = await qstash.verify({ signature, body: await req.text() });

  if (!isValid) {
    return new Response("Unauthorized", { status: 401 });
  }

  const { userId, email } = await req.json();

  // Process job
  await sendEmail({
    to: email,
    subject: "Welcome!",
    template: "welcome",
  });

  return new Response("OK");
}

// 4. Publish job from Server Action (actions/users.ts)
"use server";

import { qstash } from "@/lib/qstash";

export async function createUser(email: string) {
  const user = await prisma.user.create({ data: { email } });

  // Send welcome email asynchronously with retry
  await qstash.publishJSON({
    url: `${process.env.NEXT_PUBLIC_URL}/api/jobs/send-welcome-email`,
    body: {
      userId: user.id,
      email: user.email,
    },
    retries: 3, // Retry 3 times on failure
  });

  return user;
}

// 5. Schedule recurring job (scripts/schedule-daily-report.ts)
import { qstash } from "@/lib/qstash";

await qstash.schedules.create({
  destination: `${process.env.NEXT_PUBLIC_URL}/api/jobs/daily-report`,
  cron: "0 9 * * *", // Every day at 9 AM
  body: { type: "daily-report" },
});

// 6. Delayed job (actions/trial-reminder.ts)
"use server";

import { qstash } from "@/lib/qstash";

export async function startTrial(userId: string) {
  // Send reminder in 7 days
  await qstash.publishJSON({
    url: `${process.env.NEXT_PUBLIC_URL}/api/jobs/trial-reminder`,
    body: { userId },
    delay: 60 * 60 * 24 * 7, // 7 days in seconds
  });
}
```

**Benefits:**

- ✅ Automatic retries with exponential backoff
- ✅ Dead Letter Queue (DLQ) for failed jobs
- ✅ CRON scheduling
- ✅ Delayed execution (up to 90 days)
- ✅ No infrastructure to manage
- ✅ Perfect for Vercel serverless

**Use Cases:**

- Welcome emails after signup
- Daily/weekly reports
- Trial expiration reminders
- Webhook processing
- Data exports
- LLM API calls (with retry logic)

---

### Phase 4: Present Summary

**Display in `{user_language}`:**

```
🏗️ Architecture Summary for {Product Name}

🚀 Foundation (NOW.TS):
- ✅ Next.js 16 + Tailwind + shadcn/ui (pre-configured)
- ✅ Better Auth + Stripe + Email (ready to use)
- ✅ Organizations, payments, admin dashboard (built-in)
- ✅ PostgreSQL (Neon) + Prisma
- ✅ CI/CD, analytics, monitoring (configured)

⚡ Additional Stack:
- {Real-time}: {Upstash Realtime / Not needed}
- {Background Jobs}: {Upstash QStash / Not needed}
- {File Storage}: {Vercel Blob / Not needed}
- {Other}: {Custom requirements}

Key decisions:
1. {decision 1} - {why}
2. {decision 2} - {why}
3. {decision 3} - {why}

Implementation order:
1. Setup (Hour 1-2): Clone NOW.TS, configure env
2. Custom features (Day 1-2): {core feature}
3. Integration (Day 3-4): Connect to auth/payments
4. Launch (Day 5-7): Deploy, monitor

Time saved with NOW.TS: ~10-12 days
Estimated cost: €200 one-time + $0-40/month
```

### Phase 5: User Validation

Use AskUserQuestion:

```yaml
questions:
  - header: "Approve"
    question: "Does this architecture look good for your project?"
    options:
      - label: "Yes, let's create tasks (Recommended)"
        description: "Architecture approved, create implementation tasks"
      - label: "I have questions"
        description: "I want to discuss some decisions"
      - label: "Need changes"
        description: "Some decisions need to be different"
    multiSelect: false
```

---

## SUCCESS METRICS:

✅ All PRD features mapped to technical implementation
✅ Stack decisions justified with "Why" and trade-offs
✅ Folder structure defined
✅ Cost estimation included
✅ Implementation order defined
✅ Architecture saved to archi.md (if save_mode)
✅ User explicitly approved architecture

## FAILURE MODES:

❌ Over-engineering beyond PRD requirements
❌ Using tools not in approved stack without justification
❌ Missing cost estimation
❌ No implementation order
❌ **CRITICAL**: Not using AskUserQuestion for approval
❌ **CRITICAL**: Not responding in user's detected language

## ARCHITECTURE PROTOCOLS:

- Start with nowts stack, only add what's needed
- Every tool choice needs justification
- Simple is better than clever
- Cost matters for solo devs
- Implementation order helps with planning

---

## NEXT STEP:

After user approves architecture via AskUserQuestion, load `./step-06-tasks.md`

<critical>
🚀 NOW.TS ADVANTAGE:
- Auth, payments, organizations, email, analytics = ALREADY BUILT
- Don't plan to rebuild what's already there
- Focus architecture on UNIQUE features only
- Timeline is much shorter because foundation is done!

Remember:

- The goal is to define HOW to build what the PRD specifies
- Check NOW.TS first before adding any service
- Upstash Realtime for real-time → SSE-based, perfect for serverless
- Upstash QStash for background jobs → auto-retry, scheduling, async
- Solo dev + NOW.TS = 2-7 day timeline is realistic!
  </critical>

---

## Sources

**NOW.TS Documentation:**

- [NOW.TS Official](https://nowts.app/)
- [NOW.TS on Product Hunt](https://www.producthunt.com/products/now-ts)
- [NOW.TS Demo](https://demo.nowts.app/)

**Upstash Documentation:**

- [Upstash Realtime Quickstart](https://upstash.com/docs/realtime/overall/quickstart)
- [Upstash Realtime Blog](https://upstash.com/blog/about-upstash-realtime)
- [QStash Getting Started](https://upstash.com/docs/qstash/overall/getstarted)
- [QStash Announcement](https://upstash.com/blog/qstash-announcement)
