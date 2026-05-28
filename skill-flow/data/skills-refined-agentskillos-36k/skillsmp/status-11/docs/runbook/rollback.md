Rollback Runbook — Demo/Dev

Overview
- This runbook describes how to investigate failed loads and recover player state when the demo reports a rollback.

Steps
1) Reproduce the failure locally using the demo:
   - Start demo server: `npm run serve-demo -- --port 4173`
   - Open `http://127.0.0.1:4173/demo`
   - Corrupt the local save: `localStorage.setItem('ge-hch.smoke.save', 'not-a-json')` and click Load.

2) Inspect rollback artifacts:
   - Demo persistence writes debug saves to `src/.saves/` when `post_checkpoint` and `on_rollback` occur.
   - List files: `ls -la src/.saves`
   - View a file: `cat src/.saves/<file>.save`

3) Inspect integration logs:
   - Persistence subscriber also writes integration audit logs to `.runtime_logs/integration.log`.
   - `tail -n 200 .runtime_logs/integration.log` to see recent events.

4) Restore a known-good save
   - Replace `.saves/<file>.save` content into localStorage key `ge-hch.smoke.save` or use `node` to write a test save using `src/runtime/save-adapter.js`.

5) If corruption is systemic
   - Identify the failing component by searching stack traces in browser DevTools and logs.
   - If save schema versions mismatched, use the `load-adapter` logic in `src/runtime/load-adapter.js` to determine migration path.

Notes
- Production: migrate to IndexedDB and centralized telemetry ingestion. Demo persistence is for developer debugging only.
