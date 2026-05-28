# Slide-by-Slide Generation Protocol

**What this file covers:** Per-slide protocol, slide structure, what each slide contains, generation modes.

---

## API MODE vs CLI MODE

**API Mode (browser wizard):** Your response is collected as a single stream.
- Output ONLY HTML slides separated by `===SLIDE_SEPARATOR===`
- NO preamble, NO announcements, NO "I'll generate..." text
- First characters of response MUST be `<!DOCTYPE html>`

**CLI Mode (file-by-file):** You write individual files with the Write tool.
- Announce checkpoints as conversational text between file writes
- Each file starts with `<!DOCTYPE html>`

---

## Per-Slide Protocol (MANDATORY for EVERY Slide)

### Step 1: Announce Checkpoint (CLI MODE ONLY)

**Skip this step entirely in API mode.**

Before writing each slide file, announce what you're about to do:

```
SLIDE [N]: [Type Name]
Action: generate-new
Layout: [full-width | two-column | centered] | Components: [list of card-patterns used]
```

**Example announcements:**
```
SLIDE 3: Step 1 Question + CFU
Action: generate-new
Layout: centered | Components: title-zone, content-box, cfu-card (animated)

SLIDE 4: Step 1 Answer
Action: generate-new
Layout: two-column | Components: title-zone, content-box, svg-card, answer-card (animated)
```

**If slide contains an SVG graph, add graph workflow:**
```
SLIDE 2: Problem Setup
Action: generate-new
Layout: two-column | Components: title-zone, content-box, svg-card
Graph: Use card-patterns/svg-card.html → modify for X_MAX=10, Y_MAX=100
```

**What goes IN the slide HTML file:**
- The file starts with `<!DOCTYPE html>` - NOTHING before it
- NO checkpoint announcements (those are conversational only)
- NO protocol notes or comments
- ONLY valid HTML content starting with `<!DOCTYPE html>`

---

### Step 2: Determine Slide Type and Layout

CFU and Answer boxes are now STACKED on the same slide (both appear, one after another on click).

| Slide # | Type | Layout Options | Content |
|---------|------|----------------|---------|
| 1 | Teacher Instructions | `two-column` | **Teacher-only (students start on Slide 2).** Big Idea + Learning Targets + Deck Overview |
| 2 | Big Idea | `centered` | Grade/Unit/Lesson + Big Idea badge + statement |
| 3 | Problem Setup | `two-column` or `centered` | problem + visual |
| 4 | Step 1 | `two-column` or `centered` | step content + CFU + Answer (stacked) |
| 5 | Step 2 | `two-column` or `centered` | step content + CFU + Answer (stacked) |
| 6 | Step 3 | `two-column` or `centered` | step content + CFU + Answer (stacked) |
| 7 | Printable | `full-width` | printable format |

**Layout Selection (slides 3-6):**

| Choose `centered` when... | Choose `two-column` when... |
|---------------------------|----------------------------|
| Equation IS the visual | Text + separate visual needed |
| Simple diagram (tape, hanger) | Complex visual (coordinate graph) |
| Step is single operation | Multiple parts to explain |
| Focus on ONE thing | Show text-visual relationship |
| **Diagram IS the content** (not supporting it) | **Diagram supports/illustrates text** |

### ⚠️ The Duplication Test (CRITICAL)

**Before choosing two-column, ask: "Would I say the same thing on both sides?"**

| If this happens... | Use this layout |
|-------------------|-----------------|
| Left explains "two meanings" + Right shows "two meanings" boxes | `centered` - let the diagram BE the explanation |
| Left has equation + Right has graph of that equation | `two-column` - they show DIFFERENT representations |
| Left describes groups + Right shows the same groups visually | `centered` - remove the text, enlarge the visual |

**Example of duplication (BAD - use centered instead):**
```
LEFT COLUMN               RIGHT COLUMN
"Meaning 1: How many      [Box: "Meaning 1:
slices per group?"         How many in each group?"]
"Meaning 2: How many      [Box: "Meaning 2:
groups?"                   How many groups?"]
```
↑ This duplicates! The visual boxes say the same thing as the text. Use `centered` and let the diagram speak for itself with a brief subtitle.

