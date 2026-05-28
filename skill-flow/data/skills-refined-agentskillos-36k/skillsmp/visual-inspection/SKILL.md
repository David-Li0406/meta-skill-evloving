---
name: visual-inspection
description: Perform automated visual design inspection using Playwright MCP. Captures screenshots at mobile (375px), tablet (768px), and desktop (1280px) viewports, then analyzes them for design consistency, layout shifts, terminal aesthetic adherence, and quality issues. Use this skill PROACTIVELY after ANY design/UI changes, when adding components, modifying layouts, updating styles, or before completing design-related tasks.
allowed-tools: Read, Bash, WebFetch
---

# Visual Inspection Skill

## Purpose

This skill automates visual quality assurance for the blog using Playwright MCP. It ensures all UI changes maintain the terminal aesthetic, avoid generic AI-generated looks, and remain consistent across devices.

## When to Use This Skill

**Use PROACTIVELY for ALL visual/design changes:**

- After modifying layouts, components, or styles
- When adding new UI components or pages
- When updating colors, spacing, typography, or borders
- Before completing any design-related task
- To verify responsive behavior across devices
- When checking for unwanted layout shifts
- To validate design consistency with existing components

**Do NOT wait for the user to ask.** This skill should be your first step after implementing any UI change.

## Requirements

- **Playwright MCP server** configured in `.claude.json` (already set up for this project)
- **Dev server** running on `localhost:4321` (`pnpm dev`)

## Visual Inspection Workflow

### Step 1: Check Dev Server Status and Start if Needed

**IMPORTANT:** Track whether the server was already running before starting it. You will need this information at the end to know whether to stop the server.

Check if the dev server is already running on `localhost:4321`:

```bash
node .claude/skills/visual-inspection/scripts/visual-inspection.js check-server
```

**Note the result:**

- If the server IS running: Remember that `SERVER_WAS_ALREADY_RUNNING = true`
- If the server is NOT running: Remember that `SERVER_WAS_ALREADY_RUNNING = false`, then start it:

```bash
node .claude/skills/visual-inspection/scripts/visual-inspection.js start-server
```

The start-server command will wait for the server to be ready before returning.

### Step 2: Capture Screenshots at All Viewports

For each page you need to inspect (e.g., homepage `/`, blog index `/blog/`, individual posts `/blog/post-slug/`):

**Desktop (1280px width):**

```
Use browser_navigate to go to http://localhost:4321/path
Use browser_resize to set viewport width=1280, height=800
Use browser_take_screenshot with filename="desktop-pagename-YYYY-MM-DD.png"
```

**Tablet (768px width):**

```
Use browser_resize to set viewport width=768, height=1024
Use browser_take_screenshot with filename="tablet-pagename-YYYY-MM-DD.png"
```

**Mobile (375px width):**

```
Use browser_resize to set viewport width=375, height=667
Use browser_take_screenshot with filename="mobile-pagename-YYYY-MM-DD.png"
```

**Important:**

- Use descriptive filenames that include viewport size, page name, and date
- Do NOT include the `.playwright-mcp/` directory in the filename - the Playwright MCP tool automatically saves to that directory
- Screenshots will be saved to `.playwright-mcp/` in the project root

### Step 3: Test Interactive States (Hover/Focus)

Interactive elements should have polished hover and focus states. Use Playwright to test these programmatically.

**Common elements to test:**

- Navigation links
- Buttons (theme toggle, submit buttons, etc.)
- Blog post cards/links
- Social media icons
- Email links

**Workflow for testing hover states:**

1. **Get a page snapshot** to identify element references:

```
Use browser_snapshot to get the accessibility tree with element refs
```

2. **Hover over interactive elements** and capture screenshots:

```
Use browser_hover with element="Nav link" ref="e6"
Use browser_take_screenshot with filename="hover-nav-link-2026-01-09.png"
```

3. **Test focus states** by tabbing through elements:

```
Use browser_press_key with key="Tab" to move focus
Use browser_take_screenshot with filename="focus-state-2026-01-09.png"
```

**What to verify:**

