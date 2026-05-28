---
name: browser-testing-debugging
description: Use this skill for comprehensive browser-based UI testing, visual analysis, and debugging, including monitoring console output and tracking network requests. Ideal for validating UI features, investigating console errors, and ensuring design fidelity.
---

# Browser Testing and Debugging

This Skill provides comprehensive browser-based UI testing, visual analysis, and debugging capabilities using Chrome DevTools MCP and optional external vision models via Claudish.

## When to Use This Skill

Invoke this Skill when:

- **Validating Own Work**: After implementing UI features, verify your work in a real browser.
- **Design Fidelity Checks**: Compare implementation screenshots against design references.
- **Visual Regression Testing**: Detect layout shifts, styling issues, or visual bugs.
- **Console Error Investigation**: Investigate user-reported console errors or warnings.
- **Form/Interaction Testing**: Verify that user interactions work correctly.
- **Pre-Commit Verification**: Ensure everything is functioning before committing or deploying code.
- **Bug Reproduction**: Investigate UI bugs described by users.

## Prerequisites

### Required: Chrome DevTools MCP

This skill requires Chrome DevTools MCP. Check availability and install if needed:

```bash
# Check if available
mcp__chrome-devtools__list_pages 2>/dev/null && echo "Available" || echo "Not available"

# Install via claudeup (recommended)
npm install -g claudeup@latest
claudeup mcp add chrome-devtools
```

### Optional: External Vision Models (via OpenRouter)

For advanced visual analysis, use external vision-language models via Claudish:

```bash
# Check OpenRouter API key
[[ -n "${OPENROUTER_API_KEY}" ]] && echo "OpenRouter configured" || echo "Not configured"

# Install claudish
npm install -g claudish
```

## Visual Analysis Models (Recommended)

For best visual analysis of UI screenshots, use these models via Claudish:

### Tier 1: Best Quality (Recommended for Design Validation)

| Model | Strengths | Cost | Best For |
|-------|-----------|------|----------|
| **qwen/qwen3-vl-32b-instruct** | Best OCR, spatial reasoning, GUI automation, 32+ languages | ~$0.06/1M input | Design fidelity, OCR, element detection |
| **google/gemini-2.5-flash** | Fast, excellent price/performance, 1M context | ~$0.05/1M input | Real-time validation, large pages |
| **openai/gpt-4o** | Most fluid multimodal, strong all-around | ~$0.15/1M input | Complex visual reasoning |

### Tier 2: Fast & Affordable

| Model | Strengths | Cost | Best For |
|-------|-----------|------|----------|
| **qwen/qwen3-vl-30b-a3b-instruct** | Good balance, MoE architecture | ~$0.04/1M input | Quick checks, multiple iterations |
| **google/gemini-2.5-flash-lite** | Ultrafast, very cheap | ~$0.01/1M input | High-volume testing |

### Tier 3: Free Options

| Model | Notes |
|-------|-------|
| **openrouter/polaris-alpha** | FREE, good for testing workflows |

### Model Selection Guide

```
Design Fidelity Validation → qwen/qwen3-vl-32b-instruct (best OCR & spatial)
Quick Smoke Tests → google/gemini-2.5-flash (fast & cheap)
Complex Layout Analysis → openai/gpt-4o (best reasoning)
High Volume Testing → google/gemini-2.5-flash-lite (ultrafast)
Budget Conscious → openrouter/polaris-alpha (free)
```

## Recipe 1: Agent Self-Validation (After Implementation)

**Use Case**: Developer/UI-Developer agent validates their own work after implementing a feature.

### Pattern: Implement → Screenshot → Analyze → Report

```markdown
## After Implementing UI Feature

1. **Save file changes** (Edit tool)

2. **Capture implementation screenshot**:
   ```bash
   mcp__chrome-devtools__navigate_page(url: "http://localhost:5173/your-route")
   # Wait for page load
   mcp__chrome-devtools__take_screenshot(filePath: "/tmp/implementation.png")
   ```

3. **Analyze with embedded Claude** (always available):
   - Describe what you see in the screenshot
   - Check for obvious layout issues
   - Verify expected elements are present

4. **Optional: Enhanced analysis with vision model**:
   ```bash
   npx claudish --model qwen/qwen3-vl-32b-instruct --stdin --quiet <<EOF
   Analyze this UI screenshot and identify any visual issues:

   IMAGE: /tmp/implementation.png

   Check for:
   - Layout alignment issues
   - Spacing inconsistencies
   - Typography problems (font sizes, weights)
   - Color contrast issues
   - Missing or broken elements
   - Responsive design problems

   Provide specific, actionable feedback.
   EOF
   ```

5. **Check console for errors**:
   ```bash
   mcp__chrome-devtools__list_console_messages(types: ["error", "warn"])
   ```

6. **Check network for failures**:
   ```bash
   mcp__chrome-devtools__list_network_requests()
   ```

7. **Report results to orchestrator**
```

