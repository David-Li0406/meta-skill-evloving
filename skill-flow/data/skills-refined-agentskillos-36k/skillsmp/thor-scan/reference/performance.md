# Performance and Threading

## Threading (`--threads`)

THOR uses a single thread by default. Multi-threading is automatic in `--lab`, `--dropzone`, and `--thunderstorm` modes.

```bash
# Use all cores
--threads 0

# Use all cores except 2
--threads -2

# Use exactly 4 threads
--threads 4
```

Modules supporting threading: Filescan, RegistryChecks, Eventlog, Thunderstorm, Dropzone.

**Memory warning**: `--max_file_size` reserves a buffer PER THREAD. With 8 threads and 30MB max_file_size, expect ~240MB just for file buffers. See [performance-and-resources.md](../../thor-troubleshooting/reference/performance-and-resources.md) for detailed memory calculations and troubleshooting.

## CPU Limiting (`--cpulimit`)

Pauses THOR when **system-wide** CPU exceeds threshold. Does not throttle THOR's own usage.

```bash
# Pause when system CPU exceeds 70%
--cpulimit 70

# Disable CPU limit checking
--nocpulimit
```

Default: 95%. Minimum: 15%.

Common misconception: `--cpulimit 50` does NOT make THOR use only 50% CPU. It pauses THOR when the total system load (from all processes) exceeds 50%.

## File Size Limits

| Setting | Default | Intense Mode |
|---------|---------|--------------|
| `max_file_size` | 12MB (config) / 30MB (flag) | 200MB |
| `max_file_size_intense` | 30MB | 200MB |

Configure in `./config/thor.yml`:
```yaml
max_file_size: 12000000
max_file_size_intense: 30000000
```

**Features obeying limit**: YARA matching, hash calculation, STIX IOCs, Archive scan.

**Features ignoring limit**: LogScan, RegistryHive, EVTX, DeepDive, Filename IOCs, YARA meta rules.

## Process Priority

```bash
--lowprio       # Low process priority
--verylowprio   # Very low priority
--lowioprio     # Low disk I/O priority
--nolowprio     # Don't auto-reduce priority
```

Soft mode auto-sets low priority.

## Memory Management

```bash
# Cancel if free memory drops below 50MB
--minmem 50

# Ignore resource availability warnings (lab only)
--norescontrol
```

## Log Line Limits

```bash
# Skip remaining lines in logs exceeding limit
--max_log_lines 1000000
```

Default: 1,000,000 lines per log file.

## Runtime Limits

```bash
# Max scan duration (default: 168 hours / 7 days)
--max_runtime 72
```

## YARA Tuning

```bash
# YARA stack slots (default: 32768)
--yara-stack-size 65536

# YARA timeout per file (default: 90 seconds)
--yara-timeout 120
```

Increase stack size for complex rules. Increase timeout for large files.

## Quick Performance Wins

1. **Quick mode** (`--quick`): 80% coverage in 20% time
2. **Lookback** (`--lookback 7`): Only scan last 7 days
3. **Single module** (`-a Filescan`): Run only one module
4. **Path restriction** (`-p /suspicious/folder`): Narrow scope
5. **Disable unused features**: `--nosigma`, `--noc2`, `--noarchive`

## Risky Performance Flags

Avoid unless intentional:

| Flag | Risk |
|------|------|
| `--intense` | Long runtime, stability issues |
| `--c2-in-memory` | Many false positives on workstations |
| `--alldrives` | Includes network drives, very long runtime |
| `--mft` | High memory usage |
| `--dump-procs` | High disk space usage |
| `--full-registry` | Longer runtime, usually low value |

## Bottleneck Detection

Check `thor10.db` (Windows: `C:\ProgramData\thor\thor10.db`) with SQLiteBrowser to see statistics on slow elements.

Use CTRL+C during scan to access interrupt menu and check current element.
