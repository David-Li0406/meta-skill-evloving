---
name: x07-run
description: Use this skill for executing X07 programs, producing pass-through runner reports for both deterministic and non-deterministic environments.
---

# x07-run

Use this skill for normal program execution. `x07 run` dispatches to:

- `x07-host-runner` for deterministic `solve-*` worlds
- `x07-os-runner` for `run-os*` worlds

## Canonical commands

- Run the current project (auto-discovers `x07.json`):
  - `x07 run`

- Run a specific project profile:
  - `x07 run --profile <profile_name>`

- Check platform prerequisites for OS worlds (C compiler + common native deps):
  - `x07 doctor`

- Run a deterministic fixture world:
  - `x07 run --world solve-fs --fixtures <fixtures>`

- Run with real OS access (non-deterministic):
  - `x07 run --os`
  - (equivalently) `x07 run --world run-os`

- Generate a base sandbox policy:
  - `x07 policy init --template <template_name>`

  Policies are starting points: review and extend them for your app (roots, env keys, subprocess allowlists, limits). For net-enabled templates, keep `net.allow_hosts: []` in the base policy and use `--allow-host` / `--deny-host` to materialize derived policies for specific destinations.

- Run policy-enforced OS world (requires a policy file):
  - `x07 run --world <world_name> --policy <policy_file>`

- Materialize a derived policy with explicit network destinations (deny-by-default):
  - `x07 run --world <world_name> --policy <policy_file> --allow-host <host>`
  - `x07 run --world <world_name> --policy <policy_file> --allow-host <host> --deny-host <host>`

## Inputs

Default is empty input bytes. Provide input via:

- file: `x07 run --input <input_file>`
- stdin: `cat <input_file> | x07 run --stdin`
- base64: `x07 run --input-b64 <BASE64>`

For CLI-style programs that expect `argv_v1`, pass process args after `--` and `x07 run` will encode them into input bytes:

- `x07 run --profile <profile_name> -- <tool> <args>`

## Output contract

- Default output is a pass-through runner report JSON object on stdout:
  - `x07-host-runner.report@...` for `solve-*`
  - `x07-os-runner.report@...` for `run-os*`
- Parse based on `schema_version`.

Optional wrapper (debuggable resolution envelope):

- `x07 run --report wrapped`
- Wrapper schema: `x07.run.report@0.1.0` (field `report` contains the raw runner report object).