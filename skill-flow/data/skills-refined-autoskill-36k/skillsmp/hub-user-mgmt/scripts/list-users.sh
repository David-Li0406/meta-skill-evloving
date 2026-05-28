#!/bin/bash
# List all MCP Hub users

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLIENTS_DIR="${SCRIPT_DIR}/../../../../clients"

echo "=== MCP Hub Users ==="
echo ""
printf "%-12s %-8s %-10s %-8s\n" "USER" "ROLE" "MODE" "STATUS"
printf "%-12s %-8s %-10s %-8s\n" "----" "----" "----" "------"

for dir in "$CLIENTS_DIR"/*/; do
  if [[ -d "$dir" ]]; then
    # Skip template
    dirname=$(basename "$dir")
    [[ "$dirname" == "_template" ]] && continue

    config="$dir/client.config.json"
    if [[ -f "$config" ]]; then
      username="$dirname"

      # Parse JSON with jq if available, otherwise basic grep
      if command -v jq &> /dev/null; then
        enabled=$(jq -r '.enabled // true' "$config")
        role=$(jq -r '.jwt.role // "user"' "$config")
        mode=$(jq -r '.tools.mode // "unknown"' "$config")
      else
        enabled=$(grep -o '"enabled"[^,}]*' "$config" | cut -d: -f2 | tr -d ' ')
        role=$(grep -o '"role"[^,}]*' "$config" | cut -d: -f2 | tr -d ' "')
        mode=$(grep -o '"mode"[^,}]*' "$config" | cut -d: -f2 | tr -d ' "')
      fi

      status="active"
      [[ "$enabled" == "false" ]] && status="disabled"

      printf "%-12s %-8s %-10s %-8s\n" "$username" "$role" "$mode" "$status"
    fi
  fi
done

echo ""
echo "Config location: $CLIENTS_DIR"
