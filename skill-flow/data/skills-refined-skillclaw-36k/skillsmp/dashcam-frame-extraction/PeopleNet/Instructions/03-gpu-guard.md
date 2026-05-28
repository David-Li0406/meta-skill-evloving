# 03 - GPU Guard (≥2GB free VRAM, util <85%)

Quick checks:
```bash
nvidia-smi --query-gpu=memory.total,memory.used,utilization.gpu --format=csv,noheader,nounits
```

Interpretation:
- Ensure `memory.total - memory.used >= 2000` (MiB)
- Ensure `utilization.gpu < 85`

Optional live watch:
```bash
watch -n1 "nvidia-smi --query-gpu=memory.free,memory.used,utilization.gpu --format=csv,noheader,nounits"
```

Checkpoint (return):
- The one‑line `nvidia-smi` output showing total, used, and utilization


