# Phase 6: Interface Contracts

## Objective

Define all interaction boundaries with precise contracts for APIs, CLIs, configurations, and UIs.

## Step 1: Identify All Interfaces

```markdown
### Interface Inventory

| Interface | Type | Consumers | Direction |
|-----------|------|-----------|-----------|
| [API Endpoint] | REST/GraphQL/gRPC | [Who calls it] | In/Out/Both |
| [CLI Command] | Command Line | [Who uses it] | In/Out |
| [Config File] | Configuration | [What reads it] | In |
| [Event] | Message/Event | [Who subscribes] | Out |
| [UI Component] | User Interface | [What uses it] | Both |
```

## Step 2: API Contracts

### REST API Contract Template

```markdown
### Endpoint: [METHOD] [/path/{param}]

**Purpose**: [What this endpoint does]
**Use Case**: [UC-ID] - [Name]

**Request**:
```http
[METHOD] /api/v1/[resource]/{id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "field1": "string (required) - description",
  "field2": 123,            // number (optional) - description
  "field3": {               // object (required)
    "nested": "value"
  }
}
```

**Response Success (200/201)**:
```json
{
  "id": "uuid",
  "field1": "value",
  "createdAt": "2024-01-01T00:00:00Z",
  "_links": {
    "self": "/api/v1/resource/{id}",
    "related": "/api/v1/related/{id}"
  }
}
```

**Response Errors**:
| Status | Code | Message | When |
|--------|------|---------|------|
| 400 | INVALID_INPUT | "Field X is required" | Missing required field |
| 401 | UNAUTHORIZED | "Invalid token" | Bad/expired auth |
| 403 | FORBIDDEN | "Insufficient permissions" | User can't access |
| 404 | NOT_FOUND | "Resource not found" | ID doesn't exist |
| 409 | CONFLICT | "Resource already exists" | Duplicate creation |
| 422 | VALIDATION_ERROR | "Field X must be positive" | Business rule violation |
| 500 | INTERNAL_ERROR | "An error occurred" | System failure |

**Rate Limits**: [X] requests per [time period]
**Idempotency**: [Yes/No] - [Key field if yes]
```

### GraphQL Contract Template

```markdown
### Operation: [Query/Mutation] [operationName]

**Purpose**: [What this operation does]

**Schema**:
```graphql
type Query {
  getResource(id: ID!): Resource
  listResources(filter: ResourceFilter, limit: Int = 10): ResourceConnection!
}

type Mutation {
  createResource(input: CreateResourceInput!): Resource!
  updateResource(id: ID!, input: UpdateResourceInput!): Resource!
}

type Resource {
  id: ID!
  name: String!
  status: ResourceStatus!
  createdAt: DateTime!
}

enum ResourceStatus {
  ACTIVE
  INACTIVE
  PENDING
}

input CreateResourceInput {
  name: String!
  description: String
}
```

**Example Query**:
```graphql
query GetResource($id: ID!) {
  getResource(id: $id) {
    id
    name
    status
  }
}
```
```

### gRPC Contract Template

```markdown
### Service: [ServiceName]

**Proto Definition**:
```protobuf
syntax = "proto3";

package myservice.v1;

service ResourceService {
  rpc GetResource(GetResourceRequest) returns (Resource);
  rpc CreateResource(CreateResourceRequest) returns (Resource);
  rpc ListResources(ListResourcesRequest) returns (stream Resource);
}

message Resource {
  string id = 1;
  string name = 2;
  ResourceStatus status = 3;
  google.protobuf.Timestamp created_at = 4;
}

enum ResourceStatus {
  RESOURCE_STATUS_UNSPECIFIED = 0;
  RESOURCE_STATUS_ACTIVE = 1;
  RESOURCE_STATUS_INACTIVE = 2;
}

message GetResourceRequest {
  string id = 1;
}
```
```

## Step 3: CLI Contracts

```markdown
### Command: [command-name]

**Purpose**: [What this command does]
**Use Case**: [UC-ID] - [Name]

**Syntax**:
```
program command [subcommand] [flags] [arguments]
```

**Arguments**:
| Argument | Required | Description | Default |
|----------|----------|-------------|---------|
| [arg1] | Yes | [Description] | - |
| [arg2] | No | [Description] | [default] |

**Flags**:
| Flag | Short | Type | Description | Default |
|------|-------|------|-------------|---------|
| --output | -o | string | Output format (json\|table\|yaml) | table |
| --verbose | -v | bool | Enable verbose output | false |
| --config | -c | string | Config file path | ~/.config/app |

**Examples**:
```bash
# Basic usage
program command arg1

# With flags
program command --output json --verbose arg1