### Quick Self-Check (5-Point Validation)

Agents should perform this quick check after any UI implementation:

```markdown
## Quick Self-Validation Checklist

□ 1. Screenshot shows expected UI elements
□ 2. No console errors (check: mcp__chrome-devtools__list_console_messages)
□ 3. No network failures (check: mcp__chrome-devtools__list_network_requests)
□ 4. Interactive elements respond correctly
□ 5. Visual styling matches expectations
```

## Recipe 2: Design Fidelity Validation

**Use Case**: Compare implementation against Figma design or design reference.

### Pattern: Design Reference → Implementation → Visual Diff

```markdown
## Design Fidelity Check

### Step 1: Capture Design Reference

**From Figma**:
```bash
# Use Figma MCP to export design
mcp__figma__get_file_image(fileKey: "abc123", nodeId: "136-5051")
# Save to: /tmp/design-reference.png
```

**From URL**:
```bash
mcp__chrome-devtools__new_page(url: "https://figma.com/proto/...")
mcp__chrome-devtools__take_screenshot(filePath: "/tmp/design-reference.png")
```

**From Local File**:
```bash
# Already have reference at: /path/to/design.png
```

### Step 2: Capture Implementation

```bash
mcp__chrome-devtools__navigate_page(url: "http://localhost:5173/component")
mcp__chrome-devtools__resize_page(width: 1440, height: 900)  # Match design viewport
mcp__chrome-devtools__take_screenshot(filePath: "/tmp/implementation.png")
```

### Step 3: Visual Analysis with Vision Model

```bash
npx claudish --model qwen/qwen3-vl-32b-instruct --stdin --quiet <<EOF
Compare these two UI screenshots and identify design fidelity issues:

DESIGN REFERENCE: /tmp/design-reference.png
IMPLEMENTATION: /tmp/implementation.png

Analyze and report differences in:

## Colors & Theming
- Background colors (exact hex values)
- Text colors (headings, body, muted)
- Border and divider colors
- Button/interactive element colors

## Typography
- Font families
- Font sizes (px values)
- Font weights (regular, medium, bold)
- Line heights
- Letter spacing

## Spacing & Layout
- Padding (top, right, bottom, left)
- Margins between elements
- Gap spacing in flex/grid
- Container max-widths
- Alignment (center, left, right)

## Visual Elements
- Border radius values
- Box shadows (blur, spread, color)
- Icon sizes and colors
- Image aspect ratios

## Component Structure
- Missing elements
- Extra elements
- Wrong element order

For EACH difference found, provide:
1. Category (colors/typography/spacing/visual/structure)
2. Severity (CRITICAL/MEDIUM/LOW)
3. Expected value (from design)
4. Actual value (from implementation)
5. Specific Tailwind CSS fix

Output as structured markdown.
EOF
```

### Step 4: Generate Fix Recommendations

Parse vision model output and create actionable fixes for ui-developer agent.

## Recipe 3: Interactive Element Testing

**Use Case**: Verify buttons, forms, and interactive components work correctly.

### Pattern: Snapshot → Interact → Verify → Report

```markdown
## Interactive Testing Flow

### Step 1: Get Page Structure
```bash
mcp__chrome-devtools__take_snapshot()
# Returns all elements with UIDs
```

### Step 2: Test Each Interactive Element

**Button Test**:
```bash
# Before
mcp__chrome-devtools__take_screenshot(filePath: "/tmp/before-click.png")

# Click
mcp__chrome-devtools__click(uid: "button-submit")

# After (wait for response)
mcp__chrome-devtools__wait_for(text: "Success", timeout: 5000)
mcp__chrome-devtools__take_screenshot(filePath: "/tmp/after-click.png")

# Check results
mcp__chrome-devtools__list_console_messages(types: ["error"])
mcp__chrome-devtools__list_network_requests(resourceTypes: ["fetch", "xhr"])
```

**Form Test**:
```bash
# Fill form
mcp__chrome-devtools__fill_form(elements: [
  { uid: "input-email", value: "test@example.com" },
  { uid: "input-password", value: "SecurePass123!" }
])

# Submit
mcp__chrome-devtools__click(uid: "button-submit")

# Verify
mcp__chrome-devtools__wait_for(text: "Welcome", timeout: 5000)
```

**Hover State Test**:
```bash
mcp__chrome-devtools__take_screenshot(filePath: "/tmp/before-hover.png")
mcp__chrome-devtools__hover(uid: "button-primary")
mcp__chrome-devtools__take_screenshot(filePath: "/tmp/after-hover.png")
# Compare screenshots for hover state changes
```

### Step 3: Analyze Interaction Results

Use vision model to compare before/after screenshots:
```bash
npx claudish --model google/gemini-2.5-flash --stdin --quiet <<EOF
Compare these before/after screenshots and verify the interaction worked:

BEFORE: /tmp/before-click.png
AFTER: /tmp/after-click.png

Expected behavior: [describe what should happen]

Verify:
1. Did the expected UI change occur?
2. Are there any error states visible?
3. Did loading states appear/disappear correctly?
4. Is the final state correct?

Report: PASS/FAIL with specific observations.
EOF
```

