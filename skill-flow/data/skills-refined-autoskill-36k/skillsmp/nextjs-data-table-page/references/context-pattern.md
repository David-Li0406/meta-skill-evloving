# Context Pattern

Context provides actions to child components without prop drilling.

**Note:** This pattern works with both data fetching strategies:
- **Strategy A (Simple)**: Parent uses `useState`, passes `updateItems` that calls `setData`
- **Strategy B (SWR)**: Parent uses `useSWR`, passes `updateItems` that calls `mutate`

The context interface is identical - children don't need to know which strategy is used.

## Context Provider

```tsx
// context/[entity]-actions-context.tsx
"use client";

import { createContext, useContext, ReactNode } from "react";
import type { [Entity]ActionsContextType } from "@/types/[entity]";

const [Entity]ActionsContext = createContext<[Entity]ActionsContextType | null>(null);

interface [Entity]ActionsProviderProps {
  children: ReactNode;
  actions: [Entity]ActionsContextType;
}

export function [Entity]ActionsProvider({
  children,
  actions,
}: [Entity]ActionsProviderProps) {
  return (
    <[Entity]ActionsContext.Provider value={actions}>
      {children}
    </[Entity]ActionsContext.Provider>
  );
}

export function use[Entity]Actions() {
  const context = useContext([Entity]ActionsContext);
  if (!context) {
    throw new Error("use[Entity]Actions must be used within [Entity]ActionsProvider");
  }
  return context;
}
```

## Bulk Actions Hook

```tsx
// _components/table/[entity]-table-actions.tsx
"use client";

import { toast } from "@/components/ui/custom-toast";
import { updateBulkStatus } from "@/lib/api/[entity]";
import type { [Entity]Response } from "@/types/[entity]";

interface [Entity]TableActionsProps {
  items: [Entity]Response[];
  updateItems: (items: [Entity]Response[]) => Promise<void>;
  markUpdating: (ids: string[]) => void;
  clearUpdating: (ids?: string[]) => void;
}

/**
 * Handles bulk action operations
 */
export function use[Entity]TableActions({
  items,
  updateItems,
  markUpdating,
  clearUpdating,
}: [Entity]TableActionsProps) {
  // Handle disable items
  const handleDisable = async (ids: string[]) => {
    if (ids.length === 0) return;

    // Filter to only active items (ones that need to be disabled)
    const activeItems = items.filter(
      (item) => item.id && ids.includes(item.id) && item.isActive
    );

    if (activeItems.length === 0) {
      toast.info("Selected items are already disabled");
      return;
    }

    const idsToDisable = activeItems.map((item) => item.id!);

    try {
      // Mark items as updating (show loading spinner)
      markUpdating(idsToDisable);

      // Call API and get updated items
      const response = await updateBulkStatus(idsToDisable, false);

      // Update local state with returned data
      if (response.updatedItems?.length > 0) {
        await updateItems(response.updatedItems);
        // Small delay to ensure UI updates before clearing spinner
        await new Promise((resolve) => setTimeout(resolve, 100));
      }

      toast.success(`Successfully disabled ${response.updatedItems.length} item(s)`);
    } catch (error: unknown) {
      const err = error as { data?: { detail?: string }; message?: string };
      toast.error(
        `Failed to disable items: ${err.data?.detail || err.message || "Unknown error"}`
      );
    } finally {
      clearUpdating();
    }
  };

  // Handle enable items
  const handleEnable = async (ids: string[]) => {
    if (ids.length === 0) return;

    // Filter to only inactive items (ones that need to be enabled)
    const inactiveItems = items.filter(
      (item) => item.id && ids.includes(item.id) && !item.isActive
    );

    if (inactiveItems.length === 0) {
      toast.info("Selected items are already enabled");
      return;
    }

    const idsToEnable = inactiveItems.map((item) => item.id!);

    try {
      // Mark items as updating
      markUpdating(idsToEnable);

      // Call API and get updated items
      const response = await updateBulkStatus(idsToEnable, true);

      // Update local state with returned data
      if (response.updatedItems?.length > 0) {
        await updateItems(response.updatedItems);
        await new Promise((resolve) => setTimeout(resolve, 100));
      }

      toast.success(`Successfully enabled ${response.updatedItems.length} item(s)`);
    } catch (error: unknown) {
      const err = error as { data?: { detail?: string }; message?: string };
      toast.error(
        `Failed to enable items: ${err.data?.detail || err.message || "Unknown error"}`
      );
    } finally {
      clearUpdating();
    }
  };

  return {
    handleDisable,
    handleEnable,
  };
}
```

## Controller Component

