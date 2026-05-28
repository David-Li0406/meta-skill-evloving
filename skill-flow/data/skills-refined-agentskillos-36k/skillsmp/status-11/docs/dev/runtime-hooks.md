Runtime Hook Points — Usage Guide

Purpose
- Describe supported runtime hook points, example subscriber usage, and demo registration patterns.

Hook points available (demo/runtime)
- pre_inject: emitted before proposal generation/injection begins. Handlers may augment payload or record telemetry.
- post_inject: emitted after a proposal is produced but before it is surfaced to the player.
- pre_checkpoint: emitted synchronously before a checkpoint/save is written; handlers can mutate the save payload.
- post_checkpoint: emitted after a save is persisted; useful for persistence/audit subscribers.
- pre_load: emitted before a load is attempted; handlers may validate or veto the load.
- on_restore: emitted after a successful load/restore.
- on_rollback: emitted when a load fails and a rollback path is taken.
- on_commit / pre_commit / post_commit: beats used around AI branch commit flow (demo emits on_commit after branch play).

Example subscriber (Node/demo)
- File: `src/runtime/subscribers/demo-persistence.js`
- Registers handlers for `post_checkpoint` and `on_rollback` to write debug save artifacts under `src/.saves/` using the project's save-adapter.

Quick registration (demo shim)
- The demo shim will attempt to register demo persistence when running in a bundler/node-like environment:
  - `web/demo/js/runtime-hooks-shim.js` contains registration logic that requires `../../src/runtime/subscribers/demo-persistence` and attaches handlers to `window.RuntimeHooks`.

Best practices for subscribers
- Be async/Promise-friendly: HookManager awaits handlers but shields failures; swallow internal errors or return status objects.
- Keep handlers idempotent and non-blocking where possible (e.g., enqueue background writes rather than blocking story progress).
- Sanitize payloads and redact PII before writing logs or telemetry.

Where to look in repo
- HookManager implementation: `src/runtime/hook-manager/index.js`
- README & examples: `src/runtime/hook-manager/README.md`
- Demo shim registration: `web/demo/js/runtime-hooks-shim.js`
- Demo persistence example: `src/runtime/subscribers/demo-persistence.js`

How to run (demo)
1) Serve demo: `npm run serve-demo -- --port 4173`
2) Open: `http://127.0.0.1:4173/demo`
3) Attach a subscriber in console (advanced):
   - `window.RuntimeHooks.on('post_checkpoint', p => console.log('post_checkpoint', p));`

Acceptance criteria (docs)
- Clear examples show how to subscribe and where hook points fire.
- Demo shows persistent artifacts under `src/.saves/` when `post_checkpoint` occurs.

Notes
- These hooks are intentionally lightweight. For production usage consider an adapter that forwards telemetry to a remote ingest pipeline and a persistence adapter that uses IndexedDB or host-provided storage for large payloads.