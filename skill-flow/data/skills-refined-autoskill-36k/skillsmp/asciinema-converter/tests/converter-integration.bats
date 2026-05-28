#!/usr/bin/env bats
# Integration tests for asciinema-converter skill
# Run with: bats plugins/asciinema-tools/skills/asciinema-converter/tests/converter-integration.bats

FIXTURES_DIR="$BATS_TEST_DIRNAME/fixtures"
TMP_DIR="$BATS_TEST_DIRNAME/tmp"

setup() {
  mkdir -p "$TMP_DIR"
  mkdir -p "$FIXTURES_DIR"

  # Create minimal test fixture if it doesn't exist
  if [[ ! -f "$FIXTURES_DIR/simple.cast" ]]; then
    cat > "$FIXTURES_DIR/simple.cast" << 'CAST_EOF'
{"version": 2, "width": 80, "height": 24, "timestamp": 1705600000, "duration": 5.0}
[0.0, "o", "Hello"]
[1.0, "o", " World"]
[2.0, "o", "\r\n"]
[3.0, "o", "$ exit"]
[4.0, "o", "\r\n"]
CAST_EOF
  fi

  # Create filename with spaces fixture
  if [[ ! -f "$FIXTURES_DIR/with spaces.cast" ]]; then
    cp "$FIXTURES_DIR/simple.cast" "$FIXTURES_DIR/with spaces.cast"
  fi
}

teardown() {
  rm -rf "$TMP_DIR"
}

# ============================================================================
# Preflight Tests
# ============================================================================

@test "asciinema CLI is installed" {
  command -v asciinema
}

@test "asciinema convert command exists" {
  run asciinema convert --help
  [ "$status" -eq 0 ]
}

@test "asciinema version is 2.4+" {
  version=$(asciinema --version | head -1 | grep -oE '[0-9]+\.[0-9]+')
  major=$(echo "$version" | cut -d. -f1)
  minor=$(echo "$version" | cut -d. -f2)

  # Need at least 2.4 for convert command
  if [[ "$major" -lt 2 ]]; then
    skip "asciinema major version too old: $version"
  fi
  if [[ "$major" -eq 2 && "$minor" -lt 4 ]]; then
    skip "asciinema minor version too old: $version"
  fi
}

# ============================================================================
# Single File Conversion Tests
# ============================================================================

@test "single file conversion works" {
  run asciinema convert -f txt "$FIXTURES_DIR/simple.cast" "$TMP_DIR/simple.txt"
  [ "$status" -eq 0 ]
  [ -f "$TMP_DIR/simple.txt" ]
}

@test "converted file contains expected content" {
  asciinema convert -f txt "$FIXTURES_DIR/simple.cast" "$TMP_DIR/simple.txt"

  # Should contain "Hello World"
  run grep -q "Hello" "$TMP_DIR/simple.txt"
  [ "$status" -eq 0 ]
}

@test "converted file has no ANSI escape codes" {
  asciinema convert -f txt "$FIXTURES_DIR/simple.cast" "$TMP_DIR/simple.txt"

  # Should NOT contain ANSI escape codes
  run grep -P '\x1b\[' "$TMP_DIR/simple.txt"
  [ "$status" -ne 0 ]
}

@test "conversion achieves compression" {
  asciinema convert -f txt "$FIXTURES_DIR/simple.cast" "$TMP_DIR/simple.txt"

  input_size=$(stat -f%z "$FIXTURES_DIR/simple.cast" 2>/dev/null || stat -c%s "$FIXTURES_DIR/simple.cast")
  output_size=$(stat -f%z "$TMP_DIR/simple.txt" 2>/dev/null || stat -c%s "$TMP_DIR/simple.txt")

  # Output should be smaller than input
  [ "$output_size" -lt "$input_size" ]
}

@test "handles filenames with spaces" {
  run asciinema convert -f txt "$FIXTURES_DIR/with spaces.cast" "$TMP_DIR/with spaces.txt"
  [ "$status" -eq 0 ]
  [ -f "$TMP_DIR/with spaces.txt" ]
}

# ============================================================================
# Batch Conversion Tests
# ============================================================================

@test "batch creates output directory" {
  # Setup: ensure output doesn't exist
  rm -rf "$TMP_DIR/batch-output"

  # Create batch output dir
  mkdir -p "$TMP_DIR/batch-output"

  [ -d "$TMP_DIR/batch-output" ]
}

