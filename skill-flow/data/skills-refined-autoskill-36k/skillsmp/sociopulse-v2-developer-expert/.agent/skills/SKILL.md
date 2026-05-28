---
name: SocioPulse V2 Expert
description: Master skill for the SocioPulse V2 dual-brand monorepo platform. Provides context and references to specialized sub-skills.
---

# SocioPulse V2 - Expert Skill System

This is the **master skill** for SocioPulse V2. It provides essential context and references specialized sub-skills for different domains.

## Project Context

### What is SocioPulse V2?

SocioPulse V2 is a **dual-brand SaaS platform** serving the medicosocial and medical staffing sectors:

- **SocioPulse** (SOCIAL mode): Social & Educational sector (MECS, IME, ITEP, Crèches)
- **MedicoPulse** (MEDICAL mode): Medical & Healthcare sector (EHPAD, Cliniques, Hôpitaux)

**Single Codebase, Dual Output**: The same code generates two distinct applications via build-time configuration (`NEXT_PUBLIC_APP_MODE`).

### Core Value Propositions

1. **SOS Renfort**: Urgent mission matching (Talents ↔ Establishments)
2. **Catalogue**: Marketplace for workshops/coaching (SocioPulse only)
3. **Fil Pro**: Professional social network (LinkedIn-style)
4. **Mission Hub**: Real-time mission tracking and reporting

### Tech Stack Summary

- **Frontend**: Next.js 14 (App Router), React 18, TypeScript, Tailwind CSS
- **Backend**: NestJS 10 (Modular), Socket.IO, LiveKit
- **Database**: PostgreSQL 15+, Prisma ORM 5.x
- **Infrastructure**: Docker, Coolify 4.0 (Traefik reverse proxy)
- **Payments**: Stripe Connect
- **Real-time**: Socket.IO (chat, notifications), LiveKit (video sessions)

### Critical Branding Rules

**FORBIDDEN TERMS** (Legacy - NEVER use):

- ❌ "Les Extras", "Sanctuary", "Oracle", "SoulMirror", "Eduat'heure"

**CORRECT TERMS**:

- ✅ "SocioPulse" / "MedicoPulse" (brands)
- ✅ "Catalogue" (marketplace)
- ✅ `@sociopulse/*` (package scope)

---

## Sub-Skills Reference

This master skill is organized into **specialized sub-skills**. Each sub-skill is a standalone SKILL.md file covering a specific domain:

### 1. Design System (`skills/design-system/SKILL.md`)

Covers the polymorphic design system:

- CSS Variables theming
- Tailwind configuration
- Component patterns (Radix UI, Framer Motion)
- Typography, colors, spacing

### 2. Frontend Architecture (`skills/frontend/SKILL.md`)

Covers Next.js architecture:

- Route groups and middleware
- Dual-brand implementation
- Dashboard variants (4 types)
- Server Actions and state management

### 3. Backend Architecture (`skills/backend/SKILL.md`)

Covers NestJS modules:

- Feature modules (MatchingEngine, Payments, etc.)
- Guards, interceptors, decorators
- WebSocket implementation
- API patterns

### 4. Database & Prisma (`skills/database/SKILL.md`)

Covers database schema:

- Key models (User, ReliefMission, Service, Contract)
- Enums and business logic
- Indexes and performance
- Migration workflows

### 5. Business Logic (`skills/business-logic/SKILL.md`)

Covers domain-specific logic:

- Job taxonomies (`sos-config.ts`)
- Compliance rules (ADELI, documents)
- Matching algorithm
- Terminology mapping

### 6. Deployment (`skills/deployment/SKILL.md`)

Covers Coolify 4.0 deployment:

- Docker multi-stage builds
- Traefik labels configuration
- Environment variables
- CI/CD workflows

---

## Quick Reference

### Critical Files

- `prisma/schema.prisma` - Single source of truth for DB
- `lib/brand.ts` - Brand configuration (colors, baselines)
- `lib/domain-config.ts` - Features, terminology, compliance
- `lib/sos-config.ts` - Job taxonomies and professional rules
- `middleware.ts` - Auth and subdomain routing

### Common Commands

```bash
# Development
npm run dev              # Start all (Next.js + NestJS)
npm run api:dev          # API only

# Database
npx prisma generate      # Generate Prisma client
npx prisma db push       # Push schema changes
npx prisma studio        # Open DB GUI

# Build
npm run build            # Build frontend
npm run api:build        # Build backend

# Types (after schema changes)
cd packages/shared-types && npm run build
```

### Environment Modes

```bash
# Build SocioPulse
NEXT_PUBLIC_APP_MODE=SOCIAL npm run build

# Build MedicoPulse
NEXT_PUBLIC_APP_MODE=MEDICAL npm run build
```

---

## How to Use This Skill System

1. **Start here** (SKILL.md) for project context
2. **Navigate to sub-skills** based on your task:
   - Styling/UI? → Check `skills/design-system/`
   - Dashboard logic? → Check `skills/frontend/`
   - API endpoints? → Check `skills/backend/`
   - Database queries? → Check `skills/database/`
   - Deployment issues? → Check `skills/deployment/`
3. **Cross-reference** between skills as needed

---

*This modular skill structure allows AI agents to load only relevant context for their specific task while maintaining access to the complete project knowledge base.*
