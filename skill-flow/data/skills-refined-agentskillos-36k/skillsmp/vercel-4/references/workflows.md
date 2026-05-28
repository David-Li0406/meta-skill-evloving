# Vercel Workflows Reference

## Contents
- Deployment Workflow
- Environment Variable Management
- Debugging Failed Deployments
- Local Development Workflow

---

## Deployment Workflow

### Automatic Deployments (This Project)

Push to `main` triggers automatic production deployment. Pull requests create preview deployments.

```bash
# Standard deployment flow
git add .
git commit -m "Add feature"
git push origin main  # Auto-deploys to production
```

### Manual Deployment via CLI

```bash
# Preview deployment (staging)
vercel

# Production deployment
vercel --prod

# Deploy with visible build logs
vercel deploy --logs
```

### Deployment Checklist

Copy this checklist and track progress:
- [ ] Step 1: Run `npm run build` locally to catch errors
- [ ] Step 2: Verify environment variables are set in Vercel dashboard
- [ ] Step 3: Push to branch / open PR for preview deployment
- [ ] Step 4: Test preview URL thoroughly
- [ ] Step 5: Merge to main for production deployment
- [ ] Step 6: Verify production deployment works

---

## Environment Variable Management

### Adding Variables

```bash
# Interactive add (prompts for value)
vercel env add RESEND_API_KEY

# Add for specific environment
vercel env add RESEND_API_KEY production
vercel env add RESEND_API_KEY preview
vercel env add RESEND_API_KEY development
```

### Pulling to Local

```bash
# Download all env vars to .env.local
vercel env pull

# Pull specific environment
vercel env pull .env.production.local --environment=production
```

### Required Variables (This Project)

| Variable | Environments | Purpose |
|----------|--------------|---------|
| `RESEND_API_KEY` | All | Email sending via Resend |
| `NEXT_PUBLIC_GA_MEASUREMENT_ID` | Production | Google Analytics tracking |
| `NEXT_PUBLIC_SITE_URL` | All | Base URL for links in emails |

---

## Debugging Failed Deployments

### Build Error Investigation Workflow

```bash
# 1. Always build locally first
npm run build

# 2. If local build passes but Vercel fails, deploy with logs
vercel deploy --logs

# 3. Check function logs in dashboard
# Vercel Dashboard → Project → Deployments → [Failed] → Building
```

### Common Build Failures

**TypeScript Errors:**
```bash
# Local check
npm run lint
npx tsc --noEmit
```

**Missing Environment Variables:**
```bash
# Verify vars exist in Vercel
vercel env ls

# Build error: "RESEND_API_KEY is not defined"
# Solution: Add to Vercel dashboard or via CLI
vercel env add RESEND_API_KEY
```

**Dependency Issues:**
```bash
# Clear local cache and reinstall
rm -rf node_modules .next
npm install
npm run build
```

### Function Runtime Errors

1. Go to Vercel Dashboard → Project → Logs
2. Filter by "Functions" and timeframe
3. Look for error stack traces

**Iterate Until Pass Pattern:**

1. Check Vercel deployment logs for error
2. Reproduce error locally if possible
3. Fix the issue
4. Run `npm run build` locally
5. If build fails, fix and repeat step 4
6. Push to trigger new deployment
7. If deployment fails, return to step 1

---

## Local Development Workflow

### Setup

```bash
# Clone and install
git clone <repo>
cd xopweb
npm install

# Pull environment variables from Vercel
vercel env pull

# Start dev server
npm run dev
```

### Testing API Routes Locally

```bash
# Test contact form endpoint
curl -X POST http://localhost:3000/api/contact \
  -H "Content-Type: application/json" \
  -d '{"firstName":"Test","lastName":"User","companyName":"Acme","email":"test@example.com","message":"Hello"}'
```

### Vercel CLI Commands Reference

| Command | Purpose |
|---------|---------|
| `vercel` | Deploy preview |
| `vercel --prod` | Deploy production |
| `vercel deploy --logs` | Deploy with visible logs |
| `vercel env pull` | Download env vars locally |
| `vercel env add NAME` | Add environment variable |
| `vercel env ls` | List all env vars |
| `vercel logs` | View function logs |
| `vercel inspect <url>` | Inspect deployment details |

### Preview vs Production

| Aspect | Preview | Production |
|--------|---------|------------|
| URL | `project-hash.vercel.app` | Custom domain or `project.vercel.app` |
| Trigger | PR or `vercel` CLI | Push to main or `vercel --prod` |
| Env vars | Preview environment | Production environment |
| Use case | Testing changes | Live site |

---

## Integration with Other Skills

For email sending configuration, see the **resend** skill. For Next.js App Router patterns used in API routes, see the **nextjs** skill. For TypeScript configuration affecting builds, see the **typescript** skill.