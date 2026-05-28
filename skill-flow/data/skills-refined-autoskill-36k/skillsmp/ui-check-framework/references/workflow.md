# UI Check Workflow

Use this workflow to implement or extend the UI self-check framework without hardcoding
specific features.

## 1) Discovery scaffolding

- Locate `ui-tests/` in the project root. If missing, create it with Playwright setup,
  a `scripts/` runner folder, and `docs/` for tagging/testing guidance.
- Ensure the root `package.json` exposes:
  - `ui:test` (Playwright regression)
  - `ui:update-baseline`
  - `ui:report`
  - `ui:check` (interactive scenario suite)
  - `ui:watch` (rerun ui-check on file change)

## 2) QA tagging rules

- Apply `data-qa` tokens (prefix `qa:`) to:
  - app shell, header, toolbars
  - cards/sections
  - modals (header/body/footer/close/trigger)
  - async action buttons, spinners, toasts
  - status text and overlays
- Read `ui-tests/docs/QA_TAGGING.md` if present and keep tags consistent.

## 3) Interactive scenario coverage

The UI check must do more than static snapshots. It should:

- Toggle theme (dark/light/system)
- Open/close modals and menus with transitions
- Hover/press buttons to capture interaction states
- Trigger async loading -> success/error -> idle
- Trigger autosave status
- Append activity log entries
- Scroll within modal body (small viewport)
- Capture state-based screenshots + motion frames/video

## 4) Contract assertions

- Contrast/readability: dark/light/system must pass minimum ratio checks.
- Animation: spinners must animate; transitions must run.
- Layout stability: transient status/toasts should not shift layout.
- Modal scroll: outer page must not scroll when modal open; close always visible.
- Overlap: action buttons and modal header/footer must not overlap.
- Error visibility: failed init must show overlay; no silent blank page.

## 5) Artifacts

- Write all artifacts to `artifacts/ui-check/` (snapshots, frames, video, report).
- Group report by scenario (theme/modal/loading/autosave/etc).

## 6) Verification checklist

- Run `ui:check` locally and open the report.
- Verify that modal states capture full content (scroll if needed).
- Confirm dark/light/system all render and are tested.
- Verify at least 3 window sizes: small, medium, large.
