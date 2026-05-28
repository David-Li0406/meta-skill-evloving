# OpenAPI Documentation

Document REST APIs using OpenAPI 3.x and JSON Schema for request/response validation.

---

## When to Use

- Documenting API endpoints
- Generating API documentation
- Validating request/response payloads
- Generating client SDKs
- Contract-first API development

---

## OpenAPI Structure

### Basic Specification

```yaml
openapi: 3.0.3
info:
  title: My API
  description: API for managing resources
  version: 1.0.0
  contact:
    email: api@example.com

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: http://localhost:3000/v1
    description: Development

paths:
  /users:
    get:
      summary: List all users
      operationId: listUsers
      tags:
        - Users
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
          description: List of users
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'

    post:
      summary: Create a user
      operationId: createUser
      tags:
        - Users
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: User created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          $ref: '#/components/responses/BadRequest'
        '422':
          $ref: '#/components/responses/ValidationError'

  /users/{id}:
    get:
      summary: Get user by ID
      operationId: getUser
      tags:
        - Users
      parameters:
        - $ref: '#/components/parameters/UserId'
      responses:
        '200':
          description: User found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          $ref: '#/components/responses/NotFound'

components:
  schemas:
    User:
      type: object
      required:
        - id
        - email
        - name
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        email:
          type: string
          format: email
        name:
          type: string
          minLength: 1
          maxLength: 100
        role:
          type: string
          enum: [user, admin]
          default: user
        createdAt:
          type: string
          format: date-time
          readOnly: true

    CreateUserRequest:
      type: object
      required:
        - email
        - name
      properties:
        email:
          type: string
          format: email
        name:
          type: string
          minLength: 1
          maxLength: 100
        role:
          type: string
          enum: [user, admin]
          default: user

    UserList:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/User'
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
        hasMore:
          type: boolean

    Error:
      type: object
      required:
        - error
      properties:
        error:
          type: object
          required:
            - code
            - message
          properties:
            code:
              type: string
            message:
              type: string
            details:
              type: object

  parameters:
    UserId:
      name: id
      in: path
      required: true
      schema:
        type: string
        format: uuid

  responses:
    BadRequest:
      description: Bad request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: BAD_REQUEST
              message: Invalid request format

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: NOT_FOUND
              message: User not found

    ValidationError:
      description: Validation failed
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: VALIDATION_ERROR
              message: Request validation failed
              details:
                errors:
                  - path: /email
                    message: must be a valid email

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - bearerAuth: []
```

---

## JSON Schema Patterns

### Standalone Schema Files

Create reusable schemas in separate files:

**schemas/user.json:**
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://api.example.com/schemas/user.json",
  "title": "User",
  "type": "object",
  "required": ["email", "name"],
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid",
      "readOnly": true
    },
    "email": {
      "type": "string",
      "format": "email",
      "maxLength": 254
    },
    "name": {
      "type": "string",
      "minLength": 1,
      "maxLength": 100,
      "pattern": "^[\\p{L}\\s'-]+$"
    },
    "role": {
      "type": "string",
      "enum": ["user", "admin"],
      "default": "user"
    }
  },
  "additionalProperties": false
}
```

### Common Schema Patterns

**Nullable fields:**
```json
{
  "deletedAt": {
    "type": ["string", "null"],
    "format": "date-time"
  }
}
```

**Conditional requirements:**
```json
{
  "if": {
    "properties": { "type": { "const": "business" } }
  },
  "then": {
    "required": ["companyName", "taxId"]
  }
}
```

**Pattern matching:**
```json
{
  "phone": {
    "type": "string",
    "pattern": "^\\+?[1-9]\\d{1,14}$"
  }
}
```

---

## Request Validation

### Using AJV

```javascript
import Ajv from 'ajv';
import addFormats from 'ajv-formats';

const ajv = new Ajv({ allErrors: true, removeAdditional: true });
addFormats(ajv);

// Load schemas
import userSchema from './schemas/user.json' assert { type: 'json' };
ajv.addSchema(userSchema);

/**
 * Validation middleware factory
 * @param {string} schemaId - Schema $id or key
 * @returns {Function} Express middleware
 */
function validate(schemaId) {
  const validateFn = ajv.getSchema(schemaId);

  if (!validateFn) {
    throw new Error(`Schema not found: ${schemaId}`);
  }

  return (req, res, next) => {
    const valid = validateFn(req.body);

    if (!valid) {
      return res.status(422).json({
        error: {
          code: 'VALIDATION_ERROR',
          message: 'Request validation failed',
          details: {
            errors: validateFn.errors.map(e => ({
              path: e.instancePath || '/',
              message: e.message,
              keyword: e.keyword
            }))
          }
        }
      });
    }

    next();
  };
}

// Usage
app.post('/api/users',
  validate('https://api.example.com/schemas/user.json'),
  createUser
);
```

---

## Endpoint Documentation Command

The `/add-endpoint` command generates:
1. Route handler stub
2. OpenAPI path entry
3. JSON Schema for request/response

See `.claude/commands/add-endpoint.md` for details.

---

## File Organization

```
project/
├── openapi.yaml           # Main OpenAPI spec
├── schemas/               # JSON Schema files
│   ├── user.json
│   ├── product.json
│   └── common/
│       ├── pagination.json
│       └── error.json
└── src/
    └── api/
        ├── routes.js
        └── validators.js
```

---

## Tools

### Documentation Generation

Generate HTML docs from OpenAPI:

```bash
# Using Redoc
npx @redocly/cli build-docs openapi.yaml -o docs/api.html

# Using Swagger UI
npx swagger-ui-express
```

### Validation

Validate OpenAPI spec:

```bash
npx @redocly/cli lint openapi.yaml
```

### Client Generation

Generate TypeScript types:

```bash
npx openapi-typescript openapi.yaml -o src/types/api.d.ts
```

---

## Checklist

When documenting APIs:

- [ ] Create openapi.yaml in project root
- [ ] Define all endpoints with operationId
- [ ] Document request/response schemas
- [ ] Include error responses (400, 401, 404, 422, 500)
- [ ] Add examples for complex types
- [ ] Document authentication requirements
- [ ] Define reusable components
- [ ] Validate spec with linter
- [ ] Generate documentation
- [ ] Keep spec in sync with implementation
