#!/bin/bash

# Check for Bash 4.0+ (required for associative arrays)
if ((BASH_VERSINFO[0] < 4)); then
  echo "ERROR: Bash 4.0 or higher is required."
  exit 1
fi

# Configuration
CHANGELOG_FILE="CHANGELOG.md"
POINTER_FILE=".last-aggregated-commit"
VERBOSE=${VERBOSE:-false}

# Debug function for verbose output
debug() {
  if [ "$VERBOSE" = "true" ]; then
    echo "DEBUG: $*" >&2
  fi
}

# Create secure temporary directory
TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

# 1. Verify prerequisites
if [ ! -f "$CHANGELOG_FILE" ]; then
  echo "ERROR: $CHANGELOG_FILE doesn't exist. Please run 'init-changelog' first."
  exit 1
fi

# Validate CHANGELOG.md structure
if ! grep -q '^# Changelog' "$CHANGELOG_FILE"; then
  echo "ERROR: $CHANGELOG_FILE appears malformed (missing '# Changelog' header)"
  exit 1
fi

if ! sed -n '/^## /q;p' "$CHANGELOG_FILE" > /dev/null 2>&1; then
  echo "ERROR: Failed to parse $CHANGELOG_FILE structure"
  exit 1
fi

if ! git rev-parse --git-dir > /dev/null 2>&1; then
  echo "ERROR: Current directory is not a git repository."
  exit 1
fi

# 2. Read last aggregated commit
if [ ! -f "$POINTER_FILE" ]; then
  git rev-parse HEAD > "$POINTER_FILE"
  echo "WARN: Initialized pointer to HEAD. No changes processed."
  exit 0
fi

LAST_COMMIT=$(cat "$POINTER_FILE")

if ! git cat-file -e "$LAST_COMMIT" 2>/dev/null; then
  git rev-parse HEAD > "$POINTER_FILE"
  echo "WARN: Pointer corrupted. Reinitialized to HEAD."
  exit 0
fi

# 3. Get new commits
NEW_COMMITS=$(git log "$LAST_COMMIT"..HEAD --reverse --pretty=format:%H)

if [ -z "$NEW_COMMITS" ]; then
  echo "WARN: No new commits to process. Changelog is already up to date."
  exit 0
fi

COMMIT_COUNT=$(echo "$NEW_COMMITS" | wc -l)
debug "Processing $COMMIT_COUNT new commits"

# 4. Parse and categorize commits
declare -A entries_added entries_changed entries_deprecated entries_removed entries_fixed entries_security
declare -A seen_issues

# Conventional commit regex
RE="^(feat|fix|perf|refactor|revert|build|docs|style|test|chore|ci)(\([^)]+\))?(!)?: "

for commit in $NEW_COMMITS; do
  SUBJECT=$(git log -1 --pretty=format:%s "$commit")
  BODY=$(git log -1 --pretty=format:%b "$commit")

  debug "Processing commit: ${commit:0:7} - $SUBJECT"

  if [[ "$SUBJECT" =~ $RE ]]; then
    TYPE="${BASH_REMATCH[1]}"
    BREAKING="${BASH_REMATCH[3]}"
    debug "  Matched type: $TYPE, breaking: ${BREAKING:-no}"
  else
    debug "  Skipped: Not a conventional commit"
    continue
  fi

  case "$TYPE" in
    chore|ci|style|test|docs)
      debug "  Skipped: Non-user-facing type ($TYPE)"
      continue
      ;;
  esac

  DESC=$(echo "$SUBJECT" | sed -E 's/^[a-z]+(\([^)]+\))?(!)?: //')
  # Extract issue references in formats: #123, GH-123
  ISSUES=$(echo "$SUBJECT $BODY" | grep -oE '#[0-9]+|GH-[0-9]+' | sed -E 's/^GH-/#/' | sort -u)

  if [ -n "$ISSUES" ]; then
    debug "  Found issue references: $ISSUES"
    duplicate=false
    for issue in $ISSUES; do
      if [[ -n "${seen_issues[$issue]}" ]]; then
        duplicate=true
        break
      fi
    done
    if [ "$duplicate" = true ]; then
      debug "  Skipped: Duplicate issue reference"
      continue
    fi
    for issue in $ISSUES; do
      seen_issues[$issue]=1
    done
  fi

  if [ -n "$BREAKING" ] || echo "$BODY" | grep -qi "^BREAKING[- ]CHANGE:"; then
    BREAKING_DESC=$(echo "$BODY" | grep -i "^BREAKING[- ]CHANGE:" | sed 's/^BREAKING[- ]CHANGE: //')
    if [ -z "$BREAKING_DESC" ]; then
      BREAKING_DESC="$DESC"
    fi
    entries_changed["$commit"]="- **BREAKING**: $BREAKING_DESC"
    debug "  Categorized as: Changed (BREAKING)"
    continue
  fi

  case "$TYPE" in
    feat)
      entries_added["$commit"]="- $DESC"
      debug "  Categorized as: Added"
      ;;
    fix)
      entries_fixed["$commit"]="- $DESC"
      debug "  Categorized as: Fixed"
      ;;
    perf)
      entries_changed["$commit"]="- Improved $DESC"
      debug "  Categorized as: Changed (performance)"
      ;;
    refactor)
      if echo "$BODY" | grep -qi "user-facing\|breaking"; then
        entries_changed["$commit"]="- $DESC"
        debug "  Categorized as: Changed (refactor)"
      else
        debug "  Skipped: Refactor without user-facing changes"
      fi
      ;;
    revert)
      entries_removed["$commit"]="- Reverted: $DESC"
      debug "  Categorized as: Removed (revert)"
      ;;
    build)
      if echo "$SUBJECT" | grep -qi "deps\|upgrade"; then
        entries_changed["$commit"]="- $DESC"
        debug "  Categorized as: Changed (dependency)"
      else
        debug "  Skipped: Build commit without dependency changes"
      fi
      ;;
  esac
