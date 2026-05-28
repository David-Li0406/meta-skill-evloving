#!/usr/bin/env bash
set -euo pipefail
ROOT_FS="/"
PEOPLENET_ROOT="/home/yousuf/PROJECTS/PeopleNet"
STATE="/home/yousuf/PROJECTS/PeopleNet/state"
CONFIGS="/home/yousuf/PROJECTS/PeopleNet/configs"
PENDING="/pending_yesterday.txt"
PROC="/processed_videos.txt"
IMG="nvcr.io/nvidia/deepstream:6.4-triton-multiarch"
WIN_SRC_PREFIX="/media/yousuf/C67813AB7813996F1"
INCONT_PREFIX="/mnt/windows"
MIN_FREE_GB=20
log(){ echo "[2025-11-15 19:05:02] "; }
log "batch start"
TOTAL=1355
log "pending_total="
while IFS= read -r SRC; do
  [ -n "" ] || continue
  [ -f "" ] || { log "skip_missing: "; continue; }
  if grep -Fxq "" "/home/yousuf/PROJECTS/PeopleNet/state/processed_videos.txt" 2>/dev/null; then
    log "skip_processed: "; continue
  fi
  FREE_GB=
  if [[ -z "" || "" -lt "" ]]; then
    log "guard_low_space before: 0GB; pruning..."
    docker container prune -f >/dev/null 2>&1 || true
    docker image prune -f >/dev/null 2>&1 || true
    FREE_GB=
    if [[ -z "" || "" -lt "" ]]; then
      log "guard_still_low: 0GB; sleep 30"
      sleep 30
      continue
    fi
  fi
  VID_URI="file://"
  RUN_CONF="/run_1763251502_55308.txt"
  cat > "" <<CONF
[application]
enable-perf-measurement=0

[source0]
enable=1
type=2
uri=
num-decode-surfaces=1

[streammux]
batch-size=1
width=960
height=544
batched-push-timeout=40000
live-source=0

[primary-gie]
enable=1
gpu-id=0
config-file=/work/configs/pgie_peoplenet.txt

[sink0]
enable=1
type=1
sync=0
CONF
  log "run "
  if docker run --rm --gpus all       --log-driver json-file --log-opt max-size=5m --log-opt max-file=1       -v "/home/yousuf/PROJECTS/PeopleNet":/work       -v "":"":ro       -w /work ""       bash -lc "deepstream-app -c /work/configs/""" >/dev/null 2>&1; then
    echo "" >> "/home/yousuf/PROJECTS/PeopleNet/state/processed_videos.txt"
    log "ok "
  else
    log "fail "
  fi
  rm -f "" || true
  DONE=0
  FREE_GB=
  log "progress done= total= free_gb="
  sleep 1
done < "/home/yousuf/PROJECTS/PeopleNet/state/pending_yesterday.txt"
log "batch done"
