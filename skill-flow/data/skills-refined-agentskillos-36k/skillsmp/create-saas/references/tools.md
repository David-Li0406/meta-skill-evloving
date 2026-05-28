# Recommended Tools & Stack

Reference document for technical decisions in SaaS projects.

---

## Core Framework & Tooling

| Tool                | Purpose              | Why                                           |
| ------------------- | -------------------- | --------------------------------------------- |
| **Next.js 15**      | Full-stack framework | App Router, RSC, great DX, Vercel integration |
| **Expo**            | Mobile framework     | React Native with best DX                     |
| **Turborepo**       | Monorepo             | Fast builds, remote caching                   |
| **TypeScript**      | Type safety          | Catch errors early, better IDE support        |
| **Tailwind CSS v4** | Styling              | Fast, consistent, utility-first               |
| **Bun**             | Runtime & PM         | Fastest JS runtime & package manager          |

## UI & Components

| Tool                       | Purpose             | When to use                       |
| -------------------------- | ------------------- | --------------------------------- |
| **shadcn/ui**              | Component library   | Always - accessible, customizable |
| **React Native Reusable**  | Mobile components   | Expo/RN projects                  |
| **Uniwind**                | Mobile styling      | Tailwind-like for RN              |
| **Lucide React**           | Icons               | Default icon set                  |
| **Sonner**                 | Toast notifications | User feedback                     |
| **cmdk**                   | Command palette     | Power user features               |
| **React Hotkeys Hook**     | Keyboard shortcuts  | Power user features               |

## State & Data Fetching

| Tool                | Purpose           | When to use                          |
| ------------------- | ----------------- | ------------------------------------ |
| **TanStack Query**  | Server state      | API data, caching, mutations         |
| **nuqs**            | URL state         | Filters, pagination, shareable state |
| **Zustand**         | Client state      | Complex UI state (use sparingly)     |
| **Legend-State**    | Local-first state | Offline-first apps with sync         |
| **React Hook Form** | Forms             | All forms with validation            |
| **TanStack Form**   | Forms             | Modern alternative, more control     |
| **Zod v4**          | Validation        | Schema validation everywhere         |

## Backend & API

| Tool                 | Purpose           | When to use                  |
| -------------------- | ----------------- | ---------------------------- |
| **Server Actions**   | Mutations         | Default for data mutations   |
| **next-safe-action** | Type-safe actions | Wrap all server actions      |
| **next-zod-route**   | API routes        | When REST endpoints needed   |
| **up-fetch**         | HTTP client       | Modern fetch wrapper         |
| **AI SDK**           | LLM integration   | AI features (Vercel AI SDK)  |
| **Inngest**          | Background jobs   | Async jobs & workflows       |

## Database & ORM

| Tool            | Best for           | Trade-offs                           |
| --------------- | ------------------ | ------------------------------------ |
| **Neon**        | Most projects      | Free tier, serverless Postgres       |
| **Supabase**    | Real-time + auth   | More features, different paradigm    |
| **PlanetScale** | Scale needs        | MySQL, branching                     |
| **Convex**      | Full realtime      | Realtime DB + backend                |
| **Redis**       | Caching            | Sessions, cache, rate limiting       |
| **Prisma**      | ORM (recommended)  | Better DX, great for teams           |
| **Drizzle ORM** | ORM (performance)  | 2-3x faster than Prisma              |

## Realtime & Collaboration

| Tool           | Purpose                  | When to use                     |
| -------------- | ------------------------ | ------------------------------- |
| **Convex**     | Realtime database        | Entire app is realtime          |
| **Liveblocks** | Multiplayer features     | Cursors, presence, comments     |

## Authentication

| Tool            | Purpose       | When to use                     |
| --------------- | ------------- | ------------------------------- |
| **Better Auth** | Auth solution | Default - flexible, self-hosted |
| **Clerk**       | Managed auth  | When you want zero auth code    |

### Auth Methods

| Method                | Complexity | UX                   |
| --------------------- | ---------- | -------------------- |
| Email + Password      | 🟢 Low     | Traditional          |
| Magic Link / OTP      | 🟢 Low     | Modern, passwordless |
| OAuth (Google/GitHub) | 🟡 Medium  | Convenient for devs  |
| All combined          | 🟡 Medium  | Maximum flexibility  |

## Internationalization

| Tool                 | Purpose     | When to use         |
| -------------------- | ----------- | ------------------- |
| **next-intl**        | Next.js i18n | Web projects       |
| **react-intl**       | React i18n   | General React      |
| **expo-localization**| Expo i18n    | Mobile projects    |

