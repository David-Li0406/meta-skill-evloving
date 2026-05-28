#!/bin/bash
# Token-efficient Context7 documentation fetcher
# Combines library search + context fetch + filtering in one command

set -euo pipefail

if [ $# -lt 2 ]; then
  echo "Usage: $0 <library-name> <query> [page]" >&2
  echo "Example: $0 react useState hook" >&2
  echo "Example: $0 react useState hook 2" >&2
  exit 1
fi

LIBRARY_NAME="$1"
QUERY="$2"
PAGE="${3:-1}"  # Default to page 1 if not provided

# URL encode the query for safe use in URLs
ENCODED_QUERY=$(python3 -c "import sys, urllib.parse; print(urllib.parse.quote(sys.argv[1]))" "$QUERY")

# Check if a library ID exists by trying to fetch context
check_library_id() {
  local lib_id="$1"
  local status=$(curl -s -o /dev/null -w "%{http_code}" "https://context7.com/api/v2/context?libraryId=$lib_id&query=test")
  [ "$status" = "200" ]
}

# Search for library ID by name
search_library_id() {
  local name="$1"
  curl -s "https://context7.com/api/v2/libs/search?libraryName=$name&query=$ENCODED_QUERY" | \
    python3 -c "import sys, json; data=json.load(sys.stdin); print(data['results'][0]['id'] if data.get('results') else '')" 2>/dev/null
}

# Extract code blocks from documentation text
extract_code_blocks() {
  local max="${1:-5}"
  awk -v max="$max" '
    BEGIN {
      count = 0
      in_block = 0
      block = ""
      lang = ""
    }

    /^```/ {
      if (in_block) {
        # End of code block
        if (count < max && length(block) > 20) {
          count++
          print "### Example " count
          if (lang != "") {
            print "```" lang
          } else {
            print "```"
          }
          print block
          print "```\n"
        }
        block = ""
        lang = ""
        in_block = 0
      } else {
        # Start of code block - extract language
        in_block = 1
        lang = substr($0, 4)  # Get language after ```
      }
      next
    }

    in_block {
      if (block != "") {
        block = block "\n" $0
      } else {
        block = $0
      }
    }

    END {
      if (count == 0) {
        print "# No code blocks found"
      }
    }
  '
}

# Extract API signatures
extract_signatures() {
  local max="${1:-3}"
  awk -v max="$max" '
    BEGIN { count = 0 }
    
    # Function declarations
    /^(export )?(async )?(function|const|let|var) [a-zA-Z_$][a-zA-Z0-9_$]*.*\(/ {
      if (count < max) {
        print "- `" $0 "`"
        count++
      }
    }
    
    # Interface definitions
    /^(export )?interface [a-zA-Z_$]/ {
      if (count < max) {
        sig = $0
        getline
        while ($0 ~ /^  / && count < max) {
          sig = sig " " $0
          getline
        }
        print "- `" sig "`"
        count++
      }
    }
    
    # Type definitions
    /^(export )?type [a-zA-Z_$][a-zA-Z0-9_$]* =/ {
      if (count < max) {
        print "- `" $0 "`"
        count++
      }
    }
  '
}

# Extract important notes and warnings
extract_notes() {
  local max="${1:-3}"
  grep -iE '(important|note:|warning:|caution:|tip:|remember:|must|should not|deprecated|breaking change)' | \
    head -n "$max" | \
    sed 's/^/- /' || echo "- No important notes found"
}

# Resolve library ID
LIBRARY_ID=""

# If input contains a slash, try using it directly as library ID
if [[ "$LIBRARY_NAME" == */* ]]; then
  CANDIDATE_ID="/$LIBRARY_NAME"
  if check_library_id "$CANDIDATE_ID"; then
    LIBRARY_ID="$CANDIDATE_ID"
  fi
fi

# Fall back to searching by name if not found
if [ -z "$LIBRARY_ID" ]; then
  LIBRARY_ID=$(search_library_id "$LIBRARY_NAME")
fi

if [ -z "$LIBRARY_ID" ]; then
  echo "Error: Library '$LIBRARY_NAME' not found" >&2
  exit 1
fi

# Fetch documentation context
RAW_TEXT=$(curl -s "https://context7.com/api/v2/context?libraryId=$LIBRARY_ID&query=$ENCODED_QUERY&page=$PAGE")

if [ -z "$RAW_TEXT" ]; then
  echo "Error: No documentation received" >&2
  exit 1
fi

# Filter using shell tools (0 LLM tokens!)
OUTPUT=""

# Extract code blocks (5 max)
CODE_BLOCKS=$(echo "$RAW_TEXT" | extract_code_blocks 5)
if [ -n "$CODE_BLOCKS" ] && [ "$CODE_BLOCKS" != "# No code blocks found" ]; then
  OUTPUT+="## Code Examples\n\n$CODE_BLOCKS\n"
fi

# Extract API signatures (3 max)
SIGNATURES=$(echo "$RAW_TEXT" | extract_signatures 3)
if [ -n "$SIGNATURES" ]; then
  OUTPUT+="\n## API Signatures\n\n$SIGNATURES\n"
fi

# Extract important notes (3 max)
NOTES=$(echo "$RAW_TEXT" | extract_notes 3)
if [ -n "$NOTES" ] && [ "$NOTES" != "- No important notes found" ]; then
  OUTPUT+="\n## Important Notes\n\n$NOTES\n"
fi

# Fallback if no content extracted
if [ -z "$OUTPUT" ]; then
  OUTPUT=$(echo "$RAW_TEXT" | head -c 1000)
  OUTPUT+="\n\n[Response truncated...]"
fi

# Output filtered content
echo -e "$OUTPUT"
