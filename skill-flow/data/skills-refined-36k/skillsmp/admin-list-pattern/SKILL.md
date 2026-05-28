---
name: admin-list-pattern
description: Provides full-stack patterns for implementing searchable, paginated lists in the Erify Admin section. This skill should be used when adding or updating admin tables that require server-side filtering and debounced search.
---

# Admin List Integration Pattern

This skill outlines the standard pattern for implementing searchable, paginated lists in the `erify_studios` (frontend) and `erify_api` (backend) applications.

## Integration Overview

The pattern relies on synchronized parameter names and behaviors across the stack:
1.  **Frontend**: Uses `useTableUrlState` to sync URL params (e.g., `?name=...`) with the table's `columnFilters`.
2.  **API Boundary**: A specialized `List<Resource>QueryDto` extends the base pagination schema.
3.  **Service**: Dynamically builds a Prisma `where` clause to handle partial matches and other filters.

---

## Backend Pattern (`erify_api`)

### 1. Define the Query DTO (`schemas.ts`)

Nest the filters inside a Zod schema and extend the base pagination. Following the pattern in `models/client/schemas/client.schema.ts`:

```typescript
export const listResourceFilterSchema = z.object({
  name: z.string().optional(),
  include_deleted: z.coerce.boolean().default(false),
});

export const listResourceQuerySchema = z
  .object({
    page: z.coerce.number().int().min(1).optional().default(1),
    limit: z.coerce.number().int().min(1).optional().default(10),
  })
  .and(listResourceFilterSchema)
  .transform((data) => ({
    ...data,
    take: data.limit,
    skip: (data.page - 1) * data.limit,
  }));

export class ListResourceQueryDto extends createZodDto(listResourceQuerySchema) {}
```

### 2. Service Logic (`service.ts`)

Build the `where` clause in the service. Ensure case-insensitive partial matching for strings.

```typescript
async getResources(query: {
  skip?: number;
  take?: number;
  name?: string;
  include_deleted?: boolean;
}): Promise<Resource[]> {
  const where: Prisma.ResourceWhereInput = {};

  if (!query.include_deleted) {
    where.deletedAt = null;
  }

  if (query.name) {
    where.name = {
      contains: query.name,
      mode: 'insensitive',
    };
  }

  return this.repository.findMany({ skip: query.skip, take: query.take, where });
}
```

### 3. Controller Integration (`controller.ts`)

Pass the query DTO to the service and use `@AdminPaginatedResponse`.

```typescript
@Get()
@AdminPaginatedResponse(ResourceDto, 'List resources')
async getResources(@Query() query: ListResourceQueryDto) {
  const data = await this.service.getResources(query);
  const total = await this.service.countResources({
    name: query.name ? { contains: query.name, mode: 'insensitive' } : undefined,
    deletedAt: query.include_deleted ? undefined : null,
  });
  return this.createPaginatedResponse(data, total, query);
}
```

---

## Frontend Pattern (`erify_studios`)

### 1. Route Search Schema

Ensure the `Route` search schema includes the filter field.

```typescript
const searchSchema = z.object({
  page: z.number().int().min(1).catch(1),
  pageSize: z.number().int().min(10).max(100).catch(10),
  name: z.string().optional().catch(undefined),
});
```

### 2. AdminTable Configuration

Pass `searchColumn` and `onColumnFiltersChange` to the `AdminTable`.

```typescript
const { 
  pagination, 
  onPaginationChange, 
  columnFilters, 
  onColumnFiltersChange 
} = useTableUrlState({ from: '/system/resources/' });

const nameFilter = columnFilters.find(f => f.id === 'name')?.value as string;

const { data, isLoading } = useAdminList<Resource>('resources', {
  page: pagination.pageIndex + 1,
  limit: pagination.pageSize,
  name: nameFilter,
});

// ... inside render
<AdminTable
  // ...
  searchColumn="name"
  columnFilters={columnFilters}
  onColumnFiltersChange={onColumnFiltersChange}
/>
```

### 3. Toolbar UX (Debouncing)

The `AdminTableToolbar` (generic component) should handle internal debouncing of the input to avoid immediate server queries on every keystroke.

- **Timeout**: Use a 500ms debounce.
- **Visibility**: Only show the search input when `searchColumn` is provided.

---

## Checklist

- [ ] Backend: `QueryDto` extends pagination and includes filters.
- [ ] Backend: Service builds `where` clause with `contains` and `insensitive`.
- [ ] Frontend: `useTableUrlState` used for URL synchronization.
- [ ] Frontend: `searchColumn` passed to `AdminTable`.
- [ ] Frontend: Verification of debounced input behavior.
