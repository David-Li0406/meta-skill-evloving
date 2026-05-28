---
name: hugo-deployment-aws
description: This skill should be used when the user mentions "deploy", "deployment", "serverless", "cloudfront", "s3 bucket", "github actions", "ci/cd", "pipeline", "production", "staging", "aws deploy", "cache invalidation", "cdn", "release", "publish site", "go live", or any deployment-related commands. Provides comprehensive AWS deployment workflow using Serverless Framework, GitHub Actions CI/CD, and CloudFront CDN.
---

# Hugo AWS Deployment Guide

## CRITICAL: Deployment Rules

**NEVER run `serverless deploy` manually from the command line.**

All deployments MUST go through GitHub CI. This ensures:
- Consistent build environment
- Proper secret management
- Audit trail of all deployments
- No accidental partial deployments
- Team visibility into deployment status

### The Only Deployment Workflow

```
1. Test locally with hugo serve
2. Validate content with hugo list all
3. Commit changes to develop branch
4. Push to GitHub
5. GitHub Actions handles build + deploy
6. Wait ~5 minutes for CloudFront invalidation
```

**Deployment = Push to develop branch. Nothing else.**

## Complete Deployment Workflow

### Step 1: Local Testing

Before committing, always verify your changes locally:

```bash
# Start development server
hugo serve --buildDrafts --buildFuture

# Check for content issues
hugo list all          # List all content
hugo list drafts       # Find unpublished drafts
hugo list future       # Find future-dated content
hugo list expired      # Find expired content

# Validate build succeeds
hugo --gc --minify     # Full production build locally
```

### Step 2: Validate Content

```bash
# Check for broken internal links (if htmltest is configured)
bun run test

# Verify no draft content will be published
hugo list drafts

# Check build output size
du -sh public/
```

### Step 3: Commit and Push

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "Add new blog post about XYZ"

# Push to develop branch (triggers deployment)
git push origin develop
```

### Step 4: Monitor Deployment

1. Go to GitHub repository > Actions tab
2. Watch the workflow run
3. Green checkmark = successful deployment
4. CloudFront invalidation takes ~5 minutes after workflow completes

## Serverless Framework Configuration

### serverless.yml Structure

```yaml
service: your-site-name
frameworkVersion: '3'

provider:
  name: aws
  region: us-east-1  # Required for CloudFront
  runtime: nodejs18.x

plugins:
  - serverless-s3-sync
  - serverless-cloudfront-invalidate

custom:
  siteName: your-site-name
  hostedZoneName: yourdomain.com
  aliasHostedZoneId: Z2FDTNDATAQYW2  # CloudFront's hosted zone ID
  aliasDNSName: !GetAtt CloudFrontDistribution.DomainName

  s3Sync:
    - bucketName: ${self:custom.siteName}
      localDir: public
      deleteRemoved: true
      defaultContentType: text/html
      params:
        # Long cache for versioned assets
        - "*.js":
            CacheControl: 'public, max-age=31536000, immutable'
        - "*.css":
            CacheControl: 'public, max-age=31536000, immutable'
        - "*.woff":
            CacheControl: 'public, max-age=31536000, immutable'
        - "*.woff2":
            CacheControl: 'public, max-age=31536000, immutable'
        - "*.png":
            CacheControl: 'public, max-age=31536000, immutable'
        - "*.jpg":
            CacheControl: 'public, max-age=31536000, immutable'
        - "*.jpeg":
            CacheControl: 'public, max-age=31536000, immutable'
        - "*.webp":
            CacheControl: 'public, max-age=31536000, immutable'
        - "*.avif":
            CacheControl: 'public, max-age=31536000, immutable'
        - "*.gif":
            CacheControl: 'public, max-age=31536000, immutable'
        - "*.ico":
            CacheControl: 'public, max-age=31536000, immutable'
        # Shorter cache for SVG (may contain dynamic content)
        - "*.svg":
            CacheControl: 'public, max-age=86400'
        # No cache for HTML (always fetch fresh)
        - "*.html":
            CacheControl: 'no-cache, no-store, must-revalidate'
        - "*.xml":
            CacheControl: 'public, max-age=3600'
        - "*.json":
            CacheControl: 'public, max-age=3600'

  cloudfrontInvalidate:
    - distributionIdKey: CloudFrontDistributionId
      items:
        - '/*'  # Full invalidation on every deploy

