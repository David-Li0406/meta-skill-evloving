---
name: API Management
description: This skill should be used when the user asks to "API gateway, rate limiting, API versioning, GraphQL, REST API, API security, Kong, API documentation, API design, OpenAPI, Swagger", or needs help with API gateway configuration, rate limiting, versioning, and API security.
version: 1.0.0
---

# API Management

Comprehensive guidance for designing, securing, and managing APIs using gateways, rate limiting, versioning strategies, and documentation.

## API Gateway Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                         API Gateway                               │
├──────────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │
│  │  Auth    │  │  Rate    │  │  Request │  │  Load            │ │
│  │  Layer   │→ │  Limiter │→ │  Routing │→ │  Balancing       │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────────┘ │
│       ↓             ↓             ↓               ↓              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │
│  │  Logging │  │ Caching  │  │Transform │  │  Circuit Breaker │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
                               │
            ┌──────────────────┼──────────────────┐
            ▼                  ▼                  ▼
     ┌──────────┐       ┌──────────┐       ┌──────────┐
     │ Service  │       │ Service  │       │ Service  │
     │    A     │       │    B     │       │    C     │
     └──────────┘       └──────────┘       └──────────┘
```

## Kong Gateway

### Installation

```yaml
# docker-compose.yml - Kong with PostgreSQL
version: '3.8'

services:
  kong-database:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: kong
      POSTGRES_DB: kong
      POSTGRES_PASSWORD: ${KONG_PG_PASSWORD}
    volumes:
      - kong_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "kong"]
      interval: 10s
      timeout: 5s
      retries: 5

  kong-migration:
    image: kong:3.4
    command: kong migrations bootstrap
    environment:
      KONG_DATABASE: postgres
      KONG_PG_HOST: kong-database
      KONG_PG_PASSWORD: ${KONG_PG_PASSWORD}
    depends_on:
      kong-database:
        condition: service_healthy

  kong:
    image: kong:3.4
    environment:
      KONG_DATABASE: postgres
      KONG_PG_HOST: kong-database
      KONG_PG_PASSWORD: ${KONG_PG_PASSWORD}
      KONG_PROXY_ACCESS_LOG: /dev/stdout
      KONG_ADMIN_ACCESS_LOG: /dev/stdout
      KONG_PROXY_ERROR_LOG: /dev/stderr
      KONG_ADMIN_ERROR_LOG: /dev/stderr
      KONG_ADMIN_LISTEN: 0.0.0.0:8001
    ports:
      - "8000:8000"   # Proxy
      - "8443:8443"   # Proxy SSL
      - "8001:8001"   # Admin API
    depends_on:
      kong-migration:
        condition: service_completed_successfully
    healthcheck:
      test: ["CMD", "kong", "health"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  kong_data:
```

### Kong Configuration (Declarative)

```yaml
# kong.yml - Declarative configuration
_format_version: "3.0"

services:
  - name: users-service
    url: http://users-api:3000
    routes:
      - name: users-route
        paths:
          - /api/v1/users
        strip_path: false
        methods:
          - GET
          - POST
          - PUT
          - DELETE
    plugins:
      - name: rate-limiting
        config:
          minute: 100
          hour: 1000
          policy: redis
          redis_host: redis
      - name: key-auth
        config:
          key_names:
            - X-API-Key
            - apikey
      - name: cors
        config:
          origins:
            - "*"
          methods:
            - GET
            - POST
            - PUT
            - DELETE
          headers:
            - Content-Type
            - Authorization
            - X-API-Key

  - name: orders-service
    url: http://orders-api:3000
    routes:
      - name: orders-route
        paths:
          - /api/v1/orders
    plugins:
      - name: jwt
        config:
          claims_to_verify:
            - exp
      - name: request-transformer
        config:
          add:
            headers:
              - "X-Request-ID:$(uuid)"

consumers:
  - username: mobile-app
    keyauth_credentials:
      - key: ${MOBILE_API_KEY}
    plugins:
      - name: rate-limiting
        config:
          minute: 200  # Higher limit for mobile

  - username: web-app
    keyauth_credentials:
      - key: ${WEB_API_KEY}

plugins:
  - name: prometheus
  - name: correlation-id
    config:
      header_name: X-Correlation-ID
      generator: uuid
```

## AWS API Gateway

### REST API Configuration

```yaml
# serverless.yml - API Gateway with Serverless Framework
service: my-api

provider:
  name: aws
  runtime: nodejs18.x
  region: us-east-1
  apiGateway:
    apiKeys:
      - name: mobile-key
        value: ${ssm:/api/keys/mobile}
      - name: web-key
        value: ${ssm:/api/keys/web}
    usagePlan:
      quota:
        limit: 10000
        period: MONTH
      throttle:
        burstLimit: 200
        rateLimit: 100

functions:
  getUsers:
    handler: src/handlers/users.list
    events:
      - http:
          path: /users
          method: get
          cors: true
          authorizer:
            type: COGNITO_USER_POOLS
            authorizerId: !Ref ApiAuthorizer
          request:
            parameters:
              querystrings:
                page: false
                limit: false
            schemas:
              application/json: ${file(schemas/get-users.json)}

  createUser:
    handler: src/handlers/users.create
    events:
      - http:
          path: /users
          method: post
          cors: true
          authorizer:
            type: COGNITO_USER_POOLS
            authorizerId: !Ref ApiAuthorizer
          request:
            schemas:
              application/json: ${file(schemas/create-user.json)}

resources:
  Resources:
    ApiAuthorizer:
      Type: AWS::ApiGateway::Authorizer
      Properties:
        Name: CognitoAuthorizer
        Type: COGNITO_USER_POOLS
        IdentitySource: method.request.header.Authorization
        RestApiId: !Ref ApiGatewayRestApi
        ProviderARNs:
          - !GetAtt UserPool.Arn

    # Custom domain
    ApiDomainName:
      Type: AWS::ApiGateway::DomainName
      Properties:
        DomainName: api.example.com
        CertificateArn: ${ssm:/certificates/api-cert-arn}

    ApiBasePathMapping:
      Type: AWS::ApiGateway::BasePathMapping
      Properties:
        DomainName: !Ref ApiDomainName
        RestApiId: !Ref ApiGatewayRestApi
        Stage: ${opt:stage}
```

### Request Validation

```json
// schemas/create-user.json
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "title": "CreateUser",
  "type": "object",
  "required": ["email", "name"],
  "properties": {
    "email": {
      "type": "string",
      "format": "email",
      "maxLength": 255
    },
    "name": {
      "type": "string",
      "minLength": 1,
      "maxLength": 100
    },
    "role": {
      "type": "string",
      "enum": ["user", "admin", "moderator"]
    }
  },
  "additionalProperties": false
}
```

## Rate Limiting

### Redis-Based Rate Limiter

```javascript
// rateLimiter.js - Token bucket implementation
const Redis = require('ioredis');

