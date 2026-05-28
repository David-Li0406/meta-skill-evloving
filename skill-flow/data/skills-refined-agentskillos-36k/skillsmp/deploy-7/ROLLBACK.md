# Rollback Procedures

How to rollback a failed deployment.

## Quick Rollback

If the latest deployment broke something:

```bash
# SSH to Orange Pi
ssh user@192.168.50.35

# List available image versions
docker images | grep claude-assistant | head -20

# Identify the previous working version (second entry for each image)
# Example: 192.168.50.35:5000/claude-assistant-backend:abc1234

# Stop the broken container
docker stop claude-assistant-backend

# Remove it
docker rm claude-assistant-backend

# Start with previous version
docker run -d \
  --name claude-assistant-backend \
  --network claude-assistant-network \
  --restart unless-stopped \
  -p 8000:8000 \
  -e APP_ENV=production \
  # ... (copy env vars from Jenkinsfile) ...
  192.168.50.35:5000/claude-assistant-backend:<previous-version>
```

## Rollback Specific Service

### Backend

```bash
# Stop and remove
docker stop claude-assistant-backend
docker rm claude-assistant-backend

# Start previous version (replace VERSION with actual tag)
docker run -d \
  --name claude-assistant-backend \
  --network claude-assistant-network \
  --restart unless-stopped \
  -p 8000:8000 \
  -e APP_ENV=production \
  -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  -e POSTGRES_HOST=192.168.50.35 \
  -e POSTGRES_PORT=5432 \
  -e POSTGRES_USER=$POSTGRES_USER \
  -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
  -e TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN \
  -e TELEGRAM_ALLOWED_USER_IDS=$TELEGRAM_ALLOWED_USER_IDS \
  -e TELEGRAM_MCP_HOST=claude-assistant-telegram-mcp \
  -e TELEGRAM_MCP_PORT=8080 \
  192.168.50.35:5000/claude-assistant-backend:VERSION
```

### MCP Server (Example: GitHub)

```bash
docker stop claude-assistant-github-mcp
docker rm claude-assistant-github-mcp

docker run -d \
  --name claude-assistant-github-mcp \
  --network claude-assistant-network \
  --restart unless-stopped \
  -p 8083:8083 \
  -e GITHUB_TOKEN=$GITHUB_TOKEN \
  -e GITHUB_MCP_HOST=0.0.0.0 \
  -e GITHUB_MCP_PORT=8083 \
  192.168.50.35:5000/claude-assistant-github-mcp:VERSION
```

## Full System Rollback

If you need to rollback everything:

```bash
# Stop all containers
docker stop $(docker ps -q --filter "name=claude-assistant")

# Remove all containers
docker rm $(docker ps -aq --filter "name=claude-assistant")

# Re-run Jenkins with previous commit
# Option 1: Trigger build from specific commit
git checkout <previous-commit>
git push -f origin main  # CAUTION: Force push

# Option 2: Revert commit and push
git revert HEAD
git push origin main
# Then trigger normal Jenkins build
```

## Find Previous Versions

```bash
# List all images with tags
docker images --format "{{.Repository}}:{{.Tag}}" | grep claude-assistant | sort

# Check image creation dates
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.CreatedAt}}" | grep claude-assistant

# Get git commit from image version
# If version is git hash (e.g., abc1234), check:
git log --oneline | grep abc1234
```

## Database Rollback

If a migration broke the database:

```bash
# Connect to PostgreSQL
psql -h 192.168.50.35 -U postgres -d claude_assistant_platform

# Check recent migrations
SELECT * FROM alembic_version;

# Rollback to specific revision (if using Alembic)
cd Backend
uv run alembic downgrade <revision>
```

## Prevention

To avoid needing rollbacks:

1. **Test locally** before pushing
2. **Use feature branches** and merge via PR
3. **Tag releases** for easy identification
4. **Keep previous images** (don't prune immediately)

## Emergency Contacts

If you can't resolve the issue:

1. Check Jenkins build logs for the failure point
2. Check container logs for runtime errors
3. Verify environment variables are set correctly
4. Check Docker network connectivity