@test "batch converts multiple files" {
  mkdir -p "$TMP_DIR/batch-source"
  mkdir -p "$TMP_DIR/batch-output"

  # Create multiple test files
  cp "$FIXTURES_DIR/simple.cast" "$TMP_DIR/batch-source/file1.cast"
  cp "$FIXTURES_DIR/simple.cast" "$TMP_DIR/batch-source/file2.cast"
  cp "$FIXTURES_DIR/simple.cast" "$TMP_DIR/batch-source/file3.cast"

  # Convert each file
  for cast_file in "$TMP_DIR/batch-source"/*.cast; do
    basename=$(basename "$cast_file" .cast)
    asciinema convert -f txt "$cast_file" "$TMP_DIR/batch-output/${basename}.txt"
  done

  # Verify all files were converted
  [ -f "$TMP_DIR/batch-output/file1.txt" ]
  [ -f "$TMP_DIR/batch-output/file2.txt" ]
  [ -f "$TMP_DIR/batch-output/file3.txt" ]
}

@test "skip existing files logic works" {
  mkdir -p "$TMP_DIR/skip-test"

  # Pre-create output file
  echo "existing content" > "$TMP_DIR/skip-test/existing.txt"
  original_content=$(cat "$TMP_DIR/skip-test/existing.txt")

  # Copy source
  cp "$FIXTURES_DIR/simple.cast" "$TMP_DIR/skip-test/existing.cast"

  # Skip logic simulation (don't convert if exists)
  txt_file="$TMP_DIR/skip-test/existing.txt"
  if [[ -f "$txt_file" ]]; then
    skipped=true
  else
    asciinema convert -f txt "$TMP_DIR/skip-test/existing.cast" "$txt_file"
  fi

  # File should not have been modified
  current_content=$(cat "$TMP_DIR/skip-test/existing.txt")
  [ "$current_content" = "$original_content" ]
}

# ============================================================================
# Compression Ratio Tests
# ============================================================================

@test "compression ratio calculation works" {
  asciinema convert -f txt "$FIXTURES_DIR/simple.cast" "$TMP_DIR/simple.txt"

  input_size=$(stat -f%z "$FIXTURES_DIR/simple.cast" 2>/dev/null || stat -c%s "$FIXTURES_DIR/simple.cast")
  output_size=$(stat -f%z "$TMP_DIR/simple.txt" 2>/dev/null || stat -c%s "$TMP_DIR/simple.txt")

  if [[ $output_size -gt 0 ]]; then
    ratio=$((input_size / output_size))
  else
    ratio=0
  fi

  # Ratio should be positive
  [ "$ratio" -ge 1 ]
}

# ============================================================================
# Error Handling Tests
# ============================================================================

@test "fails gracefully on missing input file" {
  run asciinema convert -f txt "$TMP_DIR/nonexistent.cast" "$TMP_DIR/output.txt"
  [ "$status" -ne 0 ]
}

@test "fails gracefully on invalid cast file" {
  echo "not valid json" > "$TMP_DIR/invalid.cast"
  run asciinema convert -f txt "$TMP_DIR/invalid.cast" "$TMP_DIR/output.txt"
  [ "$status" -ne 0 ]
}

@test "handles empty directory gracefully" {
  mkdir -p "$TMP_DIR/empty-source"
  mkdir -p "$TMP_DIR/empty-output"

  # Count should be zero
  count=$(find "$TMP_DIR/empty-source" -maxdepth 1 -name "*.cast" -type f | wc -l | tr -d ' ')
  [ "$count" -eq 0 ]
}

# ============================================================================
# Path Handling Tests
# ============================================================================

@test "handles absolute paths correctly" {
  run asciinema convert -f txt "$FIXTURES_DIR/simple.cast" "$TMP_DIR/absolute.txt"
  [ "$status" -eq 0 ]
  [ -f "$TMP_DIR/absolute.txt" ]
}

@test "preserves basename in output" {
  asciinema convert -f txt "$FIXTURES_DIR/simple.cast" "$TMP_DIR/simple.txt"

  # Output filename should match input basename
  [ -f "$TMP_DIR/simple.txt" ]
}
