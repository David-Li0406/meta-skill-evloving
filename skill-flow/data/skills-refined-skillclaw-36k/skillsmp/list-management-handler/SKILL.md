---
name: list-management-handler
description: Lead list CRUD, segmentation, and filtering for team-scoped lead data.
---

# List Management Handler

> **Status**: BETA
> **Location**: `apps/api/src/app/lead/`
> **Primary Function**: Query and filter leads by tags, search, and phone availability.

## Overview
List management is implemented through lead services, filters, and business-list search. It supports pagination, tag filtering, and dedup strategies, but does not yet model saved lists as first-class entities.

## Verified Code References
- `apps/api/src/app/lead/services/lead.service.ts`
- `apps/api/src/app/lead/services/lead-filter.service.ts`
- `apps/api/src/app/lead/controllers/business-list.controller.ts`
- `apps/api/src/app/lead/repositories/lead.repository.ts`
- `apps/api/src/app/team/objects/business-list-settings.object.ts`

## Current State

### What Already Exists
- Lead pagination with tag, phone, and search filters
- Lead CRUD operations and phone number management
- Business list search controller (team-scoped)
- Redis-backed dedup and filtering in `LeadFilterService`

### What Still Needs to be Built
- Saved list entities and list membership tracking
- List-level analytics and export utilities
- UI workflows for list segmentation and scheduling

## Nextier-Specific Example
```typescript
// apps/api/src/app/lead/services/lead.service.ts
const query = this.db
  .select()
  .from(leadsTable)
  .where((t) =>
    and(
      eq(t.teamId, options.teamId),
      options?.tags?.length
        ? arrayOverlaps(t.tags, options.tags)
        : undefined,
      typeof options.hasPhone === "boolean"
        ? options.hasPhone
          ? isNotNull(t.phone)
          : isNull(t.phone)
        : undefined,
      !options.searchQuery
        ? undefined
        : or(
            ilike(t.firstName, `%${options.searchQuery}%`),
            ilike(t.lastName, `%${options.searchQuery}%`),
            ilike(t.company, `%${options.searchQuery}%`),
            ilike(t.email, `%${options.searchQuery}%`),
            ilike(t.phone, `%${options.searchQuery}%`),
          ),
    ),
  )
  .$dynamic();
```

## Integration Points
| Skill | Integration Point |
| --- | --- |
| `data-lake-orchestration-agent` | Raw list items become leads after enrichment |
| `lead-state-manager` | List filtering often drives state-based segments |
| `campaign-optimizer` | Campaigns use lead filters for targeting |
| `workflow-orchestration-engine` | Batch filtering and dedup workflows |

## Cost Information
- No direct API cost in lead filtering; business list provider costs depend on external billing.

## Multi-Tenant Considerations
- All list queries require `teamId` and filter by tenant scope.
- Redis dedup keys are prefixed with `teamId` to avoid cross-tenant collisions.
