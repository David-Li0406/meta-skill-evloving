# Workflow: Deploy Application

## Purpose
Execute safe, reliable application deployments to staging or production environments. This workflow ensures proper validation, monitoring, and rollback capabilities are in place.

## When to Use
- Deploying a new version to staging or production
- Executing planned releases
- Performing hotfix deployments
- Rolling out feature flags or configuration changes

## Prerequisites
- Application is built and tested
- Deployment target environment is ready
- Access credentials and permissions configured
- Monitoring and alerting are operational
- Rollback plan is documented

## Workflow Steps

### 1. Pre-Deployment Validation

**Load and execute pre-deployment checklist:**
- Reference: `context/checklists/pre-deployment.md`

**Critical validations:**
- [ ] All tests passing in CI/CD pipeline
- [ ] Security scans completed with no critical issues
- [ ] Database migrations tested and ready (if applicable)
- [ ] Configuration changes reviewed
- [ ] Dependent services are healthy
- [ ] Rollback plan documented and tested
- [ ] Team notified of deployment window
- [ ] On-call engineer identified

**Ask clarifying questions:**
- "What environment are you deploying to? (staging/production)"
- "Is this a routine deployment or a hotfix?"
- "Have database migrations been tested?"
- "Is there a maintenance window scheduled?"

### 2. Select Deployment Strategy

**Choose based on requirements:**

**Rolling Deployment** (Default for Kubernetes)
- Use when: Standard deployment, no downtime tolerance
- Characteristics: Gradual instance replacement
- Rollback: Automated on health check failure
- Load: `context/patterns/deployment-strategies.md` for details

**Blue-Green Deployment**
- Use when: Zero-downtime required, instant rollback needed
- Characteristics: Full environment swap
- Rollback: Switch traffic back to blue environment
- Best for: Critical production services

**Canary Deployment**
- Use when: High-risk changes, need gradual validation
- Characteristics: Progressive traffic shifting (10% → 50% → 100%)
- Rollback: Automated on metric threshold breach
- Best for: Major feature releases

**Feature Flag Deployment**
- Use when: Code deployed but feature toggled
- Characteristics: Deployment decoupled from release
- Rollback: Disable feature flag
- Best for: Gradual feature rollouts

### 3. Prepare Environment

**For containerized deployments:**
```bash
# Verify image is available
docker pull <registry>/<image>:<tag>

# Verify image integrity
docker inspect <image> | grep -i "digest"

# Review image vulnerabilities
trivy image <registry>/<image>:<tag>
```

**For non-containerized deployments:**
```bash
# Verify artifact availability
# Check artifact checksums
# Verify configuration files
# Ensure dependencies are available
```

**Environment configuration:**
- Verify environment variables are set
- Check secrets are accessible
- Validate configuration files
- Test database connectivity

### 4. Execute Deployment

**For Kubernetes (Rolling Update):**
```yaml
# Update deployment with new image
kubectl set image deployment/<name> <container>=<image>:<tag>

# Monitor rollout status
kubectl rollout status deployment/<name>

# Watch pod status
kubectl get pods -w

# Check deployment events
kubectl describe deployment/<name>
```

**For Blue-Green Deployment:**
```yaml
1. Deploy new version to green environment
2. Run smoke tests against green environment
3. Verify health checks pass
4. Switch traffic from blue to green
5. Monitor metrics for anomalies
6. Keep blue environment ready for rollback
```

**For Canary Deployment:**
```yaml
1. Deploy canary version alongside stable
2. Route 10% of traffic to canary
3. Monitor canary metrics for 15-30 minutes
4. If healthy, increase to 50% traffic
5. Monitor for another 15-30 minutes
6. If healthy, increase to 100% traffic
7. Remove old version
```

**For Cloud Platforms:**
```bash
# AWS Elastic Beanstalk
eb deploy --label <version>

# Google App Engine
gcloud app deploy --version <version>

# Heroku
git push heroku main
```

### 5. Monitor Deployment

**Key metrics to watch:**
- Error rate (should not increase)
- Response time (should remain stable)
- Request rate (traffic shifting correctly)
- CPU/Memory usage (should be reasonable)
- Database connection pool (no exhaustion)

**Monitoring checklist:**
- [ ] Health checks passing
- [ ] Error rate within normal range
- [ ] Response times acceptable
- [ ] No increase in 5xx errors
- [ ] Logs show no critical errors
- [ ] Resource utilization normal
- [ ] Dependent services responding

**Set up monitoring:**
- Reference: `workflows/monitor.md` for full monitoring setup

### 6. Run Smoke Tests

**Execute post-deployment smoke tests:**
```yaml
Smoke test checklist:
- [ ] Application responds on expected port
- [ ] Health endpoint returns 200 OK
- [ ] Database connectivity working
- [ ] External API integrations functioning
- [ ] Authentication/authorization working
- [ ] Critical user flows operational
- [ ] Static assets loading correctly
```

**Automated smoke tests:**
```bash
# API health check
curl -f https://<domain>/health || exit 1

# Database connectivity
curl -f https://<domain>/api/status || exit 1

# Critical endpoint
curl -f https://<domain>/api/critical-feature || exit 1
```

