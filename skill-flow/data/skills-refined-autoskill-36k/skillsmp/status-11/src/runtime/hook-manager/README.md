Runtime HookManager

Usage snippets (demo):

const HookManager = require('../hook-manager');
const createTelemetrySubscriber = require('../subscribers/telemetry');
const createPersistenceSubscriber = require('../subscribers/persistence');

const hm = new HookManager();
const telemetry = createTelemetrySubscriber(console);
const persistence = createPersistenceSubscriber();

// register handlers
hm.on('pre_inject', telemetry.pre_inject);
hm.on('post_inject', telemetry.post_inject);
hm.on('pre_checkpoint', telemetry.pre_checkpoint);
hm.on('post_checkpoint', telemetry.post_checkpoint);

hm.on('state_change', persistence.on_state_change);
hm.on('audit', persistence.audit);

// emit example
await hm.emitParallel('pre_inject', { branchId: 'b1' });

Note: subscribers must be resilient; HookManager will catch and surface handler results without throwing.

Demo additions in this branch:

- `src/runtime/subscribers/demo-persistence.js` — writes debug `.save` artifacts to `src/.saves/` on `post_checkpoint` and `on_rollback` (dev/demo only).
- `web/demo/js/runtime-hooks-shim.js` — attempts to register the demo persistence subscriber when loaded in a bundler/node-like environment so debug saves are produced during local dev and CI.
- `web/demo/js/inkrunner.js` — shows a lightweight rollback toast UI when a load fails. The toast is demo-only and displays a pointer to `src/.saves/` where debug artifacts are written.

How to test the rollback toast in a browser:

1) Start the demo server:
   - `npm run serve-demo -- --port 4173`
   - Open `http://127.0.0.1:4173/demo` in your browser.

2) Cause a load failure to trigger rollback handling. Two quick options:
   - Corrupt the saved payload:
     a) Open DevTools → Console
     b) Run: `localStorage.setItem('ge-hch.smoke.save', 'not-a-json')`
     c) Click the "Load" button in the demo page or run: `window.__inkrunner.loadState()`
     d) You should see a red toast at the bottom-right with a message referencing `/src/.saves/`.

   - Remove InkJS or simulate an error during load:
     a) In DevTools Console run: `delete window.inkjs` then click "Load" or call `window.__inkrunner.loadState()`.
     b) The toast should appear when the load fails and `on_rollback` is emitted.

3) Inspect debug saves:
   - On successful `post_checkpoint` events the demo persistence subscriber writes files to `src/.saves/`.
   - On failures the subscriber writes a small rollback debug save you can inspect.
   - Inspect saved files from your shell: `ls -l src/.saves && cat src/.saves/<file>.save`.

Notes & caveats:
- The toast and demo persistence are intentionally lightweight and for development only; they rely on the bundler/node environment to register persistence. Plain static-only page loads may not register the demo persistence subscriber.
- The debug save directory is `src/.saves/` in the repository root. CI artifacts may be stored elsewhere depending on CI config.

If you want, I can also add a query-parameter toggle (e.g., `?demo_persistence=1`) so the demo registers the subscriber even on static loads. Would you like that?
