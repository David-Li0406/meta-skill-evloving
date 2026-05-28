---
name: mxl-postprocess
description: This skill should be used when users need to extract, export, and plot MaxwellLink outputs from molecules and EM solvers (e.g., `additional_data_history`, cavity histories, spectra helpers).
---

# Post-processing and export

## Collect molecular diagnostics
- Read per-molecule diagnostics from `molecule.additional_data_history` (list of dicts).
- Convert to arrays by extracting keys (`time_au`, `mux_au`, `Pe`, `energy_au`, ...).

## Collect solver histories (when enabled)
- For `SingleModeSimulation(record_history=True)`, use `sim.time_history`, `qc_history`, `pc_history`, and `molecule_response_history`.
- For `LaserDrivenSimulation(record_history=True)`, use `sim.time_history`, `drive_history`, and `molecule_response_history`.

## Export
- Write CSV/NPZ from the collected arrays for reproducibility and downstream plotting.
- Keep the export code inside the project folder so it travels with inputs.

## References
- Snippets: `skills/mxl-postprocess/references/postprocessing.md`
- Tools: `src/maxwelllink/tools/` (pulse helpers and spectra utilities)

