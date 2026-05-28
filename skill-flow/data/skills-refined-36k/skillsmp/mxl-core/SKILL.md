---
name: mxl-core
description: This skill should be used when users need the canonical MaxwellLink workflow, including socket vs embedded coupling, units/time handling, and MPI/HPC invariants.
---

# MaxwellLink core workflow

## Enforce invariants
- Create new runnable inputs only under `projects/YYYY-MM-DD-NAME/`.
- Keep runs reproducible by storing parameters in a `config.json` (or similar) and avoiding hard-coded absolute paths.
- Never pass both `hub=...` and `driver=...` to `maxwelllink.Molecule`; provide exactly one.

## Choose coupling mode
- Use embedded mode when the driver can run in the same Python process:
  - Construct molecules with `Molecule(driver="<id>", driver_kwargs={...})`.
- Use socket mode when drivers must run as separate processes or nodes:
  - Construct a `SocketHub(...)`, pass `hub=hub` into each `Molecule(...)`, and launch one `mxl_driver --model <id> ...` per molecule.

## Handle units/time
- For Meep: set `time_units_fs` on `MeepSimulation(...)` and keep it consistent when interpreting driver times.
- For SingleMode/LaserDriven: work directly in atomic units and set `dt_au` explicitly.

## Handle MPI and multi-process execution
- Launch socket drivers only once (rank 0) under MPI; rely on MaxwellLink broadcasts for other ranks.
- Set generous `timeout` for HPC and tune `latency` to match driver cost.
- If attaching many molecules, consider `store_additional_data=False` for most molecules to limit memory usage; keep it `True` only for the molecules you intend to export/plot.

## Validate before running
- Use `skills/mxl-project-scaffold/scripts/mxl_validate_project.py` to sanity-check `config.json` and required files.
- When debugging behavior, compare to patterns in `tests/` and `docs/source/usage.rst`.

## References
- Solver choice: `skills/mxl-core/references/solver_quickref.md`
- Driver choice: `skills/mxl-core/references/driver_quickref.md`
