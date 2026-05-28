# Meep + TLS over TCP (SLURM two-step)

This template illustrates a SLURM two-step pattern for running the EM solver and driver on different nodes:
- Main job starts the `SocketHub` and writes `tcp_host_port_info.txt`
- Driver job waits until the host/port file exists and then connects

## Files
- `config.json`: run parameters
- `em_main.py`: Meep + MaxwellLink main (server)
- `driver.py`: TLS driver launcher (client)
- `submit_main.sh`: SLURM script for the main job
- `submit_driver.sh`: SLURM script for the driver job

## Submit
```bash
job_main_id=$(sbatch submit_main.sh | awk '{print $4}')
sbatch --dependency=after:${job_main_id} submit_driver.sh
```

Convenience:
- `./submit_all.sh`
- `./clean.sh`

## Notes
- If `socket.gethostname()` is not resolvable from the driver node, set a reachable hostname explicitly:
  - `export MXL_HOST=$(hostname -f)`
- Add more driver jobs (each running `driver.py` with different parameters) for multiple molecules.
