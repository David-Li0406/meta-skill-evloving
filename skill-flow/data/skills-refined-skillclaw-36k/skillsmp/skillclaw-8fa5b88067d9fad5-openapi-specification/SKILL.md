---
name: openapi-specification
description: Use this skill when you need to create, document, or validate RESTful APIs using the OpenAPI Specification (OAS).
---

# OpenAPI Specification Skill

This skill provides guidance on creating and maintaining OpenAPI specifications, ensuring adherence to industry standards and best practices.

## Core Concepts

### OpenAPI Specification (OAS)
- API description format (YAML/JSON)
- Version 3.1 (latest) and 3.0
- Machine-readable API contracts
- Automatic documentation generation
- Client/server code generation
- API validation and testing

### Key Components
- **Paths**: Define API endpoints.
- **Operations**: Specify HTTP methods (GET, POST, etc.).
- **Parameters**: Input data for API requests.
- **Request/Response Bodies**: Structure of data sent and received.
- **Schemas**: Data models used in requests and responses.
- **Security Schemes**: Authentication and authorization methods.
- **Components**: Reusable objects across the API.

## Best Practices

### Operation Naming Conventions
Use the following prefixes for operation IDs:
| Operation Type | Name | HTTP Method | Example |
|----------------|------|-------------|---------|
| Get single     | `get{Resource}` | GET | `getUser` |
| List multiple   | `list{Resources}` | GET | `listUsers` |
| Search with filters | `search{Resources}` | POST | `searchUsers` |
| Create new     | `create{Resource}` | POST | `createUser` |
| Update existing | `update{Resource}` | PUT/PATCH | `updateUser` |
| Delete resource | `delete{Resource}` | DELETE | `deleteUser` |

### Descriptions
- Always derive operation descriptions from official vendor documentation.
- If descriptions are unavailable, create minimal factual descriptions.

### Schema Organization
- Prioritize model definitions from official documentation.
- Include all documented fields in schemas.

### Parameter Naming
- Use operation-specific names for shared parameters to avoid conflicts.

## Example OpenAPI Specification

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
      operationId: listPosts
      summary: List all posts
      description: Returns a paginated list of blog posts.
      parameters:
        - name: page
          in: query
          description: Page number
          required: false
          schema:
            type: integer
            minimum: 1
            default: 1
        - name: limit
          in: query
          description: Items per page
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
        '400':
          description: Bad request
```