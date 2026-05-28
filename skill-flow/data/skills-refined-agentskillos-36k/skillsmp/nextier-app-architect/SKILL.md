---
name: nextier-app-architect
description: Architecture map for the OutreachGlobal Nextier Nx monorepo (NestJS API + Next.js frontend).
---

# Nextier App Architect

> **Status**: PRODUCTION
> **Location**: `apps/api/`, `apps/front/`, `nx.json`
> **Primary Function**: Provide codebase architecture context for consistent feature work.

## Overview
This skill summarizes how the Nx monorepo is organized (NestJS API in `apps/api`, Next.js UI in `apps/front`, shared packages in `packages/`) and the core platform concerns: multi-tenant isolation, AI orchestration, messaging, and enrichment.

## Verified Code References
- `apps/api/src/main.ts` - Fastify bootstrap, CORS, global prefix
- `apps/api/src/app/app.module.ts` - Module wiring (AI, messaging, billing, data lake)
- `apps/api/src/database/schema/` - Drizzle schemas and enums
- `apps/front/next.config.js` - Next.js configuration
- `nx.json` - Nx workspace configuration
- `apps/front/project.json` - Nx targets for the frontend
- `apps/api/project.json` - Nx targets for the API

## Current State

### What Already Exists
- NestJS API with Fastify adapter, GraphQL module, and global interceptors
- Next.js frontend app under `apps/front`
- AI Orchestrator with provider routing, caching, and usage metering
- Agent modules for Gianna, Cathy, Neva, Luci, and Copilot
- Messaging integrations (SignalHouse and Twilio)
- Multi-tenant scoping via `teamId` in services and schemas

### What Still Needs to be Built
- Documentation-only skill; keep references current as modules evolve.

## Nextier-Specific Example
```typescript
// apps/api/src/app/app.module.ts
BullModule.forRootAsync({
  useFactory: (configService: ConfigService) => {
    return {
      connection: {
        url: configService.get("REDIS_URL"),
      },
      prefix: "nextier_jobs",
    };
  },
  inject: [ConfigService],
  imports: [ConfigModule],
}),
```

## Integration Points
| Skill | Integration Point |
| --- | --- |
| `workflow-orchestration-engine` | AI Orchestrator providers and routing |
| `luci-enrichment-agent` | Data lake and enrichment modules |
| `signalhouse-integration` | SMS delivery and webhook handling |
| `gianna-sdr-agent` | SMS opener service and queue consumer |
| `ai-co-pilot-response-generator` | Response suggestion endpoints |

## Cost Information
- No direct external API cost; this skill documents code paths that may call paid services.

## Multi-Tenant Considerations
- `TenantContextInterceptor` sets tenant context; most services query by `teamId`.
- Database schemas include `teamId` on core tables (leads, campaigns, messages).
