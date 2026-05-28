# Stack Selection Framework

## Purpose

Choose the right technologies for your project. Default to boring, proven tools unless you have a specific reason to deviate.

---

## Decision Principles

### The Boring Technology Rule

**Default:** Use the most boring technology that solves your problem.

**Why:**
- Better documentation
- More StackOverflow answers
- Fewer edge-case bugs
- Easier to hire/hand off
- More stable long-term

**When to use exciting technology:**
- Boring option genuinely can't solve the problem
- You have deep expertise in the exciting option
- The project is explicitly experimental

---

## The ID8 Default Stack

This is the starting point. Deviate only with reason.

| Layer | Default | Why |
|-------|---------|-----|
| **Framework** | Next.js 14+ (App Router) | React + SSR + API + Edge |
| **Language** | TypeScript (strict) | Catch errors, better DX |
| **Styling** | Tailwind CSS | Fast, consistent, no CSS debugging |
| **Components** | shadcn/ui | Accessible, customizable, no lock-in |
| **Database** | Supabase (PostgreSQL) | Managed, real-time, auth, storage |
| **Auth** | Supabase Auth | Already integrated, handles edge cases |
| **Storage** | Supabase Storage | Already integrated with auth |
| **Hosting** | Vercel | Zero-config Next.js, edge network |
| **State** | React Query + Zustand | Server state + minimal client state |
| **Forms** | React Hook Form + Zod | Performant forms, schema validation |
| **Monitoring** | Sentry + Vercel Analytics | Errors + performance |

---

## Decision Matrix by Category

### Frontend Framework

| Option | Choose When | Avoid When |
|--------|-------------|------------|
| **Next.js (App Router)** | Default choice, need SSR/SEO, want full-stack | Building pure SPA |
| **Remix** | Heavy forms, progressive enhancement focus | Need extensive React ecosystem |
| **Astro** | Content-heavy, minimal JS needed | Highly interactive app |
| **Vite + React** | Pure SPA, no SSR needed | Need SEO, server rendering |

**Default:** Next.js App Router

### Database

| Option | Choose When | Avoid When |
|--------|-------------|------------|
| **Supabase (PostgreSQL)** | Default, need realtime, auth, storage | Need graph queries |
| **PlanetScale (MySQL)** | Need serverless branching, high scale | Need PostGIS, complex queries |
| **Neon (PostgreSQL)** | Need branching, Vercel integration | Need built-in auth |
| **MongoDB Atlas** | Document model fits, rapid prototyping | Complex relations, transactions |
| **SQLite (Turso)** | Edge-first, simple needs | Complex queries, large scale |

**Default:** Supabase

### Authentication

| Option | Choose When | Avoid When |
|--------|-------------|------------|
| **Supabase Auth** | Using Supabase, need simple auth | Complex enterprise SSO |
| **Clerk** | Need beautiful prebuilt components | Budget constrained |
| **Auth.js (NextAuth)** | Need custom providers, own DB | Want managed solution |
| **Lucia** | Full control, understand auth well | Want managed solution |

**Default:** Supabase Auth (if using Supabase), Clerk otherwise

### State Management

| Option | Choose When | Avoid When |
|--------|-------------|------------|
| **React Query** | Server state, caching, sync | Client-only state |
| **SWR** | Simpler server state needs | Complex cache invalidation |
| **Zustand** | Simple global client state | Everything (overuse) |
| **Jotai** | Atom-based state, bottom-up | Simple global state |
| **Redux** | Complex state machines, time-travel | 99% of apps |

**Default:** React Query (server) + Zustand (client, if needed)

### Styling

| Option | Choose When | Avoid When |
|--------|-------------|------------|
| **Tailwind CSS** | Default, rapid development | Deep CSS customization needed |
| **CSS Modules** | Component-scoped, familiar CSS | Rapid prototyping |
| **Styled Components** | Dynamic styles, theming | Performance critical |
| **Panda CSS** | Type-safe, build-time CSS | Simple projects |

