#!/bin/bash
# validate_railway_env.sh - Railway environment validation via GraphQL
# Part of the agent-skills registry
# Compatible with: Claude Code, Codex CLI, OpenCode, Gemini CLI, Antigravity

set -e

# Source shared utilities
SKILLS_ROOT="${CLAUDE_PLUGIN_ROOT:-$HOME/.agent/skills}"
if [[ -f "$SKILLS_ROOT/lib/railway-common.sh" ]]; then
  source "$SKILLS_ROOT/lib/railway-common.sh"
else
  RED='\033[0;31m'
  GREEN='\033[0;32m'
  YELLOW='\033[1;33m'
  NC='\033[0m'
  log_info() { echo -e "${GREEN}✓${NC} $*"; }
  log_warn() { echo -e "${YELLOW}⚠${NC} $*"; }
  log_error() { echo -e "${RED}✗${NC} $*"; }
fi

# Default values
PROJECT_ID=""
SERVICE_NAME=""

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --project-id)
      PROJECT_ID="$2"
      shift 2
      ;;
    --service)
      SERVICE_NAME="$2"
      shift 2
      ;;
    -h|--help)
      echo "Usage: $0 [--project-id ID] [--service NAME]"
      echo ""
      echo "Validate Railway environment configuration via GraphQL API."
      echo ""
      echo "Options:"
      echo "  --project-id ID   Railway project ID (uses linked project if not specified)"
      echo "  --service NAME   Specific service to validate"
      echo "  -h, --help       Show this help message"
      echo ""
      echo "Examples:"
      echo "  $0                              # Validate linked project"
      echo "  $0 --project-id xxx           # Validate specific project"
      echo "  $0 --service backend          # Validate specific service"
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      echo "Use -h for help"
      exit 1
      ;;
  esac
done

echo "🔍 Railway Environment Validation"
echo ""

# Get project ID if not specified
if [[ -z "$PROJECT_ID" ]]; then
  if command -v railway &>/dev/null; then
    PROJECT_ID=$(railway status --json 2>/dev/null | jq -r '.project.id // empty' || echo "")

    if [[ -z "$PROJECT_ID" ]]; then
      log_error "No Railway project linked"
      echo "   Run: railway link"
      echo "   Or specify: $0 --project-id <ID>"
      exit 1
    fi
  else
    log_error "Railway CLI not found"
    echo "   Install: npm install -g @railway/cli"
    exit 1
  fi
fi

# Get environment ID
ENV_ID=$(railway status --json 2>/dev/null | jq -r '.environment.id // empty' || echo "")

if [[ -z "$ENV_ID" ]]; then
  log_error "No linked environment found"
  echo "   Run: railway link"
  exit 1
fi

log_info "Validating project: $PROJECT_ID"
log_info "Environment: $ENV_ID"

# Check if railway-api.sh exists
if [[ ! -f "$SKILLS_ROOT/lib/railway-api.sh" ]]; then
  log_error "Railway API script not found"
  echo "   Expected: $SKILLS_ROOT/lib/railway-api.sh"
  echo "   Install from: https://github.com/railwayapp/railway-skills"
  exit 1
fi

# Function to execute GraphQL query
graphql_query() {
  local query="$1"
  local variables="$2"

  bash <<'SCRIPT'
    SKILLS_ROOT="${CLAUDE_PLUGIN_ROOT:-$HOME/.agent/skills}"
    ${SKILLS_ROOT}/lib/railway-api.sh \
      '__QUERY__' \
      '__VARIABLES__'
SCRIPT
}

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Environment Configuration"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Query environment config
echo ""
echo "📋 Fetching environment configuration..."

ENV_CONFIG=$(bash <<SCRIPT
SKILLS_ROOT="${CLAUDE_PLUGIN_ROOT:-$HOME/.agent/skills}"
\${SKILLS_ROOT}/lib/railway-api.sh \
  'query envConfig(\$envId: String!) {
    environment(id: \$envId) {
      id
      name
      config(decryptVariables: false)
    }
  }' \
  "{\"envId\": \"$ENV_ID\"}"
SCRIPT
)

# Check for errors
if echo "$ENV_CONFIG" | jq -e '.errors' &>/dev/null; then
  log_error "Failed to fetch environment config"
  echo "$ENV_CONFIG" | jq -r '.errors[] | .message'
  exit 1
fi

# Parse services
SERVICE_COUNT=$(echo "$ENV_CONFIG" | jq -r '.environment.config.services // {} | length' 2>/dev/null || echo "0")

if [[ "$SERVICE_COUNT" -eq 0 ]]; then
  log_warn "No services found in environment"
