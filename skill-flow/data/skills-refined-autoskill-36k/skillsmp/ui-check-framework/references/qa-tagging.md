# QA Tagging Rules

Use `data-qa` (or `data-testid`) tokens that start with `qa:`. Tokens are space-separated.

## Required tokens (minimum)

- `qa:app-shell`            Root application container.
- `qa:header:main`          Main page header.
- `qa:toolbar:header`       Header toolbar container.
- `qa:card:*`               Each top-level card/section.
- `qa:modal:*`              Each modal container.
- `qa:modal-header:*`       Modal header container.
- `qa:modal-body:*`         Modal scroll container.
- `qa:modal-footer:*`       Modal footer container.
- `qa:modal-close:*`        Single close button per modal.
- `qa:modal-trigger:*`      Button that opens a modal.
- `qa:action:async`         Any async action button (pull/sync/etc).
- `qa:action:*`             Action buttons (async or sync).
- `qa:spinner:*`            Spinner element shown during loading.
- `qa:toast:*`              Toast messages.
- `qa:overlay:*`            Full-screen overlays (loading/error).
- `qa:status:*`             Inline status text (autosave, badges, inline state).

## Naming examples

- `data-qa="qa:card:activity-log"`
- `data-qa="qa:modal:settings"`
- `data-qa="qa:modal-body:settings"`
- `data-qa="qa:modal-close:settings"`
- `data-qa="qa:action:pull qa:action:async"`
- `data-qa="qa:spinner:pull"`
- `data-qa="qa:toast:success"`
- `data-qa="qa:overlay:init"`
- `data-qa="qa:status:autosave"`

## Behavior conventions

- Async actions should toggle `data-qa-state="idle|loading|success|error"`.
- Modals must keep header/close visible at small window height (720px) and
  allow internal scroll in the body.
- Use unique identifiers for each card/modal (suffix after the second colon).
