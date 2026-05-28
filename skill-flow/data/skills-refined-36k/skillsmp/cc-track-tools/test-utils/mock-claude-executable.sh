#!/bin/bash

# Mock Claude executable for testing
# This mimics the Claude Code CLI behavior for testing

# Check for version request (SDK often checks this first)
if [[ "$1" == "--version" ]]; then
  echo "1.0.0-mock"
  exit 0
fi

# Read all input (might be multiline)
input=$(cat)

# Check if input contains "Research the codebase" (from capture-plan enrichment)
if echo "$input" | grep -q "Research the codebase"; then
  # Return a mock task file content
  cat <<'EOF'
# Task: Test Task

## Requirements
- [ ] Implement feature
- [ ] Add tests
- [ ] Update documentation

## Success Criteria
- All tests pass
- Feature works as expected

## Recent Progress
- Task created via integration test
EOF
  exit 0
fi

# Check if input contains "review" (from stop-review)
if echo "$input" | grep -q "review"; then
  # Return a mock review response
  cat <<'EOF'
{
  "decision": "continue",
  "reason": "Changes align with task requirements"
}
EOF
  exit 0
fi

# Check if input contains "Update the task file" (from pre-compact)
if echo "$input" | grep -q "Update the task file"; then
  # Return the same content with a compaction note
  echo "$input" | sed 's/## Recent Progress/## Recent Progress\n- [Compaction occurred]/'
  exit 0
fi

# Default response for unknown requests
echo "Mock response for testing"
exit 0