---
name: otel-ui-enhancement-workflow
description: Standard workflow for planning, implementing, testing, and deploying enhancements to otel-ui. Covers feature development, bug fixes, and configuration changes with proper versioning and GitOps deployment.
---

# otel-ui Enhancement Workflow

This skill provides the standard workflow for creating any enhancement, feature, or fix for the otel-ui React application.

## When to Use

Use this skill when you need to:

- Implement a new React component or feature
- Fix bugs in existing functionality
- Update dependencies or configurations
- Make authentication improvements
- Add new API integrations
- Update styling or UI/UX

## Standard Enhancement Workflow

### Step 1: Plan the Enhancement

**Define the scope**:

```markdown
## Enhancement: [Brief Title]

**Problem/Need**: What issue are we solving or feature adding?

**Proposed Solution**: High-level approach

**Affected Components**:

- [ ] Frontend (React components)
- [ ] Authentication (src/services/auth.ts)
- [ ] API Client (src/services/api.ts)
- [ ] Configuration (ConfigMap, .env)
- [ ] Documentation

**Estimated Effort**: X hours

**Version Impact**: Patch/Minor/Major (see semver guidelines)
```

**Semver Guidelines**:

- **Patch (x.y.Z)**: Bug fixes, auth tweaks, config updates, documentation
- **Minor (x.Y.0)**: New features, components, API endpoints, non-breaking changes
- **Major (X.0.0)**: Breaking changes, major redesigns, API contract changes

**Update project-plan.md**:

- Add task to appropriate section (In Progress or Pending)
- Link to related GitHub issue if exists

### Step 2: Set Up Development Environment

**Branch Strategy**:

```bash
cd /home/ubuntu/git/otel-ui

# Ensure on latest develop
git checkout develop
git pull origin develop

# Create feature branch
git checkout -b feature/brief-name
# or
git checkout -b fix/issue-description
```

**Start Development Server**:

```bash
# Activate environment
source setup.sh  # or ./setup.sh

# Start dev server (http://localhost:5173)
npm run dev

# In another terminal - start API backend if needed
cd /home/ubuntu/git/otel-demo
source venv/bin/activate
python run.py  # http://localhost:8080
```

### Step 3: Implement the Enhancement

**Development Checklist**:

- [ ] **Write Code**
  - Follow TypeScript strict mode
  - Use existing patterns from codebase
  - Keep components small and focused
  - Extract reusable logic to hooks or utilities

- [ ] **Type Safety**
  - Use types from `@stuartshay/otel-types` for API
  - Define interfaces for component props
  - Avoid `any` type - use `unknown` if necessary

- [ ] **Error Handling**
  - Add try/catch blocks for async operations
  - Display user-friendly error messages
  - Log errors to console for debugging
  - Consider error boundaries for component crashes

- [ ] **Testing During Development**

  ```bash
  # Type check
  npx tsc --noEmit

  # Lint
  npm run lint:all

  # Format
  npm run format

  # Test in browser
  # - Manual testing of new functionality
  # - Check browser console for errors
  # - Test in different scenarios
  ```

**Common Code Patterns**:

```typescript
// API Client Call
import { apiClient } from '../services/api';

const fetchData = async () => {
  try {
    const response = await apiClient.get('/endpoint');
    setData(response.data);
  } catch (error) {
    console.error('Failed to fetch data:', error);
    setError('Unable to load data');
  }
};

// Auth-Protected Component
import { useAuth } from '../contexts/AuthContext';

const ProtectedComponent = () => {
  const { user, isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }

  return <div>Protected content</div>;
};

// Environment Config
import { getConfig } from '../config/runtime';

const apiUrl = getConfig('API_BASE_URL');
```

### Step 4: Test Locally

**Pre-commit Testing**:

```bash
# 1. Type check
npm run type-check

# 2. Lint all code
npm run lint:all

# 3. Format code
npm run format

# 4. Build for production (catch build errors)
npm run build

# 5. Preview production build
npm run preview
# Open http://localhost:4173

# 6. Manual testing checklist
# - Login flow works
# - New feature works as expected
# - Existing features not broken (smoke test)
# - No console errors
# - Mobile responsive (resize browser)
```

