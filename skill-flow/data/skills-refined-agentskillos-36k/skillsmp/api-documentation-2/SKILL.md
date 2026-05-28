---
name: api-documentation
description: This skill provides patterns for generating and maintaining API documentation including OpenAPI specs, endpoint documentation, and example generation.
---

# API Documentation Skill

Generate and maintain comprehensive API documentation.

## When to Use

- Generating OpenAPI/Swagger specifications
- Documenting REST API endpoints
- Creating request/response examples
- Documenting API versioning
- Building API reference guides

## Reference Documents

- [OpenAPI Patterns](./references/openapi-patterns.md) - OpenAPI/Swagger specification patterns
- [Endpoint Documentation](./references/endpoint-documentation.md) - Standards for documenting endpoints
- [Example Generation](./references/example-generation.md) - Request/response example patterns
- [Versioning Documentation](./references/versioning-docs.md) - API versioning documentation

## Core Principles

### 1. Document Every Endpoint

Every public endpoint needs:
- HTTP method and path
- Description of purpose
- Request parameters
- Request body schema
- Response schemas
- Error responses
- Authentication requirements

### 2. Provide Realistic Examples

```yaml
# Good example - realistic data
example:
  id: "ord_1234567890"
  customer_email: "jane.doe@example.com"
  total: 149.99
  items:
    - product_id: "prod_abc"
      name: "Wireless Headphones"
      quantity: 1
      price: 149.99

# Bad example - placeholder data
example:
  id: "string"
  customer_email: "string"
  total: 0
```

### 3. Document Errors Thoroughly

```yaml
responses:
  400:
    description: Validation error
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/ValidationError'
        example:
          error: "validation_error"
          message: "Invalid request parameters"
          details:
            - field: "email"
              message: "Must be a valid email address"
```

## Workflow: Generating API Documentation

### Step 1: Discover Endpoints

```bash
# Find all route definitions
grep -r "@router\|@api\|@app\." --include="*.py" src/
grep -r "router\.\|app\." --include="*.ts" src/
```

### Step 2: Extract Endpoint Info

For each endpoint, gather:
- Path and method
- Path parameters
- Query parameters
- Request body structure
- Response structure
- Status codes

### Step 3: Generate OpenAPI Spec

```yaml
openapi: 3.0.0
info:
  title: My API
  version: 1.0.0
  description: API for managing orders

paths:
  /orders:
    post:
      summary: Create a new order
      operationId: createOrder
      tags:
        - Orders
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateOrderRequest'
      responses:
        '201':
          description: Order created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Order'
```

### Step 4: Add Examples

```yaml
components:
  schemas:
    Order:
      type: object
      properties:
        id:
          type: string
          example: "ord_1234567890"
        status:
          type: string
          enum: [pending, confirmed, shipped, delivered]
          example: "pending"
        total:
          type: number
          format: float
          example: 149.99
```

### Step 5: Validate Spec

```bash
# Validate OpenAPI spec
npx @redocly/cli lint openapi.yaml

# Generate docs preview
npx @redocly/cli preview-docs openapi.yaml
```

## Documentation Templates

### Endpoint Documentation

```markdown
## Create Order

Creates a new order for the authenticated user.

**Endpoint:** `POST /api/orders`

**Authentication:** Required (Bearer token)

### Request

#### Headers
| Header | Required | Description |
|--------|----------|-------------|
| Authorization | Yes | Bearer token |
| Content-Type | Yes | application/json |

#### Body
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| items | array | Yes | List of items to order |
| items[].product_id | string | Yes | Product identifier |
| items[].quantity | integer | Yes | Quantity (1-100) |
| shipping_address_id | string | No | Use saved address |

### Response

#### Success (201)
```json
{
  "id": "ord_1234567890",
  "status": "pending",
  "total": 149.99,
  "items": [...],
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Errors
| Status | Description |
|--------|-------------|
| 400 | Invalid request body |
| 401 | Authentication required |
| 422 | Validation failed |
```

## Quick Reference

### HTTP Status Codes

| Code | When to Use |
|------|-------------|
| 200 | Successful GET, PUT, PATCH |
| 201 | Successful POST (resource created) |
| 204 | Successful DELETE (no content) |
| 400 | Bad request (malformed syntax) |
| 401 | Authentication required |
| 403 | Permission denied |
| 404 | Resource not found |
| 422 | Validation error |
| 500 | Server error |

### Common Schema Patterns

```yaml
# Pagination
PaginatedResponse:
  type: object
  properties:
    data:
      type: array
      items:
        $ref: '#/components/schemas/Item'
    meta:
      type: object
      properties:
        total:
          type: integer
        page:
          type: integer
        per_page:
          type: integer
        has_next:
          type: boolean

# Error Response
ErrorResponse:
  type: object
  required:
    - error
    - message
  properties:
    error:
      type: string
    message:
      type: string
    details:
      type: array
      items:
        type: object
        properties:
          field:
            type: string
          message:
            type: string
```
