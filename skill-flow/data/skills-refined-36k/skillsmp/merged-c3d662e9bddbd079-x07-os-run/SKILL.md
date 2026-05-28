---
name: x07-os-run
description: Use this skill for executing OS-world programs with real I/O or policy-enforced execution via run-os and run-os-sandboxed.
---

# x07-os-run

Prefer `x07 run --os` (or `x07 run --world run-os*`) for normal execution. Use `x07-os-runner` directly only when you need runner-specific flags (policy debugging, auto-FFI toggles, explicit compiled artifact paths) or when debugging runner behavior.

Use this skill when you need real OS I/O (fs/net/process/time) via `run-os` or policy-enforced execution via `run-os-sandboxed`.

## Canonical commands (recommended: `x07 run`)

- Run the current project (unsandboxed):
  - `x07 run --os`
  - (equivalently) `x07 run --world run-os`

- Run a project explicitly (unsandboxed):
  - `x07 run --project <project_file.json> --world run-os`

- Run sandboxed (requires an explicit policy):
  - `x07 run --project <project_file.json> --world run-os-sandboxed --policy <policy_file.json>`

- Generate a schema-valid base policy:
  - `x07 policy init --template <template_name>`

- Materialize a derived policy with explicit destinations (only in run-os-sandboxed):
  - `x07 run --project <project_file.json> --world run-os-sandboxed --policy <policy_file.json> --allow-host <host:port>`
  - `x07 run --project <project_file.json> --world run-os-sandboxed --policy <policy_file.json> --deny-host <host:* >`

- Run a single program (when not using a project manifest):
  - `x07 run --program <program_file.json> --world run-os --module-root <module_root>`

## Expert backend commands (`x07-os-runner`)

- Run a program (unsandboxed):
  - `x07-os-runner --program <program_file.json> --world run-os --module-root <module_root>`

- Run a project (unsandboxed):
  - `x07-os-runner --project <project_file.json> --world run-os`

- Run sandboxed (requires an explicit policy):
  - `x07-os-runner --program <program_file.json> --world run-os-sandboxed --policy <policy_file.json> --module-root <module_root>`

## Policy

Policies are a starting point. Generate one from a template, then extend it deliberately for your app (roots, env, subprocess allowlists, limits). For net-enabled templates, keep `net.allow_hosts` empty in the base policy and use `x07 run --allow-host` to materialize auditable derived policies for specific destinations.

## Output contract

- `x07 run` in `run-os*` worlds prints an `x07-os-runner.report@...` JSON report to stdout (pass-through).
- `x07-os-runner` prints the same report shape when invoked directly.

In both cases:
- Use the process exit code for pass/fail.
- Parse the JSON for `schema_version`, `mode`, `world`, and base64-encoded output bytes.