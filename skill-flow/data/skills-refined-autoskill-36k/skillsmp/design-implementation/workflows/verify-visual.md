# Verify Visual Workflow

Visual verification using Claude multimodal vision and automated checks.

## Triggers

- "verify the implementation"
- "check the UI"
- "take a screenshot and verify"
- "does this match the design?"

## Verification Checklist

### 1. Automated Checks

```bash
# Capture current state
bun ${SKILL_DIR}/tools/playwright-runner.ts full \
  --url http://localhost:${PORT} \
  --output-dir ${SKILL_DIR}/history/${FEATURE_ID}
```

Parse `capture.json` for:

| Check | Command | Pass Criteria |
|-------|---------|---------------|
| Console errors | Captured by Playwright | `errors.filter(e => e.includes('Console'))` is empty |
| Network failures | Captured by Playwright | No 4xx/5xx responses |
| TypeScript | `bun tsc --noEmit` | Exit code 0 |
| React errors | Console capture | No "React" or "hydration" errors |

### 2. Visual Analysis (Claude Vision)

Use Claude's multimodal capabilities to analyze screenshots:

```
Read the screenshot at: ${SCREENSHOT_PATH}

Compare against the feature specification:
${FEATURE_SPEC}

Evaluate:
1. Layout matches spec? (header, sections, footer in correct positions)
2. Typography correct? (headings, body text, fonts)
3. Colors match? (backgrounds, text, accents)
4. Spacing appropriate? (padding, margins, gaps)
5. Components present? (buttons, inputs, images)
6. Responsive considerations visible?

Respond with:
- PASS: All criteria met
- ISSUES: List specific discrepancies
```

### 3. Figma Comparison (if available)

If Figma reference exists:

```
Compare these two images:
1. Figma design: ${FIGMA_SCREENSHOT}
2. Implementation: ${CURRENT_SCREENSHOT}

Identify differences in:
- Layout/positioning (>5px difference)
- Colors (visible mismatch)
- Typography (font, size, weight)
- Spacing (padding, margins)
- Missing elements
- Extra elements

Tolerance: ${LAYOUT_TOLERANCE}% (from config)
```

## Verification Result Format

```json
{
  "passed": true | false,
  "checks": {
    "console": { "passed": true, "errors": [] },
    "network": { "passed": true, "failures": [] },
    "typescript": { "passed": true, "errors": [] },
    "visual": { "passed": true, "issues": [] }
  },
  "screenshot": "history/feature-1/iteration-2.png",
  "timestamp": "2026-01-08T10:30:00Z"
}
```

## Error Categorization

When issues are found, categorize for `fix-errors` workflow:

| Category | Examples | Priority |
|----------|----------|----------|
| `console-error` | Undefined variable, import error | P0 |
| `typescript-error` | Type mismatch, missing prop | P0 |
| `network-error` | 404 asset, failed API call | P1 |
| `visual-layout` | Wrong positioning, missing element | P1 |
| `visual-style` | Wrong color, font size | P2 |
| `visual-minor` | Slight spacing difference | P3 |

## Quick Verification (No Figma)

For verbal descriptions without Figma:

```
Verify this implementation matches:
"${VERBAL_DESCRIPTION}"

Screenshot: ${SCREENSHOT_PATH}

Check for:
1. All mentioned elements present
2. Reasonable styling (not broken)
3. No obvious errors visible
4. Interactive elements look clickable
```

## Continuous Verification

During iteration loop:

```
AFTER each code change:
1. Wait ${HMR_DELAY}ms for HMR
2. Run quick verification (console + TS)
3. IF quick passes: Run full visual
4. IF quick fails: Skip visual, report errors
```

## Output to User

```markdown
## Verification Results

| Check | Status | Details |
|-------|--------|---------|
| Console | PASS | No errors |
| Network | PASS | All requests succeeded |
| TypeScript | PASS | No type errors |
| Visual | ISSUES | See below |

### Visual Issues Found
1. Header text should be larger (spec says 48px, appears ~36px)
2. CTA button missing hover state

### Screenshot
[View current state](history/feature-1/iteration-2.png)

### Recommendation
Run fix-errors workflow to address visual issues.
```
