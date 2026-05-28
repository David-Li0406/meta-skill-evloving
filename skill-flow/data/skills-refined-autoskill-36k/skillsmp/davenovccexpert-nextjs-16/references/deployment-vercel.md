<overview>
Deploy Next.js 16 to Vercel with zero configuration. Vercel is the native platform for Next.js with automatic optimizations.
</overview>

<quick_deploy>
**First deployment:**
```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy (from project root)
vercel

# Deploy to production
vercel --prod
```

**Git integration (recommended):**
1. Push code to GitHub/GitLab/Bitbucket
2. Go to vercel.com/new
3. Import repository
4. Configure settings
5. Deploy

Every push to main → production deployment
Every PR → preview deployment
</quick_deploy>

<environment_variables>
**Add via CLI:**
```bash
# Add for all environments
vercel env add DATABASE_URL

# Add for specific environment
vercel env add DATABASE_URL production
vercel env add DATABASE_URL preview
vercel env add DATABASE_URL development
```

**Add via dashboard:**
1. Go to Project Settings → Environment Variables
2. Add key and value
3. Select environments (Production, Preview, Development)

**Access in code:**
```typescript
const dbUrl = process.env.DATABASE_URL
```

**Secret references (for sensitive values):**
```bash
vercel secrets add my-secret "secret-value"
# Then reference: @my-secret
```
</environment_variables>

<build_settings>
**Default settings (usually correct):**
- Framework: Next.js (auto-detected)
- Build command: `next build`
- Output directory: `.next`
- Install command: `npm install`

**Override in vercel.json:**
```json
{
  "buildCommand": "npm run build",
  "installCommand": "npm ci",
  "framework": "nextjs"
}
```

**Node.js version:**
```json
{
  "functions": {
    "api/**/*.ts": {
      "runtime": "nodejs20.x"
    }
  }
}
```
</build_settings>

<domains>
**Add custom domain:**
```bash
vercel domains add example.com

# Or via dashboard: Project Settings → Domains
```

**Redirect www to apex:**
```json
// vercel.json
{
  "redirects": [
    {
      "source": "/:path*",
      "has": [{ "type": "host", "value": "www.example.com" }],
      "destination": "https://example.com/:path*",
      "permanent": true
    }
  ]
}
```
</domains>

<edge_config>
**Use Edge Config for feature flags:**
```bash
npm i @vercel/edge-config
```

```typescript
import { get } from '@vercel/edge-config'

export default async function Page() {
  const showBanner = await get('showBanner')

  return (
    <div>
      {showBanner && <Banner />}
    </div>
  )
}
```
</edge_config>

<analytics>
**Enable analytics:**
```bash
npm i @vercel/analytics
```

```tsx
// app/layout.tsx
import { Analytics } from '@vercel/analytics/react'

export default function Layout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  )
}
```

**Speed Insights:**
```bash
npm i @vercel/speed-insights
```

```tsx
import { SpeedInsights } from '@vercel/speed-insights/next'

export default function Layout({ children }) {
  return (
    <html>
      <body>
        {children}
        <SpeedInsights />
      </body>
    </html>
  )
}
```
</analytics>

<caching>
**Vercel automatically optimizes caching for Next.js 16:**

- Static assets: Long-lived cache
- Server-rendered pages: ISR based on `cacheLife`
- API routes: Per-route caching

**Edge caching for ISR:**
```tsx
async function getData() {
  'use cache'
  cacheLife('hours')

  // Vercel caches at edge automatically
  return await fetchData()
}
```
</caching>

<vercel_json>
**Common configurations:**

```json
{
  "redirects": [
    { "source": "/old", "destination": "/new", "permanent": true }
  ],
  "rewrites": [
    { "source": "/api/:path*", "destination": "https://api.example.com/:path*" }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Frame-Options", "value": "DENY" }
      ]
    }
  ],
  "regions": ["iad1", "sfo1"],
  "functions": {
    "api/heavy.ts": {
      "memory": 1024,
      "maxDuration": 60
    }
  }
}
```
</vercel_json>

<troubleshooting>
**Build failures:**
```bash
# Check build locally first
npm run build

# View build logs
vercel logs [deployment-url]
```

**Environment variable issues:**
```bash
# List env vars
vercel env ls

# Pull env vars locally
vercel env pull
```

**Function timeouts:**
- Default: 10s (Hobby), 60s (Pro)
- Increase via `maxDuration` in vercel.json or function config
</troubleshooting>
