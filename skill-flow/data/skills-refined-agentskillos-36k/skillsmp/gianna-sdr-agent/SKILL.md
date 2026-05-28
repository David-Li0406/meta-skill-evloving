---
name: gianna-sdr-agent
description: SMS opener agent that generates cold outreach and routes responses for Nextier.
---

# GIANNA SDR Agent

> **Status**: PRODUCTION
> **Location**: `apps/api/src/app/gianna/`
> **Primary Function**: Generate SMS openers and classify inbound replies.

## Overview
GIANNA handles template-based outbound openers and inbound reply classification, with queue-based sending and escalation to CATHY or SABRINA. AI fallback is available via the AI Orchestrator.

## Verified Code References
- `apps/api/src/app/gianna/gianna.service.ts`
- `apps/api/src/app/gianna/gianna.controller.ts`
- `apps/api/src/app/gianna/gianna.consumer.ts`
- `apps/api/src/app/gianna/gianna.module.ts`
- `apps/api/src/lib/signalhouse/signalhouse.service.ts`
- `apps/api/src/app/ai-orchestrator/ai-orchestrator.service.ts`
- `apps/api/src/database/schema-alias.ts` (messagesTable, leadsTable)

## Current State

### What Already Exists
- Opener templates by category (property, business, general)
- Intent classification with opt-out handling
- Queue-based SMS delivery via BullMQ consumer
- Escalation events to CATHY and SABRINA
- AI fallback using AiOrchestrator for freeform responses
- REST endpoints for opener, respond, send, classify, and health

### What Still Needs to be Built
- Persistent conversation state beyond message count
- Human review workflow persistence (only flags in response today)
- A/B testing analytics for opener performance
- Team-level personality configuration storage

## Nextier-Specific Example
```typescript
// apps/api/src/app/gianna/gianna.service.ts
async generateOpener(
  context: GiannaContext,
  category: "property" | "business" | "general" = "general",
): Promise<GiannaResponse> {
  const templates = OPENER_TEMPLATES[category] || OPENER_TEMPLATES.general;
  const template = templates[Math.floor(Math.random() * templates.length)];

  const message = this.applyTemplate(template, context);

  return {
    message,
    confidence: 100,
    requiresHumanReview: false,
    nextAction: { type: "wait" },
  };
}
```

## Integration Points
| Skill | Integration Point |
| --- | --- |
| `signalhouse-integration` | SMS delivery via `SignalHouseService` in the consumer |
| `cathy-nurture-agent` | Escalation for nurture flows (`escalate-cathy`) |
| `workflow-orchestration-engine` | AI fallback via `AiOrchestratorService` |
| `lead-state-manager` | State transitions handled downstream from inbound events |
| `ai-co-pilot-response-generator` | Shares inbound response context and messaging data |

## Cost Information
- AI fallback uses OpenAI pricing from `apps/api/src/app/ai-orchestrator/providers/provider.types.ts`.
- SMS costs are billed by SignalHouse and not hard-coded in this module.

## Multi-Tenant Considerations
- `teamId` is required on all requests and used for DB queries and queue jobs.
- Message logs store `teamId` to keep agent activity isolated.
