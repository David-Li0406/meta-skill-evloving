# Health Monitoring Reference

## Health Matrix API

```typescript
const health = await fetch('/api/dashboard/health-matrix').then(r => r.json());
```

## Indicators Per Project

1. **Deployment** - Age of last deployment
   - ✅ Healthy: < 24 hours
   - ⚠️ Warning: 24-72 hours
   - ❌ Critical: > 72 hours

2. **HTTP** - Endpoint response
   - ✅ Healthy: 200 OK
   - ⚠️ Warning: 3xx redirects
   - ❌ Critical: 4xx/5xx errors

3. **Database** - Connection status
   - ✅ Healthy: Connected, queries working
   - ❌ Critical: Connection failed

4. **Registry** - Notion sync status (Empathy Ledger only)
   - ✅ Healthy: Synced < 1 hour
   - ⚠️ Warning: Synced > 1 hour

## Expected Output Format

```
🏥 System Health Check - All ACT Projects

┌─────────────────────┬────────────┬──────┬──────────┬──────────┐
│ Project             │ Deployment │ HTTP │ Database │ Registry │
├─────────────────────┼────────────┼──────┼──────────┼──────────┤
│ Empathy Ledger      │ ⚠️  18h    │ ✅   │ ✅       │ ⚠️       │
│ JusticeHub          │ ✅ 2h      │ ✅   │ ✅       │ N/A      │
│ The Harvest         │ ✅ 4h      │ ✅   │ ✅       │ N/A      │
│ ACT Farm            │ ❌ 72h     │ ⚠️   │ ✅       │ N/A      │
│ Goods               │ ✅ 6h      │ ✅   │ ✅       │ N/A      │
│ ACT Studio          │ ✅ 1h      │ ✅   │ ✅       │ N/A      │
└─────────────────────┴────────────┴──────┴──────────┴──────────┘

⚠️  Warnings:
  • ACT Farm: Last deployed 3 days ago (STALE)

🏆 Overall: 5/6 systems healthy (83%)
```

## Dashboard URLs

- Sprint progress: `/api/dashboard/sprint`
- Velocity: `/api/dashboard/velocity`
- Burndown: `/api/dashboard/burndown`
- Health matrix: `/api/dashboard/health-matrix`
- Deployments: `/api/dashboard/deployments`
