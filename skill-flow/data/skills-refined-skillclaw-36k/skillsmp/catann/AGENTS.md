# Catann Skill Guide (authoritative, self-updating)

This document is the **single source of truth** for working on Catann tests and
related tooling. Update it in-place whenever new knowledge is discovered so it
stays accurate and complete. Do **not** add a changelog.

## Purpose
- Ensure the Catann test workflow is repeatable and reliable.
- Capture discoveries about how the Catann test harness and `catann_files` work.

## Key implementation facts
- The Catann iframe script (`src/routes/catann/app/IframeScriptString.ts`) loads
  the Colonist client from `public/public_catann/index.html`, and in dev mode
  rewrites CDN asset URLs to `/public_catann/catann_files` so assets and bundles
  load locally.
- WebSocket traffic is intercepted in the iframe:
  - `WebSocket.send` posts `{ catann: true, id, clientData }` to the parent.
  - The parent test listens for `message` events and records `clientData` bytes
    for comparison.
- `catann_files` enums in `src/routes/catann/app/catann_files_enums.ts` mirror
  values extracted from the Colonist bundles under
  `public/public_catann/catann_files` and are used by Catann logic.

## Test expectations and comparisons
- `starting_settlement.json` stores expected `socket.send` byte arrays for the
  starting settlement flow.
- The Playwright test compares captured `socket.send` messages to the expected
  list **after filtering ignorable heartbeats** (payloads that start with
  `[4, 8, ...]`).
- Only click interactions should drive the test flow; avoid DOM or canvas
  injections in finished tests.

## Asset and file locations
- Catann client assets: `public/public_catann/catann_files/`
- Catann test harness: `src/routes/catann/test/playwright_test.spec.ts`
- Expected message recordings: `src/routes/catann/test/starting_settlement.json`
