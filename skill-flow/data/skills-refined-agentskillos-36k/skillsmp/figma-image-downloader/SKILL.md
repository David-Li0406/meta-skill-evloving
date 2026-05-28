---
name: figma-image-downloader
description: "WHAT: Download screen screenshots from Figma files via bash script. WHEN: extracting visual assets, creating screenshot references, archiving designs. KEYWORDS: figma, download, screenshot, images, frames, png, export, design."
---

# Figma Image Downloader

Download screen screenshots from Figma design files using a bash script.

## When to Use This Skill

Use this skill when:

- Downloading screenshots of mobile screens from Figma
- Creating visual references for implementation
- Extracting screen assets for documentation
- Building screenshot galleries from Figma files
- Testing visual regression against Figma designs
- Archiving design states for version tracking

## Prerequisites

**Required:**
- bash, curl, and jq installed locally
- Figma personal access token

**Environment Variable:**
```bash
export FIGMA_API_KEY="your-figma-personal-access-token"
```

**Obtaining Figma Access Token:**
1. Go to https://www.figma.com/settings (Figma Settings → Account)
2. Scroll to "Personal access tokens" section
3. Click "Generate new token"
4. Give it a name (e.g., "Claude Code")
5. Copy the token and set as FIGMA_API_KEY environment variable

**Quick link:** https://www.figma.com/settings#access-tokens

## How It Works

The script:
1. Extracts file key and node ID from Figma URL
2. Fetches file structure from Figma API
3. Filters for all FRAME nodes
4. Requests high-resolution PNG exports (2x scale)
5. Downloads images to `.devorch/artifacts/figma-screenshots/{fileKey}/`
6. Names files based on Figma frame names (sanitized)

## Usage

### Basic Usage

```bash
# Navigate to your project directory
cd /path/to/your/project

# Run the script with a Figma URL
.claude/skills/figma-dev-mode/figma-image-downloader/scripts/download-figma-images.sh "https://figma.com/design/FILE_KEY/Design-Name?node-id=123-456"
```

### URL Format

The script accepts Figma URLs in these formats:

```
https://figma.com/file/FILE_KEY/Design-Name
https://figma.com/design/FILE_KEY/Design-Name
https://figma.com/design/FILE_KEY/Design-Name?node-id=123-456
```

**node-id parameter (optional):**
- If provided: Downloads screens within that specific node
- If omitted: Downloads from first page in the file

### Example

```bash
# Download all screens from a Figma file
.claude/skills/figma-dev-mode/figma-image-downloader/scripts/download-figma-images.sh \
  "https://figma.com/design/abc123xyz/Mobile-App-Screens?node-id=100-200"
```

**Output:**
```
Found 12 screens
✓ home_screen
✓ profile_screen
✓ settings_screen
...
✅ Downloaded 12 screens to .devorch/artifacts/figma-screenshots/abc123xyz
```

## Output Structure

Images are saved to:
```
.devorch/artifacts/figma-screenshots/
└── {fileKey}/
    ├── home_screen.png
    ├── profile_screen.png
    ├── settings_screen.png
    └── ...
```

**File Naming:**
- Frame names from Figma are sanitized
- Non-alphanumeric characters replaced with underscores
- Converted to lowercase
- Example: "Home / Main Screen" → "home___main_screen.png"

## Screen Detection

The script processes all frames:
- **Detection**: Finds all `FRAME` type nodes
- **No size filtering**: Downloads all screens regardless of dimensions
- **Skips**: Components, groups, and other non-frame node types

## Image Quality

**Resolution:**
- 2x scale for high-resolution exports
- Suitable for retina displays
- Good balance between quality and file size

**Format:**
- PNG format for lossless quality
- Preserves transparency if present in design
- Compatible with all platforms

## Error Handling

### Missing Environment Variable

```
ERROR: Missing FIGMA_API_KEY or URL_ARG argument
```

**Fix:** Set the FIGMA_API_KEY environment variable:
```bash
export FIGMA_API_KEY="your-token-here"
```

### Invalid Figma URL

```
ERROR: Invalid Figma URL
```

**Fix:** Ensure URL contains valid file key:
- Must be `/file/` or `/design/` URL
- Must contain file key segment

### API Error

```
ERROR: API Error: 403
```

**Possible causes:**
- Invalid or expired access token
- File is private and token lacks access
- Token missing required scopes

**Fix:**
- Regenerate Figma access token
- Ensure file is accessible with your account
- Verify token has file read permissions

### Node Not Found

```
ERROR: Node not found
```

**Fix:**
- Verify node-id parameter in URL is correct
- Try omitting node-id to search entire file
- Check if node was deleted or moved in Figma

### No Screens Found

```
ERROR: No screens found
```

