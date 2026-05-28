# REST API Documentation - E-commerce Platform

Complete REST API documentation for an e-commerce platform with authentication, product catalog, orders, and payments.

## 📝 Prompt

```
Create comprehensive REST API documentation for an e-commerce platform:

Context:
- Platform: Node.js/Express backend
- Database: PostgreSQL
- Authentication: JWT tokens
- Payment: Stripe integration

Include documentation for:
- Authentication endpoints (login, register, token refresh)
- Product endpoints (CRUD operations, search, filtering)
- Cart management
- Order processing
- Payment integration
- User profile management

For each endpoint include:
- HTTP method and path
- Description
- Authentication requirements
- Request parameters/body
- Response format with examples
- Error codes and messages
- Rate limiting info
```

## 📚 API Documentation

### Base URL
```
Production: https://api.example-commerce.com/v1
Staging: https://staging-api.example-commerce.com/v1
Development: http://localhost:3000/v1
```

### Authentication

All authenticated endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

---

## 🔐 Authentication Endpoints

### Register New User

**POST** `/auth/register`

Create a new user account.

**Authentication:** None required

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "firstName": "John",
  "lastName": "Doe",
  "phone": "+1234567890"
}
```

**Validation Rules:**
- `email`: Valid email format, unique
- `password`: Minimum 8 characters, must include uppercase, lowercase, number, and special character
- `firstName`: 2-50 characters
- `lastName`: 2-50 characters
- `phone`: Valid phone format (optional)

**Success Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "usr_1a2b3c4d5e6f",
      "email": "user@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "phone": "+1234567890",
      "createdAt": "2026-01-22T10:30:00Z"
    },
    "tokens": {
      "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "expiresIn": 3600
    }
  }
}
```

**Error Responses:**
```json
// 400 Bad Request - Validation Error
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      {
        "field": "email",
        "message": "Email already exists"
      },
      {
        "field": "password",
        "message": "Password must be at least 8 characters"
      }
    ]
  }
}

// 429 Too Many Requests
{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many registration attempts. Please try again in 15 minutes."
  }
}
```

**Rate Limit:** 5 requests per 15 minutes per IP

---

### Login

**POST** `/auth/login`

Authenticate user and receive access tokens.

**Authentication:** None required

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "usr_1a2b3c4d5e6f",
      "email": "user@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "role": "customer"
    },
    "tokens": {
      "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "expiresIn": 3600
    }
  }
}
```

**Error Responses:**
```json
// 401 Unauthorized
{
  "success": false,
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Invalid email or password"
  }
}