```tsx
// _components/table/[entity]-table-controller.tsx
"use client";

import { Table } from "@tanstack/react-table";
import {
  DynamicTableBar,
  SelectionDisplay,
  EnableButton,
  DisableButton,
  RefreshButton,
  ColumnToggleButton,
  SearchInput,
} from "@/components/data-table";
import { Add[Entity]Button } from "../actions/add-[entity]-button";

interface [Entity]TableControllerProps {
  selectedIds: string[];
  isUpdating: boolean;
  onClearSelection: () => void;
  onDisable: (ids: string[]) => void;
  onEnable: (ids: string[]) => void;
  onRefresh: () => void;
  tableInstance: Table<unknown> | null;
}

export function [Entity]TableController({
  selectedIds,
  isUpdating,
  onClearSelection,
  onDisable,
  onEnable,
  onRefresh,
  tableInstance,
}: [Entity]TableControllerProps) {
  return (
    <div className="shrink-0">
      <DynamicTableBar
        variant="controller"
        hasSelection={selectedIds.length > 0}
        left={
          <div className="flex items-center gap-3 flex-1">
            <SelectionDisplay
              selectedCount={selectedIds.length}
              onClearSelection={onClearSelection}
              itemName="item"
            />
            <SearchInput
              placeholder="Search..."
              urlParam="search"
              debounceMs={500}
            />
          </div>
        }
        right={
          <>
            <Add[Entity]Button onAdd={onRefresh} />
            <DisableButton
              selectedIds={selectedIds}
              onDisable={onDisable}
              disabled={isUpdating}
            />
            <EnableButton
              selectedIds={selectedIds}
              onEnable={onEnable}
              disabled={isUpdating}
            />
            <RefreshButton onRefresh={onRefresh} />
            {tableInstance && <ColumnToggleButton table={tableInstance} />}
          </>
        }
      />
    </div>
  );
}
```

## Key Points

1. **Context Pattern**: Actions defined in parent, consumed by children via hook
2. **Bulk Actions Hook**: Filters items by current state before API call
3. **Loading States**: `markUpdating`/`clearUpdating` control spinner display
4. **Toast Notifications**: Success/error feedback for all actions
5. **Server Response**: Always use API response to update cache

---

## Edit Sheet Pattern

When editing a row, table data contains only partial fields (columns shown). The edit form needs the complete entity.

**Solution:** Use `onFetchEntity` to load complete data before opening the sheet.

See [edit-sheet-pattern.md](edit-sheet-pattern.md) for the full pattern.

### Context Type with onFetchEntity

```tsx
export interface ActionResult<T = unknown> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface [Entity]ActionsContextType {
  onToggleStatus: (id: string, isActive: boolean) => Promise<ActionResult>;
  onUpdate: (id: string, payload: Record<string, unknown>) => Promise<ActionResult>;
  onBulkUpdateStatus: (ids: string[], isActive: boolean) => Promise<ActionResult>;
  onFetchEntity: (id: string) => Promise<ActionResult<[Entity]Response>>;
  onRefresh: () => Promise<ActionResult>;
  updateItems: (items: [Entity]Response[]) => void;
}
```

### Usage in Row Actions

```tsx
// _components/table/[entity]-row-actions.tsx
"use client";

import { useState, useTransition } from "react";
import { use[Entity]Actions } from "../../context/[entity]-actions-context";
import { Edit[Entity]Sheet } from "../modal/edit-[entity]-sheet";
import { toast } from "@/components/ui/custom-toast";
import type { [Entity]Response } from "@/types/[entity]";

export function [Entity]RowActions({ entityId }: { entityId: string }) {
  const { onFetchEntity, updateItems } = use[Entity]Actions();
  const [editingData, setEditingData] = useState<[Entity]Response | null>(null);
  const [isPending, startTransition] = useTransition();

  const handleEditClick = () => {
    startTransition(async () => {
      const result = await onFetchEntity(entityId);
      if (result.success && result.data) {
        setEditingData(result.data);
      } else {
        toast.error(result.error || "Failed to load item");
      }
    });
  };

  const handleUpdate = (updated: [Entity]Response) => {
    updateItems([updated]);
    setEditingData(null);
  };

  return (
    <>
      <Button onClick={handleEditClick} disabled={isPending}>
        {isPending ? <Loader2 className="animate-spin" /> : "Edit"}
      </Button>

      {editingData && (
        <Edit[Entity]Sheet
          item={editingData}
          open={!!editingData}
          onClose={() => setEditingData(null)}
          onUpdate={handleUpdate}
        />
      )}
    </>
  );
}
```

### Key Points

1. **Button shows loading** - spinner on the edit button during fetch
2. **Sheet opens ready** - no loading state inside the sheet
3. **Error handling** - toast on fetch failure, sheet doesn't open
4. **Uses context actions** - `onFetchEntity` and `updateItems` from context
