# Agent-Browser State Management

Best practices for agent-browser usage in www-audit workflow. Based on aave.com dogfooding (2026-01-22).

## Clean-State Checklist

**CRITICAL**: Run this checklist before EVERY screenshot (scroll, interaction, mobile, desktop).

```
Is page in clean state for screenshot?
├── Cookie/consent banner visible?
│   └── NO: dismiss banner, wait 500ms, re-check
├── Any dropdown/modal/panel open?
│   └── NO: close all (Esc/click outside), wait 500ms, re-check
├── Lingering hover/focus/toast/notification?
│   └── NO: click body, wait 200ms, re-check
├── Multiple interaction states active?
│   └── NO: close all except target interaction, wait 500ms
├── Inspect tools/dev console open?
│   └── NO: close dev tools
└── All clean?
    └── YES: capture screenshot, add to validation table
```

## Pre-Flight Checklist (Before FIRST Screenshot)

1. Open page with agent-browser
2. Wait for full load: `agent-browser wait --load networkidle`
3. Dismiss cookie banner (if present):
   ```bash
   agent-browser click '[data-dismiss-cookie-banner]'
   agent-browser wait 200
   ```
4. Close any auto-open modals/tooltips
5. Run clean-state checklist
6. If not clean: fix issues, re-run checklist
7. ONLY THEN: capture first screenshot

## Interaction Capture Loop (Mandatory Pattern)

**For EACH interaction state to capture:**

```bash
# Step 1: Pre-flight clean state check
agent-browser snapshot -i -c  # Verify no dropdowns/modals open
# If not clean: close overlays, wait 500ms, re-check

# Step 2: Trigger interaction
agent-browser click '[data-menu-trigger]'  # or hover, etc.
agent-browser wait 300  # Wait for animation

# Step 3: Capture interaction screenshot
agent-browser screenshot z-menu-open.png

# Step 4: IMMEDIATE cleanup
agent-browser press Escape  # Close dropdown
# OR: agent-browser eval "document.querySelector('[data-menu-trigger]').click()"
# OR: agent-browser click body  # Click outside to close
agent-browser wait 500  # Wait for close animation

# Step 5: Verify clean state
agent-browser snapshot -i -c
# Check output: no "menu" or "dropdown" or "modal" elements visible

# Step 6: Add validation table entry
# | z-menu-open.png | PASS | Products menu open, background clean |

# Step 7: ONLY if PASS, proceed to next interaction
# If FAIL: go back to Step 1
```

## Anti-Pattern Examples from Aave Audit

### BAD: Dropdown Pollution
```bash
# DON'T DO THIS
agent-browser click '[data-menu-trigger]'
agent-browser screenshot z-menu-open.png
agent-browser scroll down 900  # ❌ Menu still open!
agent-browser screenshot z-scroll-1.png  # ❌ Polluted with open menu
```

**Problem**: z-scroll-1.png shows Products menu still open from earlier interaction (aave audit).

### GOOD: Explicit Cleanup
```bash
# DO THIS
agent-browser click '[data-menu-trigger]'
agent-browser screenshot z-menu-open.png
agent-browser press Escape  # Close menu
agent-browser wait 500  # Wait for close animation
agent-browser snapshot -i -c  # Verify clean
agent-browser scroll down 900  # ✅ Clean page
agent-browser screenshot z-scroll-1.png  # ✅ No pollution
```

### BAD: Multiple Simultaneous States
```bash
# DON'T DO THIS
agent-browser click '[data-products-menu]'  # Opens Products dropdown
# User also triggers detail panel somehow
agent-browser screenshot z-button-products-hover.png  # ❌ Two panels open!
```

**Problem**: z-button-products-hover.png shows BOTH Products dropdown AND "Aave for Web" detail panel (aave audit). Unclear what the screenshot demonstrates.

### GOOD: One State at a Time
```bash
# DO THIS
agent-browser click '[data-products-menu]'  # Open Products
agent-browser wait 300
agent-browser screenshot z-menu-products-open.png  # ✅ Only menu open

# Close before next interaction
agent-browser press Escape
agent-browser wait 500
agent-browser snapshot -i -c  # Verify closed

# Now capture detail panel separately
agent-browser click '[data-detail-trigger]'
agent-browser wait 300
agent-browser screenshot z-panel-detail-open.png  # ✅ Only panel open
```