else
  log_info "Found $SERVICE_COUNT service(s)"

  echo ""
  echo "Services:"
  echo "$ENV_CONFIG" | jq -r '.environment.config.services | to_entries[] | "
    \"\(.key)\"
    ┌─ Source: \(.value.source.repo // .value.source.image // \"Dockerfile\")
    ├─ Builder: \(.value.build.builder // \"NIXPACKS\")
    ├─ Build: \(.value.build.buildCommand // \"auto\")
    ├─ Start: \(.value.deploy.startCommand // \"auto\")
    └─ Variables: \(.value.variables | length) defined
  "'
fi

# Check for staged changes
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Staged Changes"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

STAGED_CHANGES=$(bash <<SCRIPT
SKILLS_ROOT="${CLAUDE_PLUGIN_ROOT:-$HOME/.agent/skills}"
\${SKILLS_ROOT}/lib/railway-api.sh \
  'query stagedChanges(\$envId: String!) {
    environmentStagedChanges(environmentId: \$envId) {
      id
      patch(decryptVariables: false)
    }
  }' \
  "{\"envId\": \"$ENV_ID\"}"
SCRIPT
)

# Check if there are staged changes
if echo "$STAGED_CHANGES" | jq -e '.environmentStagedChanges.patch' &>/dev/null; then
  HAS_SERVICES=$(echo "$STAGED_CHANGES" | jq -r '.environmentStagedChanges.patch.services // {} | length' 2>/dev/null || echo "0")

  if [[ "$HAS_SERVICES" -gt 0 ]]; then
    log_warn "Found staged changes not yet deployed:"
    echo ""
    echo "$STAGED_CHANGES" | jq -r '.environmentStagedChanges.patch.services | to_entries[] | "
      \"\(.key)\"
      ┌─ Changes detected
      └─ Run: railway apply  OR  railway environment stage commit
    "'
  else
    log_info "No staged changes"
  fi
else
  log_info "No staged changes"
fi

# Check for required variables
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Variable Validation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Get variables via CLI (more reliable for rendered values)
if command -v railway &>/dev/null; then
  VARS_JSON=$(railway variables --json 2>/dev/null || echo "{}")

  # Check for common required variables
  REQUIRED_VARS=(
    "DATABASE_URL"
    "SUPABASE_URL"
    "CLERK_SECRET_KEY"
    "API_URL"
    "REDIS_URL"
  )

  MISSING_VARS=()

  echo ""
  echo "Checking required variables..."
  for VAR in "${REQUIRED_VARS[@]}"; do
    if echo "$VARS_JSON" | jq -e --arg VAR "$VAR" '.[$VAR]' &>/dev/null; then
      log_info "$VAR is set"
    else
      MISSING_VARS+=("$VAR")
    fi
  done

  if [[ ${#MISSING_VARS[@]} -gt 0 ]]; then
    echo ""
    log_warn "Missing potentially required variables:"
    for VAR in "${MISSING_VARS[@]}"; do
      echo "   - $VAR"
    done
  fi
fi

# Service-specific validation
if [[ -n "$SERVICE_NAME" ]]; then
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "Service: $SERVICE_NAME"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  # Get service details
  SERVICE_CONFIG=$(echo "$ENV_CONFIG" | jq -r ".environment.config.services[\"$SERVICE_NAME\"] // empty" 2>/dev/null || echo "")

  if [[ -z "$SERVICE_CONFIG" ]] || [[ "$SERVICE_CONFIG" == "null" ]]; then
    log_error "Service '$SERVICE_NAME' not found"
    echo ""
    echo "Available services:"
    echo "$ENV_CONFIG" | jq -r '.environment.config.services | keys[]'
    exit 1
  fi

  # Display service details
  echo ""
  echo "Configuration:"
  echo "$SERVICE_CONFIG" | jq -r '
    "Source: " + (.source.repo // .source.image // "Dockerfile")
  '

  BUILD_CMD=$(echo "$SERVICE_CONFIG" | jq -r '.build.buildCommand // "auto"')
  START_CMD=$(echo "$SERVICE_CONFIG" | jq -r '.deploy.startCommand // "auto"')

  echo "Build: $BUILD_CMD"
  echo "Start: $START_CMD"

  # Check for build/start conflict
  if [[ "$BUILD_CMD" != "auto" ]] && [[ "$BUILD_CMD" == "$START_CMD" ]]; then
    log_error "buildCommand and startCommand are identical"
    echo "   Railway requires different commands"
  fi

  # Show variables
  VAR_COUNT=$(echo "$SERVICE_CONFIG" | jq -r '.variables | length' 2>/dev/null || echo "0")
  echo ""
  echo "Variables: $VAR_COUNT defined"

  if [[ "$VAR_COUNT" -gt 0 ]]; then
    echo "$SERVICE_CONFIG" | jq -r '.variables | keys[]' | sed 's/^/  - /'
  fi
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Validation complete"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
