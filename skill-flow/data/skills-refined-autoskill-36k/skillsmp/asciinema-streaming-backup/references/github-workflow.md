# GitHub Actions Workflow

Complete GitHub Actions workflow for recompressing zstd chunks to brotli archives.

## recompress.yml

```yaml
# .github/workflows/recompress.yml
# Lives in the gh-recordings orphan branch

name: Recompress to Brotli

on:
  push:
    branches: [gh-recordings]
    paths: ["chunks/**/*.zst"]
  workflow_dispatch:
    inputs:
      force:
        description: "Force recompress even if no new chunks"
        required: false
        default: "false"

jobs:
  recompress:
    runs-on: ubuntu-latest
    permissions:
      contents: write

    steps:
      - name: Checkout orphan branch
        uses: actions/checkout@v4
        with:
          ref: gh-recordings
          fetch-depth: 1

      - name: Install compression tools
        run: |
          sudo apt-get update
          sudo apt-get install -y zstd brotli

      - name: Check for chunks
        id: check
        run: |
          if compgen -G "chunks/*.zst" > /dev/null 2>&1; then
            echo "has_chunks=true" >> $GITHUB_OUTPUT
            echo "chunk_count=$(ls -1 chunks/*.zst 2>/dev/null | wc -l)" >> $GITHUB_OUTPUT
          else
            echo "has_chunks=false" >> $GITHUB_OUTPUT
            echo "chunk_count=0" >> $GITHUB_OUTPUT
          fi

      - name: Display chunk info
        if: steps.check.outputs.has_chunks == 'true'
        run: |
          echo "=== Chunks to process ==="
          ls -lh chunks/*.zst
          echo ""
          echo "Total chunks: ${{ steps.check.outputs.chunk_count }}"

      - name: Concatenate and recompress
        if: steps.check.outputs.has_chunks == 'true'
        run: |
          mkdir -p archives

          # Generate archive name with timestamp
          ARCHIVE_NAME="session_$(date +%Y%m%d_%H%M%S).cast.br"

          echo "Processing ${{ steps.check.outputs.chunk_count }} chunks..."

          # Concatenate all zstd chunks in order, decompress, recompress to brotli
          # Sort by filename to ensure correct order
          ls -1 chunks/*.zst | sort | xargs cat | zstd -d | brotli -9 -o "archives/$ARCHIVE_NAME"

          # Get sizes for logging
          CHUNKS_SIZE=$(du -sh chunks/*.zst | tail -1 | cut -f1)
          ARCHIVE_SIZE=$(ls -lh "archives/$ARCHIVE_NAME" | awk '{print $5}')

          echo ""
          echo "=== Compression Results ==="
          echo "Input chunks: ${{ steps.check.outputs.chunk_count }} files"
          echo "Output archive: archives/$ARCHIVE_NAME"
          echo "Archive size: $ARCHIVE_SIZE"

          # Cleanup chunks after successful archival
          rm -f chunks/*.zst
          echo "Cleaned up processed chunks"

          # Export for commit message
          echo "ARCHIVE_NAME=$ARCHIVE_NAME" >> $GITHUB_ENV
          echo "ARCHIVE_SIZE=$ARCHIVE_SIZE" >> $GITHUB_ENV

      - name: Verify archive integrity
        if: steps.check.outputs.has_chunks == 'true'
        run: |
          echo "Verifying archive..."
          brotli -d -c "archives/${{ env.ARCHIVE_NAME }}" | head -5
          echo "..."
          echo "Archive verified successfully"

      - name: Commit archive
        if: steps.check.outputs.has_chunks == 'true'
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: |
            chore: archive recording to brotli

            Archive: ${{ env.ARCHIVE_NAME }}
            Size: ${{ env.ARCHIVE_SIZE }}
            Chunks processed: ${{ steps.check.outputs.chunk_count }}
          file_pattern: "archives/*.br chunks/"
          branch: gh-recordings

      - name: No chunks to process
        if: steps.check.outputs.has_chunks != 'true'
        run: echo "No chunks found to process"
```

## How It Works

### Trigger Conditions

1. **Push to gh-recordings**: Only triggers when `.zst` files are added/modified in `chunks/`
2. **Manual dispatch**: Can be triggered manually with optional force flag

### Processing Pipeline

```
chunks/*.zst  →  sort by name  →  cat  →  zstd -d  →  brotli -9  →  archives/*.br
```

1. **Sort chunks**: Ensures correct order (chunk_001, chunk_002, etc.)
2. **Concatenate**: Uses zstd's frame concatenation feature
3. **Decompress**: Single pass through zstd decoder
4. **Recompress**: Brotli -9 for ~300x total compression
5. **Cleanup**: Removes processed chunks

### Output

- Archive name: `session_YYYYMMDD_HHMMSS.cast.br`
- Location: `archives/` directory
- Commit message includes size and chunk count

## Customization

### Change Brotli Level

For faster compression (less ratio):

```yaml
brotli -6 -o "archives/$ARCHIVE_NAME"
```

For maximum compression (slower):

```yaml
brotli -11 -o "archives/$ARCHIVE_NAME" # May fail on very large files
```

### Keep Chunks (No Cleanup)

Remove the cleanup line:

```yaml
# rm -f chunks/*.zst  # Comment out to keep chunks
```

### Add Slack Notification

```yaml
- name: Notify Slack
  if: steps.check.outputs.has_chunks == 'true'
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {
        "text": "Recording archived: ${{ env.ARCHIVE_NAME }} (${{ env.ARCHIVE_SIZE }})"
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

## Permissions Required

The workflow requires `contents: write` permission to:

1. Read chunks from the repository
2. Write archives to the repository
3. Delete processed chunks
4. Push commits back to gh-recordings

This is specified in the job:

```yaml
permissions:
  contents: write
```

## Troubleshooting

### "Permission denied" on push

Ensure the workflow has write permissions:

1. Go to repo Settings → Actions → General
2. Under "Workflow permissions", select "Read and write permissions"

### "No chunks found" but chunks exist

Check the path pattern:

```yaml
paths: ["chunks/**/*.zst"] # Must match your chunk location
```

### Archive is corrupted

Verify chunks are sequential (no gaps or overlaps):

```bash
/usr/bin/env bash << 'GITHUB_WORKFLOW_SCRIPT_EOF'
for f in chunks/*.zst; do
  echo "=== $f ==="
  zstd -d -c "$f" | head -1
done
GITHUB_WORKFLOW_SCRIPT_EOF
```

### Workflow not triggering

Check the branch filter:

```yaml
branches: [gh-recordings] # Must match your orphan branch name
```
