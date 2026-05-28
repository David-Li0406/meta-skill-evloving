#!/bin/bash
# Complete commit workflow: format, archive, changelog, and commit
# Single script handles everything after user approves implementation

set -e

TICKET="$1"
COMMIT_MSG="$2"
REPO_URL="$3"
DESCRIPTION="$4"
shift 4 2>/dev/null || true
FILES=("$@")

if [ -z "$TICKET" ] || [ -z "$COMMIT_MSG" ]; then
    echo "Usage: archive.sh <ticket-path> <commit-message> <repo-url> [description] [files...]"
    echo "Example: archive.sh .work/tickets/20260115-feature.md 'Add new feature' https://github.com/org/repo 'Enables users to authenticate with session-based login' src/foo.ts"
    exit 1
fi

if [ ! -f "$TICKET" ]; then
    echo "Error: Ticket not found: $TICKET"
    exit 1
fi

BRANCH=$(git branch --show-current)

if [ -z "$BRANCH" ]; then
    echo "Error: Cannot archive ticket: not on a named branch."
    echo "       Please checkout a branch first (e.g., git checkout -b feature-branch)"
    exit 1
fi

TICKET_DIR=$(dirname "$TICKET")
ARCHIVE_DIR="${TICKET_DIR}/archive/${BRANCH}"
CHANGELOG=".work/changelogs/${BRANCH}.md"
TICKET_FILENAME=$(basename "$TICKET")

# Step 1: Move ticket to archive
echo "==> Archiving ticket..."
mkdir -p "$ARCHIVE_DIR"
mkdir -p ".work/changelogs"
mv "$TICKET" "$ARCHIVE_DIR/"
echo "    ${ARCHIVE_DIR}/${TICKET_FILENAME}"

# Step 2: Initialize CHANGELOG if not exists
if [ ! -f "$CHANGELOG" ]; then
    cat > "$CHANGELOG" << 'HEADER'
# Branch Changelog

## Added

## Changed

## Removed
HEADER
fi

# Step 3: Determine section based on commit message verb
SECTION="Changed"
case "$COMMIT_MSG" in
    Add*|Create*|Implement*|Introduce*)
        SECTION="Added"
        ;;
    Remove*|Delete*)
        SECTION="Removed"
        ;;
esac

# Step 4: Create changelog entry with placeholder
ENTRY="- ${COMMIT_MSG} - [ticket](${TICKET_FILENAME})"

awk -v section="## $SECTION" -v entry="$ENTRY" -v desc="$DESCRIPTION" '
    $0 == section {
        print
        getline
        print entry
        if (desc != "") print "  " desc
        next
    }
    { print }
' "$CHANGELOG" > "${CHANGELOG}.tmp" && mv "${CHANGELOG}.tmp" "$CHANGELOG"
echo "==> Updated CHANGELOG"

# Step 5: Stage all changes and commit
echo "==> Committing..."
git add -A
git commit -m "${COMMIT_MSG}

Co-Authored-By: Claude <noreply@anthropic.com>"

COMMIT_HASH=$(git rev-parse --short HEAD)

# Step 6: Update CHANGELOG with commit hash and amend
if [ -n "$REPO_URL" ]; then
    sed -i.bak "s|- ${COMMIT_MSG} - \[ticket\]|- ${COMMIT_MSG} ([${COMMIT_HASH}](${REPO_URL}/commit/${COMMIT_HASH})) - [ticket]|" "$CHANGELOG"
    rm -f "${CHANGELOG}.bak"
    git add "$CHANGELOG"
    git commit --amend --no-edit
    echo "==> Added commit hash to CHANGELOG"
fi

echo ""
echo "Done!"
echo "  Commit: ${COMMIT_HASH}"
echo "  Ticket: ${ARCHIVE_DIR}/${TICKET_FILENAME}"
