#!/bin/bash
# Sync local topics into a global feature branch
GLOBAL_BRANCH=$1

if [ -z "$GLOBAL_BRANCH" ]; then
  echo "Usage: ./git_sync.sh feature/your-feature-name"
  exit 1
fi

# 1. Update main first
git checkout main && git pull origin main

# 2. Create/Update the Global Feature Branch
git checkout -b "$GLOBAL_BRANCH" || git checkout "$GLOBAL_BRANCH"

# 3. Find and Merge Topic Branches
TOPICS=$(git branch --list 'topic/*' | sed 's/* //')
for TOPIC in $TOPICS; do
  echo "Merging $TOPIC into $GLOBAL_BRANCH..."
  git merge "$TOPIC" --no-edit
done

echo "✅ Ready to push $GLOBAL_BRANCH"
