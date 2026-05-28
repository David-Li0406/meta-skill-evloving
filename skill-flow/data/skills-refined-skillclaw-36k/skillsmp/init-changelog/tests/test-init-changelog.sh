#!/bin/bash

# Test suite for init-changelog.sh

# Resolve script path relative to this test file
SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")/../scripts" && pwd)/init-changelog.sh"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

setup() {
  TEST_DIR=$(mktemp -d)
  cd "$TEST_DIR" || exit 1
}

setup_git() {
  git init --quiet
  git config user.email "test@example.com"
  git config user.name "Test User"
}

teardown() {
  rm -rf "$TEST_DIR"
}

fail() {
  echo -e "${RED}FAIL: $1${NC}"
  teardown
  exit 1
}

pass() {
  echo -e "${GREEN}PASS: $1${NC}"
}

run_test() {
  echo "Running: $1"
  setup
  $1
  teardown
}

# --- Basic Tests ---

test_creates_changelog() {
  setup_git
  git commit --allow-empty -m "Initial commit" --quiet

  "$SCRIPT_PATH" > /dev/null

  if [[ -f "CHANGELOG.md" ]]; then
    pass "Creates CHANGELOG.md"
  else
    fail "Failed to create CHANGELOG.md"
  fi
}

test_already_initialized() {
  setup_git
  git commit --allow-empty -m "Initial commit" --quiet

  # First run
  "$SCRIPT_PATH" > /dev/null

  # Second run
  output=$("$SCRIPT_PATH")

  if [[ "$output" == *"WARN"* ]] && [[ "$output" == *"already initialized"* ]]; then
    pass "Already initialized (graceful exit)"
  else
    fail "Failed to handle already initialized case: $output"
  fi
}

test_pointer_initialization() {
  setup_git
  git commit --allow-empty -m "Initial commit" --quiet

  "$SCRIPT_PATH" > /dev/null

  if [[ -f ".last-aggregated-commit" ]]; then
    pass "Pointer initialization (.last-aggregated-commit created)"
  else
    fail "Failed to create .last-aggregated-commit"
  fi
}

# --- Version Detection Tests ---

test_version_from_git_tag() {
  setup_git
  git commit --allow-empty -m "Initial commit" --quiet
  git tag -a "v1.2.3" -m "Version 1.2.3"

  "$SCRIPT_PATH" > /dev/null

  content=$(cat CHANGELOG.md)
  if [[ "$content" == *"## [1.2.3]"* ]]; then
    pass "Version detection from git tag"
  else
    fail "Failed to detect version from git tag"
  fi
}

test_version_from_package_json() {
  setup_git
  git commit --allow-empty -m "Initial commit" --quiet

  echo '{"version": "2.3.4"}' > package.json

  "$SCRIPT_PATH" > /dev/null

  content=$(cat CHANGELOG.md)
  if [[ "$content" == *"## [2.3.4]"* ]]; then
    pass "Version detection from package.json"
  else
    fail "Failed to detect version from package.json"
  fi
}

test_version_from_cargo_toml() {
  setup_git
  git commit --allow-empty -m "Initial commit" --quiet

  cat > Cargo.toml << EOF
[package]
name = "test"
version = "3.4.5"
EOF

  "$SCRIPT_PATH" > /dev/null

  content=$(cat CHANGELOG.md)
  if [[ "$content" == *"## [3.4.5]"* ]]; then
    pass "Version detection from Cargo.toml"
  else
    fail "Failed to detect version from Cargo.toml"
  fi
}

test_version_from_pyproject_toml() {
  setup_git
  git commit --allow-empty -m "Initial commit" --quiet

  cat > pyproject.toml << EOF
[project]
name = "test"
version = "4.5.6"
EOF

  "$SCRIPT_PATH" > /dev/null

  content=$(cat CHANGELOG.md)
  if [[ "$content" == *"## [4.5.6]"* ]]; then
    pass "Version detection from pyproject.toml"
  else
    fail "Failed to detect version from pyproject.toml"
  fi
}

test_default_version() {
  setup_git
  git commit --allow-empty -m "Initial commit" --quiet

  # No version files or tags
  "$SCRIPT_PATH" > /dev/null

  content=$(cat CHANGELOG.md)
  if [[ "$content" == *"## [0.1.0]"* ]]; then
    pass "Default version (0.1.0)"
  else
    fail "Failed to use default version"
  fi
}

# --- Smart Pointer Tests ---

test_small_repo_pointer() {
  setup_git

  # Create exactly 50 commits (≤100 threshold)
  for i in {1..50}; do
    git commit --allow-empty -m "Commit $i" --quiet
  done

  "$SCRIPT_PATH" > /dev/null

  # Get first commit
  FIRST_COMMIT=$(git rev-list --max-parents=0 HEAD)
  POINTER_VALUE=$(cat .last-aggregated-commit)

  if [[ "$POINTER_VALUE" == "$FIRST_COMMIT" ]]; then
    pass "Small repo pointer (≤100 commits → first commit)"
  else
    fail "Pointer not set to first commit for small repo"
  fi
}

