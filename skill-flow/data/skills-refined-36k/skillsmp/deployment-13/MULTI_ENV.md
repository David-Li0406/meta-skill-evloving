# Multi-Environment Deployment Workflows

**For complete reference**, see [docs/deployment/MULTI_ENV.md](../../../docs/deployment/MULTI_ENV.md)

---

## Deploy to Dev Workflow

**Trigger:** Push to `dev` branch

**Pattern: Feature → Dev → Test**

```bash
#!/bin/bash
set -euo pipefail

# 1. Build Docker image
IMAGE_TAG=$ECR_REGISTRY/worker:$GIT_SHA
docker build -t $IMAGE_TAG .
docker push $IMAGE_TAG

# 2. Get immutable digest
DIGEST=$(docker inspect --format='{{index .RepoDigests 0}}' $IMAGE_TAG)

# 3. Deploy to dev Lambda
aws lambda update-function-code \
  --function-name [PROJECT_NAME]-worker-dev \
  --image-uri $DIGEST

aws lambda wait function-updated \
  --function-name [PROJECT_NAME]-worker-dev

# 4. Run smoke tests
pytest tests/smoke --env=dev --tier=3

echo "✅ Dev deployment complete"
echo "Digest: $DIGEST"
```

**When to use:** Feature development, bug fixes, experiments, fast iteration

---

## Promote to Staging Workflow

**Trigger:** Merge to `main` branch (via PR from dev)

**Pattern: Promote → Test → Validate**

```bash
#!/bin/bash
set -euo pipefail

# 1. Get digest from dev (NO rebuild!)
DEV_DIGEST=$(aws lambda get-function \
  --function-name [PROJECT_NAME]-worker-dev \
  --query 'Code.ImageUri' --output text)

echo "Promoting from dev: $DEV_DIGEST"

# 2. Deploy SAME image to staging
aws lambda update-function-code \
  --function-name [PROJECT_NAME]-worker-staging \
  --image-uri $DEV_DIGEST

aws lambda wait function-updated \
  --function-name [PROJECT_NAME]-worker-staging

# 3. Run integration tests
pytest tests/integration --env=staging --tier=2

# 4. Smoke test staging endpoint
curl -f https://staging.example.com/api/health || exit 1

echo "✅ Staging deployment complete"
echo "Same digest as dev: $DEV_DIGEST"
```

**When to use:** Pre-production validation, QA testing, performance testing

---

## Promote to Production Workflow

**Trigger:** Create tag `v*.*.*` on `main` branch

**Pattern: Promote → Test → Publish Version → Update Alias**

```bash
#!/bin/bash
set -euo pipefail

TAG_NAME=$1  # e.g., v1.2.0

# 1. Get digest from staging (NO rebuild!)
STAGING_DIGEST=$(aws lambda get-function \
  --function-name [PROJECT_NAME]-worker-staging \
  --query 'Code.ImageUri' --output text)

echo "Promoting from staging: $STAGING_DIGEST"
echo "Release tag: $TAG_NAME"

# 2. Deploy SAME image to production
aws lambda update-function-code \
  --function-name [PROJECT_NAME]-worker-prod \
  --image-uri $STAGING_DIGEST

aws lambda wait function-updated \
  --function-name [PROJECT_NAME]-worker-prod

# 3. Smoke test production endpoint
curl -f https://api.example.com/health || exit 1

# 4. Publish immutable version
VERSION=$(aws lambda publish-version \
  --function-name [PROJECT_NAME]-worker-prod \
  --description "Release $TAG_NAME" \
  --query 'Version' --output text)

echo "Published Lambda version: $VERSION"

# 5. Update 'live' alias to new version (zero-downtime)
aws lambda update-alias \
  --function-name [PROJECT_NAME]-worker-prod \
  --name live \
  --function-version $VERSION

echo "✅ Production deployment complete"
echo "Live alias → Version $VERSION"
echo "Same digest as staging: $STAGING_DIGEST"
```

**When to use:** Releases only, after staging validation, semantic versioning

---

## Artifact Promotion Verification

**Verify all environments use EXACT same image:**

```bash
#!/bin/bash

echo "Checking image consistency across environments..."

DEV_DIGEST=$(aws lambda get-function \
  --function-name [PROJECT_NAME]-worker-dev \
  --query 'Code.ImageUri' --output text)

STAGING_DIGEST=$(aws lambda get-function \
  --function-name [PROJECT_NAME]-worker-staging \
  --query 'Code.ImageUri' --output text)

PROD_DIGEST=$(aws lambda get-function \
  --function-name [PROJECT_NAME]-worker-prod \
  --query 'Code.ImageUri' --output text)

echo ""
echo "Dev:     $DEV_DIGEST"
echo "Staging: $STAGING_DIGEST"
echo "Prod:    $PROD_DIGEST"
echo ""

if [ "$DEV_DIGEST" = "$STAGING_DIGEST" ] && [ "$STAGING_DIGEST" = "$PROD_DIGEST" ]; then
  echo "✅ All environments use IDENTICAL image"
else
  echo "⚠️  Environments have different images"
  [ "$DEV_DIGEST" != "$STAGING_DIGEST" ] && echo "  - Dev ≠ Staging"
  [ "$STAGING_DIGEST" != "$PROD_DIGEST" ] && echo "  - Staging ≠ Prod"
fi
```

---

## Quick Reference Commands

### Environment Switching
```bash
# Switch Terraform to dev environment
cd terraform
terraform init -backend-config=envs/dev/backend.hcl -reconfigure

# Switch to staging
terraform init -backend-config=envs/staging/backend.hcl -reconfigure

# Switch to production
terraform init -backend-config=envs/prod/backend.hcl -reconfigure
```

### Query Current Environment
```bash
# Check which Lambda image is deployed
aws lambda get-function \
  --function-name [PROJECT_NAME]-worker-dev \
  --query 'Code.ImageUri'

# Check Terraform workspace
terraform workspace show

# Check Doppler environment
doppler configure get
```

### Environment Configuration
```bash
# Load dev secrets
ENV=dev doppler run -- aws lambda invoke ...

# Load staging secrets
ENV=staging doppler run -- aws lambda invoke ...

# Load production secrets
ENV=production doppler run -- aws lambda invoke ...
```

### Compare Environments
```bash
# Compare Lambda configurations
diff <(aws lambda get-function-configuration --function-name worker-dev) \
     <(aws lambda get-function-configuration --function-name worker-staging)

# Compare environment variables
aws lambda get-function-configuration \
  --function-name worker-dev \
  --query 'Environment.Variables' > dev-vars.json

aws lambda get-function-configuration \
  --function-name worker-staging \
  --query 'Environment.Variables' > staging-vars.json

diff dev-vars.json staging-vars.json
```

---

## Reference

**Complete guide**: [docs/deployment/MULTI_ENV.md](../../../docs/deployment/MULTI_ENV.md)

**Topics covered in complete guide:**
- Environment architecture (three-tier strategy)
- Configuration differences (Lambda memory, timeout, log retention)
- Terraform backend configuration and state isolation
- Doppler environment-specific secrets management
- Resource naming conventions and AWS tags
- Environment-specific configuration files (terraform.tfvars)
- Multi-environment testing strategies
- Environment isolation best practices
- Branch-based deployment (complete CI/CD YAML)
- Artifact promotion principle (build once, deploy many)
- Environment promotion flow
