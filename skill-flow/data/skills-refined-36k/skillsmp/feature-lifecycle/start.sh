#!/bin/bash
# feature-lifecycle/start.sh
# Starts a new feature by creating branch, docs, and story skeleton.

set -e

if [ -z "$1" ]; then
  echo "Usage: start-feature <issue-id>"
  echo "Example: start-feature bd-123"
  exit 1
fi

ISSUE_ID=$1
BRANCH_NAME="feature-${ISSUE_ID}"
DOC_FILE="docs/${ISSUE_ID}.md"
STORY_DIR="docs/testing/stories"
STORY_FILE="${STORY_DIR}/story-${ISSUE_ID}.yml"

# 1. Create Branch
if git show-ref --verify --quiet "refs/heads/${BRANCH_NAME}"; then
  echo "⚠️  Branch ${BRANCH_NAME} already exists. Switching..."
  git checkout "${BRANCH_NAME}"
else
  echo "🌿 Creating branch ${BRANCH_NAME}..."
  git checkout -b "${BRANCH_NAME}"
fi

# 2. Create Doc Context
if [ ! -f "${DOC_FILE}" ]; then
  echo "📄 Creating context doc: ${DOC_FILE}..."
  mkdir -p docs
  cat > "${DOC_FILE}" <<EOF
# Context: ${ISSUE_ID}

## Objective
[Link to Beads Issue]

## Implementation Plan
- [ ] Step 1
- [ ] Step 2
EOF
  git add "${DOC_FILE}"
else
  echo "✅ Context doc exists: ${DOC_FILE}"
fi

# 3. Create Story Skeleton (The Guardrail)
if [ ! -f "${STORY_FILE}" ]; then
  echo "🧪 Creating story skeleton: ${STORY_FILE}..."
  mkdir -p "${STORY_DIR}"
  cat > "${STORY_FILE}" <<EOF
name: ${ISSUE_ID} Verification
description: Automated verification for feature ${ISSUE_ID}

steps:
  - name: Login
    path: /login
    action: check_element
    selector: "input[name='email']"

  # TODO: Add specific feature verification steps here
  # - name: Check New Feature
  #   path: /dashboard
  #   ...
EOF
  git add "${STORY_FILE}"
  echo "📝 Created story file. PLEASE EDIT THIS FILE to define 'Done'."
else
  echo "✅ Story file exists: ${STORY_FILE}"
fi

echo ""
echo "🚀 Feature ${ISSUE_ID} started!"
echo "   Branch: ${BRANCH_NAME}"
echo "   Doc: ${DOC_FILE}"
echo "   Story: ${STORY_FILE}"
echo ""
echo "NEXT STEPS:"
echo "1. Edit ${STORY_FILE} to define success."
echo "2. Edit ${DOC_FILE} to refine plan."
echo "3. Run 'sync-feature \"initial setup\"' to save."
