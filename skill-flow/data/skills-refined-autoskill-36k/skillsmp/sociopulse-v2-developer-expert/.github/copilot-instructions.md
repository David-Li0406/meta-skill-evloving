# SocioPulse/MedicoPulse Copilot Instructions

## Project Overview

Multi-brand B2B/B2C platform (SocioPulse for social services, MedicoPulse for medical) connecting healthcare establishments with freelance professionals (Talents). Monorepo with Next.js 14 frontend, NestJS API, PostgreSQL via Prisma, and real-time Socket.IO.

## Architecture

```
├── app/                   # Next.js App Router (frontend)
│   ├── (platform)/        # Protected authenticated routes (dashboards, bookings)
│   ├── (auth)/            # Login/onboarding flows
│   └── (admin)/           # Admin dashboard (dash.* subdomain)
├── apps/api/src/          # NestJS backend API
│   ├── common/guards/     # JwtAuthGuard, RolesGuard, MissionAccessGuard
│   └── [feature]/         # Feature modules (auth, payments, matching-engine, etc.)
├── components/            # React components organized by domain
├── lib/                   # Shared utilities (auth.ts, brand.ts, config.ts, domain-config.ts)
├── packages/shared-types/ # @sociopulse/types - shared Prisma types/DTOs
└── prisma/schema.prisma   # Database schema (1400+ lines, source of truth)
```

## Brand & Domain System (Critical)

Single codebase serves two brands via `NEXT_PUBLIC_APP_MODE`:
- **SOCIAL** → SocioPulse (teal/indigo) — social workers, educators
- **MEDICAL** → MedicoPulse (rose) — healthcare professionals

### Brand Helpers (`lib/brand.ts`)
```typescript
import { currentBrand, isMedical, isSocial } from '@/lib/brand';
// currentBrand.appName, currentBrand.primaryColor, etc.
```

### Domain Config (`lib/domain-config.ts`)
Extended configuration for feature flags, terminology, and compliance:
```typescript
import { domainConfig, getTerm, isFeatureEnabled } from '@/lib/domain-config';

// Feature flags
if (isFeatureEnabled('enableWorkshops')) { /* Social only */ }
if (isFeatureEnabled('enableShiftView')) { /* Medical only */ }

// Terminology overrides
getTerm('mission')  // Medical: "Vacation" | Social: "Mission"
getTerm('talent')   // Medical: "Soignant" | Social: "Intervenant"

// Compliance rules
domainConfig.compliance.requiresADELI     // Medical only
domainConfig.compliance.requiresDriverLicense  // Social only
```

### Dashboard Polymorphism (2×2 Matrix)
Dashboards adapt UI based on `(Medical/Social) × (Client/Talent)`:

| Mode | Client Dashboard | Talent Dashboard |
|------|------------------|------------------|
| Medical | `shift-planner` (calendar-dense) | `job-ticker` (urgent shifts list) |
| Social | `project-hub` (card-based) | `portfolio-feed` (skills + feed) |

Use `DashboardResolver` for automatic routing:
```typescript
import { DashboardResolver } from '@/components/dashboard';
<DashboardResolver role="CLIENT" />  // Renders correct variant
```

CSS uses polymorphic variables in `globals.css`. **Never hardcode `teal-500` or `rose-500`.**

## API Patterns (NestJS)

**Creating protected endpoints:**
```typescript
import { JwtAuthGuard, RolesGuard, MissionAccessGuard } from '../common/guards';
import { Roles, CurrentUser, CurrentUserPayload } from '../common/decorators';

@UseGuards(JwtAuthGuard)              // Auth required
@UseGuards(JwtAuthGuard, RolesGuard)  // Auth + role check
@Roles('CLIENT', 'ADMIN')             // Allowed roles
async myEndpoint(@CurrentUser() user: CurrentUserPayload) { }
```

**Mission-specific access:** Use `MissionAccessGuard` for endpoints involving mission data—validates user is participant of the mission.

All routes versioned under `/api/v1/`. Rate limiting via `@Throttle()` decorator.

## Authentication Flow

- **JWT** stored in `accessToken` cookie (7-day expiry)
- **Frontend:** `lib/auth.ts` → `auth.login()`, `auth.getToken()`, `auth.logout()`
- **API URL:** Always use `getApiUrl()` from `lib/config.ts` (handles dev/prod/Docker)
- **Middleware:** `middleware.ts` handles route protection + role-based redirects

## Database (Prisma)

**After schema changes:**
```bash
npm run db:generate  # Regenerate client (REQUIRED)
npm run db:push      # Push to DB (dev only)
```

**Key models:** `User` (role: CLIENT/TALENT/ADMIN), `ReliefMission` (SOS missions), `Booking` (video sessions), `Contract`, `Profile`, `Establishment`

**Types:** Import from `@lesextras/types`:
```typescript
import { User, UserRole, MissionStatus, type Prisma } from '@lesextras/types';
```

## Real-time (Socket.IO)

`SocketProvider` in root layout connects with JWT. Use hooks:
```typescript
const { socket, isConnected } = useSocket();
const { messages, sendMessage } = useMissionChat(missionId);
const { notifications } = useNotifications();
```

## UI Components

```typescript
import { Button, Card, Badge, Input } from '@/components/ui';
import { toast } from 'sonner';  // toast.success(), toast.error()
```

Icons: `lucide-react`. Always use polymorphic Tailwind classes (`bg-primary-600`, not `bg-teal-600`).

## Commands

```bash
npm run dev          # Frontend (localhost:3000)
npm run api:dev      # API (localhost:4000)
npm run db:generate  # Regenerate Prisma client after schema changes
npm run db:push      # Push schema to DB (dev)
npm run db:studio    # Prisma Studio
npm run db:seed      # Seed database
npm run test:smoke   # Playwright smoke tests
```

## Creating New Features

| Task | Location | Notes |
|------|----------|-------|
| API endpoint | `apps/api/src/[feature]/` | Register module in `app.module.ts` |
| Page | `app/(platform)/[route]/page.tsx` | Use `'use client'` for interactivity |
| Component | `components/[domain]/` | Export via `index.ts` barrel |
| Shared type | `packages/shared-types/index.ts` | Re-export from Prisma |

## User Roles & Routing

- `CLIENT` — Establishments/individuals hiring → `/dashboard/client`
- `TALENT` — Freelance professionals → `/dashboard/talent`
- `ADMIN` — Platform admins → `/admin` (uses `dash.*` subdomain in prod)

Check role in frontend via decoded JWT, in API via `@Roles()` decorator.

## Docker Deployment

```bash
docker build --build-arg NEXT_PUBLIC_APP_MODE=SOCIAL -t sociopulse-web .
docker build --build-arg NEXT_PUBLIC_APP_MODE=MEDICAL -t medicopulse-web .
```

Traefik routes: `api.sociopulse.fr`, `sociopulse.fr`, `medicopulse.fr`