# Build hook - skipped when SKIP_BUILD=true (CI builds separately)
hooks:
  before:deploy:deploy:
    - ./build.sh
```

### Build Hook Script (build.sh)

```bash
#!/bin/bash
if [ "$SKIP_BUILD" = "true" ]; then
  echo "Skipping build (SKIP_BUILD=true)"
  exit 0
fi
hugo --gc --minify
```

## AWS Architecture

```
                    ┌─────────────────┐
                    │   Route53       │
                    │   (DNS)         │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   CloudFront    │
                    │   (CDN)         │
                    │                 │
                    │ - HTTP/2 + HTTP/3
                    │ - HTTPS redirect│
                    │ - gzip/brotli   │
                    │ - URL rewrite   │
                    │   function      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   S3 Bucket     │
                    │   (Private)     │
                    │                 │
                    │ - OAC access    │
                    │ - Cache headers │
                    │ - Versioning    │
                    └─────────────────┘
```

### Key Architecture Points

1. **S3 Bucket is Private**: No public access, only CloudFront can read via Origin Access Control (OAC)
2. **CloudFront URL Rewrite Function**: Handles clean URLs, adding `/index.html` to directory requests
3. **HTTPS Everywhere**: HTTP automatically redirects to HTTPS
4. **Edge Locations**: Content served from nearest CloudFront edge location

## Cache Headers Strategy

### Long Cache (1 Year) - Immutable Assets

Files that include content hashes in their names can be cached forever:

```
*.js, *.css       → public, max-age=31536000, immutable
*.woff, *.woff2   → public, max-age=31536000, immutable
*.png, *.jpg      → public, max-age=31536000, immutable
*.webp, *.avif    → public, max-age=31536000, immutable
*.gif, *.ico      → public, max-age=31536000, immutable
```

### Medium Cache (1 Day) - Semi-Dynamic

```
*.svg             → public, max-age=86400
```

### Short Cache (1 Hour) - Feeds and Data

```
*.xml (RSS/sitemap) → public, max-age=3600
*.json              → public, max-age=3600
```

### No Cache - HTML Pages

```
*.html            → no-cache, no-store, must-revalidate
```

### Why Full Cache Invalidation?

Every deployment triggers `/*` invalidation because:
- Hugo's fingerprinting means asset URLs change when content changes
- HTML files reference new asset URLs
- Full invalidation ensures consistency
- CloudFront's first 1000 invalidations/month are free

## GitHub Actions Workflow

### Complete Workflow File (.github/workflows/deploy.yml)

```yaml
name: Deploy to AWS

on:
  push:
    branches:
      - develop
  workflow_dispatch:
    inputs:
      purge_cache:
        description: 'Force full cache purge'
        required: false
        default: 'false'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Needed for .GitInfo

      - name: Setup Bun
        uses: oven-sh/setup-bun@v1
        with:
          bun-version: latest

      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v3
        with:
          hugo-version: 'latest'
          extended: true

      - name: Cache Hugo resources
        uses: actions/cache@v4
        with:
          path: resources
          key: hugo-resources-${{ hashFiles('assets/**') }}
          restore-keys: |
            hugo-resources-

      - name: Install dependencies
        run: bun install

      - name: Build site
        run: hugo --gc --minify
        env:
          HUGO_ENV: production

      - name: Deploy to AWS
        run: bunx serverless deploy --stage production
        env:
          SKIP_BUILD: 'true'  # Already built above
          SERVERLESS_ACCESS_KEY: ${{ secrets.SERVERLESS_ACCESS_KEY }}
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

### Required GitHub Secrets

Configure these in Repository Settings > Secrets and Variables > Actions:

| Secret | Description |
|--------|-------------|
| `SERVERLESS_ACCESS_KEY` | Serverless Framework dashboard key |
| `AWS_ACCESS_KEY_ID` | AWS IAM access key |
| `AWS_SECRET_ACCESS_KEY` | AWS IAM secret key |

### IAM Permissions Required

The AWS IAM user needs permissions for:
- S3: Full access to the site bucket
- CloudFront: CreateInvalidation, GetDistribution
- Route53: (if managing DNS)
- CloudFormation: Full access (Serverless uses this)
- Lambda@Edge: (if using edge functions)

### Manual Trigger with Cache Purge

For emergencies or cache issues, trigger manually from GitHub Actions:
1. Go to Actions > Deploy to AWS
2. Click "Run workflow"
3. Set `purge_cache` to `true`
4. Click "Run workflow"

## Troubleshooting

### CI Build Failed

1. Check GitHub Actions logs for the specific error
2. Common issues:
   - Hugo version mismatch
   - Missing dependencies in package.json
   - Invalid front matter in content files
   - Asset pipeline errors (missing source files)

```bash
# Reproduce locally
hugo --gc --minify
```

### Site Not Updating After Deploy

CloudFront invalidation takes time:
1. Wait 5 minutes after successful deploy
2. Check invalidation status in AWS Console > CloudFront > Invalidations
3. Hard refresh browser: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)
4. Try incognito/private window

### 404 Errors on Pages

Check Hugo URL configuration:

```bash
# In hugo.toml
uglyURLs = false  # Use /page/ not /page.html
```

Verify CloudFront function is handling URL rewrites:
- `/about` should internally request `/about/index.html`
- `/blog/post` should request `/blog/post/index.html`

### Cache Issues / Stale Content

```bash
# Option 1: Manual workflow with purge
# Go to GitHub Actions > Run workflow > purge_cache = true

# Option 2: Check what's actually in S3
aws s3 ls s3://your-bucket-name/path/to/file

# Option 3: Check CloudFront cache behavior
aws cloudfront get-distribution-config --id YOUR_DIST_ID
```

### Serverless Deployment Errors

**Never debug by running serverless locally.** Instead:

1. Check CI logs for the exact error
2. Verify AWS credentials are valid
3. Check CloudFormation stack status in AWS Console
4. Look for resource limits (S3 bucket name taken, etc.)

### DNS Not Resolving

1. Verify Route53 hosted zone matches domain
2. Check nameservers at registrar point to Route53
3. Use `dig yourdomain.com` to check propagation
4. DNS changes can take up to 48 hours (usually faster)

## Local Development vs Production

| Aspect | Local (`hugo serve`) | Production (CI Deploy) |
|--------|---------------------|----------------------|
| Base URL | `localhost:1313` | Your domain |
| Drafts | Included | Excluded |
| Future posts | Included | Excluded |
| Minification | Off | On |
| Fingerprinting | Off | On |
| Source maps | Available | Stripped |

## Emergency Rollback

If a bad deployment goes out:

1. **Quick fix**: Revert commit and push
   ```bash
   git revert HEAD
   git push origin develop
   ```

2. **Immediate rollback**: Use AWS Console
   - Go to S3 bucket
   - Enable versioning (if not already)
   - Restore previous versions of affected files
   - Create CloudFront invalidation

3. **Full rollback via CI**:
   ```bash
   git checkout <previous-good-commit>
   git push -f origin develop  # Caution: force push
   ```

## Cost Optimization

- CloudFront: First 1TB/month is free tier eligible
- S3: Minimal cost for static sites (~$0.023/GB/month)
- Invalidations: First 1000 paths/month free
- Route53: $0.50/hosted zone/month

**Tip**: Use `hugo --gc` to clean up unused cache files before deploy.
