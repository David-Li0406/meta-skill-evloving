# Stitch Prompting Best Practices

## Contents
- [Golden Rules](#golden-rules)
- [Prompt Length Guidelines](#prompt-length-guidelines)
- [Visual Style Tips](#visual-style-tips)
- [Common Pitfalls](#common-pitfalls)
- [UI/UX Vocabulary](#uiux-vocabulary)

---

## Golden Rules

### Rule 1: Be Specific and Incremental
Generic prompts produce generic results. Focus on one screen/component at a time.

```
❌ "Create a landing page"
✅ "Mobile product detail page for herbal tea shop with image gallery,
   price, reviews, add-to-cart. Neutral Japandi palette, minimal typography."
```

### Rule 2: One Major Change Per Prompt
Multiple changes cause Stitch to "forget" or break existing layouts.

```
❌ "Add filters, change title alignment, and add a gear icon"
✅ Three separate prompts:
   1. "Add filter dropdowns above the task table"
   2. "Move page title to the left, aligned with the table"
   3. "Add gear icon to top-right for admin settings"
```

### Rule 3: Use UI/UX Terminology
Standard vocabulary yields better results than generic descriptions.

---

## Prompt Length Guidelines

| Length | Risk Level | Use Case |
|--------|------------|----------|
| < 500 chars | ✅ Safe | Single component or refinement |
| 500-800 chars | ✅ Good | Simple screen or targeted update |
| 800-1500 chars | ✅ Optimal | Full screen with multiple components |
| 1500-2500 chars | ⚠️ Caution | Complex screen, may need splitting |
| > 2500 chars | ❌ Risky | Will likely omit content |

**Principle:** Use structured bullets with specs, not prose paragraphs. 1000 specific characters in bullet format beats 2000 vague prose.

---

## Visual Style Tips

### Colors
- **Use hex codes:** `#FFA344` is precise, "amber" is ambiguous
- **Specify usage:** "Primary: #2563EB, accent: #F59E0B, background: #09090b"
- **Mood-based OK too:** "Warm, inviting palette" when exploring

### Typography
- Be specific: "Playful sans-serif" or "Serif headings, sans-serif body"
- Include sizing hints: "18px bold title, 14px body"

### Imagery
- Describe the vibe: "Lifestyle photography, not sterile product shots"
- Coordinate with theme: "Ensure images match the dark theme"

### Reference Apps
Stitch understands design references:
- "Warp Terminal aesthetic"
- "Linear-style minimal"
- "Notion-like cards"
- "VS Code dark theme"

---

## Common Pitfalls

### ASCII Diagrams Don't Work
Stitch interprets ASCII as literal text, not spatial relationships.

```
❌ Pasting ASCII layout diagrams
✅ Plain language: "Three-panel layout: left sidebar 280px,
   center scrollable content, right toggleable file tree"
```

### Specs Documents Overwhelm
A 1000-line UI spec with ASCII diagrams and tables will fail.

**Solution:** Convert spec sections into focused prompts:
```
SPEC SECTION:
"### Collapsible Sidebar
Location: Left edge, full height
Default State: Expanded (280px)
Sections: Projects, Recent Sessions, New Project button"

CONVERTED TO PROMPT:
"Design collapsible left sidebar for developer tool.
Full height, 280px expanded. Contains:
- Search input at top
- PROJECTS section with folder icons
- RECENT SESSIONS with timestamps
- New Project button at bottom
Dark theme (#161b22 bg), light text (#e6edf3)."
```

### Technical Over-Specification
CSS variable names add noise without helping.

```
❌ "Use --bg-canvas: #0d1117 for Layer 0, box-shadow: 0 8px 24px..."
✅ "Deep dark background (#0d1117) with lighter surfaces for panels.
   Modals feel elevated with subtle shadows."
```

### Layout Breaks on Edit
Adding features can regenerate entire layouts unexpectedly.

**Solution:**
- One change per prompt
- Never combine layout + component changes
- Take mental note of working states before major edits

---

## UI/UX Vocabulary

Use these terms for better Stitch interpretation:

| Category | Preferred Terms |
|----------|-----------------|
| **Layout** | navigation bar, sidebar, card layout, grid, sticky header, hero section, footer |
| **Components** | CTA button, search bar, dropdown, modal, toast, accordion, tooltip, badge |
| **Behavior** | on click, hover state, loading spinner, empty state, disabled state |
| **Visuals** | full-width hero, ghost button, high-contrast CTA, dark theme, rounded corners |
| **Structure** | padding, margin, gap, flex row, grid 2-column, max-width, scrollable |
