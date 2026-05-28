---
name: mxl-driver-psi4-rttddft
description: This skill should be used when users want to run the Psi4 RT-TDDFT driver (rttddft) with MaxwellLink and need required inputs, parameters, and socket/embedded invocation patterns.
---

# Psi4 RT-TDDFT driver (`rttddft`)

## Confirm prerequisites
- Ensure `psi4` is installed and importable in the driver environment.
- Provide an XYZ geometry file whose second line specifies charge and multiplicity (e.g., `0 1`).

## Configure socket mode
- Run:
  - `mxl_driver --model rttddft --address <host> --port <port> --param "molecule_xyz=../tddft_benchmark/hcn.xyz, functional=b3lyp, basis=cc-pvdz, dt_rttddft_au=0.04, dft_grid_name=SG1, electron_propagation=pc, threshold_pc=1e-6, memory=16GB, num_threads=16" --verbose`

## Configure embedded mode
- Instantiate:
  - `Molecule(driver="rttddft", driver_kwargs={...})`

## Notes
- Keep `dt_rttddft_au` small enough for stable electronic propagation; the driver can sub-step under a larger EM time step.
- On HPC, match `num_threads` to `--cpus-per-task` (single driver) or set `num_threads=1` when launching many drivers in the same SLURM job.
- Use `checkpoint=true` and `restart=true` for long jobs or unstable HPC environments.
- Read full parameter docs in `docs/source/drivers/rttddft.rst`.
