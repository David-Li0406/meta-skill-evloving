---
name: docugen
description: |
  Automate creation of step-by-step documentation from web or desktop workflows.
  Use when: (1) "document this workflow", (2) "create a walkthrough for [URL]",
  (3) "generate documentation", (4) "record this process", (5) "make a guide for",
  (6) "document this desktop app", (7) "capture macOS/Windows workflow".
  Produces professional markdown with annotated screenshots, contextual explanations,
  prerequisites, and expected results. Supports both browser-based (Playwright/Chrome
  DevTools MCP) and native desktop application recording (accessibility APIs + vision).
author: WYRE Technology
version: 1.1.0
date: 2026-01-23
triggers:
  - document this workflow
  - create a walkthrough
  - generate documentation
  - record this process
  - make a guide for
  - document how to
  - create step-by-step guide
  - document this application
  - capture desktop workflow
  - document Windows application
  - document macOS application
  - capture native app
  - desktop software guide
  - record desktop process
---

# DocuGen: Intelligent Documentation Generator

DocuGen transforms web-based and desktop workflows into professional-quality documentation with
annotated screenshots and contextual explanations.

## Quick Start

### Web Workflow
1. Provide the starting URL
2. Describe the workflow goal (e.g., "create a new project")
3. DocuGen will guide you through the recording process

**Example:**
```
Document this workflow: Create a new repository on GitHub
Starting URL: https://github.com/new
```

### Desktop Workflow
1. Name the application and workflow goal
2. DocuGen detects desktop mode automatically from your description
3. Follow prompts to perform each action while screenshots are captured

**Example:**
```
Document this desktop workflow: Change display resolution in System Settings
Application: System Settings
```

## Capabilities

- **Semantic Understanding**: Generates contextual explanations, not just "click here"
- **Screenshot Annotation**: Highlights, arrows, and numbered callouts
- **Professional Output**: Markdown with proper structure, prerequisites, and expected results
- **Audience Adaptation**: Adjust detail level for beginner/intermediate/expert
- **Dual Mode**: Supports both web (browser) and desktop (native app) recording
- **Accessibility Integration**: Uses platform accessibility APIs for precise element identification
- **Visual Fallback**: Claude Vision analysis when accessibility data is unavailable

## Requirements

### MCP Integrations (Web Mode)
- **Playwright MCP** or **Chrome DevTools MCP**: For browser automation and DOM access

### Python Dependencies (Both Modes)
- PIL/Pillow: Screenshot annotation
- scikit-image: SSIM step detection
- mss: Cross-platform screenshot capture (desktop mode)
- anthropic: Claude Vision API for visual element analysis (desktop mode fallback)

### Platform Dependencies (Desktop Mode, Optional)
- **macOS**: pyobjc-framework-Quartz, atomacos (accessibility)
- **Windows**: pywin32, pywinauto (accessibility)
- **Linux**: python-xlib (window enumeration only, no accessibility backend)

## Mode Detection

DocuGen automatically determines whether to use web or desktop recording based on
keywords in the user's request.

### Desktop Mode Keywords
Match any of these to activate desktop mode:
- "desktop", "native app", "application" (without URL)
- "System Preferences", "System Settings", "Finder", "Explorer"
- "Windows application", "macOS application"
- "installed software", "desktop software"
- App-specific names: "Photoshop", "Excel", "VS Code", "Terminal", etc.

### Web Mode Keywords
Match any of these (or presence of a URL) to activate web mode:
- "website", "web app", "browser", "URL", "http"
- Any valid URL in the request
- "login page", "dashboard", "web portal"

### Detection Priority
1. **Explicit URL provided** → Web mode (always)
2. **Desktop keywords matched** → Desktop mode
3. **Web keywords matched** → Web mode
4. **Ambiguous** → Ask user via `AskUserQuestion`

```
AskUserQuestion:
  question: "Is this a web-based or desktop application workflow?"
  header: "Mode"
  options:
    - label: "Web (browser)"
      description: "Recording in a web browser using Playwright/Chrome DevTools"
    - label: "Desktop (native app)"
      description: "Recording a native desktop application with screenshot capture"
```

## Workflow Orchestration

### Phase 1: Initiation