### 7. Verify Deployment

**Post-deployment verification:**
- Reference: `context/checklists/post-deployment.md`

**Critical validations:**
- [ ] All pods/instances are running
- [ ] Health checks passing consistently
- [ ] No error spikes in logs
- [ ] Metrics within acceptable ranges
- [ ] Database migrations applied successfully
- [ ] Configuration changes active
- [ ] Cache invalidated if necessary
- [ ] CDN updated if applicable

**Check deployment details:**
```bash
# Kubernetes
kubectl get deployments
kubectl get pods
kubectl logs <pod-name>

# Docker
docker ps
docker logs <container-id>

# Cloud platform
# Use platform-specific commands to verify
```

### 8. Handle Issues

**If deployment issues occur:**

**Minor issues (warnings, non-critical errors):**
- Document issue
- Monitor for escalation
- Plan fix for next deployment
- Continue monitoring

**Major issues (service degradation):**
- Assess impact severity
- Consider rollback if > 5% error rate
- Engage incident response if needed
- Execute rollback procedure

**Critical issues (service down):**
- Execute immediate rollback (see `workflows/rollback.md`)
- Engage incident response team
- Notify stakeholders
- Preserve logs and metrics for post-mortem

### 9. Gradual Traffic Shift (Canary/Blue-Green)

**For canary deployments:**
```yaml
Phase 1: 10% traffic for 15-30 minutes
- Monitor error rate, latency, resource usage
- Compare metrics to stable version
- If degraded, roll back immediately

Phase 2: 50% traffic for 15-30 minutes
- Continue monitoring
- Validate database performance
- Check dependent service impact

Phase 3: 100% traffic
- Complete rollout
- Monitor for 1-2 hours
- Remove old version after stability confirmed
```

**For blue-green deployments:**
```yaml
1. Green environment receives 100% traffic
2. Monitor for 30-60 minutes
3. If stable, decommission blue environment
4. If issues, switch back to blue instantly
```

### 10. Post-Deployment Activities

**Communication:**
- Notify team of successful deployment
- Update status page if applicable
- Document any issues encountered
- Share deployment metrics with stakeholders

**Documentation:**
- Record deployment timestamp
- Document version deployed
- Note any manual steps taken
- Update runbooks if needed
- Create post-deployment report

**Monitoring:**
- Continue elevated monitoring for 24 hours
- Watch for gradual issues (memory leaks, etc.)
- Monitor business metrics for impact
- Set up alerts for anomalies

## Deliverables

**Deployment artifacts:**
- Deployed application version in target environment
- Deployment logs and metrics
- Post-deployment verification results
- Incident reports (if any issues occurred)

**Documentation:**
- Deployment timestamp and version
- Any manual steps taken
- Issues encountered and resolutions
- Rollback plan validation

## Validation Checklist

Before marking deployment complete:
- [ ] All instances/pods are healthy
- [ ] Health checks passing consistently
- [ ] Error rates within normal range
- [ ] Response times acceptable
- [ ] Smoke tests passing
- [ ] Monitoring active and showing normal metrics
- [ ] Logs reviewed, no critical errors
- [ ] Team notified of completion
- [ ] Rollback plan still accessible
- [ ] Post-deployment checklist completed

## Common Deployment Patterns

**Zero-downtime deployment:**
```yaml
1. Ensure multiple instances running
2. Use rolling update strategy
3. Configure readiness probes
4. Set proper termination grace period
5. Wait for new pods ready before terminating old
```

**Database migration deployment:**
```yaml
1. Deploy backward-compatible schema changes first
2. Deploy application code
3. Verify application works with old and new schema
4. Deploy data migration
5. Remove backward compatibility code in next release
```

**Configuration-only deployment:**
```yaml
1. Update ConfigMap/environment variables
2. Trigger rolling restart of pods
3. Verify new configuration loaded
4. Monitor for configuration-related errors
```

## Troubleshooting

**Pods/instances not starting:**
- Check resource limits (CPU/memory)
- Review application logs
- Verify image availability
- Check secrets/config availability

**Health checks failing:**
- Verify health endpoint logic
- Check application startup time vs. probe timing
- Review application logs for startup errors
- Validate database connectivity

**Deployment stuck/hanging:**
- Check pod events: `kubectl describe pod <name>`
- Review resource quotas
- Verify image pull secrets
- Check for pod security policy blocks

**Performance degradation:**
- Review resource allocation
- Check database connection pooling
- Verify cache configuration
- Monitor dependent service health

## Rollback Triggers

Execute rollback immediately if:
- Error rate increases > 5% above baseline
- Response time degrades > 50% above baseline
- Health checks failing on > 10% of instances
- Critical functionality broken
- Security vulnerability discovered
- Database corruption detected

**Rollback procedure:** See `workflows/rollback.md`

## Success Metrics

A successful deployment achieves:
- **Zero downtime** or within agreed maintenance window
- **Error rate** remains stable (< 1% increase)
- **Response time** remains within SLA
- **Quick rollout** completed in planned timeframe
- **Healthy instances** all pods/instances pass health checks
- **No incidents** no customer-facing issues
- **Clean logs** no critical errors in application logs
