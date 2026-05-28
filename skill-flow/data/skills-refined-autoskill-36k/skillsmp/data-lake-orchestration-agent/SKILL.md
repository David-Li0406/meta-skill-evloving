---
name: data-lake-orchestration-agent
description: CSV import and list-item orchestration for the raw data lake feeding LUCI.
---

# Data Lake Orchestration Agent

> **Status**: PRODUCTION
> **Location**: `apps/api/src/app/raw-data-lake/`
> **Primary Function**: Import raw list items, tag verticals, and prepare blocks for enrichment.

## Overview
The raw data lake is the entry point for CSV list imports. It stores list items (not yet leads) and exposes endpoints to browse, segment, and create enrichment blocks for LUCI.

## Verified Code References
- `apps/api/src/app/raw-data-lake/raw-data-lake.service.ts`
- `apps/api/src/app/raw-data-lake/raw-data-lake.controller.ts`
- `apps/api/src/app/raw-data-lake/raw-data-lake.module.ts`
- `apps/api/src/database/schema-alias.ts` (leadsTable)

## Current State

### What Already Exists
- USBizData CSV parsing with fixed column mapping
- Vertical detection via SIC codes and sector tags
- Browse, stats, and vertical summary endpoints
- Block creation for enrichment handoff to LUCI

### What Still Needs to be Built
- External object store import connectors beyond CSV strings
- Export utilities for raw list items
- Multi-file import batching UI workflows

## Nextier-Specific Example
```typescript
// apps/api/src/app/raw-data-lake/raw-data-lake.service.ts
const content =
  typeof csvBuffer === "string" ? csvBuffer : csvBuffer.toString("utf-8");
const records = this.parseCSV(content);

stats.total = records.length;
if (records.length === 0) {
  return stats;
}
```

## Integration Points
| Skill | Integration Point |
| --- | --- |
| `luci-enrichment-agent` | Block creation and enrichment handoff |
| `list-management-handler` | Lead list browsing and segmentation inputs |
| `cost-guardian` | Estimated enrichment cost for block sizing |
| `workflow-orchestration-engine` | Batch import workflows and scheduling |

## Cost Information
- Raw imports are free; enrichment costs begin when LUCI runs Tracerfy/Trestle.
- Estimated enrichment cost is surfaced in block creation responses.

## Multi-Tenant Considerations
- All queries are scoped by `teamId` via `TenantContext`.
- Raw list items are stored per team to prevent cross-tenant visibility.
