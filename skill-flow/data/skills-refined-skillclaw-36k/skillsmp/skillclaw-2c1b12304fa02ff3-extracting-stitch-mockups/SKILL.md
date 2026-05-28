---
name: extracting-stitch-mockups
description: Use this skill when you need to extract and download mockup images from Google Stitch project pages using a provided project URL.
---

# Extract Stitch Mockups

## Quick Start
1. **Get project URL** - User provides `https://stitch.withgoogle.com/projects/{id}`
2. **Navigate to URL** - Use the appropriate browser tool to access the Stitch project page.
3. **Check generation status** - Ensure that the mockups are fully generated before proceeding.
4. **Extract image URLs** - Parse the page to find image URLs from `lh3.googleusercontent.com/aida/...`.
5. **Download images** - Use a utility script or built-in functions to download the images.
6. **Save to exports** - Images are saved to `design-intent/google-stitch/{feature}/exports/`.

---

## Feature Directory Resolution

Determine the target feature directory using this fallback chain:

1. **User specifies** - Optional `--feature` argument provided.
2. **Auto-detect** - Match the Stitch project title to existing `design-intent/google-stitch/{feature}/` directories.
3. **Prompt user** - List existing directories and ask the user to select or create a new one.

### Auto-Detection Logic
- Extract the project title from the Stitch page (e.g., "Eco-Travel Home Screen").
- Normalize to feature format: lowercase, hyphens, strip special characters.
- Search for matching directories in `design-intent/google-stitch/`.
- If multiple partial matches are found, prompt the user to select.

---

## Extraction Process

### Prerequisites
- Active Google session in the browser being used.
- Required libraries and tools installed (e.g., Playwright, urllib).

### Extraction Steps
1. **Navigate to Stitch URL** using the browser tool.
2. **Wait for page load** and check if generation is complete.
3. **Take a DOM snapshot** to capture the current state of the page.
4. **Parse the snapshot** to find `<img>` elements with `src` containing `lh3.googleusercontent.com/aida/`.
5. **Extract image URLs** from the parsed snapshot.
6. **Download images** using `urllib.request.urlretrieve()` or a utility script.
7. **Save images** to the designated `exports/` directory.

### Utility Script (Optional)
The Python script provides utility functions for directory resolution and downloading:

```python
from extract_images import resolve_output_dir, download_images

# Resolve output directory and download images
```