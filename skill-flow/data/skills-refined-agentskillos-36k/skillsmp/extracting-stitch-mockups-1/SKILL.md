---
name: extracting-stitch-mockups
description: >
  Extracts generated mockup images from Google Stitch project pages.
  Use when user provides a Stitch project URL (stitch.withgoogle.com/projects/...),
  mentions extracting/downloading Stitch mockups, saving Stitch designs, or wants to
  archive generated design assets. Uses Cursor's built-in browser (MCP browser tools).
allowed-tools: Read, Write, Bash, Grep, Glob, Browser
---

# Extract Stitch Mockups

## Quick Start
1. **Get project URL** - User provides `https://stitch.withgoogle.com/projects/{id}`
2. **Navigate to URL** - Use Cursor's built-in browser (`mcp_cursor-ide-browser_browser_navigate`)
3. **Extract image URLs** - Get snapshot and parse DOM for image URLs (`lh3.googleusercontent.com/aida/`)
4. **Download images** - Use `urllib.request` or utility script to download images
5. **Save to exports** - Images saved to `design-intent/google-stitch/{feature}/exports/`

---

## Feature Directory Resolution

Determine target feature directory using this fallback chain:

1. **User specifies** - Optional `--feature` argument provided
2. **Auto-detect** - Match Stitch project title to existing `design-intent/google-stitch/{feature}/` directories
3. **Prompt user** - List existing directories and ask user to select or create new

### Auto-Detection Logic
- Extract project title from Stitch page (e.g., "Eco-Travel Home Screen")
- Normalize to feature format: lowercase, hyphens, strip special chars
- Search for matching directory in `design-intent/google-stitch/`
- If multiple partial matches, prompt user to select

---

## Extraction Process

### Prerequisites
- Cursor IDE with built-in browser (MCP browser tools)
- Active Google session in Cursor's browser

### Extraction Steps

1. **Navigate to Stitch URL** using `mcp_cursor-ide-browser_browser_navigate`
2. **Wait for page load** and check if generation is complete
3. **Take DOM snapshot** using `mcp_cursor-ide-browser_browser_snapshot`
4. **Parse snapshot** to find `<img>` elements with `src` containing `lh3.googleusercontent.com/aida/`
5. **Extract image URLs** from the parsed snapshot
6. **Download images** using `urllib.request.urlretrieve()` or the utility script
7. **Save images** to `design-intent/google-stitch/{feature}/exports/`

### Utility Script (Optional)

The Python script provides utility functions for directory resolution and downloading:

```python
from extract_images import resolve_output_dir, download_images

# Resolve output directory
output_dir = resolve_output_dir(project_title="My Project", feature="dashboard")

# Download images
saved_files = download_images(image_urls=["url1", "url2"], output_dir=output_dir)
```

### Image Filtering
- Source: `lh3.googleusercontent.com/aida/...` URLs only
- Size filter: Images with dimensions >= 400px (mockups, not UI elements)
- Excludes: avatars, icons, UI chrome

### Generation Check
Script checks for "Generating..." status on page:
- If detected: Exit with message to retry after generation completes
- If complete: Proceed with extraction

---

## Output Structure

Images saved to existing feature's `exports/` directory:

```
design-intent/google-stitch/{feature}/exports/
├── mockup-1.png
├── mockup-2.png
└── mockup-N.png
```

### File Naming
- Sequential numbering: `mockup-{index}.png`
- Index starts at 1
- Preserves original image format (typically PNG)

---

## Report

After extraction, display summary:

```
Extracted {N} mockups from Stitch project

Project: {project-title}
URL: {project-url}

Saved to: design-intent/google-stitch/{feature}/exports/
  - mockup-1.png (400x800)
  - mockup-2.png (400x800)
  - ...

Feature directory:
  design-intent/google-stitch/{feature}/
  ├── prompt-v{N}.md
  ├── exports/          <- Mockups saved here
  │   ├── mockup-1.png
  │   └── mockup-2.png
  └── wireframes/
```

---

## Common Issues

- **Not authenticated** - Sign into Google in Cursor's browser, then retry
- **Still generating** - Wait for Stitch to complete generation, then retry
- **No images found** - Verify project has completed generating and check snapshot for image elements
- **No feature directory** - Run authoring-stitch-prompts first, or specify feature directory

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions.

## Reference Files
- [WORKFLOW.md](WORKFLOW.md) - Detailed extraction workflow using MCP browser tools
- [EXAMPLES.md](EXAMPLES.md) - Sample extractions
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Error handling and common issues
