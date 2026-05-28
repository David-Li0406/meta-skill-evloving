# Columns Pattern

Column definitions use TanStack Table with loading state support via `updatingIds`.

## Table Body Component

```tsx
// _components/table/[entity]-table-body.tsx
"use client";

import { DataTable } from "@/components/data-table";
import { useMemo, useState, useCallback } from "react";
import type { [Entity]Response } from "@/types/[entity]";
import { [Entity]TableController } from "./[entity]-table-controller";
import { create[Entity]TableColumns } from "./[entity]-table-columns";
import { use[Entity]TableActions } from "./[entity]-table-actions";
import { [Entity]Actions } from "../actions/actions-menu";

interface [Entity]TableBodyProps {
  items: [Entity]Response[];
  mutate: () => void;
  updateItems: (items: [Entity]Response[]) => Promise<void>;
}

export default function [Entity]TableBody({
  items,
  mutate,
  updateItems,
}: [Entity]TableBodyProps) {
  const [tableInstance, setTableInstance] = useState<
    import("@tanstack/react-table").Table<[Entity]Response> | null
  >(null);
  const [selectedItems, setSelectedItems] = useState<[Entity]Response[]>([]);
  const [updatingIds, setUpdatingIds] = useState<Set<string>>(new Set());
  const isUpdating = updatingIds.size > 0;

  const selectedIds = selectedItems
    .map((item) => item.id)
    .filter(Boolean) as string[];

  // Mark items as being updated
  const markUpdating = useCallback((ids: string[]) => {
    setUpdatingIds(new Set(ids));
  }, []);

  // Clear updating state
  const clearUpdating = useCallback(
    (ids?: string[]) => {
      if (ids?.length) {
        const newSet = new Set(updatingIds);
        ids.forEach((id) => newSet.delete(id));
        setUpdatingIds(newSet);
      } else {
        setUpdatingIds(new Set());
      }
    },
    [updatingIds]
  );

  // Handle clear selection after bulk operations
  const handleClearSelection = useCallback(() => {
    setSelectedItems([]);
  }, []);

  // Handle refresh
  const handleRefresh = useCallback(() => {
    mutate();
  }, [mutate]);

  // Get bulk action handlers
  const { handleDisable, handleEnable } = use[Entity]TableActions({
    items,
    updateItems,
    markUpdating,
    clearUpdating,
  });

  // Create columns with actions
  const columns = useMemo(
    () =>
      create[Entity]TableColumns({
        updatingIds,
        updateItems,
        mutate,
        markUpdating,
        clearUpdating,
      }).map((column) => {
        // Special handling for actions column
        if (column.id === "actions") {
          return {
            ...column,
            cell: ({ row }: { row: { original: [Entity]Response } }) => {
              const isRowUpdating = Boolean(
                row.original.id && updatingIds.has(row.original.id)
              );
              return (
                <div
                  className={`flex justify-center ${
                    isRowUpdating ? "opacity-60 pointer-events-none" : ""
                  }`}
                  onClick={(e) => e.stopPropagation()}
                >
                  <[Entity]Actions
                    item={row.original}
                    onUpdate={mutate}
                    onItemUpdated={(updated) => updateItems([updated])}
                    disabled={isRowUpdating}
                  />
                </div>
              );
            },
          };
        }
        return column;
      }),
    [updatingIds, updateItems, mutate, markUpdating, clearUpdating]
  );

  // Memoize data
  const data = useMemo(() => items, [items]);

  return (
    <div className="h-full flex flex-col min-h-0 ml-2 space-y-2">
      {/* Controller Bar */}
      <[Entity]TableController
        selectedIds={selectedIds}
        isUpdating={isUpdating}
        onClearSelection={handleClearSelection}
        onDisable={handleDisable}
        onEnable={handleEnable}
        onRefresh={handleRefresh}
        tableInstance={tableInstance}
      />

      {/* Table */}
      <div className="flex-1 min-h-0 flex flex-col">
        <DataTable
          columns={columns}
          data={data}
          tableInstanceHook={(table) => setTableInstance(table)}
          onRowSelectionChange={setSelectedItems}
          renderToolbar={() => null}
          enableRowSelection={true}
          enableSorting={false}
        />
      </div>
    </div>
  );
}
```

## Columns Definition

