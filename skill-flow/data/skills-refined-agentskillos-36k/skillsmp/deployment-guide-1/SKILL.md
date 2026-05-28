---
name: deployment-guide
description: Guide for deploying TrainTrack to Firebase Hosting and GitHub Pages, including build configuration and environment setup
---

This skill provides comprehensive guidance for deploying TrainTrack to production, covering Firebase Hosting, GitHub Pages, static export configuration, and CI/CD workflows.

## Deployment Overview

TrainTrack uses **static site generation** with Next.js `output: 'export'` configuration. The build outputs to an `out/` directory that can be deployed to various static hosting platforms.

**Supported Platforms:**
- Firebase Hosting (production)
- GitHub Pages (testing/dev)

## Static Export Configuration

**Next.js Config:** [next.config.mjs](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/next.config.mjs)

**Key Settings:**
```javascript
output: 'export',
trailingSlash: true,
images: { unoptimized: true },
ignoreBuildErrors: true
```

**Build Output:** `out/` directory

**Important Notes:**
- All routes are static (no server-side rendering)
- Images must be unoptimized for static export
- Query parameters work (used for edit booking with `?id=`)
- Trailing slash required for proper routing

## Firebase Hosting Deployment

### GitHub Actions Workflow

**File:** [.github/workflows/cloudrun-deploy.yml](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/.github/workflows/cloudrun-deploy.yml)

**Trigger:** Push to `master` branch

**Deployment Steps:**
1. Checkout code
2. Setup Node.js (version 20)
3. Install dependencies with `npm ci`
4. Create `.env` file from GitHub secrets
5. Build static export with `npm run build`
6. Deploy to Firebase Hosting

**GitHub Secrets Required:**
```
FIREBASE_SERVICE_ACCOUNT          # Service account JSON
FIREBASE_PROJECT_ID               # Firebase project ID
NEXT_PUBLIC_FIREBASE_API_KEY      # Firebase config
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN  # Firebase config
NEXT_PUBLIC_FIREBASE_PROJECT_ID   # Firebase config
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID
NEXT_PUBLIC_FIREBASE_APP_ID
NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID
GEMINI_API_KEY                    # For AI features
```

### Manual Deployment

**Prerequisites:**
- Firebase CLI installed
- Logged in with `firebase login`
- Firebase project configured

**Commands:**
```bash
# Build the static export
npm run build

# Deploy to Firebase Hosting
firebase deploy --only hosting
```

**Firebase Configuration:**

**Project Config:** [.firebaserc](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/.firebaserc)
```json
{
  "projects": {
    "default": "your-project-id"
  }
}
```

**Hosting Config:** [firebase.json](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/firebase.json)
```json
{
  "hosting": {
    "public": "out",
    "ignore": [
      "firebase.json",
      "**/.*",
      "**/node_modules/**"
    ],
    "rewrites": [
      {
        "source": "**",
        "destination": "/index.html"
      }
    ]
  }
}
```

**Rewrites Rule:** Ensures all routes serve `/index.html` for SPA-like behavior with client-side routing.

## GitHub Pages Deployment

### GitHub Actions Workflow

**File:** [.github/workflows/deploy-gh-pages.yml](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/.github/workflows/deploy-gh-pages.yml)

**Trigger:** Push to `dev` branch

**Deployment Steps:**
1. Checkout code
2. Setup Node.js (version 20)
3. Install dependencies with `npm ci`
4. Create `.env` file from GitHub secrets
5. Build with base path: `NEXT_PUBLIC_BASE_PATH: /TrainTrack`
6. Setup Pages
7. Upload artifact from `out/` directory
8. Deploy to GitHub Pages

**Base Path Configuration:**
- Required for GitHub Pages to work in a subdirectory
- Set as `NEXT_PUBLIC_BASE_PATH: /TrainTrack`
- Next.js uses this for asset paths

**Permissions:**
```yaml
permissions:
  contents: read
  pages: write
  id-token: write
```

**Concurrency Control:**
```yaml
concurrency:
  group: "pages"
  cancel-in-progress: false
```

## Build Commands

### Development Build
```bash
npm run dev
# Runs on port 9002
# Uses CSR with hot reload
```

### Production Build
```bash
npm run build
# Outputs to out/ directory
# Static export for deployment
```

### Type Checking
```bash
npm run typecheck
# TypeScript validation without build
```

### Linting
```bash
npm run lint
# ESLint validation
```

## Environment Variables

### Required Variables

**Firebase Configuration:**
```
NEXT_PUBLIC_FIREBASE_API_KEY=<api_key>
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=<project_id>.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=<project_id>
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=<project_id>.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=<sender_id>
NEXT_PUBLIC_FIREBASE_APP_ID=<app_id>
NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID=<measurement_id>
NEXT_PUBLIC_FIREBASE_DATABASE_ID=<database_id> # Optional
```

**AI Configuration:**
```
GEMINI_API_KEY=<your_gemini_api_key>
```

**GitHub Pages Specific:**
```
NEXT_PUBLIC_BASE_PATH=/TrainTrack
```

