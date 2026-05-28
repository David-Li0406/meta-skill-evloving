<workflow name="ship-app">
<title>Ship Next.js 16 App</title>

<required_reading>
**Read these reference files NOW:**
1. references/deployment-vercel.md
2. references/deployment-docker.md
3. references/security.md
</required_reading>

<process>

<step name="1-pre-deployment-checklist">
<title>Pre-Deployment Checklist</title>

```bash
# 1. Build passes
npm run build

# 2. Types pass
npx tsc --noEmit

# 3. Tests pass
npm test

# 4. Lint passes
npm run lint
```

**Check environment variables:**
```bash
# Ensure all required env vars are documented
cat .env.example

# Verify no secrets in .env.local are committed
git status
```

**Security review:**
- [ ] No API keys in code
- [ ] HTTPS enforced
- [ ] CSP headers configured
- [ ] Server Actions have auth checks
</step>

<step name="2-choose-deployment-target">
<title>Choose Deployment Target</title>

**Option A: Vercel (Recommended)**
- Zero configuration
- Edge functions
- Analytics included
- Automatic HTTPS

**Option B: Docker**
- Full control
- Any cloud provider
- Self-managed scaling

**Option C: Node.js Self-Hosted**
- Simple setup
- Traditional servers
- Manual management
</step>

<step name="3a-deploy-to-vercel">
<title>Deploy to Vercel</title>

**First deployment:**
```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
vercel
```

**Connect to Git (recommended):**
1. Push code to GitHub/GitLab/Bitbucket
2. Go to vercel.com
3. Import repository
4. Configure environment variables
5. Deploy

**Environment variables:**
```bash
# Add via CLI
vercel env add DATABASE_URL production

# Or via dashboard
# Settings → Environment Variables
```

**Production deployment:**
```bash
vercel --prod
```
</step>

<step name="3b-deploy-with-docker">
<title>Deploy with Docker</title>

**Create Dockerfile:**
```dockerfile
# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Stage 2: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

# Stage 3: Production
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]
```

**Enable standalone output:**
```typescript
// next.config.ts
const nextConfig = {
  output: 'standalone',
}
```

**Build and run:**
```bash
# Build image
docker build -t my-nextjs-app .

# Run container
docker run -p 3000:3000 -e DATABASE_URL="..." my-nextjs-app
```

**Docker Compose for local testing:**
```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
    restart: unless-stopped
```
</step>

<step name="3c-self-hosted-nodejs">
<title>Self-Hosted Node.js</title>

**Build for production:**
```bash
npm run build
```

**Start production server:**
```bash
npm start
```

**Using PM2 for process management:**
```bash
# Install PM2
npm i -g pm2

# Start app
pm2 start npm --name "nextjs" -- start

# Enable startup script
pm2 startup
pm2 save

# Monitor
pm2 monit
```

**Nginx reverse proxy:**
```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```
</step>

<step name="4-configure-production-settings">
<title>Configure Production Settings</title>

**Install sharp for image optimization:**
```bash
npm install sharp
```

**Configure security headers:**
```typescript
// next.config.ts
const nextConfig = {
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'origin-when-cross-origin',
          },
          {
            key: 'Content-Security-Policy',
            value: "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';",
          },
        ],
      },
    ]
  },
}
```
</step>

<step name="5-setup-monitoring">
<title>Set Up Monitoring</title>

**Vercel Analytics (if using Vercel):**
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

**Error tracking (e.g., Sentry):**
```bash
npx @sentry/wizard@latest -i nextjs
```

**Health check endpoint:**
```typescript
// app/api/health/route.ts
export async function GET() {
  return Response.json({ status: 'ok', timestamp: new Date().toISOString() })
}
```
</step>

<step name="6-verify-deployment">
<title>Verify Deployment</title>

```bash
# Check site is accessible
curl -I https://your-domain.com

# Check health endpoint
curl https://your-domain.com/api/health

# Run Lighthouse on production
npx lighthouse https://your-domain.com --view
```

**Verify:**
- [ ] Site loads correctly
- [ ] All pages work
- [ ] API routes respond
- [ ] Images load and are optimized
- [ ] Authentication works
- [ ] Environment variables are set
- [ ] HTTPS is enforced
- [ ] Security headers present
</step>

</process>

<anti_patterns>
**Avoid:**
- Committing `.env.local` or secrets to git
- Deploying without running build locally first
- Skipping security headers
- Not setting up monitoring
- Using development mode in production
- Forgetting to install sharp for image optimization
</anti_patterns>

<success_criteria>
Deployment is complete when:
- [ ] Site is accessible at production URL
- [ ] HTTPS enabled
- [ ] All environment variables configured
- [ ] Health check passes
- [ ] Core Web Vitals acceptable
- [ ] Error monitoring active
- [ ] Security headers configured
- [ ] CI/CD pipeline set up (optional but recommended)
</success_criteria>

</workflow>
