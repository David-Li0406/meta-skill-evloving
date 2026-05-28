# Zero-Downtime Deployment Patterns

Lambda versioning and alias strategies for production deployments without service interruption.

**Principle:** Every Lambda update replaces running code. Versioning + Aliases enable atomic switchover with instant rollback.

---

## The Problem: Direct Lambda Updates

**Traditional deployment:**

```bash
aws lambda update-function-code --function-name worker --image-uri $NEW_IMAGE
```

**Issues:**
- ❌ Brief unavailability during update (function not invocable)
- ❌ No rollback mechanism (previous code replaced)
- ❌ Can't test new version before promoting to production
- ❌ All traffic immediately hits new code (no gradual rollout)

**Result:** Every deployment is risky.

---

## The Solution: Version + Alias Pattern

### Three-Layer Architecture

```
Layer 1: $LATEST (mutable, testing)
   ↓ publish version when stable
Layer 2: Version N (immutable snapshot)
   ↓ update alias when validated
Layer 3: Alias (production pointer)
```

**Benefits:**
- ✅ Zero downtime (alias update is atomic)
- ✅ Instant rollback (point alias to previous version)
- ✅ Test before promotion ($LATEST → Version)
- ✅ Traffic shifting (weighted aliases for gradual rollout)

---

## Lambda Versioning Concepts

### $LATEST (Mutable Staging)

**Characteristics:**
- Always points to most recent function code
- Mutable (can be updated)
- Use for testing and validation
- NEVER point production traffic here

**Deployment Pattern:**
```bash
# Update $LATEST with new code
aws lambda update-function-code \
  --function-name worker \
  --image-uri 123456789012.dkr.ecr.ap-southeast-1.amazonaws.com/worker:abc123

# Wait for update to complete (don't skip this!)
aws lambda wait function-updated --function-name worker

# Test $LATEST
aws lambda invoke \
  --function-name worker:$LATEST \
  --payload '{"test": true}' \
  /tmp/response.json

# Validate response
if grep -q "errorMessage" /tmp/response.json; then
  echo "❌ $LATEST has errors, not promoting to version"
  exit 1
fi
```

### Versions (Immutable Snapshots)

**Characteristics:**
- Immutable (cannot be changed after publish)
- Numbered sequentially (1, 2, 3, ...)
- Represent stable, validated code
- Can be deleted (unlike $LATEST)

**Publishing Pattern:**
```bash
# Publish new version from $LATEST
VERSION=$(aws lambda publish-version \
  --function-name worker \
  --description "Release v1.2.0: Add new feature" \
  --query 'Version' --output text)

echo "Published version: $VERSION"
# Output: Published version: 42
```

**Version Metadata:**
```bash
# List all versions
aws lambda list-versions-by-function --function-name worker

# Get specific version details
aws lambda get-function --function-name worker --qualifier 42
```

### Aliases (Production Pointers)