done

# 5. Check if there are any user-facing changes
TOTAL_ENTRIES=$((${#entries_added[@]} + ${#entries_changed[@]} + ${#entries_deprecated[@]} + ${#entries_removed[@]} + ${#entries_fixed[@]} + ${#entries_security[@]}))

debug "Summary: $TOTAL_ENTRIES total entries (Added: ${#entries_added[@]}, Changed: ${#entries_changed[@]}, Deprecated: ${#entries_deprecated[@]}, Removed: ${#entries_removed[@]}, Fixed: ${#entries_fixed[@]}, Security: ${#entries_security[@]})"

if [ $TOTAL_ENTRIES -eq 0 ]; then
  echo "WARN: No user-facing changes to add. Changelog unchanged."
  git rev-parse HEAD > "$POINTER_FILE"
  exit 0
fi

# 6. Preserve existing structure
sed -n '/^## /q;p' "$CHANGELOG_FILE" > "$TEMP_DIR/changelog_header.txt"
sed -n '/^## \[[0-9]/,$p' "$CHANGELOG_FILE" > "$TEMP_DIR/changelog_versions.txt"

# 7. Build unreleased section
UNRELEASED="## [Unreleased]\n\n"

if [ ${#entries_added[@]} -gt 0 ]; then
  UNRELEASED+="### Added\n"
  while IFS= read -r entry; do
    UNRELEASED+="$entry\n"
  done < <(for commit in "${!entries_added[@]}"; do echo "${entries_added[$commit]}"; done | sort)
  UNRELEASED+="\n"
fi

if [ ${#entries_changed[@]} -gt 0 ]; then
  UNRELEASED+="### Changed\n"
  # Sort BREAKING changes first (alphabetically), then regular changes (alphabetically)
  while IFS= read -r entry; do
    UNRELEASED+="$entry\n"
  done < <(for commit in "${!entries_changed[@]}"; do
    if [[ "${entries_changed[$commit]}" == *"**BREAKING**"* ]]; then
      echo "${entries_changed[$commit]}"
    fi
  done | sort)
  while IFS= read -r entry; do
    UNRELEASED+="$entry\n"
  done < <(for commit in "${!entries_changed[@]}"; do
    if [[ "${entries_changed[$commit]}" != *"**BREAKING**"* ]]; then
      echo "${entries_changed[$commit]}"
    fi
  done | sort)
  UNRELEASED+="\n"
fi

if [ ${#entries_deprecated[@]} -gt 0 ]; then
  UNRELEASED+="### Deprecated\n"
  while IFS= read -r entry; do
    UNRELEASED+="$entry\n"
  done < <(for commit in "${!entries_deprecated[@]}"; do echo "${entries_deprecated[$commit]}"; done | sort)
  UNRELEASED+="\n"
fi

if [ ${#entries_removed[@]} -gt 0 ]; then
  UNRELEASED+="### Removed\n"
  while IFS= read -r entry; do
    UNRELEASED+="$entry\n"
  done < <(for commit in "${!entries_removed[@]}"; do echo "${entries_removed[$commit]}"; done | sort)
  UNRELEASED+="\n"
fi

if [ ${#entries_fixed[@]} -gt 0 ]; then
  UNRELEASED+="### Fixed\n"
  while IFS= read -r entry; do
    UNRELEASED+="$entry\n"
  done < <(for commit in "${!entries_fixed[@]}"; do echo "${entries_fixed[$commit]}"; done | sort)
  UNRELEASED+="\n"
fi

if [ ${#entries_security[@]} -gt 0 ]; then
  UNRELEASED+="### Security\n"
  while IFS= read -r entry; do
    UNRELEASED+="$entry\n"
  done < <(for commit in "${!entries_security[@]}"; do echo "${entries_security[$commit]}"; done | sort)
  UNRELEASED+="\n"
fi

# 8. Reconstruct CHANGELOG.md
{
  cat "$TEMP_DIR/changelog_header.txt"
  printf "%b\n" "$UNRELEASED"
  cat "$TEMP_DIR/changelog_versions.txt"
} > "$CHANGELOG_FILE"

# 9. Update pointer
git rev-parse HEAD > "$POINTER_FILE"

# 10. Build detailed success message

CATEGORIES=""
[ ${#entries_added[@]} -gt 0 ] && CATEGORIES+="${#entries_added[@]} Added, "
[ ${#entries_changed[@]} -gt 0 ] && CATEGORIES+="${#entries_changed[@]} Changed, "
[ ${#entries_deprecated[@]} -gt 0 ] && CATEGORIES+="${#entries_deprecated[@]} Deprecated, "
[ ${#entries_removed[@]} -gt 0 ] && CATEGORIES+="${#entries_removed[@]} Removed, "
[ ${#entries_fixed[@]} -gt 0 ] && CATEGORIES+="${#entries_fixed[@]} Fixed, "
[ ${#entries_security[@]} -gt 0 ] && CATEGORIES+="${#entries_security[@]} Security, "
CATEGORIES=${CATEGORIES%, }  # Remove trailing comma and space

echo "SUCCESS: Changelog updated with $TOTAL_ENTRIES entries ($CATEGORIES)."
