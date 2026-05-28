# SingleModeSimulation + TLS (TCP socket)

This template runs `SingleModeSimulation` coupled to a TLS driver over TCP (fast socket workflow on one machine).

## Run (two terminals)

Terminal A (EM / SingleModeSimulation):
```bash
python em.py
```

Terminal B (driver):
```bash
python driver.py
```

## Edit parameters
Edit `config.json`:
- Hub: `hub.host`, `hub.port`, `hub.timeout`, `hub.latency`
- Single-mode simulation: `sim.*` (atomic units)
- TLS: `tls.*` (used by `driver.py`)

The run writes `tls_history.csv` (or `output_csv`) in this folder.

