---
name: dev-parity-guard
description: Maintains parity between development and production environments by validating scripts, proxies, and project structure.
---

# Dev Parity Guard Skill

This skill prevents regressions by ensuring the local development environment correctly mirrors the production "save point" and incorporates all critical architectural fixes.

## Critical Parity Rules

### 1. Script Integrity (package.json)
The `dev` script must ALWAYS support API routes.
- **Rule**: `scripts.dev` should be `"vercel dev"`.
- **Why**: Standard `vite` server ignores `/api` directory, leading to 404s/500s on checkout, mail, and image streaming.
- **Verification**: `grep '"dev": "vercel dev"' package.json`

### 2. API Proxying (vite.config.ts)
The frontend must correctly route API calls to the local backend during development.
- **Rule**: Ensure `server.proxy` include `/api/gallery` and `/api/photos` targeting `http://localhost:3001`.
- **Reason**: Local development (port 3000) needs to talk to the local background server (port 3001) for heavy lifting like image processing.

### 3. Image Delivery Consistency
High-resolution images must be proxied to avoid Google Drive 3rd-party cookie blocks.
- **Rule**: ALWAYS use `/api/gallery/stream?fileId=...` instead of direct Drive URLs in `src/components/`.
- **Detection**: Check `PhotoGallery.tsx` and `PhotoLightbox.tsx` for direct Drive links.

### 4. Project Root Awareness
Commands must be run from the repository root.
- **Rule**: Never run `npm` or `git` from the user home directory.
- **Target Dir**: `/Users/thelostunfounds/thelostandunfounds`

## Pre-Flight Checklist (Run Before Every Session)
- [ ] **Sync Branch**: `git pull origin main` to get the latest "save point".
- [ ] **Check Port 3000**: `lsof -ti:3000` (Stop existing rogue servers).
- [ ] **Validate Env**: `./scripts/validate-env.sh --local`
- [ ] **Check Dependencies**: `npm install` if `package.json` changed.

## Automated Verification
Run the parity validation script to check for common regressions:
```bash
./scripts/validate-parity.sh
```

## Regression Prevention Workflow
1. **Commit**: Before committing, verify the change works locally with `vercel dev`.
2. **Deploy**: After deployment, verify production URL.
3. **Save Point**: Immediately sync your local branch with the deployed `main` branch.
