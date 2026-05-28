---
name: x07-agent-playbook
description: Use this skill when you need to establish a baseline workflow for building X07 programs with the released toolchain, ensuring proper execution and management of dependencies.
---

# Skill body

This skill sets the baseline workflow and constraints for autonomous agents writing X07 programs. It assumes end-users only have the released toolchain binaries, not the toolchain source repo.

## Tooling

Execution should go through `x07 run` (single front door). The standalone runner binaries (`x07-host-runner`, `x07-os-runner`) remain available for expert usage, but are not part of the default agent loop.

If the task needs OS worlds or native dependencies (curl/openssl, etc.), run `x07 doctor` early and follow its suggestions.

## Single canonical agent loop (edit → format → lint → run)

1. Create or edit x07AST JSON (`*.x07.json`).
2. Canonicalize formatting:
   - `x07 fmt --input src/main.x07.json --write --report-json`
3. Lint (world-gating + structural checks):
   - `x07 lint --input src/main.x07.json --world solve-pure --report-json`
4. Apply tool-provided quickfixes (when available):
   - `x07 fix --input src/main.x07.json --world solve-pure --write --report-json`
5. If a targeted structural change is needed, apply an explicit JSON Patch:
   - `x07 ast apply-patch --in src/main.x07.json --patch /tmp/repair.patch.json --validate`
6. Run in the correct capability world (canonical: `x07 run`):
   - For deterministic solve worlds (recommended default): `x07 run`
   - For OS worlds (unsandboxed): `x07 run --profile os`
   - For OS worlds (policy-enforced): 
     - Initialize policy: `x07 policy init --template <cli|http-client|web-service|fs-tool|sqlite-app|postgres-client|worker>`
     - Run with policy: `x07 run --profile sandbox` (optionally add `--allow-host ...` / `--deny-host ...` to materialize derived policies)

   For CLI-style programs that expect `argv_v1`, pass process args after `--` and `x07 run` will encode them into input bytes:
   - `x07 run --profile os -- tool --help`

   Expert backends (use only when you need runner-only flags or are debugging runner behavior):
   - For solve worlds: `x07-host-runner --project x07.json`
   - For OS worlds: `x07-os-runner --project x07.json --world run-os`
7. If the project uses dependencies, update the lockfile:
   - `x07 pkg lock --project x07.json`

Keep each iteration small and deterministic; if a repair loop does not converge quickly, stop and re-evaluate the approach.