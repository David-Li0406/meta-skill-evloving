#!/bin/bash

# Test suite for remove-empty-headers.sh

# Resolve script path relative to this test file
SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")/../scripts" && pwd)/remove-empty-headers.sh"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

setup() {
  TEST_DIR=$(mktemp -d)
  cd "$TEST_DIR" || exit 1
}

teardown() {
  rm -rf "$TEST_DIR"
}

fail() {
  echo -e "${RED}✗ $1${NC}"
  teardown
  exit 1
}

pass() {
  echo -e "${GREEN}✓ $1${NC}"
}

run_test() {
  setup
  $1
  teardown
}

# =============================================================================
# Core Functionality Tests (5 tests)
# =============================================================================

test_preserves_l1_empty_headers() {
  cat > test.md << 'EOF'
# Empty L1

## Section
content
EOF

  "$SCRIPT_PATH" test.md > /dev/null

  if grep -q "# Empty L1" test.md; then
    pass "Preserves L1 empty headers"
  else
    fail "Failed to preserve L1 empty header"
  fi
}

test_preserves_l2_empty_headers() {
  cat > test.md << 'EOF'
## Empty L2

### Section
content
EOF

  "$SCRIPT_PATH" test.md > /dev/null

  if grep -q "## Empty L2" test.md; then
    pass "Preserves L2 empty headers"
  else
    fail "Failed to preserve L2 empty header"
  fi
}

test_removes_l3_empty_headers() {
  cat > test.md << 'EOF'
### Empty L3

### Content
text
EOF

  "$SCRIPT_PATH" test.md > /dev/null

  if ! grep -q "### Empty L3" test.md && grep -q "### Content" test.md; then
    pass "Removes L3 empty headers"
  else
    fail "Failed to remove L3 empty header or removed content header"
  fi
}

test_removes_l4_l5_l6_empty_headers() {
  cat > test.md << 'EOF'
#### Empty L4

##### Empty L5

###### Empty L6

#### Content L4
text
EOF

  "$SCRIPT_PATH" test.md > /dev/null

  if ! grep -q "#### Empty L4" test.md && \
     ! grep -q "##### Empty L5" test.md && \
     ! grep -q "###### Empty L6" test.md && \
     grep -q "#### Content L4" test.md; then
    pass "Removes L4, L5, L6 empty headers"
  else
    fail "Failed to remove L4/L5/L6 empty headers or removed content header"
  fi
}

test_preserves_headers_with_content() {
  cat > test.md << 'EOF'
# L1 Header
L1 content

## L2 Header
L2 content

### L3 Header
L3 content

#### L4 Header
L4 content

##### L5 Header
L5 content

###### L6 Header
L6 content
EOF

  "$SCRIPT_PATH" test.md > /dev/null

  header_count=$(grep -c "^#" test.md)

  if [ "$header_count" -eq 6 ]; then
    pass "Preserves headers with content"
  else
    fail "Failed to preserve all headers with content (found $header_count, expected 6)"
  fi
}

# =============================================================================
# Edge Case Tests (6 tests)
# =============================================================================

test_consecutive_empty_headers() {
  cat > test.md << 'EOF'
### Empty 1

### Empty 2

### Empty 3

### Content
text
EOF

  "$SCRIPT_PATH" test.md > /dev/null

  if ! grep -q "### Empty 1" test.md && \
     ! grep -q "### Empty 2" test.md && \
     ! grep -q "### Empty 3" test.md && \
     grep -q "### Content" test.md; then
    pass "Consecutive empty headers"
  else
    fail "Failed to remove consecutive empty headers"
  fi
}

test_mixed_empty_and_content() {
  cat > test.md << 'EOF'
### Empty 1

### Content 1
text

### Empty 2

### Content 2
more text
EOF

  "$SCRIPT_PATH" test.md > /dev/null

  if ! grep -q "### Empty 1" test.md && \
     ! grep -q "### Empty 2" test.md && \
     grep -q "### Content 1" test.md && \
     grep -q "### Content 2" test.md; then
    pass "Mixed empty and content"
  else
    fail "Failed to handle mixed empty and content headers"
  fi
}

test_empty_file() {
  touch test.md

  "$SCRIPT_PATH" test.md > /dev/null

  if [ ! -s test.md ]; then
    pass "Empty file"
  else
    fail "Empty file produced unexpected content"
  fi
}

test_no_headers() {
  cat > test.md << 'EOF'
This is just plain text.
No headers here.
Just paragraphs.
EOF

  original_content=$(cat test.md)
  "$SCRIPT_PATH" test.md > /dev/null
  new_content=$(cat test.md)

  if [ "$original_content" = "$new_content" ]; then
    pass "No headers"
  else
    fail "File with no headers was modified"
  fi
}

test_whitespace_only_sections() {
  cat > test.md << 'EOF'
### Empty with whitespace



### Content
text
EOF

  "$SCRIPT_PATH" test.md > /dev/null

  if ! grep -q "### Empty with whitespace" test.md && \
     grep -q "### Content" test.md; then
    pass "Whitespace only sections"
  else
    fail "Failed to treat whitespace-only section as empty"
  fi
}