#### Web Mode
When user provides URL and workflow description:
1. Validate Playwright MCP or Chrome DevTools MCP is available
2. Create output directory for images
3. Navigate to starting URL
4. Confirm workflow goal with user

#### Desktop Mode
When user describes a desktop application workflow:
1. Detect platform capabilities via `get_capture_capabilities()`
2. Create output directory for images
3. Report available capture features (accessibility, window enumeration)
4. Confirm workflow goal and target application with user
5. Initialize `StepDetector` with desktop thresholds

### Phase 2: Recording

#### Web Mode Recording
For each user action:
1. Capture screenshot before action
2. Record element metadata (selector, text, ARIA labels)
3. Execute action via MCP
4. Capture screenshot after action
5. Compare screenshots using SSIM (threshold < 0.90)
6. If significant change detected, mark as step boundary

#### Desktop Mode Recording
For each user action:
1. Prompt user to describe the next action they will perform
2. Call `StepDetector.capture_before()` to take baseline screenshot
3. Prompt user to perform the action on their desktop
4. Call `StepDetector.capture_after(description)` to capture result
5. SSIM comparison (threshold < 0.87 for desktop) detects step boundary
6. If significant change detected:
   a. Get element metadata via `get_element_metadata(x, y, screenshot_path)`
   b. Accessibility backend provides element name, type, role
   c. If no accessibility data, fall back to Claude Vision analysis
   d. Record step with element metadata and source attribution
7. Offer user option to add more steps or finish recording

#### Desktop Step Capture Flow
```
User: "I'm going to click the Save button"

1. StepDetector.capture_before()
   → Takes screenshot, stores as baseline

2. [User performs action on desktop]

3. User: "Done" (or press Enter)

4. StepDetector.capture_after("Click Save button")
   → Takes screenshot
   → Compares SSIM (e.g., 0.74 < 0.87 threshold)
   → Returns StepRecord with before/after paths

5. get_element_metadata(click_x, click_y, after_screenshot_path)
   → Tries accessibility: {name: "Save", type: "button", source: "accessibility"}
   → Or vision fallback: {name: "Save", type: "button", source: "visual", confidence: 0.9}

6. Record step with full metadata
```

### Phase 3: Processing
After recording completes:
1. Run `detect_step.py` to finalize step boundaries
2. **Interactive Redaction Review** (see below)
3. Run `annotate_screenshot.py` to add visual annotations
4. Run `process_images.py` to optimize file sizes

### Interactive Redaction (User Prompts)

Before annotating screenshots, prompt the user to review detected sensitive regions.
Use `AskUserQuestion` to give users control over what gets redacted.

#### Auto-Detection First

Smart annotation auto-detects common sensitive fields:
- Password fields (`type="password"`)
- SSN, credit card, API key fields
- Email and phone number inputs

#### Prompt User for Confirmation

After auto-detection, present findings to user:

```
AskUserQuestion:
  question: "I detected 3 potentially sensitive fields to blur. Review?"
  header: "Redaction"
  options:
    - label: "Show me what you found"
      description: "Review auto-detected fields before blurring"
    - label: "Blur all detected fields"
      description: "Trust auto-detection and blur everything"
    - label: "No redaction needed"
      description: "Skip all blurring for this workflow"
```

#### If User Selects Review

Present each detected field:

```
AskUserQuestion:
  question: "Field: 'Password' input at coordinates (120, 340). Blur this?"
  header: "Blur field?"
  options:
    - label: "Yes, blur it"
      description: "Add blur to hide this content"
    - label: "No, keep visible"
      description: "This content is safe to show"
    - label: "Blur all remaining"
      description: "Skip review, blur everything else"
```

#### Custom Redaction Regions

After auto-detection review, offer to add custom regions:

```
AskUserQuestion:
  question: "Add any custom regions to blur?"
  header: "Custom blur"
  options:
    - label: "Yes, let me specify"
      description: "I'll describe regions that need blurring"
    - label: "No, we're done"
      description: "Proceed with current selections"
```

If user wants custom regions, prompt for description:
- "Describe what to blur (e.g., 'the email address in the top right')"
- Use element metadata to locate described content
- Confirm coordinates before applying

#### Redaction Session Data

Track redaction decisions in session:

```json
{
  "redactionReview": {
    "autoDetected": [
      {"field": "password", "coords": [120, 340, 200, 30], "approved": true},
      {"field": "email", "coords": [120, 400, 200, 30], "approved": false}
    ],
    "customRegions": [
      {"description": "company logo", "coords": [10, 10, 100, 50]}
    ],
    "userChoice": "reviewed"
  }
}
```

### Phase 4: Generation
1. Load `writing_style_guide.md` reference for quality standards
2. Run `generate_markdown.py` with captured data
3. Enrich step descriptions with contextual explanations
4. Auto-detect prerequisites based on workflow analysis
5. Generate expected results for each step
6. Add troubleshooting section for common issues

### Phase 5: Output
1. Save markdown to output directory
2. Verify all image references are valid
3. Generate table of contents if multi-section
4. Present summary to user

## Progressive Disclosure

Load references as needed:
- `references/writing_style_guide.md` - During Phase 4 generation
- `references/annotation_conventions.md` - During Phase 3 processing
- `references/troubleshooting_patterns.md` - For troubleshooting section

## Contextual Description Generation (FR-3.2, US-2)

During Phase 4, analyze the captured workflow data to generate contextual descriptions that explain
**why** each step matters, not just what to do.

### Semantic Analysis Process

For each recorded step, analyze:

1. **Workflow Context**: The overall goal described by the user
2. **DOM Metadata**: Element text, ARIA labels, and semantic roles
3. **Step Sequence**: Position in workflow and relationship to adjacent steps
4. **Visual Changes**: What changed between before/after screenshots

### Description Generation Rules

Apply `references/writing_style_guide.md` and generate:

1. **Purpose Statement**: Why this action is necessary
   - Connect action to workflow goal
   - Explain what capability or state this enables
   - Example: "Access the project settings to configure team permissions"

2. **Action Description**: What to do (imperative, ≤25 words)
   - Use element text/label for specificity
   - Include location hints from DOM structure
   - Example: "Click **Settings** in the left sidebar menu"

3. **Expected Result**: What user should observe
   - Describe visible confirmation of success
   - Use present tense
   - Example: "The Settings panel opens with the General tab selected"

### Output Format

Generate enriched step data as JSON:

```json
{
  "step": 1,
  "action": "click",
  "elementText": "New Project",
  "context": "Creates a new project workspace to organize your team's work",
  "description": "Click **New Project** in the top navigation bar to start creating your project.",
  "expected": "The New Project dialog appears with fields for project name and description.",
  "prerequisites_detected": ["Logged into account", "On dashboard page"]
}
```

### Prerequisites Auto-Detection

Analyze the workflow to automatically detect prerequisites:

| Pattern | Detected Prerequisite |
|---------|----------------------|
| Login page in first steps | "Active user account" |
| Navigation from dashboard | "Logged into the application" |
| Specific URL patterns | "Access to [feature name]" |
| Role-specific UI elements | "Appropriate permissions" |
| Form pre-filled data | "Required information prepared" |

### Context Inference Examples

| Element Metadata | Generated Context |
|-----------------|-------------------|
| `button#submit-form, "Submit"` | "Submits the completed form for processing" |
| `a[href="/settings"], "Settings"` | "Opens application settings to customize your experience" |
| `input[type="search"], placeholder="Search..."` | "Filters results to find specific items quickly" |
| `button.delete, "Delete"` | "Permanently removes the selected item" |
| `nav > a, "Dashboard"` | "Returns to the main overview of your workspace" |

### Quality Guidelines

- **Avoid generic phrases**: Don't write "Click the button" - specify which button and why
- **Connect to user goals**: Each step should relate to the workflow objective
- **Be specific about outcomes**: "The modal closes" vs "The save is confirmed"
- **Match audience level**: Adjust verbosity based on `beginner|intermediate|expert`

## Output Structure

Generated documentation follows this structure:
```markdown
# [Workflow Title]

## Overview
[Brief description of what this guide covers]

## Prerequisites
- [Auto-detected requirements]
- [User-provided prerequisites]

## Steps

### Step 1: [Action Title]
[Contextual description explaining WHY this step matters]

![Step 1 Screenshot](./images/step-01-description.png)

**Expected result:** [What user should see after this step]

[... additional steps ...]

## Troubleshooting

**[Common Issue]**
[Description and resolution]
```

