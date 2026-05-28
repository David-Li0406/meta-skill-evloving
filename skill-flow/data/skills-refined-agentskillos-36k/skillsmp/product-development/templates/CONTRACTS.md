# Interface Contract Templates

## REST API Contract Template

```yaml
# OpenAPI 3.0 specification template
openapi: 3.0.3
info:
  title: [API Name]
  version: 1.0.0
  description: [API Description]

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://api.staging.example.com/v1
    description: Staging

paths:
  /resources:
    get:
      summary: List resources
      operationId: listResources
      tags: [Resources]
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
            maximum: 100
        - name: offset
          in: query
          schema:
            type: integer
            default: 0
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ResourceList'
        '401':
          $ref: '#/components/responses/Unauthorized'

    post:
      summary: Create resource
      operationId: createResource
      tags: [Resources]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateResourceRequest'
      responses:
        '201':
          description: Created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Resource'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'

  /resources/{id}:
    get:
      summary: Get resource by ID
      operationId: getResource
      tags: [Resources]
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Resource'
        '404':
          $ref: '#/components/responses/NotFound'

components:
  schemas:
    Resource:
      type: object
      required: [id, name, status, createdAt]
      properties:
        id:
          type: string
          format: uuid
        name:
          type: string
          minLength: 1
          maxLength: 255
        status:
          type: string
          enum: [active, inactive, pending]
        createdAt:
          type: string
          format: date-time

    CreateResourceRequest:
      type: object
      required: [name]
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 255
        description:
          type: string
          maxLength: 1000

    ResourceList:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/Resource'
        pagination:
          $ref: '#/components/schemas/Pagination'

    Pagination:
      type: object
      properties:
        total:
          type: integer
        limit:
          type: integer
        offset:
          type: integer

    Error:
      type: object
      required: [code, message]
      properties:
        code:
          type: string
        message:
          type: string
        details:
          type: object

  responses:
    BadRequest:
      description: Bad Request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    Unauthorized:
      description: Unauthorized
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    NotFound:
      description: Not Found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - bearerAuth: []
```

## CLI Contract Template

```markdown
# CLI Command: [command-name]

## Synopsis
```
program [global-flags] command [command-flags] [arguments...]
```

## Global Flags
| Flag | Short | Type | Default | Description |
|------|-------|------|---------|-------------|
| --config | -c | string | ~/.config/app/config.yaml | Config file path |
| --verbose | -v | bool | false | Enable verbose output |
| --quiet | -q | bool | false | Suppress non-error output |
| --output | -o | string | text | Output format (text\|json\|yaml) |

## Commands

### `command create`
Create a new resource.

**Usage:**
```
program create [flags] <name>
```

**Arguments:**
| Argument | Required | Description |
|----------|----------|-------------|
| name | Yes | Name of the resource to create |

**Flags:**
| Flag | Short | Type | Default | Description |
|------|-------|------|---------|-------------|
| --description | -d | string | "" | Resource description |
| --tags | -t | []string | [] | Tags (can specify multiple) |
| --dry-run | | bool | false | Preview without creating |

**Examples:**
```bash
# Basic creation
program create my-resource

# With options
program create my-resource -d "Description" -t tag1 -t tag2

# Dry run
program create my-resource --dry-run

# JSON output
program -o json create my-resource
```

**Output (text):**
```
Created resource: my-resource (id: abc123)
```

**Output (json):**
```json
{
  "id": "abc123",
  "name": "my-resource",
  "status": "created"
}
```

### `command list`
List all resources.

**Usage:**
```
program list [flags]
```

**Flags:**
| Flag | Short | Type | Default | Description |
|------|-------|------|---------|-------------|
| --filter | -f | string | "" | Filter expression |
| --limit | -l | int | 20 | Max results |
| --all | -a | bool | false | Show all (ignore limit) |

## Exit Codes
| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Invalid arguments |
| 3 | Resource not found |
| 4 | Permission denied |
| 5 | Network error |
| 10 | Configuration error |
```

