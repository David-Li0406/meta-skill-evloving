# Meep + TLS (UNIX socket)

This template runs a Meep FDTD simulation coupled to a TLS driver in **socket** mode using a UNIX-domain socket (single node).

## Run (two terminals)

Terminal A (EM / Meep):
```bash
python em.py
```

Terminal B (driver):
```bash
python driver.py
```

## Edit parameters
Edit `config.json`:
- Hub: `unixsocket`, `hub.timeout`, `hub.latency`
- Meep: `time_units_fs`, `cell_size`, `pml_thickness`, `resolution`, `until`
- Molecule placement/regularization: `molecule.*`
- TLS: `tls.*` (used by `driver.py`)

The run writes `tls_history.csv` (or `output_csv`) in this folder.

