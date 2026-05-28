---
name: bootstrap-qcow2-build-plan-iteration
description: Iterate bootstrap-qcow2 sysroot/rootfs build plans inside the container using sysroot-runner overrides, state bookmarks, and failure reports, then back-annotate stable fixes into SysrootBuilder for reproducible clean builds.
---

# Iterate the sysroot/rootfs build plan (in-container)

Treat the build plan JSON as immutable during iteration. Use the overrides file for “what should be back-annotated later”, and use the state file for “where am I in this run”.

## Canonical paths (inside the rootfs)

- Plan (immutable): `/var/lib/sysroot-build-plan.json`
- Overrides (mutable, back-annotate later): `/var/lib/sysroot-build-overrides.json`
- State/bookmark (mutable, auto-updated): `/var/lib/sysroot-build-state.json`
- Failure reports (append-only): `/var/lib/sysroot-build-reports/*.json`

Source trees:

- Live repo (mutable, preferred for iteration): `/work/bootstrap-qcow2`
- Staged snapshot (static, produced by sysroot-builder): `/workspace/bootstrap-qcow2-master`

## Minimal iteration loop

1. Confirm you are inside the expected rootfs:
   - `test -f /var/lib/sysroot-build-state.json && cat /var/lib/sysroot-build-state.json`
   - `test -f /var/lib/sysroot-build-plan.json`
   - `test -d /workspace && ls /workspace | head`
2. If you are iterating on the tooling itself, build it from the live repo:
   - `cd /work/bootstrap-qcow2`
   - If Crystal cache permissions fail: `CRYSTAL_CACHE_DIR=/tmp/crystal_cache shards build`
   - Refresh entrypoints: `./bin/bq2 --install`
3. Run the plan:
   - `./bin/bq2 sysroot-runner`
   - The runner auto-resumes by skipping steps listed as completed in `/var/lib/sysroot-build-state.json` and invalidates that state automatically when the overrides file changes.
4. On failure:
   - Read the newest report in `/var/lib/sysroot-build-reports/`.
   - Encode the next hypothesis in `/var/lib/sysroot-build-overrides.json`.
   - Re-run `./bin/bq2 sysroot-runner` (avoid changing the plan JSON).

## Codex session continuity

When launching Codex via `bq2 codex-namespace`, the wrapper stores the most recent Codex session id in `/work/.codex-session-id` and will auto-resume it on the next `bq2 codex-namespace` run.

## Back-annotate after a successful round

When a full phase (or full end-to-end run) succeeds with the overrides in place:

1. Translate the effective overrides into `src/sysroot_builder.cr` (usually `phase_specs`, per-package flags, patches, env, destdir/prefix defaults).
2. Add/adjust specs to lock in the new behavior.
3. Delete `/var/lib/sysroot-build-overrides.json` and `/var/lib/sysroot-build-state.json`.
4. Re-run from scratch (rebuild the rootfs workspace if needed) to validate the plan is now reproducible without overrides.

## Use CLI flags only for narrow debugging

`sysroot-runner` supports flags like `--phase` and `--package`, but prefer the continuous loop above: run the default plan, let state handle resume, and keep your mutable intent in the overrides file.
