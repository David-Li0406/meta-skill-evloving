---
name: ai-co-pilot-response-generator
description: Generates response suggestions and auto-replies for inbound messages using AI Orchestrator.
---

# AI Co-Pilot Response Generator

> **Status**: BETA
> **Location**: `apps/api/src/app/ai-co-pilot/`
> **Primary Function**: Suggest and auto-respond to inbound SMS with context-aware replies.

## Overview
Co-Pilot generates reply suggestions for inbound messages using conversation history, lead context, and agent personality mapping. It exposes both REST and GraphQL endpoints and can auto-respond to specific objections.

## Verified Code References
- `apps/api/src/app/ai-co-pilot/services/response-generator.service.ts`
- `apps/api/src/app/ai-co-pilot/services/auto-respond.service.ts`
- `apps/api/src/app/ai-co-pilot/ai-co-pilot.controller.ts`
- `apps/api/src/app/ai-co-pilot/resolvers/co-pilot.resolver.ts`
- `apps/api/src/app/ai-co-pilot/ai-co-pilot.module.ts`
- `apps/api/src/app/ai-orchestrator/ai-orchestrator.service.ts`
- `apps/api/src/database/schema/worker-phones.schema.ts`

## Current State

### What Already Exists
- Response suggestion generation with AI Orchestrator and template fallback
- Phone number to tenant mapping via worker phone assignments and phone pools
- Conversation history lookup from `messages` table
- REST endpoints for generate, inbound, auto-respond, and phone config
- GraphQL queries and mutations for suggestions

### What Still Needs to be Built
- Persisted suggestion storage and acceptance analytics (accept/reject are no-ops today)
- Fine-grained per-team response style configuration
- Unified review queue for auto-respond outcomes

## Nextier-Specific Example
```typescript
// apps/api/src/app/ai-co-pilot/services/response-generator.service.ts
const history = await this.getConversationHistory(conversationId, 10);
const lead = await this.getLeadByPhone(phoneNumber);
const campaign = lead?.campaignId
  ? await this.getCampaign(lead.campaignId)
  : undefined;

const context = this.buildContext(
  inboundMessage,
  history,
  lead,
  campaign,
  config,
);

const suggestions = await this.generateAISuggestions(
  teamId,
  context,
  maxSuggestions,
  preferredTone,
  includeReasoning,
);
```

## Integration Points
| Skill | Integration Point |
| --- | --- |
| `workflow-orchestration-engine` | AI Orchestrator for suggestion generation |
| `signalhouse-integration` | Auto-respond sends SMS via SignalHouse |
| `gianna-sdr-agent` | Shared agent personality mapping and SMS tone |
| `lead-journey-tracker` | Conversation history uses `messages` table |
| `lead-state-manager` | Auto-respond outcomes can drive state changes |

## Cost Information
- Suggestion generation uses OpenAI pricing from `apps/api/src/app/ai-orchestrator/providers/provider.types.ts`.
- Auto-respond messages incur SignalHouse SMS costs (not priced in code).

## Multi-Tenant Considerations
- `teamId` controls response generation and authorization in both REST and GraphQL layers.
- Phone number mapping ties inbound numbers to the owning team.
