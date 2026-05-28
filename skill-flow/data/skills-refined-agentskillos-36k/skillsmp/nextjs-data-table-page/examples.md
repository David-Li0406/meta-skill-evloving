# Data Table Page Examples

Real-world examples for Next.js data table pages with SSR, SWR, and server actions.

## Example 1: Complete Page Structure

```
app/(pages)/setting/users/
├── page.tsx                      # Server component with SSR
├── loading.tsx                   # Loading skeleton
├── error.tsx                     # Error boundary
└── _components/
    ├── context/
    │   └── users-context.tsx     # Client state + SWR
    ├── table/
    │   ├── users-table.tsx       # Main table component
    │   ├── columns.tsx           # Column definitions
    │   ├── user-actions.tsx      # Row actions dropdown
    │   ├── users-toolbar.tsx     # Search, filters, bulk actions
    │   └── users-pagination.tsx  # Pagination controls
    ├── dialogs/
    │   ├── create-user-dialog.tsx
    │   └── edit-user-dialog.tsx
    └── types/
        └── index.ts              # Local types
```

## Example 2: Server Component Page (SSR)

```typescript
// app/(pages)/setting/users/page.tsx
import { auth } from "@/lib/auth/server-auth";
import { redirect } from "next/navigation";
import { getUsers } from "@/lib/actions/users.actions";
import UsersTable from "./_components/table/users-table";
import { UsersProvider } from "./_components/context/users-context";

interface PageProps {
  searchParams: Promise<{
    page?: string;
    limit?: string;
    search?: string;
    status?: string;
  }>;
}

export default async function UsersPage({ searchParams }: PageProps) {
  // Auth check
  const session = await auth();
  if (!session?.accessToken) redirect("/login");

  // Parse search params
  const params = await searchParams;
  const page = Number(params.page) || 1;
  const limit = Number(params.limit) || 10;
  const search = params.search || "";
  const status = params.status;

  // Server-side data fetching (SSR)
  const initialData = await getUsers(limit, (page - 1) * limit, { 
    search,
    is_active: status === "active" ? true : status === "inactive" ? false : undefined
  });

  return (
    <div className="container py-6">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold">Users</h1>
          <p className="text-muted-foreground">Manage system users</p>
        </div>
      </div>
      
      {/* Provider wraps client components, passes SSR data */}
      <UsersProvider initialData={initialData}>
        <UsersTable />
      </UsersProvider>
    </div>
  );
}
```

## Example 3: Context Provider with SWR

```typescript
// app/(pages)/setting/users/_components/context/users-context.tsx
"use client";

import { createContext, useContext, useState, useCallback, ReactNode } from "react";
import useSWR from "swr";
import { fetchClient } from "@/lib/fetch/client";
import type { User, UsersResponse } from "@/types/users";

interface UsersContextType {
  // Data
  users: User[];
  total: number;
  isLoading: boolean;
  error: Error | null;
  
  // Selection
  selectedIds: string[];
  setSelectedIds: (ids: string[]) => void;
  clearSelection: () => void;
  
  // Pagination
  page: number;
  setPage: (page: number) => void;
  limit: number;
  setLimit: (limit: number) => void;
  
  // Filters
  search: string;
  setSearch: (search: string) => void;
  statusFilter: string | null;
  setStatusFilter: (status: string | null) => void;
  
  // Actions
  refresh: () => void;
  mutateUsers: (data: UsersResponse) => void;
}

const UsersContext = createContext<UsersContextType | null>(null);

const fetcher = (url: string) => 
  fetchClient.get<UsersResponse>(url).then(r => r.data);

interface UsersProviderProps {
  children: ReactNode;
  initialData: UsersResponse;
}

export function UsersProvider({ children, initialData }: UsersProviderProps) {
  // Selection state
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  
  // Pagination state
  const [page, setPage] = useState(1);
  const [limit, setLimit] = useState(10);
  
  // Filter state
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState<string | null>(null);

  // Build query string
  const buildQueryString = useCallback(() => {
    const params = new URLSearchParams({
      limit: limit.toString(),
      skip: ((page - 1) * limit).toString(),
    });
    if (search) params.append("search", search);
    if (statusFilter) params.append("is_active", statusFilter === "active" ? "true" : "false");
    return params.toString();
  }, [page, limit, search, statusFilter]);

  // SWR for client-side data fetching with SSR fallback
  const { data, error, isLoading, mutate } = useSWR(
    `/api/setting/users?${buildQueryString()}`,
    fetcher,
    {
      fallbackData: initialData,
      revalidateOnFocus: false,
      revalidateOnReconnect: true,
      keepPreviousData: true,
    }
  );

  const refresh = useCallback(() => {
    mutate();
  }, [mutate]);

  const clearSelection = useCallback(() => {
    setSelectedIds([]);
  }, []);

  // Reset page when filters change
  const handleSearchChange = useCallback((value: string) => {
    setSearch(value);
    setPage(1);
  }, []);

  const handleStatusFilterChange = useCallback((value: string | null) => {
    setStatusFilter(value);
    setPage(1);
  }, []);

  return (
    <UsersContext.Provider
      value={{
        users: data?.items || [],
        total: data?.total || 0,
        isLoading,
        error,
        selectedIds,
        setSelectedIds,
        clearSelection,
        page,
        setPage,
        limit,
        setLimit,
        search,
        setSearch: handleSearchChange,
        statusFilter,
        setStatusFilter: handleStatusFilterChange,
        refresh,
        mutateUsers: mutate,
      }}
    >
      {children}
    </UsersContext.Provider>
  );
}

export function useUsers() {
  const context = useContext(UsersContext);
  if (!context) {
    throw new Error("useUsers must be used within UsersProvider");
  }
  return context;
}
```