**Possible causes:**
- File contains no frames
- Selected node doesn't contain any screens
- Frames are components or other types

**Fix:**
- Check Figma file has frames
- Try different node-id or omit to search entire file
- Verify frames exist in Figma

## Integration with Claude Code

When Claude Code needs to download Figma images:

```markdown
To download screens from the Figma file, I'll use the figma-image-downloader skill.

First, let me extract the file key from the URL you provided: `abc123xyz`

Now I'll run the download script:
```

Then execute:
```bash
.claude/skills/figma-dev-mode/figma-image-downloader/scripts/download-figma-images.sh \
  "https://figma.com/design/abc123xyz/App-Screens"
```

## Common Workflows

### Workflow 1: Download Screens for Implementation Reference

1. Get Figma URL from user or design handoff
2. Ensure FIGMA_API_KEY is set
3. Run script with URL
4. Review downloaded images in `figma-screenshots/{fileKey}/`
5. Use screenshots as visual reference during implementation

### Workflow 2: Extract Screens from Specific Figma Page

1. Open Figma file and navigate to target page
2. Right-click page → Copy link
3. Extract node-id from URL
4. Run script with full URL including node-id
5. Verify only screens from that page were downloaded

### Workflow 3: Archive Design States

1. Run script before starting implementation
2. Commit screenshots to git for version tracking
3. Use for visual regression testing later
4. Compare implementation against archived designs

### Workflow 4: Build Screenshot Documentation

1. Download screens from multiple Figma files
2. Organize by feature or flow
3. Use in design documentation
4. Reference in PRs and specs

## Best Practices

**Set environment variable persistently:**
Add to your shell profile (~/.zshrc, ~/.bashrc):
```bash
export FIGMA_API_KEY="your-token-here"
```

**Organize downloads by spec:**
```bash
# Images are automatically saved to .devorch/artifacts/figma-screenshots/{fileKey}/
# Copy them to spec visuals if needed:
SPEC_NAME="2025-01-10-onboarding-flow"
mkdir -p devorch/specs/$SPEC_NAME/planning/visuals
cp .devorch/artifacts/figma-screenshots/*/*.png devorch/specs/$SPEC_NAME/planning/visuals/
```

**Use in CI/CD pipelines:**
```yaml
# Example GitHub Actions step
- name: Download Figma screenshots
  env:
    FIGMA_API_KEY: ${{ secrets.FIGMA_API_KEY }}
  run: |
    .claude/skills/figma-dev-mode/figma-image-downloader/scripts/download-figma-images.sh \
      "${{ env.FIGMA_DESIGN_URL }}"
```

**Gitignore is already configured:**
The `.devorch/artifacts/` directory is typically already gitignored.

Or commit for version tracking:
```bash
# Commit screenshots for visual regression
git add .devorch/artifacts/figma-screenshots/
git commit -m "docs: add Figma screenshots for feature X"
```

## Comparison with Figma MCP

**Figma MCP (figma-researcher skill):**
- Uses MCP server for structured data extraction
- Gets design tokens, colors, spacing, typography
- Reads component hierarchy and properties
- Requires MCP server installation
- Better for: Design specifications, token mapping

**Figma Image Downloader (this skill):**
- Standalone bash script
- Downloads PNG screenshots
- Downloads all frames
- No MCP server required
- Better for: Visual references, screenshot galleries

**Use both:**
- Use figma-researcher to extract design specs
- Use figma-image-downloader to get visual assets
- Combine for complete design implementation workflow

## Script Reference

**Location:**
`.claude/skills/figma-dev-mode/figma-image-downloader/scripts/download-figma-images.sh`

**Dependencies:**
- bash (standard on macOS/Linux)
- curl (for HTTP requests)
- jq (for JSON parsing)

**API Endpoints Used:**
- `GET https://api.figma.com/v1/files/{fileKey}` - Get file structure
- `GET https://api.figma.com/v1/images/{fileKey}` - Get image export URLs

**Figma API Documentation:**
https://www.figma.com/developers/api

## Troubleshooting

**Script not found:**
```bash
# Verify script location
ls -la .claude/skills/figma-dev-mode/figma-image-downloader/scripts/

# If missing, skill may not be installed
devorch install
```

**Permission denied:**
```bash
# Make script executable
chmod +x .claude/skills/figma-dev-mode/figma-image-downloader/scripts/download-figma-images.sh

# Or run with bash explicitly
bash .claude/skills/figma-dev-mode/figma-image-downloader/scripts/download-figma-images.sh "$URL"
```

**Network timeouts:**
- Large files may take time to process
- Script downloads images sequentially
- Check network connection
- Retry if interrupted

**Rate limiting:**
- Figma API has rate limits
- Script includes no rate limit handling
- For large batches, add delays between files
- Consider using Figma Enterprise for higher limits
