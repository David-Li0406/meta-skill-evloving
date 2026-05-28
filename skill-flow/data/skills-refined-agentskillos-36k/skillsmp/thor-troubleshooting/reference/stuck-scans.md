# Stuck Scans

## Quick Diagnosis

### Step 1: Check if THOR is Actually Running

```bash
# Windows
tasklist | findstr thor

# Linux/macOS
ps aux | grep thor
```

If no process: THOR exited. Check logs for errors.
If process exists: Continue to Step 2.

### Step 2: Use CTRL+C Interrupt Menu

Press **CTRL+C** during a running scan to access the interrupt menu:
1. Shows currently scanned element
2. Option to continue or abort

**What to look for:**
- Same element for extended time → likely stuck on that file/path
- Element changing but slow → resource constraints or large files
- No response to CTRL+C → process may be suspended by AV/EDR

### Step 3: Check Current Element

If stuck on a specific element:

| Element Type | Common Cause | Solution |
|--------------|--------------|----------|
| Large file | File exceeds timeout | `--yara-timeout 180` or `--max_file_size` |
| Archive | Deeply nested or large | `--noarchive` or `--max-recursion-depth 2` |
| Log file | Very large log | `--max_log_lines 500000` |
| Network path | Slow/unavailable share | Use `-p` to exclude, or `--nonetwork` |
| Mounted image | Slow disk I/O | Check mount, use faster storage |

## Common Stuck Patterns

### "Frozen at 98%"

Almost always AV/EDR interference. See [av-edr-interference.md](av-edr-interference.md).

### Stuck on Archive

```bash
# Skip archive scanning entirely
thor64.exe --noarchive -p C:\

# Limit archive recursion
thor64.exe --max-recursion-depth 2 --max-nested-objects 5000 -p C:\
```

### Stuck on Large Log File

```bash
# Limit log lines processed
thor64.exe --max_log_lines 500000 -p C:\
```

### Stuck on Memory Analysis

```bash
# Increase YARA timeout for memory scans
thor64.exe --yara-timeout 180 --image_file memory.dmp

# Skip process memory scanning on live systems
thor64.exe --noprocs -p C:\
```

### Stuck Initializing

If stuck during initialization (before scan starts):

1. Check license validity: valid `.lic` file present?
2. Check signature loading: corrupted signatures?
3. Check disk space: enough space for temp files?

```bash
# Test with minimal signatures
thor64.exe --init-selector TEST_NONEXISTENT -p C:\temp
```

### Slow Due to Deep Scan Selector Overload

**Symptom**: Scan runs but takes much longer than expected on similar systems.

**Cause**: Custom `--de` (extension) or `--dm` (magic header) flags adding too many files to deep scan.

**Diagnosis**:
```bash
# Check what deep scan selectors are active
thor64.exe --print-deepscan-selectors

# Check if you passed custom selectors
grep -E '\-\-de|\-\-dm' your_command_line
```

**How deep scan works**: THOR reads file magic headers (not extensions) to determine which files get full YARA scanning. Adding broad selectors like `.txt` or `.log` can increase scan time dramatically.

**Solutions**:
```bash
# Remove custom selectors if not needed
# Use --intense only when necessary (scans ALL files regardless of magic)
# Review ThorDB timing data for deep_scan category
```

## Windows-Specific Issues

### Quick Edit Mode

**Symptom**: Scan stops when you click in the cmd window.

**Cause**: Windows Quick Edit mode pauses console processes on click.

**Solution**: Press Enter to resume, or disable Quick Edit:
- Right-click title bar → Properties → uncheck Quick Edit Mode

### High System Load Pausing THOR

**Symptom**: THOR pauses intermittently.

**Cause**: `--cpulimit` triggered by system-wide CPU load.

**Solution**:
```bash
# Disable CPU limit
thor64.exe --nocpulimit -p C:\

# Or raise the threshold
thor64.exe --cpulimit 99 -p C:\
```

### Low Memory Abort

**Symptom**: THOR exits with memory warning.

**Cause**: Free memory dropped below `--minmem` threshold.

**Solution**:
```bash
# Lower the threshold (risky)
thor64.exe --minmem 30 -p C:\

# Or close other applications
```

## Linux/macOS-Specific Issues

### Permission Denied Loops

**Symptom**: Slow progress with many permission errors.

**Cause**: Running as non-root, or filesystem permissions.

**Solution**: Run as root, or exclude inaccessible paths:
```bash
sudo ./thor-linux-64 -p /
```

### NFS/CIFS Mount Hangs

**Symptom**: Stuck when scanning mounted network shares.

**Cause**: Slow or unresponsive network filesystem.

**Solution**: Exclude network mounts or scan local only:
```bash
./thor-linux-64 -p /home -p /var  # explicit local paths
```

## Gathering Evidence

### Before Killing THOR

1. Note the CTRL+C output (current element)
2. Run `thor-util diagnostics` in another terminal
3. Check system resource usage (CPU, RAM, disk I/O)
4. Save the partial log file

### Diagnostic Data to Collect

```bash
# While THOR is stuck
thor-util diagnostics

# After killing THOR
thor-util diagnostics --run
```

The `--run` flag re-runs with debug logging and monitors for interference.

## Recovery Steps

### Resume Interrupted Scan

```bash
# If ThorDB was enabled (default)
thor64.exe --resume -p C:\
```

Note: Resume restores previous parameters in v11. In v10, you must re-specify flags.

### Start Fresh

```bash
# Clear ThorDB and start over
thor64.exe --nothordb -p C:\
```
