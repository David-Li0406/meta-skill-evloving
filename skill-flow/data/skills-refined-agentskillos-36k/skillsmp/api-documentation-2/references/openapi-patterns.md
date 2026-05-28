# OpenAPI Patterns

Patterns for creating well-structured OpenAPI specifications.

## File Organization

### Single File (Small APIs)

```yaml
# openapi.yaml
openapi: 3.0.0
info:
  title: My API
  version: 1.0.0

paths:
  # All paths here

components:
  schemas:
    # All schemas here
  securitySchemes:
    # All auth schemes here
```

### Multi-File (Large APIs)

```
api/
├── openapi.yaml        # Main file with $ref to others
├── paths/
│   ├── orders.yaml
│   ├── users.yaml
│   └── products.yaml
├── schemas/
│   ├── order.yaml
│   ├── user.yaml
│   └── product.yaml
└── examples/
    ├── order-examples.yaml
    └── user-examples.yaml
```

Main file with references:

```yaml
# openapi.yaml
openapi: 3.0.0
info:
  title: My API
  version: 1.0.0

paths:
  /orders:
    $ref: './paths/orders.yaml#/orders'
  /users:
    $ref: './paths/users.yaml#/users'

components:
  schemas:
    Order:
      $ref: './schemas/order.yaml#/Order'
```

## Path Patterns

### RESTful Resource Paths

```yaml
paths:
  /orders:
    get:
      summary: List orders
      operationId: listOrders
    post:
      summary: Create order
      operationId: createOrder

  /orders/{orderId}:
    get:
      summary: Get order
      operationId: getOrder
    put:
      summary: Update order
      operationId: updateOrder
    delete:
      summary: Delete order
      operationId: deleteOrder

  /orders/{orderId}/items:
    get:
      summary: List order items
      operationId: listOrderItems
    post:
      summary: Add item to order
      operationId: addOrderItem
```

### Path Parameters

```yaml
parameters:
  - name: orderId
    in: path
    required: true
    description: Unique order identifier
    schema:
      type: string
      pattern: '^ord_[a-zA-Z0-9]{10}$'
    example: "ord_1234567890"
```

### Query Parameters

```yaml
parameters:
  - name: page
    in: query
    description: Page number for pagination
    schema:
      type: integer
      minimum: 1
      default: 1
    example: 1

  - name: per_page
    in: query
    description: Items per page
    schema:
      type: integer
      minimum: 1
      maximum: 100
      default: 20
    example: 20

  - name: status
    in: query
    description: Filter by status
    schema:
      type: string
      enum: [pending, confirmed, shipped, delivered]
    example: "pending"

  - name: sort
    in: query
    description: Sort field and direction
    schema:
      type: string
      pattern: '^[a-z_]+:(asc|desc)$'
    example: "created_at:desc"
```

## Request Body Patterns

### JSON Request

```yaml
requestBody:
  required: true
  content:
    application/json:
      schema:
        $ref: '#/components/schemas/CreateOrderRequest'
      examples:
        basic:
          summary: Basic order
          value:
            items:
              - product_id: "prod_abc"
                quantity: 1
        withDiscount:
          summary: Order with discount code
          value:
            items:
              - product_id: "prod_abc"
                quantity: 2
            discount_code: "SAVE10"
```

### File Upload

```yaml
requestBody:
  content:
    multipart/form-data:
      schema:
        type: object
        properties:
          file:
            type: string
            format: binary
          description:
            type: string
        required:
          - file
```

## Response Patterns

### Success Response

```yaml
responses:
  '200':
    description: Successful response
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/Order'
    headers:
      X-Request-Id:
        description: Request tracking ID
        schema:
          type: string
```

### Paginated Response

```yaml
responses:
  '200':
    description: List of orders
    content:
      application/json:
        schema:
          type: object
          properties:
            data:
              type: array
              items:
                $ref: '#/components/schemas/Order'
            meta:
              $ref: '#/components/schemas/PaginationMeta'
            links:
              $ref: '#/components/schemas/PaginationLinks'
```

### Error Responses

```yaml
responses:
  '400':
    description: Bad request
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/Error'
        example:
          error: "bad_request"
          message: "Invalid JSON in request body"

  '401':
    description: Unauthorized
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/Error'
        example:
          error: "unauthorized"
          message: "Authentication required"

  '422':
    description: Validation error
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/ValidationError'
        example:
          error: "validation_error"
          message: "Request validation failed"
          details:
            - field: "email"
              message: "Must be a valid email"
            - field: "items"
              message: "Must contain at least one item"
```

## Schema Patterns

### Basic Object

```yaml
Order:
  type: object
  required:
    - id
    - status
    - items
  properties:
    id:
      type: string
      description: Unique order identifier
      example: "ord_1234567890"
    status:
      type: string
      enum: [pending, confirmed, shipped, delivered, cancelled]
      description: Current order status
      example: "pending"
    items:
      type: array
      items:
        $ref: '#/components/schemas/OrderItem'
    created_at:
      type: string
      format: date-time
      description: Order creation timestamp
      example: "2024-01-15T10:30:00Z"
```

### Inheritance (allOf)

```yaml
CreateOrderRequest:
  allOf:
    - $ref: '#/components/schemas/OrderBase'
    - type: object
      required:
        - items
      properties:
        discount_code:
          type: string
          description: Optional discount code

OrderResponse:
  allOf:
    - $ref: '#/components/schemas/OrderBase'
    - type: object
      required:
        - id
        - created_at
      properties:
        id:
          type: string
        created_at:
          type: string
          format: date-time
```

### Polymorphism (oneOf)

```yaml
PaymentMethod:
  oneOf:
    - $ref: '#/components/schemas/CreditCard'
    - $ref: '#/components/schemas/BankTransfer'
    - $ref: '#/components/schemas/PayPal'
  discriminator:
    propertyName: type
    mapping:
      credit_card: '#/components/schemas/CreditCard'
      bank_transfer: '#/components/schemas/BankTransfer'
      paypal: '#/components/schemas/PayPal'
```

## Security Patterns

### Bearer Token

```yaml
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: JWT token from /auth/login

security:
  - bearerAuth: []

paths:
  /public/health:
    get:
      security: []  # No auth required
      summary: Health check
```

### API Key

```yaml
components:
  securitySchemes:
    apiKey:
      type: apiKey
      in: header
      name: X-API-Key
      description: API key from dashboard
```

### OAuth2

```yaml
components:
  securitySchemes:
    oauth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: https://auth.example.com/authorize
          tokenUrl: https://auth.example.com/token
          scopes:
            read:orders: Read orders
            write:orders: Create and modify orders
```
