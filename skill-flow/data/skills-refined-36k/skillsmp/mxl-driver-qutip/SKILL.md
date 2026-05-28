---
name: mxl-driver-qutip
description: This skill should be used when users want to run the QuTiP molecular driver (preset TLS or custom Hamiltonians) in MaxwellLink and need correct parameter passing for socket or embedded mode.
---

# QuTiP driver (model Hamiltonians)

## Confirm prerequisites
- Ensure `qutip` is installed in the driver environment; import failures are expected otherwise.

## Use preset TLS mode
- Prefer passing TLS parameters as top-level tokens to avoid comma-parsing confusion:
  - Socket: `mxl_driver --model qutip --port <port> --param "preset=tls, omega=0.242, mu12=187, orientation=2, pe_initial=1e-4"`
  - Embedded: `Molecule(driver="qutip", driver_kwargs={"preset": "tls", "omega": 0.242, "mu12": 187, "orientation": 2, "pe_initial": 1e-4})`

## Use custom-module mode
- Provide a Python file that defines `build_model(**kwargs)` and returns `H0`, `mu_ops`, optional `c_ops`, and optional `rho0`.
  - Socket (module next to the job): `mxl_driver --model qutip --port <port> --param "preset=custom, module=hcn_qutip.py"`
  - Socket (absolute path): `mxl_driver --model qutip --port <port> --param "preset=custom, module=/abs/path/spec.py"`
  - Embedded: `Molecule(driver="qutip", driver_kwargs={"preset": "custom", "module": "hcn_qutip.py"})`
  - Ensure the driver process can import the module:
    - Launch the driver from the directory that contains the module, or
    - Add that directory to `PYTHONPATH`, or
    - Use an absolute `module=...` path on shared filesystem.

## Notes
- Use `fd_dmudt=true` only when an analytical dipole-current expression is unavailable or unstable.
- For example setups, compare to `tests/test_qutip/` and `docs/source/drivers/qutip.rst`.