**Optional: Playwright E2E Tests**:

```bash
# Run existing tests
npx playwright test

# Run specific test file
npx playwright test tests/auth-flow.spec.ts

# Run in headed mode (see browser)
npx playwright test --headed

# Debug mode
npx playwright test --debug
```

### Step 5: Commit Changes

**Commit Message Format**:

```text
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks (deps, config, tooling)
- `perf`: Performance improvements

**Examples**:

```bash
# Feature
git commit -m "feat(dashboard): Add user statistics widget

Display user activity stats on dashboard:
- Total API calls count
- Recent trace IDs
- Success/error rate chart

Closes #42"

# Bug fix
git commit -m "fix(auth): Prevent token refresh loop on 401

Token refresh was triggering multiple times on API 401 errors,
causing infinite loop. Now debounce refresh calls and only
retry once before forcing re-login."

# Documentation
git commit -m "docs: Update authentication.md with PKCE flow

Add detailed PKCE flow diagram and troubleshooting steps
for common Cognito integration issues."
```

**Commit Workflow**:

```bash
# Stage changes
git add src/components/Dashboard.tsx
git add src/services/api.ts

# Commit with message
git commit -m "feat(dashboard): Add user statistics widget"

# Pre-commit hooks will run automatically:
# - ESLint
# - Prettier
# - Markdownlint (for .md files)
# - Type check
```

### Step 6: Version and Tag

**Determine Version Bump**:

```bash
# Current version
cat VERSION
# Example: 1.0.33

# Decide new version based on change:
# - Patch: 1.0.34 (bug fix)
# - Minor: 1.1.0 (new feature)
# - Major: 2.0.0 (breaking change)
```

**Update Version**:

```bash
# Update version files (VERSION, package.json)
bash scripts/update-version.sh 1.1.0

# Commit version bump
git add VERSION package.json
git commit -m "chore: Bump version to 1.1.0"

# Push feature branch
git push origin feature/brief-name

# Create PR to develop (if using PR workflow)
# OR merge directly to develop
git checkout develop
git merge feature/brief-name
git push origin develop

# Tag release
git tag v1.1.0
git push origin v1.1.0
```

### Step 7: Build and Push Docker Image

**Option A: GitHub Actions (Recommended)**:

```bash
# Merge to main branch triggers automatic build
git checkout main
git merge develop
git push origin main

# Monitor build: https://github.com/stuartshay/otel-ui/actions

# Wait for completion (2-4 minutes)
# Image pushed to: stuartshay/otel-ui:1.1.0
```

**Option B: Manual Build** (if needed):

```bash
cd /home/ubuntu/git/otel-ui

# Build multi-platform image
docker build -t stuartshay/otel-ui:1.1.0 \
             -t stuartshay/otel-ui:latest .

# Push to Docker Hub
docker push stuartshay/otel-ui:1.1.0
docker push stuartshay/otel-ui:latest

# Verify on Docker Hub
# https://hub.docker.com/r/stuartshay/otel-ui/tags
```

### Step 8: Update Kubernetes Manifests

**Update k8s-gitops**:

```bash
cd /home/ubuntu/git/k8s-gitops/apps/base/otel-ui

# Update manifests with new version
./update-version.sh 1.1.0

# Files updated:
# - VERSION
# - kustomization.yaml (newTag)
# - deployment.yaml (image + APP_VERSION env)

# Commit and push
cd /home/ubuntu/git/k8s-gitops
git add apps/base/otel-ui/
git commit -m "feat: Update otel-ui to v1.1.0 - add user statistics"
git push origin master
```

### Step 9: Deploy to Production

**Argo CD Auto-Sync**:

```bash
# Argo CD detects git changes and syncs automatically
# Default sync interval: 3 minutes

# Monitor deployment
kubectl rollout status deployment otel-ui -n otel-ui --timeout=180s

# Check running version
kubectl get deployment otel-ui -n otel-ui \
  -o jsonpath='{.spec.template.spec.containers[0].image}'
# Expected: stuartshay/otel-ui:1.1.0

