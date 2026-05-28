---
name: mxl-driver-ase
description: This skill should be used when users want to run the ASE driver for classical/BOMD dynamics in MaxwellLink and need charge conventions and socket/embedded invocation patterns.
---

# ASE driver (`ase`)

## Confirm prerequisites
- Ensure `ase` is installed in the driver environment.
- Ensure the chosen ASE calculator backend is installed (e.g., Psi4/ORCA/DFTB+).

## Configure socket mode
- Run:
  - `mxl_driver --model ase --address <host> --port <port> --param "atoms=../HCN_benchmark/hcn.xyz, calculator=psi4, calc_kwargs=method=b3lyp, basis=cc-pvdz, memory=2GB, num_threads=1, charges=[-0.2467948 -0.00296554 0.24976034]"`

## Configure embedded mode
- Instantiate:
  - `Molecule(driver="ase", driver_kwargs={...})`

## Notes
- Provide either `charges=[...]` or set `recompute_charges=true`; the driver errors if no charges are available.
- CLI parsing splits on commas: pass arrays/lists as space-separated values in brackets (no commas), e.g. `charges=[0.1 -0.2 0.1]`.
- For Psi4-backed ASE calculations, `basis`, `memory`, `num_threads`, etc. can be passed as top-level tokens; the driver forwards unknown keys to the calculator.
- Read full parameter docs in `docs/source/drivers/ase.rst`.
