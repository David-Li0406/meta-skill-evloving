#!/usr/bin/env bash
#SBATCH -J mxl_main
#SBATCH -o mxl_main.%j.out
#SBATCH -e mxl_main.%j.err

set -euo pipefail
srun -n "${SLURM_NTASKS:-1}" python -u em_main.py
