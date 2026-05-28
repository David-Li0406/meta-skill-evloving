---
name: migestion
description: >
  Main entry point for MiGestion development - quick reference for all components.
  Trigger: General MiGestion development questions, project overview, component navigation.
license: MIT
metadata:
  author: migestion
  version: '1.0'
  scope: [root]
  auto_invoke: 'General MiGestion development questions'
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## Components

| Component | Stack                                                                     | Location        |
| --------- | ------------------------------------------------------------------------- | --------------- |
| API       | Node.js 20, Express 4, TypeScript 5, Prisma, MySQL 8, Redis 7             | `packages/api/` |
| Web       | React 18, TypeScript 5, Vite 5, Tailwind CSS, Zustand 4, TanStack Query 5 | `packages/web/` |

## Quick Commands

```bash
# Global
npm install              # Install dependencies
npm run dev              # Start both services (API:3000, Web:5173)
npm run build            # Build all
npm run test             # Test all
npm run lint             # Lint all

# API
npm run dev:api          # Start API dev server
npm run build:api        # Build API
npm run test:api         # Run API unit tests
npm run db:generate      # Generate Prisma client
npm run db:migrate       # Run migrations
npm run db:seed          # Seed database
npm run db:studio        # Open Prisma Studio

# Web
npm run dev:web          # Start Web dev server
npm run build:web        # Build Web
npm run test:web         # Run Web unit tests
npm run test:e2e         # Run E2E tests

# Docker
docker-compose up -d     # Start infrastructure (MySQL, Redis)
docker-compose down      # Stop infrastructure
```

## Architecture

**Monorepo Structure:**

```
migestion/
├── packages/
│   ├── api/                 # Backend
│   │   ├── src/
│   │   │   ├── config/      # Configuration, constants
│   │   │   ├── infrastructure/  # Prisma, Redis, Socket.IO
│   │   │   ├── modules/     # Business logic (auth, clients, etc.)
│   │   │   └── shared/      # Middleware, utils, errors
│   │   └── tests/          # Jest unit tests
│   └── web/                 # Frontend
│       ├── src/
│       │   ├── components/  # Reusable UI components
│       │   ├── pages/       # Feature pages
│       │   ├── contexts/    # React contexts
│       │   ├── hooks/       # Custom hooks
│       │   ├── services/    # API integration
│       │   ├── stores/      # Zustand stores
│       │   └── lib/         # Utilities
│       └── e2e/           # Playwright E2E tests
```

**Module Pattern (API):**

- `*.controller.ts` - HTTP request handlers (thin layer)
- `*.service.ts` - Business logic layer
- `*.repository.ts` - Database access layer (Prisma)
- `*.dto.ts` - Data transfer objects
- `*.validator.ts` - Zod validation schemas
- `*.routes.ts` - Route definitions

**Component Pattern (Web):**

- `src/components/ui/` - Reusable UI components (Button, Input, etc.)
- `src/pages/` - Feature pages (ClientsPage, DashboardPage, etc.)
- `src/services/` - API service functions
- `src/stores/` - Zustand state stores
- `src/contexts/` - React contexts (Socket, etc.)
- `src/hooks/` - Custom hooks (useAuth, etc.)

## Commit Style

`feat:`, `fix:`, `docs:`, `chore:`, `perf:`, `refactor:`, `test:`

## Related Skills

- `migestion-api` - Backend patterns (Express, Prisma, modules)
- `migestion-web` - Frontend patterns (React, Zustand, design system)
- `migestion-prisma` - Database patterns (multi-tenant queries)
- `migestion-test-api` - API testing with Jest
- `migestion-test-web` - Web E2E testing with Playwright

## Resources

- **API Documentation**: http://localhost:3000/api/docs (Swagger UI)
- **README**: See root `README.md` for detailed project info
