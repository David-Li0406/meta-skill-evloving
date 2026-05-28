---
name: lead-state-manager
description: Canonical lead state machine with transitions, timers, and event logging.
---

# Lead State Manager

> **Status**: BETA
> **Location**: `apps/api/src/app/lead/` and `apps/api/src/database/schema/canonical-lead-state.schema.ts`
> **Primary Function**: Enforce valid lead lifecycle transitions with timers and events.

## Overview
Lead state transitions are centralized in `LeadService.updateLeadState` and backed by a canonical schema that defines states, events, and timers. Timers are executed by a scheduled job to advance retargeting flows.

## Verified Code References
- `apps/api/src/app/lead/services/lead.service.ts`
- `apps/api/src/database/schema/canonical-lead-state.schema.ts`
- `apps/api/src/app/lead/schedules/lead.schedule.ts`
- `apps/api/src/app/lead/controllers/signalhouse-webhook.controller.ts`

## Current State

### What Already Exists
- Canonical `LeadState` enum and transition map
- Event log and timer tables for state changes
- `updateLeadState` validation and event recording
- Timer execution job for 7D/14D transitions
- Inbound SMS webhooks enqueue state transitions

### What Still Needs to be Built
- Centralized UI for state history and transition auditing
- State-based SLA reporting and alerting
- External integrations to trigger transitions (beyond SignalHouse)

## Nextier-Specific Example
```typescript
// apps/api/src/database/schema/canonical-lead-state.schema.ts
export const VALID_STATE_TRANSITIONS: Record<LeadState, LeadState[]> = {
  new: ["touched", "suppressed"],
  touched: ["retargeting", "responded", "suppressed"],
  retargeting: ["responded", "suppressed"],
  responded: [
    "soft_interest",
    "email_captured",
    "high_intent",
    "in_call_queue",
    "suppressed",
  ],
  soft_interest: [
    "email_captured",
    "content_nurture",
    "high_intent",
    "in_call_queue",
    "suppressed",
  ],
  email_captured: [
    "content_nurture",
    "high_intent",
    "in_call_queue",
    "suppressed",
  ],
  content_nurture: [
    "high_intent",
    "appointment_booked",
    "in_call_queue",
    "suppressed",
  ],
  high_intent: ["appointment_booked", "in_call_queue", "closed", "suppressed"],
  appointment_booked: ["in_call_queue", "closed", "suppressed"],
  in_call_queue: ["closed", "suppressed"],
  closed: [],
  suppressed: [],
};
```

## Integration Points
| Skill | Integration Point |
| --- | --- |
| `signalhouse-integration` | Inbound SMS triggers state transitions via webhook |
| `gianna-sdr-agent` | Escalations and responses influence state updates |
| `cathy-nurture-agent` | Nurture cadence relates to retargeting timers |
| `lead-journey-tracker` | Events and messages provide journey context |
| `workflow-orchestration-engine` | Timer execution and queue coordination |

## Cost Information
- No external API costs; state transitions are internal DB operations.

## Multi-Tenant Considerations
- `teamId` is enforced on all transitions and event inserts.
- Timer queries and event logs are filtered by tenant scope.
