---
name: production-deployment-checklist
description: Use this skill when deploying integrations to production, preparing for launch, or implementing go-live procedures for various platforms.
---

# Production Deployment Checklist

## Overview
Complete checklist for deploying integrations to production.

## Prerequisites
- Staging environment tested and verified
- Production API keys available
- Deployment pipeline configured
- Monitoring and alerting ready

## Instructions

### Step 1: Pre-Deployment Configuration
- [ ] Production API keys in secure vault
- [ ] Environment variables set in deployment platform
- [ ] API key scopes are minimal (least privilege)
- [ ] Webhook endpoints configured with HTTPS
- [ ] Webhook secrets stored securely

### Step 2: Code Quality Verification
- [ ] All tests passing (`npm test`)
- [ ] No hardcoded credentials
- [ ] Error handling covers all relevant error types
- [ ] Rate limiting/backoff implemented
- [ ] Logging is production-appropriate

### Step 3: Infrastructure Setup
- [ ] Health check endpoint includes connectivity checks
- [ ] Monitoring/alerting configured
- [ ] Circuit breaker pattern implemented
- [ ] Graceful degradation configured

### Step 4: Documentation Requirements
- [ ] Incident runbook created
- [ ] Key rotation procedure documented
- [ ] Rollback procedure documented
- [ ] On-call escalation path defined

### Step 5: Deploy with Gradual Rollout
```bash
# Pre-flight checks
curl -f https://staging.example.com/health
curl -s https://status.example.com

# Gradual rollout - start with canary (10%)
kubectl apply -f k8s/production.yaml
kubectl set image deployment/integration app=image:new --record
kubectl rollout pause deployment/integration

# Monitor canary traffic for 10 minutes
sleep 600
# Check error rates and latency before continuing

# If healthy, continue rollout to 50%
kubectl rollout resume deployment/integration
kubectl rollout pause deployment/integration
sleep 300

# Complete rollout to 100%
kubectl rollout resume deployment/integration
kubectl rollout status deployment/integration
```

## Output
- Deployed integration
- Health checks passing
- Monitoring active
- Rollback procedure documented