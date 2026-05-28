# Batch Processing Patterns

Patterns and best practices for bulk conversion of .cast files.

## Directory Organization

### Recommended Structure

```
~/Downloads/cast-txt/           # Default output directory
├── 20260118_232025.Claude Code.w0t1p1.*.txt
├── 20260118_235012.Claude Code.w0t2p1.*.txt
└── ...
```

### Alternative: Date-Based Hierarchy

For archives with thousands of files:

```
~/.local/share/asciinema-txt/
├── 2026/
│   ├── 01/
│   │   ├── 18/
│   │   │   ├── session-001.txt
│   │   │   └── session-002.txt
│   │   └── 19/
│   └── 02/
└── 2025/
```

### Source Directories

| Directory         | Purpose                     | Notes                           |
| ----------------- | --------------------------- | ------------------------------- |
| `~/asciinemalogs` | iTerm2 auto-logged (future) | Default when configured         |
| `~/Downloads`     | Manual downloads            | Fallback if asciinemalogs empty |
| `${PWD}`          | Current project             | For project-specific recordings |

---

## Skip/Resume Logic

### Basic Skip (Default)

Skip files that already have corresponding .txt:

```bash
txt_file="$OUTPUT_DIR/${basename}.txt"

if [[ -f "$txt_file" ]]; then
  echo "SKIP: $basename (already exists)"
  ((skipped++))
  continue
fi
```

### Timestamp-Based Invalidation

Re-convert if source is newer:

```bash
cast_mtime=$(stat -f%m "$cast_file" 2>/dev/null)
txt_mtime=$(stat -f%m "$txt_file" 2>/dev/null || echo 0)

if [[ -f "$txt_file" && "$txt_mtime" -ge "$cast_mtime" ]]; then
  echo "SKIP: $basename (up to date)"
  continue
fi
```

### Force Re-Convert

Disable skip logic with `--skip-existing=false`:

```bash
if [[ "$SKIP_EXISTING" != "false" && -f "$txt_file" ]]; then
  echo "SKIP: $basename"
  continue
fi
```

---

## Progress Reporting

### Per-File Progress

```bash
echo "[$current/$total] Converting: $basename"
```

### Aggregate Summary

```bash
echo ""
echo "=== Batch Complete ==="
echo "Converted: $converted"
echo "Skipped:   $skipped"
echo "Failed:    $failed"
echo "Total:     $total"
```

### Compression Ratio Reporting

```bash
# Per-file ratio
ratio=$((input_size / output_size))
echo "OK: $basename (${ratio}:1)"

# Aggregate ratio
if [[ $total_output_size -gt 0 ]]; then
  overall_ratio=$((total_input_size / total_output_size))
  echo "Overall compression: ${overall_ratio}:1"
fi
```

---

## Handling 1000+ Files

### Memory-Efficient Iteration

Avoid loading all filenames into memory:

```bash
# WRONG: Loads all names into array
files=($(find . -name "*.cast"))

# CORRECT: Stream processing
find "$SOURCE_DIR" -maxdepth 1 -name "*.cast" -type f | while read -r cast_file; do
  # Process one at a time
done
```

### Size-Tiered Processing

Process largest files first to identify memory issues early:

```bash
# Sort by size descending, process largest first
find "$SOURCE_DIR" -maxdepth 1 -name "*.cast" -type f -print0 | \
  xargs -0 ls -S | while read -r cast_file; do
    # Largest files first
done
```

### Parallel Processing (Advanced)

Use GNU parallel for multi-core conversion:

```bash
# Requires: brew install parallel
find "$SOURCE_DIR" -name "*.cast" | \
  parallel -j4 'asciinema convert -f txt {} {.}.txt'
```

**Caution**: Monitor memory usage with parallel conversion of large files.

---

## iTerm2 Auto-Log Filename Parsing

### Filename Format

```
{creationTimeString}.{profileName}.{termid}.{iterm2.pid}.{autoLogId}.cast
```

### Example

```
20260118_232025.Claude Code.w0t1p1.70C05103-2F29-4B42-8067-BE475DB6126A.68721.4013739999.cast
```

### Component Extraction

Parse from right to left (most reliable):

```bash
filename="20260118_232025.Claude Code.w0t1p1.70C05103-2F29-4B42-8067-BE475DB6126A.68721.4013739999.cast"

# Remove .cast extension
base="${filename%.cast}"

# Extract autoLogId (last component)
autoLogId="${base##*.}"
base="${base%.*}"

# Extract pid
pid="${base##*.}"
base="${base%.*}"

# Extract UUID (contains hyphens)
uuid="${base##*.}"
base="${base%.*}"

# Extract termid (w#t#p# format)
termid="${base##*.}"
base="${base%.*}"

# Remaining is: creationTimeString.profileName
# Profile name can have dots, so extract timestamp first
timestamp="${base%%.*}"
profileName="${base#*.}"
```

### Metadata Extraction

```bash
# Parse creation timestamp
timestamp="20260118_232025"
date="${timestamp:0:8}"      # 20260118
time="${timestamp:9:6}"      # 232025
year="${date:0:4}"           # 2026
month="${date:4:2}"          # 01
day="${date:6:2}"            # 18
```

---

## Error Handling

### Allow-on-Error Semantics

Continue batch even when individual files fail:

```bash
for cast_file in "$SOURCE_DIR"/*.cast; do
  if ! asciinema convert -f txt "$cast_file" "$txt_file" 2>/dev/null; then
    echo "FAIL: $basename"
    ((failed++))
    failed_files+=("$cast_file")
    continue  # Don't abort batch
  fi
done
```

### Error Log

Write failures to log file:

```bash
ERROR_LOG="$OUTPUT_DIR/.conversion-errors.log"

if ! asciinema convert -f txt "$cast_file" "$txt_file" 2>>"$ERROR_LOG"; then
  echo "FAIL: $basename (see $ERROR_LOG)"
fi
```

### Post-Batch Summary

```bash
if [[ $failed -gt 0 ]]; then
  echo ""
  echo "=== FAILED FILES ($failed) ==="
  printf '%s\n' "${failed_files[@]}"
  echo ""
  echo "Re-run failed files:"
  echo "for f in ${failed_files[*]}; do asciinema convert -f txt \"\$f\" \"${OUTPUT_DIR}/\$(basename \"\$f\" .cast).txt\"; done"
fi
```

---

## Performance Benchmarks

### Typical Conversion Speeds

| File Size | Duration    | Compression | Notes                  |
| --------- | ----------- | ----------- | ---------------------- |
| 10MB      | ~1 second   | ~100:1      | Short session          |
| 100MB     | ~5 seconds  | ~500:1      | Typical 2-hour session |
| 500MB     | ~20 seconds | ~800:1      | Full day session       |
| 1GB       | ~45 seconds | ~900:1      | Extended session       |
| 4GB       | ~3 minutes  | ~950:1      | Maximum observed       |

### Batch Estimates

| Files | Avg Size | Est. Time   | Notes                    |
| ----- | -------- | ----------- | ------------------------ |
| 100   | 50MB     | ~2 minutes  | Daily batch              |
| 500   | 100MB    | ~15 minutes | Weekly cleanup           |
| 2400  | 150MB    | ~1 hour     | Full archive (skip mode) |

---

## Related

- [Anti-Patterns](./anti-patterns.md) - Common mistakes to avoid
- [Integration Guide](./integration-guide.md) - Chaining with analyze
