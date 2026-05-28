# API Endpoints

## Authentication

### Login
```http
POST /api/auth/login
Content-Type: application/json

{
    "username": "admin",
    "password": "password"
}

Response:
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_in": 3600
}
```

## Portfolio

### Get Balance
```http
GET /api/portfolio/balance
Authorization: Bearer <token>

Response:
{
    "total_value": 10000.0,
    "available": 8500.0,
    "locked": 1500.0,
    "currency": "USDT"
}
```

### Get Holdings
```http
GET /api/portfolio/holdings
Authorization: Bearer <token>

Response:
{
    "holdings": [
        {"asset": "BTC", "amount": 0.5, "value_usdt": 25000},
        {"asset": "ETH", "amount": 5.0, "value_usdt": 10000}
    ]
}
```

## Trading

### Place Order
```http
POST /api/orders
Authorization: Bearer <token>
Content-Type: application/json

{
    "symbol": "BTC/USDT",
    "side": "buy",
    "type": "limit",
    "amount": 0.001,
    "price": 50000
}

Response:
{
    "order_id": "abc123",
    "status": "open",
    "created_at": "2024-01-15T10:30:00Z"
}
```

### Get Trade History
```http
GET /api/trades/history?limit=50
Authorization: Bearer <token>

Response:
{
    "trades": [
        {
            "id": "trade1",
            "symbol": "BTC/USDT",
            "side": "buy",
            "price": 50000,
            "amount": 0.001,
            "timestamp": "2024-01-15T10:30:00Z"
        }
    ]
}
```

## Configuration

### Get Bot Config
```http
GET /api/config
Authorization: Bearer <token>

Response:
{
    "trading_mode": "spot",
    "risk_level": "medium",
    "exchanges": ["binance", "coinbase"]
}
```

### Update Config
```http
PUT /api/config
Authorization: Bearer <token>
Content-Type: application/json

{
    "risk_level": "low"
}
```
