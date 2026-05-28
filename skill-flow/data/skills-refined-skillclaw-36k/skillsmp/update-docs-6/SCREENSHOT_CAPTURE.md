# Screenshot Capture for Documentation

Use the Playwright MCP to capture screenshots of the application for documentation purposes.

## Prerequisites

- The application must be running locally (frontend at `http://localhost:5173`)
- Only capture screenshots from localhost - never from external hosts

## Screenshot Storage

Save all screenshots to the documentation repository:
```
/Users/roelandhofkens/Projects/Ai/video-story-creator-docs/images/screenshots/
```

## Workflow

### 1. Navigate and Capture

Use Playwright MCP tools to:

1. **Navigate to the page** (use headless mode):
   ```
   playwright_navigate to http://localhost:5173 with headless=true
   ```

2. **Login if required** (default credentials):
   - Email: `roeland.hofkens@bluefields.ai`
   - Password: Use `VIDEO_STORY_LOCAL_ADMIN_PWD` environment variable

3. **Take screenshots**:
   ```
   playwright_screenshot with name and savePng=true
   ```

4. **Validate and retry** (see Screenshot Validation section below)

### 2. Screenshot Validation

After capturing each screenshot, validate that it shows the relevant content for the documentation context.

**Validation Process:**

1. **Analyze the screenshot** - Read the captured image and assess:
   - Does it show the UI element or feature being documented?
   - Is the relevant content visible and not obscured?
   - Are there distracting or irrelevant elements taking up space?

2. **If the screenshot is NOT suitable**, take corrective action:
   - **Scroll** to bring the relevant content into view
   - **Collapse** sidebars, panels, or accordions that are not relevant
   - **Click** to close modals, tooltips, or menus that obscure content
   - **Resize** the viewport if needed for better framing
   - **Navigate** to a different view or tab if the content is elsewhere

3. **Retake the screenshot** after corrections

4. **Repeat validation** - maximum **3 attempts** per screenshot to avoid endless loops

**Decision Flow:**
```
Capture Screenshot
       ↓
   Analyze Image
       ↓
   Is content relevant? ──Yes──→ Keep screenshot, proceed
       ↓ No
   Attempt < 3? ──No──→ Keep best attempt, log warning, proceed
       ↓ Yes
   Apply corrections (scroll/collapse/click)
       ↓
   Retake screenshot
       ↓
   (loop back to Analyze)
```

**Example Corrections:**
- Content below fold → `playwright_evaluate` to scroll down
- Sidebar distracting → Click collapse button or navigate to fullscreen view
- Modal blocking → Click close button or press Escape
- Wrong tab selected → Click the correct tab

### 4. Playwright MCP Tools Reference

**Navigation:**
- `playwright_navigate` - Go to a URL (localhost only!)
- `playwright_click` - Click elements
- `playwright_fill` - Fill form fields
- `playwright_get_visible_text` - Get page content

**Screenshots:**
- `playwright_screenshot` - Capture screenshot
  - `name`: Descriptive name for the screenshot
  - `fullPage`: Set to true for full page capture
  - `savePng`: Set to true to save as PNG file
  - `selector`: Optional CSS selector for specific element

**Cleanup:**
- `playwright_close` - Close browser when done

### 5. Screenshot Naming Convention

Use descriptive, kebab-case names:
- `dashboard-projects-list.png`
- `digital-twin-voice-setup.png`
- `project-wizard-step1.png`
- `video-preview-player.png`

### 6. Move Screenshots to Docs Repo

After capturing, move screenshots to the docs repository:
```bash
mv ~/Downloads/<screenshot-name>.png /Users/roelandhofkens/Projects/Ai/video-story-creator-docs/images/screenshots/
```

### 7. Reference in Documentation

Use screenshots in MDX files:
```mdx
<img src="/images/screenshots/dashboard-projects-list.png" alt="Projects Dashboard" />
```

Or with Frame component for styled screenshots:
```mdx
<Frame>
  <img src="/images/screenshots/dashboard-projects-list.png" alt="Projects Dashboard" />
</Frame>
```

## Security Rules

- **ONLY** navigate to `localhost` URLs (http://localhost:5173, http://localhost:8080)
- **NEVER** navigate to external hosts or production URLs
- **NEVER** capture screenshots with sensitive data visible
- Close the browser when done with `playwright_close`

## Example: Capturing Login Flow

```
1. playwright_navigate to http://localhost:5173 with headless=true
2. playwright_screenshot name="login-page" with savePng=true
3. Read screenshot → Validate login form is visible → OK
4. playwright_fill email field
5. playwright_fill password field
6. playwright_screenshot name="login-filled" with savePng=true
7. Read screenshot → Validate form shows filled fields → OK
8. playwright_click sign in button
9. playwright_screenshot name="dashboard-after-login" with savePng=true
10. Read screenshot → Validate dashboard content visible
    → If sidebar obscures content: click collapse, retake (attempt 2)
    → If content below fold: scroll down, retake (attempt 2)
    → Max 3 attempts, then proceed with best result
11. playwright_close
```
