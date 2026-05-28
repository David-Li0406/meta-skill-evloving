# OpenAPI Specification Reference

## OpenAPI 3.0 Document Structure

### Root Object (OpenAPI Object)

**Required Fields:**
- `openapi`: Version string (e.g., "3.0.3", "3.1.0")
- `info`: API metadata
- `paths`: Available endpoints and operations

**Optional Fields:**
- `servers`: Target server URLs
- `components`: Reusable schemas and objects
- `security`: API-wide security requirements
- `tags`: Operation grouping
- `externalDocs`: Additional documentation

### Info Object

```yaml
info:
  title: API Title
  version: 1.0.0
  description: API description
  contact:
    name: API Support
    email: support@example.com
  license:
    name: Apache 2.0
```

### Servers Object

```yaml
servers:
  - url: https://api.example.com/v1
    description: Production server
  - url: https://staging.example.com/v1
    description: Staging server
    variables:
      port:
        default: '443'
```

### Paths Object

Maps endpoint paths to operations:

```yaml
paths:
  /users:
    get:
      summary: List users
      operationId: listUsers
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
      responses:
        '200':
          description: Success
    post:
      summary: Create user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/User'
```

### Operation Object

Each HTTP method (get, post, put, delete, patch, etc.) contains:

- `operationId`: Unique identifier
- `summary`: Short description
- `description`: Detailed description
- `tags`: Operation categorization
- `parameters`: Query, path, header, cookie parameters
- `requestBody`: Request payload specification
- `responses`: Expected responses by status code
- `security`: Authentication requirements
- `deprecated`: Boolean flag

### Parameter Object

```yaml
parameters:
  - name: userId
    in: path           # path, query, header, cookie
    required: true
    schema:
      type: string
    description: User identifier
  - name: limit
    in: query
    schema:
      type: integer
      default: 20
```

**Parameter Locations:**
- `path`: URL path parameter (e.g., `/users/{userId}`)
- `query`: Query string parameter (e.g., `?limit=10`)
- `header`: HTTP header
- `cookie`: Cookie value

### Request Body Object

```yaml
requestBody:
  required: true
  content:
    application/json:
      schema:
        $ref: '#/components/schemas/User'
      examples:
        userExample:
          value:
            name: John Doe
            email: john@example.com
    application/xml:
      schema:
        $ref: '#/components/schemas/User'
```

### Responses Object

```yaml
responses:
  '200':
    description: Successful operation
    content:
      application/json:
        schema:
          type: array
          items:
            $ref: '#/components/schemas/User'
  '400':
    description: Bad request
  '401':
    description: Unauthorized
  '404':
    description: Not found
```

### Components Object

Reusable definitions:

```yaml
components:
  schemas:
    User:
      type: object
      required:
        - name
        - email
      properties:
        id:
          type: integer
          format: int64
        name:
          type: string
        email:
          type: string
          format: email
        tags:
          type: array
          items:
            type: string
    Error:
      type: object
      properties:
        code:
          type: integer
        message:
          type: string

  parameters:
    limitParam:
      name: limit
      in: query
      schema:
        type: integer

  requestBodies:
    UserBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/User'

  responses:
    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

  securitySchemes:
    api_key:
      type: apiKey
      name: api_key
      in: header
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
    oauth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: https://example.com/oauth/authorize
          tokenUrl: https://example.com/oauth/token
          scopes:
            read: Read access
            write: Write access
```

## Security Schemes

### API Key

```yaml
securitySchemes:
  ApiKeyAuth:
    type: apiKey
    in: header        # header, query, or cookie
    name: X-API-Key
```

### HTTP Authentication

```yaml
securitySchemes:
  BasicAuth:
    type: http
    scheme: basic

  BearerAuth:
    type: http
    scheme: bearer
    bearerFormat: JWT
```

### OAuth 2.0

```yaml
securitySchemes:
  OAuth2:
    type: oauth2
    flows:
      authorizationCode:
        authorizationUrl: https://example.com/oauth/authorize
        tokenUrl: https://example.com/oauth/token
        scopes:
          read: Read access
          write: Write access
      clientCredentials:
        tokenUrl: https://example.com/oauth/token
        scopes:
          admin: Admin access
```

### OpenID Connect

```yaml
securitySchemes:
  OpenID:
    type: openIdConnect
    openIdConnectUrl: https://example.com/.well-known/openid-configuration
```

## Data Types and Formats

**Types:**
- `string`: Text values
- `number`: Floating-point numbers (formats: float, double)
- `integer`: Whole numbers (formats: int32, int64)
- `boolean`: true/false
- `array`: Ordered list
- `object`: Key-value pairs

**String Formats:**
- `date`: ISO 8601 date (2023-01-31)
- `date-time`: ISO 8601 datetime (2023-01-31T10:00:00Z)
- `password`: Obscured input
- `byte`: Base64 encoded
- `binary`: Binary data
- `email`: Email address
- `uuid`: UUID format
- `uri`: URI reference

## Schema Object Features

### Required Fields

```yaml
schema:
  type: object
  required:
    - name
    - email
  properties:
    name:
      type: string
    email:
      type: string
```

### Nested Objects

```yaml
schema:
  type: object
  properties:
    user:
      type: object
      properties:
        name:
          type: string
        address:
          type: object
          properties:
            street:
              type: string
            city:
              type: string
```

### Arrays

```yaml
schema:
  type: array
  items:
    type: string
# or
schema:
  type: array
  items:
    $ref: '#/components/schemas/User'
```

### Enumerations

```yaml
schema:
  type: string
  enum:
    - pending
    - approved
    - rejected
```

### Nullable Values

```yaml
# OpenAPI 3.0
schema:
  type: string
  nullable: true

# OpenAPI 3.1
schema:
  type: ['string', 'null']
```

## References ($ref)

Reference components or external files:

```yaml
# Internal reference
schema:
  $ref: '#/components/schemas/User'

# External reference
schema:
  $ref: './common.yaml#/components/schemas/Error'

# Parameter reference
parameters:
  - $ref: '#/components/parameters/limitParam'
```
