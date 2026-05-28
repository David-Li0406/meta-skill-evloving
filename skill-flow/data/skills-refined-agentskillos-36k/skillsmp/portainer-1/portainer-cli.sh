#!/bin/bash
# Portainer CLI Helper Script
# Usage: ./portainer-cli.sh <command> [options]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check for required tools
check_dependencies() {
  for cmd in curl jq; do
    if ! command -v $cmd &> /dev/null; then
      echo -e "${RED}Error: $cmd is required but not installed.${NC}"
      exit 1
    fi
  done
}

# Load config from environment or prompt
load_config() {
  if [ -z "$PORTAINER_URL" ]; then
    echo -e "${YELLOW}PORTAINER_URL not set.${NC}"
    read -p "Enter Portainer URL: " PORTAINER_URL
  fi

  if [ -z "$PORTAINER_TOKEN" ]; then
    echo -e "${YELLOW}PORTAINER_TOKEN not set.${NC}"
    read -s -p "Enter Portainer API Token: " PORTAINER_TOKEN
    echo
  fi
}

# Get endpoint ID (assumes first endpoint)
get_endpoint_id() {
  curl -s -X GET "$PORTAINER_URL/api/endpoints" \
    -H "X-API-Key: $PORTAINER_TOKEN" | jq '.[0].Id'
}

# List all stacks
cmd_list() {
  echo -e "${GREEN}Fetching stacks...${NC}"

  local stacks=$(curl -s -X GET "$PORTAINER_URL/api/stacks" \
    -H "X-API-Key: $PORTAINER_TOKEN")

  echo ""
  echo "| ID | Name | Status | Type | Created |"
  echo "|----|------|--------|------|---------|"

  echo "$stacks" | jq -r '.[] | "| \(.Id) | \(.Name) | \(if .Status == 1 then "Active" else "Inactive" end) | \(if .Type == 2 then "Compose" else "Swarm" end) | \(.CreationDate | strftime("%Y-%m-%d %H:%M")) |"'
}

# Get stack status
cmd_status() {
  local stack_name="$1"

  if [ -z "$stack_name" ]; then
    echo -e "${RED}Error: Stack name required${NC}"
    echo "Usage: $0 status <stack-name>"
    exit 1
  fi

  echo -e "${GREEN}Checking status for: $stack_name${NC}"

  local stack=$(curl -s -X GET "$PORTAINER_URL/api/stacks" \
    -H "X-API-Key: $PORTAINER_TOKEN" | jq ".[] | select(.Name==\"$stack_name\")")

  if [ -z "$stack" ] || [ "$stack" == "null" ]; then
    echo -e "${RED}Stack '$stack_name' not found${NC}"
    exit 1
  fi

  echo ""
  echo "Stack Details:"
  echo "$stack" | jq '{
    Id,
    Name,
    Status: (if .Status == 1 then "Active" else "Inactive" end),
    Type: (if .Type == 2 then "Compose" else "Swarm" end),
    EntryPoint,
    CreationDate: (.CreationDate | strftime("%Y-%m-%d %H:%M:%S")),
    GitRepo: .GitConfig.URL,
    GitBranch: .GitConfig.ReferenceName,
    AutoUpdate: .AutoUpdate.Interval
  }'

  # Get containers for this stack
  local endpoint_id=$(get_endpoint_id)
  local stack_id=$(echo "$stack" | jq -r '.Id')

  echo ""
  echo "Containers:"
  curl -s "$PORTAINER_URL/api/endpoints/$endpoint_id/docker/containers/json?all=true" \
    -H "X-API-Key: $PORTAINER_TOKEN" | \
    jq -r ".[] | select(.Labels[\"com.docker.compose.project\"]==\"$stack_name\") | \"  - \(.Names[0]): \(.State) (\(.Status))\""
}

# Redeploy stack
cmd_redeploy() {
  local stack_name="$1"
  local pull_images="${2:-true}"

  if [ -z "$stack_name" ]; then
    echo -e "${RED}Error: Stack name required${NC}"
    echo "Usage: $0 redeploy <stack-name> [pull-images: true/false]"
    exit 1
  fi

  echo -e "${GREEN}Redeploying: $stack_name${NC}"

  local stack_id=$(curl -s -X GET "$PORTAINER_URL/api/stacks" \
    -H "X-API-Key: $PORTAINER_TOKEN" | jq -r ".[] | select(.Name==\"$stack_name\") | .Id")

  if [ -z "$stack_id" ] || [ "$stack_id" == "null" ]; then
    echo -e "${RED}Stack '$stack_name' not found${NC}"
    exit 1
  fi

  local endpoint_id=$(get_endpoint_id)

  local response=$(curl -s -X PUT "$PORTAINER_URL/api/stacks/$stack_id/git/redeploy?endpointId=$endpoint_id" \
    -H "X-API-Key: $PORTAINER_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"pullImage\": $pull_images, \"prune\": false}")

  if echo "$response" | jq -e '.message' > /dev/null 2>&1; then
    echo -e "${RED}Error: $(echo "$response" | jq -r '.message')${NC}"
    exit 1
  else
    echo -e "${GREEN}Redeploy initiated successfully!${NC}"
    echo "$response" | jq '{Id, Name, Status: (if .Status == 1 then "Active" else "Inactive" end)}'
  fi
}

