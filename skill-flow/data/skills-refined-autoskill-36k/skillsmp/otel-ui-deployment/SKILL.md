---
name: otel-ui-deployment
description: Deploy and manage otel-ui React application with OAuth2 authentication. Covers version updates, authentication fixes, Docker builds, and GitOps deployments to k8s-pi5-cluster.
---

# otel-ui Deployment Workflow

This skill manages the complete deployment lifecycle of the otel-ui React application, from code changes to production deployment on k8s-pi5-cluster.

## When to Use

Use this skill when you need to:

- Fix authentication issues (OAuth2/Cognito logout, callback, token handling)
- Deploy a new version of otel-ui
- Update authentication configuration (Cognito settings, redirect URIs)
- Troubleshoot login/logout flows
- Build and push Docker images
- Update Kubernetes manifests via GitOps

## Architecture Overview

```text
User → ui.lab.informationcart.com (nginx ingress)
  → oauth2-proxy (ingress-level auth)
    → otel-ui pods (React SPA in nginx)
      → otel-demo API (Flask backend)
        → PostgreSQL database
```

**Key Components**:

- **Frontend**: React + TypeScript + Vite
- **Auth**: AWS Cognito OAuth2/PKCE via `oidc-client-ts`
- **Deployment**: Docker (nginx) → Kubernetes (2 replicas)
- **GitOps**: GitHub → Argo CD auto-sync
- **Domain**: ui.lab.informationcart.com (MetalLB 192.168.1.100)

## Repository Structure

```text
otel-ui/                          # Frontend React app
├── src/
│   ├── services/
│   │   └── auth.ts              # OAuth2/PKCE authentication
│   ├── config/
│   │   └── runtime.ts           # Runtime config from window
│   └── components/              # React components
├── public/
│   └── config.js                # Injected at runtime by nginx
├── VERSION                       # Semver version
├── package.json                  # NPM dependencies
└── scripts/
    └── update-version.sh        # Automated version updater

k8s-gitops/                      # GitOps manifests
└── apps/base/otel-ui/
    ├── VERSION                   # Deployed version
    ├── deployment.yaml          # K8s deployment
    ├── ingress.yaml             # Ingress with oauth2-proxy
    ├── configmap.yaml           # Runtime config injection
    └── update-version.sh        # K8s manifest updater
```

## Common Tasks

### Task 1: Fix Authentication Issues

**Symptoms**:

- Logout shows Cognito error dialog
- Callback fails with "parameter not present" errors
- Users stuck on login redirect loop

**Root Causes**:

- Incorrect logout URL format (OAuth2 params on Cognito logout endpoint)
- Missing/incorrect redirect_uri parameters
- Malformed callback URLs

**Diagnosis**:

1. Check browser console for errors
2. Check Network tab for failed redirects (302, 400)
3. Verify localStorage has user tokens: `localStorage.getItem('oidc.user:...')`

**Fix Pattern**:

```typescript
// src/services/auth.ts

// ❌ BAD: oidc-client-ts adds OAuth2 params
await this.userManager.signoutRedirect();

// ✅ GOOD: Manual Cognito logout URL
await this.userManager.removeUser();
const logoutUrl = `https://${cognitoDomain}/logout?client_id=${clientId}&logout_uri=${encodeURIComponent(origin)}`;
window.location.href = logoutUrl;
```

**Common Fixes**:

1. **Logout URL**: Use manual redirect, not `signoutRedirect()`
2. **Callback handling**: Ensure `handleCallback()` called on `/callback` route
3. **Token storage**: Verify `WebStorageStateStore` uses `localStorage`
4. **CORS**: Check oauth2-proxy allows preflight OPTIONS requests

### Task 2: Deploy New Version

**Full Deployment Workflow**:

```bash
# 1. Make code changes in otel-ui repository
cd /home/ubuntu/git/otel-ui

# 2. Commit changes to develop branch
git checkout develop
git add src/services/auth.ts
git commit -m "fix: Correct logout URL construction"

# 3. Update version (semver: major.minor.patch)
bash scripts/update-version.sh 1.0.33

# 4. Commit version bump
git add VERSION package.json
git commit -m "chore: Bump version to 1.0.33"

# 5. Push to develop
git push origin develop

# 6. Tag release
git tag v1.0.33
git push origin v1.0.33

# 7. Merge to main (triggers GitHub Actions Docker build)
git checkout main
git merge develop
git push origin main

# 8. Wait for GitHub Actions to build and push Docker image
# Check: https://github.com/stuartshay/otel-ui/actions
# Docker Hub: https://hub.docker.com/r/stuartshay/otel-ui

# 9. Update k8s-gitops manifests
cd /home/ubuntu/git/k8s-gitops/apps/base/otel-ui
./update-version.sh 1.0.33

