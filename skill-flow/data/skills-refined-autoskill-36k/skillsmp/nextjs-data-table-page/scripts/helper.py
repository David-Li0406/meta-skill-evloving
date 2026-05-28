#!/usr/bin/env python3
"""
Data Table Page Helper Script

Utilities for generating Next.js data table pages with SSR, SWR, and server actions.

Usage:
    python helper.py generate NAME [BASE_PATH]  # Generate complete data table page
    python helper.py page NAME [BASE_PATH]      # Generate page.tsx only
    python helper.py context NAME [BASE_PATH]   # Generate context provider only
    python helper.py table NAME [BASE_PATH]     # Generate table components only
    python helper.py columns NAME [FIELDS]      # Generate columns with fields
    python helper.py actions NAME [BASE_PATH]   # Generate server actions only
    python helper.py api NAME [BASE_PATH]       # Generate API routes only
    python helper.py types NAME [FIELDS]        # Generate TypeScript types
    python helper.py validate                   # Validate existing structure
"""

import sys
import os
import re
import json

def to_pascal(name: str) -> str:
    """Convert to PascalCase."""
    return ''.join(word.capitalize() for word in name.replace('-', '_').split('_'))

def to_kebab(name: str) -> str:
    """Convert to kebab-case."""
    s = re.sub(r'(?<!^)(?=[A-Z])', '-', name).lower()
    return s.replace('_', '-')

def to_camel(name: str) -> str:
    """Convert to camelCase."""
    pascal = to_pascal(name)
    return pascal[0].lower() + pascal[1:]

def generate_page(name: str, base_path: str = "setting"):
    """Generate page.tsx with SSR data loading."""
    pascal = to_pascal(name)
    kebab = to_kebab(name)
    camel = to_camel(name)
    
    dir_path = f"app/(pages)/{base_path}/{kebab}"
    os.makedirs(dir_path, exist_ok=True)
    
    template = f'''import {{ auth }} from "@/lib/auth/server-auth";
import {{ redirect }} from "next/navigation";
import {{ get{pascal}s }} from "@/lib/actions/{kebab}.actions";
import {pascal}sTable from "./_components/table/{kebab}s-table";
import {{ {pascal}sProvider }} from "./_components/context/{kebab}s-context";

interface PageProps {{
  searchParams: Promise<{{
    page?: string;
    limit?: string;
    search?: string;
  }}>;
}}

export default async function {pascal}sPage({{ searchParams }}: PageProps) {{
  const session = await auth();
  if (!session?.accessToken) redirect("/login");

  const params = await searchParams;
  const page = Number(params.page) || 1;
  const limit = Number(params.limit) || 10;
  const search = params.search || "";

  // SSR data fetching
  const initialData = await get{pascal}s(limit, (page - 1) * limit, {{ search }});

  return (
    <div className="container py-6">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold">{pascal}s</h1>
          <p className="text-muted-foreground">Manage {camel}s</p>
        </div>
      </div>
      
      <{pascal}sProvider initialData={{initialData}}>
        <{pascal}sTable />
      </{pascal}sProvider>
    </div>
  );
}}
'''
    
    # Loading state
    loading_template = f'''import {{ Skeleton }} from "@/components/ui/skeleton";

export default function Loading() {{
  return (
    <div className="container py-6">
      <div className="flex justify-between items-center mb-6">
        <Skeleton className="h-8 w-32" />
        <Skeleton className="h-10 w-24" />
      </div>
      <div className="space-y-4">
        <Skeleton className="h-10 w-64" />
        <div className="border rounded-lg">
          {{Array.from({{ length: 5 }}).map((_, i) => (
            <div key={{i}} className="flex items-center gap-4 p-4 border-b last:border-0">
              <Skeleton className="h-4 w-4" />
              <Skeleton className="h-4 w-48" />
              <Skeleton className="h-4 w-32" />
            </div>
          ))}}
        </div>
      </div>
    </div>
  );
}}
'''
    
    # Error boundary
    error_template = f'''"use client";

import {{ useEffect }} from "react";
import {{ Button }} from "@/components/ui/button";

export default function Error({{
  error,
  reset,
}}: {{
  error: Error & {{ digest?: string }};
  reset: () => void;
}}) {{
  useEffect(() => {{
    console.error("{pascal}s page error:", error);
  }}, [error]);

  return (
    <div className="container py-6">
      <div className="flex flex-col items-center justify-center min-h-[400px]">
        <h2 className="text-xl font-semibold mb-4">Something went wrong!</h2>
        <p className="text-muted-foreground mb-4">{{error.message}}</p>
        <Button onClick={{reset}}>Try again</Button>
      </div>
    </div>
  );
}}
'''
    
    with open(f"{dir_path}/page.tsx", 'w') as f:
        f.write(template)
    print(f"✓ Created {dir_path}/page.tsx")
    
    with open(f"{dir_path}/loading.tsx", 'w') as f:
        f.write(loading_template)
    print(f"✓ Created {dir_path}/loading.tsx")
    
    with open(f"{dir_path}/error.tsx", 'w') as f:
        f.write(error_template)
    print(f"✓ Created {dir_path}/error.tsx")