**For `two-column` layout (text + visual side-by-side):**
- Left: Main content (36-48px) + Problem reminder at bottom left corner (≤15 words)
- Right: SVG visual or diagram
- **⚠️ Left and right must show DIFFERENT content**
- Problem reminder uses `card-patterns/simple-patterns/problem-reminder.html` positioned at y=450

**For `centered` layout (stacked hero content):**
- Main: Large equation/diagram centered (hero element)
- Support: Brief text below (optional)
- **Use when the diagram IS the teaching, not just supporting it**

See `reference/layout-presets.md` for pixel dimensions and HTML examples.

**Note:** Practice problems are embedded directly in the Printable slide (slide 7) rather than having separate presentation slides.

---

### Step 3: Add CFU + Answer Boxes (Same Position, PPTX Animation)

**CFU and Answer boxes occupy the SAME position on the same slide. Both use PPTX animation - CFU appears first, then Answer overlays it on the second click.**

Add BOTH boxes BEFORE the closing `</body>` tag on Step slides (4, 5, 6):

**CFU Box (appears on first click):**
```html
<div data-pptx-region="cfu-box" data-pptx-x="653" data-pptx-y="40" data-pptx-w="280" data-pptx-h="115" style="position: absolute; top: 40px; right: 20px; width: 280px; background: #fef3c7; border-radius: 8px; padding: 12px; border-left: 4px solid #f59e0b; z-index: 100;">
  <p style="font-weight: bold; margin: 0 0 6px 0; font-size: 12px; color: #92400e;">CHECK FOR UNDERSTANDING</p>
  <p style="margin: 0; font-size: 13px; color: #1d1d1d;">[CFU question using strategy verb]</p>
</div>
```

**Answer Box (SAME position, appears on second click and overlays CFU):**
```html
<div data-pptx-region="answer-box" data-pptx-x="653" data-pptx-y="40" data-pptx-w="280" data-pptx-h="115" style="position: absolute; top: 40px; right: 20px; width: 280px; background: #dcfce7; border-radius: 8px; padding: 12px; border-left: 4px solid #22c55e; z-index: 101;">
  <p style="font-weight: bold; margin: 0 0 6px 0; font-size: 12px; color: #166534;">ANSWER</p>
  <p style="margin: 0; font-size: 13px; color: #1d1d1d;">[Answer explanation]</p>
</div>
```

**How animation works:**
- Both boxes are on the SAME slide at the SAME position (y=40)
- `data-pptx-region="cfu-box"` appears on FIRST click (yellow box)
- `data-pptx-region="answer-box"` appears on SECOND click (green box overlays yellow)
- Answer box has higher z-index (101) to visually layer on top
- See `card-patterns/simple-patterns/cfu-answer-card.html` for full pattern

---

### Step 4: Compose Slides from Atomic Components

**For ALL slides (1-6, printable generated separately as slide 7):**

1. **ANNOUNCE** checkpoint to user (plain text, CLI mode only)
2. **CHOOSE LAYOUT** from the table above (full-width or two-column)
3. **COMPOSE** slide using atomic card-patterns:
   - **title-zone**: Badge ("STEP N: [VERB]") + Title + optional Subtitle
   - **content-box**: Main text content (instructions, questions, explanations)
   - **svg-card**: Graph or diagram (if visual slide)
   - Use patterns from `card-patterns/` folder as HTML snippets
4. **IF Visual Type = "coordinate-graph"**: Read `04-svg-workflow.md` FIRST
5. **IF Visual Type = "diagram" (non-graph SVG)**: Read `../../reference/diagram-patterns.md` FIRST
   - Includes: tape diagrams, hanger diagrams, double number lines, input-output tables, area models
   - Based on Illustrative Mathematics (IM) curriculum representations
6. **VERIFY** the pre-flight checklist (see `checklists/pre-flight.md`)
7. **WRITE** slide file using Write tool (file starts with `<!DOCTYPE html>`)

### Step 5: Repeat Protocol

For each slide N from 1 to 6:
1. Return to Step 1
2. Announce checkpoint (plain text to user, CLI mode only)
3. Compose slide using card-patterns
4. Write slide file (starts with `<!DOCTYPE html>`, no other content before it)
5. Continue until all slides complete

