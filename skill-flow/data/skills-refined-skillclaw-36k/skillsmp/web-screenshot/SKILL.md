---
name: web-screenshot
description: This skill should be used when the user asks to "save screenshot", "capture web image", "save image from web", "screenshot this", or when fetching web content that includes images to save.
---

# /web-screenshot

Save images and screenshots from web content to a git-managed resources folder with descriptive naming.

## Instructions

When saving images from web content:

### 1. Naming Convention

Save files to `resources/screenshots/` using this format:

```
YYYYMMDD-HHMMSS_topic_slug.ext
```

**Components:**

- `YYYYMMDD-HHMMSS`: Timestamp (e.g., `20260122-143052`)
- `topic`: Category/source (e.g., `google-doodle`, `github`, `docs`)
- `slug`: Brief description in kebab-case (e.g., `mlk-day-2026`, `react-hooks-diagram`)
- `ext`: Original file extension (`.png`, `.jpg`, `.gif`, `.webp`)

**Examples:**

- `20260122-143052_google-doodle_mlk-day-2026.png`
- `20260115-091230_github_actions-workflow-diagram.png`
- `20260120-162045_docs_api-architecture.jpg`

### 2. Saving Process

```bash
# Get current timestamp
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

# Download with descriptive name
curl -L -o "resources/screenshots/${TIMESTAMP}_topic_slug.ext" "IMAGE_URL"
```

### 3. Verify and Display

After saving:

1. Use the `Read` tool to verify the image was saved correctly
2. Display the image to the user
3. Confirm the saved path

### 4. Git Tracking

All screenshots in `resources/screenshots/` are git-tracked. After saving:

- Files are ready for commit
- Use descriptive commit messages: `docs: add screenshot of [topic]`

### 5. Index File

Update `resources/screenshots/INDEX.md` with a clickable link to the file:

```markdown
## Screenshots

| Date       | File                                                                                               | Description           | Source         |
| ---------- | -------------------------------------------------------------------------------------------------- | --------------------- | -------------- |
| 2026-01-22 | [`20260122-143052_google-doodle_mlk-day-2026.png`](20260122-143052_google-doodle_mlk-day-2026.png) | MLK Day Google Doodle | doodles.google |
```

**Format:** `[filename](filename)` - links to the file in the same directory for one-click viewing.

## Examples

**User:** "What's the Google Doodle today? Save it as a screenshot"
**Action:** Fetch doodle, save as `20260122-143052_google-doodle_mlk-day-2026.png`

**User:** "Save this architecture diagram"
**Action:** Download image, save as `20260122-150000_docs_system-architecture.png`

**User:** "Screenshot the GitHub Actions workflow"
**Action:** Capture/fetch image, save as `20260122-160000_github_actions-workflow.png`
