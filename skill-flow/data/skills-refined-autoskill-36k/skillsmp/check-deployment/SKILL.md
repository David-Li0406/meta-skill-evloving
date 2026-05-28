---
name: check-deployment
description: Check deployment status on Orange Pi - container health, logs, and service status. Use when checking if deployment succeeded, debugging production issues, verifying services are running, or when user asks "is it running", "check prod", "deployment status", "are services up", or "production health".
allowed-tools: Read, Bash(curl:*), Bash(ssh:*), Grep
---

# Check Deployment Status

This skill verifies the health and status of the production deployment on Orange Pi.

## Quick Status Check

### All Services Health

```bash
echo "=== Service Health ==="
for port in 8000 8081 8082 8083 8084 8085; do
  name=$(case $port in
    8000) echo "Backend" ;;
    8081) echo "Telegram MCP" ;;
    8082) echo "Motion MCP" ;;
    8083) echo "GitHub MCP" ;;
    8084) echo "Calendar MCP" ;;
    8085) echo "Gmail MCP" ;;
  esac)
  status=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 http://192.168.50.35:$port/health)
  if [ "$status" = "200" ]; then
    echo "✅ $name (port $port): healthy"
  else
    echo "❌ $name (port $port): unhealthy (HTTP $status)"
  fi
done
```

### Container Status

```bash
ssh user@192.168.50.35 "docker ps --filter 'name=claude-assistant' --format 'table {{.Names}}\t{{.Status}}'"
```

## Detailed Checks

### Backend Service

```bash
# Health endpoint
curl -s http://192.168.50.35:8000/health | jq .

# Recent logs
ssh user@192.168.50.35 "docker logs --tail 20 claude-assistant-backend"
```

### MCP Servers

```bash
# Telegram MCP
curl -s http://192.168.50.35:8081/health | jq .

# Motion MCP
curl -s http://192.168.50.35:8082/health | jq .

# GitHub MCP
curl -s http://192.168.50.35:8083/health | jq .

# Google Calendar MCP (includes OAuth status)
curl -s http://192.168.50.35:8084/health | jq .
curl -s http://192.168.50.35:8084/auth/status | jq .

# Gmail MCP (includes OAuth status)
curl -s http://192.168.50.35:8085/health | jq .
curl -s http://192.168.50.35:8085/auth/status | jq .
```

### Frontend

```bash
# Check if serving
curl -s -o /dev/null -w "%{http_code}" http://192.168.50.35:3000/
```

## Common Issues

### Container Not Running

```bash
# Check if container exists but stopped
ssh user@192.168.50.35 "docker ps -a --filter 'name=claude-assistant-backend'"

# Check exit code
ssh user@192.168.50.35 "docker inspect claude-assistant-backend --format '{{.State.ExitCode}}'"

# View logs for crash reason
ssh user@192.168.50.35 "docker logs --tail 50 claude-assistant-backend"
```

### Health Check Failing

```bash
# Check detailed health
curl -v http://192.168.50.35:8000/health

# Check container health status
ssh user@192.168.50.35 "docker inspect claude-assistant-backend --format '{{.State.Health.Status}}'"
```

### Network Issues

```bash
# Check Docker network
ssh user@192.168.50.35 "docker network inspect claude-assistant-network"

# Verify containers are on network
ssh user@192.168.50.35 "docker network inspect claude-assistant-network --format '{{range .Containers}}{{.Name}} {{end}}'"
```

### OAuth Not Working

```bash
# Check Google Calendar auth
curl -s http://192.168.50.35:8084/auth/status | jq '.authenticated'

# If false, get auth URL
curl -s http://192.168.50.35:8084/auth/url

# Same for Gmail
curl -s http://192.168.50.35:8085/auth/status | jq '.authenticated'
curl -s http://192.168.50.35:8085/auth/url
```

## Resource Usage

```bash
# Check container resource usage
ssh user@192.168.50.35 "docker stats --no-stream --format 'table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}' \$(docker ps -q --filter 'name=claude-assistant')"
```

## Recent Deployments

```bash
# Check when containers were created
ssh user@192.168.50.35 "docker ps --filter 'name=claude-assistant' --format 'table {{.Names}}\t{{.CreatedAt}}'"

# Check image versions
ssh user@192.168.50.35 "docker ps --filter 'name=claude-assistant' --format 'table {{.Names}}\t{{.Image}}'"
```

## Status Report Template

```
## Deployment Status Report

**Checked at:** [timestamp]

### Services
| Service | Status | Details |
|---------|--------|---------|
| Backend | ✅/❌ | [details] |
| Telegram MCP | ✅/❌ | [details] |
| Motion MCP | ✅/❌ | [details] |
| GitHub MCP | ✅/❌ | [details] |
| Google Calendar MCP | ✅/❌ | OAuth: [status] |
| Gmail MCP | ✅/❌ | OAuth: [status] |
| Frontend | ✅/❌ | [details] |

### Issues Found
- [List any issues]

### Recommendations
- [List any recommended actions]
```
