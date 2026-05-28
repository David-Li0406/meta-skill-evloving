---
name: building-uiux
description: Use this skill when implementing user interfaces or user experiences, guiding through exploration of design variations, frontend setup, iteration, and proper integration.
---

# Skill body

## Overview

This skill guides you through implementing user interfaces and experiences with an emphasis on exploration, feedback, and proper integration.

**Core principle:** Explore variations, iterate with feedback, ensure proper integration.

**Announce at start:** "I'm using the Building UI/UX skill to implement your interface."

## The Process

### Phase 1: Scope & Variation Planning

1. **Ask the user:**
   - "Would you like to:
     - See multiple UI variations to choose from?
     - Go with a single design approach?"

2. **If multiple variations:**
   - Ask what kinds of variations they want (e.g., minimalist vs rich, card-based vs list-based, light vs dark).
   - Aim for 2-4 distinct approaches.
   - Plan to implement all variations in a way that allows easy comparison.

### Phase 2: Frontend Environment Setup

**For web projects:**

1. Check if the dev server is running:
   - If not, identify the start command (e.g., `npm run dev`, `npm start`).
   - Start the dev server.
   - Note the localhost URL (typically `http://localhost:3000` or similar).
   - Inform user: "Starting dev server at [URL]".

**For other UI types:**
- Identify appropriate preview/testing mechanism and set up accordingly.

### Phase 3: Implementation

**When implementing multiple variations:**

- Stack variations in a way that makes comparison easy. For web UIs, this typically means:
  - Render all variations on a single page, stacked vertically.
  - Add clear section dividers/headings for each variation.
  - Use consistent spacing between variations.
  - Ensure each variation is self-contained and functional.

**Example for React:**
```tsx
export default function UIExploration() {
  return (
    <div className="ui-exploration">
      <section className="variation">
        <h2>Variation 1: Minimalist</h2>
        {/* Implementation of the minimalist design */}
      </section>
      {/* Additional variations go here */}
    </div>
  );
}
```