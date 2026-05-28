---
name: workflow-orchestration-engine
description: Central AI Orchestrator for routing tasks, fallbacks, caching, and usage tracking.
---

# Workflow Orchestration Engine

> **Status**: PRODUCTION
> **Location**: `apps/api/src/app/ai-orchestrator/`
> **Primary Function**: Execute AI tasks with provider routing, fallbacks, and caching.

## Overview
The AI Orchestrator is the single entry point for AI tasks (SMS classify/generate, research). It handles provider routing, fallback chains, caching for research tasks, and usage tracking.

## Verified Code References
- `apps/api/src/app/ai-orchestrator/ai-orchestrator.service.ts`
- `apps/api/src/app/ai-orchestrator/providers/provider.types.ts`
- `apps/api/src/app/ai-orchestrator/usage/usage-meter.service.ts`
- `apps/api/src/database/schema/ai-prompts.schema.ts`

## Current State

### What Already Exists
- Provider routing and fallback chains across OpenAI, Anthropic, Perplexity
- Prompt lookup from `ai_prompts` with versioning
- Research result caching for Perplexity tasks
- Usage metering and dashboard aggregation
- Health checks for provider circuit breakers

### What Still Needs to be Built
- Per-team policy overrides for model routing
- Cost-based throttling for all tasks
- Unified orchestration metrics dashboards in UI

## Nextier-Specific Example
```typescript
// apps/api/src/app/ai-orchestrator/ai-orchestrator.service.ts
const providers: AiProvider[] = options.skipFallback
  ? [routing.provider]
  : [routing.provider, ...(FALLBACK_CHAINS[routing.provider] || [])];

for (let i = 0; i < providers.length; i++) {
  const provider = providers[i];
  const model =
    i === 0
      ? prompt?.model || routing.model
      : this.getFallbackModel(provider, task);

  // provider call handled in callProvider(...)
}
```

## Integration Points
| Skill | Integration Point |
| --- | --- |
| `gianna-sdr-agent` | SMS classification and AI fallback responses |
| `cathy-nurture-agent` | Positive-response generation |
| `neva-research-copilot` | Perplexity research tasks |
| `ai-co-pilot-response-generator` | Response suggestions for inbox |
| `ai-agent-lifecycle-management` | Usage tracking and health checks |

## Cost Information
- Model pricing is defined in `provider.types.ts` and used to compute cost per call.
- Usage is recorded in `usage_records` via `UsageMeterService`.

## Multi-Tenant Considerations
- All AI calls are scoped by `AiContext.teamId`.
- Usage records and prompts are stored per team.
