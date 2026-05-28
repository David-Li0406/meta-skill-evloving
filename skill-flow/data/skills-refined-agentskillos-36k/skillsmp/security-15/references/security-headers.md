# HTTP Security Headers

Configure security headers to protect against common web attacks.

## Essential Headers

### Content-Security-Policy (CSP)

Controls which resources the browser can load.

```http
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self' https://api.example.com; frame-ancestors 'none';
```

**Directives:**
- `default-src 'self'` - Only load from same origin by default
- `script-src` - JavaScript sources
- `style-src` - CSS sources
- `img-src` - Image sources
- `connect-src` - Fetch/XHR destinations
- `frame-ancestors 'none'` - Prevent clickjacking

### Strict-Transport-Security (HSTS)

Force HTTPS connections.

```http
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

- `max-age=31536000` - Remember for 1 year
- `includeSubDomains` - Apply to all subdomains
- `preload` - Submit to browser preload lists

### X-Content-Type-Options

Prevent MIME type sniffing.

```http
X-Content-Type-Options: nosniff
```

### X-Frame-Options

Prevent clickjacking (legacy, use CSP frame-ancestors).

```http
X-Frame-Options: DENY
```

### Referrer-Policy

Control referrer information leakage.

```http
Referrer-Policy: strict-origin-when-cross-origin
```

### Permissions-Policy

Disable unused browser features.

```http
Permissions-Policy: geolocation=(), microphone=(), camera=()
```

## Framework Configuration

### Express.js (Node.js)

```javascript
const helmet = require('helmet');
app.use(helmet());

// Or configure individually
app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'"],
    styleSrc: ["'self'", "'unsafe-inline'"],
    imgSrc: ["'self'", "data:", "https:"],
  },
}));
```

### Django (Python)

```python
# settings.py
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
CSP_DEFAULT_SRC = ("'self'",)
```

### Spring Boot (Java)

```java
@Configuration
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http.headers(headers -> headers
            .contentSecurityPolicy(csp -> csp
                .policyDirectives("default-src 'self'"))
            .frameOptions(frame -> frame.deny())
            .httpStrictTransportSecurity(hsts -> hsts
                .maxAgeInSeconds(31536000)
                .includeSubDomains(true)));
        return http.build();
    }
}
```

### Nginx

```nginx
add_header Content-Security-Policy "default-src 'self';" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "DENY" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
```

## Testing Headers

```bash
# Check headers
curl -I https://example.com

# Security header scanner
npx security-headers https://example.com

# Mozilla Observatory
# https://observatory.mozilla.org
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| `unsafe-inline` in CSP | XSS possible | Use nonces or hashes |
| Missing HSTS | Downgrade attacks | Add HSTS header |
| `X-Frame-Options: SAMEORIGIN` | Still allows some framing | Use `DENY` or CSP |
| No `Referrer-Policy` | URL leakage | Set strict policy |
| Report-only forever | No protection | Enforce CSP |