# Check pod status
kubectl get pods -n otel-ui
# Should see: 2/2 Running
```

**Manual Sync** (if auto-sync disabled):

```bash
# Apply manifests directly
kubectl apply -k /home/ubuntu/git/k8s-gitops/apps/base/otel-ui/ -n otel-ui

# Wait for rollout
kubectl rollout status deployment otel-ui -n otel-ui
```

### Step 10: Verify Production Deployment

**Health Checks**:

```bash
# 1. Check pods running
kubectl get pods -n otel-ui
# Expected: All pods Running, Ready 1/1

# 2. Check logs for errors
kubectl logs -n otel-ui -l app=otel-ui --tail=50
# Look for: No ERROR or WARNING messages

# 3. Test ingress endpoint
curl -sI https://ui.lab.informationcart.com/
# Expected: HTTP/2 200

# 4. Test full page load
curl -s https://ui.lab.informationcart.com/ | grep -o '<title>.*</title>'
# Expected: <title>otel-ui</title>

# 5. Check application version
curl -s https://ui.lab.informationcart.com/ | grep -o 'window.APP_VERSION.*'
# Expected: window.APP_VERSION = "1.1.0"
```

**Manual Browser Testing**:

```text
1. Open https://ui.lab.informationcart.com
2. Clear cache (Ctrl+Shift+R)
3. Login with test credentials
4. Test new feature
5. Test existing features (smoke test)
6. Check browser console for errors
7. Test on mobile (or resize browser)
8. Test logout
```

### Step 11: Update Documentation

**Update project-plan.md**:

```markdown
# Move completed task from "In Progress" to "Completed"

## Completed Tasks ✅

### [Task Number]. [Enhancement Name]

- [x] Implement component
- [x] Add tests
- [x] Update documentation
- [x] Deploy to production (v1.1.0)
```

**Update README.md** (if needed):

```markdown
# Update deployment status

**Deployment Status**: Version 1.1.0 deployed to [ui.lab.informationcart.com]

# Add new features to feature list

- **User Statistics** - Real-time activity dashboard
```

**Update authentication.md** (if auth-related):

```markdown
# Add troubleshooting entry

# Update configuration examples

# Document new auth flows
```

**Create Migration Guide** (if breaking changes):

```markdown
# docs/migrations/v1-to-v2.md

# Migration Guide: v1.x to v2.0

## Breaking Changes

1. **Authentication API Changed**
   - Old: `authService.login()`
   - New: `authService.signIn(options)`

## Migration Steps

[Step-by-step guide]
```

### Step 12: Post-Deployment Validation

**Monitor for Issues** (24-48 hours):

```bash
# Watch pod restarts
kubectl get pods -n otel-ui --watch

# Monitor logs for errors
kubectl logs -n otel-ui -l app=otel-ui -f

# Check resource usage
kubectl top pods -n otel-ui

# View events
kubectl get events -n otel-ui --sort-by='.lastTimestamp'
```

**New Relic Monitoring**:

1. Check traces for new endpoints
2. Verify no increase in error rate
3. Monitor response times
4. Check for new JavaScript errors

**User Feedback**:

1. Monitor support channels (if any)
2. Check GitHub issues for bug reports
3. Review analytics (if configured)

## Rollback Procedure

If issues found in production:

```bash
# 1. Identify last working version
cd /home/ubuntu/git/k8s-gitops
git log --oneline apps/base/otel-ui/VERSION | head -5

# 2. Rollback k8s manifests
cd apps/base/otel-ui
./update-version.sh 1.0.33  # Previous working version

# 3. Commit and push
cd /home/ubuntu/git/k8s-gitops
git add -A
git commit -m "revert: Rollback otel-ui to v1.0.33 due to [issue]"
git push origin master

# 4. Monitor rollback
kubectl rollout status deployment otel-ui -n otel-ui

# 5. Verify old version running
kubectl get pods -n otel-ui -o wide