// 423 Locked
{
  "success": false,
  "error": {
    "code": "ACCOUNT_LOCKED",
    "message": "Account locked due to too many failed login attempts. Try again in 30 minutes."
  }
}
```

**Rate Limit:** 10 requests per 15 minutes per IP

---

### Refresh Token

**POST** `/auth/refresh`

Get a new access token using a refresh token.

**Authentication:** None required

**Request Body:**
```json
{
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expiresIn": 3600
  }
}
```

**Error Response:**
```json
// 401 Unauthorized
{
  "success": false,
  "error": {
    "code": "INVALID_TOKEN",
    "message": "Invalid or expired refresh token"
  }
}
```

---

## 🛍️ Product Endpoints

### Get All Products

**GET** `/products`

Retrieve a paginated list of products with optional filtering and sorting.

**Authentication:** Optional (public endpoint, but authenticated users see personalized data)

**Query Parameters:**
```
?page=1              // Page number (default: 1)
&limit=20            // Items per page (default: 20, max: 100)
&category=electronics // Filter by category slug
&minPrice=50         // Minimum price filter
&maxPrice=500        // Maximum price filter
&search=laptop       // Search in name and description
&sort=price          // Sort by: price, name, createdAt, popularity
&order=asc           // Order: asc, desc
&inStock=true        // Filter by stock availability
```

**Example Request:**
```bash
GET /products?page=1&limit=10&category=electronics&sort=price&order=asc
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "products": [
      {
        "id": "prod_1a2b3c4d",
        "name": "Wireless Bluetooth Headphones",
        "slug": "wireless-bluetooth-headphones",
        "description": "Premium noise-canceling headphones with 30-hour battery life",
        "price": 149.99,
        "compareAtPrice": 199.99,
        "currency": "USD",
        "category": {
          "id": "cat_electronics",
          "name": "Electronics",
          "slug": "electronics"
        },
        "images": [
          {
            "id": "img_1",
            "url": "https://cdn.example.com/products/headphones-main.jpg",
            "alt": "Black wireless headphones",
            "order": 1
          }
        ],
        "inventory": {
          "inStock": true,
          "quantity": 45,
          "sku": "WBH-001-BLK"
        },
        "ratings": {
          "average": 4.7,
          "count": 328
        },
        "createdAt": "2025-12-15T08:00:00Z",
        "updatedAt": "2026-01-20T14:30:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "totalPages": 15,
      "totalItems": 147,
      "hasNextPage": true,
      "hasPreviousPage": false
    }
  }
}
```

**Rate Limit:** 100 requests per minute

---

### Get Product by ID

**GET** `/products/:id`

Retrieve detailed information about a specific product.

**Authentication:** Optional

**Path Parameters:**
- `id`: Product ID (e.g., `prod_1a2b3c4d`)

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "product": {
      "id": "prod_1a2b3c4d",
      "name": "Wireless Bluetooth Headphones",
      "slug": "wireless-bluetooth-headphones",
      "description": "Premium noise-canceling headphones with 30-hour battery life",
      "fullDescription": "Experience crystal-clear audio with our premium wireless headphones...",
      "price": 149.99,
      "compareAtPrice": 199.99,
      "currency": "USD",
      "category": {
        "id": "cat_electronics",
        "name": "Electronics",
        "slug": "electronics"
      },
      "images": [
        {
          "id": "img_1",
          "url": "https://cdn.example.com/products/headphones-main.jpg",
          "alt": "Black wireless headphones",
          "order": 1
        }
      ],
      "specifications": {
        "brand": "AudioTech",
        "color": "Black",
        "weight": "250g",
        "batteryLife": "30 hours",
        "warranty": "2 years"
      },
      "inventory": {
        "inStock": true,
        "quantity": 45,
        "sku": "WBH-001-BLK",
        "lowStockThreshold": 10
      },
      "ratings": {
        "average": 4.7,
        "count": 328,
        "distribution": {
          "5": 220,
          "4": 85,
          "3": 15,
          "2": 5,
          "1": 3
        }
      },
      "reviews": [
        {
          "id": "rev_1",
          "userId": "usr_abc123",
          "userName": "Sarah M.",
          "rating": 5,
          "comment": "Best headphones I've ever owned!",
          "createdAt": "2026-01-15T10:00:00Z"
        }
      ],
      "relatedProducts": ["prod_2b3c4d5e", "prod_3c4d5e6f"],
      "createdAt": "2025-12-15T08:00:00Z",
      "updatedAt": "2026-01-20T14:30:00Z"
    }
  }
}
```

**Error Response:**
```json
// 404 Not Found
{
  "success": false,
  "error": {
    "code": "PRODUCT_NOT_FOUND",
    "message": "Product with ID 'prod_1a2b3c4d' not found"
  }
}
```

---

### Create Product (Admin Only)

**POST** `/products`

Create a new product in the catalog.

**Authentication:** Required (Admin role)

**Request Body:**
```json
{
  "name": "Smart Watch Pro",
  "slug": "smart-watch-pro",
  "description": "Advanced fitness tracking smartwatch",
  "fullDescription": "Track your health and fitness goals...",
  "price": 299.99,
  "compareAtPrice": 349.99,
  "categoryId": "cat_electronics",
  "images": [
    {
      "url": "https://cdn.example.com/products/watch-main.jpg",
      "alt": "Smart watch front view",
      "order": 1
    }
  ],
  "specifications": {
    "brand": "TechWear",
    "color": "Silver",
    "waterproof": "IP68",
    "batteryLife": "7 days"
  },
  "inventory": {
    "sku": "SWP-001-SLV",
    "quantity": 100
  }
}
```

**Success Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "product": {
      "id": "prod_new123",
      "name": "Smart Watch Pro",
      "slug": "smart-watch-pro",
      "price": 299.99,
      "createdAt": "2026-01-22T10:30:00Z"
    }
  }
}
```

**Error Response:**
```json
// 403 Forbidden
{
  "success": false,
  "error": {
    "code": "INSUFFICIENT_PERMISSIONS",
    "message": "Admin role required to create products"
  }
}
```

**Rate Limit:** 20 requests per hour (admin users)

---

## 🛒 Cart Endpoints

### Get Cart

**GET** `/cart`

Retrieve the current user's shopping cart.

**Authentication:** Required

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "cart": {
      "id": "cart_usr_1a2b3c4d",
      "userId": "usr_1a2b3c4d",
      "items": [
        {
          "id": "item_1",
          "product": {
            "id": "prod_1a2b3c4d",
            "name": "Wireless Bluetooth Headphones",
            "price": 149.99,
            "image": "https://cdn.example.com/products/headphones-thumb.jpg"
          },
          "quantity": 2,
          "subtotal": 299.98
        }
      ],
      "summary": {
        "subtotal": 299.98,
        "tax": 24.00,
        "shipping": 9.99,
        "discount": 0,
        "total": 333.97
      },
      "updatedAt": "2026-01-22T10:15:00Z"
    }
  }
}
```