## Recipe 4: Responsive Design Validation

**Use Case**: Verify UI works across different screen sizes.

### Pattern: Resize → Screenshot → Analyze

```markdown
## Responsive Testing

### Breakpoints to Test

| Breakpoint | Width | Description |
|------------|-------|-------------|
| Mobile | 375px | iPhone SE |
| Mobile L | 428px | iPhone 14 Pro Max |
| Tablet | 768px | iPad |
| Desktop | 1280px | Laptop |
| Desktop L | 1920px | Full HD |

### Automated Responsive Check

```bash
#!/bin/bash
# Test all breakpoints

BREAKPOINTS=(375 428 768 1280 1920)
URL="http://localhost:5173/your-route"

for width in "${BREAKPOINTS[@]}"; do
  echo "Testing ${width}px..."

  # Resize and screenshot
  mcp__chrome-devtools__resize_page(width: $width, height: 900)
  mcp__chrome-devtools__take_screenshot(filePath: "/tmp/responsive-${width}.png")
done
```

### Visual Analysis for Responsive Issues

```bash
npx claudish --model qwen/qwen3-vl-32b-instruct --stdin --quiet <<EOF
Analyze these responsive screenshots for layout issues:

MOBILE (375px): /tmp/responsive-375.png
TABLET (768px): /tmp/responsive-768.png
DESKTOP (1280px): /tmp/responsive-1280.png

Check for:
1. Text overflow or truncation
2. Elements overlapping
3. Improper stacking on mobile
4. Touch targets too small (<44px)
5. Hidden content that shouldn't be hidden
6. Horizontal scroll issues
7. Image scaling problems

Report issues by breakpoint with specific CSS fixes.
EOF
```

## Recipe 5: Accessibility Validation

**Use Case**: Verify accessibility standards (WCAG 2.1 AA).

### Pattern: Snapshot → Analyze → Check Contrast

```markdown
## Accessibility Check

### Automated A11y Testing

```bash
# Get full accessibility tree
mcp__chrome-devtools__take_snapshot(verbose: true)

# Check for common issues:
# - Missing alt text
# - Missing ARIA labels
# - Incorrect heading hierarchy
# - Missing form labels
```

### Visual Contrast Analysis

```bash
npx claudish --model qwen/qwen3-vl-32b-instruct --stdin --quiet <<EOF
Analyze this screenshot for accessibility issues:

IMAGE: /tmp/implementation.png

Check WCAG 2.1 AA compliance:

1. **Color Contrast**
   - Text contrast ratio (need 4.5:1 for normal, 3:1 for large)
   - Interactive element contrast
   - Focus indicator visibility

2. **Visual Cues**
   - Do links have underlines or other visual differentiation?
   - Are error states clearly visible?
   - Are required fields indicated?

3. **Text Readability**
   - Font size (minimum 16px for body)
   - Line height (minimum 1.5)
   - Line length (max 80 characters)

4. **Touch Targets**
   - Minimum 44x44px for interactive elements
   - Adequate spacing between targets

Report violations with severity and specific fixes.
EOF
```

## Recipe 6: Console & Network Debugging

**Use Case**: Investigate runtime errors and API issues.

### Pattern: Monitor → Capture → Analyze

```markdown
## Debug Session

### Real-Time Console Monitoring

```bash
# Get all console messages
mcp__chrome-devtools__list_console_messages(includePreservedMessages: true)

# Filter by type
mcp__chrome-devtools__list_console_messages(types: ["error", "warn"])

# Get specific error details
mcp__chrome-devtools__get_console_message(msgid: 123)
```

### Network Request Analysis

```bash
# Get all requests
mcp__chrome-devtools__list_network_requests()

# Filter API calls only
mcp__chrome-devtools__list_network_requests(resourceTypes: ["fetch", "xhr"])

# Get failed request details
mcp__chrome-devtools__get_network_request(reqid: 456)
```

### Error Pattern Analysis

Common error patterns to look for:

| Error Type | Pattern | Common Cause |
|------------|---------|--------------|
| React Error | "Cannot read property" | Missing null check |
| React Error | "Invalid hook call" | Hook rules violation |
| Network Error | "CORS" | Missing CORS headers |
| Network Error | "401" | Auth token expired |
| Network Error | "404" | Wrong API endpoint |
| Network Error | "500" | Server error |

## Integration with Agents

### For Developer Agent

After implementing any UI feature, the developer agent should:

```markdown
## Developer Self-Validation Protocol

1. Save code changes
2. Navigate to the page: `mcp__chrome-devtools__navigate_page`
3. Take screenshot: `mcp__chrome-devtools__take_screenshot`
4. Check console: `mcp__chrome-devtools__list_console_messages(types: ["error"])`
5. Check network: `mcp__