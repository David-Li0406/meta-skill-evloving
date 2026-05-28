# LaserDrivenSimulation + TLS (embedded)

This template runs `LaserDrivenSimulation` coupled to a single TLS driver in **embedded** mode.

## Run
```bash
python em.py
```

## Edit parameters
Edit `config.json`:
- Simulation: `sim.*` (atomic units)
- Drive: `drive.*`
- TLS: `tls.*` (atomic units)

The run writes `tls_history.csv` (or `output_csv`) in this folder.

