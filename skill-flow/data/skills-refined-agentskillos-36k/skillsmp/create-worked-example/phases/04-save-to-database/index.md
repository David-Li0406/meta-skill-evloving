# Phase 4: Save & Export

## Purpose
Save the worked example to the database and export to PPTX or Google Slides for classroom use.

## Output Format
All slides are **960×540px, light theme** (7 slides). CFU/Answer boxes use PPTX animation. See `03-generate-slides/02-technical-rules.md` for technical specs.

## Prerequisites
- Phases 1-3 complete
- All slide HTML generated

---

## Phase 4.0: Optimize for Export (NEW - Run First!)

**Before saving or exporting, optimize slides for better PPTX quality.**

See: **[optimize-for-export.md](./optimize-for-export.md)** for full instructions.

### Quick Summary

The optimization step converts simple SVGs to HTML, resulting in **editable PPTX elements** instead of static images:

| Before Optimization | After Optimization |
|---------------------|-------------------|
| SVG rect + text → Screenshot (PNG) | HTML div + p → Native shapes/text |
| Teacher can't edit | Teacher can move/resize/edit |

### When to Convert SVGs

| SVG Contains | Action |
|--------------|--------|
| Only `<rect>`, `<text>`, `<line>`, `<circle>` | **Convert to HTML** |
| `<path>` with curves, gradients, graphs | Keep as SVG |

### Browser Wizard: Automatic Optimization

The browser wizard automatically runs optimization before export:
1. Click "Export to Slides"
2. System analyzes all slides for simple SVGs
3. Simple SVGs converted to HTML `visual-*` regions
4. Optimized slides exported to PPTX/Google Slides

### CLI Mode: Manual Optimization

Before saving, review each slide and convert simple SVGs manually following the patterns in `optimize-for-export.md`.

---

## Workflow Options

There are **two workflows** depending on how the deck was created:

| Workflow | When to Use | Save Method | Export Options |
|----------|-------------|-------------|----------------|
| **Browser Wizard** | Created in `/scm/workedExamples/create` | Step 4 UI | PPTX download, Google Slides |
| **CLI Mode** | Created via Claude Code skill | sync-to-db.js script | Manual PPTX export |

---

## Browser Wizard Workflow (Recommended)

If slides were created using the browser wizard at `/scm/workedExamples/create`:

### Step 4.1: Review Metadata

The wizard's Step 4 displays a form with:
- **Title** (required) - Display name for the deck
- **Slug** (required) - URL-safe identifier (lowercase, hyphens only)
- **Math Concept** - Topic area (e.g., "Linear Equations")
- **Math Standard** - Standard code (e.g., "8.EE.C.7")
- **Is Public** - Visibility setting

### Step 4.2: Export Options

**Before saving**, you can export to:

#### Export to PPTX (Download)

Generates a PowerPoint file that can be:
- Edited in Microsoft PowerPoint
- Uploaded to Google Drive manually
- Shared via email or LMS

**API Endpoint:** `POST /api/scm/worked-examples/export-pptx`
```typescript
{
  slides: SlideData[],  // Array of { slideNumber, htmlContent }
  title: string,        // Deck title
  mathConcept?: string  // Optional metadata
}
// Returns: Binary PPTX file
```

#### Export to Google Slides (Direct)

Uploads directly to the user's Google Drive as a Google Slides presentation.

**Requirements:**
- User must be signed in with Google OAuth
- Google Drive scope must be authorized

**API Endpoint:** `POST /api/scm/worked-examples/export-google-slides`
```typescript
{
  slides: SlideData[],  // Array of { slideNumber, htmlContent }
  title: string,        // Deck title
  mathConcept?: string, // Optional metadata
  slug?: string         // If provided, saves URL to database
}
// Returns: { success: true, url: string, fileId: string }
```

**Flow:**
1. Generate PPTX server-side
2. Upload to user's Google Drive
3. Convert to Google Slides format
4. Return Google Slides URL
5. If `slug` provided, save URL to database

### Step 4.3: Save to Database

Click "Save Deck" to:
1. Create a `WorkedExampleDeck` document in MongoDB
2. Store all HTML slides
3. Link to Google Slides URL (if exported)
4. Clear the wizard's local state

**Server Action:** `saveWorkedExampleDeck`

---

## CLI Mode Workflow

If slides were created using Claude Code (file-by-file with Write tool):

### Step 4.1: Create metadata.json

**File:** `src/app/presentations/{slug}/metadata.json`

```json
{
  "title": "[STRATEGY NAME] - [TOPIC]",
  "slug": "[slug]",
  "mathConcept": "[from PROBLEM ANALYSIS]",
  "mathStandard": "[if known, e.g., 7.RP.A.1]",
  "gradeLevel": "[6/7/8 or 'Algebra 1']",
  "unitNumber": [number],
  "lessonNumber": [number],
  "scopeAndSequenceId": "[from Phase 1 or null]",
  "strategyName": "[from STRATEGY DEFINITION]",
  "strategySteps": ["[VERB 1]", "[VERB 2]", "[VERB 3 if applicable]"],
  "learningGoals": [
    "[goal 1]",
    "[goal 2 if applicable]"
  ],
  "scenarios": [
    "[Scenario 1 name]",
    "[Scenario 2 name]",
    "[Scenario 3 name]"
  ]
}
```

### Step 4.2: Sync to MongoDB

```bash
source .env.local && node .claude/skills/create-worked-example-sg/scripts/sync-to-db.js {slug}
```

**Expected output:**
```
✅ HTML Deck saved successfully!
Deck ID: [ObjectId]
Slug: [slug]
Total slides: 9
📁 Local files: src/app/presentations/[slug]/
🔗 View at: /presentations/[slug]
```

