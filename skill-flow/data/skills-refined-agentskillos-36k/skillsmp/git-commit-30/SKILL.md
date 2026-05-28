---
name: git-commit
description: Commit all changes with validation, conventional commit message, GPG signing, and push to origin
invocation: /bkff:git-commit
arguments:
  - name: --message
    type: string
    required: false
    description: Override auto-generated commit message
  - name: --co-author
    type: string
    required: false
    description: Add co-author attribution (format "Name <email>")
---

# Commit Changes

Validates changes, stages all new and modified files, generates a conventional commit message, creates a GPG-signed commit, and pushes to origin.

## Usage

```
/bkff:git-commit [--message "custom message"] [--co-author "Name <email>"]
```

## Options

| Option | Description |
|--------|-------------|
| `--message` | Override the auto-generated commit message |
| `--co-author` | Add a co-author to the commit |

## What It Does

1. Validates changes using build tool (make lint, npm run lint, etc.)
2. Halts if validation fails with error details
3. Stages all changes (`git add -A`)
4. Analyzes changes to generate conventional commit type and scope
5. Creates a GPG-signed commit
6. Pushes to origin

## Conventional Commit Types

| Change Pattern | Generated Type |
|----------------|----------------|
| New files in `src/` | `feat` |
| Bug fixes, modifications | `fix` |
| Refactoring | `refactor` |
| Test file changes only | `test` |
| Documentation changes | `docs` |
| Build/config changes | `build` |

## Example Output

```
## Commit Created

### Validation
- ✓ Build tool validation passed

### Changes Committed
- **Files**: 3 files changed
  - M src/auth.ts
  - A src/utils.ts
  - M README.md

### Commit
- **Hash**: abc1234
- **Message**: feat(auth): implement login functionality
- **Signed**: Yes

### Push
- **Status**: Success
```

## Requirements

- Must be run inside a git worktree
- `git` CLI for commit and push
- GPG configured for commit signing
- Build tool with validate/lint target (optional)

## Error Cases

- **No changes**: "Nothing to commit"
- **Validation failed**: Shows lint/test errors
- **GPG unavailable**: Error with configuration instructions
- **Push failed**: Commit preserved locally, retry instructions

## Implementation

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
source "$PLUGIN_DIR/lib/common.sh"
source "$PLUGIN_DIR/lib/git-helpers.sh"
source "$PLUGIN_DIR/lib/validation.sh"

# Parse arguments
CUSTOM_MESSAGE=""
CO_AUTHOR=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --message|-m)
            CUSTOM_MESSAGE="$2"
            shift 2
            ;;
        --co-author)
            CO_AUTHOR="$2"
            shift 2
            ;;
        *)
            shift
            ;;
    esac
done

require_worktree

# Check for changes
if ! has_changes; then
    info "Nothing to commit. Working directory is clean."
    exit 0
fi

echo "## Commit Process"
echo ""

# FR-012, FR-013: Run validation
echo "### Validation"
if has_validate_target; then
    if run_validation; then
        echo "- ✓ Build tool validation passed"
    else
        echo "- ✗ Build tool validation failed"
        echo ""
        error_exit "Fix validation errors before committing."
    fi
else
    echo "- ⊘ No validation target found (skipped)"
fi
echo ""

# FR-016: Check GPG signing availability
if ! has_signing_available; then
    error_exit "GPG signing required but unavailable. Configure GPG key first:\n  git config --global user.signingkey <KEY_ID>\n  git config --global commit.gpgsign true"
fi

# FR-014: Stage all changes
info "Staging all changes..."
git add -A

# Get list of staged files for display and analysis
STAGED_FILES=$(git diff --cached --name-status)
STAGED_COUNT=$(echo "$STAGED_FILES" | grep -c '^' || echo "0")

echo "### Changes to Commit"
echo "- **Files**: $STAGED_COUNT files"
echo "$STAGED_FILES" | while IFS=$'\t' read -r status file; do
    printf "  - %s %s\n" "$status" "$file"
done
echo ""

