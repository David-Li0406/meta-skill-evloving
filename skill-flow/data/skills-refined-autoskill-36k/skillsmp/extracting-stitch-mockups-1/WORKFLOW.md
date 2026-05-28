# Workflow: Extract Stitch Mockups

Detailed steps for extracting mockup images from Google Stitch projects using Cursor's built-in browser (MCP browser tools).

---

## Step-by-Step Process

### 1. Validate Input

Check URL format:
```
URL must contain: stitch.withgoogle.com/projects/
```

**Expected URL format:** `https://stitch.withgoogle.com/projects/{project-id}`

### 2. Navigate to Stitch URL

Use Cursor's built-in browser to navigate:

```typescript
// Navigate to the Stitch project page
mcp_cursor-ide-browser_browser_navigate({
  url: "https://stitch.withgoogle.com/projects/123"
})
```

**Note:** The browser maintains the user's Google session automatically.

### 3. Wait for Page Load

Wait for the page to fully load:

```typescript
// Wait for content to load
mcp_cursor-ide-browser_browser_wait_for({
  time: 3  // seconds
})
```

This ensures all lazy-loaded images are rendered.

### 4. Check Generation Status

Take a snapshot to check if the project is still generating:

```typescript
// Get page snapshot
const snapshot = mcp_cursor-ide-browser_browser_snapshot({})

// Check snapshot content for "Generating" text
if (snapshot.content.includes("Generating") && 
    snapshot.content.toLowerCase().includes("estimated time")) {
  // Project is still generating, wait and retry
}
```

**Status indicators:**
- "Generating..." text visible
- "estimated time" mention
- Spinner/loading UI elements

### 5. Extract Image URLs from Snapshot

Parse the snapshot to find image elements:

```typescript
// Parse snapshot to find <img> elements
// Filter for src containing "lh3.googleusercontent.com/aida/"

const imageUrls = [];
// Iterate through snapshot nodes to find img elements
// Extract src attribute from matching elements
```

**Filtering criteria:**
- Element type: `img`
- URL pattern: `lh3.googleusercontent.com/aida/`

### 6. Extract Project Title

Extract from snapshot:

**Priority order:**
1. `h1` element in snapshot
2. Element with `title` class
3. Element with `project-name` class
4. Fallback: Extract from URL

Parse the snapshot to find the title element and extract its text content.

### 7. Resolve Feature Directory

Use the utility script's `resolve_output_dir` function:

**Fallback chain:**
1. User-provided `--feature` argument
2. Auto-detect from existing directories
3. Prompt user to select
4. Create new from project title

**Auto-detection logic:**
```python
from extract_images import resolve_output_dir, normalize_feature_name

normalized = normalize_feature_name(project_title)
# "Eco-Travel Home Screen" -> "eco-travel-home-screen"

output_dir = resolve_output_dir(
    project_title=project_title,
    feature=None  # or specify explicitly
)
```

### 8. Download Images

Download images using `urllib.request` or the utility script:

```python
import urllib.request
from pathlib import Path

output_dir = Path("design-intent/google-stitch/{feature}/exports")
output_dir.mkdir(parents=True, exist_ok=True)

for i, img_url in enumerate(image_urls, 1):
    filename = f"mockup-{i}.png"
    filepath = output_dir / filename
    urllib.request.urlretrieve(img_url, filepath)
```

**Output location:** `design-intent/google-stitch/{feature}/exports/`

**Alternative using utility script:**
```python
from extract_images import download_images

saved_files = download_images(
    image_urls=image_urls,
    output_dir=output_dir,
    project_title=project_title
)
```

### 9. Generate Report

Display extraction summary with:
- Project title and URL
- Number of images extracted
- Output directory path
- List of saved files

---

## Image URL Reference

Based on investigation of Stitch's image patterns:

### Image Sources

- **Mockups:** `lh3.googleusercontent.com/aida/...` (400px+) - These are the target images
- **Avatars:** `stitch-avatar.png` - Excluded from extraction
- **UI assets:** `app-companion-430619.appspot.com` - Excluded from extraction

### URL Pattern

All mockup images from Stitch use this pattern:
```
https://lh3.googleusercontent.com/aida/{unique-id}
```

Filter for URLs containing `lh3.googleusercontent.com/aida/` in the `src` attribute of `<img>` elements.

---

## Error Handling

### Authentication Failure

**Symptoms:**
- Redirected to Google sign-in
- Page shows "Sign in" prompt
- No images captured

**Solution:** Sign into Google in Cursor's browser, then retry. The browser maintains the session automatically.

### Generation In Progress

**Symptoms:**
- Page shows "Generating..."
- Status text mentions "estimated time"
- Spinner visible

**Solution:** Wait for generation to complete (~40 seconds), then retry.

### No Images Found

**Symptoms:**
- Script completes but no images saved
- "No mockup images found" message

**Possible causes:**
1. Project is empty (no designs generated)
2. Generation failed on Stitch side
3. Network filtering blocked image responses

### Invalid URL

**Symptoms:**
- "Invalid Stitch project URL" error

**Solution:** Use full URL format:
`https://stitch.withgoogle.com/projects/{project-id}`

---

## Performance Notes

- **Total extraction time:** ~5-10 seconds
- **Network wait:** 3 seconds (for page load)
- **Typical image count:** 1-6 per project
- **Image size:** ~100-500KB each

---

## Security Considerations

- Uses Cursor's built-in browser with user's existing session
- Images downloaded via authenticated session
- No data transmitted to external services
- All processing done locally
