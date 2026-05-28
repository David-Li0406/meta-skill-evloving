# Diagnostics & Failure Artifacts

The fastest way to reduce future edits is to make every failure produce enough evidence to fix without guesswork.

## Also Capture on Success (Checkpoints)

Capture a small set of “result screenshots” at verification checkpoints and use them to decide pass/fail.
See `references/visual-validation.md`.

## Always Capture on Failure

On exception, save:
- Screenshot (full page)
- HTML dump (`page.content()`)
- Accessibility snapshot (JSON)
- Trace zip (`context.tracing.stop(path="trace.zip")`)

Recommended naming:
- `{prefix}_{YYYYMMDD_HHMMSS}.png`
- `{prefix}_{YYYYMMDD_HHMMSS}.html`
- `{prefix}_{YYYYMMDD_HHMMSS}_a11y.json`
- `{prefix}_{YYYYMMDD_HHMMSS}.zip`

## Trace

Use Playwright tracing:
- Start before the flow: `context.tracing.start(screenshots=True, snapshots=True, sources=True)`
- Stop on success or failure, always producing a file.

This is the single most useful artifact for “works on my machine / flaky timing” issues.

## Minimal Python Pattern (Sync API)

Implement the pattern in the automation codebase (not inside the skill):
- create an output directory
- wrap the run in `try/except/finally`
- on exception, write artifacts then re-raise

## What to Look For

- “Element is not attached” → locator points to a re-rendered node; re-locate after state change
- “Timeout” → contract mismatch; waiting for the wrong thing; add a step exit condition
- Popup didn’t open → click did nothing; check overlay, disabled state, or wrong “duplicate text” target
