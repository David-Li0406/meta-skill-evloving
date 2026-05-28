# Vercel CLI Complete Reference

<deployment_commands>

## List Deployments

```bash
vercel ls                              # List all deployments
vercel ls --prod                       # Production only
vercel ls --meta key=value            # Filter by metadata
vercel ls --output json               # JSON output
vercel ls --scope team-slug           # Specific team
```

## Inspect Deployment

```bash
vercel inspect <deployment-url>        # Full deployment details
vercel inspect <deployment-url> --json # JSON output

# Output includes:
# - Build command and output
# - Environment variables used
# - Functions and routes
# - Error messages if failed
```

## Runtime Logs

```bash
vercel logs <deployment-url>           # Stream logs (5 min max)
vercel logs <deployment-url> --json   # JSON format
vercel logs <deployment-url> | jq 'select(.level == "warning")'  # Filter warnings
```

</deployment_commands>

<build_commands>

## Local Build

```bash
vercel build                           # Build with preview env
vercel build --prod                    # Build with production env
vercel build --debug                   # Verbose output
vercel build --yes                     # Skip prompts, auto-pull env
vercel build --target staging         # Custom environment
```

## Build Output

Build artifacts are placed in `.vercel/output/` following Build Output API v3:

```
.vercel/output/
├── config.json
├── static/           # Static files
└── functions/        # Serverless functions
```

</build_commands>

<deploy_commands>

## Deploy Options

```bash
vercel deploy                          # Deploy to preview
vercel deploy --prod                   # Deploy to production
vercel deploy --prebuilt              # Deploy pre-built output
vercel deploy --force                  # Skip build cache
vercel deploy --with-cache            # Keep cache with --force
vercel deploy --logs                   # Show build logs
vercel deploy --no-wait               # Don't wait for completion
vercel deploy --archive tgz           # Compress for large projects
vercel deploy -e KEY=value            # Runtime env var
vercel deploy --build-env KEY=value   # Build-time env var
vercel deploy --regions iad1          # Specify function region
vercel deploy --target staging        # Custom environment
vercel deploy --skip-domain           # Don't assign domains (with --prod)
vercel deploy --meta key=value        # Add metadata
```

## Deploy from CI

```bash
# In CI, use token
VERCEL_TOKEN=xxx vercel deploy --token=$VERCEL_TOKEN

# Or with project linking
vercel link --yes
vercel deploy --yes
```

</deploy_commands>

<environment_commands>

## Environment Variables

```bash
vercel env ls                          # List all env vars
vercel env ls production              # Production only
vercel env add                        # Add interactively
vercel env add SECRET production      # Add to specific env
vercel env rm SECRET                  # Remove
vercel env pull                       # Pull to .env.local
vercel env pull .env                  # Pull to specific file
```

## Pull Project Settings

```bash
vercel pull                            # Pull env vars + settings
vercel pull --yes                      # Skip confirmation
vercel pull --environment production  # Specific environment
```

</environment_commands>

<project_commands>

## Project Management

```bash
vercel project ls                      # List projects
vercel project add                     # Create project
vercel project rm <name>              # Remove project
vercel link                           # Link current directory
vercel link --yes                     # Auto-confirm
vercel unlink                         # Unlink project
```

## Domain Management

```bash
vercel domains ls                      # List domains
vercel domains add <domain>           # Add domain
vercel domains rm <domain>            # Remove domain
vercel domains inspect <domain>       # Domain details
vercel alias <deployment> <domain>    # Alias deployment
```

</project_commands>

<debugging_commands>

## Debug Build Issues

```bash
# 1. Pull latest settings
vercel pull --yes

# 2. Build locally with debug
vercel build --debug 2>&1 | tee build.log

# 3. Check for specific errors
grep -i "error\|failed\|warning" build.log

# 4. Check memory usage during build
VERCEL_DEBUG_MEMORY_REPORT=1 vercel build
```

## Debug Runtime Issues

```bash
# Stream logs and filter errors
vercel logs <url> --json | jq 'select(.level == "error")'

# Get deployment events
vercel inspect <url> --json | jq '.events'
```

## Force Fresh Build

```bash
# Skip all caches
vercel deploy --force

# Or set env var
VERCEL_FORCE_NO_BUILD_CACHE=1 vercel deploy
```

</debugging_commands>

<global_options>

## Global Options (apply to all commands)

```bash
--cwd <dir>           # Set working directory
--debug               # Debug output
--global-config <dir> # Global config directory
--help                # Show help
--local-config <file> # Local config file
--no-color            # Disable colors
--scope <team>        # Team scope
--token <token>       # Auth token
```

</global_options>

<ci_integration>

## CI/CD Integration

```bash
# GitHub Actions example
- name: Deploy to Vercel
  run: |
    npm i -g vercel
    vercel pull --yes --environment=production --token=${{ secrets.VERCEL_TOKEN }}
    vercel build --prod --token=${{ secrets.VERCEL_TOKEN }}
    vercel deploy --prebuilt --prod --token=${{ secrets.VERCEL_TOKEN }}

# Or use official action
- uses: amondnet/vercel-action@v25
  with:
    vercel-token: ${{ secrets.VERCEL_TOKEN }}
    vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
    vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
    vercel-args: '--prod'
```

</ci_integration>
