#!/bin/bash
set -euo pipefail

# apply-items.sh - Execute GitHub mutations for items
#
# Usage: apply-items.sh < items.json
#        cat items.json | apply-items.sh
#
# Reads items with responses, executes GitHub API mutations
# Only processes items where response.enabled == true

# Read JSON from stdin
ITEMS=$(cat)

# Process each enabled item
echo "$ITEMS" | jq -c '.[] | select(.response.enabled == true)' | while read -r item; do
  ID=$(echo "$item" | jq -r '.id')
  TYPE=$(echo "$item" | jq -r '.type')
  ACTION=$(echo "$item" | jq -r '.response.action')
  RESOLVE=$(echo "$item" | jq -r '.response.resolve')
  EMOJI=$(echo "$item" | jq -r '.response.emoji // empty')
  REPLY=$(echo "$item" | jq -r '.response.reply // empty')

  echo "Processing item $ID ($ACTION)..."

  # Skip if action is defer or discuss (no GitHub changes)
  if [[ "$ACTION" == "defer" ]] || [[ "$ACTION" == "discuss" ]]; then
    echo "  Skipped (action: $ACTION)"
    continue
  fi

  # Get node IDs
  PR_NODE_ID=$(echo "$item" | jq -r '._prNodeId // empty')
  THREAD_ID=$(echo "$item" | jq -r '._threadId // empty')
  COMMENT_ID=$(echo "$item" | jq -r '._commentId // empty')

  # Build and execute mutation
  if [[ "$TYPE" == "threads" ]]; then
    # Review thread: react, optionally reply, resolve
    MUTATION="mutation {"

    # Add reaction
    if [[ -n "$EMOJI" ]] && [[ -n "$COMMENT_ID" ]]; then
      # Map emoji name to GitHub enum
      EMOJI_ENUM=$(echo "$EMOJI" | tr '[:lower:]' '[:upper:]' | sed 's/_//')
      MUTATION="$MUTATION
        addReaction(input: {subjectId: \"$COMMENT_ID\", content: $EMOJI_ENUM}) { reaction { content } }"
    fi

    # Add reply
    if [[ -n "$REPLY" ]] && [[ "$REPLY" != "null" ]] && [[ -n "$PR_NODE_ID" ]] && [[ -n "$COMMENT_ID" ]]; then
      # Escape reply for GraphQL
      REPLY_ESCAPED=$(echo "$REPLY" | jq -Rs '.')
      MUTATION="$MUTATION
        addPullRequestReviewComment(input: {pullRequestId: \"$PR_NODE_ID\", inReplyTo: \"$COMMENT_ID\", body: $REPLY_ESCAPED}) { comment { id } }"
    fi

    # Resolve thread
    if [[ "$RESOLVE" == "true" ]] && [[ -n "$THREAD_ID" ]]; then
      MUTATION="$MUTATION
        resolveReviewThread(input: {threadId: \"$THREAD_ID\"}) { thread { isResolved } }"
    fi

    MUTATION="$MUTATION
    }"

    # Execute
    if gh api graphql -f query="$MUTATION" --silent 2>/dev/null; then
      echo "  Done"
    else
      echo "  Error executing mutation" >&2
    fi

  elif [[ "$TYPE" == "comment-part" ]]; then
    # PR comment: react, minimize when all parts done
    if [[ -n "$EMOJI" ]] && [[ -n "$COMMENT_ID" ]]; then
      EMOJI_ENUM=$(echo "$EMOJI" | tr '[:lower:]' '[:upper:]' | sed 's/_//')
      gh api graphql -f query="
        mutation {
          addReaction(input: {subjectId: \"$COMMENT_ID\", content: $EMOJI_ENUM}) { reaction { content } }
        }
      " --silent 2>/dev/null && echo "  Reacted" || echo "  Error adding reaction" >&2
    fi

    # Note: minimizeComment should only happen when ALL parts are resolved
    # This script handles individual items; summary/batch logic should track this
    echo "  Note: Minimize comment manually when all parts resolved"
  fi
done

echo "Apply complete."