# 6. Fix issue in develop branch
cd /home/ubuntu/git/otel-ui
git checkout develop
# Make fixes, test, redeploy with new version
```

## Quality Checklist

Before marking enhancement complete:

- [ ] **Code Quality**
  - [ ] TypeScript strict mode compliance
  - [ ] No linting errors
  - [ ] Code formatted with Prettier
  - [ ] No console errors in browser

- [ ] **Functionality**
  - [ ] Feature works as specified
  - [ ] Edge cases handled
  - [ ] Error states handled gracefully
  - [ ] Loading states implemented

- [ ] **Testing**
  - [ ] Manual testing completed
  - [ ] Existing features not broken
  - [ ] Responsive on mobile
  - [ ] Cross-browser compatible (Chrome, Firefox, Safari)

- [ ] **Security**
  - [ ] No secrets in code
  - [ ] Auth properly implemented
  - [ ] Input validation added
  - [ ] XSS/CSRF protection considered

- [ ] **Performance**
  - [ ] No unnecessary re-renders
  - [ ] Large lists virtualized/paginated
  - [ ] Images optimized
  - [ ] Bundle size reasonable

- [ ] **Documentation**
  - [ ] Code comments for complex logic
  - [ ] README.md updated
  - [ ] project-plan.md updated
  - [ ] API changes documented

- [ ] **Deployment**
  - [ ] Version bumped appropriately
  - [ ] Git tag created
  - [ ] Docker image built and pushed
  - [ ] K8s manifests updated
  - [ ] Production deployment verified

- [ ] **Monitoring**
  - [ ] Logs checked for errors
  - [ ] Traces visible in New Relic
  - [ ] No performance degradation
  - [ ] Error rates normal

## Example: Complete Enhancement Flow

**Scenario**: Add a "Service Health" component showing API status

```bash
# 1. Plan
echo "Enhancement: Service Health Component
- Show otel-demo API status
- Display last check time
- Auto-refresh every 30s
- Version: 1.1.0 (minor - new feature)" > /tmp/plan.md

# 2. Branch
cd /home/ubuntu/git/otel-ui
git checkout develop
git pull
git checkout -b feature/service-health

# 3. Implement
# Create src/components/ServiceHealth.tsx
# Update src/App.tsx to include component

# 4. Test
npm run type-check
npm run lint:all
npm run build
npm run dev
# Manual test in browser

# 5. Commit
git add src/components/ServiceHealth.tsx src/App.tsx
git commit -m "feat(components): Add ServiceHealth status widget

Display real-time API health with auto-refresh:
- Polls /health endpoint every 30s
- Shows green/red status indicator
- Displays last check timestamp
- Error handling with retry logic"

# 6. Version
bash scripts/update-version.sh 1.1.0
git add VERSION package.json
git commit -m "chore: Bump version to 1.1.0"
git push origin feature/service-health

# 7. Merge
git checkout develop
git merge feature/service-health
git push origin develop
git tag v1.1.0
git push origin v1.1.0

# 8. Build (automatic via GitHub Actions)
git checkout main
git merge develop
git push origin main

# 9. Update k8s
cd /home/ubuntu/git/k8s-gitops/apps/base/otel-ui
./update-version.sh 1.1.0
cd /home/ubuntu/git/k8s-gitops
git add -A
git commit -m "feat: Update otel-ui to v1.1.0 - service health widget"
git push origin master

# 10. Verify
kubectl rollout status deployment otel-ui -n otel-ui
curl -I https://ui.lab.informationcart.com/
# Test in browser

# 11. Document
# Update docs/project-plan.md
# Update README.md with new feature
git add docs/ README.md
git commit -m "docs: Document ServiceHealth component"
git push origin develop

# 12. Monitor
kubectl logs -n otel-ui -l app=otel-ui -f
# Check New Relic traces
```

## Related Documentation

- [otel-ui Deployment Skill](../otel-ui-deployment/SKILL.md)
- [Project Plan](../../docs/project-plan.md)
- [Authentication Guide](../../docs/authentication.md)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)

## Quick Reference

```bash
# Setup
git checkout develop && git pull && git checkout -b feature/name

# Development
npm run dev                    # Start dev server
npm run type-check            # Check types
npm run lint:all              # Lint everything
npm run build                 # Production build

# Version
bash scripts/update-version.sh 1.1.0

# Deploy
cd /home/ubuntu/git/k8s-gitops/apps/base/otel-ui && ./update-version.sh 1.1.0

# Verify
kubectl rollout status deployment otel-ui -n otel-ui
curl -I https://ui.lab.informationcart.com/
```
