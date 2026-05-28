---
name: linear-uploads
description: Download attachments and images from Linear issues. Use when fetching screenshots, images, or file attachments from Linear comments or descriptions.
allowed-tools: Bash(linear-cli:*)
---

# Linear Uploads

Download attachments and images from Linear issues using `linear-cli`.

## Download to File

```bash
# Download image/attachment to file
linear-cli up fetch "https://uploads.linear.app/..." -f image.png

# Download screenshot
linear-cli up fetch "https://uploads.linear.app/abc/def/screenshot.png" -f /tmp/screenshot.png
```

## Output to Stdout

```bash
# Pipe to other tools
linear-cli up fetch "https://uploads.linear.app/..." | base64

# Pipe to file
linear-cli up fetch "https://uploads.linear.app/..." > file.png
```

## Finding Upload URLs

Upload URLs are found in:
- Issue descriptions
- Comments (use `linear-cli cm list ISSUE_ID --output json`)

URLs follow pattern: `https://uploads.linear.app/{org}/{upload}/{filename}`

## When to Use Each Mode

**Use `-f` (file) when Claude needs to view the image:**
```bash
# Download to /tmp, then use Read tool to view
linear-cli up fetch "https://uploads.linear.app/..." -f /tmp/screenshot.png
# Then: Read tool on /tmp/screenshot.png (Claude is multimodal)
```

**Use stdout when piping to other CLI tools:**
```bash
# Pipe to base64, imagemagick, etc.
linear-cli up fetch "https://uploads.linear.app/..." | base64
```

## Tips

- Requires valid Linear API key
- Use `-f` to specify output filename
- Without `-f`, outputs raw bytes to stdout
- Claude cannot interpret raw stdout bytes—always use `-f` + Read tool to view images
