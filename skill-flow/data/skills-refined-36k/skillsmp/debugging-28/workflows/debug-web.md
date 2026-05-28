# Web/Network Debugging Workflow

## When to Use

- CORS errors
- Network request failures
- SSL/TLS certificate issues
- Performance problems (slow loading)
- Security header issues
- Caching problems
- WebSocket connection issues

## Step 1: Gather Symptoms

```
□ What is the exact error in console/network tab?
□ Which requests are failing?
□ Is it all requests or specific ones?
□ Browser-specific or all browsers?
□ Works in one environment but not another?
□ Any recent infrastructure changes?
```

## Step 2: Network Tab Analysis

Open DevTools → Network tab

### Key things to check:
```
□ Status code (red = failed)
□ Request/Response headers
□ Request payload
□ Response body
□ Timing breakdown
□ Initiator (what triggered request)
```

### Filter techniques:
- `XHR` - Just API calls
- `status-code:500` - Just 500 errors
- `domain:api.example.com` - Just one domain
- `-domain:cdn.example.com` - Exclude CDN

## Step 3: CORS Debugging

### The Error:
```
Access to XMLHttpRequest at 'https://api.example.com' from origin
'https://app.example.com' has been blocked by CORS policy
```

### Understanding CORS:
```
Browser makes request →
  If cross-origin → Preflight check (OPTIONS) →
    Server responds with allowed origins →
      If allowed → Actual request
      If not → CORS error
```

### Check preflight response:
```
Required headers from server:
Access-Control-Allow-Origin: https://app.example.com  (or *)
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Allow-Credentials: true  (if using cookies)
```

### Common CORS fixes:

| Issue | Fix |
|-------|-----|
| Origin not allowed | Add origin to allowed list |
| Method not allowed | Add method to Allow-Methods |
| Header not allowed | Add header to Allow-Headers |
| Credentials issue | Set Allow-Credentials: true |
| Wildcard with creds | Can't use *, specify origin |

### Server-side examples:

```python
# FastAPI
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
```

```javascript
// Express
const cors = require('cors');
app.use(cors({
  origin: 'https://app.example.com',
  credentials: true
}));
```

## Step 4: SSL/TLS Issues

### Common errors:
```
NET::ERR_CERT_AUTHORITY_INVALID
→ Self-signed or untrusted CA
→ Fix: Use trusted CA, or add exception for dev

NET::ERR_CERT_DATE_INVALID
→ Certificate expired
→ Fix: Renew certificate

NET::ERR_CERT_COMMON_NAME_INVALID
→ Certificate doesn't match domain
→ Fix: Get cert for correct domain, add SAN

Mixed Content
→ HTTPS page loading HTTP resource
→ Fix: Update all URLs to HTTPS
```

### Check certificate:
```bash
# View certificate details
openssl s_client -connect example.com:443 -servername example.com

# Check expiry
echo | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -noout -dates
```

## Step 5: Performance Debugging

### Network timing breakdown:
```
Queueing     → Request waiting in browser queue
Stalled      → Waiting for connection
DNS Lookup   → Resolving hostname
Initial Connection → TCP handshake
SSL          → TLS handshake
Request sent → Time to send request
Waiting (TTFB) → Time to first byte (server processing)
Content Download → Receiving response
```

### Common performance issues:

| Large TTFB | Server is slow | Profile backend |
| Large Download | Response too big | Compress, paginate |
| Many requests | Too many resources | Bundle, lazy load |
| Queueing | HTTP/1.1 limit | Use HTTP/2, domain sharding |

### Performance profiling:
```
DevTools → Lighthouse
→ Run audit
→ Check opportunities and diagnostics
```

### Key metrics:
- **LCP** (Largest Contentful Paint) - Main content loaded
- **FID** (First Input Delay) - Interactivity
- **CLS** (Cumulative Layout Shift) - Visual stability
- **TTFB** (Time to First Byte) - Server response

## Step 6: Caching Issues

### Cache headers to check:
```
Cache-Control: max-age=3600, public
ETag: "abc123"
Last-Modified: Wed, 21 Oct 2024 07:28:00 GMT
Expires: Thu, 22 Oct 2024 07:28:00 GMT
```

### Force fresh request:
- Hard refresh: Ctrl+Shift+R
- Clear cache: DevTools → Application → Clear storage
- Disable cache: DevTools → Network → Disable cache

### Common cache issues:
| Symptom | Cause | Fix |
|---------|-------|-----|
| Old content showing | Aggressive caching | Add cache-busting, reduce max-age |
| Always re-fetching | No cache headers | Add Cache-Control |
| Partial updates | Cached HTML, new JS | Version static assets |
| CDN stale | CDN cache not purged | Purge CDN, use versioned URLs |

## Step 7: Security Headers

### Check security headers:
```bash
curl -I https://example.com

# Or use: https://securityheaders.com
```

### Important headers:
```
Content-Security-Policy: default-src 'self'
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Strict-Transport-Security: max-age=31536000; includeSubDomains
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=()
```

### CSP debugging:
```
Refused to load script from 'https://cdn.example.com'
→ CSP blocking the source
→ Check: Content-Security-Policy header
→ Fix: Add source to appropriate directive

# Report-only mode for testing
Content-Security-Policy-Report-Only: default-src 'self'
```

## Step 8: WebSocket Debugging

### Check WebSocket connection:
```
DevTools → Network → WS filter

Look for:
- 101 Switching Protocols (success)
- Connection close codes
- Messages sent/received
```

### Common WebSocket issues:
| Issue | Cause | Fix |
|-------|-------|-----|
| 403 on upgrade | CORS/auth | Check Origin header, auth |
| Connection drops | Timeout, proxy | Heartbeat/ping, proxy config |
| SSL error | wss:// cert issue | Check certificate |

### WebSocket debugging:
```javascript
const ws = new WebSocket('wss://api.example.com/ws');

ws.onopen = () => console.log('Connected');
ws.onclose = (e) => console.log('Closed', e.code, e.reason);
ws.onerror = (e) => console.error('Error', e);
ws.onmessage = (e) => console.log('Message', e.data);
```

## Step 9: Proxy/Load Balancer Issues

### Check if proxy is the issue:
```bash
# Direct request (bypass proxy)
curl --resolve api.example.com:443:1.2.3.4 https://api.example.com/health

# Check proxy headers
X-Forwarded-For: client-ip
X-Forwarded-Proto: https
X-Real-IP: client-ip
```

### Common proxy issues:
- Request timeout (increase proxy timeout)
- Large request rejected (increase body limit)
- WebSocket not proxied (enable WebSocket proxy)
- Headers stripped (preserve headers)

## Step 10: Fix and Verify

```
1. Identify root cause
2. Apply fix
3. Test in multiple browsers
4. Test with cache cleared
5. Test in incognito/private mode
6. Verify in staging before production
7. Monitor for regressions
```

## Quick Reference: Common Network Errors

| Error | Meaning | Likely Cause |
|-------|---------|--------------|
| net::ERR_CONNECTION_REFUSED | Server not listening | Service down, wrong port |
| net::ERR_CONNECTION_TIMED_OUT | No response | Firewall, network issue |
| net::ERR_NAME_NOT_RESOLVED | DNS failure | Wrong domain, DNS issue |
| net::ERR_CERT_* | SSL/TLS issue | Certificate problem |
| CORS error | Cross-origin blocked | Missing CORS headers |
| Mixed Content | HTTPS loading HTTP | Update to HTTPS URLs |
