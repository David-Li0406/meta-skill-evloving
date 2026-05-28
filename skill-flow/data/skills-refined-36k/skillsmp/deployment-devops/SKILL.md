---
name: Deployment & DevOps
description: Deploy to production with Vercel and manage environment
---

# Deployment & DevOps Skill

## Overview
Deploy the Smarter.Poker platform to production using Vercel and manage the environment.

## Auto-Publish Workflow

### Steps (Mandatory after code changes)
```bash
# 1. Build
npm run build

# 2. Commit
git add -A && git commit -m "[description]"

# 3. Push
git push origin main

# 4. Deploy
vercel --prod

# 5. Verify
curl -s "https://smarter.poker/" | grep -o "buildId[^,]*"
```

## Environment Variables

### Required in Vercel
```
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGc...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGc...
OPENAI_API_KEY=sk-...
```

### Local (.env.local)
```
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGc...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGc...
OPENAI_API_KEY=sk-...
```

## Domain Configuration

### Production
- Primary: `smarter.poker`
- Redirect: `www.smarter.poker` → `smarter.poker`

### Middleware (middleware.js)
```javascript
export function middleware(request) {
  const host = request.headers.get('host') || '';
  
  // Redirect www to non-www
  if (host.startsWith('www.')) {
    return NextResponse.redirect(
      new URL(request.url.replace('www.', ''))
    );
  }
  
  return NextResponse.next();
}
```

## Cron Jobs (Vercel)

### Configure in vercel.json
```json
{
  "crons": [
    {
      "path": "/api/cron/horses-clips",
      "schedule": "0 * * * *"
    },
    {
      "path": "/api/cron/horses-news",
      "schedule": "0 8,20 * * *"
    },
    {
      "path": "/api/cron/horses-memes",
      "schedule": "0 6,14,22 * * *"
    }
  ]
}
```

## Build Optimization

### next.config.js
```javascript
module.exports = {
  reactStrictMode: false,  // Required for Supabase auth
  images: {
    domains: ['xxx.supabase.co'],
    unoptimized: false
  },
  experimental: {
    optimizeCss: true
  }
};
```

## Monitoring

### Check Build Status
```bash
vercel ls
```

### View Logs
```bash
vercel logs smarter.poker --follow
```

### Rollback
```bash
vercel rollback
```

## Troubleshooting

### Build Fails
1. Check `npm run build` locally first
2. Review Vercel build logs
3. Check for missing env vars

### 404 on Routes
- Ensure pages exist in `/pages/`
- Check for dynamic route issues

### API Timeout
- Vercel serverless has 10s limit (free), 60s (pro)
- Move long operations to background jobs

### Cache Issues
1. Redeploy: `vercel --prod --force`
2. Purge CDN cache in Vercel dashboard
3. Test in incognito/hard refresh

## Security Checklist
- [ ] No secrets in client-side code
- [ ] Service role key only in API routes
- [ ] RLS enabled on all tables
- [ ] CORS configured properly