### Environment File Creation

**In CI/CD (GitHub Actions):**
```yaml
- name: Create .env file for build
  run: |
    echo "GEMINI_API_KEY=${{ secrets.GEMINI_API_KEY }}" >> .env
    echo "NEXT_PUBLIC_FIREBASE_API_KEY=${{ secrets.NEXT_PUBLIC_FIREBASE_API_KEY }}" >> .env
    # ... other variables
```

**Local Development:**
Create `.env.local` file in project root with all required variables.

## Build Process Details

### Static Export Generation

**Output Directory:** `out/`

**Contents:**
- `index.html` - Main entry point
- Static assets (CSS, JS, images)
- Pre-rendered pages
- `_next/static/` - Next.js static assets

**Route Handling:**
- All routes are pre-rendered
- Client-side navigation works with query parameters
- No server-side routes or API endpoints

### Image Optimization

**Important:** Images must be unoptimized for static export:
```javascript
images: { unoptimized: true }
```

**Why:** Next.js image optimization requires server-side processing, which isn't available in static exports.

**Workaround:**
- Use standard `<img>` tags
- Optimize images manually before adding to project
- Use image CDN services if needed

## Troubleshooting

### Build Errors

**TypeScript/ESLint Errors:**
```javascript
ignoreBuildErrors: true
```
This setting allows builds to proceed even if TypeScript/ESLint errors exist. Fix errors before production deployment.

**Missing Environment Variables:**
- Verify all `NEXT_PUBLIC_*` variables are set
- Check `.env` file exists in project root
- Ensure GitHub secrets are configured

**Static Export Failures:**
- Check for server-side code usage
- Verify no API routes exist
- Ensure all components use `"use client"` directive

### Deployment Errors

**Firebase Deployment Failures:**
- Verify `FIREBASE_SERVICE_ACCOUNT` secret is valid JSON
- Check Firebase project ID matches
- Ensure Firebase CLI is authenticated

**GitHub Pages Failures:**
- Verify Pages is enabled in repository settings
- Check `NEXT_PUBLIC_BASE_PATH` is set correctly
- Ensure branch permissions are configured

**Asset 404 Errors:**
- Verify `trailingSlash: true` in config
- Check asset paths include base path for GitHub Pages
- Ensure `public/` directory contains all assets

### Runtime Errors

**Firebase Authentication Issues:**
- Verify Firebase config is correct
- Check Firestore rules allow read access
- Ensure app is not blocked by CORS

**Routing Issues:**
- Check `trailingSlash` configuration
- Verify query parameters work for edit pages
- Ensure client-side navigation is working

**Data Not Loading:**
- Verify Firestore rules allow read access
- Check Firebase config is correct
- Ensure collections exist in Firestore

## Best Practices

### Before Deploying

1. **Test Locally:**
   ```bash
   npm run build
   npm run dev  # Test static build
   ```

2. **Run Type Checking:**
   ```bash
   npm run typecheck
   ```

3. **Run Linting:**
   ```bash
   npm run lint
   ```

4. **Verify Environment Variables:**
   - Check all required variables are set
   - Test Firebase connection locally
   - Verify API keys are valid

### CI/CD Best Practices

1. **Use Branch Protection:**
   - Require PR reviews before merging to `master`
   - Require status checks to pass

2. **Secrets Management:**
   - Never commit `.env` files
   - Use GitHub secrets for sensitive data
   - Rotate API keys regularly

3. **Build Caching:**
   - Use `actions/setup-node` with cache
   - Speeds up CI/CD runs

### Deployment Strategy

1. **Firebase Hosting (Production):**
   - Deploy from `master` branch
   - Use for production environment
   - Full Firebase integration

2. **GitHub Pages (Testing):**
   - Deploy from `dev` branch
   - Use for testing environment
   - Quick preview without Firebase

## Monitoring and Maintenance

### Build Status

- Check GitHub Actions tab for build status
- Monitor deployment logs for errors
- Review build times for performance issues

### Firebase Console

- Monitor Hosting usage
- Check Analytics data
- Review Authentication logs

### Performance Monitoring

- Use Firebase Performance Monitoring
- Monitor Core Web Vitals
- Track build size over time

## Rollback Procedures

### Firebase Hosting

```bash
# View deployment history
firebase hosting:rollback --project <project-id>

# Or deploy previous version
git checkout <previous-commit>
npm run build
firebase deploy --only hosting
```

### GitHub Pages

```bash
# Revert to previous commit
git revert <commit-hash>
git push origin <branch>
```

## Key Files Reference

- [next.config.mjs](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/next.config.mjs) - Build configuration
- [firebase.json](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/firebase.json) - Firebase hosting config
- [.firebaserc](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/.firebaserc) - Firebase project config
- [.github/workflows/cloudrun-deploy.yml](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/.github/workflows/cloudrun-deploy.yml) - Firebase deployment
- [.github/workflows/deploy-gh-pages.yml](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/.github/workflows/deploy-gh-pages.yml) - GitHub Pages deployment
- [package.json](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/package.json) - Build scripts
