# Diagnostics

## thor-util diagnostics

The primary diagnostic tool for THOR issues.

### Basic Usage

```bash
# Collect diagnostics (works while THOR is running or after)
thor-util diagnostics

# Collect with debug re-run (monitors for interference)
thor-util diagnostics --run

# Custom output location
thor-util diagnostics --output /path/to/diagnostics.zip
```

### What It Collects

The diagnostics pack (`diagnostics.zip`) contains:

| File | Description |
|------|-------------|
| `parameters.json` | Full THOR configuration snapshot - all flags and their values at collection time |
| `progress.json` | Real-time scan state: current module, worker tasks with stack traces, CPU wait % |
| `cpu.pprof` | CPU profiling data (Go pprof format) - shows where THOR spent CPU time |
| `heap.pprof` | Heap/memory profiling - shows memory allocation by function |
| `goroutine.pprof` | Goroutine stack traces - shows what all threads are doing (deadlock detection) |
| `newestlog.txt` | Recent THOR log output at collection time |
| `processlist.json` | All running processes on the system |
| `thor.dmp` | Memory dump of the THOR process |
| `diagnostics.log` | Log of the diagnostics collection itself |

**Note:** The `.pprof` files are particularly useful for diagnosing slow scans or stuck processes. See [Analyzing pprof Files](#analyzing-pprof-files) below.

### When to Use Each Mode

| Situation | Command |
|-----------|---------|
| THOR currently stuck | `thor-util diagnostics` (from another terminal) |
| THOR finished but had issues | `thor-util diagnostics` |
| Need to reproduce issue | `thor-util diagnostics --run` |
| Suspect AV/EDR interference | `thor-util diagnostics --run` |

The `--run` flag re-executes the last scan command with debug logging and monitors for external process interference (AV/EDR signals).

## Analyzing pprof Files

The diagnostics pack includes Go pprof profiling files that provide deep insight into THOR's runtime behavior. These require Go to be installed (`go tool pprof`).

### Prerequisites

```bash
# Check if Go is installed
go version

# If not installed:
# macOS: brew install go
# Linux: apt install golang / yum install golang
# Windows: download from https://go.dev/dl/
```

### Quick Analysis (Command Line)

```bash
# Extract the diagnostics pack
unzip diagnostics.zip -d diagnostics-pack
cd diagnostics-pack

# CPU: Show top CPU consumers
go tool pprof -top cpu.pprof

# CPU: Show top by cumulative time (includes time in called functions)
go tool pprof -top -cum cpu.pprof

# Memory: Show top memory allocators
go tool pprof -top heap.pprof

# Goroutines: Show all goroutine stacks (find stuck/blocked threads)
go tool pprof -top goroutine.pprof
```

### Interactive Mode

```bash
# Start interactive session
go tool pprof cpu.pprof

# Inside pprof:
(pprof) top           # Top consumers
(pprof) top -cum      # Top by cumulative time
(pprof) list funcName # Show annotated source for a function
(pprof) web           # Generate SVG call graph (requires graphviz)
(pprof) png           # Generate PNG call graph
(pprof) quit
```

### Web UI with Flame Graph

The most visual way to analyze profiles:

```bash
# Start web UI on port 8080
go tool pprof -http=:8080 cpu.pprof

# Opens browser with:
# - Flame graph (best for finding hot paths)
# - Call graph
# - Top functions
# - Source view
```

### What Each Profile Reveals

**cpu.pprof - CPU Time Analysis**
- Which YARA rules are slow
- Which modules consume the most CPU
- Hot code paths during scanning

Common findings:
- Expensive regex in YARA rules
- Slow archive decompression
- Inefficient file matching patterns

**heap.pprof - Memory Analysis**
- What's consuming memory
- Memory leaks
- Large allocations

Common findings:
- Large files loaded into memory
- Many small allocations from string processing
- Signature compilation memory usage

**goroutine.pprof - Thread/Concurrency Analysis**
- What each worker thread is doing
- Blocked/waiting goroutines
- Potential deadlocks

Common findings:
- Workers stuck on I/O (network/disk)
- Lock contention
- Goroutines waiting on external resources

### Example: Finding a Slow YARA Rule

```bash
# 1. Check CPU profile for YARA-related functions
go tool pprof -top cpu.pprof | grep -i yara

# 2. Start web UI for detailed view
go tool pprof -http=:8080 cpu.pprof

# 3. In flame graph, look for tall stacks under:
#    - yara.* functions
#    - regexp.* functions (regex matching)
#    - compress.* functions (archive handling)
```

### Example: Finding Why THOR Is Stuck

```bash
# Check goroutine stacks
go tool pprof -top goroutine.pprof

# Look for goroutines in these states:
# - "IO wait" - stuck on disk/network
# - "select" - waiting for channel
# - "lock" - waiting for mutex

# View full stack traces
go tool pprof goroutine.pprof
(pprof) traces
```

### Sharing pprof Analysis

To share findings with support or colleagues:

```bash
# Generate a PDF report
go tool pprof -pdf cpu.pprof > cpu-analysis.pdf

# Generate SVG (vector, zoomable)
go tool pprof -svg cpu.pprof > cpu-analysis.svg

# Generate text report
go tool pprof -text cpu.pprof > cpu-analysis.txt
```

## Debug Mode

Run THOR with verbose debugging:

```bash
thor64.exe --debug -p C:\path
```

Produces detailed output including:
- Module start/stop times
- File processing details
- Rule matching information
- Resource usage

### Targeted Debug

Debug specific modules:

```bash
# Debug only Filescan module
thor64.exe --debug -a Filescan -p C:\path

# Debug with all output
thor64.exe --debug --printall -a Filescan -p C:\temp
```

## CTRL+C Interrupt Menu

During any scan, press **CTRL+C** to access the interrupt menu.

### What It Shows

1. **Currently scanned element** - the file/path/object THOR is processing
2. **Module** - which THOR module is active (Filescan, Registry, Eventlog, etc.)
3. **Progress** - overall scan completion percentage
4. **Continue/abort options** - choose to resume or terminate

### Interactive Options

```
Press 'c' to continue scanning
Press 'a' to abort (writes partial results)
Press 'd' to dump current state to log
```

### Diagnosis Workflow

1. Press CTRL+C once
2. Note the **current element** and **module**
3. Wait 30-60 seconds, press CTRL+C again
4. Compare: is the element the same?

**If same element**: THOR is stuck on that specific item (see solutions below)
**If different element**: THOR is progressing, just slowly (may be normal)
**If no response**: Process may be suspended by AV/EDR

### Common Stuck Elements and Solutions

| Stuck On | Likely Cause | Solution |
|----------|--------------|----------|
| Large archive file | Decompression timeout | `--noarchive` or `--max-recursion-depth 2` |
| Large log file | Line-by-line parsing | `--max_log_lines 500000` |
| Network path | Slow/unavailable share | Exclude path or use local storage |
| Single executable | Complex YARA matching | `--yara-timeout 180` |
| Process memory | Large process or suspended | `--noprocs` on live systems |

### When CTRL+C Doesn't Work

If pressing CTRL+C produces no output:

1. The process may be suspended by AV/EDR
2. Try `kill -SIGINT <pid>` on Linux (sends same signal)
3. Check if process is in "T" (traced/stopped) state: `ps aux | grep thor`
4. See [av-edr-interference.md](av-edr-interference.md) for recovery steps

## ThorDB Statistics

THOR maintains a SQLite database with scan statistics.

**Location:**
- Windows: `C:\ProgramData\thor\thor10.db`
- Linux: `/var/lib/thor/thor10.db` or `~/.thor/thor10.db`

**View with SQLiteBrowser:**
1. Download: https://sqlitebrowser.org/
2. Open `thor10.db`
3. Check `statistics` table for slow elements

**Key tables:**
- `scans`: Scan history
- `statistics`: Element processing times
- `findings`: Previous findings (for diff mode)

## Log Analysis

### Text Log Fields

Key fields to check in THOR logs:

```
MODULE: Which component generated the message
LEVEL: Info/Notice/Warning/Alert/Error
TARGET: File/element being processed
TIME: Processing duration
MESSAGE: Detailed information
```

### Common Error Patterns

| Pattern | Meaning | Action |
|---------|---------|--------|
| `ERROR: License` | License issue | Check `.lic` file |
| `ERROR: Signature` | Corrupt signatures | `thor-util update --force` |
| `WARN: Timeout` | YARA timeout | `--yara-timeout 180` |
| `WARN: Skipped` | File too large | `--max_file_size` increase |
| `ERROR: Permission` | Access denied | Run as admin/root |

## System Diagnostics

### Windows

```powershell
# Check THOR process
Get-Process thor64 | Select-Object *

# Check memory
Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 10

# Check disk space
Get-PSDrive -PSProvider FileSystem
```

### Linux

```bash
# Check THOR process
ps aux | grep thor

# Check memory
free -h
cat /proc/meminfo

# Check disk space
df -h

# Check I/O
iostat -x 1 5
```

### macOS

```bash
# Check THOR process
ps aux | grep thor

# Check memory
vm_stat

# Check disk
df -h
```

## Bottleneck Identification

### CPU Bottleneck

Symptoms:
- High CPU usage
- Scan progressing but slow

Solutions:
- `--threads` adjustment
- `--lowprio` / `--verylowprio`
- `--cpulimit` if sharing with production workload

### Memory Bottleneck

Symptoms:
- Swap usage high
- THOR killed by OOM
- System slowdown

Solutions:
- `--threads` reduction (memory scales with threads)
- `--max_file_size` reduction
- `--minmem` adjustment
- Close other applications

### Disk I/O Bottleneck

Symptoms:
- Low CPU but slow progress
- High disk wait times

Solutions:
- `--lowioprio`
- Scan from faster storage
- Avoid scanning network shares

### Network Bottleneck

Symptoms:
- Stuck on network paths
- Timeouts

Solutions:
- Exclude network shares
- Use `-p` for local paths only
- Check network connectivity

## Support Information

When contacting Nextron support, provide:

1. **diagnostics.zip** from `thor-util diagnostics`
2. THOR version: `thor64.exe --version`
3. Operating system and version
4. License type (lab, workstation, server)
5. Exact command that caused issues
6. Description of expected vs actual behavior

## Quick Troubleshooting Checklist

1. [ ] Is THOR running? (`ps` / `tasklist`)
2. [ ] Does CTRL+C respond?
3. [ ] What element is it processing?
4. [ ] Is AV/EDR excluded?
5. [ ] Are there disk/memory/CPU constraints?
6. [ ] Is the license valid?
7. [ ] Are signatures up to date?
8. [ ] Did `thor-util diagnostics` reveal anything?
