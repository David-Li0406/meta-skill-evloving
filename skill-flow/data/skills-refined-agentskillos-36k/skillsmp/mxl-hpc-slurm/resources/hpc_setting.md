# HPC Setting (Single Source of Truth)

> Agents using the `mxl-hpc-slurm` skill must read this file **before** generating SLURM scripts. If the user requests a different cluster, ask for overrides; otherwise default to this profile.

## Cluster profile: Purdue Anvil
- Docs: https://www.rcac.purdue.edu/knowledge/anvil/run/examples/slurm
- Nodes: 128 CPU cores per node, ~2 GiB RAM per core (≈256 GiB per node)
- Queues (partitions):
  - `shared` — up to 128 CPUs on one node (ideal default for single-node hub+driver tests)
  - `wholenode` — full-node multiples (128 × N tasks) for large MPI/driver swarms
- File systems: use the job submit directory (`$SLURM_SUBMIT_DIR`) or project scratch that is visible to dependent jobs.

## Agent defaults when emitting SLURM headers
- Always include `--nodes` + `--ntasks`; keep `--nodes=1` unless the user asks for multi-node scaling.
- Default walltime: `--time=02:00:00` for quick tests; extend if user supplies expected runtime.
- Use `--job-name` to reflect the case name (e.g., `mxl_main`, `mxl_driver`).
- Write stdout/stderr to `%j`-suffixed files to keep runs separate.

### Single-job template (one-node hub + drivers)
```bash
#!/usr/bin/env bash
#SBATCH --nodes=1
#SBATCH --ntasks=128           # adjust downward if not using all cores
#SBATCH --time=02:00:00
#SBATCH -J mxl_anvil_test
#SBATCH -o mxl.%j.out
#SBATCH -e mxl.%j.err
#SBATCH -p shared

set -euo pipefail
module purge
module load anaconda/2023.03 || true   # optional; keep if available

srun -n "${SLURM_NTASKS:-1}" python -u em_main.py
```

### Two-step pattern (recommended with `mxl-hpc-slurm` skill)
- Main job starts the hub, writes `tcp_host_port_info.txt`, and binds host/port as in `skills/mxl-hpc-slurm/references/slurm_recipes.md`.
- Driver job(s) wait for the file, read host/port, then run `mxl_driver ... --address "$HOST" --port "$PORT"`.
- Submit driver job with `sbatch --dependency=after:${job_main_id}`.
- Use `shared` for single-node tests; switch to `wholenode` if you truly need 128×N tasks across N nodes.

## When to adjust settings
- GPU runs: Anvil GPUs live in other partitions (not covered here); ask the user for partition/constraint names.
- Large memory: request `--mem` explicitly if >2 GiB per task is required; otherwise defaults suffice.
- Multi-node MPI: set `--nodes=N`, `--ntasks-per-node=128`, keep `wholenode`.

## Quick checklist for agents
- [ ] Confirm cluster = Anvil; if not, collect partition, cores/node, walltime defaults.
- [ ] Use paths visible to all dependent jobs (shared filesystem).
- [ ] Add `set -euo pipefail` and `module purge` to scripts.
- [ ] Emit `%j` in log filenames to avoid collisions.
- [ ] Persist `tcp_host_port_info.txt` beside the SLURM scripts so driver jobs can read it.
