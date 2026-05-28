# 09 - Final Report (Verification Artifacts)

When done, provide:

1) Discovery
- Lines/counts of `state/src_park_f.txt`, `state/src_park_r.txt`
- Pending count and first 5–10 entries from `state/pending_videos.txt`

2) Staging and Guards
- `df -h` (first 2 lines) before/after last staging step
- One‑line `nvidia-smi` snapshot: `memory.total, memory.used, utilization.gpu`

3) Inference Samples
- Path of one per‑video CSV and `head -n 5` of it
- Last 20 lines of the most recent DeepStream log

4) Consolidation
- `consolidated_rows` and `central_log_rows` printed values
- `head -n 5` of `Outputs/peoplenet_consolidated.csv`

5) Optional QC
- Preview directory path and 3 sample filenames


