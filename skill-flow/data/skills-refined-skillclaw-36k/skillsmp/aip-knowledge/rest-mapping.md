# REST/OpenAPI Adaptations from Protobuf AIPs

## Linter Rules

**This is a reference document only.** No automated rules - this document helps translate protobuf AIP concepts to REST/OpenAPI equivalents.

Related rules that apply to REST APIs:

- `aip122/*` - Naming conventions
- `aip131/get-no-body` - GET without body
- `aip133/post-returns-201` - POST status codes
- `aip134/patch-over-put` - PATCH for updates

Google's AIPs are written with Protocol Buffers in mind. This guide maps those patterns to REST/OpenAPI conventions.

## Resource Names

### Protobuf Style

```
projects/123/locations/us-east1/instances/my-instance
```

### REST Adaptation

```
/projects/123/locations/us-east1/instances/my-instance
```

Or with nested resources:

```
/projects/{project_id}/instances/{instance_id}
```

**Decision:** Choose hierarchical paths when:

- Resources have clear ownership
- Access control follows hierarchy
- You'll never need to query across parents

Choose flat paths with query filters when:

- Resources can exist under multiple parents
- Cross-parent queries are common

## Standard Methods Mapping

| AIP Method | HTTP   | URI Pattern       | Request Body       | Response          |
| ---------- | ------ | ----------------- | ------------------ | ----------------- |
| Get        | GET    | `/resources/{id}` | None               | Resource          |
| List       | GET    | `/resources`      | None               | Collection        |
| Create     | POST   | `/resources`      | Resource           | Resource          |
| Update     | PATCH  | `/resources/{id}` | Resource (partial) | Resource          |
| Delete     | DELETE | `/resources/{id}` | None               | Empty or Resource |

## Custom Methods

### Protobuf

```protobuf
rpc CancelOrder(CancelOrderRequest) returns (Order) {
  option (google.api.http) = {
    post: "/v1/{name=orders/*}:cancel"
    body: "*"
  };
}
```

### REST Adaptation

Use `:action` suffix:

```
POST /orders/{order_id}:cancel
POST /orders/{order_id}:ship
POST /documents/{doc_id}:publish
```

Or verb-based paths (less AIP-aligned but common):

```
POST /orders/{order_id}/cancel
POST /orders/{order_id}/shipments
```

**Recommendation:** Use `:action` for state transitions, nested resources for creating related entities.

## Field Mask

### Protobuf

```protobuf
import "google/protobuf/field_mask.proto";

message UpdateBookRequest {
  Book book = 1;
  google.protobuf.FieldMask update_mask = 2;
}
```

### REST Adaptation

Option 1: Query parameter

```
PATCH /books/123?update_mask=title,author.name
```

Option 2: Request body field

```json
{
  "book": { "title": "New Title" },
  "update_mask": "title"
}
```

Option 3: HTTP header (less common)

```
PATCH /books/123
X-Update-Mask: title,author.name
```

**Recommendation:** Request body field for complex updates, query param for simple cases.

## Timestamps

### Protobuf

```protobuf
import "google/protobuf/timestamp.proto";

google.protobuf.Timestamp create_time = 1;
```

### REST/JSON

```json
{
  "create_time": "2024-01-15T10:30:00Z"
}
```

Always use RFC 3339 / ISO 8601 format with timezone.

```yaml
# OpenAPI
created_at:
  type: string
  format: date-time
  example: '2024-01-15T10:30:00Z'
```

## Duration

### Protobuf

```protobuf
import "google/protobuf/duration.proto";

google.protobuf.Duration timeout = 1;
```

### REST Options

Option 1: ISO 8601 duration string

```json
{ "timeout": "PT30S" }  // 30 seconds
{ "timeout": "P1D" }     // 1 day
```

Option 2: Seconds as number (simpler)

```json
{ "timeout_seconds": 30 }
```

Option 3: Human-readable with unit

```json
{ "timeout": "30s" }
{ "timeout": "5m" }
```

