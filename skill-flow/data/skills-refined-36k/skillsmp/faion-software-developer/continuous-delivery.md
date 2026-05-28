---
id: continuous-delivery
name: "Continuous Delivery"
domain: DEV
skill: faion-software-developer
category: "development-practices"
---

# Continuous Delivery (CD)

## Overview

Continuous Delivery is a software development practice where code changes are automatically prepared for release to production. It expands on Continuous Integration by ensuring that code is always in a deployable state. Every change that passes automated tests can be released to production with the push of a button.

## When to Use

- Web applications and SaaS products
- Teams aiming for frequent releases
- When manual deployments cause bottlenecks
- Projects requiring rapid iteration
- Organizations seeking to reduce deployment risk

## Prerequisites

- Continuous Integration in place
- Comprehensive automated testing
- Version control (everything in code)
- Infrastructure as Code
- Feature flags (for incomplete features)

## Key Principles

### Every Commit is Releasable

```markdown
## Requirements
- Automated testing at every stage
- No manual testing gates
- Feature flags for incomplete work
- Backward compatible changes

## Benefits
- Reduced risk (small batches)
- Faster feedback
- Lower deployment stress
- Easy rollback
```

### Deployment Pipeline

```markdown
## Pipeline Stages
Commit → Build → Test → Stage → Production
   ↓       ↓       ↓       ↓         ↓
 Trigger  Compile  Unit   Deploy   Deploy
         Package  Integ   Test    Manual/Auto
                  E2E    Verify
```

### Automation Everything

```markdown
## Automate
✅ Build process
✅ Test execution
✅ Environment provisioning
✅ Database migrations
✅ Configuration management
✅ Deployment
✅ Monitoring setup
✅ Rollback

## Manual (Approval Only)
- Production deployment trigger (CD)
- Or fully automated (Continuous Deployment)
```

## CD Pipeline Implementation

### GitHub Actions Example

```yaml
# .github/workflows/cd.yml
name: CD Pipeline

on:
  push:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # Stage 1: Build and Unit Test
  build:
    runs-on: ubuntu-latest
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Run unit tests
        run: pytest tests/unit --cov=src --cov-fail-under=80

      - name: Build Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}

  # Stage 2: Integration Tests
  integration:
    needs: build
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: test
        ports:
          - 5432:5432
    steps:
      - uses: actions/checkout@v4

      - name: Run integration tests
        run: pytest tests/integration
        env:
          DATABASE_URL: postgresql://postgres:test@localhost:5432/test

  # Stage 3: Deploy to Staging
  staging:
    needs: integration
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - name: Deploy to staging
        run: |
          kubectl set image deployment/app \
            app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
            --namespace=staging

      - name: Wait for rollout
        run: kubectl rollout status deployment/app -n staging --timeout=300s

      - name: Run smoke tests
        run: ./scripts/smoke-tests.sh https://staging.example.com

  # Stage 4: E2E Tests on Staging
  e2e:
    needs: staging
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run E2E tests
        uses: cypress-io/github-action@v6
        with:
          config: baseUrl=https://staging.example.com

  # Stage 5: Deploy to Production (Manual Approval)
  production:
    needs: e2e
    runs-on: ubuntu-latest
    environment: production  # Requires manual approval
    steps:
      - name: Deploy to production
        run: |
          kubectl set image deployment/app \
            app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
            --namespace=production

      - name: Wait for rollout
        run: kubectl rollout status deployment/app -n production --timeout=300s

      - name: Run production smoke tests
        run: ./scripts/smoke-tests.sh https://example.com

      - name: Notify deployment
        run: |
          curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
            -d '{"text": "Deployed ${{ github.sha }} to production"}'
```

### Database Migrations

```python
# Continuous Delivery requires safe migrations
# Use backward-compatible migrations only

# migrations/versions/001_add_user_email.py

"""Add email column to users table."""

from alembic import op
import sqlalchemy as sa

def upgrade():
    # Step 1: Add nullable column (backward compatible)
    op.add_column('users', sa.Column('email', sa.String(255), nullable=True))

def downgrade():
    op.drop_column('users', 'email')

# Next deployment: make required
# migrations/versions/002_make_email_required.py
def upgrade():
    # Step 2: After data migration, add constraint
    op.alter_column('users', 'email', nullable=False)
```

