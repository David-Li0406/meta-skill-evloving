# Pagination (AIP-158)

## Linter Rules

The following rules automatically check pagination:

| Rule ID                      | Severity   | What It Checks                                                                   |
| ---------------------------- | ---------- | -------------------------------------------------------------------------------- |
| `aip158/list-paginated`      | warning    | Collection endpoints (GET `/resources`) have `page_size` and `page_token` params |
| `aip158/max-page-size`       | suggestion | `page_size`/`limit` param has `maximum` constraint in schema                     |
| `aip158/response-next-token` | warning    | 200 response schema includes `next_page_token` field                             |

To skip a rule: `aip-review spec.yaml --skip-rules aip158/max-page-size`

## Request Parameters

| Parameter    | Type    | Required | Description                                |
| ------------ | ------- | -------- | ------------------------------------------ |
| `page_size`  | integer | No       | Max items per page (default: 20, max: 100) |
| `page_token` | string  | No       | Opaque cursor from previous response       |

## Response Schema

```json
{
  "data": [
    { "id": "order_1", "status": "shipped" },
    { "id": "order_2", "status": "pending" }
  ],
  "next_page_token": "eyJsYXN0X2lkIjoib3JkZXJfMiJ9",
  "total_size": 142
}
```

## OpenAPI Definition

```yaml
paths:
  /orders:
    get:
      parameters:
        - name: page_size
          in: query
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
        - name: page_token
          in: query
          schema:
            type: string
      responses:
        '200':
          content:
            application/json:
              schema:
                type: object
                required: [data]
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Order'
                  next_page_token:
                    type: string
                    description: Token for next page, absent on last page
                  total_size:
                    type: integer
                    description: Total items (optional, may be expensive)
```

## Cursor vs Offset Pagination

### Cursor-based (Recommended)

**Pros:**

- Stable under concurrent writes
- Efficient for large datasets
- No skipped/duplicate items

**Implementation:**

```typescript
// Encode cursor
const cursor = Buffer.from(
  JSON.stringify({
    last_id: items[items.length - 1].id,
    last_created: items[items.length - 1].created_at,
  })
).toString('base64');

// Decode and query
const decoded = JSON.parse(Buffer.from(page_token, 'base64').toString());
const items = await db.query(
  `
  SELECT * FROM orders 
  WHERE (created_at, id) > ($1, $2)
  ORDER BY created_at, id
  LIMIT $3
`,
  [decoded.last_created, decoded.last_id, page_size]
);
```

### Offset-based (Use sparingly)

**When acceptable:**

- Small, static datasets
- Admin UIs where "jump to page N" is needed
- Data rarely changes

**Avoid when:**

- Dataset > 10k items
- Frequent inserts/deletes
- Real-time data

## Total Count Considerations

Including `total_size` requires a COUNT query which can be expensive.

**Options:**

1. **Always include** - Simple, but may slow down large collections
2. **Request with parameter** - `GET /orders?include_total=true`
3. **Approximate count** - Use `pg_class.reltuples` or similar
4. **Never include** - Clients use "has more" signal from `next_page_token`

```yaml
# Option 2: Explicit request
parameters:
  - name: include_total
    in: query
    schema:
      type: boolean
      default: false
```

## Page Size Limits

```typescript
const DEFAULT_PAGE_SIZE = 20;
const MAX_PAGE_SIZE = 100;

function normalizePageSize(requested?: number): number {
  if (!requested) return DEFAULT_PAGE_SIZE;
  return Math.min(Math.max(1, requested), MAX_PAGE_SIZE);
}
```

## Empty Pages

When no items match:

```json
{
  "data": [],
  "next_page_token": null
}
```

**Do not** return 404 for empty collections.

## Nested Resource Pagination

For paginated sub-resources:

```
GET /users/123/orders?page_size=10&page_token=xxx
```

The token is scoped to the parent resource - don't reuse tokens across different parents.

## NestJS Implementation

```typescript
// pagination.dto.ts
export class PaginationParams {
  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(1)
  @Max(100)
  page_size?: number = 20;

  @IsOptional()
  @IsString()
  page_token?: string;
}

// paginated-response.dto.ts
export class PaginatedResponse<T> {
  data: T[];
  next_page_token?: string;
  total_size?: number;
}

// orders.controller.ts
@Get()
async listOrders(
  @Query() pagination: PaginationParams,
): Promise<PaginatedResponse<Order>> {
  return this.ordersService.list(pagination);
}
```

## Fastify Implementation

```typescript
const paginationSchema = {
  querystring: {
    type: 'object',
    properties: {
      page_size: { type: 'integer', minimum: 1, maximum: 100, default: 20 },
      page_token: { type: 'string' },
    },
  },
};

fastify.get('/orders', { schema: paginationSchema }, async (request) => {
  const { page_size, page_token } = request.query;
  return ordersService.list({ page_size, page_token });
});
```

## Common Mistakes

❌ **Exposing raw database offset**

```json
{ "limit": 20, "offset": 500 }
```

✅ **Opaque cursor** - Clients can't manipulate, server can change implementation

❌ **Different pagination styles per endpoint**

✅ **Consistent pagination across all list endpoints**

❌ **Requiring page_token on first request**

✅ **page_token is optional, absence means "start from beginning"**