## Event/Message Contract Template

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://example.com/schemas/events/resource-created.json",
  "title": "ResourceCreated Event",
  "description": "Emitted when a new resource is created",
  "type": "object",
  "required": ["eventId", "eventType", "eventVersion", "timestamp", "source", "data"],
  "properties": {
    "eventId": {
      "type": "string",
      "format": "uuid",
      "description": "Unique identifier for this event instance"
    },
    "eventType": {
      "type": "string",
      "const": "resource.created",
      "description": "Type of event"
    },
    "eventVersion": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+$",
      "description": "Schema version (e.g., '1.0')"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "When the event occurred"
    },
    "source": {
      "type": "string",
      "description": "Service that produced the event"
    },
    "correlationId": {
      "type": "string",
      "description": "ID to correlate related events"
    },
    "data": {
      "type": "object",
      "required": ["resourceId", "name", "createdBy"],
      "properties": {
        "resourceId": {
          "type": "string",
          "format": "uuid"
        },
        "name": {
          "type": "string"
        },
        "createdBy": {
          "type": "string"
        },
        "metadata": {
          "type": "object",
          "additionalProperties": true
        }
      }
    }
  },
  "examples": [
    {
      "eventId": "550e8400-e29b-41d4-a716-446655440000",
      "eventType": "resource.created",
      "eventVersion": "1.0",
      "timestamp": "2024-01-15T10:30:00Z",
      "source": "resource-service",
      "correlationId": "req-123",
      "data": {
        "resourceId": "res-456",
        "name": "My Resource",
        "createdBy": "user-789",
        "metadata": {
          "environment": "production"
        }
      }
    }
  ]
}
```

## Configuration Schema Template

```yaml
# JSON Schema for configuration file
$schema: http://json-schema.org/draft-07/schema#
title: Application Configuration
type: object
required:
  - server
additionalProperties: false

properties:
  server:
    type: object
    required: [host, port]
    properties:
      host:
        type: string
        default: localhost
        description: Server hostname
      port:
        type: integer
        minimum: 1
        maximum: 65535
        default: 8080
        description: Server port
      tls:
        type: object
        properties:
          enabled:
            type: boolean
            default: false
          cert:
            type: string
            description: Path to TLS certificate
          key:
            type: string
            description: Path to TLS key

  database:
    type: object
    properties:
      url:
        type: string
        format: uri
        description: Database connection string
      pool:
        type: object
        properties:
          min:
            type: integer
            default: 2
          max:
            type: integer
            default: 10

  logging:
    type: object
    properties:
      level:
        type: string
        enum: [debug, info, warn, error]
        default: info
      format:
        type: string
        enum: [json, text]
        default: json

  features:
    type: object
    additionalProperties:
      type: boolean
    default: {}
    description: Feature flags

# Environment variable mapping
x-env-mapping:
  server.host: APP_SERVER_HOST
  server.port: APP_SERVER_PORT
  database.url: APP_DATABASE_URL
  logging.level: APP_LOG_LEVEL
```

## UI Component Contract Template (TypeScript)

```typescript
/**
 * Component: ResourceCard
 * Purpose: Display a resource summary with actions
 * Use Cases: UC-005, UC-006
 */

// Props interface
export interface ResourceCardProps {
  /** Unique identifier for the resource */
  id: string;

  /** Resource data to display */
  resource: Resource;

  /** Available actions for this resource */
  actions?: ResourceAction[];

  /** Callback when an action is triggered */
  onAction?: (action: ResourceAction, resourceId: string) => void;

  /** Visual variant */
  variant?: 'default' | 'compact' | 'detailed';

  /** Whether the card is in a loading state */
  loading?: boolean;

  /** Whether the card is selected */
  selected?: boolean;

  /** Additional CSS classes */
  className?: string;
}

// Related types
export interface Resource {
  id: string;
  name: string;
  description?: string;
  status: ResourceStatus;
  createdAt: Date;
  updatedAt: Date;
  metadata?: Record<string, unknown>;
}

export type ResourceStatus = 'active' | 'inactive' | 'pending' | 'error';

export type ResourceAction = 'view' | 'edit' | 'delete' | 'duplicate';

// Component states
export interface ResourceCardState {
  isHovered: boolean;
  isActionMenuOpen: boolean;
  pendingAction: ResourceAction | null;
}

// Events emitted
export interface ResourceCardEvents {
  'action': { action: ResourceAction; resourceId: string };
  'select': { resourceId: string; selected: boolean };
  'hover': { resourceId: string; hovered: boolean };
}

// Accessibility requirements
export const a11yRequirements = {
  role: 'article',
  ariaLabel: 'Resource card for {name}',
  keyboardNav: ['Enter to select', 'Space to toggle actions', 'Escape to close menu'],
  focusIndicator: 'visible outline on focus',
};

// Visual states
export const visualStates = {
  default: 'Standard appearance',
  hover: 'Elevated shadow, highlight border',
  selected: 'Primary border, checkmark indicator',
  loading: 'Skeleton placeholder',
  error: 'Error border, error icon',
  disabled: 'Reduced opacity, no interactions',
};
```