## Configuration

### Audience Levels
- `beginner`: Full context, warnings, detailed explanations
- `intermediate`: Standard detail, key warnings only
- `expert`: Concise, minimal explanation

### Output Options
- `imageFormat`: png (default), jpg
- `embedImages`: false (file references) or true (base64)
- `includeTableOfContents`: true for 5+ steps
- `generatePdf`: true (default) - Generate PDF alongside markdown

### Redaction Options
- `interactiveRedaction`: true (default) - Prompt user to review detected fields
- `autoBlurSensitive`: true (default) - Auto-detect and blur sensitive fields
- `redactionReviewMode`: "summary" | "each" | "none"
  - `summary`: Show count of detected fields, ask to review
  - `each`: Prompt for each detected field individually
  - `none`: Auto-blur without prompting (use with caution)

## Audience Adaptation (US-4)

Adjust documentation detail and tone based on the target audience level.

### Beginner Level (`audience=beginner`)

Generate documentation with:
- **Full context**: Explain why each step is necessary and what it accomplishes
- **Detailed warnings**: Include caution notes for irreversible actions
- **Navigation hints**: Describe where to find elements on screen
- **Terminology explanations**: Define any technical terms
- **Expected results**: Detailed descriptions of what should happen

**Example step (beginner):**
```markdown
### Step 3: Save your project

Before you can share your project with others, you need to save it first.
This ensures all your changes are stored and creates a link you can share.

> **Note:** Saving cannot be undone. Make sure you're happy with your
> project name before proceeding.

Click the **Save** button (the blue button with a disk icon) in the top-right
corner of the screen.

**Expected result:** A green "Saved successfully!" message appears briefly,
and the URL in your browser's address bar changes to include your project ID.
```

### Intermediate Level (`audience=intermediate`)

Generate documentation with:
- **Standard context**: Brief explanation of step purpose
- **Key warnings only**: Only critical cautions
- **Concise expected results**: What confirms success

**Example step (intermediate):**
```markdown
### Step 3: Save your project

Click **Save** in the top-right corner to store your changes.

> **Warning:** This action cannot be undone.

**Expected result:** "Saved successfully!" confirmation appears.
```

### Expert Level (`audience=expert`)

Generate documentation with:
- **Minimal context**: Just the action
- **No warnings**: Unless absolutely critical
- **Brief expected results**: Single sentence or omitted

**Example step (expert):**
```markdown
### Step 3: Save your project

Click **Save**. Confirmation message confirms success.
```

### Adaptation Matrix

| Aspect | Beginner | Intermediate | Expert |
|--------|----------|--------------|--------|
| Step length | 50-100 words | 25-50 words | 10-25 words |
| Context | Full explanation | Brief purpose | Omit |
| Warnings | All applicable | Critical only | Rare |
| Screenshots | Every step | Key steps | Minimal |
| Navigation hints | Detailed | Brief | Omit |
| Terminology | Defined | Assumed known | Assumed known |

## Troubleshooting Generation (FR-3.7)

Automatically generate a troubleshooting section based on workflow analysis.
Reference `references/troubleshooting_patterns.md` for templates.

### Workflow Type Detection

Analyze the recorded workflow to identify type and generate relevant issues:

| Workflow Pattern | Troubleshooting Focus |
|-----------------|----------------------|
| Login/authentication | Session expired, invalid credentials, 2FA issues |
| Form submission | Validation errors, required fields, format issues |
| File upload | Size limits, format restrictions, upload failures |
| Search/filter | No results, too many results, filter confusion |
| Settings/configuration | Permission denied, changes not saving |
| Data creation | Naming conflicts, duplicate entries |
| Navigation | Page not found, access denied |

### Auto-Detection Rules

Based on captured UI elements, automatically detect applicable issues:

```json
{
  "detected_patterns": [
    {"pattern": "input[type='password']", "issue": "authentication"},
    {"pattern": "input[type='file']", "issue": "file_upload"},
    {"pattern": "form[action]", "issue": "form_submission"},
    {"pattern": ".search-input", "issue": "search_results"},
    {"pattern": "button:disabled", "issue": "permissions"}
  ]
}
```

