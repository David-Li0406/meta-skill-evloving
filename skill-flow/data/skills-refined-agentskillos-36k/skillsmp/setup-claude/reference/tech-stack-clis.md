# Tech Stack CLIs Reference

This reference lists CLI tools by category with installation and authentication commands.

## Core Principle

> **CLI over MCP**: CLIs are more token-efficient than MCPs.
> Each MCP adds tool definitions to your context window. CLIs add nothing.

---

## Quick Reference Table

| Service | CLI | Install | Auth Command | Auth Check |
|---------|-----|---------|--------------|------------|
| Vercel | `vercel` | `npm i -g vercel` | `vercel login` | `vercel whoami` |
| Supabase | `supabase` | `npm i -g supabase` | `supabase login` | `supabase projects list` |
| Convex | `npx convex` | Built-in | `npx convex dev` | `npx convex dashboard` |
| Stripe | `stripe` | `brew install stripe/stripe-cli/stripe` | `stripe login` | `stripe config --list` |
| Sentry | `sentry-cli` | `npm i -g @sentry/cli` | `sentry-cli login` | `sentry-cli info` |
| AWS | `aws` | `brew install awscli` | `aws configure` | `aws sts get-caller-identity` |
| GitHub | `gh` | `brew install gh` | `gh auth login` | `gh auth status` |
| Railway | `railway` | `npm i -g @railway/cli` | `railway login` | `railway whoami` |
| Netlify | `netlify` | `npm i -g netlify-cli` | `netlify login` | `netlify status` |
| Cloudflare | `wrangler` | `npm i -g wrangler` | `wrangler login` | `wrangler whoami` |
| Firebase | `firebase` | `npm i -g firebase-tools` | `firebase login` | `firebase projects:list` |
| PlanetScale | `pscale` | `brew install planetscale/tap/pscale` | `pscale auth login` | `pscale org list` |
| Turso | `turso` | `brew install tursodatabase/tap/turso` | `turso auth login` | `turso auth whoami` |
| Neon | `neonctl` | `npm i -g neonctl` | `neonctl auth` | `neonctl me` |
| Clerk | n/a | No CLI | Use dashboard | - |
| Auth0 | `auth0` | `npm i -g auth0-cli` | `auth0 login` | `auth0 tenants list` |

---

## By Category

### Hosting & Deployment

#### Vercel
```bash
# Install
npm install -g vercel

# Authenticate
vercel login

# Verify
vercel whoami

# Common commands
vercel                    # Deploy preview
vercel --prod            # Deploy production
vercel env pull          # Pull env vars
vercel ls                # List deployments
vercel logs [url]        # View logs
vercel inspect [url]     # Inspect deployment
```

#### Netlify
```bash
# Install
npm install -g netlify-cli

# Authenticate
netlify login

# Verify
netlify status

# Common commands
netlify deploy           # Deploy draft
netlify deploy --prod    # Deploy production
netlify env:list         # List env vars
netlify sites:list       # List sites
netlify dev              # Local development
```

#### Railway
```bash
# Install
npm install -g @railway/cli

# Authenticate
railway login

# Verify
railway whoami

# Common commands
railway init             # Initialize project
railway up               # Deploy
railway logs             # View logs
railway variables        # Manage env vars
railway run [cmd]        # Run with env vars
```

#### Cloudflare (Workers/Pages)
```bash
# Install
npm install -g wrangler

# Authenticate
wrangler login

# Verify
wrangler whoami

# Common commands
wrangler dev             # Local development
wrangler deploy          # Deploy worker
wrangler pages deploy    # Deploy pages
wrangler tail            # Live logs
```

#### AWS
```bash
# Install (macOS)
brew install awscli

# Install (other)
pip install awscli

# Authenticate
aws configure

# Verify
aws sts get-caller-identity

# Common commands
aws s3 ls                # List S3 buckets
aws lambda list-functions
aws cloudformation describe-stacks
```

### Databases

#### Supabase
```bash
# Install
npm install -g supabase

# Authenticate
supabase login

# Verify
supabase projects list

# Common commands
supabase init            # Initialize project
supabase start           # Start local instance
supabase db reset        # Reset local database
supabase db push         # Push migrations
supabase db pull         # Pull remote schema
supabase link            # Link to project
supabase gen types typescript  # Generate types
```

#### Convex
```bash
# Uses npx (no global install needed)

# Common commands
npx convex dev           # Start dev server
npx convex deploy        # Deploy to production
npx convex dashboard     # Open dashboard
npx convex codegen       # Generate types
npx convex env set KEY=value
```

#### PlanetScale
```bash
# Install (macOS)
brew install planetscale/tap/pscale

# Authenticate
pscale auth login

# Verify
pscale org list

# Common commands
pscale database list
pscale branch create [db] [branch]
pscale connect [db] [branch]
pscale deploy-request create [db] [branch]
```

#### Turso (libSQL)
```bash
# Install (macOS)
brew install tursodatabase/tap/turso

# Authenticate
turso auth login

# Verify
turso auth whoami

# Common commands
turso db create [name]
turso db list
turso db shell [name]
turso db tokens create [name]
```

#### Neon
```bash
# Install
npm install -g neonctl

# Authenticate
neonctl auth

# Verify
neonctl me

# Common commands
neonctl projects list
neonctl branches list
neonctl connection-string
```

### Payments

