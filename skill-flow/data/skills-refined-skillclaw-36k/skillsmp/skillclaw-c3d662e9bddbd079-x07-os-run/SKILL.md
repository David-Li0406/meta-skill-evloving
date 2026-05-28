---
name: x07-os-run
description: Use this skill when you need to execute OS-world programs with real I/O or in a sandboxed environment using the x07 framework.
---

# Skill body

Prefer `x07 run --os` (or `x07 run --world run-os*`) for normal execution. Use `x07-os-runner` directly only when you need runner-specific flags (policy debugging, auto-FFI toggles, explicit compiled artifact paths) or when you are debugging runner behavior.

## Canonical commands (recommended: `x07 run`)

- **Run the current project (unsandboxed)**:
  - `x07 run --os`
  - (equivalently) `x07 run --world run-os`

- **Run a project explicitly (unsandboxed)**:
  - `x07 run --project x07.json --world run-os`

- **Run sandboxed (requires an explicit policy)**:
  - `x07 run --project x07.json --world run-os-sandboxed --policy run-os-policy.json`

- **Generate a schema-valid base policy**:
  - `x07 policy init --template cli`
  - `x07 policy init --template http-client`
  - `x07 policy init --template web-service`
  - `x07 policy init --template fs-tool`
  - `x07 policy init --template sqlite-app`
  - `x07 policy init --template postgres-client`
  - `x07 policy init --template worker`

- **Materialize a derived policy with explicit destinations (only in run-os-sandboxed)**:
  - `x07 run --project x07.json --world run-os-sandboxed --policy .x07/policies/base/http-client.sandbox.base.policy.json --allow-host example.com:443`
  - `x07 run --project x07.json --world run-os-sandboxed --policy .x07/policies/base/http-client.sandbox.base.policy.json --deny-host example.com:*`

- **Run a single program (when not using a project manifest)**:
  - `x07 run --program src/main.x07.json --world run-os --module-root src`

## Expert backend commands (`x07-os-runner`)

- **Run a program (unsandboxed)**:
  - `x07-os-runner --program src/main.x07.json --world run-os --module-root src`

- **Run a project (unsandboxed)**:
  - `x07-os-runner --project x07.json --world run-os`

- **Run sandboxed (requires an explicit policy)**:
  - `x07-os-runner --program src/main.x07.json --world run-os-sandboxed --policy run-os-policy.json --module-root src`

## Policy

Policies are a starting point. Generate one from a template, then extend it deliberately for your app (roots, env, subprocess allowlists, limits).