### Troubleshooting Output Format

Generate 2-3 relevant issues per workflow:

```markdown
## Troubleshooting

**Form submission fails without error message**
1. Check all required fields are completed (marked with *)
2. Verify email and phone fields are in correct format
3. Scroll up to check for error messages at the top of the form

**"Invalid input" error on project name**
Project names can only contain letters, numbers, and hyphens. Remove any
special characters or spaces and try again.

**Save button is disabled**
This indicates you may not have edit permissions for this project. Contact
your organization administrator to request Editor access.
```

### Issue Priority

Select troubleshooting issues in this priority:
1. **Highly likely**: Issues directly related to recorded workflow
2. **Commonly encountered**: General issues for this workflow type
3. **Edge cases**: Only if space permits

## Playwright MCP Integration

### Browser Launch and Navigation

Use Playwright MCP to control the browser. The following tools are essential:

```
# Launch browser with appropriate viewport
browser_launch: { headless: false, viewport: { width: 1280, height: 720 } }

# Navigate to starting URL
browser_navigate: { url: "https://example.com" }

# Take screenshot at CSS resolution (ALWAYS use scale: "css"!)
browser_screenshot: { path: "step-01.png", scale: "css", fullPage: false }
```

### Element Interaction and Metadata Capture

Before each action, capture element metadata for documentation:

```javascript
// Get element metadata
{
  selector: "button#submit",           // CSS selector used
  text: "Submit",                       // Visible text content
  ariaLabel: "Submit form",            // ARIA label if present
  role: "button",                       // ARIA role
  boundingBox: { x, y, width, height } // Position for annotation
}
```

### DOM Event Tracking (FR-1.5)

For dynamic content, track DOM mutations:

```
// MutationObserver events to track:
- childList: Elements added/removed
- attributes: Class changes, visibility changes
- characterData: Text content changes
```

### Session Data Structure

Store recording session as JSON for processing:

#### Web Mode Session
```json
{
  "sessionId": "uuid",
  "mode": "web",
  "startUrl": "https://example.com",
  "workflowDescription": "Create a new project",
  "startTime": "2026-01-20T10:00:00Z",
  "steps": [
    {
      "step": 1,
      "action": "click",
      "selector": "button#new-project",
      "elementText": "New Project",
      "ariaLabel": "Create new project",
      "boundingBox": { "x": 100, "y": 200, "width": 120, "height": 40 },
      "screenshotBefore": "step-01-before.png",
      "screenshotAfter": "step-01-after.png",
      "ssimScore": 0.72,
      "timestamp": "2026-01-20T10:00:05Z",
      "domChanges": ["modal opened", "form displayed"]
    }
  ],
  "endTime": "2026-01-20T10:05:00Z"
}
```

#### Desktop Mode Session
```json
{
  "sessionId": "uuid",
  "mode": "desktop",
  "app_name": "System Settings",
  "workflowDescription": "Change display resolution",
  "platform": {
    "os": "macos",
    "dpi_scale": 2.0,
    "has_accessibility": true,
    "has_window_enumeration": true
  },
  "startTime": "2026-01-23T14:00:00Z",
  "steps": [
    {
      "step": 1,
      "action": "click",
      "description": "Click Displays in the sidebar",
      "mode": "desktop",
      "app_name": "System Settings",
      "window_title": "System Settings",
      "element": {
        "name": "Displays",
        "type": "button",
        "bounds": { "x": 85, "y": 320, "width": 180, "height": 32 },
        "source": "accessibility"
      },
      "screenshotBefore": "step-01-before.png",
      "screenshotAfter": "step-01-after.png",
      "ssimScore": 0.68,
      "timestamp": "2026-01-23T14:00:12Z"
    },
    {
      "step": 2,
      "action": "click",
      "description": "Select Scaled resolution option",
      "mode": "desktop",
      "app_name": "System Settings",
      "window_title": "Displays",
      "element": {
        "name": "Scaled",
        "type": "radio",
        "bounds": { "x": 420, "y": 285, "width": 120, "height": 24 },
        "source": "visual",
        "confidence": 0.88
      },
      "screenshotBefore": "step-02-before.png",
      "screenshotAfter": "step-02-after.png",
      "ssimScore": 0.75,
      "timestamp": "2026-01-23T14:00:30Z"
    }
  ],
  "endTime": "2026-01-23T14:02:00Z"
}
```

