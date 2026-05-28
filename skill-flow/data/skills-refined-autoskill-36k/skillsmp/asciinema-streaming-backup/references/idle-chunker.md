# Idle Chunker Script (DEPRECATED)

> **DEPRECATED**: This inline chunker has been superseded by the launchd daemon architecture.
> See [ADR 2025-12-26](/docs/adr/2025-12-26-asciinema-daemon-architecture.md) for rationale.
>
> **Use instead**: `/asciinema-tools:daemon-setup` to configure the background daemon.

---

**Historical Reference**: The following documents the v9.3 inline chunker approach for reference only.

## idle-chunker.sh (LEGACY)

```bash
/usr/bin/env bash << 'PREFLIGHT_EOF'
#!/usr/bin/env bash
# idle-chunker.sh - Creates zstd chunks during recording idle periods
#
# Usage: idle-chunker.sh <cast_file> <recordings_dir> [idle_threshold]
#
# Arguments:
#   cast_file       - Path to the active .cast recording file
#   recordings_dir  - Path to the orphan branch clone (e.g., ~/asciinema_recordings/repo-name)
#   idle_threshold  - Seconds of inactivity before chunking (default: 30)
#
# Environment:
#   CHUNK_PREFIX    - Prefix for chunk filenames (default: chunk)
#   PUSH_ENABLED    - Set to "false" to disable auto-push (default: true)
#   VERBOSE         - Set to "true" for debug output (default: false)

set -euo pipefail

# Arguments
CAST_FILE="${1:?Usage: idle-chunker.sh <cast_file> <recordings_dir> [idle_threshold]}"
RECORDINGS_DIR="${2:?Usage: idle-chunker.sh <cast_file> <recordings_dir> [idle_threshold]}"
IDLE_THRESHOLD="${3:-30}"

# Configuration
CHUNK_PREFIX="${CHUNK_PREFIX:-chunk}"
PUSH_ENABLED="${PUSH_ENABLED:-true}"
VERBOSE="${VERBOSE:-false}"
ZSTD_LEVEL="${ZSTD_LEVEL:-3}"
POLL_INTERVAL="${POLL_INTERVAL:-5}"

# State
last_chunk_pos=0
chunk_count=0

log() {
  echo "[$(date +%H:%M:%S)] $*"
}

debug() {
  [[ "$VERBOSE" == "true" ]] && log "DEBUG: $*"
}

# Validate inputs
if [[ ! -d "$RECORDINGS_DIR" ]]; then
  log "ERROR: Recordings directory not found: $RECORDINGS_DIR"
  exit 1
fi

if [[ ! -d "$RECORDINGS_DIR/chunks" ]]; then
  log "Creating chunks directory..."
  mkdir -p "$RECORDINGS_DIR/chunks"
fi

cd "$RECORDINGS_DIR"

log "Idle chunker started"
log "  Monitoring: $CAST_FILE"
log "  Chunks to: $RECORDINGS_DIR/chunks/"
log "  Idle threshold: ${IDLE_THRESHOLD}s"
log "  Auto-push: $PUSH_ENABLED"
log ""
log "Waiting for recording to start..."

# Wait for file to exist
while [[ ! -f "$CAST_FILE" ]]; do
  sleep 2
done

log "Recording detected, monitoring for idle periods..."

# Get file modification time (cross-platform)
get_mtime() {
  local file="$1"
  if [[ "$(uname)" == "Darwin" ]]; then
    stat -f%m "$file" 2>/dev/null || echo 0
  else
    stat -c%Y "$file" 2>/dev/null || echo 0
  fi
}

# Get file size (cross-platform)
get_size() {
  local file="$1"
  if [[ "$(uname)" == "Darwin" ]]; then
    stat -f%z "$file" 2>/dev/null || echo 0
  else
    stat -c%s "$file" 2>/dev/null || echo 0
  fi
}

# Main loop
while true; do
  # Check if file still exists (recording might have ended)
  if [[ ! -f "$CAST_FILE" ]]; then
    log "Recording file removed, creating final chunk..."
    break
  fi

  # Check idle time
  file_mtime=$(get_mtime "$CAST_FILE")
  now=$(date +%s)
  idle_seconds=$((now - file_mtime))

  debug "Idle: ${idle_seconds}s, Threshold: ${IDLE_THRESHOLD}s"

  if (( idle_seconds >= IDLE_THRESHOLD )); then
    current_size=$(get_size "$CAST_FILE")

    if (( current_size > last_chunk_pos )); then
      chunk_count=$((chunk_count + 1))
      chunk_name="${CHUNK_PREFIX}_$(date +%Y%m%d_%H%M%S)_${chunk_count}.cast"
      new_bytes=$((current_size - last_chunk_pos))

      log "Idle detected (${idle_seconds}s) - creating chunk..."

      # Extract only new bytes since last chunk (no overlap!)
      tail -c +"$((last_chunk_pos + 1))" "$CAST_FILE" > "chunks/$chunk_name"

      # Compress with zstd
      zstd -${ZSTD_LEVEL} --rm "chunks/$chunk_name"

      log "Created: chunks/${chunk_name}.zst (${new_bytes} bytes, chunk #${chunk_count})"

      # Push to GitHub
      if [[ "$PUSH_ENABLED" == "true" ]]; then
        if git add chunks/ && git commit -m "chunk #${chunk_count}: $(date +%H:%M)" 2>/dev/null; then
          if git push 2>/dev/null; then
            log "Pushed to GitHub"
          else
            log "WARNING: Push failed (will retry next chunk)"
          fi
        fi
      fi

      # Update position tracker
      last_chunk_pos=$current_size

      # Reset idle detection (wait for new content)
      sleep $POLL_INTERVAL
    fi
  fi

  sleep $POLL_INTERVAL
done

# Final chunk if there's remaining data
if [[ -f "$CAST_FILE" ]]; then
  current_size=$(get_size "$CAST_FILE")
  if (( current_size > last_chunk_pos )); then
    chunk_count=$((chunk_count + 1))
    chunk_name="${CHUNK_PREFIX}_$(date +%Y%m%d_%H%M%S)_final.cast"

    tail -c +"$((last_chunk_pos + 1))" "$CAST_FILE" > "chunks/$chunk_name"
    zstd -${ZSTD_LEVEL} --rm "chunks/$chunk_name"

    log "Created final chunk: chunks/${chunk_name}.zst"

    if [[ "$PUSH_ENABLED" == "true" ]]; then
      git add chunks/ && git commit -m "chunk #${chunk_count}: final" && git push
      log "Pushed final chunk to GitHub"
    fi
  fi
fi

log "Idle chunker finished (${chunk_count} chunks created)"
PREFLIGHT_EOF
```