def generate_context(name: str, base_path: str = "setting"):
    """Generate context provider with SWR."""
    pascal = to_pascal(name)
    kebab = to_kebab(name)
    camel = to_camel(name)
    
    dir_path = f"app/(pages)/{base_path}/{kebab}/_components/context"
    os.makedirs(dir_path, exist_ok=True)
    
    template = f'''"use client";

import {{ createContext, useContext, useState, useCallback, ReactNode }} from "react";
import useSWR from "swr";
import {{ fetchClient }} from "@/lib/fetch/client";
import type {{ {pascal}, {pascal}sResponse }} from "@/types/{kebab}";

interface {pascal}sContextType {{
  {camel}s: {pascal}[];
  total: number;
  isLoading: boolean;
  error: Error | null;
  selectedIds: string[];
  setSelectedIds: (ids: string[]) => void;
  clearSelection: () => void;
  refresh: () => void;
  mutate{pascal}s: (data?: {pascal}sResponse | ((current?: {pascal}sResponse) => {pascal}sResponse | undefined), revalidate?: boolean) => void;
  page: number;
  setPage: (page: number) => void;
  limit: number;
  setLimit: (limit: number) => void;
  search: string;
  setSearch: (search: string) => void;
}}

const {pascal}sContext = createContext<{pascal}sContextType | null>(null);

const fetcher = (url: string) => fetchClient.get<{pascal}sResponse>(url).then(r => r.data);

interface {pascal}sProviderProps {{
  children: ReactNode;
  initialData: {pascal}sResponse;
}}

export function {pascal}sProvider({{ children, initialData }}: {pascal}sProviderProps) {{
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [page, setPage] = useState(1);
  const [limit, setLimit] = useState(10);
  const [search, setSearch] = useState("");

  const buildQueryString = useCallback(() => {{
    const params = new URLSearchParams({{
      limit: limit.toString(),
      skip: ((page - 1) * limit).toString(),
    }});
    if (search) params.append("search", search);
    return params.toString();
  }}, [page, limit, search]);

  const {{ data, error, isLoading, mutate }} = useSWR(
    `/api/{base_path}/{kebab}?${{buildQueryString()}}`,
    fetcher,
    {{
      fallbackData: initialData,
      revalidateOnFocus: false,
      keepPreviousData: true,
    }}
  );

  const refresh = useCallback(() => mutate(), [mutate]);
  const clearSelection = useCallback(() => setSelectedIds([]), []);

  const handleSearchChange = useCallback((value: string) => {{
    setSearch(value);
    setPage(1);
  }}, []);

  return (
    <{pascal}sContext.Provider
      value={{{{
        {camel}s: data?.items || [],
        total: data?.total || 0,
        isLoading,
        error,
        selectedIds,
        setSelectedIds,
        clearSelection,
        refresh,
        mutate{pascal}s: mutate,
        page,
        setPage,
        limit,
        setLimit,
        search,
        setSearch: handleSearchChange,
      }}}}
    >
      {{children}}
    </{pascal}sContext.Provider>
  );
}}

export function use{pascal}s() {{
  const context = useContext({pascal}sContext);
  if (!context) {{
    throw new Error("use{pascal}s must be used within {pascal}sProvider");
  }}
  return context;
}}
'''
    
    filepath = f"{dir_path}/{kebab}s-context.tsx"
    with open(filepath, 'w') as f:
        f.write(template)
    print(f"✓ Created {filepath}")

