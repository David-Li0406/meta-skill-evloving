---
name: screenshot
description: Get the latest screenshot from ShareX and display it in the conversation
user: true
---

# Screenshot - Latest ShareX Screenshot

## Instructions

When the user runs `/screenshot`, you should:

1. Find the latest screenshot from ShareX Screenshots folder:
   ```
   C:\Users\AnveshJarabani\Downloads\sharex\Screenshots
   ```
   WSL path: `/mnt/c/Users/AnveshJarabani/Downloads/sharex/Screenshots`

2. Use the Read tool to display the image in the conversation

3. Show the image filename and timestamp

## Implementation

```bash
# Find latest screenshot (all common image formats)
SHAREX_DIR="/mnt/c/Users/AnveshJarabani/Downloads/sharex/Screenshots"
LATEST=$(find "$SHAREX_DIR" -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" -o -name "*.gif" -o -name "*.bmp" \) -printf '%T@ %p\n' 2>/dev/null | sort -rn | head -1 | cut -d' ' -f2-)

if [ -n "$LATEST" ]; then
    echo "Latest screenshot: $(basename "$LATEST")"
    echo "Created: $(date -r "$LATEST" '+%Y-%m-%d %H:%M:%S')"
    # Then use Read tool to display it
else
    echo "No screenshots found in ShareX folder"
fi
```

## Steps

1. Use Bash to find the latest image file (any format: png, jpg, jpeg, gif, bmp)
2. Show the filename and creation time
3. Use Read tool to display the image (Read supports image files)
4. Ask user if they want to analyze or discuss the screenshot
