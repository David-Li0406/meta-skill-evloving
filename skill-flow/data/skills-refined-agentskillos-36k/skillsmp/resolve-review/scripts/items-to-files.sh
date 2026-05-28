#!/bin/bash
set -euo pipefail

# items-to-files.sh - Convert Item JSON to markdown files
#
# Usage: items-to-files.sh <output-dir> < items.json
#        cat items.json | items-to-files.sh <output-dir>
#
# Creates one .md file per item in output-dir

OUTPUT_DIR="${1:?Usage: items-to-files.sh <output-dir>}"
mkdir -p "$OUTPUT_DIR"

# Read JSON from stdin
ITEMS=$(cat)

# Process each item
echo "$ITEMS" | jq -c '.[]' | while read -r item; do
  ID=$(echo "$item" | jq -r '.id')
  TYPE=$(echo "$item" | jq -r '.type')
  GIST=$(echo "$item" | jq -r '.feedback[0].gist')

  # Generate filename slug from gist
  SLUG=$(echo "$GIST" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//' | sed 's/-$//' | cut -c1-30)
  FILENAME=$(printf "%02d-%s.md" "$ID" "$SLUG")
  FILEPATH="$OUTPUT_DIR/$FILENAME"

  # Build frontmatter
  {
    echo "---"
    echo "item: $ID"
    echo "type: $TYPE"
    echo -n "urls: ["
    echo "$item" | jq -r '[.feedback[].url] | join(", ")' | tr -d '\n'
    echo "]"
    echo -n "authors: ["
    echo "$item" | jq -r '[.feedback[].author] | unique | join(", ")' | tr -d '\n'
    echo "]"
    echo "created: $(echo "$item" | jq -r '.feedback[0].created')"
    echo "outdated: $(echo "$item" | jq -r 'if ._outdated then "true" else "false" end')"

    # Add part info for comment-parts
    if [[ "$TYPE" == "comment-part" ]]; then
      PART_INDEX=$(echo "$item" | jq -r '.feedback[0].partIndex // 1')
      PART_TOTAL=$(echo "$item" | jq -r '.feedback[0].partTotal // 1')
      echo "part: $PART_INDEX"
      echo "partTotal: $PART_TOTAL"
    fi
    echo "---"
    echo

    # Feedback section
    echo "# Feedback"
    echo

    echo "$item" | jq -c '.feedback[]' | while read -r fb; do
      FB_GIST=$(echo "$fb" | jq -r '.gist')
      FB_AUTHOR=$(echo "$fb" | jq -r '.author')
      FB_URL=$(echo "$fb" | jq -r '.url')
      FB_BODY=$(echo "$fb" | jq -r '.body')
      FB_FILE=$(echo "$fb" | jq -r '.file // empty')
      FB_LINE=$(echo "$fb" | jq -r '.line // empty')
      FB_DIFF=$(echo "$fb" | jq -r '.diffHunk // empty')
      FB_PARENT=$(echo "$fb" | jq -r '.parentBody // empty')

      echo "## $FB_GIST"
      echo

      if [[ -n "$FB_FILE" ]]; then
        echo "@$FB_AUTHOR · $FB_FILE:$FB_LINE · [link]($FB_URL)"
      else
        echo "@$FB_AUTHOR · [link]($FB_URL)"
      fi
      echo

      # For comment-parts with parent
      if [[ -n "$FB_PARENT" ]] && [[ "$FB_PARENT" != "$FB_BODY" ]]; then
        echo "Full comment:"
        echo "$FB_PARENT" | sed 's/^/> /'
        echo
        echo "This part:"
      fi

      echo "$FB_BODY" | sed 's/^/> /'
      echo

      if [[ -n "$FB_DIFF" ]]; then
        echo '```diff'
        echo "$FB_DIFF"
        echo '```'
        echo
      fi

      # Replies
      echo "$fb" | jq -c '.replies // [] | .[]' 2>/dev/null | while read -r reply; do
        REPLY_AUTHOR=$(echo "$reply" | jq -r '.author')
        REPLY_BODY=$(echo "$reply" | jq -r '.body')
        echo "### @$REPLY_AUTHOR"
        echo
        echo "$REPLY_BODY" | sed 's/^/> /'
        echo
      done
    done

    # Analysis section (placeholder for CC to fill)
    echo "# Analysis"
    echo
    echo "_CC will analyze and suggest an action._"
    echo

    # Response section
    echo "# Response"
    echo
    echo '```yaml'
    echo "enabled: true"
    echo "action: null"
    echo "resolve: true"
    echo "emoji: thumbs_up"
    echo "reply: null"
    echo "commit: null"
    echo '```'
    echo
    echo "_Edit the yaml above to set your response._"

  } > "$FILEPATH"

  echo "Created: $FILENAME"
done