**Recommendation:** Use seconds as number for simplicity, ISO 8601 for precision.

## Enumerations

### Protobuf

```protobuf
enum OrderStatus {
  ORDER_STATUS_UNSPECIFIED = 0;
  PENDING = 1;
  SHIPPED = 2;
  DELIVERED = 3;
}
```

### REST/JSON

Use string values, not integers:

```json
{ "status": "PENDING" }
```

```yaml
# OpenAPI
status:
  type: string
  enum: [PENDING, SHIPPED, DELIVERED, CANCELLED]
```

Include "UNSPECIFIED" only if clients need to explicitly indicate "not set."

## Oneof

### Protobuf

```protobuf
message Notification {
  oneof channel {
    EmailConfig email = 1;
    SmsConfig sms = 2;
    WebhookConfig webhook = 3;
  }
}
```

### REST Options

Option 1: Discriminated union with `type` field

```json
{
  "channel": {
    "email_address": "user@example.com",
    "type": "email"
  }
}
```

Option 2: Nullable fields (at most one populated)

```json
{
  "email": { "address": "user@example.com" },
  "sms": null,
  "webhook": null
}
```

Option 3: Separate endpoints

```
POST /notifications/email
POST /notifications/sms
POST /notifications/webhook
```

**Recommendation:** Discriminated union with `type` for API clarity.

```yaml
# OpenAPI
NotificationChannel:
  type: object
  required: [type]
  properties:
    type:
      type: string
      enum: [email, sms, webhook]
    email_address:
      type: string
    phone_number:
      type: string
    webhook_url:
      type: string
  discriminator:
    propertyName: type
    mapping:
      email: '#/components/schemas/EmailChannel'
      sms: '#/components/schemas/SmsChannel'
      webhook: '#/components/schemas/WebhookChannel'
```

## Any (Dynamic Typing)

### Protobuf

```protobuf
import "google/protobuf/any.proto";

google.protobuf.Any payload = 1;
```

### REST Adaptation

Option 1: Type URL field

```json
{
  "payload": {
    "@type": "type.example.com/OrderCreatedEvent",
    "order_id": "ord_123",
    "total": 99.99
  }
}
```

Option 2: Separate type and data

```json
{
  "payload": {
    "order_id": "ord_123"
  },
  "payload_type": "OrderCreatedEvent"
}
```

## Empty Response

### Protobuf

```protobuf
import "google/protobuf/empty.proto";

rpc DeleteBook(DeleteBookRequest) returns (google.protobuf.Empty);
```

### REST Options

Option 1: 204 No Content (truly empty)

```
HTTP/1.1 204 No Content
```

Option 2: Return deleted resource (soft delete)

```
HTTP/1.1 200 OK
{
  "id": "book_123",
  "deleted": true,
  "deleted_at": "2024-01-15T10:30:00Z"
}
```

Option 3: Empty JSON object

```
HTTP/1.1 200 OK
{}
```

**Recommendation:** 204 for hard delete, 200 with resource for soft delete.

## Repeated Fields (Arrays)

### Protobuf

```protobuf
repeated string tags = 1;
```

### REST/JSON

```json
{
  "tags": ["urgent", "review", "q1"]
}
```

Empty array vs missing field:

- `"tags": []` - explicitly empty
- Field absent - use default (usually empty)

## Maps

### Protobuf

```protobuf
map<string, string> labels = 1;
```

### REST/JSON

```json
{
  "labels": {
    "environment": "production",
    "team": "platform"
  }
}
```

```yaml
# OpenAPI
labels:
  type: object
  additionalProperties:
    type: string
```

## Wrapper Types (Nullable Primitives)

### Protobuf

```protobuf
import "google/protobuf/wrappers.proto";

google.protobuf.Int32Value priority = 1;  // nullable int
```

### REST/JSON

JSON natively supports null:

```json
{ "priority": null }
{ "priority": 5 }
```

```yaml
# OpenAPI
priority:
  type: integer
  nullable: true
```
