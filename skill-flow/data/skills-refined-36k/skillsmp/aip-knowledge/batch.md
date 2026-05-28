# Batch Operations (AIP-231, AIP-234, AIP-235)

## Linter Rules

**No automated rules yet.** Batch operation patterns are checked manually. The content below is best-practice guidance from AIP-231+.

Future rules planned:

- Batch size limits validation
- Batch endpoint naming conventions
- Partial failure response format

## When to Batch

Use batch operations when clients need to:

- Create/update/delete multiple resources atomically
- Process lists of items more efficiently than N individual requests
- Reduce network round-trips

## Batch Create

```yaml
paths:
  /orders:batchCreate:
    post:
      summary: Create multiple orders
      requestBody:
        content:
          application/json:
            schema:
              type: object
              required: [requests]
              properties:
                requests:
                  type: array
                  maxItems: 100
                  items:
                    $ref: '#/components/schemas/CreateOrderRequest'
      responses:
        '200':
          content:
            application/json:
              schema:
                type: object
                properties:
                  orders:
                    type: array
                    items:
                      $ref: '#/components/schemas/Order'
```

## Batch Get

```yaml
paths:
  /orders:batchGet:
    get:
      summary: Get multiple orders by ID
      parameters:
        - name: ids
          in: query
          required: true
          schema:
            type: array
            items:
              type: string
            maxItems: 100
          style: form
          explode: false
      responses:
        '200':
          content:
            application/json:
              schema:
                type: object
                properties:
                  orders:
                    type: array
                    items:
                      $ref: '#/components/schemas/Order'
```

**Note:** Order of response matches order of request IDs. Missing items return null in position.

## Batch Update

```yaml
paths:
  /orders:batchUpdate:
    post:
      summary: Update multiple orders
      requestBody:
        content:
          application/json:
            schema:
              type: object
              required: [requests]
              properties:
                requests:
                  type: array
                  maxItems: 100
                  items:
                    type: object
                    properties:
                      order:
                        $ref: '#/components/schemas/Order'
                      update_mask:
                        type: string
                        description: Fields to update
```

## Batch Delete

```yaml
paths:
  /orders:batchDelete:
    post:
      summary: Delete multiple orders
      requestBody:
        content:
          application/json:
            schema:
              type: object
              required: [ids]
              properties:
                ids:
                  type: array
                  maxItems: 100
                  items:
                    type: string
                force:
                  type: boolean
                  default: false
                  description: Skip deletion checks
```

## Partial Failure Handling

When some items succeed and others fail:

### Option 1: All-or-Nothing (Transactional)

Return error if any item fails:

```json
{
  "error": {
    "code": "INVALID_ARGUMENT",
    "details": [
      {
        "error": {
          "code": "NOT_FOUND",
          "message": "Order ord_xyz not found"
        },
        "index": 2,
        "type": "batch_failure"
      }
    ],
    "message": "Batch operation failed"
  }
}
```

### Option 2: Partial Success

Return results with per-item status:

```json
{
  "results": [
    {
      "index": 0,
      "status": "SUCCESS",
      "order": { "id": "ord_123", ... }
    },
    {
      "index": 1,
      "status": "SUCCESS",
      "order": { "id": "ord_456", ... }
    },
    {
      "index": 2,
      "status": "FAILED",
      "error": {
        "code": "INVALID_ARGUMENT",
        "message": "Invalid quantity"
      }
    }
  ],
  "success_count": 2,
  "failure_count": 1
}
```

**HTTP Status for Partial Success:**

- `200` if all succeed
- `207 Multi-Status` if partial (WebDAV status, widely understood)
- `400` or `422` if you want to force client to handle errors

## Implementation

```typescript
@Post('batchCreate')
async batchCreateOrders(
  @Body() request: BatchCreateOrdersRequest,
): Promise<BatchCreateOrdersResponse> {
  const results = await Promise.allSettled(
    request.requests.map((req, index) =>
      this.ordersService.create(req).then(order => ({ index, order }))
    )
  );

  const successes = results
    .filter((r): r is PromiseFulfilledResult<any> => r.status === 'fulfilled')
    .map(r => r.value);

  const failures = results
    .filter((r): r is PromiseRejectedResult => r.status === 'rejected')
    .map((r, i) => ({ index: i, error: mapError(r.reason) }));

  return {
    orders: successes.map(s => s.order),
    errors: failures,
    success_count: successes.length,
    failure_count: failures.length,
  };
}
```

## Limits

Always enforce batch size limits:

```typescript
const MAX_BATCH_SIZE = 100;

@Post('batchCreate')
async batchCreateOrders(@Body() request: BatchCreateOrdersRequest) {
  if (request.requests.length > MAX_BATCH_SIZE) {
    throw new BadRequestException(
      `Batch size ${request.requests.length} exceeds maximum ${MAX_BATCH_SIZE}`
    );
  }
  // ...
}
```

Document limits in OpenAPI:

```yaml
maxItems: 100
```

## Async Batch Operations

For large batches (>100 items or slow processing):

```
POST /orders:batchCreate
→ 202 Accepted
{
  "operation": {
    "name": "operations/op_batch123",
    "done": false,
    "metadata": {
      "type": "BatchCreateOrdersMetadata",
      "total_count": 500,
      "processed_count": 0
    }
  }
}
```

See `references/lro.md` for polling pattern.

## Common Mistakes

❌ **No batch size limit**

✅ **Enforce and document limits** (typically 100-1000)

❌ **Silent partial failures**

✅ **Explicit per-item status or all-or-nothing**

❌ **Different error format for batch vs single**

✅ **Consistent error schema** across all operations

❌ **Batch endpoints that are just loops**

✅ **Optimize batch operations** (bulk insert, parallel processing)
