# InkJS Demo and Smoke Trigger

This document explains how to run the InkJS-based smoke demo and where to find its assets.

## Layout
- `web/demo/index.html` — lightweight static page that runs the InkJS story and UI.
- `web/demo/js/telemetry.js` — telemetry facade (ConsoleTelemetry by default) with enable/disable toggle.
- `web/demo/js/inkrunner.js` — runner that loads the story, renders choices, handles telemetry, and save/load.
- `web/demo/js/smoke.js` — dependency-free smoke visual (canvas-based).
- `web/stories/demo.ink` — the stable demo Ink story with the `#smoke` tag. CI and docs reference this as the canonical fallback story.
- `web/demo/vendor/ink.js` — vendored InkJS compiler build (ink-full). Replace this file to update version. **Serve from repo root or web/ so this file and /stories/demo.ink are exposed.**

## Running the demo
1. Serve over HTTP (only) so the runner can fetch `web/stories/demo.ink` and compile at runtime. **Serve from repo root or `web/` (not `web/demo`) so `/stories/demo.ink` is reachable**:
   ```bash
   npx http-server web    # serves /demo and /stories (stable demo.ink included)
   # or any static server rooted at repo root or web/
   ```
2. InkJS is vendored locally at `web/demo/vendor/ink.js` (ink-full with Compiler). If you prefer CDN, swap the script tag in `web/demo/index.html` to `https://unpkg.com/inkjs/dist/ink-full.js` (or desired version).
3. On page load you should see the story text and available choices. Console logs will show `story_start` once the story begins.

## Interacting
- Click or tap choices to advance. A `choice_selected` telemetry log is emitted for every choice.
- When the story line with tag `#smoke` is presented, the runner emits `smoke_triggered` and starts the smoke effect using the current control values.
- Control panel: adjust smoke duration (seconds) and intensity (1–10). Save and Load buttons persist and restore story plus smoke state.
- Save/load uses `localStorage` key `ge-hch.smoke.save`. Saved data includes Ink story state JSON, smoke state, and control settings.

## Telemetry configuration
- Telemetry facade: `window.Telemetry` (ConsoleTelemetry by default) with methods `emit(eventName, payload?)`, `enable()`, `disable()`, and property `enabled` (boolean).
- Events emitted by the runner: `story_start` (on story init), `choice_selected` (on every choice), `smoke_triggered` (when the #smoke tag is seen), `story_complete` (when story ends).
- Note: telemetry emission is performed by the runtime/player (web/demo/js/inkrunner.js) — it does not require content-level choice tags like `#choice_selected`. The runtime emits `choice_selected` when a player choice is selected.
- Toggle telemetry off: in devtools console run `window.Telemetry.disable()` or set `window.Telemetry.enabled = false`. Re-enable with `window.Telemetry.enable()`.

## Testing
- Automated: `npm run test:unit` (Jest) and `npm run test:demo` (Playwright E2E against the demo). `npm test` runs both.
- Story validation (CI/local): `node scripts/validate-story.js web/stories/demo.ink` parses and smoke-tests the stable story. CI also runs `.github/workflows/validate-story.yml` on story or validator changes.
- Manual: see checklist below.

## Manual validation checklist
- Open `web/demo/index.html` in browser with devtools console.
- Observe `story_start` log on load and initial text displayed.
- When the `#smoke` tagged line appears, observe `smoke_triggered` and visible smoke that fades out over ~3s.
- Click choices; ensure `choice_selected` logs and text updates. When no choices remain, `story_complete` should log.
- Click Save, refresh or click Load; state should restore, including position and smoke config. If the previous smoke was running, it restarts.
- (Optional) Telemetry toggle: set `window.Telemetry.enabled = false` and confirm telemetry logs stop; re-enable and confirm logs resume.

## Stable demo story
- Location: `web/stories/demo.ink` (stable, versioned in git).
- Swap instructions: to test a generated story, serve the repo from root and replace `web/stories/demo.ink` (or use Playwright routing) with your generated file, then run `node scripts/validate-story.js path/to/story.ink` followed by `npm run test:demo`.
- Keep stories small (target 100–400 lines) so validation and Playwright runs stay fast. Ensure each story branches and reaches an `END`.
- CI validate command: `node scripts/validate-story.js web/stories/demo.ink`.

## Notes
- Keep assets lightweight; avoid large binaries. Placeholder visuals are acceptable for this demo.
- If replacing CDN with a vendored copy, prefer a minified build and update documentation accordingly.
