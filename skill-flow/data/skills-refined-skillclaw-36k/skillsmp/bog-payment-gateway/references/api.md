# BOG Payment Gateway API Reference

> **IMPORTANT**:
> - All callback and redirect URLs MUST use HTTPS. BOG will reject requests with HTTP URLs.
> - All API requests MUST include `Accept-Language` header with value `ka` (Georgian) or `en` (English).

## Table of Contents
1. [Authentication](#authentication)
2. [Create Order](#create-order)
3. [Get Payment Details](#get-payment-details)
4. [Refund Payment](#refund-payment)
5. [Error Codes](#error-codes)
6. [Callback Handling](#callback-handling)

---

## Authentication

### Token Endpoint
```
POST https://oauth2.bog.ge/auth/realms/bog/protocol/openid-connect/token
```

### Request Headers
| Header | Value |
|--------|-------|
| Content-Type | `application/x-www-form-urlencoded` |
| Authorization | `Basic {base64(client_id:client_secret)}` |

### Request Body
```
grant_type=client_credentials
```

### Response
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 300
}
```

### Notes
- Token expires in ~5 minutes (300 seconds)
- Implement token caching to avoid excessive auth requests
- Never expose `client_secret` in client-side code

---

## Create Order

### Endpoint
```
POST https://api.bog.ge/payments/v1/ecommerce/orders
```

### Request Headers
| Header | Value | Required |
|--------|-------|----------|
| Authorization | `Bearer {access_token}` | Yes |
| Content-Type | `application/json` | Yes |
| Accept-Language | `ka` or `en` | No |
| Idempotency-Key | UUID v4 | Recommended |

### Request Body

```json
{
  "callback_url": "https://merchant.com/api/bog/callback",
  "external_order_id": "MERCHANT-ORDER-12345",
  "capture": "automatic",
  "purchase_units": {
    "currency": "GEL",
    "total_amount": 150.50,
    "total_discount_amount": 10.00,
    "basket": [
      {
        "product_id": "SKU-001",
        "description": "Product Name",
        "quantity": 2,
        "unit_price": 75.25,
        "unit_discount_price": 5.00,
        "total_price": 140.50,
        "vat": 23.42,
        "vat_percent": 18,
        "image": "https://merchant.com/images/product.jpg"
      }
    ],
    "delivery": {
      "amount": 10.00
    }
  },
  "redirect_urls": {
    "success": "https://merchant.com/payment/success",
    "fail": "https://merchant.com/payment/fail"
  },
  "buyer": {
    "full_name": "John Doe",
    "masked_email": "j***@example.com",
    "masked_phone": "+995*****1234"
  },
  "payment_method": ["card", "google_pay", "apple_pay"],
  "ttl": 600,
  "config": {
    "account": {
      "tag": "default"
    }
  }
}
```

### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| callback_url | string | Yes | URL for payment result notification |
| external_order_id | string | No | Merchant's order identifier |
| capture | string | No | `automatic` (default) or `manual` |
| purchase_units | object | Yes | Order details |
| purchase_units.currency | string | No | `GEL` (default), `USD`, `EUR` |
| purchase_units.total_amount | number | Yes | Total order amount |
| purchase_units.basket | array | Yes | Array of basket items |
| redirect_urls | object | No | Success/fail redirect URLs |
| buyer | object | No | Customer information |
| payment_method | array | No | Allowed payment methods |
| ttl | number | No | Time-to-live in seconds (default 600) |

### Basket Item Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| product_id | string | Yes | Product SKU/ID |
| quantity | number | Yes | Item quantity |
| unit_price | number | Yes | Price per unit |
| description | string | No | Product description |
| unit_discount_price | number | No | Discount per unit |
| total_price | number | No | Total for line item |
| vat | number | No | VAT amount |
| vat_percent | number | No | VAT percentage |
| image | string | No | Product image URL |

### Response
```json
{
  "id": "bog-order-uuid-here",
  "external_order_id": "MERCHANT-ORDER-12345",
  "status": "created",
  "currency": "GEL",
  "total_amount": 150.50,
  "_links": {
    "details": {
      "href": "https://api.bog.ge/payments/v1/receipt/bog-order-uuid-here"
    },
    "redirect": {
      "href": "https://payments.bog.ge/payment/bog-order-uuid-here"
    }
  }
}
```

**Important**: Redirect the customer to `_links.redirect.href` to complete payment.

---

## Get Payment Details

### Endpoint
```
GET https://api.bog.ge/payments/v1/receipt/{order_id}
```

### Request Headers
| Header | Value |
|--------|-------|
| Authorization | `Bearer {access_token}` |

### Response
```json
{
  "id": "bog-order-uuid-here",
  "external_order_id": "MERCHANT-ORDER-12345",
  "status": "completed",
  "order_status": {
    "key": "completed",
    "value": "Payment completed successfully"
  },
  "payment_detail": {
    "code": 100,
    "message": "Successful payment",
    "card_mask": "4***********1234",
    "transaction_id": "txn-uuid-here"
  },
  "purchase_units": {
    "currency": "GEL",
    "total_amount": 150.50
  },
  "create_date": "2024-01-15T10:30:00Z",
  "payment_date": "2024-01-15T10:32:00Z"
}
```

### Order Status Values
| Key | Description |
|-----|-------------|
| created | Order created, awaiting payment |
| processing | Payment in progress |
| completed | Payment successful |
| rejected | Payment declined |
| expired | Order TTL expired |
| refunded | Full refund processed |
| partially_refunded | Partial refund processed |

---

## Refund Payment

### Endpoint
```
POST https://api.bog.ge/payments/v1/payment/refund/{order_id}
```

### Request Headers
| Header | Value | Required |
|--------|-------|----------|
| Authorization | `Bearer {access_token}` | Yes |
| Content-Type | `application/json` | Yes |
| Idempotency-Key | UUID v4 | Recommended |

### Request Body (Partial Refund)
```json
{
  "amount": 50.00
}
```

For **full refund**, send empty body or omit `amount`.

### Response
```json
{
  "key": "request_received",
  "message": "Refund request received",
  "action_id": "refund-action-uuid"
}
```

### Refund Rules
- Full refunds: Card, Apple Pay, Google Pay, BOG authorization
- Partial refunds: Card, Apple Pay, Google Pay only
- Refunds cannot be cancelled once initiated
- Multiple partial refunds allowed until full amount refunded

---

## Error Codes

### Payment Response Codes

| Code | Key | Description | Action |
|------|-----|-------------|--------|
| 100 | successful_payment | Payment completed | Fulfill order |
| 200 | successful_preauth | Pre-auth approved | Capture when ready |
| 101 | card_limited | Card usage restricted | Customer contacts bank |
| 102 | saved_card_not_found | Stored card missing | Re-enter card details |
| 103 | invalid_card | Card validation failed | Check card details |
| 104 | transaction_limit | Too many transactions | Wait and retry |
| 105 | card_expired | Card validity ended | Use different card |
| 106 | amount_limit | Amount exceeds limit | Reduce amount or contact bank |
| 107 | insufficient_funds | Balance too low | Use different card |
| 108 | auth_declined | 3DS/auth failed | Retry or use different card |
| 109 | technical_issue | System error | Retry later |
| 110 | transaction_expired | Timeout occurred | Create new order |
| 111 | auth_timeout | 3DS timeout | Retry payment |
| 112 | general_error | Unspecified error | Contact support |
| 199 | unknown | Unknown response | Contact support |

### HTTP Status Codes

| Status | Meaning |
|--------|---------|
| 200 | Success |
| 400 | Bad request - Check request body |
| 401 | Unauthorized - Check/refresh token |
| 404 | Not found - Check order_id |
| 409 | Conflict - Duplicate idempotency key |
| 500 | Server error - Retry later |

---

## Callback Handling

BOG sends a POST request to your `callback_url` when payment status changes.

### Callback Payload
```json
{
  "order_id": "bog-order-uuid-here",
  "external_order_id": "MERCHANT-ORDER-12345",
  "status": "completed",
  "payment_detail": {
    "code": 100,
    "message": "Successful payment"
  },
  "timestamp": "2024-01-15T10:32:00Z"
}
```

### Callback Best Practices
1. **Respond quickly** - Return 200 within 5 seconds
2. **Idempotency** - Handle duplicate callbacks gracefully
3. **Verify** - Always verify payment via API, don't trust callback alone
4. **Log** - Record all callbacks for debugging
5. **Async processing** - Queue heavy operations, respond immediately

### Example Callback Handler (Express.js)
```typescript
app.post('/api/bog/callback', async (req, res) => {
  const { order_id, status, payment_detail } = req.body;

  // Respond immediately
  res.status(200).json({ received: true });

  // Process asynchronously
  if (status === 'completed' && payment_detail.code === 100) {
    // Verify via API
    const verified = await verifyPayment(order_id);
    if (verified) {
      await fulfillOrder(order_id);
    }
  }
});
```

---

## Payment Methods

### Supported Methods
- **card** - Visa, MasterCard, American Express
- **google_pay** - Google Pay
- **apple_pay** - Apple Pay
- **bog_auth** - Bank of Georgia authorization

### Specifying Payment Methods
```json
{
  "payment_method": ["card", "google_pay", "apple_pay"]
}
```

Omit to allow all available methods.

---

## Pre-Authorization (Hold Funds)

For pre-authorization (holding funds without immediate capture):

```json
{
  "capture": "manual",
  ...
}
```

### Capture Pre-Authorized Payment
```
POST https://api.bog.ge/payments/v1/payment/capture/{order_id}
Authorization: Bearer {access_token}
```

Pre-authorized payments must be captured within 7 days.
