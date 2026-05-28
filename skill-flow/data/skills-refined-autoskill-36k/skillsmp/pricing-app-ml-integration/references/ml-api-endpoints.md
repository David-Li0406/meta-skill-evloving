# MercadoLibre API Endpoints Reference

Common ML API endpoints used in Pricing App.

## OAuth

```
POST https://api.mercadolibre.com/oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token
&client_id={CLIENT_ID}
&client_secret={CLIENT_SECRET}
&refresh_token={REFRESH_TOKEN}
```

**Response:**
```json
{
  "access_token": "APP_USR-xxx",
  "token_type": "bearer",
  "expires_in": 21600,
  "refresh_token": "TG-xxx"
}
```

## Items API

### Get Single Item
```
GET https://api.mercadolibre.com/items/{ITEM_ID}
Authorization: Bearer {ACCESS_TOKEN}
```

### Get Multiple Items (Batch)
```
GET https://api.mercadolibre.com/items?ids={ID1},{ID2},{ID3}
Authorization: Bearer {ACCESS_TOKEN}
```

**Max:** 20 items per request

**Response:** Array of `{code: 200, body: {...}}` objects

### Update Item Price
```
PUT https://api.mercadolibre.com/items/{ITEM_ID}
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "price": 15000
}
```

### Update Item Stock
```
PUT https://api.mercadolibre.com/items/{ITEM_ID}
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "available_quantity": 5
}
```

### Get User Items
```
GET https://api.mercadolibre.com/users/{USER_ID}/items/search
Authorization: Bearer {ACCESS_TOKEN}

Query params:
- status: active|paused|closed
- offset: pagination offset
- limit: max 50
```

## Orders API

### Get Order
```
GET https://api.mercadolibre.com/orders/{ORDER_ID}
Authorization: Bearer {ACCESS_TOKEN}
```

### Search Orders
```
GET https://api.mercadolibre.com/orders/search
Authorization: Bearer {ACCESS_TOKEN}

Query params:
- seller: {USER_ID}
- order.status: confirmed|payment_required|paid|cancelled
- order.date_created.from: ISO8601
- order.date_created.to: ISO8601
```

## Notifications (Webhooks)

ML sends notifications to your webhook URL when:
- New order created (`orders_v2`)
- Item updated (`items`)
- New question (`questions`)

**Webhook payload:**
```json
{
  "topic": "orders_v2",
  "resource": "/orders/123456789",
  "user_id": 12345,
  "sent": "2025-01-15T10:30:00.000Z"
}
```

**Your endpoint must:**
- Respond within 3 seconds with `200 OK`
- Queue processing in background
- Handle duplicate notifications (idempotent)

## Rate Limits

- **Default:** 10 requests/second
- **Batch endpoints:** Count as 1 request (regardless of items)
- **429 Response:** Wait and retry with exponential backoff

## Error Codes

| Code | Meaning |
|------|---------|
| 200 | OK |
| 400 | Bad request (invalid params) |
| 401 | Unauthorized (invalid/expired token) |
| 404 | Resource not found |
| 429 | Too many requests (rate limit) |
| 500 | ML server error (retry) |

## Resources

- [ML API Docs](https://developers.mercadolibre.com/es_ar/api-docs-es)
- [OAuth Guide](https://developers.mercadolibre.com/es_ar/autenticacion-y-autorizacion)
- [Items API](https://developers.mercadolibre.com/es_ar/items-y-busquedas)
- [Orders API](https://developers.mercadolibre.com/es_ar/gestiona-ventas)
