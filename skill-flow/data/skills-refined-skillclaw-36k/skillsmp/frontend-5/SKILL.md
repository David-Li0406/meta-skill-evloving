---
name: frontend
description: Scaffold frontend CRUD pages - queries hook, route, page, table, and create dialog. Use after data_model scaffold when building UI for an entity.
---

# Frontend Scaffolding

Generates React components for CRUD operations on an entity.

## Quick Scaffold

```bash
python .claude/skills/frontend/scripts/scaffold.py <EntityName>

# Examples:
python .claude/skills/frontend/scripts/scaffold.py Campaign
python .claude/skills/frontend/scripts/scaffold.py BlogPost --dry-run
```

**Prerequisites**: Run `data_model` scaffold first to create oRPC routes.

## Generated Files

| File | Path |
|------|------|
| Queries hook | `packages/dash/ui/src/queries/{entity-name}.ts` |
| Route | `packages/dash/ui/src/routes/_authenticated/workspaces/$workspaceSlug/{entity-name}.tsx` |
| Page | `packages/dash/ui/src/components/{entity-name}/{EntityName}Page.tsx` |
| Table | `packages/dash/ui/src/components/{entity-name}/{EntityName}Table.tsx` |
| Create dialog | `packages/dash/ui/src/components/{entity-name}/{EntityName}CreateDialog.tsx` |

## Post-Scaffold Steps

1. Add route to sidebar (if needed)
2. Customize table columns
3. Add form fields to create dialog
4. Run `pnpm lint`

---

## Patterns

### Grouped Query Hook

All CRUD operations in one hook:

```typescript
const { list, create, update, remove } = useCampaign();

// List data
const { data, isLoading } = list;

// Mutations
await create.mutateAsync({ workspaceSlug, name });
await update.mutateAsync({ workspaceSlug, id, name });
await remove.mutateAsync({ workspaceSlug, id });
```

### oRPC Direct Usage

For one-off queries, use oRPC directly:

```typescript
import { orpc } from "@/lib/orpc-client";

// In component
const { data } = useQuery(
  orpc.campaign.list.queryOptions({
    input: { workspaceSlug },
  })
);

// Direct call (in handlers, loaders)
const result = await orpc.campaign.create.call({
  workspaceSlug,
  name: "New Campaign",
});

// Query key for invalidation
queryClient.invalidateQueries({
  queryKey: orpc.campaign.list.key({ input: { workspaceSlug } }),
});
```

### TanStack Router Pattern

```typescript
import { createFileRoute } from "@tanstack/react-router";
import * as z from "zod";

const searchSchema = z.object({
  status: z.enum(["active", "paused"]).optional(),
  page: z.coerce.number().positive().optional(),
});

export const Route = createFileRoute(
  "/_authenticated/workspaces/$workspaceSlug/campaign",
)({
  validateSearch: searchSchema,
  pendingComponent: WorkspaceLoading,
  component: CampaignPage,
});
```

---

## Reference Files

| Component | Example |
|-----------|---------|
| Queries | `packages/dash/ui/src/queries/radar.ts` |
| Route | `packages/dash/ui/src/routes/_authenticated/workspaces/$workspaceSlug/radar.tsx` |
| Page | `packages/dash/ui/src/components/radar/RadarPage.tsx` |
| Table | `packages/dash/ui/src/components/radar/RadarSourceTable.tsx` |
