# Pre-Flight Checklist

**Verify BEFORE writing each slide.**

---

## The 3-Second Scan Test (VERIFY FIRST)

**Can a student understand the slide's key point in 3 seconds?**

If not, it's too cluttered. Remove content until it passes.

---

## Conciseness Checks

- [ ] **NO explanatory subtitles** (no "First, let's figure out...")
- [ ] **Problem reminder <= 15 words** (e.g., "30 nuggets total. 6 per student. How many students?")
- [ ] **CFU question: ONE question, <= 12 words** (no two-part questions!)
- [ ] **Answer box <= 25 words** (1-2 sentences only)
- [ ] **Left/Right columns are COMPLEMENTARY** (text left, visual right - NO duplication)
- [ ] **No redundant info boxes** (no "Reading the graph: ..." boxes)
- [ ] **Visuals are self-explanatory** (no text boxes explaining what's already shown)

---

## ⚠️ The Duplication Test (two-column layouts)

**If using two-column, verify you're not duplicating:**

- [ ] Left column says something DIFFERENT than the visual on the right
- [ ] If left explains "meanings" and right shows "meanings" boxes → use `centered` instead
- [ ] If left describes groups and right shows those same groups → use `centered` instead

**Ask:** "Am I saying the same thing twice?" If yes, switch to `centered` and let the diagram be the content.

---

## Technical Requirements

- [ ] File starts with `<!DOCTYPE html>` (NO checkpoint, NO comments before it)
- [ ] Body: `width: 960px; height: 540px`
- [ ] All text in `<p>`, `<h1-6>`, `<ul>`, `<ol>` (NOT bare text in divs)
- [ ] Layout uses `.row`/`.col` classes (NOT inline `display: flex`)
- [ ] Fonts: Arial, Georgia, Courier New only
- [ ] **Colors: 6-digit hex ONLY (e.g., #ffffff) - NEVER rgb/rgba/named colors**
- [ ] Backgrounds/borders on `<div>` only (NOT on `<p>`, `<h1>`)
- [ ] No onclick handlers or CSS animations (D3.js is allowed for diagrams)
- [ ] Light theme (white #ffffff, dark text #1d1d1d)

---

## PPTX Export (data-pptx attributes)

- [ ] Key regions have `data-pptx-region`, `data-pptx-x/y/w/h` attributes
- [ ] Badge: `data-pptx-x="20" data-pptx-y="16" data-pptx-w="100" data-pptx-h="30"`
- [ ] Title: `data-pptx-x="130" data-pptx-y="16" data-pptx-w="810" data-pptx-h="30"`
- [ ] Subtitle: `data-pptx-x="20" data-pptx-y="55" data-pptx-w="920" data-pptx-h="30"`
- [ ] CFU/Answer boxes: `data-pptx-x="653" data-pptx-y="40" data-pptx-w="280" data-pptx-h="115"`

---

## If Right-Column Has Visual Content

- [ ] Each distinct element has its own `data-pptx-region="visual-*"`
- [ ] Each element has `data-pptx-x`, `data-pptx-y`, `data-pptx-w`, `data-pptx-h`
- [ ] Wrapper div has NO data-pptx-region
- [ ] Coordinates don't overlap (stack with 10-16px gaps)

---

## If SVG Visual

- [ ] Read `04-svg-workflow.md` first
- [ ] SVG wrapped in container with `data-pptx-region="svg-container"` and position attributes
- [ ] All `<text>` elements have `font-family="Arial"`
- [ ] SVG container in SAME position as other step slides
- [ ] **⚠️ EVERY element group wrapped in `<g data-pptx-layer="...">`** (REQUIRED for editability)
- [ ] Layer names follow convention: `label-X`, `shape-N`, `base`, `arrow-X`
- [ ] If using D3.js: visualization code creates layers with `data-pptx-layer` attributes
- [ ] If using D3.js: include `<script src="https://d3js.org/d3.v7.min.js"></script>` in head

---

## If Slide Has CFU/Answer Boxes (Step Slides 4-6)

- [ ] BOTH CFU and Answer boxes are on the SAME slide (stacked)
- [ ] CFU box has `data-pptx-region="cfu-box"` at y=40
- [ ] Answer box has `data-pptx-region="answer-box"` at y=150
- [ ] Both are positioned with absolute positioning (top-right, stacked vertically)
- [ ] CFU question references strategy verb
- [ ] Answer is direct, <= 25 words
- [ ] Problem reminder is at bottom left corner (y=450)
