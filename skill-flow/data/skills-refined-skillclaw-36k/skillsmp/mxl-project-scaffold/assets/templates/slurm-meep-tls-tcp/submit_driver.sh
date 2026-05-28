#!/usr/bin/env bash
#SBATCH -J mxl_driver
#SBATCH -o mxl_driver.%j.out
#SBATCH -e mxl_driver.%j.err

set -euo pipefail
python driver.py

