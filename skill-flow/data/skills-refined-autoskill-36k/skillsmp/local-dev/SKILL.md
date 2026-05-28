---
name: local-dev
description: Run the Claude Assistant Platform locally for development. Use when starting local development, running services locally, testing locally, or when user says "run locally", "start dev", "local setup", "dev environment", or "run the stack".
allowed-tools: Read, Bash, Grep, Write, Edit
---

# Local Development Setup

This skill runs the full Claude Assistant Platform stack locally for development.

## Services Required for Local Development

| Service | Directory | Port | Health Check |
|---------|-----------|------|--------------|
| Backend | `Backend/` | 8000 | `http://localhost:8000/health` |
| Motion MCP | `MCPS/motion/` | 8081 | `http://localhost:8081/health` |
| GitHub MCP | `MCPS/github/` | 8083 | `http://localhost:8083/health` |
| Google Calendar MCP | `MCPS/google-calendar/` | 8084 | `http://localhost:8084/health` |
| Gmail MCP | `MCPS/gmail/` | 8085 | `http://localhost:8085/health` |
| Google Drive MCP | `MCPS/google-drive/` | 8087 | `http://localhost:8087/health` |
| Frontend | `Frontend/` | 3000 | `http://localhost:3000/` |

**Note:** Telegram MCP is NOT included - it runs as part of the Backend service.

## Database Configuration

**The PostgreSQL database runs on the local network at `192.168.50.35:5432`, NOT locally.**

The database is already deployed and does not need to be started as part of local development. Ensure your `.env` file has:

```bash
POSTGRES_HOST=192.168.50.35
POSTGRES_PORT=5432
```

To verify database connectivity:
```bash
# Test connection to network database
pg_isready -h 192.168.50.35 -p 5432 -U postgres
```

## Step 1: Check Prerequisites

Before starting, verify:

```bash
# Check uv is installed
uv --version > /dev/null 2>&1 && echo "uv: OK" || echo "uv: NOT INSTALLED"

# Check node is installed
node --version > /dev/null 2>&1 && echo "Node: OK" || echo "Node: NOT INSTALLED"
```

## Step 2: Check Which Services Are Already Running

**IMPORTANT:** Before starting any service, check if it's already running to avoid port conflicts.

```bash
# Check all service health endpoints
echo "=== Checking Service Status ==="

# Backend (port 8000)
curl -s -o /dev/null -w "%{http_code}" --connect-timeout 2 http://localhost:8000/health 2>/dev/null | grep -q "200" && echo "Backend (8000): RUNNING" || echo "Backend (8000): NOT RUNNING"

# Motion MCP (port 8081)
curl -s -o /dev/null -w "%{http_code}" --connect-timeout 2 http://localhost:8081/health 2>/dev/null | grep -q "200" && echo "Motion MCP (8081): RUNNING" || echo "Motion MCP (8081): NOT RUNNING"

# GitHub MCP (port 8083)
curl -s -o /dev/null -w "%{http_code}" --connect-timeout 2 http://localhost:8083/health 2>/dev/null | grep -q "200" && echo "GitHub MCP (8083): RUNNING" || echo "GitHub MCP (8083): NOT RUNNING"

# Google Calendar MCP (port 8084)
curl -s -o /dev/null -w "%{http_code}" --connect-timeout 2 http://localhost:8084/health 2>/dev/null | grep -q "200" && echo "Google Calendar MCP (8084): RUNNING" || echo "Google Calendar MCP (8084): NOT RUNNING"

# Gmail MCP (port 8085)
curl -s -o /dev/null -w "%{http_code}" --connect-timeout 2 http://localhost:8085/health 2>/dev/null | grep -q "200" && echo "Gmail MCP (8085): RUNNING" || echo "Gmail MCP (8085): NOT RUNNING"

# Google Drive MCP (port 8087)
curl -s -o /dev/null -w "%{http_code}" --connect-timeout 2 http://localhost:8087/health 2>/dev/null | grep -q "200" && echo "Google Drive MCP (8087): RUNNING" || echo "Google Drive MCP (8087): NOT RUNNING"

# Frontend (port 3000)
curl -s -o /dev/null -w "%{http_code}" --connect-timeout 2 http://localhost:3000/ 2>/dev/null | grep -q "200" && echo "Frontend (3000): RUNNING" || echo "Frontend (3000): NOT RUNNING"
```

## Step 3: Start Services That Are Not Running

For each service that is NOT running, start it in a new terminal/background.

### Start MCP Servers First (Backend depends on these)

**Motion MCP (if not running):**
```bash
cd MCPS/motion
make run
# Runs on port 8081
```

**GitHub MCP (if not running):**
```bash
cd MCPS/github
make run
# Runs on port 8083
```

**Google Calendar MCP (if not running):**
```bash
cd MCPS/google-calendar
make run
# Runs on port 8084
```

**Gmail MCP (if not running):**
```bash
cd MCPS/gmail
make run
# Runs on port 8085
```

**Google Drive MCP (if not running):**
```bash
cd MCPS/google-drive
make run
# Runs on port 8087
```

### Start Backend (after MCP servers are ready)

**Backend (if not running):**
```bash
cd Backend
make run
# Runs on port 8000
# Also starts Telegram polling if TELEGRAM_BOT_TOKEN is set
```

### Start Frontend (after Backend is ready)

