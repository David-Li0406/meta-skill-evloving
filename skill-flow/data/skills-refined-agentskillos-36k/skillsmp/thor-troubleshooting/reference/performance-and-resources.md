# Performance and Resource Issues

## Memory Usage Traps

### The Formula: max_file_size × threads

THOR reserves memory buffers for file scanning based on this formula:

```
RAM_reserved ≈ threads × max_file_size
```

This is the most common cause of unexpected memory exhaustion in lab environments.

### Why This Matters

**Lab mode auto-enables multi-threading** (one thread per CPU core). Combined with increased file size limits, memory can escalate quickly:

| Scenario | Threads | Max File Size | Reserved Buffers |
|----------|---------|---------------|------------------|
| Default single-thread | 1 | 30MB | ~30MB |
| Quick mode (4 cores) | 4 | 30MB | ~120MB |
| Lab mode (16 cores) | 16 | 200MB | **~3.2GB** |
| Lab mode (16 cores) | 16 | 2GB | **~32GB** |

### Baseline RAM Requirements

Beyond the file buffers, THOR itself requires:
- **Single thread**: ~300MB to ~500MB baseline
- **Multi-threaded**: ~800MB to ~1500MB baseline (depending on modules enabled)

Total memory = baseline + (threads × max_file_size)

### Symptoms of Memory Pressure

- THOR killed by OOM (Out of Memory) killer on Linux
- System becomes unresponsive during scan
- Swap thrashing (high disk I/O, slow progress)
- THOR crashes without clear error message
- `--minmem` threshold triggers early termination

### Reducing Memory Usage

**Priority order** (preserve detection capability):

1. **Reduce threads first** (if you have many cores)
   ```bash
   # Use only 4 threads instead of all cores
   --threads 4
   ```

2. **Reduce max_file_size** (impacts large file scanning)
   ```bash
   # Reduce from 200MB to 50MB
   --max_file_size 50000000
   ```

3. **Avoid combining high values**
   ```bash
   # BAD: 16 threads × 200MB = 3.2GB just for buffers
   --threads 0 --max_file_size 200000000

   # BETTER: 8 threads × 100MB = 800MB for buffers
   --threads 8 --max_file_size 100000000
   ```

### Key Insight

**Reduce max_file_size before reducing detection depth.**

Lowering `max_file_size` from 200MB to 50MB:
- Only affects scanning of files larger than 50MB
- Such large files are rarely malicious executables
- Most malware is under 10MB
- Preserves full detection on 99%+ of files

Reducing threads or disabling modules has broader impact on detection coverage.

### Lab Mode Considerations

In `--lab` mode, THOR auto-enables:
- Multi-threading (all cores)
- Intense mode (200MB max file size)
- Full registry scanning
- MFT analysis (additional memory)

For memory-constrained lab VMs, explicitly set limits:
```bash
thor64.exe --lab -p E:\ --threads 4 --max_file_size 50000000
```

### Monitoring Memory

```bash
# Linux: Watch memory during scan
watch -n 5 'free -h'

# Windows: Check available memory
wmic OS get FreePhysicalMemory
```

Set a safety threshold:
```bash
# Cancel if free memory drops below 500MB
--minmem 500
```

## Related

- See [performance.md](../../thor-scan/reference/performance.md) for threading and file size flag details
- See [stuck-scans.md](stuck-scans.md) for diagnosing frozen scans
