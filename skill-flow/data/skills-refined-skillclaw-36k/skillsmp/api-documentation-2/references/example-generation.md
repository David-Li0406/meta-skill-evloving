# Example Generation

Patterns for creating realistic and helpful API examples.

## Example Quality Guidelines

### Realistic Data

```yaml
# BAD - Placeholder data
example:
  name: "string"
  email: "string"
  id: 0

# GOOD - Realistic data
example:
  name: "Jane Smith"
  email: "jane.smith@example.com"
  id: "usr_7k9m2n4p5q"
```

### Consistent IDs

Use prefixed IDs that indicate the resource type:

```yaml
# User ID
id: "usr_7k9m2n4p5q"

# Order ID
id: "ord_1a2b3c4d5e"

# Product ID
id: "prod_xyz123abc"

# Transaction ID
id: "txn_9f8e7d6c5b"
```

### Realistic Timestamps

Use recent, specific timestamps:

```yaml
# BAD
created_at: "2020-01-01T00:00:00Z"

# GOOD
created_at: "2024-01-15T10:30:45Z"
updated_at: "2024-01-15T14:22:18Z"
```

## Multiple Examples

### Showing Different Scenarios

```yaml
examples:
  basic:
    summary: Basic order
    description: A simple order with one item
    value:
      items:
        - product_id: "prod_headphones"
          quantity: 1
      total: 149.99

  multipleItems:
    summary: Order with multiple items
    description: Order containing several different products
    value:
      items:
        - product_id: "prod_headphones"
          quantity: 1
        - product_id: "prod_case"
          quantity: 2
        - product_id: "prod_cable"
          quantity: 1
      total: 189.97

  withDiscount:
    summary: Order with discount
    description: Order with a promotional discount applied
    value:
      items:
        - product_id: "prod_headphones"
          quantity: 1
      discount_code: "SAVE20"
      discount_amount: 30.00
      total: 119.99

  giftOrder:
    summary: Gift order
    description: Order shipped as a gift with custom message
    value:
      items:
        - product_id: "prod_headphones"
          quantity: 1
      is_gift: true
      gift_message: "Happy Birthday!"
      gift_wrapping: true
      total: 159.99
```

### Error Examples

```yaml
responses:
  '422':
    description: Validation error
    content:
      application/json:
        examples:
          missingRequired:
            summary: Missing required field
            value:
              error: "validation_error"
              message: "Request validation failed"
              details:
                - field: "email"
                  message: "Email is required"

          invalidFormat:
            summary: Invalid field format
            value:
              error: "validation_error"
              message: "Request validation failed"
              details:
                - field: "email"
                  message: "Must be a valid email address"
                - field: "phone"
                  message: "Must be a valid phone number"

          businessRule:
            summary: Business rule violation
            value:
              error: "validation_error"
              message: "Request validation failed"
              details:
                - field: "quantity"
                  message: "Cannot exceed available stock (50)"
```

## Code Examples

### cURL Examples

```markdown
#### Create Order

```bash
curl -X POST https://api.example.com/v1/orders \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {"product_id": "prod_headphones", "quantity": 1}
    ],
    "shipping_address_id": "addr_home"
  }'
```

#### List Orders with Filtering

```bash
curl -G https://api.example.com/v1/orders \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." \
  -d "status=pending" \
  -d "created_after=2024-01-01" \
  -d "per_page=50"
```
```

### Language-Specific Examples

```markdown
#### Python

```python
import requests

# Create order
response = requests.post(
    "https://api.example.com/v1/orders",
    headers={
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    },
    json={
        "items": [
            {"product_id": "prod_headphones", "quantity": 1}
        ],
        "shipping_address_id": "addr_home"
    }
)

order = response.json()
print(f"Created order: {order['id']}")
```

#### JavaScript

```javascript
const response = await fetch('https://api.example.com/v1/orders', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${apiToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    items: [
      { product_id: 'prod_headphones', quantity: 1 }
    ],
    shipping_address_id: 'addr_home'
  })
});

const order = await response.json();
console.log(`Created order: ${order.id}`);
```

#### Ruby

```ruby
require 'httparty'

response = HTTParty.post(
  'https://api.example.com/v1/orders',
  headers: {
    'Authorization' => "Bearer #{api_token}",
    'Content-Type' => 'application/json'
  },
  body: {
    items: [
      { product_id: 'prod_headphones', quantity: 1 }
    ],
    shipping_address_id: 'addr_home'
  }.to_json
)

order = response.parsed_response
puts "Created order: #{order['id']}"
```
```

## Response Examples

### Successful Response

```yaml
responses:
  '201':
    description: Order created successfully
    content:
      application/json:
        example:
          id: "ord_1a2b3c4d5e"
          status: "pending"
          items:
            - id: "item_abc123"
              product_id: "prod_headphones"
              product_name: "Wireless Headphones Pro"
              quantity: 1
              unit_price: 149.99
              total: 149.99
          subtotal: 149.99
          tax: 12.00
          shipping: 5.99
          total: 167.98
          shipping_address:
            name: "Jane Smith"
            line1: "123 Main Street"
            city: "San Francisco"
            state: "CA"
            postal_code: "94102"
            country: "US"
          created_at: "2024-01-15T10:30:45Z"
          estimated_delivery: "2024-01-20"
```

### List Response with Pagination

```yaml
responses:
  '200':
    description: List of orders
    content:
      application/json:
        example:
          data:
            - id: "ord_1a2b3c4d5e"
              status: "delivered"
              total: 167.98
              created_at: "2024-01-15T10:30:45Z"
            - id: "ord_2b3c4d5e6f"
              status: "shipped"
              total: 89.99
              created_at: "2024-01-14T15:22:30Z"
            - id: "ord_3c4d5e6f7g"
              status: "pending"
              total: 249.00
              created_at: "2024-01-14T09:15:00Z"
          meta:
            total: 47
            page: 1
            per_page: 20
            total_pages: 3
          links:
            self: "/v1/orders?page=1&per_page=20"
            next: "/v1/orders?page=2&per_page=20"
            last: "/v1/orders?page=3&per_page=20"
```

## Webhook Examples

```yaml
webhooks:
  orderCreated:
    post:
      summary: Order created event
      description: Sent when a new order is placed
      requestBody:
        content:
          application/json:
            example:
              event: "order.created"
              timestamp: "2024-01-15T10:30:45Z"
              data:
                id: "ord_1a2b3c4d5e"
                status: "pending"
                total: 167.98
                customer_id: "usr_7k9m2n4p5q"

  orderShipped:
    post:
      summary: Order shipped event
      requestBody:
        content:
          application/json:
            example:
              event: "order.shipped"
              timestamp: "2024-01-17T14:22:18Z"
              data:
                id: "ord_1a2b3c4d5e"
                status: "shipped"
                tracking_number: "1Z999AA10123456784"
                carrier: "UPS"
                estimated_delivery: "2024-01-20"
```

## Testing Examples

Include examples for testing:

```markdown
### Test Mode

Use test API keys to simulate various scenarios:

#### Test Cards
| Number | Scenario |
|--------|----------|
| 4242424242424242 | Successful payment |
| 4000000000000002 | Card declined |
| 4000000000009995 | Insufficient funds |

#### Test Order IDs
| ID | Scenario |
|----|----------|
| ord_test_success | Successfully completes |
| ord_test_cancel | Cancels after 5 seconds |
| ord_test_refund | Refunds after 10 seconds |
```