- [ ] Hover states are visible and intentional (not just default browser styles)
- [ ] Color changes follow the design system (cyan/teal accents)
- [ ] Transitions are smooth, not jarring
- [ ] Focus indicators are visible for keyboard navigation (accessibility)
- [ ] Hover effects don't cause layout shifts
- [ ] Interactive feedback matches across similar elements (consistency)

**Example hover test sequence:**

```
1. browser_navigate to http://localhost:4321
2. browser_snapshot (note the refs for nav links, social icons, etc.)
3. browser_hover element="Home nav link" ref="e6"
4. browser_take_screenshot filename="hover-nav-home.png"
5. browser_hover element="LinkedIn icon" ref="e10"
6. browser_take_screenshot filename="hover-social-linkedin.png"
7. browser_hover element="Theme toggle button" ref="e24"
8. browser_take_screenshot filename="hover-theme-toggle.png"
```

**Tip:** Compare hover screenshots against the design system to ensure accent colors and transition styles match expectations.

### Step 4: Analyze Screenshots

Use the Read tool to view each screenshot (Claude Code can read images). For each screenshot, check:

#### Design Quality Checklist

**CRITICAL: Avoid Generic AI-Generated Looks**

- [ ] Does this look like a generic template? (If yes, flag immediately)
- [ ] Is it consistent with other components in the project?
- [ ] Does it match the terminal/developer aesthetic?
- [ ] Are interactions smooth, intentional, and polished?
- [ ] Would a user recognize this as custom-designed (not AI-generated)?

**Terminal Aesthetic Compliance**

