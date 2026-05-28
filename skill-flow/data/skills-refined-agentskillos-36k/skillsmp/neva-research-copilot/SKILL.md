---
name: neva-research-copilot
description: Research copilot providing business intelligence and context for outreach.
---

# NEVA Research Copilot

> **Status**: PRODUCTION
> **Location**: `apps/api/src/app/neva/`
> **Primary Function**: Enrich leads with business context using Perplexity research.

## Overview
NEVA provides advisory-only research packets used to personalize outreach. It calls Perplexity via the AI Orchestrator, caches results, and stores structured context in the database.

## Verified Code References
- `apps/api/src/app/neva/neva.service.ts`
- `apps/api/src/app/neva/neva.controller.ts`
- `apps/api/src/app/neva/neva.module.ts`
- `apps/api/src/app/ai-orchestrator/ai-orchestrator.service.ts`
- `apps/api/src/lib/cache/cache.service.ts`
- `apps/api/src/database/schema/neva.schema.ts`

## Current State

### What Already Exists
- `NevaService.enrich` for Perplexity-backed research packets
- Cache-first lookup with memory + database fallback
- Confidence evaluation and risk flags
- Discovery call question preparation
- REST endpoints for enrich, context lookup, discovery prep, and evaluation

### What Still Needs to be Built
- Deeper personalization fields (industry language, opening hooks) beyond basic parsing
- Extended source tracking beyond Perplexity summary
- Admin tooling for manual research overrides

## Nextier-Specific Example
```typescript
// apps/api/src/app/neva/neva.service.ts
const cacheKey = `neva:${request.teamId}:${request.leadId}`;

if (!options?.skipCache) {
  const cached = await this.getContext(request.leadId, request.teamId);
  if (cached) {
    this.logger.log(`[NEVA] Cache hit for ${business.name}`);
    return cached;
  }
}

const query = this.buildResearchQuery(business, context);

const aiContext = {
  teamId: request.teamId,
  traceId: uuid(),
  leadId: request.leadId,
  channel: "system" as const,
};

const research = await this.aiOrchestrator.researchDeep(aiContext, query);
```

## Integration Points
| Skill | Integration Point |
| --- | --- |
| `workflow-orchestration-engine` | AI Orchestrator executes Perplexity tasks |
| `gianna-sdr-agent` | Uses NEVA recommendations for opener tone and worker selection |
| `cathy-nurture-agent` | Uses NEVA context for follow-up tone and objections |
| `lead-state-manager` | Research packets can influence lead state routing |
| `ai-co-pilot-response-generator` | Co-pilot can incorporate NEVA context if available |

## Cost Information
- Perplexity pricing is defined in `apps/api/src/app/ai-orchestrator/providers/provider.types.ts`.
- Each research call includes a per-request fee and token costs per the model pricing table.

## Multi-Tenant Considerations
- Cache keys and database rows are scoped by `teamId`.
- `NevaContextPacket` includes `teamId` and should not be reused across tenants.
