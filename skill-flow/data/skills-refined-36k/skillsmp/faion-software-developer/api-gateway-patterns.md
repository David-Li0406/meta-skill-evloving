# API Gateway Patterns

**ID:** api-gateway-patterns

## Problem

Direct API access creates security, scaling, and management challenges. Need unified entry point.

## Framework

**Gateway Functions:**

| Function | Description |
|----------|-------------|
| Routing | Direct requests to correct service |
| Load Balancing | Distribute traffic across instances |
| Authentication | Validate tokens, API keys |
| Rate Limiting | Protect services from overload |
| Caching | Reduce backend load |
| Request/Response Transform | Modify payloads |
| SSL Termination | Handle HTTPS |
| Logging/Monitoring | Centralized observability |

## Kong Gateway

```yaml
# kong.yml
_format_version: "3.0"

services:
  - name: user-service
    url: http://user-service:8080
    routes:
      - name: users-route
        paths:
          - /api/users
        strip_path: false

  - name: order-service
    url: http://order-service:8080
    routes:
      - name: orders-route
        paths:
          - /api/orders

plugins:
  - name: rate-limiting
    config:
      minute: 100
      policy: local

  - name: jwt
    config:
      secret_is_base64: false
      claims_to_verify:
        - exp

  - name: cors
    config:
      origins:
        - https://app.example.com
      methods:
        - GET
        - POST
        - PUT
        - DELETE
      headers:
        - Authorization
        - Content-Type

  - name: request-transformer
    config:
      add:
        headers:
          - X-Request-ID:$(uuid)
```

## AWS API Gateway

```yaml
# serverless.yml (Serverless Framework)
service: user-api

provider:
  name: aws
  runtime: python3.11

functions:
  getUsers:
    handler: handlers.get_users
    events:
      - http:
          path: /users
          method: get
          cors: true
          authorizer:
            type: COGNITO_USER_POOLS
            authorizerId:
              Ref: ApiGatewayAuthorizer

  createUser:
    handler: handlers.create_user
    events:
      - http:
          path: /users
          method: post
          cors: true

resources:
  Resources:
    ApiGatewayAuthorizer:
      Type: AWS::ApiGateway::Authorizer
      Properties:
        Name: CognitoAuthorizer
        Type: COGNITO_USER_POOLS
        IdentitySource: method.request.header.Authorization
        RestApiId:
          Ref: ApiGatewayRestApi
        ProviderARNs:
          - arn:aws:cognito-idp:us-east-1:123456789:userpool/us-east-1_abc123

    UsagePlan:
      Type: AWS::ApiGateway::UsagePlan
      Properties:
        UsagePlanName: BasicPlan
        Throttle:
          BurstLimit: 100
          RateLimit: 50
        Quota:
          Limit: 1000
          Period: DAY
```

## Nginx as Gateway

```nginx
# /etc/nginx/nginx.conf
upstream user_service {
    server user-service-1:8080 weight=3;
    server user-service-2:8080 weight=2;
    keepalive 32;
}

upstream order_service {
    server order-service:8080;
}

server {
    listen 443 ssl http2;
    server_name api.example.com;

    ssl_certificate /etc/ssl/certs/api.crt;
    ssl_certificate_key /etc/ssl/private/api.key;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req zone=api_limit burst=20 nodelay;

    # CORS
    add_header 'Access-Control-Allow-Origin' 'https://app.example.com';
    add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS';

    location /api/users {
        proxy_pass http://user_service;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Request-ID $request_id;
    }

    location /api/orders {
        proxy_pass http://order_service;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Health check
    location /health {
        return 200 '{"status":"ok"}';
        add_header Content-Type application/json;
    }
}
```

## Gateway Patterns

**Backend for Frontend (BFF):**

```
Mobile App  ->  Mobile BFF  ->  Microservices
Web App     ->  Web BFF     ->  Microservices
```

**API Composition:**

```python
# Gateway aggregates multiple service calls
@app.get("/api/dashboard")
async def get_dashboard(user_id: str):
    async with httpx.AsyncClient() as client:
        user, orders, notifications = await asyncio.gather(
            client.get(f"http://user-service/users/{user_id}"),
            client.get(f"http://order-service/users/{user_id}/orders?limit=5"),
            client.get(f"http://notification-service/users/{user_id}/unread")
        )

    return {
        "user": user.json(),
        "recentOrders": orders.json(),
        "notifications": notifications.json()
    }
```

## Best Practices

- Keep gateway stateless
- Implement circuit breakers
- Cache responses at edge
- Use async for downstream calls
- Monitor gateway performance
- Version gateway configuration
- Implement request tracing

## Agent

faion-api-agent