- [ ] Uses monospace typography where appropriate
- [ ] Accent colors: bright cyan (#07f5bd) for dark mode, teal (#00b894) for light mode
- [ ] Clean, professional, developer-friendly appearance
- [ ] Smooth dark/light mode transitions
- [ ] NO generic rounded corners everywhere (avoid rounded-lg on everything)
- [ ] NO default Tailwind button styles (blue bg, white text)
- [ ] NO cookie-cutter card shadows (shadow-md/lg)
- [ ] NO predictable hover effects (simple color changes)

**Design Consistency**

- [ ] Border radius matches existing components
- [ ] Shadows match existing patterns
- [ ] Spacing follows established scale
- [ ] Colors from the defined palette (reference design-system.md)
- [ ] Typography consistent with existing components
- [ ] If one component uses `border border-border-default`, all borders follow this pattern

**Layout & Responsiveness**

- [ ] No unwanted layout shifts between viewports
- [ ] Content remains readable at all sizes
- [ ] Interactive elements are appropriately sized for touch (minimum 44x44px on mobile)
- [ ] Navigation is accessible on all devices
- [ ] Images scale properly without distortion
- [ ] Text doesn't overflow containers

**Accessibility**

- [ ] Text contrast meets WCAG 2.1 AA (4.5:1 minimum for body text)
- [ ] Interactive elements have visible focus states
- [ ] Color is not the only indicator of state changes
- [ ] Touch targets are appropriately sized (44x44px minimum)

### Step 5: Report Findings

Provide a structured report:

```markdown
## Visual Inspection Report

**Page:** [page name]
**Date:** [YYYY-MM-DD]
**Viewports Tested:** Desktop (1280px), Tablet (768px), Mobile (375px)

### ✅ Passed Checks

- [List what looks good]

### ⚠️ Issues Found

1. **[Issue category]**: [Description]
    - Screenshot: `[filename].png` (in `.playwright-mcp/`)
    - Severity: Critical/High/Medium/Low
    - Recommendation: [How to fix]

### 🎨 Design Consistency

- [Comment on consistency with existing components]
- [Comment on terminal aesthetic adherence]

### 📱 Responsive Behavior

- [Comment on layout shifts, breakpoints, mobile usability]

### 🖱️ Interactive States

- [Comment on hover effects - are they polished and consistent?]
- [Comment on focus indicators - are they visible for keyboard navigation?]
- [Comment on transitions - are they smooth or jarring?]

### ♿ Accessibility Notes

- [Comment on contrast, focus states, touch targets]
```

### Step 6: Clean Up - Stop Dev Server if Started

**IMPORTANT:** Only stop the dev server if YOU started it in Step 1.

Check your notes from Step 1:

- If `SERVER_WAS_ALREADY_RUNNING = true`: Do NOT stop the server. Leave it running for the user.
- If `SERVER_WAS_ALREADY_RUNNING = false`: Stop the server:

```bash
node .claude/skills/visual-inspection/scripts/visual-inspection.js stop-server
```

This ensures you don't leave background processes running that the user didn't ask for, while also not disrupting a server the user was already using.

## Design System Reference

Always cross-reference findings with `.claude/context/design-system.md` for:

- Color palette and usage
- Spacing scale
- Typography system
- Component patterns
- Border and shadow standards

## Common Issues to Watch For

1. **Generic AI-generated appearance** - The #1 priority. Flag immediately.
2. **Inconsistent border radius** - All components should use the same values
3. **Layout shifts** - Content jumping between viewports
4. **Poor contrast** - Text that's hard to read in light or dark mode
5. **Missing hover states** - Interactive elements need feedback
6. **Overflow issues** - Text or images breaking out of containers
7. **Inconsistent spacing** - Different gaps between similar elements

## Helper Script

A JavaScript helper script is available at `scripts/visual-inspection.js` with utilities for managing screenshots and the dev server.

Available commands:

```bash
# Check if dev server is running
node .claude/skills/visual-inspection/scripts/visual-inspection.js check-server

# Start the dev server
node .claude/skills/visual-inspection/scripts/visual-inspection.js start-server

# Stop the dev server (kills processes on port 4321)
node .claude/skills/visual-inspection/scripts/visual-inspection.js stop-server

# List all screenshots with metadata
node .claude/skills/visual-inspection/scripts/visual-inspection.js list

# Clean screenshots older than 7 days
node .claude/skills/visual-inspection/scripts/visual-inspection.js clean --days 7

# Validate a screenshot filename
node .claude/skills/visual-inspection/scripts/visual-inspection.js validate desktop-homepage-2026-01-09.png
```

## Output Storage

All screenshots are saved to `.playwright-mcp/` (gitignored). This keeps visual artifacts out of version control while preserving them for review.

**Note:** The Playwright MCP tool automatically saves screenshots to the `.playwright-mcp/` directory. When using `browser_take_screenshot`, only provide the filename (e.g., `desktop-homepage-2026-01-09.png`), not the full path. Including the directory prefix will cause double-nesting.

## Best Practices

1. **Always capture all three viewports** - Don't skip mobile or tablet
2. **Use descriptive filenames** - Include viewport, page, and date
3. **Review screenshots yourself** - Don't just rely on automation
4. **Compare with existing components** - Open other pages to check consistency
5. **Check both light and dark modes** - Toggle theme and capture both
6. **Test interactive states** - Use `browser_hover` to verify hover effects on key elements
7. **Verify focus indicators** - Tab through the page to ensure keyboard navigation works
8. **Document all issues** - Even small ones should be noted

## Integration with Development Workflow

This skill should be used:

- **After every UI change** - Before marking tasks complete
- **Before creating PRs** - As part of the pre-PR checklist
- **During code reviews** - When reviewing design changes
- **When adding new pages** - To ensure consistency with existing pages
- **After dependency updates** - To catch unexpected style changes

## Example Usage

**User:** "I've added a new blog post card component"

**You should:**

1. Start dev server (if not running)
2. Navigate to page with the new component
3. Capture screenshots at all three viewports
4. Read and analyze each screenshot
5. Provide detailed report on design quality, consistency, and issues
6. Recommend fixes for any problems found

**User:** "Before I merge this PR, can you check the designs?"

**You should:**

1. Identify which pages were modified
2. Capture screenshots of all affected pages
3. Compare with existing components for consistency
4. Check for layout shifts across viewports
5. Verify terminal aesthetic compliance
6. Provide comprehensive report with pass/fail for each criterion

## References

- **Design System**: `.claude/context/design-system.md` - Color palette, spacing, typography, component patterns
- **Project Instructions**: `CLAUDE.md` - Design philosophy and quality standards
- **MCP Config**: `.claude.json` - Playwright MCP server configuration