class RateLimiter {
    constructor(redis, options = {}) {
        this.redis = redis;
        this.windowMs = options.windowMs || 60000; // 1 minute
        this.maxRequests = options.maxRequests || 100;
        this.keyPrefix = options.keyPrefix || 'ratelimit:';
    }

    async isAllowed(identifier) {
        const key = `${this.keyPrefix}${identifier}`;
        const now = Date.now();
        const windowStart = now - this.windowMs;

        const pipeline = this.redis.pipeline();

        // Remove old entries
        pipeline.zremrangebyscore(key, 0, windowStart);
        // Count current entries
        pipeline.zcard(key);
        // Add new entry
        pipeline.zadd(key, now, `${now}-${Math.random()}`);
        // Set expiry
        pipeline.expire(key, Math.ceil(this.windowMs / 1000));

        const results = await pipeline.exec();
        const currentCount = results[1][1];

        return {
            allowed: currentCount < this.maxRequests,
            remaining: Math.max(0, this.maxRequests - currentCount - 1),
            resetAt: new Date(now + this.windowMs),
        };
    }
}

// Express middleware
function rateLimitMiddleware(limiter) {
    return async (req, res, next) => {
        const identifier = req.headers['x-api-key'] || req.ip;
        const result = await limiter.isAllowed(identifier);

        res.set({
            'X-RateLimit-Limit': limiter.maxRequests,
            'X-RateLimit-Remaining': result.remaining,
            'X-RateLimit-Reset': result.resetAt.toISOString(),
        });

        if (!result.allowed) {
            return res.status(429).json({
                error: 'Too many requests',
                retryAfter: Math.ceil((result.resetAt - Date.now()) / 1000),
            });
        }

        next();
    };
}

