---
name: mxl-troubleshoot
description: This skill should be used when MaxwellLink simulations stall, diverge, or produce missing/incorrect observables; it provides a first-aid checklist for sockets, units, and driver configuration.
---

# Troubleshooting first aid

## Socket stalls or deadlocks
- Verify hub and driver agree on `--unix/--address/--port` and the same UNIX socket name or TCP port.
- For SLURM two-step runs, confirm the host/port file is written to a shared directory and the driver job waits until it exists.
- Increase `timeout` for HPC and slow drivers; reduce `latency` only after basic correctness is verified.
- Launch external drivers only once under MPI (rank 0).

## Unit and axis mismatches
- For Meep, verify `time_units_fs` is set and consistent; time is reported in atomic units in driver histories.
- Verify `orientation` (TLS/QuTiP preset) and `coupling_axis` (SingleMode/LaserDriven) are consistent with simulation dimensionality.

## Driver errors
- Confirm optional dependencies are installed in the driver environment (`pymeep`, `qutip`, `psi4`, `ase`).
- For ASE/LAMMPS, confirm per-atom charges exist (`charges=[...]` or `recompute_charges=true`).
- If `get_available_host_port(localhost=False)` fails on a locked-down cluster, avoid outbound probes: bind the hub to `host=""` and write a reachable hostname via `MXL_HOST` or `hostname -f`.
- Enable `checkpoint=true`/`restart=true` when drivers may be pre-empted.

## Next actions
- Compare behavior to minimal reference tests under `tests/`.
- Use `skills/mxl-postprocess/SKILL.md` to export and inspect diagnostics.