**Default:** Tailwind CSS

### Component Library

| Option | Choose When | Avoid When |
|--------|-------------|------------|
| **shadcn/ui** | Full control, accessible, customizable | Need out-of-box design |
| **Radix Primitives** | Building own design system | Need styled components |
| **Headless UI** | Tailwind-native, simpler needs | Need extensive components |
| **Chakra UI** | Theming system, quick start | Need high customization |
| **Material UI** | Material design required | Custom design needs |

**Default:** shadcn/ui

### Hosting

| Option | Choose When | Avoid When |
|--------|-------------|------------|
| **Vercel** | Next.js, zero-config deploy | Budget constrained at scale |
| **Netlify** | Simpler needs, good free tier | Need Edge runtime extensively |
| **Railway** | Need containers, databases | Static sites |
| **Fly.io** | Need containers, edge, global | Simple static sites |
| **Cloudflare Pages** | Edge-first, cost sensitive | Need serverless functions |

**Default:** Vercel

---

## Decision Process

### Step 1: Start with Defaults

Begin with the ID8 Default Stack. Write down any constraints that might require deviation.

### Step 2: Identify Forcing Functions

**Forcing functions that require deviation:**

| Constraint | May Require |
|------------|-------------|
| Complex real-time multiplayer | Convex, Liveblocks |
| Heavy ML/AI workloads | Separate Python backend |
| Mobile app needed | React Native, Expo |
| Desktop app needed | Electron, Tauri |
| Specific compliance (HIPAA) | Self-hosted or certified providers |
| Offline-first | SQLite, local-first architecture |
| Complex search | Algolia, Typesense, Meilisearch |
| Heavy file processing | Separate worker service |

### Step 3: Document Decisions

For any non-default choice:

```markdown
## Decision: {Technology}

**Choice:** {What you picked}
**Default was:** {What the default would have been}
**Reason:** {Why you deviated}
**Trade-offs:**
- Gained: {benefits}
- Lost: {drawbacks}
```

---

## Cost Considerations

### Free/Cheap Tier Viability

| Service | Free Tier | When You Pay |
|---------|-----------|--------------|
| **Vercel** | Hobby (personal) | Team features, bandwidth |
| **Supabase** | 500MB DB, 1GB storage | More storage, team, backups |
| **Clerk** | 10k MAU | More users, features |
| **Sentry** | 5k errors/month | More volume, features |
| **Cloudflare** | Generous | Enterprise features |

### Estimated Monthly Costs by Stage

| Stage | Estimated Cost |
|-------|----------------|
| **Development** | $0-20/mo |
| **MVP (< 100 users)** | $0-50/mo |
| **Early traction (100-1k users)** | $50-200/mo |
| **Growing (1k-10k users)** | $200-500/mo |

---

## Technology Radar

### Adopt (Use freely)
- Next.js 14 App Router
- Supabase
- Tailwind CSS
- shadcn/ui
- TypeScript
- React Query

### Trial (Use with caution)
- Convex (for real-time)
- Turso (edge SQLite)
- tRPC (type-safe APIs)
- Drizzle ORM

### Assess (Watch, don't adopt yet)
- Bun runtime
- Hono framework
- Effect-TS

### Hold (Avoid for new projects)
- Create React App
- Redux for most apps
- Styled Components (perf concerns)
- Firebase (vendor lock-in, cost)

---

## Quick Reference

**"I need to build a..."**

| Type | Stack |
|------|-------|
| SaaS dashboard | Next.js + Supabase + shadcn/ui |
| Marketing site | Next.js (static) + Tailwind |
| Blog | Next.js + MDX + Contentlayer |
| E-commerce | Next.js + Supabase + Stripe |
| Real-time app | Next.js + Supabase Realtime |
| Mobile app | Expo + Supabase |
| CLI tool | Node.js + Commander |
| API service | Next.js API routes or Hono |
| AI/ML app | Next.js + Python backend + Vercel AI SDK |
