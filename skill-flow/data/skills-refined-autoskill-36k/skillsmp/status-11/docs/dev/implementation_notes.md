# Implementation Notes (Developer)

This document collects implementation-oriented notes, runbooks, and validation checklists for features as they evolve.

## Smoke (M0 Scaffold) — run/test/validate contract (ge-hch.1.2)

This section defines what “Smoke” means for M0 validation. It is intended to keep implementation, tests, and docs aligned.

### Definition

A build is considered **Smoke-passing** if:

1. **Browser/dev run:** the web demo (e.g., web/demo/index.html or running the dev server) loads and:
   - displays a visible UI state immediately
   - accepts at least one input method (mouse/touch/keyboard) that advances the UI state
   - does not crash/hard hang
   - does not emit unbounded exception spam

2. **Desktop browser:** The demo can be loaded in a desktop browser and run with the same baseline interactions.

3. **Mobile browser:** The demo loads in a mobile browser (or emulator) and supports at least touch input.

### Manual validation checklist

For PR review (or local development), record results in `bd` comments:
- Demo run instructions present (e.g., `cd web && npm ci && npm start` or open `web/demo/index.html`)
- Demo entry point exists: `web/demo/index.html` or equivalent
- Dev run: demo loads and first page displays; can advance; no fatal errors
- Desktop browser: loads and runs; can advance; no fatal errors
- Mobile browser: loads and runs; can advance; no fatal errors

### Automated test expectations (ties to `ge-hch.1.2.3`)

At least one automated browser test should exist that:
- loads the demo (dev server or built static files)
- asserts that expected UI root elements exist (or other minimal stable indicators)
- simulates an input event (click/tap/keyboard) and asserts the visible state changes

### Observability / logging

Telemetry is **deferred** to `ge-hch.1.3`.

For Smoke validation until then:
- Browser: use the browser DevTools console for errors/exceptions.
- Dev server/static artifact: use console logs for errors/exceptions.
- Desktop build (if produced): use the browser/player logs.

Once telemetry is implemented, update this section with:
- where telemetry files/streams are emitted in the runtime
- the expected schema/format
- what constitutes a telemetry error vs. acceptable early placeholders

### Troubleshooting

Symptom → likely cause → fix:

- **Demo missing (`web/demo/index.html` not found)** → demo not created yet or not available from artifact store → create the demo at that path or fetch it from the agreed artifact mechanism.
- **Dev server fails** → missing dependencies or incorrect Node version → run `npm ci` and confirm Node/npm versions; check build logs.
- **Demo shows blank/empty screen** → assets not served or UI not wired → confirm demo entry point and inspect browser console for missing files or runtime errors.
- **Mobile demo fails** → unsupported setting/package or incompatible asset usage → test in mobile emulation and inspect browser console.
