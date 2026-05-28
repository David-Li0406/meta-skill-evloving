---
name: lead-journey-tracker
description: Tracks outbound/inbound messaging activity and journey signals.
---

# Lead Journey Tracker

> **Status**: BETA
> **Location**: `apps/api/src/app/message/` and journey schemas
> **Primary Function**: Record and gate communications to build journey history.

## Overview
Lead journey tracking is currently represented by message records, inbox items, and canonical lead events. It provides the foundation for attribution and analytics but does not yet implement a full journey dashboard.

## Verified Code References
- `apps/api/src/app/message/services/message.service.ts`
- `apps/api/src/app/lead/controllers/signalhouse-webhook.controller.ts`
- `apps/api/src/database/schema/canonical-lead-state.schema.ts`
- `apps/api/src/app/inbox/models/inbox-item.model.ts`

## Current State

### What Already Exists
- Message creation with outbound gating (TCPA suppression checks)
- Inbound SMS classification logged to inbox items
- Lead event schema for timeline history
- Outbound message idempotency schema

### What Still Needs to be Built
- Attribution reporting and journey visualization
- Cross-channel analytics (SMS + email + voice)
- Aggregated engagement scoring per lead

## Nextier-Specific Example
```typescript
// apps/api/src/app/message/services/message.service.ts
const gateCheck = await this.outboundGate.canContact(
  options.leadId,
  channel,
);
if (!gateCheck.allowed) {
  throw new ForbiddenException(
    `Cannot send ${channel.toUpperCase()}: ${gateCheck.reason}`,
  );
}
```

## Integration Points
| Skill | Integration Point |
| --- | --- |
| `signalhouse-integration` | Inbound SMS events create journey entries |
| `lead-state-manager` | Lead events provide lifecycle milestones |
| `gianna-sdr-agent` | Outbound and inbound SMS logged to messages |
| `cathy-nurture-agent` | Follow-up cadence ties into message history |
| `campaign-optimizer` | Campaign activity drives message volume |

## Cost Information
- No direct external API costs; messaging costs are billed by providers.

## Multi-Tenant Considerations
- Message and inbox queries are filtered by `teamId`.
- Suppression checks prevent cross-tenant messaging errors.