## Example 4: Optimistic Updates

```typescript
// Optimistic delete example
const handleDelete = async (userId: string) => {
  const { users, mutateUsers, refresh } = useUsers();
  
  // Optimistic update - remove from UI immediately
  mutateUsers(
    (current) => current ? {
      ...current,
      items: current.items.filter(u => u.id !== userId),
      total: current.total - 1,
    } : current,
    false // Don't revalidate yet
  );

  try {
    const result = await deleteUser(userId);
    if (!result.success) {
      // Revert on error
      refresh();
      toast.error(result.error);
    } else {
      toast.success("User deleted");
    }
  } catch (error) {
    refresh();
    toast.error("Failed to delete user");
  }
};

// Optimistic status toggle
const handleToggleStatus = async (user: User) => {
  const { mutateUsers, refresh } = useUsers();
  
  // Optimistic update
  mutateUsers(
    (current) => current ? {
      ...current,
      items: current.items.map(u => 
        u.id === user.id ? { ...u, is_active: !u.is_active } : u
      ),
    } : current,
    false
  );

  try {
    const result = await toggleUserStatus(user.id, !user.is_active);
    if (!result.success) {
      refresh();
      toast.error(result.error);
    }
  } catch (error) {
    refresh();
    toast.error("Failed to update status");
  }
};
```

## Example 5: Bulk Actions

```typescript
// app/(pages)/setting/users/_components/table/users-toolbar.tsx
"use client";

import { useUsers } from "../context/users-context";
import { bulkDeleteUsers, bulkUpdateStatus } from "@/lib/actions/users.actions";
import { toast } from "sonner";

export function UsersToolbar() {
  const { selectedIds, clearSelection, refresh } = useUsers();
  const hasSelection = selectedIds.length > 0;

  const handleBulkDelete = async () => {
    if (!confirm(`Delete ${selectedIds.length} users?`)) return;
    
    const result = await bulkDeleteUsers(selectedIds);
    
    if (result.success) {
      toast.success(`Deleted ${selectedIds.length} users`);
      clearSelection();
      refresh();
    } else {
      toast.error(result.error);
    }
  };

  const handleBulkActivate = async () => {
    const result = await bulkUpdateStatus(selectedIds, true);
    
    if (result.success) {
      toast.success(`Activated ${selectedIds.length} users`);
      clearSelection();
      refresh();
    } else {
      toast.error(result.error);
    }
  };

  const handleBulkDeactivate = async () => {
    const result = await bulkUpdateStatus(selectedIds, false);
    
    if (result.success) {
      toast.success(`Deactivated ${selectedIds.length} users`);
      clearSelection();
      refresh();
    } else {
      toast.error(result.error);
    }
  };

  return (
    <div className="flex items-center gap-2">
      {hasSelection && (
        <>
          <span className="text-sm text-muted-foreground">
            {selectedIds.length} selected
          </span>
          <Button variant="outline" size="sm" onClick={handleBulkActivate}>
            Activate
          </Button>
          <Button variant="outline" size="sm" onClick={handleBulkDeactivate}>
            Deactivate
          </Button>
          <Button variant="destructive" size="sm" onClick={handleBulkDelete}>
            Delete
          </Button>
          <Button variant="ghost" size="sm" onClick={clearSelection}>
            Clear
          </Button>
        </>
      )}
    </div>
  );
}
```

