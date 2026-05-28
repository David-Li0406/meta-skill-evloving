---
name: openapi-specification
description: Use this skill for expert-level guidance on creating, documenting, and validating OpenAPI specifications for APIs.
---

# OpenAPI Specification

Expert guidance for OpenAPI Specification (formerly Swagger) - the industry-standard for describing RESTful APIs with automatic documentation and code generation.

## Core Concepts

### OpenAPI Specification (OAS)
- API description format (YAML/JSON)
- Version 3.1 (latest) and 3.0
- Machine-readable API contracts
- Automatic documentation generation
- Client/server code generation
- API validation and testing

### Key Components
- Paths (endpoints)
- Operations (HTTP methods)
- Parameters
- Request/Response bodies
- Schemas (data models)
- Security schemes
- Components (reusable objects)

## Basic OpenAPI Specification Example

```yaml
openapi: 3.1.0
info:
  title: Blog API
  description: RESTful API for blog management
  version: 1.0.0
  contact:
    name: API Support
    email: support@example.com
  license:
    name: MIT

servers:
  - url: https://api.example.com/v1
    description: Production server
  - url: https://staging-api.example.com/v1
    description: Staging server

paths:
  /posts:
    get:
      summary: List all posts
      operationId: listPosts
      parameters:
        - name: page
          in: query
          required: false
          schema:
            type: integer
            minimum: 1
            default: 1
        - name: limit
          in: query
          required: false
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Post'
                  pagination:
                    $ref: '#/components/schemas/Pagination'
    post:
      summary: Create a new post
      operationId: createPost
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PostCreate'
      responses:
        '201':
          description: Post created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Post'

components:
  schemas:
    Post:
      type: object
      required:
        - id
        - title
        - content
        - author
        - status
        - createdAt
      properties:
        id:
          type: integer
          format: int64
          readOnly: true
        title:
          type: string
          minLength: 5
          maxLength: 200
        content:
          type: string
          minLength: 10
        author:
          $ref: '#/components/schemas/User'
        status:
          type: string
          enum: [draft, published]
          default: draft
        createdAt:
          type: string
          format: date-time
          readOnly: true

    User:
      type: object
      properties:
        id:
          type: integer
          format: int64
        email:
          type: string
          format: email
        name:
          type: string

    Pagination:
      type: object
      properties:
        page:
          type: integer
        limit:
          type: integer
        total:
          type: integer
        totalPages:
          type: integer
```

## Advanced Features

### Webhooks (OpenAPI 3.1)

```yaml
webhooks:
  postCreated:
    post:
      summary: Post created webhook
      operationId: onPostCreated
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Post'
      responses:
        '200':
          description: Webhook received
```

### Polymorphism (oneOf/anyOf/allOf)

```yaml
components:
  schemas:
    Pet:
      oneOf:
        - $ref: '#/components/schemas/Cat'
        - $ref: '#/components/schemas/Dog'
```

## Validation and Best Practices

### Standard Rules
- **Operation Naming Conventions**: Use specific prefixes for operations (e.g., `get{Resource}`, `list{Resources}`, `create{Resource}`).
- **Descriptions**: Always derive from official documentation; include accurate descriptions for operations.
- **Schema Organization**: Follow a priority for model definitions, ensuring all documented fields are included.

### Security Schemes
- Always use OAuth2 type with scopes for security definitions.

### Schema Validation
- Validate specifications using tools like `swagger-cli` after any changes.

### Documentation Quality
- Include operation summaries, parameter descriptions, and document all enum values with `x-enum-descriptions`.

## Remember
Following these standards ensures consistent API design, clean code generation, and maintainable specifications.

--- 

**Resources**
- OpenAPI Spec: https://spec.openapis.org/
- Swagger Editor: https://editor.swagger.io/
- OpenAPI Tools: https://openapi.tools/