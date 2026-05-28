---
name: extracting-stitch-mockups
description: Use this skill to extract generated mockup images from Google Stitch project pages when provided with a Stitch project URL.
---

# Extract Stitch Mockups

## Quick Start
1. **Get project URL** - User provides `https://stitch.withgoogle.com/projects/{id}`
2. **Resolve feature directory** - Determine where to save using fallback chain
3. **Run extraction process** - Navigate to the URL, take a DOM snapshot, and extract image URLs
4. **Download images** - Save images to `design-intent/google-stitch/{feature}/exports/`

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
- Active Google session in the browser (Chrome or Cursor's built-in browser)
- Required tools: Playwright or MCP browser tools

### Extraction Steps
1. **Navigate to Stitch URL** using the appropriate browser tool
2. **Wait for page load** and check if generation is complete
3. **Take DOM snapshot** and parse for image URLs (`lh3.googleusercontent.com/aida/`)
4. **Download images** using a utility script or direct method
5. **Save images** to `design-intent/google-stitch/{feature}/exports/`

### Image Filtering
- Source: `lh3.googleusercontent.com/aida/...` URLs only
- Size filter: Images with dimensions >= 400px (mockups, not UI elements)
- Excludes: avatars, icons, UI chrome

### Generation Check
- If "Generating..." status is detected, exit with a message to retry after generation completes.

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

- **Not authenticated** - Sign into Google in the browser, then retry
- **Still generating** - Wait for Stitch to complete generation, then retry
- **No images found** - Verify project has completed generating and check snapshot for image elements
- **No feature directory** - Run authoring-stitch-prompts first, or specify `--feature`

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions.

## Reference Files
- [WORKFLOW.md](WORKFLOW.md) - Detailed extraction workflow
- [EXAMPLES.md](EXAMPLES.md) - Sample extractions
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Error handling and common issues