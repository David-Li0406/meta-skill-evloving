# Workflow: Rollback Deployment

## Purpose
Safely and quickly revert to a previous stable version when a deployment causes issues. This workflow ensures minimal downtime and service restoration with proper validation.

## When to Use
- New deployment causes elevated error rates
- Service degradation or outages after deployment
- Critical bugs discovered in production
- Security vulnerabilities in deployed version
- Failed health checks or monitoring alerts
- Customer-reported issues after deployment

## Prerequisites
- Previous stable version is known and accessible
- Monitoring shows deployment is causing issues
- Decision to rollback has been made
- Team is notified of rollback in progress

## Rollback Decision Criteria

**Rollback immediately if:**
- Error rate increases > 5% above baseline
- Response time degrades > 50% above baseline
- Health checks failing on > 10% of instances
- Critical functionality is broken
- Security vulnerability discovered
- Database corruption detected
- Service completely down

**Consider rollback if:**
- Error rate increases 2-5% above baseline
- Response time degrades 20-50% above baseline
- Non-critical functionality broken
- Performance degradation affecting users
- Monitoring alerts firing persistently

**Don't rollback for:**
- Minor cosmetic issues
- Single-instance failures (in multi-instance setup)
- Temporary spikes that resolve
- Known and acceptable issues

## Workflow Steps

### 1. Assess Situation

**Gather critical information:**
- What version is currently deployed?
- What was the previous stable version?
- When did the deployment occur?
- What is the current error rate and impact?
- How many users/requests are affected?
- Is this a partial rollout (canary) or full deployment?

**Check monitoring:**
- Review error rate trends
- Check response time metrics
- Review recent logs for errors
- Assess customer impact
- Verify issue correlation with deployment

**Ask clarifying questions:**
- "What symptoms are you seeing?"
- "What version was deployed and when?"
- "What was the last known stable version?"
- "Is this a full rollback or partial traffic shift?"

### 2. Notify Stakeholders

**Immediate notifications:**
```yaml
Notify:
  - Development team
  - On-call engineers
  - Product/business stakeholders
  - Customer support team (if customer-facing)

Communication should include:
  - Issue description
  - Decision to rollback
  - Expected rollback duration
  - Current impact assessment
```

**Update status page:**
- If customer-facing, update status page
- Set status to "Investigating" or "Identified"
- Provide transparent communication

### 3. Prepare for Rollback

**Identify rollback target:**
```bash
# For Kubernetes
kubectl rollout history deployment/<name>

# Identify previous revision
kubectl rollout history deployment/<name> --revision=<number>

# For Docker
docker images | grep <image-name>

# For cloud platforms
# Check deployment history in platform UI
```

**Verify previous version availability:**
```bash
# Verify image/artifact exists
docker pull <registry>/<image>:<previous-tag>

# Or verify artifact in artifact repository
```

**Preserve current state for debugging:**
```bash
# Kubernetes: Save current deployment
kubectl get deployment <name> -o yaml > deployment-failed.yaml

# Capture current logs
kubectl logs <pod-name> > failed-deployment-logs.txt

# Take snapshot of metrics
# Screenshot dashboards showing issue
```

### 4. Execute Rollback

**For Kubernetes (Automated Rollback):**
```bash
# Quick rollback to previous revision
kubectl rollout undo deployment/<name>

# Or rollback to specific revision
kubectl rollout undo deployment/<name> --to-revision=<number>

# Monitor rollback progress
kubectl rollout status deployment/<name>

# Watch pods
kubectl get pods -w

# Verify rollback completed
kubectl rollout history deployment/<name>
```

**For Blue-Green Deployment:**
```yaml
1. Identify blue (stable) environment
2. Switch traffic back from green to blue
3. Verify traffic flowing to blue
4. Monitor blue environment health
5. Keep green environment for debugging
```

**For Canary Deployment:**
```yaml
1. Immediately stop traffic to canary
2. Route 100% traffic to stable version
3. Remove canary instances
4. Verify all traffic on stable
5. Monitor for stability
```