# FR-015: Generate conventional commit message
generate_commit_type() {
    local files="$1"

    # Check for new files (feat)
    if echo "$files" | grep -q '^A'; then
        # New source files = feat
        if echo "$files" | grep -qE '^A.*\.(ts|js|py|go|rs|java|sh)$'; then
            echo "feat"
            return
        fi
    fi

    # Check for test files only
    if echo "$files" | grep -qE 'test|spec' && ! echo "$files" | grep -vqE 'test|spec'; then
        echo "test"
        return
    fi

    # Check for docs only
    if echo "$files" | grep -qE '\.(md|txt|rst)$' && ! echo "$files" | grep -vqE '\.(md|txt|rst)$'; then
        echo "docs"
        return
    fi

    # Check for build/config files
    if echo "$files" | grep -qE '(Makefile|package\.json|Cargo\.toml|\.yml|\.yaml)'; then
        echo "build"
        return
    fi

    # Default to fix for modifications
    echo "fix"
}

generate_scope() {
    local files="$1"

    # Extract common directory from changed files
    local first_dir
    first_dir=$(echo "$files" | head -1 | awk -F'\t' '{print $2}' | cut -d'/' -f1)

    # If it's a known directory, use it as scope
    case "$first_dir" in
        src|lib|pkg|cmd|internal)
            # Get the next level directory as scope
            local scope
            scope=$(echo "$files" | head -1 | awk -F'\t' '{print $2}' | cut -d'/' -f2)
            if [[ -n "$scope" && "$scope" != *.* ]]; then
                echo "$scope"
                return
            fi
            ;;
        skills|plugins|commands)
            echo "$first_dir"
            return
            ;;
    esac

    echo ""
}

generate_description() {
    local commit_type="$1"
    local files="$2"

    # Get the first changed file for context
    local first_file
    first_file=$(echo "$files" | head -1 | awk -F'\t' '{print $2}' | xargs basename 2>/dev/null || echo "files")
    first_file="${first_file%.*}"  # Remove extension

    case "$commit_type" in
        feat) echo "add ${first_file} functionality" ;;
        fix) echo "update ${first_file}" ;;
        docs) echo "update documentation" ;;
        test) echo "update tests" ;;
        build) echo "update build configuration" ;;
        *) echo "update ${first_file}" ;;
    esac
}

if [[ -n "$CUSTOM_MESSAGE" ]]; then
    COMMIT_MSG="$CUSTOM_MESSAGE"
else
    COMMIT_TYPE=$(generate_commit_type "$STAGED_FILES")
    COMMIT_SCOPE=$(generate_scope "$STAGED_FILES")
    COMMIT_DESC=$(generate_description "$COMMIT_TYPE" "$STAGED_FILES")

    if [[ -n "$COMMIT_SCOPE" ]]; then
        COMMIT_MSG="${COMMIT_TYPE}(${COMMIT_SCOPE}): ${COMMIT_DESC}"
    else
        COMMIT_MSG="${COMMIT_TYPE}: ${COMMIT_DESC}"
    fi
fi

# Add co-author if specified
if [[ -n "$CO_AUTHOR" ]]; then
    COMMIT_MSG="${COMMIT_MSG}

Co-authored-by: ${CO_AUTHOR}"
fi

# FR-016: Create signed commit
info "Creating signed commit..."
if git commit -S -m "$COMMIT_MSG"; then
    COMMIT_HASH=$(git rev-parse --short HEAD)
    success "Commit created: $COMMIT_HASH"
else
    error_exit "Failed to create commit"
fi

echo ""
echo "### Commit"
echo "- **Hash**: $COMMIT_HASH"
echo "- **Message**: $(echo "$COMMIT_MSG" | head -1)"
echo "- **Signed**: Yes"
[[ -n "$CO_AUTHOR" ]] && echo "- **Co-Author**: $CO_AUTHOR"
echo ""

# FR-017: Push to origin
echo "### Push"
info "Pushing to origin..."
if git push; then
    echo "- **Status**: Success"
    echo ""
    success "Commit pushed to origin."
else
    warn "Push failed (commit preserved locally)"
    echo "- **Status**: Failed"
    echo ""
    echo "Run 'git push' to retry."
fi
```
