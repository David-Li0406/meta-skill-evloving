#!/bin/bash

# Test suite for edit-changelog.sh

# Resolve script path relative to this test file
SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")/../scripts" && pwd)/edit-changelog.sh"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

setup() {
  TEST_DIR=$(mktemp -d)
  cd "$TEST_DIR" || exit 1
  git init --quiet
  git config user.email "test@example.com"
  git config user.name "Test User"
  
  # Create initial changelog
  echo "# Changelog" > CHANGELOG.md
  echo "" >> CHANGELOG.md
  echo "## [1.0.0] - 2025-01-01" >> CHANGELOG.md
  echo "- Initial release" >> CHANGELOG.md
  
  # Initial commit
  git add CHANGELOG.md
  git commit -m "chore: initial commit" --quiet
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

# --- Tests ---

test_prerequisites_missing_changelog() {
  rm CHANGELOG.md
  output=$("$SCRIPT_PATH" 2>&1)
  if [[ $? -eq 1 ]] && [[ "$output" == *"CHANGELOG.md doesn't exist"* ]]; then
    pass "Prerequisites check (missing CHANGELOG.md)"
  else
    fail "Prerequisites check failed to detect missing CHANGELOG.md"
  fi
}

test_bootstrap_pointer() {
  # No pointer file initially
  output=$("$SCRIPT_PATH")
  
  if [[ -f ".last-aggregated-commit" ]]; then
    pass "Bootstrap pointer created"
  else
    fail "Bootstrap pointer not created"
  fi
}

test_standard_flow() {
  # Initialize pointer
  "$SCRIPT_PATH" > /dev/null
  
  # Create commits
  touch file1 && git add file1 && git commit -m "feat: add feature A" --quiet
  touch file2 && git add file2 && git commit -m "fix: fix bug B" --quiet
  
  # Run script
  "$SCRIPT_PATH" > /dev/null
  
  # Verify content
  content=$(cat CHANGELOG.md)
  if [[ "$content" == *"### Added"* ]] && [[ "$content" == *"- add feature A"* ]] && \
     [[ "$content" == *"### Fixed"* ]] && [[ "$content" == *"- fix bug B"* ]]; then
    pass "Standard flow (feat/fix)"
  else
    echo "$content"
    fail "Standard flow failed to generate correct entries"
  fi
}

test_deduplication() {
  # Initialize pointer
  "$SCRIPT_PATH" > /dev/null
  
  # Create commits with same issue
  touch file1 && git add file1 && git commit -m "feat: add feature (#123)" --quiet
  touch file2 && git add file2 && git commit -m "feat: update feature (#123)" --quiet
  
  # Run script
  "$SCRIPT_PATH" > /dev/null
  
  # Verify content (should only have the first one)
  count=$(grep -c "(#123)" CHANGELOG.md)
  if [[ $count -eq 1 ]]; then
    pass "Deduplication by issue number"
  else
    fail "Deduplication failed (found $count occurrences)"
  fi
}

test_breaking_change() {
  # Initialize pointer
  "$SCRIPT_PATH" > /dev/null
  
  # Create breaking commit
  touch file1 && git add file1 && git commit -m "feat!: breaking feature" --quiet
  
  # Run script
  "$SCRIPT_PATH" > /dev/null
  
  # Verify content
  content=$(cat CHANGELOG.md)
  if [[ "$content" == *"### Changed"* ]] && [[ "$content" == *"- **BREAKING**: breaking feature"* ]]; then
    pass "Breaking change detection"
  else
    fail "Breaking change detection failed"
  fi
}

test_no_new_commits() {
  # Initialize pointer
  "$SCRIPT_PATH" > /dev/null
  
  # Run script again without new commits
  output=$("$SCRIPT_PATH")
  
  if [[ "$output" == *"No new commits"* ]]; then
    pass "No new commits handled gracefully"
  else
    fail "Failed to handle no new commits"
  fi
}

test_corrupted_pointer() {
  # Initialize pointer
  "$SCRIPT_PATH" > /dev/null
  
  # Corrupt it
  echo "invalid-hash-123" > .last-aggregated-commit
  
  # Run script (should recover)
  output=$("$SCRIPT_PATH")
  
  if [[ "$output" == *"Pointer corrupted"* ]]; then
    pass "Corrupted pointer recovery"
  else
    fail "Failed to handle corrupted pointer"
  fi
}

test_ignored_types() {
  "$SCRIPT_PATH" > /dev/null
  
  git commit --allow-empty -m "chore: cleanup" --quiet
  git commit --allow-empty -m "docs: update readme" --quiet
  git commit --allow-empty -m "test: add tests" --quiet
  git commit --allow-empty -m "style: format code" --quiet
  git commit --allow-empty -m "ci: update pipeline" --quiet
  
  "$SCRIPT_PATH" > /dev/null
  
  content=$(cat CHANGELOG.md)
  if [[ "$content" != *"cleanup"* ]] && [[ "$content" != *"update readme"* ]]; then
    pass "Ignored types (chore, docs, etc.)"
  else
    fail "Failed to ignore non-user-facing types"
  fi
}

test_revert_commit() {
  "$SCRIPT_PATH" > /dev/null
  git commit --allow-empty -m "revert: undo feature X" --quiet
  "$SCRIPT_PATH" > /dev/null
  
  content=$(cat CHANGELOG.md)
  if [[ "$content" == *"### Removed"* ]] && [[ "$content" == *"- Reverted: undo feature X"* ]]; then
    pass "Revert commit handling"
  else
    fail "Failed to handle revert commit"
  fi
}

test_conditional_types() {
  "$SCRIPT_PATH" > /dev/null
  
  # Should be included
  git commit --allow-empty -m "build: upgrade deps" --quiet
  # Use -m twice to set subject and body separately
  git commit --allow-empty -m "refactor: user-facing cleanup" -m "This is a user-facing change" --quiet
  
  # Should be ignored
  git commit --allow-empty -m "build: internal script" --quiet
  git commit --allow-empty -m "refactor: internal cleanup" --quiet
  
  "$SCRIPT_PATH" > /dev/null
  
  content=$(cat CHANGELOG.md)
  if [[ "$content" == *"upgrade deps"* ]] && [[ "$content" == *"user-facing cleanup"* ]] && \
     [[ "$content" != *"internal script"* ]] && [[ "$content" != *"internal cleanup"* ]]; then
    pass "Conditional types (build/refactor)"
  else
    fail "Failed to handle conditional types correctly"
  fi
}

test_scoped_commit() {
  "$SCRIPT_PATH" > /dev/null
  git commit --allow-empty -m "feat(auth): add login" --quiet
  "$SCRIPT_PATH" > /dev/null
  
  content=$(cat CHANGELOG.md)
  if [[ "$content" == *"- add login"* ]]; then
    pass "Scoped commit handling"
  else
    fail "Failed to handle scoped commit"
  fi
}

test_non_conventional() {
  "$SCRIPT_PATH" > /dev/null
  git commit --allow-empty -m "wip: random stuff" --quiet
  "$SCRIPT_PATH" > /dev/null

  content=$(cat CHANGELOG.md)
  if [[ "$content" != *"random stuff"* ]]; then
    pass "Non-conventional commit skipped"
  else
    fail "Failed to skip non-conventional commit"
  fi
}

test_malformed_changelog() {
  # Create a changelog without the proper header
  echo "# Wrong Header" > CHANGELOG.md
  echo "## [1.0.0]" >> CHANGELOG.md

  output=$("$SCRIPT_PATH" 2>&1)
  if [[ $? -eq 1 ]] && [[ "$output" == *"appears malformed"* ]]; then
    pass "Malformed changelog detection"
  else
    fail "Failed to detect malformed changelog"
  fi
}

test_entry_ordering() {
  "$SCRIPT_PATH" > /dev/null

  # Create commits that should be sorted alphabetically
  git commit --allow-empty -m "feat: zebra feature" --quiet
  git commit --allow-empty -m "feat: apple feature" --quiet
  git commit --allow-empty -m "feat: middle feature" --quiet

  "$SCRIPT_PATH" > /dev/null

  content=$(cat CHANGELOG.md)

  # Get line numbers where each feature appears
  apple_line=$(echo "$content" | grep -n "apple feature" | cut -d: -f1)
  middle_line=$(echo "$content" | grep -n "middle feature" | cut -d: -f1)
  zebra_line=$(echo "$content" | grep -n "zebra feature" | cut -d: -f1)

  # Check if apple < middle < zebra (alphabetical order)
  if [[ $apple_line -lt $middle_line ]] && [[ $middle_line -lt $zebra_line ]]; then
    pass "Entry ordering within categories"
  else
    fail "Entries not properly sorted (apple:$apple_line, middle:$middle_line, zebra:$zebra_line)"
  fi
}

test_enhanced_output_messages() {
  "$SCRIPT_PATH" > /dev/null

  git commit --allow-empty -m "feat: new feature" --quiet
  git commit --allow-empty -m "fix: bug fix" --quiet

  output=$("$SCRIPT_PATH")

  if [[ "$output" == *"2 entries"* ]] && [[ "$output" == *"1 Added"* ]] && [[ "$output" == *"1 Fixed"* ]]; then
    pass "Enhanced output messages"
  else
    fail "Output message doesn't contain detailed statistics: $output"
  fi
}

test_gh_issue_format() {
  "$SCRIPT_PATH" > /dev/null

  # Create commits with GH-123 format
  git commit --allow-empty -m "feat: feature A (GH-456)" --quiet
  git commit --allow-empty -m "feat: feature B (GH-456)" --quiet

  "$SCRIPT_PATH" > /dev/null

  # Should deduplicate based on GH-456
  count=$(grep -c "GH-456\|#456" CHANGELOG.md)
  if [[ $count -eq 1 ]]; then
    pass "GH-format issue extraction and deduplication"
  else
    fail "GH-format issue handling failed (found $count occurrences)"
  fi
}

test_verbose_mode() {
  "$SCRIPT_PATH" > /dev/null

  git commit --allow-empty -m "feat: test feature" --quiet

  output=$(VERBOSE=true "$SCRIPT_PATH" 2>&1)

  if [[ "$output" == *"DEBUG:"* ]] && [[ "$output" == *"Processing"* ]]; then
    pass "Verbose mode"
  else
    fail "Verbose mode not working"
  fi
}

test_no_user_facing_changes() {
  "$SCRIPT_PATH" > /dev/null

  # Create only non-user-facing commits
  git commit --allow-empty -m "chore: cleanup" --quiet
  git commit --allow-empty -m "docs: update" --quiet

  output=$("$SCRIPT_PATH")

  if [[ "$output" == *"No user-facing changes"* ]]; then
    pass "No user-facing changes detection"
  else
    fail "Failed to detect when no user-facing changes present"
  fi
}

# --- Run All ---

run_test test_prerequisites_missing_changelog
run_test test_bootstrap_pointer
run_test test_standard_flow
run_test test_deduplication
run_test test_breaking_change
run_test test_no_new_commits
run_test test_corrupted_pointer
run_test test_ignored_types
run_test test_revert_commit
run_test test_conditional_types
run_test test_scoped_commit
run_test test_non_conventional
run_test test_malformed_changelog
run_test test_entry_ordering
run_test test_enhanced_output_messages
run_test test_gh_issue_format
run_test test_verbose_mode
run_test test_no_user_facing_changes

echo "All tests passed."
