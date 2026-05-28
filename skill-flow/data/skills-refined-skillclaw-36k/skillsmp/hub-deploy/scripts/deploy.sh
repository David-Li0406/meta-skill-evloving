#!/usr/bin/env bash
# MCP Hub Deploy Script
# Adapt this script to your server setup
#
# Usage: ./deploy.sh [service]
#   ./deploy.sh         # Deploy all services
#   ./deploy.sh hub     # Deploy hub only
#
set -euo pipefail

# ============================================================
# CONFIGURATION - ADAPT THESE TO YOUR SETUP
# ============================================================

# Server paths
ROOT="/opt/mcp-hub"                    # Where the repo lives on server
REPO_DIR="${ROOT}/mcp-hub"             # Repo directory name
COMPOSE_FILE="${REPO_DIR}/deploy/docker-compose.yml"

# Git remote (SSH recommended for deploy keys)
GIT_REMOTE="git@github.com:YOUR-ORG/YOUR-REPO.git"
SSH_KEY="${HOME}/.ssh/id_ed25519"      # Deploy key path

# Services to deploy (space-separated)
ALL_SERVICES="hub"                      # Add more: "hub notion agent-worker"

# Health check base URL
HEALTH_BASE_URL="https://your-domain.com"

# ============================================================
# SCRIPT LOGIC - Usually no changes needed below
# ============================================================

SERVICE="${1:-all}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${BLUE}$1${NC}"; }
success() { echo -e "${GREEN}✅ $1${NC}"; }
warn() { echo -e "${YELLOW}⚠️ $1${NC}"; }
error() { echo -e "${RED}❌ $1${NC}"; }

# Validate configuration
if [[ "$GIT_REMOTE" == *"YOUR-ORG"* ]]; then
  error "Please configure GIT_REMOTE in this script"
  exit 1
fi

if [[ "$HEALTH_BASE_URL" == *"your-domain"* ]]; then
  warn "HEALTH_BASE_URL not configured - health checks will be skipped"
fi

cd "${REPO_DIR}" || { error "Repo directory not found: ${REPO_DIR}"; exit 1; }

# Ensure git safe-directory for root
git config --global --add safe.directory "${REPO_DIR}" 2>/dev/null || true

# Ensure remote uses correct URL
CURRENT_REMOTE=$(git remote get-url origin 2>/dev/null || echo "")
if [[ "$CURRENT_REMOTE" != "$GIT_REMOTE" ]]; then
  log "Updating git remote..."
  git remote set-url origin "$GIT_REMOTE"
fi

# Pull latest
log "🔄 Pulling latest changes..."
git stash --include-untracked 2>/dev/null || true
if [[ -f "$SSH_KEY" ]]; then
  GIT_SSH_COMMAND="ssh -i ${SSH_KEY} -o IdentitiesOnly=yes" git pull --rebase
else
  git pull --rebase
fi
git stash drop 2>/dev/null || true

# Determine services to deploy
if [[ "$SERVICE" == "all" ]]; then
  SERVICES="$ALL_SERVICES"
else
  SERVICES="$SERVICE"
fi

# Build
log "🏗️ Building: ${SERVICES}..."
# shellcheck disable=SC2086
docker compose -f "${COMPOSE_FILE}" --project-directory "${REPO_DIR}" build $SERVICES

# Restart
log "🚀 Restarting: ${SERVICES}..."
for svc in $SERVICES; do
  docker rm -f "$svc" 2>/dev/null || true
done
# shellcheck disable=SC2086
docker compose -f "${COMPOSE_FILE}" --project-directory "${REPO_DIR}" up -d --no-deps $SERVICES

# Health checks
if [[ "$HEALTH_BASE_URL" != *"your-domain"* ]]; then
  log "🔍 Running health checks..."
  sleep 3

  # Get auth token if available
  AUTH_HEADER=()
  if [[ -f "${REPO_DIR}/.env" ]]; then
    SERVICE_TOKEN=$(grep '^MCP_SERVICE_TOKEN=' "${REPO_DIR}/.env" 2>/dev/null | tail -n1 | cut -d'=' -f2- || true)
    if [[ -n "$SERVICE_TOKEN" ]]; then
      AUTH_HEADER=(-H "Authorization: Bearer ${SERVICE_TOKEN}")
    fi
  fi

  # Check hub health
  if curl -fsS "${AUTH_HEADER[@]}" "${HEALTH_BASE_URL}/health" >/dev/null 2>&1; then
    success "Hub health: OK"
  else
    warn "Hub health: Not responding (may need auth)"
  fi
fi

success "Deploy complete!"
echo ""
log "Services deployed: ${SERVICES}"
log "Check logs: docker compose -f ${COMPOSE_FILE} logs -f"
