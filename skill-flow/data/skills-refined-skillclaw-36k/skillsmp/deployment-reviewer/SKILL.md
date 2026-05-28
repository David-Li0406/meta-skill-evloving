---
name: deployment-reviewer
description: Reviews the potential-parakeet frontend deployment configuration, fixes the "Hello World" entry point issue, and provides setup guides for AWS, Cloudflare, and Neon/Supabase.
---

# Deployment Reviewer

## Overview

This skill helps review and fix the deployment configuration for the `potential-parakeet` frontend. It specifically addresses the issue where the static "Hello World" (or "QuantDash") HTML is served instead of the React application, and provides step-by-step guides for deploying to modern cloud platforms.

## Capability 1: Fix Frontend Entry Point (The "Hello World" Fix)

The most common issue in this codebase is `dashboard/index.html` not being linked to the React application in `dashboard/src`.

### Validation Step
Check if `dashboard/index.html` contains the following script tag just before the closing `</body>` tag:
```html
<script type="module" src="/src/index.tsx"></script>
```

### Fix Instructions
To switch from the static HTML view to the "Real" React App:
1.  Open `dashboard/index.html`.
2.  Ensure there is a root element: `<div id="root"></div>`.
3.  Add the script module link: `<script type="module" src="/src/index.tsx"></script>`.
4.  Remove conflicting static content (like the hardcoded "QuantDash" HTML) if it replaces the `#root` div. Usually, `index.html` should be empty except for the metadata and the `#root` div.

## Capability 2: Deployment Guides

### AWS Deployment (S3 + CloudFront)
1.  **Build**: Run `npm run build` in `dashboard/`. Output is in `dashboard/dist`.
2.  **S3**: Create a bucket (e.g., `parakeet-dashboard`). correctly verify `Block Public Access` settings (off if using direct S3 website hosting, on if using CloudFront OAI).
3.  **Upload**: Sync `dist/` content to S3 bucket.
4.  **CloudFront**: Create distribution pointing to S3 bucket.
    -   **Important**: Set "Default Root Object" to `index.html`.
    -   **Error Pages**: Configure 404 to return `index.html` (Status 200) for SPA routing.

### Cloudflare Pages Deployment
1.  **Connect**: Link GitHub repo to Cloudflare Pages.
2.  **Build Settings**:
    -   **Framework**: Vite
    -   **Build Command**: `npm run build`
    -   **Build Output Directory**: `dist` (or `dashboard/dist` if monorepo root is used).
3.  **Environment Variables**: Add needed vars from `.env` to Cloudflare project settings.

## Capability 3: Neon & Supabase Setup

### Environment Variables
The React app requires these variables (ensure they start with `VITE_`):

```bash
VITE_SUPABASE_URL=https://<project-ref>.supabase.co
VITE_SUPABASE_ANON_KEY=<your-anon-key>
# If using direct Postgres via Neon
DATABASE_URL=postgres://<user>:<password>@<host>/<dbname>?sslmode=require
```

### Verification
1.  Check `dashboard/.env` exists.
2.  Verify `vite.config.ts` exposes these if manually proxying, though Vite handles `VITE_` vars automatically.

## Tools
Run the included script to verify the local build environment:
`python scripts/verify_deployment.py`
