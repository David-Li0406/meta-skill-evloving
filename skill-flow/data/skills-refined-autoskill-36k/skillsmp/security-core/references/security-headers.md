# Security Headers

Essential HTTP security headers for web applications.

## Quick Reference

| Header | Purpose | Priority |
|--------|---------|----------|
| Content-Security-Policy | Prevent XSS, injection attacks | ⚠️ Critical |
| Strict-Transport-Security | Enforce HTTPS | ⚠️ Critical |
| X-Frame-Options | Prevent clickjacking | 🟡 High |
| X-Content-Type-Options | Prevent MIME sniffing | 🟡 High |
| Referrer-Policy | Control referrer information | 🟢 Medium |
| Permissions-Policy | Control browser features | 🟢 Medium |

## Implementation

### TypeScript (Express + Helmet)

```typescript
import express from 'express';
import helmet from 'helmet';

const app = express();

app.use(
  helmet({
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        scriptSrc: ["'self'", "'unsafe-inline'"], // Avoid unsafe-inline in production
        styleSrc: ["'self'", "'unsafe-inline'"],
        imgSrc: ["'self'", 'data:', 'https:'],
        connectSrc: ["'self'"],
        fontSrc: ["'self'"],
        objectSrc: ["'none'"],
        mediaSrc: ["'self'"],
        frameSrc: ["'none'"],
      },
    },
    crossOriginEmbedderPolicy: true,
    crossOriginOpenerPolicy: { policy: 'same-origin' },
    crossOriginResourcePolicy: { policy: 'same-origin' },
    dnsPrefetchControl: { allow: false },
    frameguard: { action: 'deny' },
    hsts: {
      maxAge: 31536000, // 1 year
      includeSubDomains: true,
      preload: true,
    },
    ieNoOpen: true,
    noSniff: true,
    originAgentCluster: true,
    permittedCrossDomainPolicies: { permittedPolicies: 'none' },
    referrerPolicy: { policy: 'strict-origin-when-cross-origin' },
    xssFilter: true,
  })
);

// Disable X-Powered-By
app.disable('x-powered-by');
```

### Python (FastAPI)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI()

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)

    # CSP
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self'; "
        "connect-src 'self'; "
        "frame-ancestors 'none';"
    )

    # HSTS
    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains; preload"
    )

    # Other headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = (
        "geolocation=(), microphone=(), camera=()"
    )

    return response
```

### Rust (Axum)

```rust
use axum::{
    http::{header, HeaderValue, Request, StatusCode},
    middleware::Next,
    response::Response,
};

async fn add_security_headers<B>(
    req: Request<B>,
    next: Next<B>,
) -> Result<Response, StatusCode> {
    let mut response = next.run(req).await;

    let headers = response.headers_mut();

    // CSP
    headers.insert(
        header::CONTENT_SECURITY_POLICY,
        HeaderValue::from_static(
            "default-src 'self'; \
             script-src 'self'; \
             style-src 'self' 'unsafe-inline'; \
             img-src 'self' data: https:; \
             font-src 'self'; \
             connect-src 'self'; \
             frame-ancestors 'none';"
        ),
    );

    // HSTS
    headers.insert(
        header::STRICT_TRANSPORT_SECURITY,
        HeaderValue::from_static("max-age=31536000; includeSubDomains; preload"),
    );

    // Other headers
    headers.insert(
        header::X_CONTENT_TYPE_OPTIONS,
        HeaderValue::from_static("nosniff"),
    );

    headers.insert(
        header::X_FRAME_OPTIONS,
        HeaderValue::from_static("DENY"),
    );

    headers.insert(
        "Referrer-Policy",
        HeaderValue::from_static("strict-origin-when-cross-origin"),
    );

    Ok(response)
}
```

## Content Security Policy (CSP)

### Directives

```
Content-Security-Policy:
  default-src 'self';
  script-src 'self' https://cdn.example.com;
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https:;
  font-src 'self';
  connect-src 'self' https://api.example.com;
  frame-src 'none';
  object-src 'none';
  base-uri 'self';
  form-action 'self';
  frame-ancestors 'none';
  upgrade-insecure-requests;
```

### Nonces for Inline Scripts

```typescript
import crypto from 'crypto';

app.use((req, res, next) => {
  res.locals.nonce = crypto.randomBytes(16).toString('base64');
  next();
});

app.use(
  helmet({
    contentSecurityPolicy: {
      directives: {
        scriptSrc: ["'self'", (req, res) => `'nonce-${res.locals.nonce}'`],
      },
    },
  })
);

app.get('/', (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html>
      <head>
        <script nonce="${res.locals.nonce}">
          console.log('This script is allowed');
        </script>
      </head>
    </html>
  `);
});
```

## CORS Configuration

### TypeScript

```typescript
import cors from 'cors';

app.use(
  cors({
    origin: process.env.ALLOWED_ORIGINS?.split(',') || ['https://app.example.com'],
    methods: ['GET', 'POST', 'PUT', 'DELETE'],
    allowedHeaders: ['Content-Type', 'Authorization'],
    credentials: true,
    maxAge: 86400, // 24 hours
  })
);
```

### Python

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
    max_age=86400,
)
```

## Testing Headers

### Online Tools
- [Security Headers](https://securityheaders.com/)
- [Mozilla Observatory](https://observatory.mozilla.org/)

### Automated Testing

```typescript
import { describe, it, expect } from 'vitest';
import request from 'supertest';

describe('Security Headers', () => {
  it('should set CSP header', async () => {
    const response = await request(app).get('/');

    expect(response.headers['content-security-policy']).toContain("default-src 'self'");
  });

  it('should set HSTS header', async () => {
    const response = await request(app).get('/');

    expect(response.headers['strict-transport-security']).toBe(
      'max-age=31536000; includeSubDomains; preload'
    );
  });

  it('should set X-Frame-Options', async () => {
    const response = await request(app).get('/');

    expect(response.headers['x-frame-options']).toBe('DENY');
  });

  it('should set X-Content-Type-Options', async () => {
    const response = await request(app).get('/');

    expect(response.headers['x-content-type-options']).toBe('nosniff');
  });
});
```

## Checklist

- [ ] CSP configured with strict directives
- [ ] HSTS enabled with long max-age
- [ ] X-Frame-Options set to DENY or SAMEORIGIN
- [ ] X-Content-Type-Options set to nosniff
- [ ] Referrer-Policy configured
- [ ] X-Powered-By removed
- [ ] CORS properly configured
- [ ] Headers tested with online tools
- [ ] Automated tests for headers
- [ ] CSP reports monitored
