# Filtering & Ordering (AIP-160, AIP-132)

## Linter Rules

The following rules automatically check filtering and ordering:

| Rule ID                | Severity   | What It Checks                                                     |
| ---------------------- | ---------- | ------------------------------------------------------------------ |
| `aip132/has-filtering` | suggestion | List endpoints have filter/search params or field-specific filters |
| `aip132/has-ordering`  | suggestion | List endpoints have `order_by`/`sort` query parameter              |

To skip a rule: `aip-review spec.yaml --skip-rules aip132/has-filtering`

## Filtering

### Simple Filters (Field-based)

For straightforward cases, use query parameters:

```
GET /orders?status=pending&customer_id=cust_123
```

### Rich Filtering (Filter Expression)

For complex queries, use a `filter` parameter with expression syntax:

```
GET /orders?filter=status="pending" AND total > 100
GET /orders?filter=created_at >= "2024-01-01" AND tags:"urgent"
```

### Filter Expression Syntax

```
filter     = expression
expression = term { ("AND" | "OR") term }
term       = field operator value | "(" expression ")" | "NOT" term
field      = identifier { "." identifier }
operator   = "=" | "!=" | "<" | "<=" | ">" | ">=" | ":" | "~"
value      = string | number | boolean | "null"

# Operators
=     exact match
!=    not equal
<     less than
<=    less than or equal
>     greater than
>=    greater than or equal
:     contains / has (for arrays, maps, text search)
~     regex match (use sparingly)
```

### Examples

```
# Exact match
status = "shipped"

# Comparison
total >= 100
created_at > "2024-01-01T00:00:00Z"

# Contains (arrays)
tags : "urgent"

# Text search (if supported)
title : "quarterly report"

# Negation
NOT status = "cancelled"

# Complex
(status = "pending" OR status = "processing") AND customer.tier = "premium"
```

### OpenAPI Definition

```yaml
parameters:
  - name: filter
    in: query
    description: |
      Filter expression. Supported fields: status, customer_id, created_at, total.
      Example: `status="pending" AND total > 100`
    schema:
      type: string
    examples:
      simple:
        value: 'status="pending"'
      complex:
        value: 'status="pending" AND created_at >= "2024-01-01"'
```

### Server-Side Implementation

```typescript
// filter-parser.ts
interface FilterNode {
  type: 'comparison' | 'logical' | 'not';
  // ... AST nodes
}

function parseFilter(filter: string): FilterNode {
  // Parse into AST, then convert to SQL/query
}

function filterToSQL(node: FilterNode, allowedFields: Set<string>): SQLClause {
  // Validate fields against allowlist
  // Convert to parameterized SQL
}
```

### Security Considerations

1. **Allowlist fields** - Only permit filtering on indexed, non-sensitive fields
2. **Parameterized queries** - Never interpolate filter values into SQL
3. **Limit complexity** - Cap expression depth, number of terms
4. **Rate limit** - Complex filters are expensive; rate limit aggressively

```typescript
const ALLOWED_FILTER_FIELDS = new Set([
  'status',
  'customer_id',
  'created_at',
  'total',
]);
const MAX_FILTER_DEPTH = 3;
const MAX_FILTER_TERMS = 10;
```

---

## Ordering (AIP-132)

### Request Parameter

```
GET /orders?order_by=created_at desc, id asc
GET /orders?order_by=total desc
```

### Syntax

```
order_by = field_order { "," field_order }
field_order = field [ " " direction ]
direction = "asc" | "desc"
```

Default direction is ascending.

### OpenAPI Definition

```yaml
parameters:
  - name: order_by
    in: query
    description: |
      Comma-separated list of fields to sort by. 
      Add `desc` suffix for descending order.
      Sortable fields: created_at, updated_at, total, status.
    schema:
      type: string
      default: created_at desc
    examples:
      newest:
        value: created_at desc
      multiple:
        value: status asc, created_at desc
```

### Implementation

```typescript
const SORTABLE_FIELDS = new Map([
  ['created_at', 'orders.created_at'],
  ['updated_at', 'orders.updated_at'],
  ['total', 'orders.total_amount'],
  ['status', 'orders.status'],
]);

function parseOrderBy(orderBy: string): OrderClause[] {
  return orderBy.split(',').map((part) => {
    const [field, direction = 'asc'] = part.trim().split(/\s+/);

    const column = SORTABLE_FIELDS.get(field);
    if (!column) {
      throw new InvalidArgumentError(`Cannot sort by field: ${field}`);
    }

    return { column, direction: direction.toLowerCase() as 'asc' | 'desc' };
  });
}
```

---

## Combining Filter, Order, and Pagination

Full list request:

```
GET /orders?filter=status="pending"&order_by=created_at desc&page_size=20&page_token=xxx
```

### Execution Order

1. Apply filters (WHERE)
2. Apply ordering (ORDER BY)
3. Apply pagination (LIMIT/cursor)

### Stable Ordering for Pagination

Always include a unique field in `order_by` to ensure stable pagination:

```typescript
function ensureStableOrder(orderBy: OrderClause[]): OrderClause[] {
  const hasUniqueField = orderBy.some((o) => o.column === 'id');
  if (!hasUniqueField) {
    return [...orderBy, { column: 'id', direction: 'asc' }];
  }
  return orderBy;
}
```

---

## Alternative: Simple Field Filters

For APIs that don't need complex filtering, use individual query params:

```yaml
parameters:
  - name: status
    in: query
    schema:
      type: string
      enum: [pending, processing, shipped, delivered, cancelled]
  - name: customer_id
    in: query
    schema:
      type: string
  - name: created_after
    in: query
    schema:
      type: string
      format: date-time
  - name: created_before
    in: query
    schema:
      type: string
      format: date-time
  - name: min_total
    in: query
    schema:
      type: number
  - name: max_total
    in: query
    schema:
      type: number
```

This is simpler to implement and document, but less flexible.

---

## Common Mistakes

❌ **SQL in query params**

```
GET /orders?where=status='pending'
```

✅ **Safe expression syntax** - Parse and validate, never execute directly

❌ **Allowing sort on non-indexed fields**

✅ **Allowlist sortable fields** - Only indexed columns

❌ **No default ordering**

✅ **Consistent default** - Usually `created_at desc` for recent-first

❌ **Filter without pagination**

✅ **Always paginate filtered results** - Filters can return huge sets
