---
name: mxl-driver-tls
description: This skill should be used when users want to run the built-in TLS (two-level system) driver in socket or embedded mode and need parameter conventions and example commands.
---

# TLS driver (two-level system)

## Use for lightweight benchmarks
- Use the built-in TLS driver (`tls`) for fast regression and simple light–matter prototyping.

## Configure embedded mode
- Instantiate:
  - `Molecule(driver="tls", driver_kwargs=dict(omega=..., mu12=..., orientation=..., pe_initial=..., checkpoint=..., restart=...))`

## Configure socket mode
- Launch one process per molecule:
  - `mxl_driver --model tls [--unix --address <name> | --address <host> --port <port>] --param "omega=..., mu12=..., orientation=..., pe_initial=..."`
- Keep the hub address/port/unixsocket consistent with the EM script.

## Key parameters
- `omega` (a.u.), `mu12` (a.u.), `orientation` (`0|1|2` for x/y/z), `pe_initial` (0–1), `checkpoint`, `restart`.

## Notes
- Prepare a coherent (superposition) initial TLS state by setting `0 < pe_initial < 1`; this seeds emission into vacuum-like classical fields.
- Read outputs from `molecule.additional_data_history` (keys include `time_au`, `Pe`, `Pg`, dipoles, energies).
- Use post-processing guidance in `skills/mxl-postprocess/SKILL.md`.