**For Cloud Platforms:**
```bash
# AWS Elastic Beanstalk
eb deploy --version <previous-version-label>

# Google App Engine
gcloud app services set-traffic <service> --splits <previous-version>=1

# Heroku
heroku rollback
# Or specific release
heroku releases:rollback v<number>

# Azure App Service
az webapp deployment slot swap --name <app> --resource-group <group> --slot staging --target-slot production
```

**For Manual Deployments:**
```bash
# Stop current version
systemctl stop <service>

# Deploy previous version
# (specific steps depend on deployment method)

# Start previous version
systemctl start <service>

# Verify service is running
systemctl status <service>
```

### 5. Verify Rollback

**Immediate checks:**
```bash
# Kubernetes
kubectl get pods
# Ensure all pods running

kubectl get deployment <name>
# Verify correct image/version

# Check health endpoint
curl https://<domain>/health

# Check application version endpoint
curl https://<domain>/version
```

**Health validation:**
- [ ] All instances/pods are running
- [ ] Health checks passing
- [ ] Version endpoint shows correct version
- [ ] Service responding to requests
- [ ] No error spikes in logs

### 6. Monitor Recovery

**Watch key metrics:**
```yaml
Monitor for 15-30 minutes:
  - Error rate should return to normal
  - Response time should stabilize
  - No new errors in logs
  - Customer reports should decrease
  - Dependent services stable
```

**Validation checklist:**
- [ ] Error rate back to < 1%
- [ ] Response time within SLA
- [ ] Health checks passing consistently
- [ ] No critical errors in logs
- [ ] Customer support reports declining
- [ ] Business metrics normal
- [ ] Dependent services healthy

**Check rollback completeness:**
```bash
# Verify all instances on previous version
kubectl get pods -o jsonpath='{.items[*].spec.containers[*].image}'

# Check deployment revision
kubectl rollout history deployment/<name>

# Verify no pods from failed deployment
kubectl get pods | grep <failed-version>
```

### 7. Preserve Evidence

**Collect debugging information:**
```bash
# Save failed deployment configuration
kubectl get deployment <name> -o yaml > failed-deployment.yaml

# Export failed pod logs
kubectl logs <failed-pod> > failed-pod-logs.txt
kubectl logs <failed-pod> --previous > failed-pod-previous-logs.txt

# Export events
kubectl get events --sort-by='.lastTimestamp' > failed-deployment-events.txt

# Take metric snapshots
# Export Grafana dashboards as JSON
# Screenshot critical metrics during failure
```

**Preserve for post-mortem:**
- Failed deployment configuration
- Pod/instance logs during failure
- Metrics and graphs showing issue
- Error messages and stack traces
- Database query logs (if relevant)
- Customer reports and support tickets

### 8. Communicate Status

**Update stakeholders:**
```markdown
Rollback Complete Notification:

Subject: Rollback Completed - [Service Name]

Summary:
- Deployment of version X.Y.Z caused [issue description]
- Rolled back to version X.Y.Z-1 at [timestamp]
- Service is now stable
- Impact: [number] users affected for [duration]

Current Status:
- Error rate: Back to normal (< 1%)
- Response time: Within SLA
- All instances healthy

Next Steps:
- Post-mortem scheduled for [date/time]
- Root cause analysis in progress
- Fix will be developed and tested before redeployment
```

**Update status page:**
- Change status to "Resolved"
- Provide incident timeline
- Explain resolution (rolled back)
- Indicate when fix will be deployed

### 9. Conduct Post-Mortem

**Schedule blameless post-mortem:**
- Within 24-48 hours of incident
- Include all relevant team members
- Focus on systems and processes, not individuals

**Post-mortem agenda:**
1. Timeline of events
2. What went wrong (root cause)
3. What went right (rollback worked)
4. Impact assessment
5. Action items to prevent recurrence
6. Process improvements