### Screenshot Capture Guidelines

- **Timing**: Capture before AND after each action
- **Resolution**: Native viewport resolution (target: 1280x720 minimum)
- **Performance**: Target <200ms per capture
- **Naming**: `step-{nn}-{action}.png` (e.g., `step-01-click-submit.png`)

### Atomic Coordinate Capture (CRITICAL)

**The #1 cause of misaligned annotations is capturing coordinates and screenshots at different times.**

Bounding boxes MUST be captured at the EXACT same page state as the screenshot. Any scroll,
reflow, dynamic content change, or delay between getting coordinates and taking the screenshot
will cause misalignment.

**The Golden Rule: Capture coordinates immediately before/after screenshot, same page state.**

```javascript
// CORRECT: Atomic capture sequence
await page.waitForLoadState('networkidle');  // Wait for page to stabilize
const bbox = await element.boundingBox();     // Get coordinates NOW
await page.screenshot({ path: 'step.png', scale: 'css' });  // Screenshot NOW
// bbox coordinates match the screenshot exactly
```

```javascript
// WRONG: Non-atomic capture (causes misalignment)
const bbox = await element.boundingBox();     // Get coordinates
await someOtherAction();                       // Page might change!
await page.screenshot({ path: 'step.png' });  // Screenshot - bbox is now stale
```

### Always Use CSS Scale

**ALWAYS use `scale: "css"` for screenshots.** This ensures coordinates from `boundingBox()`
match the screenshot pixels directly, eliminating DPI/devicePixelRatio issues entirely.

```
browser_screenshot: { path: "step-01.png", scale: "css" }
```

With `scale: "css"`:
- Screenshot pixels = CSS pixels
- `boundingBox()` returns CSS pixels
- Coordinates work directly, no transformation needed

**Do NOT rely on auto-scale detection** - it's a fallback, not a solution. Get it right the first time.

### Viewport Consistency

Lock viewport size at the start of recording and don't change it:

```javascript
await page.setViewportSize({ width: 1280, height: 720 });
```

Store viewport in session metadata for validation:

```json
{
  "viewport": { "width": 1280, "height": 720 },
  "elements": [
    {
      "isTarget": true,
      "boundingBox": { "x": 100, "y": 200, "width": 120, "height": 40 }
    }
  ]
}
```

### Action Recording

For each user-directed action:

1. **Wait for page stability** (`networkidle` or animations complete)
2. **Identify target element** using Playwright selectors
3. **ATOMIC CAPTURE** (do these together, no delays!):
   - Capture element metadata (selector, text, ARIA, boundingBox)
   - Take pre-action screenshot with `scale: "css"`
4. **Execute action** via appropriate Playwright tool:
   - `browser_click`: Click interactions
   - `browser_type`: Text input
   - `browser_select`: Dropdown selection
   - `browser_scroll`: Scroll actions
5. **Wait for network idle** or specified condition
6. **Take post-action screenshot** with `scale: "css"`
7. **Compare with SSIM** to detect step boundary
8. **Record DOM mutations** if significant

### Example Recording Flow (Web)

```
User: "Document creating a new GitHub repository"

1. browser_navigate: https://github.com/new
2. Wait for networkidle
3. [User says: "Enter repository name 'my-project'"]
4. ATOMIC: Capture metadata for input#repository-name (boundingBox, text, ARIA)
5. ATOMIC: browser_screenshot: { path: "step-01-before.png", scale: "css" }
   ↑ Steps 4-5 must happen with NO page changes between them!
6. browser_type: { selector: "input#repository-name", text: "my-project" }
7. Wait for networkidle
8. browser_screenshot: { path: "step-01-after.png", scale: "css" }
9. Run detect_step.py step-01-before.png step-01-after.png
10. If significant change: record as Step 1
11. Continue with next action...
```

### Example Recording Flow (Desktop)