---

### Add Item to Cart

**POST** `/cart/items`

Add a product to the shopping cart.

**Authentication:** Required

**Request Body:**
```json
{
  "productId": "prod_1a2b3c4d",
  "quantity": 2
}
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "cart": {
      "id": "cart_usr_1a2b3c4d",
      "items": [
        {
          "id": "item_1",
          "product": {
            "id": "prod_1a2b3c4d",
            "name": "Wireless Bluetooth Headphones",
            "price": 149.99
          },
          "quantity": 2,
          "subtotal": 299.98
        }
      ],
      "summary": {
        "subtotal": 299.98,
        "total": 333.97
      }
    }
  }
}
```

**Error Response:**
```json
// 400 Bad Request - Insufficient Stock
{
  "success": false,
  "error": {
    "code": "INSUFFICIENT_STOCK",
    "message": "Only 1 unit available in stock",
    "details": {
      "productId": "prod_1a2b3c4d",
      "requestedQuantity": 2,
      "availableQuantity": 1
    }
  }
}
```

---

## 📦 Order Endpoints

### Create Order

**POST** `/orders`

Create a new order from the current cart.

**Authentication:** Required

**Request Body:**
```json
{
  "shippingAddress": {
    "firstName": "John",
    "lastName": "Doe",
    "address1": "123 Main St",
    "address2": "Apt 4B",
    "city": "New York",
    "state": "NY",
    "postalCode": "10001",
    "country": "US",
    "phone": "+1234567890"
  },
  "billingAddress": {
    "sameAsShipping": true
  },
  "paymentMethodId": "pm_stripe_token_123"
}
```

**Success Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "order": {
      "id": "ord_1a2b3c4d",
      "orderNumber": "ORD-2026-001234",
      "status": "processing",
      "items": [
        {
          "productId": "prod_1a2b3c4d",
          "name": "Wireless Bluetooth Headphones",
          "quantity": 2,
          "price": 149.99,
          "subtotal": 299.98
        }
      ],
      "summary": {
        "subtotal": 299.98,
        "tax": 24.00,
        "shipping": 9.99,
        "total": 333.97
      },
      "payment": {
        "status": "paid",
        "method": "card",
        "last4": "4242"
      },
      "createdAt": "2026-01-22T10:30:00Z",
      "estimatedDelivery": "2026-01-27T00:00:00Z"
    }
  }
}
```

---

### Get Orders

**GET** `/orders`

Retrieve user's order history.

**Authentication:** Required

**Query Parameters:**
```
?page=1
&limit=10
&status=delivered  // Filter by: pending, processing, shipped, delivered, cancelled
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "orders": [
      {
        "id": "ord_1a2b3c4d",
        "orderNumber": "ORD-2026-001234",
        "status": "delivered",
        "total": 333.97,
        "itemCount": 2,
        "createdAt": "2026-01-15T10:30:00Z",
        "deliveredAt": "2026-01-20T14:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "totalPages": 3,
      "totalItems": 25
    }
  }
}
```

---

## 💳 Payment Endpoints

### Create Payment Intent

**POST** `/payments/intent`

Create a payment intent for Stripe checkout.

**Authentication:** Required

**Request Body:**
```json
{
  "amount": 33397,  // Amount in cents
  "currency": "usd"
}
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "clientSecret": "pi_1234567890_secret_abcdefgh",
    "publishableKey": "pk_test_1234567890"
  }
}
```

---

## 👤 User Profile Endpoints

### Get Profile

**GET** `/users/profile`

Get the authenticated user's profile information.

**Authentication:** Required

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "usr_1a2b3c4d",
      "email": "user@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "phone": "+1234567890",
      "addresses": [
        {
          "id": "addr_1",
          "type": "shipping",
          "address1": "123 Main St",
          "city": "New York",
          "state": "NY",
          "postalCode": "10001",
          "country": "US",
          "isDefault": true
        }
      ],
      "createdAt": "2025-06-15T10:00:00Z"
    }
  }
}
```

---

### Update Profile

**PATCH** `/users/profile`

Update user profile information.

**Authentication:** Required

**Request Body:**
```json
{
  "firstName": "John",
  "lastName": "Smith",
  "phone": "+1987654321"
}
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "usr_1a2b3c4d",
      "email": "user@example.com",
      "firstName": "John",
      "lastName": "Smith",
      "phone": "+1987654321",
      "updatedAt": "2026-01-22T10:45:00Z"
    }
  }
}
```

---