**Frontend (if not running):**
```bash
cd Frontend
npm run dev
# Runs on port 3000
```

## Agent Instructions

When running this skill, follow these steps:

1. **Verify database connectivity**: The database runs on the network at `192.168.50.35:5432` - do NOT start a local database
2. **Run health check script**: Execute the health check commands to see what's running
3. **Start missing services**: For each service showing "NOT RUNNING":
   - Navigate to its directory
   - Run `make run` (or `npm run dev` for Frontend)
   - Use background execution if running multiple services
4. **Verify all healthy**: Re-run health checks to confirm all services started

### Running Services in Background

Since all services need to run simultaneously, use background execution:

```bash
# Example: Start Motion MCP in background
cd MCPS/motion && make run &

# Or use separate terminal sessions
# The agent should inform the user to open multiple terminals
```

### Recommended Startup Order

1. Motion MCP (make run in MCPS/motion/)
2. GitHub MCP (make run in MCPS/github/)
3. Google Calendar MCP (make run in MCPS/google-calendar/)
4. Gmail MCP (make run in MCPS/gmail/)
5. Google Drive MCP (make run in MCPS/google-drive/)
6. Backend (make run in Backend/)
7. Frontend (npm run dev in Frontend/)

**Note:** Database is already running on the network - no local database startup required.

## Environment Variables Required

Ensure `.env` exists in project root with:

| Variable | Required | Service |
|----------|----------|---------|
| `ANTHROPIC_API_KEY` | Yes | Backend |
| `POSTGRES_PASSWORD` | Yes | Database |
| `TELEGRAM_BOT_TOKEN` or `TELEGRAM_DEV_BOT_TOKEN` | Yes | Backend |
| `TELEGRAM_ALLOWED_USER_IDS` | Yes | Backend |
| `MOTION_API_KEY` | For Motion | Motion MCP |
| `GITHUB_TOKEN` | For GitHub | GitHub MCP |
| `GOOGLE_CALENDAR_CLIENT_ID` | For Calendar | Google Calendar MCP |
| `GOOGLE_CALENDAR_CLIENT_SECRET` | For Calendar | Google Calendar MCP |
| `GMAIL_CLIENT_ID` | For Gmail | Gmail MCP |
| `GMAIL_CLIENT_SECRET` | For Gmail | Gmail MCP |
| `GOOGLE_DRIVE_CLIENT_ID` | For Drive | Google Drive MCP |
| `GOOGLE_DRIVE_CLIENT_SECRET` | For Drive | Google Drive MCP |

## Quick Full Stack Status Check

```bash
echo "=== Full Stack Status ==="
echo ""
echo "Database (Network):"
pg_isready -h 192.168.50.35 -p 5432 -U postgres 2>/dev/null && echo "  PostgreSQL (192.168.50.35): HEALTHY" || echo "  PostgreSQL (192.168.50.35): NOT REACHABLE"
echo ""
echo "MCP Servers (Local):"
for port in 8081 8083 8084 8085 8087; do
  name=$(case $port in 8081) echo "Motion";; 8083) echo "GitHub";; 8084) echo "Google Calendar";; 8085) echo "Gmail";; 8087) echo "Google Drive";; esac)
  status=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 2 http://localhost:$port/health 2>/dev/null)
  [ "$status" = "200" ] && echo "  $name ($port): HEALTHY" || echo "  $name ($port): NOT RUNNING"
done
echo ""
echo "Core Services (Local):"
status=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 2 http://localhost:8000/health 2>/dev/null)
[ "$status" = "200" ] && echo "  Backend (8000): HEALTHY" || echo "  Backend (8000): NOT RUNNING"
status=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 2 http://localhost:3000/ 2>/dev/null)
[ "$status" = "200" ] && echo "  Frontend (3000): HEALTHY" || echo "  Frontend (3000): NOT RUNNING"
```

## Troubleshooting

### Port Already In Use

```bash
# Find what's using a port (e.g., 8081)
lsof -i :8081  # macOS/Linux
netstat -ano | findstr :8081  # Windows
```

### MCP Server Won't Start

```bash
# Check if dependencies are installed
cd MCPS/motion  # or other MCP directory
uv sync

# Check for missing env vars
cat ../../.env | grep MOTION  # or relevant service
```

### Backend Can't Connect to MCP

Ensure MCP servers are running BEFORE starting Backend. The Backend expects:
- Motion MCP at `localhost:8081`
- GitHub MCP at `localhost:8083`
- Google Calendar MCP at `localhost:8084`
- Gmail MCP at `localhost:8085`
- Google Drive MCP at `localhost:8087`

For local development, update `.env`:
```bash
# Change from Docker hostnames to localhost
MOTION_MCP_HOST=localhost
GITHUB_MCP_HOST=localhost
GOOGLE_CALENDAR_MCP_HOST=localhost
GMAIL_MCP_HOST=localhost
GOOGLE_DRIVE_MCP_HOST=localhost
```

### Google OAuth Not Working

If Google Calendar, Gmail, or Google Drive MCPs fail OAuth:
1. Start the MCP server locally
2. Visit the auth URL for the relevant service:
   - Calendar: `http://localhost:8084/auth/url`
   - Gmail: `http://localhost:8085/auth/url`
   - Google Drive: `http://localhost:8087/auth/url`
3. Complete OAuth in browser
4. Tokens are saved to `data/token.json` in each MCP directory