---

## Visual Type Reference

Your visual type was determined in Phase 1. Here's what each requires:

**Text-only:**
- No graphics - pure text/equation problems
- Use content-box patterns only

**HTML table:**
- Simple data tables with highlighting
- Use `<table>` with inline styles
- See `card-patterns/simple-patterns/content-box.html` for table examples

**SVG visual (ALL other graphics):**
- Coordinate planes and graphs
- Hanger diagrams and balance problems
- Geometric shapes and diagrams
- Number lines and bar models
- Any custom visual representation (coins, objects, arrays)

**For SVG visuals, you MUST:**
1. Read `04-svg-workflow.md` for coordinate graphs
2. Read `../../reference/diagram-patterns.md` for other diagram types
3. Wrap in container with `data-pptx-region="svg-container"`
4. Include position attributes: `data-pptx-x`, `data-pptx-y`, `data-pptx-w`, `data-pptx-h`
5. **⚠️ CRITICAL: Wrap EVERY distinct element in `<g data-pptx-layer="...">`**

### ⚠️ SVG Layer Requirement (MANDATORY)

**Without `data-pptx-layer`, ALL SVG content becomes ONE merged image. Teachers cannot click, move, or edit individual elements.**

Every SVG element group MUST have its own layer:
```html
<svg viewBox="0 0 400 300">
  <g data-pptx-layer="label-title">
    <text>Title here</text>
  </g>
  <g data-pptx-layer="shape-row-1">
    <!-- First row of shapes -->
  </g>
  <g data-pptx-layer="shape-row-2">
    <!-- Second row of shapes -->
  </g>
  <g data-pptx-layer="label-equation">
    <text>48 ÷ 6 = ?</text>
  </g>
</svg>
```

**Layer naming:**
- `label-X` for text labels
- `shape-N` or `shape-row-N` for shapes/objects
- `base` for background elements
- `arrow-X` for arrows/annotations

---

## Using the Correct GRAPH PLAN

**CRITICAL: Use EACH SCENARIO'S graphPlan, NOT the mastery check's graphPlan.**

The mastery check (`problemAnalysis.graphPlan`) is for the student's exit ticket/assessment - it is NEVER shown in these slides. Each scenario has its own numbers/context, so each needs its own graphPlan:

| Slides | Source | GraphPlan to Use |
|--------|--------|------------------|
| 2-8 (Worked Example) | Scenario 1 | `scenarios[0].graphPlan` |
| 9 (Printable - Practice 1 & 2) | Scenarios 2 & 3 | `scenarios[1].graphPlan` and `scenarios[2].graphPlan` |

Each GRAPH PLAN contains the semantic decisions for that scenario:
- **Equations** with correct slope/y-intercept for that scenario's numbers
- **Scale** (X_MAX, Y_MAX) appropriate for that scenario's values
- **Line endpoints** (startPoint, endPoint) calculated for that scenario
- **keyPoints** with correct coordinates for that scenario
- **Annotations** type and position

**You MUST implement exactly what each scenario's GRAPH PLAN specifies.** Do NOT use the mastery check's graphPlan. Do NOT recalculate or change the scale.

---

## Context-Aware Generation Modes

### Mode: Full (Default)
Generate all slides from scratch.

### Mode: Continue
Resume from where generation was interrupted.
- DO NOT regenerate existing slides
- Match style of existing slides exactly
- Start from next slide number

### Mode: Update
Regenerate only specific slides with targeted changes.
- Output ONLY the slides marked for update
- Maintain same structure as existing slides
- Use original slide numbers

---

## Output Format

**Each slide file must:**
- Start with `<!DOCTYPE html>` as the very first characters
- Contain ONLY valid HTML (no checkpoint comments, no protocol notes)
- End with `</html>`

**NEVER include in slide files:**
- Checkpoint announcements (those are conversational text to user)
- Protocol comments or notes
- Any text before `<!DOCTYPE html>`

When outputting multiple slides in conversation (API mode), separate with:
```
===SLIDE_SEPARATOR===
```
