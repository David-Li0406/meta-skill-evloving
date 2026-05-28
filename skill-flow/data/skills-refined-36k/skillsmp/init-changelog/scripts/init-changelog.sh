#!/bin/bash

# Check for Bash 4.0+ (required for associative arrays in related scripts)
if ((BASH_VERSINFO[0] < 4)); then
  echo "ERROR: Bash 4.0 or higher is required."
  exit 1
fi

# Configuration
CHANGELOG_FILE="CHANGELOG.md"
POINTER_FILE=".last-aggregated-commit"
COMMIT_THRESHOLD=100  # Smart detection threshold

# 1. Verify prerequisites - Check if already initialized
if [ -f "$CHANGELOG_FILE" ]; then
  echo "WARN: Changelog already initialized. No files were changed."
  exit 0
fi

# 2. Detect current version in priority order
detect_version() {
  local version=""

  # Priority 1: Git tags
  if git rev-parse --git-dir > /dev/null 2>&1; then
    version=$(git describe --tags --abbrev=0 2>/dev/null | grep -E '^v?[0-9]+\.[0-9]+\.[0-9]+' | sed 's/^v//')
    if [ -n "$version" ]; then
      echo "$version"
      return
    fi
  fi

  # Priority 2: package.json (Node.js)
  if [ -f "package.json" ]; then
    version=$(grep -o '"version": *"[^"]*"' package.json | grep -o '[0-9][^"]*' | head -1)
    if [ -n "$version" ]; then
      echo "$version"
      return
    fi
  fi

  # Priority 3: Cargo.toml (Rust)
  if [ -f "Cargo.toml" ]; then
    version=$(grep '^version = ' Cargo.toml | grep -o '"[^"]*"' | tr -d '"' | head -1)
    if [ -n "$version" ]; then
      echo "$version"
      return
    fi
  fi

  # Priority 4: pyproject.toml (Python)
  if [ -f "pyproject.toml" ]; then
    version=$(grep '^version = ' pyproject.toml | grep -o '"[^"]*"' | tr -d '"' | head -1)
    if [ -n "$version" ]; then
      echo "$version"
      return
    fi
  fi

  # Default: Use 0.1.0
  echo "0.1.0"
}

DETECTED_VERSION=$(detect_version)
CURRENT_DATE=$(date +%Y-%m-%d)

# 3. Create CHANGELOG.md with appropriate template
if [ "$DETECTED_VERSION" != "" ]; then
  # Template with both Unreleased and current version
  cat > "$CHANGELOG_FILE" << EOF
# Changelog

## [Unreleased]

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security

## [$DETECTED_VERSION] - $CURRENT_DATE

### Added

- Initial release
EOF
else
  # Template with only Unreleased (no version detected)
  cat > "$CHANGELOG_FILE" << EOF
# Changelog

## [Unreleased]

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security
EOF
fi

# Check if CHANGELOG.md was created successfully
if [ ! -f "$CHANGELOG_FILE" ]; then
  echo "ERROR: Failed to create changelog files due to a write error."
  exit 1
fi

# 4. Initialize pointer with smart detection (only if in git repository)
if git rev-parse --git-dir > /dev/null 2>&1; then
  # Count total commits in repository
  COMMIT_COUNT=$(git rev-list --count HEAD 2>/dev/null)

  if [ $? -eq 0 ] && [ -n "$COMMIT_COUNT" ]; then
    if [ "$COMMIT_COUNT" -le "$COMMIT_THRESHOLD" ]; then
      # Small repository: set pointer to first commit (enables backfill)
      FIRST_COMMIT=$(git rev-list --max-parents=0 HEAD)
      echo "$FIRST_COMMIT" > "$POINTER_FILE"
    else
      # Large repository: set pointer to 100 commits ago (backfill recent history)
      git rev-parse HEAD~100 > "$POINTER_FILE"
    fi
  fi
fi

# 5. Output success message
echo "SUCCESS: Initialized changelog structure."