test_deep_nesting() {
  cat > test.md << 'EOF'
# L1 Empty

# L1 Content
text

## L2 Empty

## L2 Content
text

### L3 Empty

### L3 Content
text

#### L4 Empty

#### L4 Content
text

##### L5 Empty

##### L5 Content
text

###### L6 Empty

###### L6 Content
text
EOF

  "$SCRIPT_PATH" test.md > /dev/null

  # L1 and L2 empties should be preserved
  # L3-L6 empties should be removed
  if grep -q "# L1 Empty" test.md && \
     grep -q "## L2 Empty" test.md && \
     ! grep -q "### L3 Empty" test.md && \
     ! grep -q "#### L4 Empty" test.md && \
     ! grep -q "##### L5 Empty" test.md && \
     ! grep -q "###### L6 Empty" test.md && \
     grep -q "### L3 Content" test.md; then
    pass "Deep nesting"
  else
    fail "Failed to handle deep nesting correctly"
  fi
}

# =============================================================================
# Format Edge Cases (4 tests)
# =============================================================================

test_headers_with_closing_hashes() {
  cat > test.md << 'EOF'
### Empty Header ###

### Content Header ###
text
EOF

  "$SCRIPT_PATH" test.md > /dev/null

  if ! grep -q "### Empty Header ###" test.md && \
     grep -q "### Content Header ###" test.md; then
    pass "Headers with closing hashes"
  else
    fail "Failed to handle headers with closing hashes"
  fi
}

test_headers_in_code_blocks() {
  cat > test.md << 'EOF'
```
### Not a header
This is in a code block
```

### Real Header
content
EOF

  "$SCRIPT_PATH" test.md > /dev/null

  # The script processes all lines with the header pattern
  # Code blocks are preserved as-is
  if grep -q "### Not a header" test.md && \
     grep -q "### Real Header" test.md; then
    pass "Headers in code blocks"
  else
    fail "Failed to preserve code block content"
  fi
}

test_setext_headers() {
  cat > test.md << 'EOF'
Setext Header 1
===============

Setext Header 2
---------------

### ATX Header
content
EOF

  "$SCRIPT_PATH" test.md > /dev/null

  # Setext headers should be preserved (script only handles ATX-style)
  if grep -q "Setext Header 1" test.md && \
     grep -qF "===============" test.md && \
     grep -q "Setext Header 2" test.md && \
     grep -qF -- "---------------" test.md; then
    pass "Setext headers"
  else
    fail "Failed to preserve setext headers"
  fi
}

test_invalid_headers_no_space() {
  cat > test.md << 'EOF'
#NoSpace
###AlsoNoSpace

### Valid Header
content
EOF

  "$SCRIPT_PATH" test.md > /dev/null

  # Invalid headers (no space after #) should be preserved as-is
  if grep -q "#NoSpace" test.md && \
     grep -q "###AlsoNoSpace" test.md && \
     grep -q "### Valid Header" test.md; then
    pass "Invalid headers (no space)"
  else
    fail "Failed to preserve invalid header syntax"
  fi
}

# =============================================================================
# Script Behavior Tests (4 tests)
# =============================================================================

test_multiple_files() {
  cat > test1.md << 'EOF'
### Empty
EOF

  cat > test2.md << 'EOF'
### Empty
EOF

  cat > test3.md << 'EOF'
### Empty
EOF

  output=$("$SCRIPT_PATH" test1.md test2.md test3.md)

  if [[ "$output" == *"test1.md"* ]] && \
     [[ "$output" == *"test2.md"* ]] && \
     [[ "$output" == *"test3.md"* ]]; then
    pass "Multiple files"
  else
    fail "Failed to process multiple files: $output"
  fi
}

test_missing_file() {
  output=$("$SCRIPT_PATH" nonexistent.md 2>&1)

  if [[ "$output" == *"Error: File 'nonexistent.md' not found"* ]]; then
    pass "Missing file"
  else
    fail "Failed to handle missing file correctly: $output"
  fi
}

test_non_markdown_file() {
  touch test.txt

  output=$("$SCRIPT_PATH" test.txt 2>&1)

  if [[ "$output" == *"Warning:"* ]] && [[ "$output" == *"doesn't have .md extension"* ]]; then
    pass "Non-markdown file"
  else
    fail "Failed to warn about non-markdown file: $output"
  fi
}

test_no_arguments() {
  output=$("$SCRIPT_PATH" 2>&1)
  exit_code=$?

  if [[ "$output" == *"Usage:"* ]] && [ $exit_code -eq 1 ]; then
    pass "No arguments"
  else
    fail "Failed to show usage message with no arguments"
  fi
}

# =============================================================================
# Run All Tests
# =============================================================================

run_test test_preserves_l1_empty_headers
run_test test_preserves_l2_empty_headers
run_test test_removes_l3_empty_headers
run_test test_removes_l4_l5_l6_empty_headers
run_test test_preserves_headers_with_content
run_test test_consecutive_empty_headers
run_test test_mixed_empty_and_content
run_test test_empty_file
run_test test_no_headers
run_test test_whitespace_only_sections
run_test test_deep_nesting
run_test test_headers_with_closing_hashes
run_test test_headers_in_code_blocks
run_test test_setext_headers
run_test test_invalid_headers_no_space
run_test test_multiple_files
run_test test_missing_file
run_test test_non_markdown_file
run_test test_no_arguments

echo ""
echo "All tests passed."