## ⚠️ Error Codes Reference

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Request validation failed |
| `UNAUTHORIZED` | 401 | Authentication required |
| `INVALID_CREDENTIALS` | 401 | Invalid email or password |
| `INVALID_TOKEN` | 401 | Invalid or expired token |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `INSUFFICIENT_PERMISSIONS` | 403 | Admin role required |
| `NOT_FOUND` | 404 | Resource not found |
| `PRODUCT_NOT_FOUND` | 404 | Product doesn't exist |
| `CONFLICT` | 409 | Resource already exists |
| `INSUFFICIENT_STOCK` | 400 | Not enough inventory |
| `PAYMENT_FAILED` | 402 | Payment processing failed |
| `ACCOUNT_LOCKED` | 423 | Too many failed attempts |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Server error |

---

## 🔒 Authentication & Security

### JWT Token Structure
```json
{
  "userId": "usr_1a2b3c4d",
  "email": "user@example.com",
  "role": "customer",
  "iat": 1737540000,
  "exp": 1737543600
}
```

### Token Expiration
- **Access Token**: 1 hour
- **Refresh Token**: 30 days

### Security Best Practices
1. Always use HTTPS in production
2. Store tokens securely (HTTPOnly cookies or secure storage)
3. Implement CSRF protection for cookie-based auth
4. Never expose sensitive data in URLs
5. Validate all input on the server side
6. Use rate limiting to prevent abuse

---

## 📊 Rate Limiting

Rate limits are applied per user (authenticated) or per IP address (unauthenticated).

| Endpoint Type | Limit |
|--------------|-------|
| Authentication | 10 requests / 15 min |
| Public Read | 100 requests / min |
| Authenticated Read | 200 requests / min |
| Write Operations | 50 requests / min |
| Admin Operations | 100 requests / hour |

**Rate Limit Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 85
X-RateLimit-Reset: 1737540060
```

---

## 🔄 Webhooks

Subscribe to real-time events:

### Available Events
- `order.created`
- `order.updated`
- `order.cancelled`
- `payment.succeeded`
- `payment.failed`
- `product.created`
- `product.updated`

### Webhook Payload Example
```json
{
  "event": "order.created",
  "timestamp": "2026-01-22T10:30:00Z",
  "data": {
    "orderId": "ord_1a2b3c4d",
    "orderNumber": "ORD-2026-001234",
    "total": 333.97
  }
}
```

---

## 🧪 Testing

### Sandbox Environment
```
Base URL: https://sandbox-api.example-commerce.com/v1
```

### Test Credentials
```
Email: test@example.com
Password: TestPass123!
```

### Test Cards (Stripe)
```
Success: 4242 4242 4242 4242
Decline: 4000 0000 0000 0002
```

---

## 💡 Best Practices

### Pagination
Always use pagination for list endpoints to improve performance:
```bash
GET /products?page=1&limit=20
```

### Error Handling
Implement proper error handling for all API calls:
```javascript
try {
  const response = await fetch('/api/products');
  const data = await response.json();
  
  if (!data.success) {
    // Handle API error
    console.error(data.error);
  }
} catch (error) {
  // Handle network error
  console.error('Network error:', error);
}
```

### Caching
- Cache product listings for 5 minutes
- Cache individual products for 15 minutes
- Invalidate cache on product updates

### Idempotency
Use idempotency keys for critical operations:
```bash
POST /orders
Idempotency-Key: unique-key-123
```

---

## 📱 SDK Examples

### JavaScript/TypeScript
```typescript
import { EcommerceAPI } from '@example/api-client';

const api = new EcommerceAPI({
  baseURL: 'https://api.example-commerce.com/v1',
  apiKey: 'your-api-key'
});

// Get products
const products = await api.products.list({
  page: 1,
  limit: 20,
  category: 'electronics'
});

// Create order
const order = await api.orders.create({
  shippingAddress: {...},
  paymentMethodId: 'pm_123'
});
```

### Python
```python
from ecommerce_api import EcommerceAPI

api = EcommerceAPI(
    base_url='https://api.example-commerce.com/v1',
    api_key='your-api-key'
)

# Get products
products = api.products.list(
    page=1,
    limit=20,
    category='electronics'
)

# Create order
order = api.orders.create(
    shipping_address={...},
    payment_method_id='pm_123'
)
```

---

## 📞 Support

- **Documentation**: https://docs.example-commerce.com
- **API Status**: https://status.example-commerce.com
- **Support Email**: api-support@example-commerce.com
- **Developer Forum**: https://forum.example-commerce.com

---

## 🔖 Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.2.0 | 2026-01-22 | Added webhook support |
| v1.1.0 | 2025-12-01 | Added payment intents |
| v1.0.0 | 2025-06-15 | Initial release |
