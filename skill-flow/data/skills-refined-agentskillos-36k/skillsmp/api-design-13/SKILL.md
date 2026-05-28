---
name: api-design
description: Design a RESTful API endpoint
---

# API Design

Help me design a RESTful API:

## Requirements

1. **Resource**: What entity is this for?
2. **Operations**: What actions are needed (CRUD, other)?
3. **Relationships**: How does it relate to other resources?
4. **Users**: Who will call this API?

## Endpoint Design

For each operation, define:

### URL Structure

- Resource path (nouns, plural)
- Parameter placement
- Query parameters for filtering/sorting

### HTTP Methods

- GET for reads
- POST for creates
- PUT/PATCH for updates
- DELETE for removes

### Request Format

- Request body schema
- Required vs optional fields
- Validation rules

### Response Format

- Success response schema
- Pagination structure (if list)
- Error response format

### Status Codes

- 2xx for success
- 4xx for client errors
- 5xx for server errors

## Documentation

Generate OpenAPI/Swagger spec including:

- Endpoint descriptions
- Parameter definitions
- Schema definitions
- Example requests/responses

## Best Practices Check

Verify the design follows:

- RESTful conventions
- Consistent naming
- Proper status codes
- Security considerations