```
User: "Document changing display resolution in System Settings"

1. Initialize StepDetector(mode="desktop", output_dir="./output/images")
2. Get platform capabilities: accessibility=True, os=macos

3. [Ask user: "What action will you perform next?"]
4. User: "I'll click Displays in the sidebar"

5. detector.capture_before()
   → Takes baseline screenshot

6. [User clicks Displays in System Settings]
7. User: "Done"

8. detector.capture_after("Click Displays in sidebar")
   → Takes screenshot, SSIM = 0.68 (< 0.87 threshold)
   → Step detected! Saves before/after images

9. get_element_metadata(x=85, y=320, screenshot_path="step-01-after.png")
   → Accessibility: {name: "Displays", type: "button", source: "accessibility"}

10. Record Step 1 with element metadata
11. [Ask user: "What action will you perform next?"]
12. Continue or finish...
```

## Desktop Capture Integration

### Platform Initialization

At the start of a desktop recording session, detect platform capabilities:

```python
from docugen.desktop import get_capture_capabilities, StepDetector, DetectorConfig

caps = get_capture_capabilities()
# {"screenshots": True, "window_enumeration": True, "accessibility": True,
#  "os": "macos", "dpi_scale": 2.0, "notes": []}

config = DetectorConfig(mode="desktop")  # Uses 0.87 threshold
detector = StepDetector(config=config, output_dir="./output/images")
```

### Element Metadata Resolution

After capturing a step, resolve the element the user interacted with:

```python
from docugen.desktop import get_element_metadata

# Tries accessibility first, falls back to Claude Vision
element = get_element_metadata(x=420, y=285, screenshot_path="step-02-after.png")
# Returns: {"name": "Scaled", "type": "radio", "source": "accessibility"}
# Or:      {"name": "Scaled", "type": "radio", "source": "visual", "confidence": 0.88}
```

### Source-Aware Annotations

Desktop annotations adapt styling based on element source:

| Source | Color | Border Width | Meaning |
|--------|-------|-------------|---------|
| accessibility | Red-orange (255,87,51) | 3px | High-confidence, API-verified |
| visual (≥0.8) | Orange (255,165,0) | 3px | Vision-identified, confident |
| visual (<0.8) | Orange (255,165,0) | 2px | Vision-identified, uncertain |

### Desktop Markdown Generation

Desktop mode steps include additional metadata in the generated markdown:

```markdown
### Step 2: Select Scaled resolution option

**Application:** System Settings - Displays

Click **Scaled** (radio, identified via visual analysis, 88% confidence)

![Step 2](./images/step-02-after.png)

**Expected result:** Resolution options grid appears below the Scaled radio button.
```

### Desktop Recording User Prompts

Use `AskUserQuestion` to guide the user through each desktop action:

```
AskUserQuestion:
  question: "What action will you perform next on the desktop?"
  header: "Next action"
  options:
    - label: "Click an element"
      description: "I'll click a button, menu item, or other UI element"
    - label: "Type text"
      description: "I'll type into a text field or search box"
    - label: "Keyboard shortcut"
      description: "I'll use a keyboard shortcut (e.g., Cmd+S)"
    - label: "Done recording"
      description: "I've completed all the steps"
```

After the user performs their action:

```
AskUserQuestion:
  question: "Where did you click? Describe the element or approximate screen position."
  header: "Element"
  options:
    - label: "I'll describe it"
      description: "Let me tell you what I clicked on"
    - label: "Auto-detect"
      description: "Use accessibility/vision to identify the element"
```

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `detect_step.py` | SSIM-based step boundary detection |
| `annotate_screenshot.py` | Add highlights, arrows, callouts (web + desktop) |
| `generate_markdown.py` | Template-based markdown assembly (web + desktop) |
| `process_images.py` | Optimization and compression |

### Desktop-Specific Modules

| Module | Purpose |
|--------|---------|
| `desktop/capture.py` | Cross-platform screenshot capture (mss) |
| `desktop/step_detector.py` | SSIM-based step detection with debounce |
| `desktop/platform_router.py` | Accessibility backend routing + visual fallback |
| `desktop/visual_analyzer.py` | Claude Vision API for element identification |
| `desktop/platform_utils.py` | OS detection and capability reporting |

## Templates

| Template | Use Case |
|----------|----------|
| `walkthrough.md` | Default step-by-step guide |
| `quick_reference.md` | Condensed expert guide |
| `tutorial.md` | Learning-focused with exercises |
