# Local Development Environment Configuration

When running services locally (not in Docker), you need to update the MCP host settings in your `.env` file.

## Required Changes for Local Development

Add or update these variables in your `.env` file:

```bash
# =============================================================================
# LOCAL DEVELOPMENT OVERRIDES
# =============================================================================
# When running MCP servers locally (via make run), they run on localhost
# instead of Docker container hostnames.

# MCP Host Configuration for Local Development
# Change from Docker container names to localhost
MOTION_MCP_HOST=localhost
GITHUB_MCP_HOST=localhost
GOOGLE_CALENDAR_MCP_HOST=localhost
GMAIL_MCP_HOST=localhost

# Database (if using Docker for just the database)
POSTGRES_HOST=localhost
```

## Quick Setup Script

Run this to create/update local development overrides:

```bash
# Append local dev settings if not already present
grep -q "MOTION_MCP_HOST=localhost" .env || cat >> .env << 'EOF'

# =============================================================================
# LOCAL DEVELOPMENT OVERRIDES (added by /local-dev skill)
# =============================================================================
MOTION_MCP_HOST=localhost
GITHUB_MCP_HOST=localhost
GOOGLE_CALENDAR_MCP_HOST=localhost
GMAIL_MCP_HOST=localhost
POSTGRES_HOST=localhost
EOF

echo "Local development environment configured!"
```

## Service Port Summary

| Service | Local URL | Health Check |
|---------|-----------|--------------|
| Backend | http://localhost:8000 | http://localhost:8000/health |
| Frontend | http://localhost:3000 | http://localhost:3000/ |
| Motion MCP | http://localhost:8081 | http://localhost:8081/health |
| GitHub MCP | http://localhost:8083 | http://localhost:8083/health |
| Google Calendar MCP | http://localhost:8084 | http://localhost:8084/health |
| Gmail MCP | http://localhost:8085 | http://localhost:8085/health |
| PostgreSQL | localhost:5432 | `pg_isready -h localhost` |

## Switching Between Local and Docker

### For Docker Compose (Full Stack)
```bash
# Use Docker container names (default in .env.example)
MOTION_MCP_HOST=motion-mcp
GITHUB_MCP_HOST=github-mcp
GOOGLE_CALENDAR_MCP_HOST=google-calendar-mcp
GMAIL_MCP_HOST=gmail-mcp
POSTGRES_HOST=db
```

### For Local Development (make run)
```bash
# Use localhost
MOTION_MCP_HOST=localhost
GITHUB_MCP_HOST=localhost
GOOGLE_CALENDAR_MCP_HOST=localhost
GMAIL_MCP_HOST=localhost
POSTGRES_HOST=localhost
```
