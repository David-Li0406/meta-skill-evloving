---
name: trading-backend
description: Trading Backend API for OctoBot web/mobile interfaces
version: 1.0.0
license: GPL-3.0
---

# trading-backend Development

## Overview

Trading Backend provides REST API endpoints for web and mobile interfaces to interact with OctoBot. Handles authentication, real-time data streaming, trading operations, and portfolio management.

## References

- **[API Endpoints](references/api-endpoints.md)**: REST routes, authentication, request/response formats
- **[Architecture](references/architecture.md)**: Flask app structure, middleware, error handling
- **[Real-time Updates](references/realtime.md)**: WebSocket connections, Server-Sent Events

## Key Concepts

### Flask Application
RESTful API built with Flask framework.

### Authentication
JWT-based authentication for secure access.

### OctoBot Bridge
Backend communicates with OctoBot core via internal API.

## Common Tasks

### Add New Endpoint
```python
from flask import Blueprint, jsonify

api = Blueprint("api", __name__)

@api.route("/portfolio/balance", methods=["GET"])
@require_auth
def get_balance():
    balance = octobot.get_portfolio_balance()
    return jsonify(balance)
```

### Authenticate Requests
```python
from functools import wraps
import jwt

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.InvalidTokenError:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated
```

### Stream Real-time Data
```python
@api.route("/stream/prices")
def stream_prices():
    def generate():
        while True:
            price = get_current_price()
            yield f"data: {json.dumps(price)}\n\n"
            time.sleep(1)
    
    return Response(generate(), mimetype="text/event-stream")
```

## Integration Points

- **OctoBot Core**: Backend calls OctoBot API for operations
- **OctoBot-Trading**: Access trading operations
- **Web Interface**: Frontend consumes REST API
- **Mobile Apps**: Native apps use same API

## Quick Reference

### Common Endpoints
- `GET /api/portfolio`: Portfolio overview
- `POST /api/orders`: Place order
- `GET /api/trades/history`: Trade history
- `GET /api/config`: Bot configuration
- `POST /api/auth/login`: Authentication

### Error Responses
```json
{
    "error": "Invalid symbol",
    "code": 400,
    "details": "BTC/USD not found"
}
```

### Success Response
```json
{
    "success": true,
    "data": {...}
}
```

## Checklist

- [ ] Secure all endpoints with authentication
- [ ] Implement rate limiting
- [ ] Add CORS headers for web access
- [ ] Document all API routes in OpenAPI/Swagger
- [ ] Test endpoints with Postman/curl
- [ ] Handle OctoBot connection errors
- [ ] Validate all request payloads
- [ ] Log API access for auditing
