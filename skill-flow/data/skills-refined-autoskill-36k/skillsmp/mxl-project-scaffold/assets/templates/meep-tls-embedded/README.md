# Meep + TLS (embedded)

This template runs a Meep FDTD simulation coupled to a single TLS driver in **embedded** (non-socket) mode.

## Run
```bash
python em.py
```

## Edit parameters
Edit `config.json`:
- Meep: `time_units_fs`, `cell_size`, `pml_thickness`, `resolution`, `until`
- Molecule placement/regularization: `molecule.*`
- TLS: `tls.*` (atomic units)

The run writes `tls_history.csv` (or `output_csv`) in this folder.

