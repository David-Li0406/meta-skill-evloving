# UI Contracts

These contracts must be enforced generically (not hardcoded to specific buttons or modals).

## Theme & contrast

- Test dark, light, and system (simulate light + dark).
- Sample visible text nodes and compute contrast against their effective background.
- Fail if any primary text drops below threshold (e.g., 4.5:1 for normal text).

## Animation & motion

- Any element tagged `qa:spinner:*` must actually animate.
- Transitions/menus/toasts should show motion frames (not instant jump).
- Record a short video or multi-frame capture for modal enter/exit, toast, autosave.

## Loading state machine

- Any `qa:action:async` should follow idle -> loading -> success/error -> idle.
- Loading state must disable the button and show spinner/text.
- Success/error states must be transient (return to idle).

## Layout stability

- Transient UI (autosave status, toasts, inline badges) must not shift layout.
- Track bounding boxes before/after; limit delta within threshold.

## Overlap and clipping

- Action buttons and modal header/footer must not overlap.
- Detect bounding box intersection for button clusters and modal controls.
- Detect shadow clipping for hover effects where possible (capture hover state).

## Modal usability

- Modal header/close always visible at small height.
- Modal body scrolls internally; outer page should not scroll.
- Only one close button exists per modal.

## Error visibility

- Initialization/render errors must show an overlay and log details.
- Blank page (no `qa:app-shell`) is a hard failure with screenshot.