module.exports = { RateLimiter, rateLimitMiddleware };
```

### Rate Limit Tiers

```yaml
# Rate limit configuration by tier
rate_limits:
  free:
    requests_per_minute: 60
    requests_per_day: 1000
    burst_size: 10

  basic:
    requests_per_minute: 300
    requests_per_day: 10000
    burst_size: 50

  professional:
    requests_per_minute: 1000
    requests_per_day: 100000
    burst_size: 200

  enterprise:
    requests_per_minute: 10000
    requests_per_day: unlimited
    burst_size: 1000
```

## API Versioning

### URL Path Versioning

```javascript
// routes/index.js
const express = require('express');
const router = express.Router();

// Version 1
const v1Router = require('./v1');
router.use('/v1', v1Router);

// Version 2
const v2Router = require('./v2');
router.use('/v2', v2Router);

// Latest version redirect
router.use('/latest', v2Router);

module.exports = router;
```

### Header-Based Versioning

```javascript
// middleware/versioning.js
function versionMiddleware(req, res, next) {
    // Accept-Version header
    const acceptVersion = req.headers['accept-version'];
    // API-Version header (alternative)
    const apiVersion = req.headers['api-version'];
    // Query parameter fallback
    const queryVersion = req.query.version;

    req.apiVersion = acceptVersion || apiVersion || queryVersion || '2';

    // Set response header
    res.set('API-Version', req.apiVersion);

    next();
}

// Route handler with version support
function getUserHandler(req, res) {
    const { id } = req.params;

    switch (req.apiVersion) {
        case '1':
            return res.json(formatUserV1(user));
        case '2':
        default:
            return res.json(formatUserV2(user));
    }
}
```

### Content Negotiation

```javascript
// Content-type based versioning
// Accept: application/vnd.myapi.v2+json

function contentNegotiationMiddleware(req, res, next) {
    const accept = req.headers.accept || '';
    const versionMatch = accept.match(/application\/vnd\.myapi\.v(\d+)\+json/);

    req.apiVersion = versionMatch ? versionMatch[1] : '2';
    res.set('Content-Type', `application/vnd.myapi.v${req.apiVersion}+json`);

    next();
}
```

## OpenAPI Specification

```yaml
# openapi.yaml
openapi: 3.1.0
info:
  title: My API
  version: 2.0.0
  description: |
    ## Overview
    This API provides access to user and order management.

    ## Authentication
    All endpoints require an API key in the `X-API-Key` header.

    ## Rate Limiting
    - Free tier: 60 requests/minute
    - Pro tier: 1000 requests/minute
  contact:
    email: api-support@example.com
  license:
    name: MIT

servers:
  - url: https://api.example.com/v2
    description: Production
  - url: https://staging-api.example.com/v2
    description: Staging

security:
  - ApiKeyAuth: []
  - BearerAuth: []

paths:
  /users:
    get:
      summary: List users
      operationId: listUsers
      tags:
        - Users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            minimum: 1
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
        - name: sort
          in: query
          schema:
            type: string
            enum: [created_at, name, email]
      responses:
        '200':
          description: List of users
          headers:
            X-RateLimit-Limit:
              schema:
                type: integer
            X-RateLimit-Remaining:
              schema:
                type: integer
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '429':
          $ref: '#/components/responses/RateLimited'

    post:
      summary: Create user
      operationId: createUser
      tags:
        - Users
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: User created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          $ref: '#/components/responses/BadRequest'
        '409':
          description: Email already exists

  /users/{id}:
    parameters:
      - name: id
        in: path
        required: true
        schema:
          type: string
          format: uuid
    get:
      summary: Get user by ID
      operationId: getUser
      tags:
        - Users
      responses:
        '200':
          description: User details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          $ref: '#/components/responses/NotFound'

components:
  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    User:
      type: object
      properties:
        id:
          type: string
          format: uuid
        email:
          type: string
          format: email
        name:
          type: string
        role:
          type: string
          enum: [user, admin]
        createdAt:
          type: string
          format: date-time
      required:
        - id
        - email
        - name

    CreateUserRequest:
      type: object
      properties:
        email:
          type: string
          format: email
        name:
          type: string
          minLength: 1
          maxLength: 100
        role:
          type: string
          enum: [user, admin]
          default: user
      required:
        - email
        - name

    UserList:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/User'
        pagination:
          $ref: '#/components/schemas/Pagination'

    Pagination:
      type: object
      properties:
        page:
          type: integer
        limit:
          type: integer
        total:
          type: integer
        totalPages:
          type: integer

    Error:
      type: object
      properties:
        code:
          type: string
        message:
          type: string
        details:
          type: array
          items:
            type: object

  responses:
    BadRequest:
      description: Invalid request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    Unauthorized:
      description: Missing or invalid authentication
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    RateLimited:
      description: Too many requests
      headers:
        Retry-After:
          schema:
            type: integer
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
```

## API Security

### JWT Validation

```javascript
// middleware/auth.js
const jwt = require('jsonwebtoken');
const jwksClient = require('jwks-rsa');

