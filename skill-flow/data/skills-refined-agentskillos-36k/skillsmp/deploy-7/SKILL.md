---
name: deploy
description: Deploy Claude Assistant Platform to Orange Pi via Jenkins. Use when deploying to production, triggering a build, releasing, or when user says "deploy", "push to prod", "release", "ship it", or "deploy to orange pi".
allowed-tools: Read, Bash(curl:*), Bash(git:*), Grep
---

# Deploy to Orange Pi

This skill handles deployment of the Claude Assistant Platform to the Orange Pi production server.

## Quick Deploy

Trigger Jenkins pipeline:

```bash
curl -X POST "http://192.168.50.35:8080/job/claude-assistant-platform/build" \
  --user "$JENKINS_USER:$JENKINS_TOKEN"
```

## Pre-Deployment Checklist

Before deploying, verify:

- [ ] All tests pass locally (`uv run pytest`)
- [ ] No uncommitted changes (`git status`)
- [ ] Current branch is `main` or PR is merged
- [ ] No breaking changes without migration plan

## Deployment Process

### 1. Verify Local State

```bash
# Check for uncommitted changes
git status

# Verify on correct branch
git branch --show-current

# Ensure up to date with remote
git fetch origin main
git log HEAD..origin/main --oneline
```

### 2. Trigger Jenkins Build

The Jenkins pipeline will:
1. Build all 7 Docker images in parallel (ARM64)
2. Push images to registry at `192.168.50.35:5000`
3. Stop existing containers
4. Start new containers in order (MCP servers → Backend → Frontend)
5. Run health checks

### 3. Monitor Progress

- **Jenkins UI**: `http://192.168.50.35:8080`
- **Build Log**: Use Jenkins MCP `getBuildLog` tool
- **Console Output**: Watch for stage completion

### 4. Verify Deployment

After Jenkins reports success, verify services:

```bash
# Check all health endpoints
for port in 8000 8081 8082 8083 8084 8085 3000; do
  echo "Port $port: $(curl -s http://192.168.50.35:$port/health 2>/dev/null | jq -r '.status // "FAILED"')"
done
```

## Service URLs

| Service | URL |
|---------|-----|
| Backend | http://192.168.50.35:8000 |
| Frontend | http://192.168.50.35:3000 |
| Telegram MCP | http://192.168.50.35:8081 |
| Motion MCP | http://192.168.50.35:8082 |
| GitHub MCP | http://192.168.50.35:8083 |
| Google Calendar MCP | http://192.168.50.35:8084 |
| Gmail MCP | http://192.168.50.35:8085 |

## Rollback

If deployment fails, see [ROLLBACK.md](ROLLBACK.md) for rollback procedures.

## Health Checks

See [HEALTH-CHECKS.md](HEALTH-CHECKS.md) for detailed health check commands.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Jenkins build fails | Check build log for specific stage failure |
| Container won't start | Check container logs: `docker logs <container>` |
| Health check fails | Verify environment variables are set |
| MCP not responding | Check Docker network connectivity |
| OAuth errors | Re-authenticate via `/auth/url` endpoint |

## Reference

- `Jenkinsfile` - Pipeline definition
- `DOCUMENTATION/DEPLOYMENT.md` - Full deployment reference
- `.claude/rules/infrastructure/orange-pi.md` - ARM64 requirements