## Usage Examples

### Basic Usage

```bash
# Start recording in terminal 1
asciinema rec ~/project/tmp/session.cast

# Start chunker in terminal 2
~/asciinema_recordings/my-repo/idle-chunker.sh ~/project/tmp/session.cast ~/asciinema_recordings/my-repo
```

### With Custom Threshold

```bash
# Chunk after 15 seconds of idle (more frequent)
idle-chunker.sh session.cast ~/asciinema_recordings/repo 15

# Chunk after 60 seconds of idle (less frequent)
idle-chunker.sh session.cast ~/asciinema_recordings/repo 60
```

### Debug Mode

```bash
VERBOSE=true idle-chunker.sh session.cast ~/asciinema_recordings/repo
```

### Disable Auto-Push (Manual Control)

```bash
PUSH_ENABLED=false idle-chunker.sh session.cast ~/asciinema_recordings/repo

# Push manually when ready
cd ~/asciinema_recordings/repo && git push
```

## How It Works

1. **File Monitoring**: Watches the .cast file's modification time
2. **Idle Detection**: When file hasn't been modified for `IDLE_THRESHOLD` seconds
3. **Chunk Extraction**: Uses `tail -c +N` to extract only new bytes (no overlap)
4. **Compression**: zstd -3 provides ~10x compression with speed
5. **Git Push**: Commits and pushes to orphan branch
6. **Position Tracking**: Remembers last chunk position to avoid duplication

## Key Design: No Overlap

The script tracks `last_chunk_pos` to ensure chunks are **sequential, not overlapping**:

```
File:     [AAAAAABBBBBBCCCCCC]
           ^     ^     ^
Chunk 1:  [AAAAAA]     (bytes 0-5)
Chunk 2:        [BBBBBB]     (bytes 6-11)
Chunk 3:              [CCCCCC] (bytes 12-17)
```

This allows zstd concatenation to work correctly:

```bash
cat chunk_1.zst chunk_2.zst chunk_3.zst > combined.zst
zstd -d combined.zst  # Produces original file
```
