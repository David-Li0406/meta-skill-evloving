---
name: mxl-driver-psi4-rtehrenfest
description: This skill should be used when users want to run the Psi4 RT-Ehrenfest driver (rtehrenfest) with MaxwellLink and need parameters, charge conventions, and socket/embedded invocation patterns.
---

# Psi4 RT-Ehrenfest driver (`rtehrenfest`)

## Confirm prerequisites
- Ensure `psi4` is installed and importable in the driver environment.
- Provide an XYZ geometry file whose second line specifies charge and multiplicity (e.g., `0 1`).

## Configure socket mode
- Run:
  - `mxl_driver --model rtehrenfest --address <host> --port <port> --param "molecule_xyz=../HCN_benchmark/hcn.xyz, functional=b3lyp, basis=cc-pvdz, dt_rttddft_au=0.04788, dft_grid_name=SG1, memory=2GB, num_threads=1, force_type=ehrenfest, n_fock_per_nuc=6, n_elec_per_fock=6"`

## Configure embedded mode
- Instantiate:
  - `Molecule(driver="rtehrenfest", driver_kwargs={...})`

## Notes
- Use `force_type=bo` when nuclear gradients from Born–Oppenheimer surfaces are required; use `force_type=ehrenfest` for mean-field forces.
- When passing `partial_charges` on the command line, use a space-separated list in brackets (no commas), e.g. `partial_charges=[1.0 -1.0 0.0]`.
- On HPC, match `num_threads` to `--cpus-per-task` (single driver) or set `num_threads=1` when launching many drivers in the same SLURM job.
- Read full parameter docs in `docs/source/drivers/rtehrenfest.rst`.