### BAD: Cookie Banner Persistence
```bash
# DON'T DO THIS
agent-browser open https://example.com
agent-browser screenshot z-home.png  # ❌ Cookie banner visible
agent-browser scroll down 900
agent-browser screenshot z-scroll-1.png  # ❌ Banner still there
```

**Problem**: Cookie banner visible in z-scroll-1.png and z-scroll-2.png (aave audit).

### GOOD: Pre-Flight Dismiss
```bash
# DO THIS
agent-browser open https://example.com
agent-browser wait --load networkidle

# Dismiss banner BEFORE first screenshot
agent-browser click '[data-cookie-accept]'  # or [data-cookie-dismiss]
agent-browser wait 200

# Verify clean
agent-browser snapshot -i -c  # Check no banner in output

# Now capture clean
agent-browser screenshot z-home.png  # ✅ No banner
agent-browser scroll down 900
agent-browser screenshot z-scroll-1.png  # ✅ Still no banner
```

## Post-Interaction Cleanup Protocol

After capturing EVERY interaction screenshot:

1. **Close the interaction**:
   - Dropdowns/menus: `agent-browser press Escape` or click outside
   - Modals: Click close button or `Escape`
   - Hover states: `agent-browser click body` (removes hover)
   - Tooltips: Click away or wait for auto-dismiss

2. **Wait for animation complete**:
   ```bash
   agent-browser wait 500  # Standard for most animations
   # Or longer if site uses slow transitions
   ```

3. **Verify clean state**:
   ```bash
   agent-browser snapshot -i -c
   # Read output: should show NO dropdown/modal/tooltip elements
   ```

4. **Add validation table entry**:
   ```
   | z-menu-open.png | PASS | Menu open, no other overlays, clean background |
   ```

5. **ONLY if clean, proceed to next action** (scroll, next interaction, viewport change)

## Scroll Capture Protocol

Before scrolling to capture scroll screenshots:

1. **Verify clean state**:
   ```bash
   agent-browser snapshot -i -c
   # Check: no dropdowns, modals, tooltips, cookie banners
   ```

2. **If not clean**:
   - Close all overlays: `agent-browser press Escape`, `agent-browser click body`
   - Dismiss banners
   - Wait 500ms
   - Re-verify via snapshot

3. **Scroll and capture**:
   ```bash
   agent-browser scroll down 900
   agent-browser wait 300  # Let scroll animations settle
   agent-browser screenshot z-scroll-1.png
   ```

4. **Add validation table entry**:
   ```
   | z-scroll-1.png | PASS | Stats section, all overlays closed, clean |
   ```

## Validation Table Artifact (Required)

**Every specialist MUST output a validation table for ALL screenshots.**

Format:
```markdown
| Screenshot | Pass/Fail | Validation Note |
|------------|-----------|-----------------|
| z-home.png | PASS | Clean hero, no overlays, text readable, size 245KB |
| z-menu-open.png | PASS | Products menu open, no other dropdowns, background clean, size 198KB |
| z-scroll-1.png | PASS | Stats section, all dropdowns closed, banner dismissed, size 223KB |
| z-button-hover.png | FAIL | Hover didn't trigger, shows default state - re-capturing |
| z-button-hover.png | PASS | Hover visible (color change + scale), no overlays, size 187KB |
```

**Validation criteria per screenshot:**
- ✅ Content matches filename (z-menu-open shows open menu, not closed)
- ✅ No unintended overlays (cookie banners, other dropdowns, tooltips)
- ✅ One interaction state max (if interaction screenshot)
- ✅ Correct viewport (1440×900 desktop, 375×812 mobile)
- ✅ Text readable, no capture artifacts, no blur
- ✅ File size >10KB (blank screenshots are <5KB)
- ✅ Interaction triggered correctly (button shows hover, menu shows open)

**If screenshot fails validation:**
1. Delete screenshot file: `rm path/to/z-screenshot.png`
2. Fix issue:
   - Close overlays: `agent-browser press Escape`, wait 500ms
   - Re-trigger interaction if needed
   - Adjust viewport if wrong dimensions
   - Wait longer for page load if content missing
