#!/usr/bin/env bash
set -euo pipefail
while true; do
  python3 - <<'PY'
import os, sys
log_path = '/workspace/Outputs/GPU_Pipeline_Park_R_Batch1/processing_log.txt'
staging_dir = '/workspace/Staging/Park_R_Batch1'
if not os.path.isfile(log_path) or not os.path.isdir(staging_dir):
    sys.exit(0)
cur = None
status_done = False
done = []
with open(log_path, 'r', errors='ignore') as f:
    for line in f:
        if line.startswith('[') and 'Processing:' in line:
            if cur and status_done:
                done.append(cur)
            try:
                cur = line.split('Processing:',1)[1].strip()
            except Exception:
                cur = None
            status_done = False
        elif line.startswith('  '):
            s = line.strip()
            if s.startswith('Found') or s.startswith('No people detected'):
                if cur:
                    status_done = True
    if cur and status_done:
        done.append(cur)
for base in dict.fromkeys(done):
    path = os.path.join(staging_dir, base)
    if os.path.isfile(path):
        try:
            os.remove(path)
            print('deleted', path)
        except Exception as e:
            print('error', path, e)
PY
  sleep 60
done
