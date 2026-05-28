# Phase 5: Updating Existing Decks

**Responsibility:** Targeted changes to existing worked example decks.

**Delegates to:**
- `card-patterns/simple-patterns/` → Title zones, content boxes, CFU/Answer
- `card-patterns/complex-patterns/` → SVG graphs, annotations, printable slides
- `04-svg-workflow.md` → Pixel calculation formulas

---

## When to Use This Phase

| Situation | Action |
|-----------|--------|
| Changing text content | Use this phase |
| Fixing typos | Use this phase |
| Updating graph data | Use this phase |
| Modifying practice problems | Use this phase |
| Changing strategy or flow | Rerun full skill (Phases 1-4) |
| Adding/removing slides | Rerun full skill (Phases 1-4) |

---

## ⚠️ REQUIRED: Read Before Editing

**You MUST read the relevant pattern files before making changes.**

### For ANY Slide Edit
```
READ: ../03-generate-slides/01-slide-by-slide.md
READ: ../03-generate-slides/02-technical-rules.md
```

### For Text/Content Updates
```
READ: ../03-generate-slides/card-patterns/simple-patterns/title-zone.html
READ: ../03-generate-slides/card-patterns/simple-patterns/content-box.html
READ: ../03-generate-slides/card-patterns/simple-patterns/cfu-answer-card.html
```

### For SVG Graph Updates
```
READ: ../03-generate-slides/card-patterns/complex-patterns/graph-snippet.html
READ: ../03-generate-slides/04-svg-workflow.md
```

### For Printable Slide Updates (slide-7)
```
READ: ../03-generate-slides/card-patterns/complex-patterns/printable-slide-snippet.html
```

---

## Update Procedures

### Procedure A: Text Content Updates

**Step 1:** Read the existing slide

**Step 2:** Identify the component from the pattern files:
- Badge/Title/Subtitle → `simple-patterns/title-zone.html`
- Body text/lists → `simple-patterns/content-box.html`
- CFU/Answer box → `simple-patterns/cfu-answer-card.html`

**Step 3:** Use Edit tool with EXACT string matching
- Change ONLY the text content
- PRESERVE all `data-pptx-*` attributes
- PRESERVE all `style` attributes

**Step 4:** Sync to database
```bash
source .env.local && node .claude/skills/create-worked-example-sg/scripts/sync-to-db.js {slug}
```

---

### Procedure B: SVG Graph Updates

**Step 1:** Read these files FIRST:
```
READ: ../03-generate-slides/card-patterns/complex-patterns/graph-snippet.html
READ: ../03-generate-slides/04-svg-workflow.md
```

**Step 2:** Calculate new pixel positions using:
```
pixelX = 40 + (dataX / X_MAX) * 220
pixelY = 170 - (dataY / Y_MAX) * 150
```

**Step 3:** Update data elements:
- Line coordinates (`x1`, `y1`, `x2`, `y2`)
- Circle positions (`cx`, `cy`)
- Annotation text and positions

**Step 4:** PRESERVE:
- All `data-pptx-layer` attributes
- Grid lines (unless scale changes)
- Axes and tick marks
- Marker definitions in `<defs>`

**Step 5:** Sync to database

---

### Procedure C: Printable Slide Updates (slide-7)

**Step 1:** Read the pattern FIRST:
```
READ: ../03-generate-slides/card-patterns/complex-patterns/printable-slide-snippet.html
```

**Step 2:** Edit content ONLY within the `<div class="print-page">` wrappers

**Step 3:** PRESERVE these elements exactly:
- `<div class="slide-container" style="...overflow-y: auto...">`
- `<div class="print-page" style="width: 8.5in; height: 11in; ...">`
- The entire `<style>` block with `@media print` rules
- `@page { size: letter portrait; margin: 0; }`

**Step 4:** Sync to database

---

## Critical: Preserve PPTX Attributes

**Every edit MUST preserve `data-pptx-*` attributes.**

```html
<!-- These attributes enable PPTX export - NEVER remove -->
<div data-pptx-region="badge" data-pptx-x="20" data-pptx-y="16" data-pptx-w="180" data-pptx-h="35">
```

| Attribute | If Removed |
|-----------|------------|
| `data-pptx-region` | Element won't export to PPTX |
| `data-pptx-x/y/w/h` | Element positioned wrong in PPTX |
| `data-pptx-layer` | SVG layers won't separate in PPTX |
| `data-pptx-region="cfu-box"` | CFU won't animate (appear on click) |
| `data-pptx-region="answer-box"` | Answer won't animate |

---

## Browser UI: Multi-Slide Edit

For batch edits via the wizard at `/scm/workedExamples/create`:

1. Select slides with checkboxes
2. Set mode: **Edit** (purple) or **Context** (gray dashed)
3. Enter instructions
4. Click "Apply to All"

API: `POST /api/scm/worked-examples/edit-slides`

---

## Verification Checklist

**Before syncing, verify:**

- [ ] All `data-pptx-*` attributes preserved
- [ ] Slides are 960×540px
- [ ] Text in `<p>`, `<h1-6>`, `<ul>`, `<ol>` tags
- [ ] CFU/Answer boxes have correct `data-pptx-region`
- [ ] SVG layers have `data-pptx-layer` attributes
- [ ] Printable slide has `@media print` styles intact

---

## Quick Reference

| Pattern Type | Files |
|--------------|-------|
| Title/Badge | `simple-patterns/title-zone.html` |
| Content | `simple-patterns/content-box.html` |
| CFU/Answer | `simple-patterns/cfu-answer-card.html` |
| SVG Graph | `complex-patterns/graph-snippet.html` + `04-svg-workflow.md` |
| Annotations | `complex-patterns/annotation-snippet.html` |
| Printable | `complex-patterns/printable-slide-snippet.html` |
