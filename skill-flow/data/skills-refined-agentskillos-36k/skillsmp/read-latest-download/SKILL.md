---
name: read-latest-download
description: Read the latest file from the Downloads folder
user: true
---

# Read Latest Download

## Instructions

When the user runs `/read-latest-download` or mentions "latest download" or "latest file from downloads", you should:

1. Find the most recently modified file in the Downloads folder
2. Check file size and type
3. Read the file content appropriately based on type

## Implementation

### Find Latest Download

```bash
# Find latest file in Downloads folder (excluding directories)
DOWNLOADS_DIR="/mnt/c/users/anveshjarabani/downloads"
LATEST=$(find "$DOWNLOADS_DIR" -maxdepth 1 -type f -printf '%T@ %p\n' 2>/dev/null | sort -rn | head -1 | cut -d' ' -f2-)

if [ -n "$LATEST" ]; then
    echo "Latest file: $(basename "$LATEST")"
    echo "Modified: $(date -r "$LATEST" '+%Y-%m-%d %H:%M:%S')"
    echo "Size: $(du -h "$LATEST" | cut -f1)"
    echo "Path: $LATEST"
else
    echo "No files found in Downloads folder"
fi
```

### Handle Different File Types

- **Text files (.txt, .md, .log)**: Use Read tool directly
- **Large files (>256KB)**: Use Grep to search or Read with offset/limit
- **Images (.png, .jpg, .gif)**: Use Read tool (supports images)
- **PDFs (.pdf)**: Use Read tool (supports PDFs)
- **Code files (.py, .js, .sh, etc.)**: Use Read tool
- **Binary files**: Show file info, ask user what to do

## Steps

1. **Find latest file**:
   ```bash
   bash -c 'ls -lt /mnt/c/users/anveshjarabani/downloads/*.* 2>/dev/null | head -5'
   ```

2. **Check file size**:
   - If < 256KB: Read entire file
   - If > 256KB: Warn user and ask if they want to:
     - Search for specific content (Grep)
     - Read specific portion (Read with offset/limit)
     - Get summary of first/last lines

3. **Read the file**:
   - Use Read tool for text/images/PDFs
   - For large text files, use Grep to search or Read with parameters

4. **Handle errors gracefully**:
   - File too large: Offer alternatives
   - Binary file: Show metadata, offer to search for text patterns
   - Permission denied: Inform user

## Example Usage

**User**: "Read latest download"

**Assistant**:
1. Uses Bash to find latest file
2. Shows filename, size, timestamp
3. Reads content with appropriate tool
4. If errors (e.g., "latest.txt" in your case had terraform errors), extracts relevant information

## Special Cases

### Terraform Plan Output
If the latest file contains terraform output:
- Use Grep to find errors: `grep -i "error\|failed\|exception"`
- Use Grep with context: `grep -B 5 -A 5 "Error:"`
- Extract specific resource errors

### Log Files
- Show summary stats (lines, file size)
- Offer to grep for ERROR, WARN, INFO
- Show last N lines by default

### Large JSON/YAML
- Parse and show structure
- Offer to extract specific keys
- Use Grep for specific values
