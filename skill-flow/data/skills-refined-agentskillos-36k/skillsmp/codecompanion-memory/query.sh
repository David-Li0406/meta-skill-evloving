#!/bin/bash

# CodeCompanion Memory Query Script
# Wrapper around VectorCode CLI for querying codecompanion-history summaries

set -e

# Default values
PROJECT_ROOT="$HOME/codecompanion-history/summaries"
COUNT=5
VERBOSE=false
QUERY=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -q|--query)
            QUERY="$2"
            shift 2
            ;;
        -n|--count)
            COUNT="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -p|--project)
            PROJECT_ROOT="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Query codecompanion-history summaries using semantic search"
            echo ""
            echo "Options:"
            echo "  -q, --query TEXT      Search query (required)"
            echo "  -n, --count NUMBER    Number of results (default: 5)"
            echo "  -v, --verbose         Show full document content"
            echo "  -p, --project PATH    Project root path (default: ~/codecompanion-history/summaries)"
            echo "  -h, --help            Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use -h or --help for usage information"
            exit 1
            ;;
    esac
done

# Validate required parameters
if [ -z "$QUERY" ]; then
    echo "Error: --query is required"
    echo "Use -h or --help for usage information"
    exit 1
fi

# Expand tilde in path
PROJECT_ROOT="${PROJECT_ROOT/#\~/$HOME}"

# Check if vectorcode is available
if ! command -v vectorcode &> /dev/null; then
    echo "Error: vectorcode command not found"
    echo "Please install VectorCode: https://github.com/Davidyz/VectorCode"
    exit 1
fi

# Check if project root exists
if [ ! -d "$PROJECT_ROOT" ]; then
    echo "Error: Project root does not exist: $PROJECT_ROOT"
    exit 1
fi

echo "Searching in: $PROJECT_ROOT"
echo "Query: $QUERY"
echo ""

# Run vectorcode query
cd "$PROJECT_ROOT"
RESULTS=$(vectorcode query "$QUERY" -n "$COUNT" --pipe 2>/dev/null)

# Check if results are empty
if [ "$RESULTS" = "[]" ] || [ -z "$RESULTS" ]; then
    echo "No results found."
    exit 0
fi

# Parse and display results
echo "$RESULTS" | python3 -c "
import json
import sys

try:
    results = json.load(sys.stdin)
    for i, result in enumerate(results, 1):
        print(f'--- Result {i} ---')
        path = result.get('path', 'Unknown')
        print(f'Path: {path}')
        
        if '$VERBOSE' == 'true':
            document = result.get('document', '')
            print(f'\nDocument:\n{document}\n')
        else:
            # Show first 200 characters of document
            document = result.get('document', '')
            preview = document[:200] + '...' if len(document) > 200 else document
            print(f'Preview: {preview}\n')
            
except json.JSONDecodeError as e:
    print(f'Error parsing results: {e}', file=sys.stderr)
    sys.exit(1)
"
