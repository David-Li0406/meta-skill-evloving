---
name: api-documentation
description: Use this skill when creating comprehensive API documentation for REST or GraphQL APIs, utilizing OpenAPI/Swagger specifications.
---

# API Documentation

## When to use this skill

- **API Development**: When adding new endpoints.
- **Public Release**: For launching public APIs.
- **Team Collaboration**: To define frontend-backend interfaces.

## Instructions

### Step 1: OpenAPI (Swagger) Specification

Create an OpenAPI specification in YAML format:

```yaml
openapi: 3.0.0
info:
  title: <API Title>
  version: <API Version>
  description: <API Description>
servers:
  - url: <API Base URL>
paths:
  /<endpoint>:
    get:
      summary: <Brief Description>
      operationId: <Unique Identifier>
      tags:
        - <Tag>
      parameters: []
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/<Schema>'
components:
  schemas:
    <Schema>:
      type: object
      properties:
        <Property Name>:
          type: <Type>
```

### Step 2: Endpoint Documentation

For each endpoint, document the following:

- **Required Fields**:
  - **summary**: Brief description.
  - **operationId**: Unique identifier.
  - **description**: Detailed explanation.
  - **tags**: For grouping.
  - **responses**: All possible responses.

- **Recommended Fields**:
  - **parameters**: All parameters with details.
  - **requestBody**: For POST/PUT/PATCH requests.
  - **security**: Authentication requirements.

### Step 3: Authentication Documentation

Document authentication requirements:

```yaml
security:
  - bearerAuth: []

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: Use your JWT token from /auth/login
```

### Step 4: Error Responses

Standard error format:

```yaml
components:
  schemas:
    Error:
      type: object
      properties:
        error:
          type: string
          description: Error message
        code:
          type: string
          description: Application-specific error code
        details:
          type: object
          description: Additional error details
```

Common HTTP status codes:
- **200**: Success
- **201**: Created
- **204**: No Content
- **400**: Bad Request
- **401**: Unauthorized
- **403**: Forbidden
- **404**: Not Found
- **409**: Conflict
- **422**: Unprocessable Entity
- **500**: Internal Server Error

## Best Practices

1. **Use References**: For shared schemas.
2. **Add Descriptions**: To all properties.
3. **Specify Format**: For strings (email, uuid, date-time).
4. **Add Examples**: For complex schemas.
5. **Mark Required Fields**: Clearly indicate required fields in schemas.

## References

- [OpenAPI Specification](https://swagger.io/specification/)
- [Swagger UI](https://swagger.io/tools/swagger-ui/)
- [Redoc](https://redocly.com/)

## Metadata

### Version
- **Current Version**: 1.0.0
- **Last Updated**: <Last Update Date>
- **Compatible Platforms**: Claude, ChatGPT, Gemini

### Tags
`#API-documentation` `#OpenAPI` `#Swagger` `#REST` `#GraphQL` `#developer-docs`

## Examples

### Example 1: Basic Usage
<!-- Add example content here -->

### Example 2: Advanced Usage
<!-- Add advanced example content here -->