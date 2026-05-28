#!/bin/bash
# Add issues to GitHub Projects v2 board
# Usage: ./add_to_project.sh PROJECT_NUMBER OWNER REPO START_ISSUE END_ISSUE

set -e

if [ "$#" -ne 5 ]; then
    echo "Usage: $0 PROJECT_NUMBER OWNER REPO START_ISSUE END_ISSUE"
    echo "Example: $0 4 myuser myrepo 64 151"
    exit 1
fi

PROJECT_NUM=$1
OWNER=$2
REPO=$3
START=$4
END=$5

echo "📋 Adding issues #$START-#$END to project $PROJECT_NUM..."
echo

total=0
success=0
failed=0

for issue_number in $(seq $START $END); do
  total=$((total + 1))

  # Add issue to project
  result=$(gh project item-add $PROJECT_NUM --owner "$OWNER" \
    --url "https://github.com/$OWNER/$REPO/issues/$issue_number" 2>&1)

  if [ $? -eq 0 ]; then
    success=$((success + 1))
    echo "✅ Added issue #$issue_number"
  else
    failed=$((failed + 1))
    echo "❌ Failed to add issue #$issue_number: $result"
  fi

  # Rate limiting
  sleep 0.3
done

echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Summary:"
echo "   Total: $total"
echo "   Success: $success"
echo "   Failed: $failed"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
