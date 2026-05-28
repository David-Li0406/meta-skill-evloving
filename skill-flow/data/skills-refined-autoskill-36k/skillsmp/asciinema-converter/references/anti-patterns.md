# Anti-Patterns in asciinema Conversion

Common mistakes and their remediation when converting .cast files to .txt.

## Wrong Format Flag

### Problem

Using `-f raw` instead of `-f txt` produces NDJSON output, not clean text.

```bash
# WRONG: Raw format preserves ANSI codes
asciinema convert -f raw input.cast output.txt  # Still has ANSI!

# CORRECT: Text format strips ANSI
asciinema convert -f txt input.cast output.txt
```

### Impact

- ANSI escape sequences bloat file size
- Claude Code Read/Grep tools see garbage characters
- Compression ratio significantly worse (~10:1 vs ~950:1)

### Detection

```bash
# Check for ANSI escape codes in output
grep -P '\x1b\[' output.txt && echo "ERROR: ANSI codes present"
```

---

## Memory Issues with Large Files

### Problem

Files >1GB can cause memory exhaustion during conversion.

### Symptoms

- `asciinema convert` hangs or crashes
- System becomes unresponsive
- Error: "MemoryError" or "Killed"

### Impact

- ~5% of iTerm2 auto-logged sessions exceed 1GB
- Typical 8-hour coding session: 200MB-500MB
- 24-hour sessions or high output: 1-4GB

### Remediation

```bash
# Check file size before conversion
file_size=$(stat -f%z "$cast_file" 2>/dev/null || stat -c%s "$cast_file")
if [[ $file_size -gt 1073741824 ]]; then  # 1GB
  echo "WARNING: File >1GB, may cause memory issues"
  # Consider splitting or streaming approach
fi
```

### Workaround for Large Files

```bash
# Stream-process large files (experimental)
tail -n +2 large.cast | jq -r '.[2]' | \
  sed 's/\x1b\[[0-9;]*[a-zA-Z]//g' > output.txt
```

---

## Path Handling Issues

### Problem

Filenames with spaces, special characters, or Unicode cause failures.

### Common Failures

```bash
# WRONG: Unquoted paths fail with spaces
asciinema convert $FILE output.txt  # Fails if path has spaces

# WRONG: Glob patterns expand unexpectedly
for f in *.cast; do  # Fails if no .cast files exist
```

### Correct Handling

```bash
# ALWAYS quote paths
asciinema convert "$cast_file" "$txt_file"

# Guard against empty globs
shopt -s nullglob
for cast_file in "$SOURCE_DIR"/*.cast; do
  [[ -f "$cast_file" ]] || continue
  # ...
done
```

### iTerm2 Filename Gotcha

iTerm2 profile names can contain dots and spaces:

- `Claude Code` → spaces
- `my.profile.name` → dots look like extensions

```
# This filename has profile "Claude Code" with spaces
20260118_232025.Claude Code.w0t1p1.UUID.pid.id.cast
```

---

## Missing Preflight Check

### Problem

Running conversion without verifying asciinema is installed or supports convert.

### Symptoms

- `command not found: asciinema`
- `Error: Unknown command 'convert'` (old asciinema version)

### Remediation

**Always run preflight before conversion**:

```bash
# Check asciinema exists and convert command works
if ! command -v asciinema &>/dev/null; then
  echo "ERROR: asciinema not installed"
  exit 1
fi

if ! asciinema convert --help &>/dev/null 2>&1; then
  echo "ERROR: asciinema convert not available (need v2.4+)"
  exit 1
fi
```

---

## Re-Converting Unchanged Files

### Problem

Batch conversion without skip logic wastes CPU on already-converted files.

### Impact

- 2400 files × 5 seconds = 3.3 hours wasted
- Disk I/O thrashing
- Repeated compression calculations

### Remediation

**Always use skip-existing logic**:

```bash
txt_file="$OUTPUT_DIR/${basename}.txt"

# Skip if already converted
if [[ -f "$txt_file" ]]; then
  echo "SKIP: $basename (already exists)"
  ((skipped++))
  continue
fi
```

### Advanced: Size-Based Invalidation

```bash
# Re-convert if source is newer or larger
cast_mtime=$(stat -f%m "$cast_file" 2>/dev/null)
txt_mtime=$(stat -f%m "$txt_file" 2>/dev/null)

if [[ -f "$txt_file" && "$txt_mtime" -gt "$cast_mtime" ]]; then
  echo "SKIP: $basename (up to date)"
  continue
fi
```

---

## Mixing Batch and Single Mode

### Problem

Using both positional `file` argument and `--batch` flag causes undefined behavior.

### Example

```bash
# UNDEFINED: What should this do?
/asciinema-tools:convert session.cast --batch
```

### Remediation

**Mutual exclusivity check**:

```bash
if [[ -n "$FILE" && "$BATCH_MODE" == "true" ]]; then
  echo "ERROR: Cannot use both file argument and --batch"
  echo "Use: /asciinema-tools:convert FILE           # Single file"
  echo "Or:  /asciinema-tools:convert --batch        # Directory"
  exit 1
fi
```

---

## Ignoring Conversion Failures

### Problem

Silent failures in batch mode leave partially converted directories.

### Symptoms

- Missing .txt files for some .cast files
- No error log
- Inconsistent output directory

### Remediation

**Track and report failures**:

```bash
failed=0
failed_files=()

for cast_file in "$SOURCE_DIR"/*.cast; do
  if ! asciinema convert -f txt "$cast_file" "$txt_file" 2>/dev/null; then
    echo "FAIL: $basename"
    ((failed++))
    failed_files+=("$basename")
  fi
done

# Report failures at end
if [[ $failed -gt 0 ]]; then
  echo ""
  echo "=== FAILED FILES ==="
  printf '%s\n' "${failed_files[@]}"
fi
```

---

## Checklist

Before running conversions:

- [ ] Preflight check passed (asciinema installed, convert available)
- [ ] Using `-f txt` format flag
- [ ] All paths are quoted
- [ ] Skip-existing logic enabled for batch
- [ ] Large file warning for >1GB files
- [ ] Failure tracking enabled

---

## Related

- [Batch Processing](./batch-processing.md) - Patterns for bulk conversion
- [Integration Guide](./integration-guide.md) - Chaining with analyze
