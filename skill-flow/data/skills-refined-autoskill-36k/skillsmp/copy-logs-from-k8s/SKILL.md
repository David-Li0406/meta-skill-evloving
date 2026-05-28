---
name: copy-logs-from-k8s
description: Use when you need to download tikv/tiflash/s3clean logs from a Kubernetes cluster using scripts/copy_logs_from_k8s.py, including selecting specific sources and saving per-pod folders.
---

# Copy Logs From K8s

## Quick Start
- Ensure `kubectl` points to the target cluster.
- Run from the analysis directory so logs are saved there:
```
python3 .codex/copy-logs-from-k8s/scripts/copy_logs_from_k8s.py
```
- Download specific sources:
```
python3 scripts/copy_logs_from_k8s.py --sources tikv
python3 scripts/copy_logs_from_k8s.py --sources tikv,tiflash
```
- Or specify sources directly from the analysis directory:
```
python3 .codex/copy-logs-from-k8s/scripts/copy_logs_from_k8s.py --sources tiflash
```

## Outputs
- Logs are saved under `./<pod-name>/...` in the current working directory.
- tikv: `/var/lib/tikv/log`
- tiflash: `/data0/logs` (uses container `serverlog`)
- s3clean: `/tmp/s3clean.log` -> `./<pod>/s3clean.log`

## Notes
- tiflash logs use `kubectl exec ... cat` because filenames can include `:` which breaks `kubectl cp`.
- Large log sets can take time to copy; re-run safely if interrupted.

## Extend To Other Pods
- Edit `scripts/copy_logs_from_k8s.py`.
- Add the new source name to `AVAILABLE_SOURCES`.
- Add a `LogSource(...)` entry in `sources` within `main()`:
  - Set `pod_predicate` to match pod names.
  - Use `log_dir` to copy a directory or `single_file` for one file.
  - Set `container` if the pod requires a specific container.
  - Set `use_exec_copy=True` if `kubectl cp` fails or filenames include `:`.
