# Field Masks & Partial Updates (AIP-134)

## Linter Rules

| Rule ID                 | Severity   | What It Checks                                         |
| ----------------------- | ---------- | ------------------------------------------------------ |
| `aip134/patch-over-put` | suggestion | Resources with PUT also have PATCH for partial updates |

**Note:** The linter checks for PATCH availability but does not currently validate field mask implementation details. The content below is best-practice guidance.

To skip: `aip-review spec.yaml --skip-rules aip134/patch-over-put`

## The Problem

How does the server know if a field was:

- Intentionally set to `null`
- Omitted (don't change)

```json
// Did the client mean to clear description, or just not include it?
{
  "title": "Updated Title"
}
```

## Solution: Field Masks

Explicitly list which fields to update:

```
PATCH /orders/123
Content-Type: application/json

{
  "order": {
    "title": "Updated Title",
    "description": null
  },
  "update_mask": "title,description"
}
```

Now the server knows:

- `title` → set to "Updated Title"
- `description` → set to null (cleared)
- `status`, `customer_id`, etc. → unchanged

## OpenAPI Definition

```yaml
paths:
  /orders/{order_id}:
    patch:
      summary: Update an order
      parameters:
        - name: order_id
          in: path
          required: true
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              type: object
              required: [order]
              properties:
                order:
                  $ref: '#/components/schemas/Order'
                update_mask:
                  type: string
                  description: |
                    Comma-separated list of fields to update.
                    If omitted, all provided fields are updated.
                  example: 'title,description,shipping_address.city'
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Order'
```

## Nested Fields

Use dot notation for nested objects:

```json
{
  "order": {
    "shipping_address": {
      "city": "New York"
    }
  },
  "update_mask": "shipping_address.city"
}
```

Only `shipping_address.city` is updated; other address fields remain.

## Wildcard for Nested Objects

To replace entire nested object:

```json
{
  "order": {
    "shipping_address": {
      "city": "New York",
      "postal_code": "10001",
      "street": "123 Main St"
    }
  },
  "update_mask": "shipping_address"
}
```

## Implementation

```typescript
// update-mask.service.ts
export class UpdateMaskService {
  applyMask<T extends object>(
    existing: T,
    updates: Partial<T>,
    mask: string | undefined
  ): T {
    if (!mask) {
      // No mask - merge all provided fields
      return this.deepMerge(existing, updates);
    }

    const fields = mask.split(',').map((f) => f.trim());
    const result = { ...existing };

    for (const field of fields) {
      this.setNestedValue(result, field, this.getNestedValue(updates, field));
    }

    return result;
  }

  private setNestedValue(obj: any, path: string, value: any): void {
    const parts = path.split('.');
    let current = obj;

    for (let i = 0; i < parts.length - 1; i++) {
      if (!(parts[i] in current)) {
        current[parts[i]] = {};
      }
      current = current[parts[i]];
    }

    current[parts[parts.length - 1]] = value;
  }

  private getNestedValue(obj: any, path: string): any {
    return path.split('.').reduce((o, k) => o?.[k], obj);
  }
}
```

## Validation

Validate that mask fields are:

1. Actually updatable (not read-only like `id`, `created_at`)
2. Present in the request body

```typescript
const READ_ONLY_FIELDS = new Set(['id', 'created_at', 'updated_at']);
const UPDATABLE_FIELDS = new Set([
  'title',
  'description',
  'status',
  'shipping_address',
]);

function validateUpdateMask(mask: string, body: object): void {
  const fields = mask.split(',').map((f) => f.trim());

  for (const field of fields) {
    const rootField = field.split('.')[0];

    if (READ_ONLY_FIELDS.has(rootField)) {
      throw new InvalidArgumentError(`Field '${rootField}' is read-only`);
    }

    if (!UPDATABLE_FIELDS.has(rootField)) {
      throw new InvalidArgumentError(`Unknown field: '${rootField}'`);
    }

    // Optionally: verify field is present in body
    if (!hasNestedValue(body, field)) {
      throw new InvalidArgumentError(
        `Field '${field}' in update_mask but not in request body`
      );
    }
  }
}
```

## Alternative: JSON Merge Patch (RFC 7396)

Simpler but less explicit:

```
PATCH /orders/123
Content-Type: application/merge-patch+json

{
  "title": "Updated Title",
  "description": null
}
```

Rules:

- Present field with value → set
- Present field with `null` → delete
- Absent field → unchanged

**Limitation:** Can't distinguish "set to null" vs "remove field" for fields where `null` is valid.

## Alternative: JSON Patch (RFC 6902)

Most explicit, but verbose:

```
PATCH /orders/123
Content-Type: application/json-patch+json

[
  { "op": "replace", "path": "/title", "value": "Updated Title" },
  { "op": "remove", "path": "/description" }
]
```

## Comparison

| Approach      | Explicitness | Simplicity | Use When                              |
| ------------- | ------------ | ---------- | ------------------------------------- |
| Field Mask    | High         | Medium     | Complex objects, null is meaningful   |
| Merge Patch   | Medium       | High       | Simple objects, null means "clear"    |
| JSON Patch    | Highest      | Low        | Need atomic operations (test-and-set) |
| PUT (replace) | N/A          | High       | Small objects, always send complete   |

## NestJS Implementation

```typescript
// update-order.dto.ts
export class UpdateOrderDto {
  @ValidateNested()
  @Type(() => OrderDto)
  order: Partial<OrderDto>;

  @IsOptional()
  @IsString()
  update_mask?: string;
}

// orders.controller.ts
@Patch(':id')
async updateOrder(
  @Param('id') id: string,
  @Body() dto: UpdateOrderDto,
): Promise<Order> {
  if (dto.update_mask) {
    this.validateUpdateMask(dto.update_mask, dto.order);
  }

  const existing = await this.ordersService.findOne(id);
  const updated = this.updateMaskService.applyMask(
    existing,
    dto.order,
    dto.update_mask,
  );

  return this.ordersService.save(updated);
}
```

## Common Mistakes

❌ **PATCH without clarity on null handling**

✅ **Document whether null means "clear" or "unchanged"**

❌ **Allowing update of computed/read-only fields**

✅ **Validate mask against allowed fields**

❌ **Ignoring mask and updating everything**

✅ **Respect mask - only update listed fields**

❌ **PUT for partial updates**

✅ **Use PATCH** - PUT means "replace entire resource"
