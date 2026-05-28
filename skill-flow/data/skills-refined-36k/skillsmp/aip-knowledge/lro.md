# Long-Running Operations & Jobs (AIP-151, AIP-155)

## Linter Rules

**No automated rules yet.** Long-running operation patterns are checked manually. The content below is best-practice guidance from AIP-151/155.

Future rules planned:

- Operation resource schema validation
- Polling endpoint existence
- 202 Accepted for async operations

## When to Use

| Pattern         | Use When                                      |
| --------------- | --------------------------------------------- |
| Synchronous     | Operation < 1s, always succeeds/fails quickly |
| LRO (Operation) | 1s - 30min, client polls for result           |
| Job Resource    | Long-lived, repeatable, may have schedule     |
| Webhook/Async   | Fire-and-forget, notify on completion         |

## Long-Running Operations (LRO)

### Flow

```
1. Client: POST /resources:import
2. Server: 202 Accepted + Operation resource
3. Client: GET /operations/{id} (poll)
4. Server: { "done": false, "metadata": {...} }
5. ...repeat polling...
6. Server: { "done": true, "response": {...} } or { "done": true, "error": {...} }
```

### Operation Resource Schema

```yaml
components:
  schemas:
    Operation:
      type: object
      required: [name, done]
      properties:
        name:
          type: string
          description: 'Unique operation ID (e.g., operations/op_abc123)'
        done:
          type: boolean
          description: 'Whether operation has completed'
        metadata:
          type: object
          description: 'Operation-specific progress info'
          properties:
            type:
              type: string
              description: 'Operation type (e.g., ImportOrdersMetadata)'
            progress_percent:
              type: integer
              minimum: 0
              maximum: 100
            items_processed:
              type: integer
            items_total:
              type: integer
        result:
          oneOf:
            - $ref: '#/components/schemas/OperationResponse'
            - $ref: '#/components/schemas/Error'
          description: 'Present only when done=true'
```

### Initiating an LRO

```yaml
paths:
  /orders:import:
    post:
      summary: Import orders from external source
      operationId: importOrders
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ImportOrdersRequest'
      responses:
        '202':
          description: Import started
          headers:
            Location:
              schema:
                type: string
              description: URL to poll for operation status
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Operation'
```

### Polling Endpoint

```yaml
paths:
  /operations/{operation_id}:
    get:
      summary: Get operation status
      parameters:
        - name: operation_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Operation'
```

### Implementation

```typescript
// operations.service.ts
@Injectable()
export class OperationsService {
  async create(type: string, metadata: object): Promise<Operation> {
    const operation = await this.operationsRepo.create({
      id: `op_${nanoid()}`,
      type,
      done: false,
      metadata,
      created_at: new Date(),
    });
    return operation;
  }

  async complete(id: string, result: object): Promise<void> {
    await this.operationsRepo.update(id, {
      done: true,
      result: { response: result },
      completed_at: new Date(),
    });
  }

  async fail(id: string, error: ApiError): Promise<void> {
    await this.operationsRepo.update(id, {
      done: true,
      result: { error },
      completed_at: new Date(),
    });
  }
}

// orders.controller.ts
@Post('import')
@HttpCode(202)
async importOrders(
  @Body() request: ImportOrdersRequest,
  @Res() response: Response,
): Promise<Operation> {
  const operation = await this.operationsService.create(
    'ImportOrders',
    { source: request.source, items_total: request.items?.length },
  );

  // Queue background work
  await this.importQueue.add('import-orders', {
    operation_id: operation.id,
    request,
  });

  response.setHeader('Location', `/operations/${operation.id}`);
  return operation;
}
```

### Polling Guidance

Include retry guidance in response:

```typescript
@Get(':id')
async getOperation(
  @Param('id') id: string,
  @Res() response: Response,
): Promise<Operation> {
  const operation = await this.operationsService.findOne(id);

  if (!operation.done) {
    // Suggest poll interval based on operation type
    const retryAfter = this.getRetryInterval(operation);
    response.setHeader('Retry-After', retryAfter);
  }

  return operation;
}
```

---

## Jobs (AIP-155)

Use Jobs when operations are:

- Repeatable (can be re-run)
- May be scheduled
- Have lifecycle (pause, resume, cancel)

### Job Resource Schema

```yaml
components:
  schemas:
    Job:
      type: object
      properties:
        name:
          type: string
          example: 'jobs/job_abc123'
        state:
          type: string
          enum: [PENDING, RUNNING, SUCCEEDED, FAILED, CANCELLED]
        create_time:
          type: string
          format: date-time
        start_time:
          type: string
          format: date-time
        end_time:
          type: string
          format: date-time
        config:
          type: object
          description: 'Job-specific configuration'
        result:
          type: object
          description: 'Job output (when SUCCEEDED)'
        error:
          $ref: '#/components/schemas/Error'
          description: 'Error details (when FAILED)'
```

### Job Lifecycle

```
POST /jobs                    → Create job (PENDING)
POST /jobs/{id}:start        → Start job (RUNNING)
POST /jobs/{id}:cancel       → Cancel job (CANCELLED)
GET  /jobs/{id}              → Get status
GET  /jobs                   → List jobs
```

### Custom Methods for State Transitions

```yaml
paths:
  /jobs/{job_id}:start:
    post:
      summary: Start a pending job
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Job'
        '400':
          description: Job not in PENDING state

  /jobs/{job_id}:cancel:
    post:
      summary: Cancel a running job
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                reason:
                  type: string
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Job'
```

---

## Webhooks (Alternative)

For fire-and-forget with notification:

```yaml
paths:
  /orders:import:
    post:
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                source:
                  type: string
                callback_url:
                  type: string
                  format: uri
                  description: URL to POST completion notification
      responses:
        '202':
          description: Import queued
```

Callback payload:

```json
{
  "data": {
    "items_imported": 150,
    "operation_id": "op_abc123",
    "status": "succeeded"
  },
  "event": "import.completed",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## Cancellation

### Idempotent Cancel

```typescript
@Post(':id/cancel')
async cancelOperation(@Param('id') id: string): Promise<Operation> {
  const operation = await this.operationsService.findOne(id);

  if (operation.done) {
    // Already done - return current state (idempotent)
    return operation;
  }

  // Request cancellation
  await this.operationsService.requestCancellation(id);

  // Return updated state
  return this.operationsService.findOne(id);
}
```

### Cancel May Not Be Immediate

The operation may complete before cancellation takes effect. Design for this:

```json
{
  "done": true,
  "metadata": {
    "cancellation_requested": true
  },
  "name": "operations/op_abc123",
  "result": {
    "response": { "items_imported": 50 }
  }
}
```

---

## Common Mistakes

❌ **Returning 200 for async operation start**

✅ **Return 202 Accepted** with Location header

❌ **No way to track progress**

✅ **Include progress metadata** (percent, items processed, ETA)

❌ **Operations that never complete (orphaned)**

✅ **Timeout operations** - Mark failed after max duration

❌ **No way to cancel**

✅ **Support cancellation** for long operations

❌ **Polling without guidance**

✅ **Include Retry-After header** with suggested interval