## Email

| Tool            | Purpose             | Free tier    |
| --------------- | ------------------- | ------------ |
| **Resend**      | Transactional email | 3,000/month  |
| **React Email** | Email templates     | Unlimited    |
| **AWS SES**     | High volume email   | 62,000/month |

## Payments

| Tool              | Best for      | Trade-offs                     |
| ----------------- | ------------- | ------------------------------ |
| **Stripe**        | Most projects | Most flexible, well-documented |
| **Lemon Squeezy** | Simplicity    | Handles taxes, less flexible   |

## File Storage & Upload

| Tool             | Purpose         | When to use               |
| ---------------- | --------------- | ------------------------- |
| **Uploadthing**  | Simple uploads  | Quick setup, Next.js      |
| **Cloudflare R2**| Object storage  | Cheap, S3-compatible      |
| **AWS S3**       | Object storage  | Standard, watch egress    |

## Analytics & Monitoring

| Tool                 | Purpose           | When to add       |
| -------------------- | ----------------- | ----------------- |
| **PostHog**          | Product analytics | Post-launch       |
| **Plausible**        | Web analytics     | Simple, privacy   |
| **Sentry**           | Error tracking    | Post-launch       |
| **Vercel Analytics** | Web vitals        | Free with Vercel  |

## Testing

| Tool                | Purpose        | When to use          |
| ------------------- | -------------- | -------------------- |
| **Vitest**          | Unit tests     | New projects         |
| **Jest**            | Unit tests     | Legacy, wide support |
| **Testing Library** | DOM testing    | Component tests      |
| **Playwright**      | E2E (web)      | Web E2E tests        |
| **Maestro**         | E2E (mobile)   | Mobile E2E tests     |

## Quality & Linting

| Tool          | Purpose              | Why                        |
| ------------- | -------------------- | -------------------------- |
| **Biome**     | Linter & formatter   | Replaces ESLint + Prettier |
| **Knip**      | Unused code          | Find dead code & deps      |
| **Lefthook**  | Git hooks            | Faster than Husky          |
| **Lighthouse**| Web performance      | Audit web vitals           |
| **Flashlight**| Mobile performance   | Mobile perf testing        |
| **Snyk**      | Security scanning    | Vulnerability detection    |
| **rnsec**     | RN security          | React Native specific      |

## Deployment

| Tool               | Purpose | Why                      |
| ------------------ | ------- | ------------------------ |
| **Vercel**         | Hosting | Best Next.js integration |
| **GitHub Actions** | CI/CD   | Automated testing        |

---

## Decision Matrix

### When to use what

| Need               | Solution                                        |
| ------------------ | ----------------------------------------------- |
| Simple CRUD app    | Next.js + Prisma + Neon                         |
| Real-time features | Convex (full) or Neon + Liveblocks (partial)    |
| AI features        | Vercel AI SDK                                   |
| File uploads       | Uploadthing (simple) or R2/S3 (control)         |
| Background jobs    | Inngest or Trigger.dev                          |
| Search             | Algolia or Typesense                            |
| Caching            | Redis (Upstash)                                 |
| Mobile app         | Expo + React Native Reusable                    |
| Monorepo           | Turborepo + Bun                                 |
| ORM choice         | Prisma (DX) or Drizzle (performance)            |
| Forms              | React Hook Form (standard) or TanStack (modern) |

---

## Cost Estimation Template

### At 1,000 users/month

| Service   | Free tier       | Paid    |
| --------- | --------------- | ------- |
| Vercel    | 100GB bandwidth | $20/mo  |
| Neon      | 10GB storage    | $19/mo  |
| Resend    | 3,000 emails    | $20/mo  |
| **Total** | ~$0             | ~$59/mo |

### At 10,000 users/month

| Service   | Estimate     |
| --------- | ------------ |
| Vercel    | $20-50/mo    |
| Database  | $50-100/mo   |
| Email     | $50/mo       |
| **Total** | ~$120-200/mo |

---

## Important Notes

- **Zod**: Use v4, specify version to AI
- **Prisma vs Drizzle**: Prisma = better DX, Drizzle = 2-3x faster
- **Bun**: Fastest, but prefer pnpm in monorepos (better workspace support)
- **Convex vs Neon+Liveblocks**: Convex if entire app is realtime
- **AWS S3**: Watch egress costs, prefer R2 for serving assets
- **Lefthook**: Faster than Husky, written in Go
- **Biome**: Replaces ESLint + Prettier, much faster
- **Legend-State**: Best for offline-first apps with sync
- **Maestro**: More reliable than Detox for mobile E2E