def generate_table(name: str, base_path: str = "setting"):
    """Generate table components."""
    pascal = to_pascal(name)
    kebab = to_kebab(name)
    camel = to_camel(name)
    
    dir_path = f"app/(pages)/{base_path}/{kebab}/_components/table"
    os.makedirs(dir_path, exist_ok=True)
    
    # Main table
    table_template = f'''"use client";

import {{ use{pascal}s }} from "../context/{kebab}s-context";
import {{ DataTable }} from "@/components/ui/data-table";
import {{ columns }} from "./columns";
import {{ {pascal}sToolbar }} from "./{kebab}s-toolbar";
import {{ {pascal}sPagination }} from "./{kebab}s-pagination";

export default function {pascal}sTable() {{
  const {{ {camel}s, isLoading, selectedIds, setSelectedIds }} = use{pascal}s();

  return (
    <div className="space-y-4">
      <{pascal}sToolbar />
      <DataTable
        columns={{columns}}
        data={{{camel}s}}
        isLoading={{isLoading}}
        selectedIds={{selectedIds}}
        onSelectionChange={{setSelectedIds}}
      />
      <{pascal}sPagination />
    </div>
  );
}}
'''
    
    # Columns
    columns_template = f'''"use client";

import {{ ColumnDef }} from "@tanstack/react-table";
import {{ Checkbox }} from "@/components/ui/checkbox";
import {{ Badge }} from "@/components/ui/badge";
import {{ {pascal}Actions }} from "./{kebab}-actions";
import type {{ {pascal} }} from "@/types/{kebab}";

export const columns: ColumnDef<{pascal}>[] = [
  {{
    id: "select",
    header: ({{ table }}) => (
      <Checkbox
        checked={{table.getIsAllPageRowsSelected()}}
        onCheckedChange={{(value) => table.toggleAllPageRowsSelected(!!value)}}
      />
    ),
    cell: ({{ row }}) => (
      <Checkbox
        checked={{row.getIsSelected()}}
        onCheckedChange={{(value) => row.toggleSelected(!!value)}}
      />
    ),
    enableSorting: false,
  }},
  {{
    accessorKey: "name",
    header: "Name",
    cell: ({{ row }}) => <div className="font-medium">{{row.getValue("name")}}</div>,
  }},
  {{
    accessorKey: "is_active",
    header: "Status",
    cell: ({{ row }}) => (
      <Badge variant={{row.getValue("is_active") ? "success" : "secondary"}}>
        {{row.getValue("is_active") ? "Active" : "Inactive"}}
      </Badge>
    ),
  }},
  {{
    id: "actions",
    cell: ({{ row }}) => <{pascal}Actions {camel}={{row.original}} />,
  }},
];
'''
    
    # Actions
    actions_template = f'''"use client";

import {{ useState }} from "react";
import {{ MoreHorizontal, Pencil, Trash, Power }} from "lucide-react";
import {{
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
}} from "@/components/ui/dropdown-menu";
import {{ Button }} from "@/components/ui/button";
import {{ use{pascal}s }} from "../context/{kebab}s-context";
import {{ delete{pascal}, toggle{pascal}Status }} from "@/lib/actions/{kebab}.actions";
import {{ toast }} from "sonner";
import type {{ {pascal} }} from "@/types/{kebab}";

interface {pascal}ActionsProps {{
  {camel}: {pascal};
}}

export function {pascal}Actions({{ {camel} }}: {pascal}ActionsProps) {{
  const {{ refresh, mutate{pascal}s }} = use{pascal}s();
  const [isLoading, setIsLoading] = useState(false);

  const handleToggleStatus = async () => {{
    setIsLoading(true);
    
    // Optimistic update
    mutate{pascal}s(
      (current) => current ? {{
        ...current,
        items: current.items.map(item =>
          item.id === {camel}.id ? {{ ...item, is_active: !{camel}.is_active }} : item
        ),
      }} : current,
      false
    );

    const result = await toggle{pascal}Status({camel}.id, !{camel}.is_active);
    setIsLoading(false);

    if (result.success) {{
      toast.success(`${{camel}.is_active ? "Deactivated" : "Activated"}} successfully`);
    }} else {{
      refresh();
      toast.error(result.error);
    }}
  }};

  const handleDelete = async () => {{
    if (!confirm(`Delete ${{{camel}.name}}?`)) return;

    setIsLoading(true);
    const result = await delete{pascal}({camel}.id);
    setIsLoading(false);

    if (result.success) {{
      toast.success("Deleted successfully");
      refresh();
    }} else {{
      toast.error(result.error);
    }}
  }};

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="icon" disabled={{isLoading}}>
          <MoreHorizontal className="h-4 w-4" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuItem>
          <Pencil className="mr-2 h-4 w-4" />
          Edit
        </DropdownMenuItem>
        <DropdownMenuItem onClick={{handleToggleStatus}}>
          <Power className="mr-2 h-4 w-4" />
          {{{camel}.is_active ? "Deactivate" : "Activate"}}
        </DropdownMenuItem>
        <DropdownMenuSeparator />
        <DropdownMenuItem onClick={{handleDelete}} className="text-destructive">
          <Trash className="mr-2 h-4 w-4" />
          Delete
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}}
'''
    
    # Toolbar
    toolbar_template = f'''"use client";

import {{ useState, useEffect }} from "react";
import {{ Search, Plus, Trash }} from "lucide-react";
import {{ Input }} from "@/components/ui/input";
import {{ Button }} from "@/components/ui/button";
import {{ use{pascal}s }} from "../context/{kebab}s-context";

export function {pascal}sToolbar() {{
  const {{ search, setSearch, selectedIds, clearSelection }} = use{pascal}s();
  const [localSearch, setLocalSearch] = useState(search);

  useEffect(() => {{
    const timer = setTimeout(() => {{
      if (localSearch !== search) setSearch(localSearch);
    }}, 300);
    return () => clearTimeout(timer);
  }}, [localSearch, search, setSearch]);

  return (
    <div className="flex items-center justify-between">
      <div className="flex items-center gap-2">
        <div className="relative">
          <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search..."
            value={{localSearch}}
            onChange={{(e) => setLocalSearch(e.target.value)}}
            className="pl-8 w-[250px]"
          />
        </div>
        {{selectedIds.length > 0 && (
          <>
            <span className="text-sm text-muted-foreground">
              {{selectedIds.length}} selected
            </span>
            <Button variant="destructive" size="sm">
              <Trash className="mr-2 h-4 w-4" />
              Delete
            </Button>
            <Button variant="ghost" size="sm" onClick={{clearSelection}}>
              Clear
            </Button>
          </>
        )}}
      </div>
      <Button>
        <Plus className="mr-2 h-4 w-4" />
        Add New
      </Button>
    </div>
  );
}}
'''
    
    # Pagination
    pagination_template = f'''"use client";

import {{ ChevronLeft, ChevronRight }} from "lucide-react";
import {{ Button }} from "@/components/ui/button";
import {{
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
}} from "@/components/ui/select";
import {{ use{pascal}s }} from "../context/{kebab}s-context";

export function {pascal}sPagination() {{
  const {{ page, setPage, limit, setLimit, total }} = use{pascal}s();
  const totalPages = Math.ceil(total / limit);

  return (
    <div className="flex items-center justify-between">
      <div className="text-sm text-muted-foreground">
        Showing {{((page - 1) * limit) + 1}} to {{Math.min(page * limit, total)}} of {{total}}
      </div>
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          <span className="text-sm">Rows</span>
          <Select
            value={{limit.toString()}}
            onValueChange={{(v) => {{ setLimit(Number(v)); setPage(1); }}}}
          >
            <SelectTrigger className="w-[70px]">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {{[10, 20, 50, 100].map((n) => (
                <SelectItem key={{n}} value={{n.toString()}}>{{n}}</SelectItem>
              ))}}
            </SelectContent>
          </Select>
        </div>
        <div className="flex items-center gap-1">
          <Button variant="outline" size="icon" onClick={{() => setPage(page - 1)}} disabled={{page <= 1}}>
            <ChevronLeft className="h-4 w-4" />
          </Button>
          <span className="px-2 text-sm">{{page}} / {{totalPages}}</span>
          <Button variant="outline" size="icon" onClick={{() => setPage(page + 1)}} disabled={{page >= totalPages}}>
            <ChevronRight className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  );
}}
'''
    
    files = [
        (f"{dir_path}/{kebab}s-table.tsx", table_template),
        (f"{dir_path}/columns.tsx", columns_template),
        (f"{dir_path}/{kebab}-actions.tsx", actions_template),
        (f"{dir_path}/{kebab}s-toolbar.tsx", toolbar_template),
        (f"{dir_path}/{kebab}s-pagination.tsx", pagination_template),
    ]
    
    for filepath, content in files:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"✓ Created {filepath}")