# 10. Commit and push k8s manifests
cd /home/ubuntu/git/k8s-gitops
git add -A
git commit -m "chore: Update otel-ui to v1.0.33"
git push origin master

# 11. Argo CD auto-syncs (or manual sync)
kubectl rollout status deployment otel-ui -n otel-ui --timeout=120s

# 12. Verify deployment
kubectl get pods -n otel-ui
curl -sI https://ui.lab.informationcart.com/
```

**Semver Guidelines**:

- **Patch** (1.0.x): Bug fixes, auth tweaks, config updates
- **Minor** (1.x.0): New features, UI components, API endpoints
- **Major** (x.0.0): Breaking changes, major redesigns

### Task 3: Update Cognito Configuration

When changing OAuth2 settings (redirect URIs, client IDs):

**1. Update AWS Cognito User Pool**:

- Sign in to AWS Console
- Cognito → User Pools → us-east-1_ZL7M5Qa7K
- App clients → 5j475mtdcm4qevh7q115qf1sfj
- Update:
  - Callback URLs
  - Sign-out URLs
  - Allowed OAuth flows (Authorization code grant)
  - Allowed OAuth scopes (openid, profile, email)

**2. Update k8s ConfigMap**:

```bash
cd /home/ubuntu/git/k8s-gitops/apps/base/otel-ui

# Edit configmap.yaml
vim configmap.yaml

# Update values:
# VITE_COGNITO_DOMAIN
# VITE_COGNITO_CLIENT_ID
# VITE_COGNITO_REDIRECT_URI
# VITE_COGNITO_ISSUER

# Commit and deploy
git add configmap.yaml
git commit -m "feat: Update Cognito configuration"
git push origin master

# Force pod restart to pick up new config
kubectl rollout restart deployment otel-ui -n otel-ui
```

**3. Update Documentation**:

- Update [docs/authentication.md](../../docs/authentication.md)
- Update [.env.example](../../../.env.example)

### Task 4: Test Authentication Flow

**Manual Testing Checklist**:

```bash
# 1. Login Flow
Open https://ui.lab.informationcart.com
Click login
  → Redirects to Cognito
Enter credentials
  → Redirects to /callback?code=xxx
  → Exchanges code for tokens
  → Redirects to dashboard
Check localStorage: localStorage.getItem('oidc.user:...')

# 2. API Calls
Open browser DevTools → Network tab
Trigger API call (e.g., /info endpoint)
Verify headers:
  Authorization: Bearer <token>

# 3. Token Refresh
Wait for token expiry (1 hour) or simulate:
  localStorage.removeItem('oidc.user:...')
Trigger API call
  → Should auto-refresh or redirect to login

# 4. Logout Flow
Click logout
  → Clears localStorage
  → Redirects to Cognito logout
  → Redirects back to homepage
Verify localStorage cleared
Try accessing protected route → should redirect to login
```

**Automated Testing**:

```bash
cd /home/ubuntu/git/otel-ui

# Run Playwright E2E tests
npx playwright test tests/auth-flow.spec.ts

# Test coverage includes:
# - Login redirect
# - Callback handling
# - Token storage
# - API authentication
# - Logout
```

### Task 5: Rollback Deployment

If a new version has issues:

```bash
# 1. Find last working version
cd /home/ubuntu/git/k8s-gitops
git log --oneline apps/base/otel-ui/VERSION | head -10

# 2. Revert to previous version (e.g., 1.0.32)
cd apps/base/otel-ui
./update-version.sh 1.0.32

# 3. Commit and push
cd /home/ubuntu/git/k8s-gitops
git add -A
git commit -m "revert: Rollback otel-ui to v1.0.32"
git push origin master

# 4. Verify rollout
kubectl rollout status deployment otel-ui -n otel-ui
kubectl get pods -n otel-ui -o wide

