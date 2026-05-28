# Visual Validation (UI-Only Pass/Fail)

After making changes, treat screenshots as the source of truth for “did it work?”.

## Rule

Never declare a fix successful based on console logs alone (e.g., “completed successfully”).
Pass/fail must be determined from the **actual web UI state**, captured in screenshots (or observed live during reproduction).

## Verification Checkpoints

Define a small list of checkpoints for the flow (3–10):
- checkpoint name (step + intent)
- what page/modal/popup it should be on (URL pattern or title token)
- what should be visible (heading, confirmation banner, table row, field values)
- what screenshot to capture (full page vs. specific element)

Examples of good checkpoints:
- “After login: user menu visible”
- “After search: results table contains target row”
- “After form submit: confirmation number visible”
- “After download: download row shows completed status”

## Screenshot Capture Guidance

- Capture screenshots on **success** at the key checkpoints, not only on failure.
- Prefer element screenshots for dense UIs (confirmation banner, receipt number block) plus one full-page screenshot at the end.
- If a popup/new tab is part of the flow, capture a screenshot for the popup too.

Recommended naming:
- `{prefix}_{checkpoint}_{YYYYMMDD_HHMMSS}.png`

## Optional: Baseline Comparison

If the app UI is stable enough, you can keep a “golden” screenshot per checkpoint and compare diffs using Playwright’s screenshot assertions.
Only do this when fonts/layout are stable; otherwise, keep it as a human-reviewed artifact.