**Document learnings:**
```markdown
# Post-Mortem: [Deployment Incident]

## Summary
[Brief description of what happened]

## Timeline
- [Time]: Deployment initiated
- [Time]: Error rate began increasing
- [Time]: Alert fired
- [Time]: Decision to rollback made
- [Time]: Rollback initiated
- [Time]: Service restored

## Root Cause
[Technical explanation of what caused the issue]

## Impact
- Duration: [X] minutes
- Users affected: [Y]
- Error count: [Z]
- Business impact: [description]

## What Went Well
- Fast detection ([X] minutes)
- Quick rollback decision
- Smooth rollback execution
- Good communication

## What Went Wrong
- [Issue 1]
- [Issue 2]
- [Issue 3]

## Action Items
- [ ] [Fix root cause - Owner - Deadline]
- [ ] [Improve testing - Owner - Deadline]
- [ ] [Add monitoring - Owner - Deadline]
- [ ] [Update runbooks - Owner - Deadline]
```

### 10. Plan Next Deployment

**Before redeploying:**
- [ ] Root cause identified and fixed
- [ ] Additional tests added to catch issue
- [ ] Fix verified in staging environment
- [ ] Rollback plan updated with learnings
- [ ] Team briefed on what went wrong
- [ ] Enhanced monitoring for issue area
- [ ] Staged rollout plan (canary if high risk)

**Update deployment process:**
- Add tests that would have caught the issue
- Improve health checks
- Add relevant monitoring
- Update deployment checklist
- Document new failure mode

## Rollback Time Targets

**Target rollback times:**
- **Critical outage**: < 5 minutes to initiate rollback
- **Major issue**: < 10 minutes to initiate rollback
- **Minor issue**: < 30 minutes to assess and decide

**Rollback execution should complete:**
- Kubernetes: 2-5 minutes
- Blue-green: < 1 minute (traffic switch)
- Canary: < 2 minutes (stop canary traffic)
- Cloud platforms: 5-15 minutes

## Common Rollback Issues

**Rollback fails to resolve issue:**
- Issue may not be from deployment
- Database migration may be incompatible
- External dependency may have changed
- Consider if rollforward is better option

**Database migration complications:**
- If migration is not backward compatible
- May need to rollback database separately
- Plan database rollback strategy ahead of time
- Consider forward-compatible migrations only

**Configuration changes:**
- If rollback includes config changes
- Verify config is also rolled back
- Check secrets/environment variables
- Validate external service configurations

**Partial rollback needed:**
- In multi-region deployments
- May rollback only affected regions
- Coordinate rollback across regions
- Maintain traffic routing during rollback

## Troubleshooting

**Rollback command fails:**
```bash
# Check deployment status
kubectl get deployment <name>

# Check for resource issues
kubectl describe deployment <name>

# Manual rollback if automated fails
kubectl set image deployment/<name> <container>=<previous-image>
```

**Pods not rolling back:**
```bash
# Check pod events
kubectl describe pod <pod-name>

# Force pod deletion if stuck
kubectl delete pod <pod-name> --force --grace-period=0

# Check for resource constraints
kubectl get nodes
kubectl describe node <node-name>
```

**Previous version not available:**
- Ensure image retention policies allow rollback
- Keep at least 3-5 previous versions available
- Verify artifact repository access
- Have emergency deployment procedure

## Prevention Strategies

**Reduce rollback need:**
- Comprehensive testing in staging
- Canary deployments for risky changes
- Feature flags to decouple deploy from release
- Gradual rollouts with monitoring
- Automated rollback on metric threshold breach

**Improve rollback speed:**
- Practice rollback procedures regularly
- Automate rollback commands
- Document rollback procedures clearly
- Maintain runbooks for common scenarios
- Test rollback in staging environment

## Success Metrics

A successful rollback achieves:
- **Quick execution** - Rollback completed in < 5 minutes
- **Full recovery** - Error rate and performance restored
- **Evidence preserved** - Logs and metrics saved for analysis
- **Communication** - Stakeholders informed throughout
- **Learning** - Post-mortem conducted and documented
- **Prevention** - Action items defined and tracked
