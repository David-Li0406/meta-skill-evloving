---
name: tsan
description: Handle ThreadSanitizer output - redirect to files, summarize races, avoid context flooding
license: MIT
compatibility: opencode
metadata:
  category: testing
  sanitizer: thread
---

# TSAN (ThreadSanitizer) Output Handling

Use this skill when running tests compiled with `-fsanitize=thread` or when encountering ThreadSanitizer output.

## Problem

TSAN produces verbose output (50-100+ lines per race) that can flood context. A test suite might report the same race hundreds of times.

## Quick Reference

### Recommended Test Invocation

```bash
# Always redirect TSAN output to file
TSAN_OPTIONS="log_path=build/tsan.log:halt_on_error=0:history_size=2" ./test_binary

# Then summarize (don't cat the whole file!)
echo "=== TSAN Summary ==="
grep -c "WARNING: ThreadSanitizer" build/tsan.log 2>/dev/null || echo "0 races"
grep -A2 "WARNING: ThreadSanitizer" build/tsan.log | grep "#0" | sort -u | head -10
```

### Stop After First Race (For Debugging)

```bash
TSAN_OPTIONS="halt_on_error=1" ./test_binary
```

### Use Suppressions (For Known Issues)

Create `tsan_suppressions.txt`:
```
# Suppress by function name
race:KnownRacyFunction

# Suppress by file
race:src/legacy/old_code.cc

# Suppress entire library  
called_from_lib:libthirdparty.so

# Suppress by global variable
race:global_counter
```

Run with:
```bash
TSAN_OPTIONS="suppressions=tsan_suppressions.txt" ./test_binary
```

## NEVER Do This

```bash
# WRONG - floods context with potentially thousands of lines
./test_binary 2>&1

# WRONG - still floods context  
./test_binary 2>&1 | head -500  # 500 lines is still too much
```

## Summarizing TSAN Output

After running tests, summarize the log file:

```bash
# Count total races
RACE_COUNT=$(grep -c "WARNING: ThreadSanitizer" build/tsan.log 2>/dev/null || echo "0")
echo "Total TSAN reports: $RACE_COUNT"

# Get unique race locations (first stack frame only)
echo "Unique race locations:"
grep -A3 "WARNING: ThreadSanitizer" build/tsan.log | \
  grep "#0" | \
  sed 's/.*#0 //' | \
  sort | uniq -c | sort -rn | head -10
```

## Creating Issues from TSAN Output

When TSAN reports races, create concise issues:

```bash
ralph issue add "TSAN: data race in Worker::process (src/worker.cc:123)"
```

NOT verbose multi-line descriptions with full stack traces.

## TSAN_OPTIONS Reference

| Option | Value | Effect |
|--------|-------|--------|
| `log_path` | `path/to/file` | Redirect output to file |
| `halt_on_error` | `0` or `1` | Stop after first race |
| `history_size` | `0-7` | Stack trace memory (0=smallest) |
| `suppressions` | `path/to/file` | Suppression rules file |
| `verbosity` | `0-2` | Output verbosity |

Combine with colons:
```bash
TSAN_OPTIONS="log_path=out.log:halt_on_error=1:history_size=2"
```

## Suppression Types

| Type | Matches Against |
|------|-----------------|
| `race` | Function/file in either stack |
| `race_top` | Only top stack frame |
| `thread` | Thread leak reports |
| `mutex` | Locked mutex destruction |
| `signal` | Signal handler issues |
| `deadlock` | Lock inversion reports |
| `called_from_lib` | Calls from specific library |

## Example Workflow

1. **Run tests with output redirected:**
   ```bash
   TSAN_OPTIONS="log_path=build/tsan.log" make test-tsan
   ```

2. **Check if any races found:**
   ```bash
   if grep -q "WARNING: ThreadSanitizer" build/tsan.log; then
     echo "TSAN found issues"
   fi
   ```

3. **Get summary for context:**
   ```bash
   echo "TSAN: $(grep -c 'WARNING: ThreadSanitizer' build/tsan.log 2>/dev/null || echo 0) reports"
   grep -A2 "WARNING: ThreadSanitizer" build/tsan.log | grep "#0" | sort -u | head -5
   ```

4. **For each unique race, either:**
   - Fix it
   - Add to suppressions with bug reference
   - Create issue for later