3. Re-capture screenshot: `agent-browser screenshot z-screenshot.png`
4. Re-validate (repeat until PASS)
5. Update table entry to PASS

**Orchestrator enforcement:**
- Specialist output without validation table = REJECTED (specialist must re-run)
- Any screenshot with FAIL status = requires resolution before aggregation
- Orchestrator validates EVERY screenshot via Read tool (visual check)

## Timing Values

| Action | Wait Time | Reason |
|--------|-----------|--------|
| Close dropdown/modal | 500ms | Standard overlay close animation |
| Dismiss banner | 200ms | Banner fade-out |
| Trigger hover | 100ms | CSS transition delay |
| Open modal | 300ms | Modal entrance animation |
| Scroll | 300ms | Smooth scroll animation + layout shift |
| Page load | Use `--load networkidle` | Wait for all resources |
| Viewport change | 200ms | Let responsive layout settle |

## Common Mistakes

| Mistake | Evidence | Fix |
|---------|----------|-----|
| No pre-flight check | aave had cookie banner from first screenshot | Dismiss banner before ANY screenshot |
| Dropdown left open during scroll | aave z-scroll-1.png has Products menu | Close + wait + verify before scrolling |
| Multiple states in one screenshot | aave z-button-products-hover.png has 2 panels | One state per screenshot, close previous |
| Wrong naming prefix | aave used a-, b-, c- prefixes | Always use z- prefix |
| No cleanup confirmation | Assume close worked without checking | Use snapshot -i -c to verify clean |
| Screenshot-filename mismatch | z-menu-open shows closed menu | Re-trigger, re-capture, validate content |

## Enforcement Mechanisms

### 1. Required Validation Table
Specialists MUST provide table, or output is rejected by orchestrator.

### 2. Hard Fail-Fast Rules
If orchestrator detects these via Read tool, immediate action:
- Cookie banner in screenshot → DELETE, dismiss banner, RE-CAPTURE
- Dropdown in scroll screenshot → DELETE, close dropdown, RE-CAPTURE
- >1 interaction state → DELETE, isolate one state, RE-CAPTURE
- Blank/loading screenshot → DELETE, wait for load, RE-CAPTURE
- Wrong viewport → DELETE, set correct viewport, RE-CAPTURE

### 3. Quality Gate Integration
New FAIL conditions added to quality gate decision tree (SKILL.md line ~936):
- ANY screenshot with FAIL in validation table
- Cookie banner visible in ANY screenshot
- Dropdown/modal open in scroll screenshot
- Multiple interaction states in single screenshot
- Inconsistent naming (non-z- prefix)
- Screenshot filename doesn't match content

## Example: Full Interaction Sequence

Capturing hover state on primary button:

```bash
# Pre-flight: ensure clean
agent-browser open https://example.com
agent-browser wait --load networkidle
agent-browser click '[data-cookie-accept]'  # Dismiss banner
agent-browser wait 200
agent-browser snapshot -i -c  # Verify clean

# Capture default state first
agent-browser screenshot z-button-default.png
# Validation: | z-button-default.png | PASS | Default button state, no hover, clean background |

# Trigger hover
agent-browser hover 'button.primary'  # or eval to add hover class
agent-browser wait 100  # CSS transition
agent-browser screenshot z-button-hover.png

# Cleanup: remove hover
agent-browser click body  # Click away to remove hover
agent-browser wait 200
agent-browser snapshot -i -c  # Verify hover removed

# Validation: | z-button-hover.png | PASS | Button hover visible (scale + color), no other interactions |

# Now safe to scroll or capture next interaction
agent-browser scroll down 900
agent-browser wait 300
agent-browser screenshot z-scroll-1.png
# Validation: | z-scroll-1.png | PASS | First section, button back to default, no overlays |
```

## Summary

**Golden Rule**: Every screenshot capture is bracketed by clean-state checks.

```
Pre-flight → Clean state → Capture → Post-cleanup → Verify clean → Proceed
```

**Validation is not optional**. It's a required artifact that proves specialists followed the protocol.
