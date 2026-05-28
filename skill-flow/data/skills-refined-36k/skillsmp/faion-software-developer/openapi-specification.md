# OpenAPI Specification

**ID:** openapi-specification

## Problem

API documentation drifts from implementation. Need single source of truth.

## Framework

**OpenAPI 3.1 Structure:**

```yaml
openapi: 3.1.0
info:
  title: User Management API
  version: 1.0.0
  description: API for managing users and their resources
  contact:
    name: API Support
    email: api@example.com
    url: https://example.com/support
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://staging-api.example.com/v1
    description: Staging

paths:
  /users:
    get:
      summary: List all users
      operationId: listUsers
      tags: [Users]
      parameters:
        - $ref: '#/components/parameters/PageLimit'
        - $ref: '#/components/parameters/PageOffset'
        - name: status
          in: query
          schema:
            type: string
            enum: [active, inactive]
      responses:
        '200':
          description: List of users
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'
        '401':
          $ref: '#/components/responses/Unauthorized'
    post:
      summary: Create a new user
      operationId: createUser
      tags: [Users]
      requestBody:
        required: true
        content:
          application/json:
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

  /users/{userId}:
    get:
      summary: Get user by ID
      operationId: getUser
      tags: [Users]
      parameters:
        - $ref: '#/components/parameters/UserId'
      responses:
        '200':
          description: User details
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
      required: [id, email, name]
      properties:
        id:
          type: string
          format: uuid
          example: "550e8400-e29b-41d4-a716-446655440000"
        email:
          type: string
          format: email
          example: "user@example.com"
        name:
          type: string
          minLength: 1
          maxLength: 100
          example: "John Doe"
        status:
          type: string
          enum: [active, inactive]
          default: active
        createdAt:
          type: string
          format: date-time

    CreateUserRequest:
      type: object
      required: [email, name]
      properties:
        email:
          type: string
          format: email
        name:
          type: string
          minLength: 1
          maxLength: 100

    UserList:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/User'
        meta:
          $ref: '#/components/schemas/PaginationMeta'

    PaginationMeta:
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
          type: array
          items:
            type: object

  parameters:
    UserId:
      name: userId
      in: path
      required: true
      schema:
        type: string
        format: uuid

    PageLimit:
      name: limit
      in: query
      schema:
        type: integer
        minimum: 1
        maximum: 100
        default: 20

    PageOffset:
      name: offset
      in: query
      schema:
        type: integer
        minimum: 0
        default: 0

  responses:
    BadRequest:
      description: Bad request
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
      description: Resource not found
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

tags:
  - name: Users
    description: User management operations
```

## Code Generation

```bash
# Generate TypeScript client
npx openapi-typescript-codegen \
  --input ./openapi.yaml \
  --output ./src/api-client

# Generate Python client
openapi-generator generate \
  -i openapi.yaml \
  -g python \
  -o ./python-client

# Generate server stubs
openapi-generator generate \
  -i openapi.yaml \
  -g python-fastapi \
  -o ./server
```

## Best Practices

- Use $ref for reusable components
- Include examples for every schema
- Add descriptions to all operations
- Use operationId for code generation
- Validate spec with spectral or redocly
- Version control your OpenAPI spec
- Generate SDK clients from spec

## Agent

faion-api-agent