test_large_repo_pointer() {
  setup_git

  # Create 150 commits (>100 threshold)
  for i in {1..150}; do
    git commit --allow-empty -m "Commit $i" --quiet
  done

  "$SCRIPT_PATH" > /dev/null

  # Get HEAD
  EXPECTED_COMMIT=$(git rev-parse HEAD~100)
  POINTER_VALUE=$(cat .last-aggregated-commit)

  if [[ "$POINTER_VALUE" == "$EXPECTED_COMMIT" ]]; then
    pass "Large repo pointer (>100 commits → HEAD~100)"
  else
    fail "Pointer not set to HEAD~100 for large repo"
  fi
}

test_exactly_100_commits() {
  setup_git

  # Create exactly 100 commits (boundary condition)
  for i in {1..100}; do
    git commit --allow-empty -m "Commit $i" --quiet
  done

  "$SCRIPT_PATH" > /dev/null

  # Should behave as small repo (≤100)
  FIRST_COMMIT=$(git rev-list --max-parents=0 HEAD)
  POINTER_VALUE=$(cat .last-aggregated-commit)

  if [[ "$POINTER_VALUE" == "$FIRST_COMMIT" ]]; then
    pass "Exactly 100 commits (treated as ≤100)"
  else
    fail "Exactly 100 commits not handled correctly"
  fi
}

# --- Edge Cases ---

test_non_git_repository() {
  # Don't initialize git

  "$SCRIPT_PATH" > /dev/null

  if [[ -f "CHANGELOG.md" ]] && [[ ! -f ".last-aggregated-commit" ]]; then
    pass "Non-git repository (CHANGELOG created, no pointer)"
  else
    fail "Failed to handle non-git repository correctly"
  fi
}

test_version_priority() {
  setup_git
  git commit --allow-empty -m "Initial commit" --quiet

  # Create both git tag and package.json
  git tag -a "v5.6.7" -m "Version 5.6.7"
  echo '{"version": "9.9.9"}' > package.json

  "$SCRIPT_PATH" > /dev/null

  content=$(cat CHANGELOG.md)
  # Git tag should take precedence
  if [[ "$content" == *"## [5.6.7]"* ]] && [[ "$content" != *"## [9.9.9]"* ]]; then
    pass "Version priority (git tag > package.json)"
  else
    fail "Version priority not respected"
  fi
}

test_git_tag_with_v_prefix() {
  setup_git
  git commit --allow-empty -m "Initial commit" --quiet
  git tag -a "v1.0.0" -m "Version 1.0.0"

  "$SCRIPT_PATH" > /dev/null

  content=$(cat CHANGELOG.md)
  # Should strip 'v' prefix
  if [[ "$content" == *"## [1.0.0]"* ]] && [[ "$content" != *"## [v1.0.0]"* ]]; then
    pass "Git tag with 'v' prefix stripped"
  else
    fail "Failed to strip 'v' prefix from git tag"
  fi
}

# --- Template Structure Tests ---

test_template_has_all_sections() {
  setup_git
  git commit --allow-empty -m "Initial commit" --quiet

  "$SCRIPT_PATH" > /dev/null

  content=$(cat CHANGELOG.md)

  if [[ "$content" == *"### Added"* ]] && \
     [[ "$content" == *"### Changed"* ]] && \
     [[ "$content" == *"### Deprecated"* ]] && \
     [[ "$content" == *"### Removed"* ]] && \
     [[ "$content" == *"### Fixed"* ]] && \
     [[ "$content" == *"### Security"* ]]; then
    pass "Template has all Keep a Changelog sections"
  else
    fail "Template missing required sections"
  fi
}

test_template_has_unreleased() {
  setup_git
  git commit --allow-empty -m "Initial commit" --quiet

  "$SCRIPT_PATH" > /dev/null

  content=$(cat CHANGELOG.md)
  if [[ "$content" == *"## [Unreleased]"* ]]; then
    pass "Template has Unreleased section"
  else
    fail "Template missing Unreleased section"
  fi
}

test_success_message() {
  setup_git
  git commit --allow-empty -m "Initial commit" --quiet

  output=$("$SCRIPT_PATH")

  if [[ "$output" == *"SUCCESS"* ]] && [[ "$output" == *"Initialized changelog"* ]]; then
    pass "Success message format"
  else
    fail "Incorrect success message: $output"
  fi
}

# --- Run All ---

run_test test_creates_changelog
run_test test_already_initialized
run_test test_pointer_initialization
run_test test_version_from_git_tag
run_test test_version_from_package_json
run_test test_version_from_cargo_toml
run_test test_version_from_pyproject_toml
run_test test_default_version
run_test test_small_repo_pointer
run_test test_large_repo_pointer
run_test test_exactly_100_commits
run_test test_non_git_repository
run_test test_version_priority
run_test test_git_tag_with_v_prefix
run_test test_template_has_all_sections
run_test test_template_has_unreleased
run_test test_success_message

echo "All tests passed."
