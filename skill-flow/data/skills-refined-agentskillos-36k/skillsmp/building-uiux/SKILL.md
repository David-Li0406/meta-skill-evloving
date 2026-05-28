---
name: Building UI/UX
description: Use when implementing user interfaces or user experiences - guides through exploration of design variations, frontend setup, iteration, and proper integration
---

<required>
*CRITICAL* Add the following steps to your Todo list using TodoWrite:

1. Ask user if they want to experiment with multiple UI variations or see a single design
2. If user wants multiple variations, ask what kinds of variations to try
3. If building a web frontend and it's not running, start the dev server and note the localhost URL
4. Implement the UI/UX design(s)
5. Ask user for feedback on the design
6. Iterate based on feedback
7. Ensure the new UI is properly wired up and integrated
</required>

# Building UI/UX

## Overview

This skill guides you through implementing user interfaces and experiences with an emphasis on exploration, feedback, and proper integration.

**Core principle:** Explore variations, iterate with feedback, ensure proper integration.

**Announce at start:** "I'm using the nojo Building UI/UX skill to implement your interface."

## The Process

### Phase 1: Scope & Variation Planning

**Ask the user:**

"Would you like to:
- See multiple UI variations to choose from?
- Go with a single design approach?"

**If multiple variations:**
- Ask what kinds of variations they want (e.g., minimalist vs rich, card-based vs list-based, light vs dark)
- Aim for 2-4 distinct approaches
- Plan to implement all variations in a way that allows easy comparison

### Phase 2: Frontend Environment Setup

**For web projects:**

Check if the dev server is running:
- If not, identify the start command (e.g., `npm run dev`, `npm start`)
- Start the dev server
- Note the localhost URL (typically `http://localhost:3000` or similar)
- Inform user: "Starting dev server at [URL]"

**For other UI types:**
- Identify appropriate preview/testing mechanism
- Set up accordingly

### Phase 3: Implementation

**When implementing multiple variations:**

Stack variations in a way that makes comparison easy. For web UIs, this typically means:
- Render all variations on a single page, stacked vertically
- Add clear section dividers/headings for each variation
- Use consistent spacing between variations
- Ensure each variation is self-contained and functional

**Example for React:**
```tsx
export default function UIExploration() {
  return (
    <div className="ui-exploration">
      <section className="variation">
        <h2>Variation 1: Minimalist</h2>
        <MinimalistLogin />
      </section>

      <section className="variation">
        <h2>Variation 2: Modern Gradient</h2>
        <ModernLogin />
      </section>

      <section className="variation">
        <h2>Variation 3: Classic Corporate</h2>
        <ClassicLogin />
      </section>
    </div>
  );
}
```

**When implementing a single design:**
- Focus on clean, production-ready implementation
- Follow project conventions and style guides
- Ensure responsive design if applicable

### Phase 4: Feedback & Iteration

**Present to user:**
- Share the localhost URL or preview mechanism
- Briefly describe each variation (if multiple)
- Ask: "What do you think? Any changes you'd like to see?"

**Iterate based on feedback:**
- Make requested changes
- Continue asking for feedback until satisfied
- Be ready to combine elements from different variations

### Phase 4b: Visual Verification with MCP (Optional)

**When to use:** When you want to verify UI changes without asking the user to refresh their browser, or to capture evidence of the implementation.

**Using Playwright MCP tools:**

1. **Navigate to the dev server:**
   - `browser_navigate` to the localhost URL

2. **Capture visual evidence:**
   - `browser_take_screenshot` to save a PNG for visual review

3. **Verify interactions work:**
   - `browser_snapshot` to get element refs from accessibility tree
   - `browser_click`, `browser_type` to test interactive elements
   - `browser_wait_for` to verify state changes

4. **Check for console errors:**
   - `browser_console_messages` with level="error" to catch runtime errors before the user sees them

**Note:** This is supplemental to user feedback, not a replacement. Always get human feedback on design choices.

### Phase 5: Integration & Wiring

**Ensure proper integration:**

- Remove exploration scaffolding (if used)
- Wire up to actual data sources/APIs
- Connect to routing/navigation
- Add proper state management
- Implement error handling
- Add loading states if applicable
- Test all interactive elements
- Verify accessibility basics

**MCP verification (recommended):**
- Use `browser_snapshot` to verify all interactive elements are accessible
- Check `browser_console_messages` for runtime errors
- Test critical user flows with MCP tools before handing off

**Common integration points to check:**
- Form submissions → backend endpoints
- Navigation → routing system
- Authentication → auth context/store
- Data fetching → API layer
- Error boundaries → error handling
- Responsive behavior → breakpoints
