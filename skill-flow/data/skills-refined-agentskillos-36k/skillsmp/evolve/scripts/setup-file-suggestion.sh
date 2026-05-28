#!/bin/bash
# Setup file-suggestion.sh for large codebase optimization
# See: skills/06-scaling/_base/large-codebase.md

cat > ~/.claude/file-suggestion.sh << 'EOF'
#!/bin/bash
# Fast file indexing for Claude Code (large codebase optimization)
# Source: self-evolving-agent/skills/06-scaling/_base/large-codebase.md

CACHE_FILE="${HOME}/.claude/file-index-cache"
CACHE_TTL=300  # 5 minutes

# Check cache validity
if [[ -f "$CACHE_FILE" ]]; then
    if [[ "$(uname)" == "Darwin" ]]; then
        age=$(($(/bin/date +%s) - $(stat -f %m "$CACHE_FILE")))
    else
        age=$(($(/bin/date +%s) - $(stat -c %Y "$CACHE_FILE")))
    fi
    if [[ $age -lt $CACHE_TTL ]]; then
        cat "$CACHE_FILE"
        exit 0
    fi
fi

# Rebuild index
if command -v fd &>/dev/null; then
    fd --type f \
       --hidden \
       --exclude .git \
       --exclude node_modules \
       --exclude __pycache__ \
       --exclude .venv \
       --exclude dist \
       --exclude build \
       > "$CACHE_FILE"
else
    find . -type f \
        -not -path '*/.git/*' \
        -not -path '*/node_modules/*' \
        -not -path '*/__pycache__/*' \
        -not -path '*/.venv/*' \
        -not -path '*/dist/*' \
        -not -path '*/build/*' \
        > "$CACHE_FILE"
fi

cat "$CACHE_FILE"
EOF

chmod +x ~/.claude/file-suggestion.sh
