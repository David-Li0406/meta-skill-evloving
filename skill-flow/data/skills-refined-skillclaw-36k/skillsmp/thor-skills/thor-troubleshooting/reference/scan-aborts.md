# Why THOR Scans Stop Early

Quick mental model for diagnosing scan aborts:

| Symptom | Likely Cause |
|---------|--------------|
| Clear message near end of log | THOR protecting system (Rescontrol) or configured timeout |
| THOR disappears, no final message | External: user killed it, AV/EDR killed/suspended it, OS terminated it |

## Resource Control (Rescontrol) - Most Common

Rescontrol is THOR's stability guard to avoid wrecking system stability during live scans.

### Triggers

- **Low RAM**: Free physical memory drops below threshold (default ~50 MB)
- **Disk full**: Stops before system runs out of disk space
- **CPU constrained**: 1 vCPU VMs can lead to extreme throttling (slow, not always abort)

### How to Spot It

Ask for the last ~50 lines of the THOR log. Look for:

```
Error: MODULE: Rescontrol ... Available physical memory dropped below 50 MB,
stopping THOR scan in order to avoid a memory outage
(use --minmem 0 to disable this protection)
```

Followed by top RAM consumers:
```
Process with high memory usage: svchost.exe ... MEMORY_USAGE: 28.29%
Process with high memory usage: thor64.exe ... MEMORY_USAGE: 13.23%
Process with high memory usage: MsMpEng.exe ... MEMORY_USAGE: 5.46%
```

THOR may also write `heap.pprof` for deeper debugging.

### Rescontrol Flags

| Flag | Purpose |
|------|---------|
| `--minmem 0` | Disable low-memory protection (use with caution) |
| `--minmem 100` | Set threshold to 100 MB free |
| `--norescontrol` | Disable all resource control (dangerous on live systems) |

## User Termination

Common on workstations/notebooks when THOR runs without CPU limiting.

### Symptoms

- THOR just vanishes
- No final "stopping scan" message in log
- Often preceded by user complaints about fans/lag

### Mitigation

```bash
# Use CPU limiting
./thor-macosx --cpulimit 50 -p /path

# Or lower priority
./thor-macosx --lowprio -p /path
./thor-macosx --verylowprio -p /path
```

Also: run during off-hours, communicate expectations to users.

## AV/EDR Interference

Often triggered by:
- **ProcessCheck module**: Accessing processes, handles, memory queries
- **Mutex checks**: Checking for suspicious mutex names looks "malware-ish" to some EDRs

### Symptoms

- Scan stops without THOR's own stop reason
- Scan appears "frozen" or stalled
- Process in "T" (traced/stopped) state on Linux: `ps aux | grep thor`

### Mitigation

1. Add exclusions for THOR directory
2. Temporarily relax specific protections during scan window
3. If reproducible, collect diagnostics in parallel:
   ```bash
   # From another terminal while THOR is running/stuck
   thor-util diagnostics
   ```

See [av-edr-interference.md](av-edr-interference.md) for detailed patterns.

## Timeouts

### THOR Built-in Timeouts

| Mode | Default Timeout | Notes |
|------|-----------------|-------|
| Live scan | ~72 hours | Automatic stop after this duration |
| Lab scan | Effectively disabled | Multi-day forensic scans are normal |

Check with `--max-runtime` flag to adjust:
```bash
# Extend to 168 hours (1 week)
./thor-macosx --max-runtime 168 -p /path
```

### ASGARD Timeout

If THOR is launched via ASGARD, an additional ASGARD-side timeout can terminate THOR even if THOR itself would continue. Check ASGARD job configuration.

### YARA Timeout

Individual files can timeout during YARA matching:
```bash
# Increase YARA timeout per file (default 90s)
./thor-macosx --yara-timeout 180 -p /path
```

## Quick Triage Checklist

1. **Check last ~50 log lines** for Rescontrol or timeout hints
   ```bash
   tail -50 hostname_thor_*.txt
   ```

2. **If no stop reason printed** → suspect external termination (user/AV/EDR)

3. **If Rescontrol**, verify:
   - Free RAM situation (check listed top memory consumers)
   - Disk free space: `df -h`
   - Extreme settings (high thread count, large max_file_size)

4. **If AV/EDR suspected**:
   - Add exclusions and retry
   - If reproducible, collect diagnostics in parallel

## Log Snippets to Look For

### Rescontrol - Low Memory
```
Error: MODULE: Rescontrol MESSAGE: Available physical memory dropped below 50 MB,
stopping THOR scan in order to avoid a memory outage
(use --minmem 0 to disable this protection)
```

### Rescontrol - Disk Full
```
Error: MODULE: Rescontrol MESSAGE: Available disk space dropped below threshold,
stopping THOR scan
```

### Timeout Reached
```
Info: MODULE: Startup MESSAGE: Maximum runtime of 72 hours reached, stopping scan
```

### Clean Shutdown (User Interrupt)
```
Info: MODULE: Shutdown MESSAGE: Scan aborted by user (SIGINT received)
```

### No Message (External Kill)
- Log ends abruptly mid-scan
- No "Shutdown" or "Rescontrol" message
- Possible causes: `kill -9`, AV/EDR termination, OOM killer

## Related

- [Diagnostics](diagnostics.md) - Collecting debug information
- [AV/EDR Interference](av-edr-interference.md) - Detailed interference patterns
- [Performance and Resources](performance-and-resources.md) - Tuning for constrained environments
