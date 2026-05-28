---
name: cathy-nurture-agent
description: Nurture agent for follow-up messaging with escalation to Sabrina or human review.
---

# CATHY Nurture Agent

> **Status**: PRODUCTION
> **Location**: `apps/api/src/app/cathy/`
> **Primary Function**: Generate nurture follow-ups and classify inbound replies.

## Overview
CATHY handles longer-cycle follow-ups after initial contact. It generates nurture messages from stage-based templates, detects scheduling intent for escalation, and uses the AI Orchestrator for positive-response suggestions.

## Verified Code References
- `apps/api/src/app/cathy/cathy.service.ts`
- `apps/api/src/app/cathy/cathy.controller.ts`
- `apps/api/src/app/cathy/cathy.module.ts`
- `apps/api/src/app/ai-orchestrator/ai-orchestrator.service.ts`
- `apps/api/src/database/schema-alias.ts` (leadsTable, messagesTable)

## Current State

### What Already Exists
- Stage-based nurture templates and follow-up cadence logic
- Scheduling intent detection with escalation flagging
- Positive-response AI suggestion via `AiOrchestratorService`
- Lead selection for nurture based on message recency
- REST endpoints for generate, process-response, and leads-to-nurture

### What Still Needs to be Built
- Persistent nurture stage tracking per lead beyond `touchCount`
- Automated queue processing for outbound nurture sends
- Human review persistence for escalations
- Analytics for nurture sequence performance

## Nextier-Specific Example
```typescript
// apps/api/src/app/cathy/cathy.service.ts
private getSuggestedFollowupDays(stage: NurtureStage): number {
  const followupMap: Record<NurtureStage, number> = {
    initial_followup: 2,
    value_building: 4,
    objection_handling: 5,
    re_engagement: 7,
    final_attempt: 14,
  };
  return followupMap[stage];
}
```

## Integration Points
| Skill | Integration Point |
| --- | --- |
| `gianna-sdr-agent` | Escalation from opener to nurture stage via agent routing |
| `workflow-orchestration-engine` | AI response generation for positive replies |
| `lead-state-manager` | Uses lead context and message history for stage selection |
| `signalhouse-integration` | Outbound delivery handled by shared SMS infrastructure |
| `ai-co-pilot-response-generator` | Shared response tone and agent personality mapping |

## Cost Information
- AI suggestions use OpenAI pricing from `apps/api/src/app/ai-orchestrator/providers/provider.types.ts`.
- No additional external API costs are defined in this module.

## Multi-Tenant Considerations
- `teamId` is required on all service calls and used for data access.
- Lead and message queries are filtered by `teamId`.