### Feature Flags for CD

```python
# features/flags.py
from typing import Optional
import httpx

class FeatureFlagService:
    """
    Feature flags enable CD by hiding incomplete features.

    Deployment: Code ships to production
    Release: Feature becomes visible to users
    """

    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key
        self._cache: dict[str, bool] = {}

    def is_enabled(
        self,
        flag: str,
        user_id: Optional[str] = None,
        default: bool = False
    ) -> bool:
        """
        Check if feature flag is enabled.

        Supports:
        - Global on/off
        - Percentage rollout
        - User targeting
        - Environment targeting
        """
        cache_key = f"{flag}:{user_id or 'global'}"

        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            response = httpx.post(
                f"{self.api_url}/flags/{flag}/evaluate",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"user_id": user_id}
            )
            result = response.json().get("enabled", default)
            self._cache[cache_key] = result
            return result
        except Exception:
            return default

# Usage in code
feature_flags = FeatureFlagService(
    api_url=settings.FEATURE_FLAG_URL,
    api_key=settings.FEATURE_FLAG_API_KEY
)

@app.get("/dashboard")
async def dashboard(user: User):
    data = get_dashboard_data(user)

    # New feature behind flag
    if feature_flags.is_enabled("new_analytics", user.id):
        data["analytics"] = get_new_analytics(user)

    return data
```

## Deployment Strategies

### Blue-Green Deployment

```yaml
# Blue-Green: Two identical environments
# Switch traffic instantly

# Kubernetes example
apiVersion: v1
kind: Service
metadata:
  name: app
spec:
  selector:
    app: app
    version: green  # Switch to blue for rollback
  ports:
    - port: 80

---
# Blue deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: app
      version: blue
  template:
    metadata:
      labels:
        app: app
        version: blue
    spec:
      containers:
        - name: app
          image: app:v1.0.0

---
# Green deployment (new version)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: app
      version: green
  template:
    metadata:
      labels:
        app: app
        version: green
    spec:
      containers:
        - name: app
          image: app:v1.1.0
```

### Canary Deployment

```yaml
# Canary: Gradual traffic shift
# Catch issues before full rollout

# Using Istio for traffic splitting
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: app
spec:
  hosts:
    - app
  http:
    - route:
        # 90% to stable
        - destination:
            host: app
            subset: stable
          weight: 90
        # 10% to canary
        - destination:
            host: app
            subset: canary
          weight: 10

---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: app
spec:
  host: app
  subsets:
    - name: stable
      labels:
        version: v1.0.0
    - name: canary
      labels:
        version: v1.1.0
```

### Rolling Deployment

```yaml
# Rolling: Gradual pod replacement
# Default Kubernetes strategy

apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 6
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2        # Max pods over desired
      maxUnavailable: 1  # Max pods unavailable
  template:
    spec:
      containers:
        - name: app
          image: app:v1.1.0
          readinessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 15
            periodSeconds: 20
```

## Monitoring and Rollback

### Health Checks

```python
# app/health.py
from fastapi import APIRouter, Response
from datetime import datetime

router = APIRouter()

@router.get("/health")
async def health():
    """
    Kubernetes readiness/liveness probe.
    CD pipeline checks this after deployment.
    """
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/health/ready")
async def readiness():
    """
    Readiness probe: Can accept traffic?
    Checks all dependencies.
    """
    checks = {
        "database": await check_database(),
        "redis": await check_redis(),
        "external_api": await check_external_api(),
    }

    all_healthy = all(checks.values())
    status_code = 200 if all_healthy else 503

    return Response(
        content=json.dumps({"checks": checks, "ready": all_healthy}),
        status_code=status_code,
        media_type="application/json"
    )
```

### Automatic Rollback

```yaml
# Rollback on deployment failure
# .github/workflows/cd.yml (addition)

production:
  steps:
    - name: Deploy
      id: deploy
      run: kubectl set image ...

    - name: Wait for rollout
      id: rollout
      run: kubectl rollout status ...
      continue-on-error: true

    - name: Smoke tests
      id: smoke
      run: ./scripts/smoke-tests.sh
      continue-on-error: true

    - name: Rollback on failure
      if: steps.rollout.outcome == 'failure' || steps.smoke.outcome == 'failure'
      run: |
        echo "Deployment failed, rolling back..."
        kubectl rollout undo deployment/app -n production
        exit 1
```