const client = jwksClient({
    jwksUri: process.env.JWKS_URI,
    cache: true,
    rateLimit: true,
});

function getKey(header, callback) {
    client.getSigningKey(header.kid, (err, key) => {
        if (err) return callback(err);
        callback(null, key.getPublicKey());
    });
}

async function authMiddleware(req, res, next) {
    const authHeader = req.headers.authorization;

    if (!authHeader?.startsWith('Bearer ')) {
        return res.status(401).json({ error: 'Missing authorization header' });
    }

    const token = authHeader.substring(7);

    try {
        const decoded = await new Promise((resolve, reject) => {
            jwt.verify(token, getKey, {
                algorithms: ['RS256'],
                issuer: process.env.JWT_ISSUER,
                audience: process.env.JWT_AUDIENCE,
            }, (err, decoded) => {
                if (err) reject(err);
                else resolve(decoded);
            });
        });

        req.user = decoded;
        next();
    } catch (error) {
        return res.status(401).json({ error: 'Invalid token' });
    }
}

module.exports = { authMiddleware };
```

### Input Validation

```javascript
// middleware/validation.js
const Ajv = require('ajv');
const addFormats = require('ajv-formats');

const ajv = new Ajv({ allErrors: true, removeAdditional: 'all' });
addFormats(ajv);

function validate(schema) {
    const validator = ajv.compile(schema);

    return (req, res, next) => {
        const valid = validator(req.body);

        if (!valid) {
            return res.status(400).json({
                error: 'Validation failed',
                details: validator.errors.map(e => ({
                    field: e.instancePath,
                    message: e.message,
                })),
            });
        }

        next();
    };
}

// Usage
app.post('/users', validate(createUserSchema), createUserHandler);
```

## Monitoring & Analytics

### Request Logging

```javascript
// middleware/logging.js
const { v4: uuidv4 } = require('uuid');

function requestLoggingMiddleware(req, res, next) {
    const requestId = req.headers['x-request-id'] || uuidv4();
    const startTime = Date.now();

    req.requestId = requestId;
    res.set('X-Request-ID', requestId);

    res.on('finish', () => {
        const duration = Date.now() - startTime;

        console.log(JSON.stringify({
            timestamp: new Date().toISOString(),
            requestId,
            method: req.method,
            path: req.path,
            statusCode: res.statusCode,
            duration,
            userAgent: req.headers['user-agent'],
            apiKey: req.headers['x-api-key']?.substring(0, 8) + '...',
            ip: req.ip,
        }));
    });

    next();
}
```

### Prometheus Metrics

```javascript
// metrics.js
const promClient = require('prom-client');

const httpRequestsTotal = new promClient.Counter({
    name: 'http_requests_total',
    help: 'Total HTTP requests',
    labelNames: ['method', 'path', 'status'],
});

const httpRequestDuration = new promClient.Histogram({
    name: 'http_request_duration_seconds',
    help: 'HTTP request duration',
    labelNames: ['method', 'path'],
    buckets: [0.01, 0.05, 0.1, 0.5, 1, 5],
});

function metricsMiddleware(req, res, next) {
    const end = httpRequestDuration.startTimer({
        method: req.method,
        path: req.route?.path || req.path,
    });

    res.on('finish', () => {
        httpRequestsTotal.inc({
            method: req.method,
            path: req.route?.path || req.path,
            status: res.statusCode,
        });
        end();
    });

    next();
}

// Metrics endpoint
app.get('/metrics', async (req, res) => {
    res.set('Content-Type', promClient.register.contentType);
    res.end(await promClient.register.metrics());
});
```

## Best Practices

| Area | Practice |
|------|----------|
| Versioning | Use URL path versioning for public APIs |
| Rate Limiting | Implement tiered limits based on plan |
| Authentication | Use JWT with short expiry + refresh tokens |
| Validation | Validate all inputs with JSON Schema |
| Errors | Use consistent error format with codes |
| Documentation | Generate from OpenAPI spec |
| Monitoring | Track latency percentiles (p50, p95, p99) |
| Caching | Use ETags and Cache-Control headers |
