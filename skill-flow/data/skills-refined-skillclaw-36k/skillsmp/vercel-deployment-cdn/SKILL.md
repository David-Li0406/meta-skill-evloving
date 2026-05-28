---
name: Vercel Deployment & CDN
description: Deploy frontend, manage CDN caching, and automate deployments via Vercel MCP
---

# Vercel MCP Integration

Manage deployments, CDN caching, and serverless functions through the Vercel MCP server.

## Configuration ✅

**Status**: Configured via `mcp-remote https://mcp.vercel.com`

First use will prompt for Vercel authentication.

## Capabilities

| Feature | Use Case |
|---------|----------|
| **Deployments** | Deploy, rollback, promote previews |
| **CDN** | Cache invalidation, edge config |
| **Projects** | Create, configure, manage |
| **Domains** | Add, verify, configure DNS |
| **Functions** | Node.js serverless functions |

## Common Operations

### Deploy Frontend
```
Deploy the Next.js frontend to production
```

### Invalidate CDN Cache
```
Purge CDN cache for /api/* endpoints
```

### Check Deployment Status
```
Get status of latest deployment
```

## CDN Best Practices

From [Vercel CDN docs](https://vercel.com/docs/cdn):
- Use `Cache-Control` headers for static assets
- Leverage edge caching for API responses
- Use `stale-while-revalidate` for dynamic content

## Integration with Trading Platform

| Component | Vercel Feature |
|-----------|----------------|
| Frontend (Next.js) | Automatic deployments |
| API routes | Serverless functions |
| Market data | CDN edge caching |
| Static assets | Global CDN distribution |