#### Stripe
```bash
# Install (macOS)
brew install stripe/stripe-cli/stripe

# Install (other)
# Download from https://stripe.com/docs/stripe-cli

# Authenticate
stripe login

# Verify
stripe config --list

# Common commands
stripe listen --forward-to localhost:3000/api/webhooks
stripe trigger payment_intent.succeeded
stripe customers list
stripe products list
stripe prices list
stripe logs tail
```

### Monitoring & Analytics

#### Sentry
```bash
# Install
npm install -g @sentry/cli

# Authenticate
sentry-cli login

# Verify
sentry-cli info

# Common commands
sentry-cli releases new [version]
sentry-cli releases files [version] upload-sourcemaps ./dist
sentry-cli releases finalize [version]
sentry-cli releases deploys [version] new -e production
```

#### PostHog
```bash
# No official CLI
# Use PostHog MCP or API directly
```

### Version Control

#### GitHub CLI
```bash
# Install (macOS)
brew install gh

# Authenticate
gh auth login

# Verify
gh auth status

# Common commands
gh repo create
gh pr create
gh pr list
gh pr checkout [number]
gh pr merge
gh issue create
gh issue list
gh workflow run
gh run list
gh run view [id]
```

### Authentication

#### Auth0
```bash
# Install
npm install -g auth0-cli

# Authenticate
auth0 login

# Verify
auth0 tenants list

# Common commands
auth0 apps list
auth0 apis list
auth0 logs tail
auth0 test login
```

---

## Runtime & Build Tools

### Node.js Ecosystem
```bash
node --version           # Node.js
npm --version            # npm
npx --version            # npx (comes with npm)
pnpm --version           # pnpm
yarn --version           # yarn
bun --version            # Bun runtime
```

### Python Ecosystem
```bash
python --version         # Python
pip --version            # pip
poetry --version         # Poetry
uv --version             # uv (fast pip alternative)
ruff --version           # Ruff linter
```

### Other Runtimes
```bash
cargo --version          # Rust
go version               # Go
deno --version           # Deno
```

---

## ORM & Database Tools

### Prisma
```bash
# Install (project-local)
npm install prisma --save-dev

# Common commands
npx prisma init
npx prisma generate
npx prisma db push
npx prisma migrate dev
npx prisma studio
```

### Drizzle
```bash
# Install (project-local)
npm install drizzle-kit --save-dev

# Common commands
npx drizzle-kit generate
npx drizzle-kit push
npx drizzle-kit studio
npx drizzle-kit migrate
```

---

## Detection Patterns

Use these patterns to detect services from project files:

```bash
# Detect from package.json dependencies
detect_services() {
    local deps=$(cat package.json 2>/dev/null)

    echo "$deps" | grep -q '"@supabase' && echo "supabase"
    echo "$deps" | grep -q '"stripe"' && echo "stripe"
    echo "$deps" | grep -q '"@sentry' && echo "sentry"
    echo "$deps" | grep -q '"convex"' && echo "convex"
    echo "$deps" | grep -q '"@clerk' && echo "clerk"
    echo "$deps" | grep -q '"@auth0' && echo "auth0"
    echo "$deps" | grep -q '"posthog' && echo "posthog"
    echo "$deps" | grep -q '"@vercel' && echo "vercel"
    echo "$deps" | grep -q '"@netlify' && echo "netlify"
    echo "$deps" | grep -q '"@aws-sdk' && echo "aws"
}

# Detect from config files
detect_from_configs() {
    [ -d "convex" ] && echo "convex"
    [ -f "vercel.json" ] && echo "vercel"
    [ -f "netlify.toml" ] && echo "netlify"
    [ -f "supabase/config.toml" ] && echo "supabase"
    [ -f "sentry.properties" ] && echo "sentry"
    [ -f "wrangler.toml" ] && echo "cloudflare"
    [ -f "firebase.json" ] && echo "firebase"
    [ -f "railway.json" ] && echo "railway"
}

# Detect from .env variable names
detect_from_env() {
    grep -h "^[A-Z_]*=" .env .env.local .env.example 2>/dev/null | cut -d= -f1 | while read var; do
        case "$var" in
            *SUPABASE*) echo "supabase" ;;
            *STRIPE*) echo "stripe" ;;
            *SENTRY*) echo "sentry" ;;
            *CONVEX*) echo "convex" ;;
            *CLERK*) echo "clerk" ;;
            *AUTH0*) echo "auth0" ;;
            *POSTHOG*) echo "posthog" ;;
            *VERCEL*) echo "vercel" ;;
            *NETLIFY*) echo "netlify" ;;
            *AWS*) echo "aws" ;;
            *RAILWAY*) echo "railway" ;;
            *NEON*) echo "neon" ;;
            *TURSO*) echo "turso" ;;
            *PLANETSCALE*) echo "planetscale" ;;
        esac
    done | sort -u
}
```

---

## No CLI Available

These services don't have CLIs and may need MCP or API access:

| Service | Alternative |
|---------|-------------|
| Clerk | Dashboard + SDK |
| PostHog | Dashboard + SDK |
| LogRocket | Dashboard + SDK |
| Paddle | Dashboard + SDK |
| Resend | API + SDK |
| Postmark | API + SDK |
| SendGrid | API + SDK |

For these, consider:
1. Using their REST API directly via `curl` or `fetch`
2. Using their SDK programmatically
3. Setting up an MCP server if frequent interaction needed