```tsx
// _components/table/[entity]-table-columns.tsx
"use client";

import { ColumnDef } from "@tanstack/react-table";
import { Badge } from "@/components/ui/badge";
import { StatusSwitch } from "@/components/ui/status-switch";
import { Loader2 } from "lucide-react";
import type { [Entity]Response } from "@/types/[entity]";
import { toggleStatus } from "@/lib/api/[entity]";

interface ColumnsProps {
  updatingIds: Set<string>;
  mutate: () => void;
  markUpdating: (ids: string[]) => void;
  clearUpdating: (ids?: string[]) => void;
  updateItems: (items: [Entity]Response[]) => Promise<void>;
}

export function create[Entity]TableColumns({
  updatingIds,
  mutate,
  markUpdating,
  clearUpdating,
  updateItems,
}: ColumnsProps): ColumnDef<[Entity]Response>[] {
  return [
    // Selection column
    {
      id: "select",
      header: ({ table }) => (
        <div className="flex justify-center">
          <input
            type="checkbox"
            className="rounded border-gray-300 cursor-pointer"
            checked={table.getIsAllPageRowsSelected()}
            onChange={(e) => table.toggleAllPageRowsSelected(e.target.checked)}
            disabled={updatingIds.size > 0}
          />
        </div>
      ),
      cell: ({ row }) => {
        const isRowUpdating = Boolean(
          row.original.id && updatingIds.has(row.original.id)
        );
        return (
          <div
            className={`flex justify-center items-center px-2 ${
              isRowUpdating ? "opacity-60" : ""
            }`}
          >
            {isRowUpdating ? (
              <Loader2 className="w-4 h-4 text-blue-600 animate-spin" />
            ) : (
              <input
                type="checkbox"
                className="rounded border-gray-300 cursor-pointer disabled:opacity-50"
                checked={row.getIsSelected()}
                onChange={(e) => {
                  e.stopPropagation();
                  row.toggleSelected(e.target.checked);
                }}
                disabled={updatingIds.size > 0}
              />
            )}
          </div>
        );
      },
      enableSorting: false,
      enableHiding: false,
      size: 40,
    },

    // ID column (use _id for TanStack Table internal ID)
    {
      id: "_id",
      accessorKey: "id",
      header: () => <div className="text-center">ID</div>,
      cell: (info) => {
        const isRowUpdating = Boolean(
          info.row.original.id && updatingIds.has(info.row.original.id)
        );
        return (
          <div
            className={`text-center font-mono text-sm ${
              isRowUpdating ? "opacity-60" : ""
            }`}
          >
            {info.getValue() as string}
          </div>
        );
      },
    },

    // Name column (example)
    {
      id: "name",
      accessorKey: "name",
      header: () => <div className="text-center">Name</div>,
      cell: (info) => {
        const isRowUpdating = Boolean(
          info.row.original.id && updatingIds.has(info.row.original.id)
        );
        return (
          <div
            className={`flex items-center justify-center gap-2 ${
              isRowUpdating ? "opacity-60" : ""
            }`}
          >
            <span className="font-medium">{info.getValue() as string}</span>
          </div>
        );
      },
    },

    // Status column with toggle
    {
      id: "isActive",
      accessorKey: "isActive",
      header: () => <div className="text-center">Active</div>,
      cell: ({ row }) => {
        const item = row.original;
        const isRowUpdating = Boolean(item.id && updatingIds.has(item.id));
        return (
          <div
            className={`flex justify-center items-center ${
              isRowUpdating ? "opacity-60 pointer-events-none" : ""
            }`}
          >
            <StatusSwitch
              checked={item.isActive}
              onToggle={async () => {
                if (!item.id) return;
                markUpdating([item.id]);
                try {
                  const updated = await toggleStatus(item.id, !item.isActive);
                  await updateItems([updated]);
                } finally {
                  clearUpdating([item.id]);
                }
              }}
              title={item.isActive ? "Deactivate" : "Activate"}
              description={`Are you sure you want to ${
                item.isActive ? "deactivate" : "activate"
              } this item?`}
              size="sm"
            />
          </div>
        );
      },
      enableHiding: true,
    },

    // Actions column (populated in table body)
    {
      id: "actions",
      header: () => <div className="text-center">Actions</div>,
      cell: () => null, // Populated dynamically in table body
      enableSorting: false,
      enableHiding: false,
    },
  ];
}
```

## Key Points

1. **updatingIds Set**: Tracks which rows are being updated
2. **Loading States**: Show spinner, disable interactions during updates
3. **Stop Propagation**: Prevent row selection when clicking actions
4. **StatusSwitch**: Confirmation dialog before status toggle
5. **Actions Column**: Placeholder filled by table body with actual menu