### Step 4.3: Run Verification Script

```bash
npx tsx .claude/skills/create-worked-example-sg/scripts/verify-worked-example.ts --slug {slug} --verbose
```

### Step 4.4: Clean Up Progress File

After verification passes:
```bash
rm src/app/presentations/{slug}/.worked-example-progress.json
```

---

## PPTX Export Technical Details

### How HTML Becomes PPTX

The export system uses `data-pptx-*` attributes to map HTML elements to PowerPoint shapes:

```html
<div data-pptx-region="badge"
     data-pptx-x="20" data-pptx-y="16" data-pptx-w="180" data-pptx-h="35"
     style="background: #1791e8; ...">
  <p>STEP 1</p>
</div>
```

| Attribute | Purpose |
|-----------|---------|
| `data-pptx-region` | Element type (badge, title, content-box, cfu-box, etc.) |
| `data-pptx-x` | X position in pixels (from 960px width) |
| `data-pptx-y` | Y position in pixels (from 540px height) |
| `data-pptx-w` | Width in pixels |
| `data-pptx-h` | Height in pixels |

### Region Types

| Region | PPTX Behavior |
|--------|---------------|
| `badge` | Native text box with background |
| `title` | Native text (heading style) |
| `subtitle` | Native text |
| `content-box` | Text box with optional background |
| `left-column` | Text box (left side) |
| `svg-container` | Rendered as PNG image(s) |
| `cfu-box` | Text box with **click animation** (appears on click) |
| `answer-box` | Text box with **click animation** (appears on click) |

### SVG Handling

SVG elements are rendered to PNG using Puppeteer:
1. Parse SVG from HTML
2. Render in headless Chromium
3. Export as PNG with transparency
4. Embed in PPTX as image

**Multi-layer SVGs** (with `data-pptx-layer` attributes) are rendered as separate images for independent manipulation in PowerPoint.

### CFU/Answer Animation

Elements with `data-pptx-region="cfu-box"` or `"answer-box"` are:
- Added to the slide
- Set to **appear on click** (PPTX animation)
- Hidden when slide first displays
- Revealed when teacher clicks during presentation

This eliminates the need for duplicate question/answer slides.

---

## Google Slides Integration

### OAuth Requirements

Google Slides export requires:
1. User signed in via Clerk with Google OAuth
2. `https://www.googleapis.com/auth/drive.file` scope authorized

### Re-Authorization Flow

If the OAuth token expires, the wizard:
1. Shows a re-authorization prompt
2. User clicks "Re-authorize with Google"
3. Redirects to Google OAuth with `oidcPrompt: 'consent'`
4. After re-auth, automatically retries the export

### URL Persistence

When a deck is exported to Google Slides:
1. The Google Slides URL is returned
2. If `slug` is provided, URL is saved to `WorkedExampleDeck.googleSlidesUrl`
3. The deck list shows a Google Slides icon/link for decks with saved URLs

---

## API Reference

### POST /api/scm/worked-examples/export-pptx

Generates and downloads a PPTX file.

**Request:**
```json
{
  "slides": [
    { "slideNumber": 1, "htmlContent": "<!DOCTYPE html>..." }
  ],
  "title": "Balance and Isolate",
  "mathConcept": "Linear Equations"
}
```

**Response:** Binary PPTX file with `Content-Disposition: attachment`

### POST /api/scm/worked-examples/export-google-slides

Uploads to Google Drive and converts to Google Slides.

**Request:**
```json
{
  "slides": [...],
  "title": "Balance and Isolate",
  "mathConcept": "Linear Equations",
  "slug": "balance-isolate-grade8"
}
```

**Response:**
```json
{
  "success": true,
  "url": "https://docs.google.com/presentation/d/...",
  "fileId": "abc123..."
}
```

---

## Phase 4 Completion Checklist

**Browser Wizard:**
- [ ] Reviewed title and slug
- [ ] Exported to PPTX (optional)
- [ ] Exported to Google Slides (optional)
- [ ] Saved to database
- [ ] Received confirmation message

**CLI Mode:**
- [ ] metadata.json created with all required fields
- [ ] Sync script ran successfully
- [ ] Verification script passed
- [ ] Progress file deleted
- [ ] User provided with presentation URL

---

## Troubleshooting

### PPTX Export Fails

1. Check that all slides have valid HTML
2. Verify `data-pptx-*` attributes are present on key elements
3. Check server logs for Puppeteer/rendering errors

### Google Slides Export: "Authorization Required"

1. User's Google token may have expired
2. Click "Re-authorize with Google"
3. Complete OAuth flow and retry

### Sync Script Fails

1. Check slide files exist: `ls src/app/presentations/{slug}/`
2. Verify metadata.json syntax: `cat src/app/presentations/{slug}/metadata.json | jq .`
3. Check DATABASE_URL: `echo $DATABASE_URL | head -c 50`

### SVG Not Rendering in PPTX

1. Ensure SVG is wrapped in `data-pptx-region="svg-container"`
2. Verify SVG has explicit `width` and `height` or `viewBox`
3. Check for unsupported SVG features (filters, external images)

---

## Summary

Phase 4 provides three output options:

| Output | Format | Editable | Requires Auth |
|--------|--------|----------|---------------|
| **Save to DB** | HTML in MongoDB | Yes (wizard) | Clerk |
| **Export PPTX** | PowerPoint file | Yes (desktop) | No |
| **Export Google Slides** | Google Slides | Yes (online) | Google OAuth |

The user can use any combination of these options.
