---
name: Global Network
description: This skill should be used when the user asks to "configure CDN", "global load balancing", "edge computing", "network latency", "geo-routing", "DDoS protection", "WAF configuration", "content delivery", "Cloudflare setup", "AWS CloudFront", or needs help with global network infrastructure and content delivery.
version: 1.0.0
---

# Global Network

Comprehensive guidance for CDN configuration, global load balancing, and edge computing.

## CDN Configuration

### CloudFront Setup

```bash
aws cloudfront create-distribution \
  --origin-domain-name myapp.s3.amazonaws.com \
  --default-root-object index.html
```

### Cloudflare Configuration

```javascript
// cloudflare-worker.js
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const url = new URL(request.url)

  // Route based on geography
  const country = request.cf.country
  if (country === 'CN') {
    return Response.redirect('https://cn.example.com' + url.pathname)
  }

  return fetch(request)
}
```

## Global Load Balancing

### DNS-based Routing

- **Latency-based**: Route to nearest region
- **Geolocation**: Route based on user location
- **Weighted**: Distribute traffic by percentage
- **Failover**: Primary/secondary configuration

### Health Checks

```yaml
health_check:
  protocol: HTTPS
  port: 443
  path: /health
  interval: 30
  timeout: 10
  unhealthy_threshold: 3
```

## Edge Computing

### Use Cases

- Image optimization
- A/B testing at edge
- Authentication/authorization
- Request transformation
- Bot detection

### Performance Optimization

| Technique | Impact |
|-----------|--------|
| Compression | 60-80% size reduction |
| Minification | 10-30% size reduction |
| HTTP/2 | Multiplexing, header compression |
| Caching | Reduce origin requests |
| Edge compute | Reduce latency |

## DDoS Protection

- Rate limiting
- IP reputation filtering
- Challenge pages (CAPTCHA)
- Geographic blocking
- Protocol validation

## Additional Resources

### Reference Files
- **`references/cdn-providers.md`** - CDN provider comparison
- **`references/edge-patterns.md`** - Edge computing patterns
