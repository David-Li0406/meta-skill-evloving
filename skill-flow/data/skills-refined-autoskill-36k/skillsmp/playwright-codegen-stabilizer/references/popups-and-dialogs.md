# Popups, Dialogs, and Overlays

## Dialogs (`alert/confirm/prompt`)

Always attach a handler early:
- accept dialogs that block progress
- dismiss informational dialogs unless they must be accepted

Rule: Never let an unexpected dialog hang the run.

## New Windows / Tabs

Use `expect_popup()` (or equivalent) around the triggering action.
Immediately after getting the popup:
- wait for `domcontentloaded`
- assert URL/origin is expected
- close nuisance popups by URL/title pattern

## Overlays / Click Interception

Symptoms:
- click times out
- an element “intercepts pointer events”

Approaches:
- wait for overlay to disappear (if real loading)
- scroll element into view and retry
- if the site uses persistent security overlays, fall back to a controlled `evaluate()` click on the intended element

Use JS fallbacks sparingly and only with diagnostics enabled.
