---
name: SocioPulse V2 Developer Expert
description: Expert knowledge for developing, maintaining, and refactoring the SocioPulse V2 monorepo stack.
---

# SocioPulse V2 - Expert Developer Skill

This skill provides deep contextual knowledge and strict guidelines for working on the SocioPulse V2 project (formerly "Les Extras").

## 1. Project Identity & Branding (CRITICAL)

**Strict Branding Rules:**

- **Project Name:** SocioPulse (V2).
- **Forbidden Terms:**
  - ❌ "Sanctuary", "Oracle", "SoulMirror" (Legacy astrological features -> **DO NOT USE**).
  - ❌ "Eduat'heure" (Legacy marketplace name -> Use **"Catalogue"**).
  - ❌ "Les Extras" (Legacy brand -> Use **"SocioPulse"**).
- **Domains:** `socio-pulse.fr` / `dash.sociopulse.com`.
- **Packages:** Internal packages MUST be scoped as `@sociopulse/*` (e.g., `@sociopulse/types`).

## 2. Technical Architecture

### Monorepo Structure

- **Root (`/`)**: Next.js (App Router) Frontend.
- **`apps/api`**: NestJS Backend.
- **`packages/shared-types`**: Single Source of Truth for DTOs & Prisma Types.
- **`lib/`**: Shared frontend business logic & config.

### Frontend (Next.js 14)

- **Routing**: Uses Route Groups (`(platform)`, `(auth)`, `(admin)`) to separate context.
- **State**: Server Actions for mutations, React Query (or native fetch) for data.
- **Styling**: Tailwind CSS + Radix UI Primitives.
- **Animations**: Framer Motion (v12).
- **Middleware**: `middleware.ts` handles subdomain routing (`dash.*`) and role-based redirects.

### Backend (NestJS 10)

- **Modularity**: Feature-based modules (e.g., `MatchingEngineModule`, `WallFeedModule`).
- **Database**: Prisma ORM with PostgreSQL.
  - **Schema**: Complex many-to-many relations, extensive use of Enums.
- **Queueing**: Redis (for jobs/caching).
- **Realtime**: Socket.IO & LiveKit (Video).

## 3. Critical Configuration Files

- **`prisma/schema.prisma`**: The absolute source of truth for the data model. Always check this before assuming database structure.
- **`lib/sos-config.ts`**: "Logic-as-Data". Defines hierarchy of medical/social professions, compliance rules, and tags.
- **`lib/domain-config.ts`**: Configuration for whitelabeling/domains.
- **`apps/api/.env`**: Backend environment variables (Stripe, SendGrid, LiveKit keys).

## 4. Development Workflows

### Database Updates

When modifying `schema.prisma`:

```bash
# 1. Generate Client
npx prisma generate
# 2. Update Types Package
cd packages/shared-types && npm run build
# 3. Restart Dev Server (often needed to pick up new types)
```

### Dependency Management

- **Shared Types**: If you change `@sociopulse/types`, you MUST rebuild it for `apps/api` or root to see changes.
- **Install**: Use `npm install` at root.

### Common Commands

- **Start All**: `npm run dev` (Starts Next.js + NestJS).
- **Start API only**: `npm run api:dev`.
- **Lint**: `npm run lint`.

## 5. Coding Standards

- **Type Safety**: Strict TypeScript usage. No `any`. Use DTOs from `@sociopulse/types`.
- **Components**: Atomic design principles. Keep Client Components (`'use client'`) at the leaves.
- **API Communication**: Use typed server actions or strictly typed fetch wrappers.
- **Naming**:
  - Files: `camelCase.ts` or `PascalCase.tsx`.
  - CSS Classes: `kebab-case` (Tailwind).

## 6. Key Features Overview

- **SOS Renfort (`ReliefMission`)**: Urgent matching system. High complexity.
- **Catalogue (`Service`)**: Marketplace for workshops/video coaching.
- **Fil Pro (`WallFeed`)**: Social feed (LinkedIn-style).
- **Mission Hub**: Tracking active missions (Chat, Report, Timeline).

---
*Use this skill to navigate the codebase, understand constraints, and write code that fits the SocioPulse architecture seamlessly.*
