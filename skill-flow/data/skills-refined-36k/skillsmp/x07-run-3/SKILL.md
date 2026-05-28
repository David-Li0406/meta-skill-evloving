---
name: x07-run
description: Canonical execution front door for X07 programs (solve-* and run-os*), producing pass-through runner reports.
metadata:
  short-description: Run programs (canonical)
  version: 0.1.0
  kind: docs
---

# x07-run

Use this skill for normal program execution. `x07 run` dispatches to:

- `x07-host-runner` for deterministic `solve-*` worlds
- `x07-os-runner` for `run-os*` worlds

## Canonical commands

- Run the current project (auto-discovers `x07.json`):
  - `x07 run`

- Run a specific project profile:
  - `x07 run --profile test`
  - `x07 run --profile os`
  - `x07 run --profile sandbox`

- Check platform prerequisites for OS worlds (C compiler + common native deps):
  - `x07 doctor`

- Run a deterministic fixture world:
  - `x07 run --world solve-fs --fixtures fixtures`

- Run with real OS access (non-deterministic):
  - `x07 run --os`
  - (equivalently) `x07 run --world run-os`

- Generate a base sandbox policy:
  - `x07 policy init --template cli`
  - `x07 policy init --template http-client`
  - `x07 policy init --template web-service`
  - `x07 policy init --template fs-tool`
  - `x07 policy init --template sqlite-app`
  - `x07 policy init --template postgres-client`
  - `x07 policy init --template worker`

  Policies are starting points: review and extend them for your app (roots, env keys, subprocess allowlists, limits).
  For net-enabled templates, keep `net.allow_hosts: []` in the base policy and use `--allow-host` / `--deny-host` to materialize derived policies for specific destinations.

- Run policy-enforced OS world (requires a policy file):
  - `x07 run --world run-os-sandboxed --policy .x07/policies/base/cli.sandbox.base.policy.json`

- Materialize a derived policy with explicit network destinations (deny-by-default):
  - `x07 run --world run-os-sandboxed --policy .x07/policies/base/http-client.sandbox.base.policy.json --allow-host example.com:443`
  - `x07 run --world run-os-sandboxed --policy .x07/policies/base/http-client.sandbox.base.policy.json --allow-host example.com:80,443 --deny-host example.com:80`

## Inputs

Default is empty input bytes. Provide input via:

- file: `x07 run --input input.bin`
- stdin: `cat input.bin | x07 run --stdin`
- base64: `x07 run --input-b64 <BASE64>`

For CLI-style programs that expect `argv_v1`, pass process args after `--` and `x07 run` will encode them into input bytes:

- `x07 run --profile test -- tool --help`
- `x07 run --profile os -- tool --url https://example.com --depth 2 --out out/results.txt`

## Output contract

- Default output is a pass-through runner report JSON object on stdout:
  - `x07-host-runner.report@...` for `solve-*`
  - `x07-os-runner.report@...` for `run-os*`
- Parse based on `schema_version`.

Optional wrapper (debuggable resolution envelope):

- `x07 run --report wrapped`
- Wrapper schema: `x07.run.report@0.1.0` (field `report` contains the raw runner report object).