### Deployment Metrics

```python
# Track deployment metrics
# Send to monitoring (Datadog, Prometheus, etc.)

from datadog import statsd

def track_deployment(version: str, success: bool, duration: float):
    """Track deployment metrics for DORA."""

    # Deployment frequency
    statsd.increment(
        "deployment.count",
        tags=[f"version:{version}", f"success:{success}"]
    )

    # Lead time (separate tracking from commit time)
    statsd.histogram(
        "deployment.duration_seconds",
        duration,
        tags=[f"version:{version}"]
    )

    if not success:
        # Change failure rate
        statsd.increment(
            "deployment.failure",
            tags=[f"version:{version}"]
        )
```

## CD vs CI vs Continuous Deployment

| Aspect | CI | CD (Delivery) | CD (Deployment) |
|--------|----|--------------|-----------------|
| Build automation | ✅ | ✅ | ✅ |
| Automated tests | ✅ | ✅ | ✅ |
| Deploy to staging | ❌ | ✅ | ✅ |
| Production-ready | ❌ | ✅ | ✅ |
| Auto-deploy prod | ❌ | ❌ (manual) | ✅ (auto) |
| Risk level | Low | Medium | Higher |

## Common Challenges

### "We Can't Deploy That Often"

```markdown
## Cause
- Large batch sizes
- Manual testing requirements
- Fear of production issues

## Solutions
1. Smaller changes (< 200 lines)
2. Comprehensive automated tests
3. Feature flags
4. Canary deployments
5. Fast rollback capability
```

### "Testing Takes Too Long"

```markdown
## Cause
- Serial test execution
- Slow E2E tests
- Flaky tests

## Solutions
1. Parallelize tests
2. Test pyramid (more unit, fewer E2E)
3. Fix or quarantine flaky tests
4. Run E2E only on staging
5. Use contract testing
```

### "Database Changes Break CD"

```markdown
## Cause
- Non-backward-compatible migrations
- Long-running migrations
- Data migration during deployment

## Solutions
1. Expand-contract pattern
2. Split schema and data migrations
3. Online schema change tools
4. Blue-green for database changes
```

## DORA Metrics

```markdown
## Elite Performance (Target)
- Deployment frequency: On-demand (multiple per day)
- Lead time for changes: < 1 hour
- Change failure rate: 0-15%
- Time to restore: < 1 hour

## Measuring
- Track every deployment
- Measure from commit to production
- Count rollbacks and incidents
- Time to recovery from incidents
```

## Implementation Roadmap

```markdown
## Phase 1: CI Foundation (2-4 weeks)
- [ ] Automated builds on every commit
- [ ] Unit tests in pipeline (> 70% coverage)
- [ ] Code quality gates (lint, type check)
- [ ] Build artifacts stored

## Phase 2: Automated Testing (4-6 weeks)
- [ ] Integration tests automated
- [ ] E2E tests on staging
- [ ] Test parallelization
- [ ] < 15 min total pipeline time

## Phase 3: Staging Deployment (2-4 weeks)
- [ ] Auto-deploy to staging
- [ ] Staging mirrors production
- [ ] Smoke tests automated
- [ ] Feature flags implemented

## Phase 4: Production Deployment (4-8 weeks)
- [ ] One-click production deploy
- [ ] Deployment strategies (rolling/canary)
- [ ] Automated rollback
- [ ] Monitoring and alerting

## Phase 5: Continuous Deployment (optional)
- [ ] Auto-deploy to production
- [ ] Canary analysis automated
- [ ] Progressive delivery
- [ ] Chaos engineering
```

## References

- [Continuous Delivery - Jez Humble](https://continuousdelivery.com/)
- [Accelerate - Nicole Forsgren et al.](https://itrevolution.com/accelerate-book/)
- [The DevOps Handbook](https://itrevolution.com/the-devops-handbook/)
- [DORA Metrics](https://www.devops-research.com/research.html)
- [Martin Fowler - Continuous Delivery](https://martinfowler.com/bliki/ContinuousDelivery.html)
