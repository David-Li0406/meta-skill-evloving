# CLI Discovery Component

This component guides the CLI-first approach to external service integration. Always prefer CLI tools over MCP servers - they are more token-efficient and provide better control.

## Core Principle

> **CLI-First**: For every external service, check if a CLI exists before considering an MCP.
> CLIs consume zero context window, MCPs consume tokens for every tool definition.

## Discovery Flow

### Step 1: Detect Services from Project

First, scan the project to identify external services:

```bash
# Check package.json for service-related dependencies
cat package.json | grep -E "(supabase|stripe|sentry|vercel|convex|clerk|auth0|posthog|railway|netlify|aws)" || true

# Check for service-specific config files
ls -la | grep -E "(convex|supabase|vercel|netlify|firebase|amplify)" || true

# Check .env files for service URLs/keys (names only, not values)
grep -h "^[A-Z_]*=" .env .env.local .env.example 2>/dev/null | cut -d= -f1 | grep -E "(SUPABASE|STRIPE|SENTRY|VERCEL|CONVEX|CLERK|AUTH0|POSTHOG|RAILWAY|NETLIFY|AWS)" || true
```

### Step 2: Interview User for Additional Services

After auto-detection, ask about services not found in config:

```
AskUserQuestion: "What external services will this project use?"
(Multi-select)
├── Hosting: Vercel, AWS, Netlify, Railway
├── Database: Supabase, Convex, PlanetScale, Neon
├── Auth: Clerk, Auth0, Supabase Auth
├── Monitoring: Sentry, PostHog, LogRocket
├── Payments: Stripe, Paddle
├── Email: Resend, Postmark, SendGrid
└── Other (specify)
```

### Step 3: Look Up CLIs

For each identified service, look up the CLI in [reference/tech-stack-clis.md](../reference/tech-stack-clis.md).

### Step 4: Check Installation Status

```bash
# Generic check pattern
check_cli() {
    local cli_name=$1
    local check_command=$2

    if command -v "$cli_name" &> /dev/null; then
        echo "✓ $cli_name is installed"
        # Run version check
        $cli_name --version 2>/dev/null || $cli_name version 2>/dev/null || true
        return 0
    else
        echo "✗ $cli_name is not installed"
        return 1
    fi
}

# Example checks
check_cli "vercel" "vercel --version"
check_cli "supabase" "supabase --version"
check_cli "stripe" "stripe --version"
check_cli "gh" "gh --version"
check_cli "aws" "aws --version"
check_cli "railway" "railway --version"
check_cli "netlify" "netlify --version"
```

### Step 5: Check Authentication Status

Each CLI has a different way to check auth:

```bash
# Vercel
vercel whoami 2>/dev/null && echo "✓ Vercel authenticated" || echo "✗ Vercel not authenticated"

# Supabase
supabase projects list 2>/dev/null && echo "✓ Supabase authenticated" || echo "✗ Supabase not authenticated"

# Stripe
stripe config --list 2>/dev/null && echo "✓ Stripe authenticated" || echo "✗ Stripe not authenticated"

# GitHub
gh auth status 2>/dev/null && echo "✓ GitHub authenticated" || echo "✗ GitHub not authenticated"

# AWS
aws sts get-caller-identity 2>/dev/null && echo "✓ AWS authenticated" || echo "✗ AWS not authenticated"

# Railway
railway whoami 2>/dev/null && echo "✓ Railway authenticated" || echo "✗ Railway not authenticated"

# Netlify
netlify status 2>/dev/null && echo "✓ Netlify authenticated" || echo "✗ Netlify not authenticated"
```

### Step 6: Install Missing CLIs

If a CLI is not installed, offer to install:

```
AskUserQuestion: "The following CLIs are not installed: [list]. Install them?"
├── "Yes, install all" → Run install commands
├── "Let me install manually" → Show commands to copy
└── "Skip for now" → Continue without installing
```

Installation commands by platform (see [reference/tech-stack-clis.md](../reference/tech-stack-clis.md) for full list):

```bash
# npm-based CLIs
npm install -g vercel
npm install -g supabase
npm install -g @railway/cli
npm install -g netlify-cli
npm install -g @sentry/cli

# Homebrew CLIs (macOS)
brew install stripe/stripe-cli/stripe
brew install gh
brew install awscli
```

### Step 7: Authenticate CLIs

For CLIs that need authentication, run the auth command interactively:

```bash
# These commands are interactive - let them run in the terminal
vercel login
supabase login
stripe login
gh auth login
aws configure
railway login
netlify login
```

### Step 8: Document in CLAUDE.md

After CLI setup, document in CLAUDE.md:

```markdown
## Available CLIs

| Service | CLI | Status |
|---------|-----|--------|
| Vercel | `vercel` | ✓ Authenticated |
| Supabase | `supabase` | ✓ Authenticated |
| Stripe | `stripe` | ✓ Authenticated |
| GitHub | `gh` | ✓ Authenticated |

### CLI Usage Examples

- Deploy: `vercel --prod`
- Database migrations: `supabase db push`
- View Stripe events: `stripe events list`
- Create PR: `gh pr create`
```

## When to Fall Back to MCP

Only use MCP when:
1. No CLI exists for the service
2. The CLI doesn't support the needed operation
3. The operation requires complex multi-step orchestration

Example services that may need MCP:
- Some specialized APIs without CLIs
- Services with limited CLI functionality
- Browser-based operations (use Agent Browser instead)

## Service-Specific Notes

### Convex

Convex uses `npx convex` rather than a global CLI:

```bash
# Check if convex is available
npx convex --version

# Common commands
npx convex dev          # Start development server
npx convex deploy       # Deploy to production
npx convex dashboard    # Open dashboard
```

### Supabase

Supabase has both CLI and dashboard operations:

```bash
# Local development
supabase start          # Start local Supabase
supabase db reset       # Reset local database
supabase db push        # Push migrations to remote

# Project management
supabase projects list  # List projects
supabase link          # Link to remote project
```

### Vercel

```bash
# Deployment
vercel                  # Deploy preview
vercel --prod          # Deploy production
vercel env pull        # Pull environment variables

# Project info
vercel ls              # List deployments
vercel inspect [url]   # Inspect deployment
```

### Stripe

```bash
# Testing
stripe listen --forward-to localhost:3000/api/webhooks
stripe trigger payment_intent.succeeded

# Resources
stripe customers list
stripe products list
stripe prices list
```

## Output Format

Present CLI status in a clear table:

```
═══════════════════════════════════════════════════════════════════════════
CLI Discovery Results
═══════════════════════════════════════════════════════════════════════════

Service        CLI           Installed    Authenticated
───────────────────────────────────────────────────────────────────────────
Vercel         vercel        ✓            ✓
Supabase       supabase      ✓            ✗ Run: supabase login
Convex         npx convex    ✓            ✓
Stripe         stripe        ✗            -  Install: brew install stripe/stripe-cli/stripe
GitHub         gh            ✓            ✓
Sentry         sentry-cli    ✗            -  Install: npm i -g @sentry/cli

───────────────────────────────────────────────────────────────────────────
Summary: 4/6 installed, 3/4 authenticated
Action needed: Install 2 CLIs, authenticate 1 CLI
```

## Integration with Other Components

- **MCP Management**: Only enable MCP for services without usable CLIs
- **CLAUDE.md Writing**: Document available CLIs and their usage
- **Hooks Configuration**: Can add pre-push hooks that use CLIs (e.g., `vercel build`)
