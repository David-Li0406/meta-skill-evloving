# DevOps Debugging Workflow

## When to Use

- Deployment failures
- Container issues (Docker, Kubernetes)
- CI/CD pipeline failures
- Infrastructure problems
- Service unavailable
- Resource exhaustion

## Step 1: Gather Symptoms

```
□ What exactly is failing? (error message, status)
□ When did it start?
□ What was the last successful deployment?
□ What changed? (code, config, infra)
□ Is it affecting all instances or specific ones?
□ What does monitoring show?
```

## Step 2: Check Service Status

### Quick health checks:
```bash
# Is the service running?
systemctl status myapp
docker ps
kubectl get pods

# Is it responding?
curl -I http://localhost:8080/health

# Check resource usage
docker stats
kubectl top pods
htop
```

## Step 3: Container Debugging (Docker)

### View logs:
```bash
# Live logs
docker logs -f container_name

# Last 100 lines
docker logs --tail 100 container_name

# With timestamps
docker logs -t container_name
```

### Inspect container:
```bash
# Container details
docker inspect container_name

# Execute shell in running container
docker exec -it container_name /bin/sh

# See what's different from image
docker diff container_name
```

### Common Docker issues:

| Symptom | Check | Likely Cause |
|---------|-------|--------------|
| Container exits immediately | `docker logs` | App crash, missing env |
| Container won't start | `docker inspect` | Port conflict, volume issue |
| OOMKilled | `docker stats` | Memory limit too low |
| Unhealthy | Health check endpoint | App not ready, wrong port |

## Step 4: Kubernetes Debugging

### Pod status:
```bash
# Overview
kubectl get pods -o wide
kubectl describe pod pod_name

# Logs
kubectl logs pod_name
kubectl logs pod_name --previous  # Previous crash

# Events
kubectl get events --sort-by=.lastTimestamp
```

### Common K8s issues:

```
CrashLoopBackOff
→ App crashing repeatedly
→ Check: logs, env vars, config

ImagePullBackOff
→ Can't pull container image
→ Check: image name, registry auth, network

Pending
→ Can't schedule pod
→ Check: resources, node availability, affinity

OOMKilled
→ Memory limit exceeded
→ Check: memory limits, app memory usage
```

### Debug pods:
```bash
# Shell into pod
kubectl exec -it pod_name -- /bin/sh

# Run debug container
kubectl debug pod_name -it --image=busybox

# Port forward for local testing
kubectl port-forward pod_name 8080:8080
```

## Step 5: CI/CD Pipeline Debugging

### Identify failure point:
```
Pipeline stages:
1. Checkout
2. Install dependencies
3. Build
4. Test
5. Package/Docker build
6. Deploy

→ Which stage failed?
→ Check logs for that stage
```

### Common CI issues:

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Dependency install fails | Version conflict, missing dep | Lock file, clear cache |
| Build fails | Code error, env diff | Test locally same env |
| Tests fail | Flaky, env diff | See debug-tests workflow |
| Docker build fails | Layer cache, base image | Clear cache, update base |
| Deploy fails | Permissions, config | Check secrets, IAM |

### GitHub Actions debugging:
```yaml
# Add debug step
- name: Debug
  run: |
    echo "PWD: $(pwd)"
    ls -la
    env | sort

# Enable debug logging
# Set secret: ACTIONS_STEP_DEBUG = true
```

## Step 6: Infrastructure Debugging

### Check resources:
```bash
# Disk space
df -h
du -sh /*

# Memory
free -h

# CPU
top -bn1 | head -20

# Network
netstat -tlnp
ss -tlnp
```

### Cloud-specific:

```bash
# AWS
aws ec2 describe-instances --instance-id i-xxx
aws logs tail /aws/lambda/func-name
aws cloudwatch get-metric-statistics ...

# GCP
gcloud compute instances describe instance-name
gcloud logging read "resource.type=gce_instance"

# Azure
az vm show --name vm-name --resource-group rg
az monitor activity-log list
```

## Step 7: Network Debugging

```bash
# DNS resolution
nslookup hostname
dig hostname

# Port connectivity
nc -zv hostname port
telnet hostname port

# HTTP request
curl -v http://hostname:port/path

# Trace route
traceroute hostname
mtr hostname
```

### Common network issues:
- Security groups / firewall blocking
- DNS not resolving
- Service discovery not updating
- Load balancer health check failing

## Step 8: Configuration Issues

### Environment variables:
```bash
# In container
docker exec container printenv
kubectl exec pod -- printenv

# Check for missing vars
grep -r "getenv\|process.env\|os.environ" src/
```

### Secrets:
```bash
# Kubernetes secrets (base64 encoded)
kubectl get secret secret-name -o jsonpath='{.data.key}' | base64 -d

# Check secret exists
kubectl get secrets
```

### Config files:
```bash
# Compare with expected
diff -u expected.conf actual.conf

# Validate syntax
nginx -t
docker-compose config
kubectl apply --dry-run=client -f manifest.yaml
```

## Step 9: Common Deployment Patterns

### Blue-Green Issues
```
□ Is traffic routing to correct version?
□ Are health checks passing on new version?
□ Does rollback work?
```

### Rolling Update Issues
```
□ Are pods becoming ready?
□ Is there enough capacity during rollout?
□ Are connection draining settings correct?
```

### Canary Issues
```
□ Is traffic split correctly?
□ Are metrics comparing correctly?
□ Is rollback automated on failure?
```

## Step 10: Fix and Document

```
1. Apply fix (minimal change)
2. Verify service is healthy
3. Check monitoring for anomalies
4. Update runbook if new issue type
5. Consider adding alerting if not caught early
6. Post-mortem if significant outage
```

## Quick Reference: Emergency Commands

```bash
# Restart service
systemctl restart myapp
docker restart container_name
kubectl rollout restart deployment/myapp

# Rollback
kubectl rollout undo deployment/myapp
docker-compose up -d --no-deps service_name

# Scale up/down
kubectl scale deployment/myapp --replicas=3
docker-compose up -d --scale service=3

# Kill stuck process
kill -9 $(pgrep -f myapp)
docker kill container_name
kubectl delete pod pod_name --force
```

## Debugging Checklist

```
□ Check service status/health
□ Read logs (application and system)
□ Check recent changes (git, deployments)
□ Verify configuration (env, secrets, files)
□ Check resources (CPU, memory, disk)
□ Check network (DNS, ports, connectivity)
□ Compare with working environment
□ Test fix in staging first
```