## Example 6: Server Actions with Cache Mutation

```typescript
// lib/actions/users.actions.ts
"use server";

import { serverPost, serverPut, serverDelete } from "@/lib/fetch/server";
import { revalidatePath } from "next/cache";

export async function createUser(data: UserCreate) {
  try {
    const user = await serverPost<User>("/api/setting/users", data);
    revalidatePath("/setting/users");
    return { success: true, data: user };
  } catch (error) {
    return { success: false, error: getErrorMessage(error) };
  }
}

export async function bulkDeleteUsers(ids: string[]) {
  try {
    await serverPost("/api/setting/users/bulk-delete", { ids });
    revalidatePath("/setting/users");
    return { success: true };
  } catch (error) {
    return { success: false, error: getErrorMessage(error) };
  }
}

export async function bulkUpdateStatus(ids: string[], isActive: boolean) {
  try {
    await serverPut("/api/setting/users/status", { ids, is_active: isActive });
    revalidatePath("/setting/users");
    return { success: true };
  } catch (error) {
    return { success: false, error: getErrorMessage(error) };
  }
}
```

## Example 7: Loading & Error States

```typescript
// app/(pages)/setting/users/loading.tsx
import { Skeleton } from "@/components/ui/skeleton";

export default function Loading() {
  return (
    <div className="container py-6">
      <div className="flex justify-between items-center mb-6">
        <Skeleton className="h-8 w-32" />
        <Skeleton className="h-10 w-24" />
      </div>
      
      <div className="space-y-4">
        <div className="flex gap-2">
          <Skeleton className="h-10 w-64" />
          <Skeleton className="h-10 w-32" />
        </div>
        
        <div className="border rounded-lg">
          {Array.from({ length: 5 }).map((_, i) => (
            <div key={i} className="flex items-center gap-4 p-4 border-b last:border-0">
              <Skeleton className="h-4 w-4" />
              <Skeleton className="h-4 w-48" />
              <Skeleton className="h-4 w-32" />
              <Skeleton className="h-6 w-16" />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// app/(pages)/setting/users/error.tsx
"use client";

import { useEffect } from "react";
import { Button } from "@/components/ui/button";
import { AlertCircle } from "lucide-react";

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error("Users page error:", error);
  }, [error]);

  return (
    <div className="container py-6">
      <div className="flex flex-col items-center justify-center min-h-[400px] text-center">
        <AlertCircle className="h-12 w-12 text-destructive mb-4" />
        <h2 className="text-xl font-semibold mb-2">Something went wrong!</h2>
        <p className="text-muted-foreground mb-4 max-w-md">{error.message}</p>
        <Button onClick={reset}>Try again</Button>
      </div>
    </div>
  );
}
```

## Data Flow Summary

```
1. Initial Load (SSR):
   Server Component → getUsers() → FastAPI → Database
                   ↓
   UsersProvider receives initialData
                   ↓
   SWR uses fallbackData (no client fetch)

2. Client Navigation:
   URL change → SWR fetches → /api/setting/users → FastAPI
                          ↓
   Context updates → Components re-render

3. Mutations:
   User action → Server action → FastAPI → Database
            ↓
   revalidatePath() triggers
            ↓
   Optimistic update OR refresh()
            ↓
   SWR revalidates → UI updates
```
