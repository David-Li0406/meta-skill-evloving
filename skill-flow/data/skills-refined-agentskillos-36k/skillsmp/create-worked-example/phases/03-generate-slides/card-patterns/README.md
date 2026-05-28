# Card Patterns Index

This folder contains atomic HTML patterns for composing slides. **Always copy from these files - never write HTML from scratch.**

---

## Simple Patterns (Fill Placeholders)

| File | Purpose |
|------|---------|
| `simple-patterns/title-zone.html` | Badge + Title + Subtitle |
| `simple-patterns/content-box.html` | Text container (prose, lists, equations, tables) |
| `simple-patterns/problem-reminder.html` | Condensed problem summary at bottom left corner (<=15 words) |
| `simple-patterns/cfu-answer-card.html` | CFU/Answer boxes stacked on same slide (animated, appear on click) |

---

## Complex Patterns (Clone and Modify)

| File | Purpose |
|------|---------|
| `complex-patterns/slide-teacher-instructions.html` | Teacher Instructions (slide 1) - **Teacher-only, students start on Slide 2.** Two-column: Big Idea + Learning Targets (left), Deck Overview (right) |
| `complex-patterns/slide-big-idea.html` | Big Idea (slide 2) - student-facing with Grade/Unit/Lesson |
| `complex-patterns/graph-snippet.html` | Complete coordinate plane - for coordinate graphs only |
| `complex-patterns/annotation-snippet.html` | Graph annotations (labels, arrows) |
| `complex-patterns/visual-card-layers.html` | Multi-element right column |
| `complex-patterns/printable-slide-snippet.html` | Printable worksheet (slide 7) |
| `complex-patterns/d3-diagram-template.html` | **D3.js template** for programmatic diagrams |
| `svg-card.html` | SVG container wrapper |

---

## D3.js Diagrams (Recommended Default)

**Use D3 for all non-graph diagrams.** It produces visually aligned, professional graphics with automatic spacing.

`d3-diagram-template.html` shows the structure and patterns. Adapt the D3 code for each specific diagram type:
- Tape diagrams
- Double number lines
- Hanger diagrams
- Area models
- Any custom diagram

**Benefits:**
- Automatic equal spacing and alignment
- Proportional positioning
- Easy to adjust values without recalculating coordinates

**Critical:** All D3 elements must have `data-pptx-layer` attributes for PPTX export.

**Exception:** Coordinate graphs (`svgSubtype: coordinate-graph`) do NOT use D3 - use `graph-snippet.html` instead.

---

## Workflow

**Simple patterns:** Copy → Replace placeholders → Paste

**Complex patterns:** Copy → Calculate values (see `04-svg-workflow.md`) → Modify → Verify