# Delete stack
cmd_delete() {
  local stack_name="$1"

  if [ -z "$stack_name" ]; then
    echo -e "${RED}Error: Stack name required${NC}"
    echo "Usage: $0 delete <stack-name>"
    exit 1
  fi

  local stack_id=$(curl -s -X GET "$PORTAINER_URL/api/stacks" \
    -H "X-API-Key: $PORTAINER_TOKEN" | jq -r ".[] | select(.Name==\"$stack_name\") | .Id")

  if [ -z "$stack_id" ] || [ "$stack_id" == "null" ]; then
    echo -e "${RED}Stack '$stack_name' not found${NC}"
    exit 1
  fi

  echo -e "${YELLOW}Warning: This will delete stack '$stack_name' (ID: $stack_id)${NC}"
  read -p "Are you sure? (y/N): " confirm

  if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "Cancelled."
    exit 0
  fi

  local endpoint_id=$(get_endpoint_id)

  curl -s -X DELETE "$PORTAINER_URL/api/stacks/$stack_id?endpointId=$endpoint_id" \
    -H "X-API-Key: $PORTAINER_TOKEN"

  echo -e "${GREEN}Stack '$stack_name' deleted.${NC}"
}

# Get container logs
cmd_logs() {
  local stack_name="$1"
  local container_filter="$2"
  local tail="${3:-100}"

  if [ -z "$stack_name" ]; then
    echo -e "${RED}Error: Stack name required${NC}"
    echo "Usage: $0 logs <stack-name> [container-filter] [tail-lines]"
    exit 1
  fi

  local endpoint_id=$(get_endpoint_id)

  # Get containers for this stack
  local containers=$(curl -s "$PORTAINER_URL/api/endpoints/$endpoint_id/docker/containers/json?all=true" \
    -H "X-API-Key: $PORTAINER_TOKEN" | \
    jq -r ".[] | select(.Labels[\"com.docker.compose.project\"]==\"$stack_name\")")

  if [ -z "$containers" ]; then
    echo -e "${RED}No containers found for stack '$stack_name'${NC}"
    exit 1
  fi

  # If filter provided, match container name
  if [ -n "$container_filter" ]; then
    local container_id=$(echo "$containers" | jq -r "select(.Names[0] | contains(\"$container_filter\")) | .Id" | head -1)
  else
    # Show available containers and let user choose
    echo "Available containers:"
    echo "$containers" | jq -r '"  - " + .Names[0]'
    echo ""
    read -p "Enter container name filter: " container_filter
    local container_id=$(echo "$containers" | jq -r "select(.Names[0] | contains(\"$container_filter\")) | .Id" | head -1)
  fi

  if [ -z "$container_id" ]; then
    echo -e "${RED}Container not found${NC}"
    exit 1
  fi

  echo -e "${GREEN}Fetching logs (last $tail lines)...${NC}"
  echo ""

  curl -s "$PORTAINER_URL/api/endpoints/$endpoint_id/docker/containers/$container_id/logs?stdout=true&stderr=true&tail=$tail" \
    -H "X-API-Key: $PORTAINER_TOKEN" | sed 's/^.\{8\}//'
}

# Show help
cmd_help() {
  echo "Portainer CLI Helper"
  echo ""
  echo "Usage: $0 <command> [options]"
  echo ""
  echo "Commands:"
  echo "  list                          List all stacks"
  echo "  status <stack-name>           Get detailed stack status"
  echo "  redeploy <stack-name> [pull]  Redeploy a stack (pull images: true/false)"
  echo "  delete <stack-name>           Delete a stack"
  echo "  logs <stack> [container] [n]  View container logs (n = tail lines)"
  echo "  help                          Show this help"
  echo ""
  echo "Environment Variables:"
  echo "  PORTAINER_URL    Portainer instance URL"
  echo "  PORTAINER_TOKEN  Portainer API token"
  echo ""
  echo "Examples:"
  echo "  $0 list"
  echo "  $0 status my-app"
  echo "  $0 redeploy my-app true"
  echo "  $0 logs my-app backend 200"
}

# Main
check_dependencies
load_config

case "${1:-help}" in
  list)
    cmd_list
    ;;
  status)
    cmd_status "$2"
    ;;
  redeploy)
    cmd_redeploy "$2" "$3"
    ;;
  delete)
    cmd_delete "$2"
    ;;
  logs)
    cmd_logs "$2" "$3" "$4"
    ;;
  help|--help|-h)
    cmd_help
    ;;
  *)
    echo -e "${RED}Unknown command: $1${NC}"
    cmd_help
    exit 1
    ;;
esac
