# Screenshot Capture for Documentation

Use Playwright or similar tools to capture screenshots of the application for documentation purposes.

## Prerequisites

- The application must be running locally
- Only capture screenshots from localhost - never from external hosts

## Screenshot Storage

Save all screenshots to your documentation folder:
```
docs/images/screenshots/
```

## Workflow

### 1. Navigate and Capture

1. **Navigate to the page** (use headless mode if available)
2. **Login if required**
3. **Take screenshots**
4. **Validate and retry** (see Screenshot Validation section below)

### 2. Screenshot Validation

After capturing each screenshot, validate that it shows the relevant content for the documentation context.

**Validation Process:**

1. **Analyze the screenshot** - Assess:
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

### 3. Screenshot Naming Convention

Use descriptive, kebab-case names:
- `dashboard-projects-list.png`
- `settings-page.png`
- `wizard-step1.png`
- `preview-player.png`

### 4. Reference in Documentation

Use screenshots in Markdown/MDX files:
```mdx
![Projects Dashboard](/images/screenshots/dashboard-projects-list.png)
```

Or with HTML for more control:
```mdx
<img src="/images/screenshots/dashboard-projects-list.png" alt="Projects Dashboard" />
```

## Security Rules

- **ONLY** navigate to `localhost` URLs
- **NEVER** navigate to external hosts or production URLs
- **NEVER** capture screenshots with sensitive data visible
- Close the browser when done

## Example: Capturing Login Flow

```
1. Navigate to http://localhost:3000
2. Take screenshot name="login-page"
3. Validate login form is visible → OK
4. Fill email field
5. Fill password field
6. Take screenshot name="login-filled"
7. Validate form shows filled fields → OK
8. Click sign in button
9. Take screenshot name="dashboard-after-login"
10. Validate dashboard content visible
    → If sidebar obscures content: click collapse, retake (attempt 2)
    → If content below fold: scroll down, retake (attempt 2)
    → Max 3 attempts, then proceed with best result
11. Close browser
```
