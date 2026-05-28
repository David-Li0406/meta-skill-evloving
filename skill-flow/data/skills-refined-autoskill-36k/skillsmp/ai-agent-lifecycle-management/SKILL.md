---
name: ai-agent-lifecycle-management
description: Usage tracking, prompt versioning, and health checks for AI agents.
---

# AI Agent Lifecycle Management

> **Status**: BETA
> **Location**: `apps/api/src/app/ai-orchestrator/`
> **Primary Function**: Track AI usage, prompt versions, and provider health.

## Overview
Lifecycle management is implemented through usage metering, prompt versioning, and provider health checks. It does not yet cover deployment or scaling automation for agents.

## Verified Code References
- `apps/api/src/app/ai-orchestrator/ai-orchestrator.service.ts`
- `apps/api/src/app/ai-orchestrator/usage/usage-meter.service.ts`
- `apps/api/src/database/schema/ai-prompts.schema.ts`
- `apps/api/src/app/ai-orchestrator/providers/provider.types.ts`

## Current State

### What Already Exists
- Usage logging per team, provider, and task
- Monthly limit checks for AI tokens, requests, and cost
- Prompt versioning in `ai_prompts` table
- Provider health check with circuit breaker state

### What Still Needs to be Built
- Automated agent deployment and version rollouts
- Per-team lifecycle configuration UI
- End-to-end audit reports for AI task success rates

## Nextier-Specific Example
```typescript
// apps/api/src/app/ai-orchestrator/ai-orchestrator.service.ts
for (const provider of ["openai", "anthropic", "perplexity"] as const) {
  const start = Date.now();
  try {
    const circuitState = this.circuitBreaker?.getState?.(provider);
    const state = circuitState?.state || "closed";
    results[provider] = {
      status:
        state === "open"
          ? "down"
          : state === "half-open"
            ? "degraded"
            : "ok",
      latencyMs: Date.now() - start,
    };
  } catch {
    results[provider] = {
      status: "unknown",
      latencyMs: Date.now() - start,
    };
  }
}
```

## Integration Points
| Skill | Integration Point |
| --- | --- |
| `workflow-orchestration-engine` | Uses usage meter and prompt versions |
| `cost-guardian` | AI usage contributes to plan limits |
| `neva-research-copilot` | Research tasks tracked for usage |
| `gianna-sdr-agent` | SMS generation tracked for usage |

## Cost Information
- Cost per call is computed from provider pricing in `provider.types.ts`.
- Usage limits default to 1M tokens, 10k requests, or $50 per month.

## Multi-Tenant Considerations
- Usage records and prompt versions are stored per `teamId`.
- Limit checks are evaluated per tenant and can be overridden later by plan.