**Characteristics:**
- Friendly names (e.g., "live", "staging", "canary")
- Point to specific version (or $LATEST, but don't do this in production)
- Can be updated to point to different version (atomic switchover)
- Support weighted traffic shifting

**Alias Creation:**
```bash
# Create 'live' alias pointing to version 42
aws lambda create-alias \
  --function-name worker \
  --name live \
  --function-version 42 \
  --description "Production traffic"
```

**Alias Update (Zero-Downtime Deployment):**
```bash
# Update 'live' alias to new version (atomic swap)
aws lambda update-alias \
  --function-name worker \
  --name live \
  --function-version 43  # New version

# This is INSTANT - no downtime
```

**Invoking via Alias:**
```bash
# Production invocations use alias
aws lambda invoke \
  --function-name worker:live \  # Alias name
  --payload '{}' \
  /tmp/response.json
```

---

## Zero-Downtime Deployment Workflow

### Step-by-Step Process

**1. Update $LATEST with New Code**

```bash
# Deploy new image to $LATEST
aws lambda update-function-code \
  --function-name worker \
  --image-uri $ECR_REGISTRY/worker:$GIT_SHA

# Wait for update (NEVER skip this!)
aws lambda wait function-updated --function-name worker
```

**2. Test $LATEST**

```bash
# Invoke $LATEST with test payload
aws lambda invoke \
  --function-name worker:$LATEST \
  --payload '{"ticker": "NVDA19", "test": true}' \
  /tmp/test-response.json

# Validate response
if grep -q "errorMessage" /tmp/test-response.json; then
  echo "❌ Tests failed, aborting deployment"
  cat /tmp/test-response.json
  exit 1
fi

# Check CloudWatch logs for errors
ERROR_COUNT=$(aws logs filter-log-events \
  --log-group-name /aws/lambda/worker \
  --start-time $(($(date +%s) - 300))000 \  # Last 5 minutes
  --filter-pattern "ERROR" \
  --query 'length(events)' --output text)

if [ "$ERROR_COUNT" -gt 0 ]; then
  echo "❌ Found errors in CloudWatch logs"
  exit 1
fi

echo "✅ $LATEST validated successfully"
```

**3. Publish Immutable Version**

```bash
# Publish version from validated $LATEST
NEW_VERSION=$(aws lambda publish-version \
  --function-name worker \
  --description "Release v1.2.0: Add user analytics" \
  --query 'Version' --output text)

echo "📦 Published version: $NEW_VERSION"
```

**4. Update Production Alias (Zero-Downtime Switchover)**

```bash
# Get current production version (for rollback if needed)
CURRENT_VERSION=$(aws lambda get-alias \
  --function-name worker \
  --name live \
  --query 'FunctionVersion' --output text)

echo "Current production version: $CURRENT_VERSION"
echo "Promoting to version: $NEW_VERSION"

# Atomic switchover (zero downtime!)
aws lambda update-alias \
  --function-name worker \
  --name live \
  --function-version $NEW_VERSION

echo "✅ Production updated to version $NEW_VERSION"
echo "⏪ To rollback: aws lambda update-alias --function-name worker --name live --function-version $CURRENT_VERSION"
```

**5. Validate Production**

```bash
# Smoke test production alias
aws lambda invoke \
  --function-name worker:live \
  --payload '{"ticker": "NVDA19"}' \
  /tmp/prod-response.json

# Check for errors
if grep -q "errorMessage" /tmp/prod-response.json; then
  echo "❌ Production error detected, rolling back..."

  # Instant rollback
  aws lambda update-alias \
    --function-name worker \
    --name live \
    --function-version $CURRENT_VERSION

  echo "⏪ Rolled back to version $CURRENT_VERSION"
  exit 1
fi

echo "✅ Production validated successfully"
```

---

## Rollback Strategies

### Instant Rollback (< 30 seconds)

**Pattern:** Point alias to previous version.

```bash
# List recent versions
aws lambda list-versions-by-function \
  --function-name worker \
  --query 'Versions[-5:].Version' \
  --output table

# Rollback to specific version
aws lambda update-alias \
  --function-name worker \
  --name live \
  --function-version 41  # Previous working version

# Verify rollback
aws lambda get-alias --function-name worker --name live | jq .FunctionVersion
```

**Why This Works:**
- Alias update is atomic (instantaneous switchover)
- Previous version still exists (immutable)
- No code redeployment needed

### When to Rollback

**Immediate rollback if:**
- Smoke tests fail after promotion
- ERROR logs spike in CloudWatch
- User reports increase
- Performance regression detected (latency, memory)

**Investigation Pattern:**

```bash
# 1. Check recent error logs
aws logs filter-log-events \
  --log-group-name /aws/lambda/worker \
  --start-time $(($(date +%s) - 600))000 \  # Last 10 minutes
  --filter-pattern "ERROR"

# 2. Compare metrics (current vs previous version)
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Duration \
  --dimensions Name=FunctionName,Value=worker \
  --start-time $(date -u -d '10 minutes ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Average

# 3. If metrics degraded → rollback
aws lambda update-alias \
  --function-name worker \
  --name live \
  --function-version $PREVIOUS_VERSION
```

---

## Traffic Shifting Patterns

### Weighted Aliases (Gradual Rollout)

**Use Case:** Roll out new version to 10% of traffic, monitor, then increase.

**Pattern:**

```bash
# Step 1: 10% traffic to new version, 90% to old
aws lambda update-alias \
  --function-name worker \
  --name live \
  --function-version 43 \  # New version
  --routing-config '{"AdditionalVersionWeights": {"42": 0.9}}'  # 90% to v42

# Step 2: Monitor for 30 minutes
# - Check error rates
# - Compare latency
# - Validate logs

# Step 3: If stable, increase to 50%
aws lambda update-alias \
  --function-name worker \
  --name live \
  --function-version 43 \
  --routing-config '{"AdditionalVersionWeights": {"42": 0.5}}'

# Step 4: If still stable, full rollout
aws lambda update-alias \
  --function-name worker \
  --name live \
  --function-version 43 \
  --routing-config '{}'  # 100% to v43
```

**Monitoring During Rollout:**

```bash
#!/bin/bash
# monitor_canary.sh - Track error rates during gradual rollout

NEW_VERSION=43
OLD_VERSION=42

while true; do
  # Get error count for each version
  NEW_ERRORS=$(aws logs filter-log-events \
    --log-group-name /aws/lambda/worker \
    --start-time $(($(date +%s) - 300))000 \
    --filter-pattern "[version=$NEW_VERSION] ERROR" \
    --query 'length(events)' --output text)

  OLD_ERRORS=$(aws logs filter-log-events \
    --log-group-name /aws/lambda/worker \
    --start-time $(($(date +%s) - 300))000 \
    --filter-pattern "[version=$OLD_VERSION] ERROR" \
    --query 'length(events)' --output text)

  echo "$(date): New version errors: $NEW_ERRORS | Old version errors: $OLD_ERRORS"

  # Alert if new version has significantly more errors
  if [ "$NEW_ERRORS" -gt $((OLD_ERRORS * 2)) ]; then
    echo "❌ Error rate spike detected in new version!"
    echo "⏪ Rolling back..."

    aws lambda update-alias \
      --function-name worker \
      --name live \
      --function-version $OLD_VERSION

    break
  fi

  sleep 60  # Check every minute
done
```

### Blue/Green Deployment

**Pattern:** Maintain two environments, switch traffic instantly.

```
Blue Environment (Current Production)
  - Alias: live → Version 42

Green Environment (New Version)
  - Alias: staging → Version 43

Deployment:
  1. Test staging thoroughly
  2. Switch: live → Version 43 (atomic)
  3. Keep blue as rollback: blue → Version 42
```

**Implementation:**

```bash
# Before deployment
aws lambda get-alias --function-name worker --name live
# FunctionVersion: 42

# Deploy to staging, test thoroughly
aws lambda update-alias \
  --function-name worker \
  --name staging \
  --function-version 43

# Run extensive tests against staging
pytest tests/integration --env=staging

# If tests pass, switch production
aws lambda update-alias \
  --function-name worker \
  --name live \
  --function-version 43

# Create blue alias for instant rollback
aws lambda create-alias \
  --function-name worker \
  --name blue \
  --function-version 42

# After 24 hours of stable operation, delete blue alias
aws lambda delete-alias --function-name worker --name blue
```

---

## Container Image Immutability

**Principle:** Docker images deployed to Lambda are immutable by SHA256 hash.

### Why Immutability Matters

**Mutable Tags (Dangerous):**

```bash
# ❌ DON'T: Using mutable tag
aws lambda update-function-code \
  --function-name worker \
  --image-uri $ECR_REGISTRY/worker:latest  # ⚠️ Tag can change!

# Problem: "latest" tag can point to different images over time
# - Dev deploys new image with :latest tag
# - Prod redeploys (expects same code)
# - Gets DIFFERENT image than what was tested!
```

**Immutable Hashes (Safe):**

```bash
# ✅ DO: Using content-addressable hash
aws lambda update-function-code \
  --function-name worker \
  --image-uri $ECR_REGISTRY/worker@sha256:abc123...  # Immutable

# Guarantee: This hash ALWAYS points to the EXACT same image
```

### Artifact Promotion Pattern

**Build Once, Promote Many Times:**

```yaml
# .github/workflows/deploy.yml
jobs:
  build:
    # Build in dev environment
    runs-on: ubuntu-latest
    outputs:
      image_digest: ${{ steps.build.outputs.digest }}
    steps:
      - name: Build and push Docker image
        id: build
        run: |
          IMAGE_TAG=$ECR_REGISTRY/worker:$GITHUB_SHA
          docker build -t $IMAGE_TAG .
          docker push $IMAGE_TAG

          # Get immutable digest
          DIGEST=$(docker inspect --format='{{index .RepoDigests 0}}' $IMAGE_TAG)
          echo "digest=$DIGEST" >> $GITHUB_OUTPUT

  deploy-dev:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to dev
        run: |
          # Use DIGEST (immutable), not tag
          aws lambda update-function-code \
            --function-name worker-dev \
            --image-uri ${{ needs.build.outputs.image_digest }}

  deploy-staging:
    needs: [build, deploy-dev]  # Only after dev succeeds
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to staging
        run: |
          # SAME digest as dev (artifact promotion)
          aws lambda update-function-code \
            --function-name worker-staging \
            --image-uri ${{ needs.build.outputs.image_digest }}

  deploy-prod:
    needs: [build, deploy-staging]
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          # SAME digest as staging (tested exactly this image)
          aws lambda update-function-code \
            --function-name worker-prod \
            --image-uri ${{ needs.build.outputs.image_digest }}
```

**Benefits:**
- ✅ What you test in dev is EXACTLY what deploys to prod
- ✅ No "works on my machine" (same binary everywhere)
- ✅ Traceability (Git SHA → Image digest → Deployed version)
- ✅ Reproducible deployments (can redeploy exact version months later)

---

## Quick Reference

### Common Commands

```bash
# Update $LATEST with new code
aws lambda update-function-code \
  --function-name worker \
  --image-uri $IMAGE_URI
aws lambda wait function-updated --function-name worker

# Publish immutable version
VERSION=$(aws lambda publish-version \
  --function-name worker \
  --description "Release notes" \
  --query 'Version' --output text)

# Update production alias (zero-downtime)
aws lambda update-alias \
  --function-name worker \
  --name live \
  --function-version $VERSION

# Instant rollback
aws lambda update-alias \
  --function-name worker \
  --name live \
  --function-version $PREVIOUS_VERSION

# List versions
aws lambda list-versions-by-function --function-name worker

# Get alias details
aws lambda get-alias --function-name worker --name live
```

### Decision Matrix

| Scenario | Pattern | Downtime | Rollback Time |
|----------|---------|----------|---------------|
| **Dev deployment** | Update $LATEST | Acceptable | N/A (dev) |
| **Staging deployment** | Publish version | < 1 second | < 30 seconds |
| **Production deployment** | Version + Alias | 0 seconds | < 30 seconds |
| **High-risk change** | Weighted alias | 0 seconds | < 30 seconds |
| **Major release** | Blue/Green | 0 seconds | < 30 seconds |

---

## References

- [AWS Lambda Versioning](https://docs.aws.amazon.com/lambda/latest/dg/configuration-versions.html)
- [AWS Lambda Aliases](https://docs.aws.amazon.com/lambda/latest/dg/configuration-aliases.html)
- [Traffic Shifting with Aliases](https://docs.aws.amazon.com/lambda/latest/dg/configuration-aliases.html#configuring-alias-routing)
- [Lambda Container Images](https://docs.aws.amazon.com/lambda/latest/dg/images-create.html)