# 5. Check logs for issues
kubectl logs -n otel-ui -l app=otel-ui --tail=50
```

## Configuration Reference

### Environment Variables

**Production** (k8s ConfigMap):

```bash
VITE_API_BASE_URL=https://otel.lab.informationcart.com
VITE_COGNITO_DOMAIN=homelab-auth.auth.us-east-1.amazoncognito.com
VITE_COGNITO_CLIENT_ID=5j475mtdcm4qevh7q115qf1sfj
VITE_COGNITO_REDIRECT_URI=https://ui.lab.informationcart.com/callback
VITE_COGNITO_ISSUER=https://cognito-idp.us-east-1.amazonaws.com/us-east-1_ZL7M5Qa7K
VITE_APP_VERSION=1.0.33
```

**Development** (.env.local):

```bash
VITE_API_BASE_URL=http://localhost:8080
VITE_COGNITO_DOMAIN=homelab-auth.auth.us-east-1.amazoncognito.com
VITE_COGNITO_CLIENT_ID=5j475mtdcm4qevh7q115qf1sfj
VITE_COGNITO_REDIRECT_URI=http://localhost:5173/callback
VITE_COGNITO_ISSUER=https://cognito-idp.us-east-1.amazonaws.com/us-east-1_ZL7M5Qa7K
VITE_APP_VERSION=dev
```

### AWS Cognito Details

| Setting       | Value                                                                         |
| ------------- | ----------------------------------------------------------------------------- |
| User Pool ID  | us-east-1_ZL7M5Qa7K                                                           |
| Region        | us-east-1                                                                     |
| Client ID     | 5j475mtdcm4qevh7q115qf1sfj                                                    |
| Client Type   | Public (PKCE)                                                                 |
| Domain        | homelab-auth.auth.us-east-1.amazoncognito.com                                 |
| Callback URLs | https://ui.lab.informationcart.com/callback<br>http://localhost:5173/callback |
| Sign-out URLs | https://ui.lab.informationcart.com<br>http://localhost:5173                   |
| OAuth Flows   | Authorization code grant                                                      |
| OAuth Scopes  | openid, profile, email                                                        |

### Kubernetes Resources

| Resource   | Namespace      | Replicas | Image                      |
| ---------- | -------------- | -------- | -------------------------- |
| Deployment | otel-ui        | 2        | stuartshay/otel-ui:1.0.33  |
| Service    | otel-ui        | -        | ClusterIP :80              |
| Ingress    | otel-ui        | -        | ui.lab.informationcart.com |
| ConfigMap  | otel-ui-config | -        | Runtime environment vars   |

## Troubleshooting Guide

### Issue: Logout shows error dialog

**Error**: "Required String parameter 'response_type' is not present"

**Cause**: `oidc-client-ts` `signoutRedirect()` adds OAuth2 params to Cognito logout URL

**Fix**: Use manual logout URL construction (see Task 1)

### Issue: Callback fails after login

**Error**: "Failed to handle OAuth callback"

**Cause**:

- Callback URL not registered in Cognito
- State parameter mismatch
- CORS blocking token exchange

**Fix**:

1. Verify callback URL in Cognito matches exactly
2. Check browser console for specific error
3. Verify oauth2-proxy CORS settings allow POST

### Issue: Token refresh fails

**Error**: "Silent renew error"

**Cause**:

- Refresh token expired (30 days)
- Missing `silent-renew.html` file
- CORS blocking renewal request

**Fix**:

1. Ensure `public/silent-renew.html` exists
2. Check refresh token expiry in localStorage
3. Force re-login if refresh token expired

### Issue: Docker build fails

**Error**: ImagePullBackOff in Kubernetes

**Cause**: GitHub Actions build failed or image not pushed

**Fix**:

1. Check GitHub Actions: https://github.com/stuartshay/otel-ui/actions
2. Verify Docker Hub has image: https://hub.docker.com/r/stuartshay/otel-ui/tags
3. Manually build and push if needed:

   ```bash
   cd /home/ubuntu/git/otel-ui
   docker build -t stuartshay/otel-ui:1.0.33 .
   docker push stuartshay/otel-ui:1.0.33
   ```

### Issue: Argo CD not syncing

**Cause**: Auto-sync disabled or sync policy misconfigured

**Fix**:

```bash
# Check Argo CD app status
kubectl get application apps -n argocd -o yaml | grep syncPolicy

# Manual sync
kubectl apply -k /home/ubuntu/git/k8s-gitops/clusters/k8s-pi5-cluster/apps/
```

## Related Documentation

- [otel-ui README](../../../README.md)
- [Authentication Guide](../../docs/authentication.md)
- [Project Plan](../../docs/project-plan.md)
- [k8s-gitops README](../../../../k8s-gitops/README.md)
- [otel-demo API Docs](https://otel.lab.informationcart.com/apidocs)

## Version History

| Version | Date       | Changes                                  |
| ------- | ---------- | ---------------------------------------- |
| 1.0.33  | 2026-01-23 | Fixed logout URL - removed OAuth2 params |
| 1.0.32  | 2026-01-23 | Added logout redirect_uri parameter      |
| 1.0.31  | 2026-01-23 | Database endpoint path fixes             |
| 1.0.29  | 2026-01-20 | Initial authentication implementation    |

## Quick Reference Commands

```bash
# Check deployed version
kubectl get deployment otel-ui -n otel-ui -o jsonpath='{.spec.template.spec.containers[0].image}'

# View logs
kubectl logs -n otel-ui -l app=otel-ui -f

# Restart deployment
kubectl rollout restart deployment otel-ui -n otel-ui

# Check ingress
kubectl get ingress otel-ui -n otel-ui

# Test endpoint
curl -sI https://ui.lab.informationcart.com/

# Check Argo CD sync status
kubectl get application apps -n argocd

# View pod details
kubectl describe pod -n otel-ui -l app=otel-ui
```
