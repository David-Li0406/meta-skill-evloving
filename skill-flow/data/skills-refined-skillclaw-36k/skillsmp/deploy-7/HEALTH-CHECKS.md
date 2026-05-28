# Health Check Commands

Quick reference for verifying deployment health.

## All Services (Quick Check)

```bash
# Check all services at once
for port in 8000 8081 8082 8083 8084 8085; do
  status=$(curl -s -o /dev/null -w "%{http_code}" http://192.168.50.35:$port/health)
  if [ "$status" = "200" ]; then
    echo "✅ Port $port: healthy"
  else
    echo "❌ Port $port: unhealthy (HTTP $status)"
  fi
done
```

## Individual Services

### Backend (Port 8000)

```bash
curl -s http://192.168.50.35:8000/health | jq .
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "telegram": "polling",
  "version": "..."
}
```

### Telegram MCP (Port 8081)

```bash
curl -s http://192.168.50.35:8081/health | jq .
```

### Motion MCP (Port 8082)

```bash
curl -s http://192.168.50.35:8082/health | jq .
```

### GitHub MCP (Port 8083)

```bash
curl -s http://192.168.50.35:8083/health | jq .
```

### Google Calendar MCP (Port 8084)

```bash
# Health check
curl -s http://192.168.50.35:8084/health | jq .

# OAuth status
curl -s http://192.168.50.35:8084/auth/status | jq .
```

### Gmail MCP (Port 8085)

```bash
# Health check
curl -s http://192.168.50.35:8085/health | jq .

# OAuth status
curl -s http://192.168.50.35:8085/auth/status | jq .
```

### Frontend (Port 3000)

```bash
curl -s -o /dev/null -w "%{http_code}" http://192.168.50.35:3000/
# Should return 200
```

## Container Status

```bash
# List all claude-assistant containers
ssh user@192.168.50.35 "docker ps --filter 'name=claude-assistant' --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'"
```

Expected output:
```
NAMES                                  STATUS          PORTS
claude-assistant-frontend              Up 2 hours      0.0.0.0:3000->3000/tcp
claude-assistant-backend               Up 2 hours      0.0.0.0:8000->8000/tcp
claude-assistant-telegram-mcp          Up 2 hours      0.0.0.0:8081->8080/tcp
claude-assistant-motion-mcp            Up 2 hours      0.0.0.0:8082->8081/tcp
claude-assistant-github-mcp            Up 2 hours      0.0.0.0:8083->8083/tcp
claude-assistant-google-calendar-mcp   Up 2 hours      0.0.0.0:8084->8084/tcp
claude-assistant-gmail-mcp             Up 2 hours      0.0.0.0:8085->8085/tcp
```

## Container Logs

```bash
# Recent logs for specific service
ssh user@192.168.50.35 "docker logs --tail 50 claude-assistant-backend"

# Follow logs in real-time
ssh user@192.168.50.35 "docker logs -f claude-assistant-backend"

# Logs with timestamps
ssh user@192.168.50.35 "docker logs --tail 50 -t claude-assistant-backend"
```

## Database Connection

```bash
# Check if backend can reach database
curl -s http://192.168.50.35:8000/health | jq '.database'
# Should return "connected"
```

## Network Connectivity

```bash
# Verify Docker network
ssh user@192.168.50.35 "docker network inspect claude-assistant-network --format '{{range .Containers}}{{.Name}} {{end}}'"
```

## OAuth Re-authentication

If Google services show "not authenticated":

```bash
# Get auth URL for Google Calendar
curl -s http://192.168.50.35:8084/auth/url

# Get auth URL for Gmail
curl -s http://192.168.50.35:8085/auth/url
```

Open the returned URL in a browser to complete OAuth flow.
