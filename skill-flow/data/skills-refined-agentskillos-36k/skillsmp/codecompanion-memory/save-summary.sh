#!/bin/bash

# CodeCompanion Memory Save Script
# Saves a conversation summary and indexes it via VectorCode

set -e

# Configuration
SUMMARIES_DIR="$HOME/codecompanion-history/summaries"
TITLE=""
SUMMARY_ID=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--title)
            TITLE="$2"
            shift 2
            ;;
        -i|--id)
            SUMMARY_ID="$2"
            shift 2
            ;;
        -d|--dir)
            SUMMARIES_DIR="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Save a conversation summary and index it for semantic search"
            echo ""
            echo "Options:"
            echo "  -t, --title TEXT    Title for the summary (optional)"
            echo "  -i, --id ID         Summary ID (uses this instead of timestamp, enables updates)"
            echo "  -d, --dir PATH      Summaries directory (default: ~/codecompanion-history/summaries)"
            echo "  -h, --help          Show this help message"
            echo ""
            echo "The summary content should be passed via stdin."
            echo ""
            echo "Examples:"
            echo "  # Create new summary with auto-generated ID:"
            echo "  echo '# My Summary...' | $0 --title 'Debug Session'"
            echo ""
            echo "  # Create or update summary with specific ID:"
            echo "  echo '# My Summary...' | $0 --id 'ses_abc123' --title 'Debug Session'"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use -h or --help for usage information"
            exit 1
            ;;
    esac
done

# Expand tilde in path
SUMMARIES_DIR="${SUMMARIES_DIR/#\~/$HOME}"

# Ensure summaries directory exists
mkdir -p "$SUMMARIES_DIR"

# Generate or use provided ID
# If no ID provided, use timestamp (matching codecompanion-history format)
if [ -z "$SUMMARY_ID" ]; then
    SUMMARY_ID=$(date +%s)
    IS_UPDATE=false
else
    # Clean the ID - remove any problematic characters, keep alphanumeric and underscore
    SUMMARY_ID=$(echo "$SUMMARY_ID" | tr -cd '[:alnum:]_-')
    
    # Check if this is an update
    if [ -f "$SUMMARIES_DIR/${SUMMARY_ID}.md" ]; then
        IS_UPDATE=true
    else
        IS_UPDATE=false
    fi
fi

# Read summary content from stdin
CONTENT=$(cat)

if [ -z "$CONTENT" ]; then
    echo "Error: No summary content provided via stdin"
    exit 1
fi

# Build metadata header
METADATA="<!-- source: opencode -->"
if [ -n "$TITLE" ]; then
    METADATA="$METADATA\n<!-- title: $TITLE -->"
fi
METADATA="$METADATA\n<!-- created: $(date -u +%Y-%m-%dT%H:%M:%SZ) -->"
METADATA="$METADATA\n<!-- id: $SUMMARY_ID -->"
METADATA="$METADATA\n"

# Prepend metadata to content
CONTENT="${METADATA}\n${CONTENT}"

# Save the summary
SUMMARY_PATH="$SUMMARIES_DIR/${SUMMARY_ID}.md"
echo -e "$CONTENT" > "$SUMMARY_PATH"

if [ "$IS_UPDATE" = true ]; then
    echo "Summary updated: $SUMMARY_PATH"
else
    echo "Summary saved to: $SUMMARY_PATH"
fi

# Check if vectorcode is available for indexing
if command -v vectorcode &> /dev/null; then
    echo "Indexing summary with VectorCode..."
    
    # Index the specific file
    cd "$SUMMARIES_DIR"
    RESULT=$(vectorcode vectorise --project_root "$SUMMARIES_DIR" --pipe "$SUMMARY_PATH" 2>/dev/null) || {
        echo "Warning: VectorCode indexing failed, but summary was saved."
        RESULT=""
    }
    
    if [ -n "$RESULT" ]; then
        echo "VectorCode result: $RESULT"
    fi
    echo "Summary indexed successfully!"
else
    echo "Note: VectorCode not found. Summary saved but not indexed for semantic search."
    echo "Install VectorCode to enable semantic search: pipx install vectorcode"
fi

echo ""
echo "Summary ID: $SUMMARY_ID"
echo "Location: $SUMMARY_PATH"
if [ "$IS_UPDATE" = true ]; then
    echo "Status: Updated existing summary"
else
    echo "Status: Created new summary"
fi