# With config
program command -c /path/to/config arg1 arg2
```

**Exit Codes**:
| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Invalid arguments |
| 3 | Permission denied |
| 4 | Resource not found |

**Output Formats**:

**JSON**:
```json
{
  "status": "success",
  "data": { ... }
}
```

**Table**:
```
ID        NAME        STATUS
abc123    Resource1   active
def456    Resource2   pending
```
```

## Step 4: Configuration Contracts

```markdown
### Configuration: [config-name]

**File Locations** (in order of precedence):
1. Command line flag: `--config /path/to/config.yaml`
2. Environment variable: `APP_CONFIG_PATH`
3. User config: `~/.config/app/config.yaml`
4. System config: `/etc/app/config.yaml`

**Schema**:
```yaml
# Required settings
server:
  host: string          # Server hostname (required)
  port: integer         # Server port (required, 1-65535)

# Optional settings
database:
  url: string           # Database connection string
  pool_size: integer    # Connection pool size (default: 10)

logging:
  level: enum           # debug|info|warn|error (default: info)
  format: enum          # json|text (default: json)

# Feature flags
features:
  experimental: boolean # Enable experimental features (default: false)
```

**Environment Variable Mapping**:
| Config Path | Environment Variable | Example |
|-------------|---------------------|---------|
| server.host | APP_SERVER_HOST | localhost |
| server.port | APP_SERVER_PORT | 8080 |
| database.url | APP_DATABASE_URL | postgres://... |

**Validation Rules**:
| Field | Rule | Error Message |
|-------|------|---------------|
| server.port | 1-65535 | "Port must be between 1 and 65535" |
| logging.level | enum value | "Invalid log level" |
```

## Step 5: Event/Message Contracts

```markdown
### Event: [event.name]

**Purpose**: [What this event represents]
**Producer**: [What component emits this]
**Consumers**: [What components listen]

**Schema**:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["eventId", "eventType", "timestamp", "data"],
  "properties": {
    "eventId": {
      "type": "string",
      "format": "uuid"
    },
    "eventType": {
      "type": "string",
      "const": "resource.created"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "data": {
      "type": "object",
      "properties": {
        "resourceId": { "type": "string" },
        "name": { "type": "string" }
      }
    }
  }
}
```

**Example**:
```json
{
  "eventId": "550e8400-e29b-41d4-a716-446655440000",
  "eventType": "resource.created",
  "timestamp": "2024-01-01T12:00:00Z",
  "data": {
    "resourceId": "res_123",
    "name": "My Resource"
  }
}
```

**Delivery Guarantees**: [At-least-once / At-most-once / Exactly-once]
**Ordering**: [Ordered by X / Unordered]
**Retention**: [How long events are retained]
```

## Step 6: UI Component Contracts (for Frontend)

```markdown
### Component: [ComponentName]

**Purpose**: [What this component does]
**Use Case**: [UC-ID] - [Name]

**Props Interface**:
```typescript
interface ComponentNameProps {
  // Required props
  id: string;
  data: ResourceData;
  onAction: (action: ActionType) => void;

  // Optional props
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
  className?: string;
}

interface ResourceData {
  id: string;
  name: string;
  status: 'active' | 'inactive';
}

type ActionType = 'edit' | 'delete' | 'view';
```

**States**:
| State | Visual | Behavior |
|-------|--------|----------|
| Default | [Description] | [Interactions] |
| Loading | [Description] | [Interactions] |
| Error | [Description] | [Interactions] |
| Disabled | [Description] | [Interactions] |

**Events Emitted**:
| Event | Payload | When |
|-------|---------|------|
| onAction | ActionType | User clicks action button |
| onChange | NewValue | Value changes |
```

## Step 7: Contract Validation Checklist

For each interface:

- [ ] **Complete**: All fields documented
- [ ] **Consistent**: Naming conventions followed
- [ ] **Versioned**: Version strategy defined
- [ ] **Validated**: Schema validation exists
- [ ] **Documented**: Examples provided
- [ ] **Error Handling**: All error cases defined
- [ ] **Security**: Auth requirements specified

## Phase 6 Approval Gate

```markdown
## Phase 6 Summary: Interface Contracts

### Interfaces Defined
| Type | Count | Coverage |
|------|-------|----------|
| REST Endpoints | [X] | [Y]% of use cases |
| CLI Commands | [X] | [Y]% of use cases |
| Config Schemas | [X] | All components |
| Events | [X] | [Y] producers |
| UI Components | [X] | [Y]% of screens |

### API Surface
[Summary of public API]

### Breaking Change Policy
[How versioning and deprecation will work]

### Contract Testing Strategy
[How contracts will be validated]

---

**Do you approve Phase 6? Any contracts to revise before proceeding to Code Scaffolding?**
```