def generate_actions(name: str, base_path: str = "setting"):
    """Generate server actions."""
    pascal = to_pascal(name)
    kebab = to_kebab(name)
    
    os.makedirs('lib/actions', exist_ok=True)
    
    template = f'''"use server";

import {{ serverGet, serverPost, serverPut, serverDelete }} from "@/lib/fetch/server";
import {{ revalidatePath }} from "next/cache";
import type {{ {pascal}, {pascal}Create, {pascal}sResponse }} from "@/types/{kebab}";

export async function get{pascal}s(
  limit: number = 10,
  skip: number = 0,
  filters?: Record<string, string | boolean | undefined>
): Promise<{pascal}sResponse> {{
  const params = new URLSearchParams({{
    limit: limit.toString(),
    skip: skip.toString(),
  }});
  
  if (filters) {{
    Object.entries(filters).forEach(([key, value]) => {{
      if (value !== undefined) params.append(key, String(value));
    }});
  }}
  
  return serverGet<{pascal}sResponse>(`/api/{base_path}/{kebab}?${{params.toString()}}`);
}}

export async function get{pascal}(id: string): Promise<{pascal}> {{
  return serverGet<{pascal}>(`/api/{base_path}/{kebab}/${{id}}`);
}}

export async function create{pascal}(
  data: {pascal}Create
): Promise<{{ success: boolean; data?: {pascal}; error?: string }}> {{
  try {{
    const result = await serverPost<{pascal}>("/api/{base_path}/{kebab}", data);
    revalidatePath("/{base_path}/{kebab}");
    return {{ success: true, data: result }};
  }} catch (error) {{
    return {{ success: false, error: error instanceof Error ? error.message : "Failed to create" }};
  }}
}}

export async function update{pascal}(
  id: string,
  data: Partial<{pascal}>
): Promise<{{ success: boolean; error?: string }}> {{
  try {{
    await serverPut(`/api/{base_path}/{kebab}/${{id}}`, data);
    revalidatePath("/{base_path}/{kebab}");
    return {{ success: true }};
  }} catch (error) {{
    return {{ success: false, error: error instanceof Error ? error.message : "Failed to update" }};
  }}
}}

export async function delete{pascal}(
  id: string
): Promise<{{ success: boolean; error?: string }}> {{
  try {{
    await serverDelete(`/api/{base_path}/{kebab}/${{id}}`);
    revalidatePath("/{base_path}/{kebab}");
    return {{ success: true }};
  }} catch (error) {{
    return {{ success: false, error: error instanceof Error ? error.message : "Failed to delete" }};
  }}
}}

export async function toggle{pascal}Status(
  id: string,
  isActive: boolean
): Promise<{{ success: boolean; error?: string }}> {{
  try {{
    await serverPut(`/api/{base_path}/{kebab}/${{id}}/status`, {{ is_active: isActive }});
    revalidatePath("/{base_path}/{kebab}");
    return {{ success: true }};
  }} catch (error) {{
    return {{ success: false, error: error instanceof Error ? error.message : "Failed to update status" }};
  }}
}}
'''
    
    filepath = f"lib/actions/{kebab}.actions.ts"
    with open(filepath, 'w') as f:
        f.write(template)
    print(f"✓ Created {filepath}")

def generate_all(name: str, base_path: str = "setting"):
    """Generate complete data table page."""
    print(f"Generating data table page for: {name}")
    generate_page(name, base_path)
    generate_context(name, base_path)
    generate_table(name, base_path)
    generate_actions(name, base_path)
    
    kebab = to_kebab(name)
    print(f"\n✓ All components generated!")
    print(f"\nNext steps:")
    print(f"  1. Create types in types/{kebab}.ts")
    print(f"  2. Create API routes in app/api/{base_path}/{kebab}/")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    base_path = "setting"
    
    if command == 'validate':
        print("Validation not yet implemented")
    elif command in ['generate', 'page', 'context', 'table', 'actions']:
        if len(sys.argv) < 3:
            print(f"Usage: python helper.py {command} NAME [BASE_PATH]")
            sys.exit(1)
        
        name = sys.argv[2]
        if len(sys.argv) > 3:
            base_path = sys.argv[3]
        
        if command == 'generate':
            generate_all(name, base_path)
        elif command == 'page':
            generate_page(name, base_path)
        elif command == 'context':
            generate_context(name, base_path)
        elif command == 'table':
            generate_table(name, base_path)
        elif command == 'actions':
            generate_actions(name, base_path)
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)

if __name__ == '__main__':
    main()
