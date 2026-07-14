#!/usr/bin/env bash
# Hands-free driver: wait for the SIF puller to populate the base-image cache,
# then run SkillsBench execution for iter_1, iter_2 and a clean re-run of iter_3
# so every meta-skill gets a reward/pass@1 for the comparison table.
set -uo pipefail
cd /home/daweili5/meta-skill-evolving/skill-flow
LOG=/scratch/daweili5/meta_skill_evolve/posthoc_driver.log
SIFDIR=/scratch/daweili5/apptainer-sif

echo "[driver $(date)] waiting for SIF puller to finish..." >> "$LOG"
while ps -eo cmd | grep -q 'python.*[p]refetch_sifs'; do sleep 60; done

nsif=$(ls "$SIFDIR"/*.sif 2>/dev/null | wc -l)
echo "[driver $(date)] puller done; SIFs cached: $nsif" >> "$LOG"
ls "$SIFDIR"/*.sif >> "$LOG" 2>&1

# the dominant ubuntu:24.04 image is required (57 tasks); without it, abort
if [ ! -f "$SIFDIR/ubuntu_24.04.sif" ]; then
  echo "[driver $(date)] ubuntu_24.04.sif missing — executions would mostly fail; aborting" >> "$LOG"
  touch /scratch/daweili5/meta_skill_evolve/POSTHOC_ABORTED
  exit 1
fi

# clear iter_3's stale all-RuntimeError evaluation so it re-runs clean
rm -rf /tmp/metaskill-autoskill-full/iter_3/evaluation

set -a; source .env; set +a
export APPTAINER_CACHEDIR=/scratch/daweili5/apptainer-cache
export APPTAINER_SIF_DIR="$SIFDIR"
export HARBOR_APPTAINER_ROOT=/tmp/harbor-apptainer-metaskill

echo "[driver $(date)] running posthoc_exec 1 2 3 ..." >> "$LOG"
/scratch/daweili5/skill-flow-venv/bin/python -m meta_skill.posthoc_exec 1 2 3 >> "$LOG" 2>&1
echo "[driver $(date)] posthoc_exec DONE" >> "$LOG"
touch /scratch/daweili5/meta_skill_evolve/POSTHOC_DONE
