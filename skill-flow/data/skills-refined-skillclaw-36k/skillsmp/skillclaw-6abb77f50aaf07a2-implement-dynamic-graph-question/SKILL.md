---
name: implement-dynamic-graph-question
description: Use this skill when creating interactive coordinate plane questions where students can draw linear lines and explore relationships between variables.
---

# Skill body

Use this skill when creating questions where students:
- Draw lines on an interactive coordinate plane
- Explore linear relationships by drawing from points
- Create proportional relationships from the origin
- Compare multiple linear scenarios

## When to Use This Pattern

**Perfect for:**
- "Draw a line showing a proportional relationship"
- "Draw a line from (0,0) through (5, 10)"
- "Draw lines to match the given equations"
- Interactive slope/linear function exploration
- Comparing rates by drawing multiple lines

**Not suitable for:**
- Static graph reading → use [implement-static-graph-question](../implement-static-graph-question/SKILL.md)
- Simple table completion → use [implement-table-question](../implement-table-question/SKILL.md)
- Pre-defined graph manipulation (use slider pattern)

## Technology Stack

**Uses p5.js (NOT D3)** for the coordinate plane because:
- Better for real-time interactive drawing
- Simpler mouse/touch event handling
- Built-in animation and rendering loop
- Easier geometric operations

**Integrates with D3** for:
- Layout and cards (intro, explanation, etc.)
- State management
- Message protocol

## Components Required

**Copy these:**

### P5.js Coordinate Plane (Required)
- `snippets/coordinate-plane-p5.js` → Full p5 sketch in instance mode

### D3 Cards (Optional)
- `.claude/skills/question-types/snippets/cards/standard-card.js` → `createStandardCard()`
- `.claude/skills/question-types/snippets/cards/explanation-card.js` → `createExplanationCard()`

### P5.js Library (Required)
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.7.0/p5.js"></script>
```

## Quick Start

1. **Study the base implementation**:
   ```bash
   cat alex/coordinatePlane/linear-graph-drawing.ts
   cat .claude/skills/question-types/implement-dynamic-graph-question/snippets/coordinate-plane-p5.js
   ```

2. **Copy the p5 coordinate plane snippet** into your chart.js IIFE

3. **Follow the integration pattern below**

## State Shape

```javascript
function createDefaultState() {
  return {
    drawnLines: [],  // [{ start: {x, y}, end: {x, y} }, ...]
    explanation: ""
  };
}
```

## Core Integration Pattern

### 1. Load P5.js (in chart.html for testing)

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.7.0/p5.js"></script>
</head>
<body>
  <!-- Your interactive graph will be rendered here -->
</body>
</html>
```