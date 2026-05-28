# AV/EDR Interference

**This is the #1 cause of THOR scan issues.** Over 98% of "frozen" or "stuck" scans are caused by AV/EDR products suspending or interfering with THOR.

## Symptoms

- Scan appears frozen but THOR process exists
- CTRL+C shows same element repeatedly
- CPU usage drops to near-zero
- Scan progress stops at seemingly random points
- "Frozen at 98%" pattern (AV scanning THOR's output files)
- Scan runs 3-10x slower than expected (AV scanning every file THOR reads)

## How Interference Happens

1. **Real-time scanning**: AV scans every file THOR reads
2. **Behavioral analysis**: EDR suspends "suspicious" process behavior
3. **Memory scanning**: AV scans THOR's process memory (contains signatures)
4. **Output file scanning**: AV scans THOR's log/report files as they're written

## Detection

### Using thor-util diagnostics

```bash
# While THOR is running (preferred)
thor-util diagnostics

# After scan, re-run with monitoring
thor-util diagnostics --run
```

The `--run` flag monitors for external process interference during a debug scan.

### Manual Detection (Windows)

```powershell
# Check if THOR is suspended
Get-Process thor64 | Select-Object Name, Responding

# Check for high handle count (AV hooking)
Get-Process thor64 | Select-Object Name, HandleCount
```

### Manual Detection (Linux)

```bash
# Check process state (T = stopped/traced)
ps aux | grep thor

# Check for ptrace attachments
cat /proc/$(pgrep thor)/status | grep TracerPid
```

## Solutions by Product

### Windows Defender

```powershell
# Add process exclusion
Add-MpPreference -ExclusionProcess 'C:\path\to\thor64.exe'
Add-MpPreference -ExclusionProcess 'C:\path\to\thor-util.exe'

# Add folder exclusion
Add-MpPreference -ExclusionPath 'C:\path\to\thor\'

# Verify exclusions
Get-MpPreference | Select-Object -ExpandProperty ExclusionProcess
```

### CrowdStrike Falcon

1. Falcon Console → Configuration → Prevention Policies
2. Add THOR folder to exclusions
3. Consider adding hash-based exclusions for THOR binaries

### SentinelOne

**Known issue**: SentinelOne pollutes process memory, causing false positives in THOR's process memory scanning.

**Workaround**:
```bash
# Skip process memory scanning
thor64.exe --noprocs -p C:\
```

Or add process exclusion in SentinelOne Management Console.

### Carbon Black

1. CB Defense → Policies → Sensor Settings
2. Add path exclusions for THOR directory
3. Add process exclusions for thor64.exe

### McAfee ENS

McAfee has complex exclusion requirements:

1. Threat Prevention → On-Access Scan → Exclusions
2. Add THOR installation path
3. Add THOR output directory
4. May need to exclude by process name AND path

See ASGARD manual for detailed McAfee configuration.

### Symantec/Broadcom Endpoint Protection

1. Clients → Policies → Exceptions
2. Add folder exception for THOR directory
3. Add application exception for THOR binaries

### Sophos

1. Sophos Central → Endpoint Protection → Policies
2. Add Scanning Exclusions for THOR folder
3. Add Application Control exception if needed

### Microsoft Defender for Endpoint (MDE)

```powershell
# Local exclusion
Add-MpPreference -ExclusionProcess 'C:\path\to\thor64.exe'

# Organization-wide: Configure via Intune or Group Policy
# Defender ATP → Settings → Advanced features → Exclusions
```

## Generic Exclusion Checklist

For any AV/EDR product, exclude:

1. **THOR installation directory** (all files)
2. **THOR output directory** (logs, reports)
3. **THOR process names**: `thor64.exe`, `thor.exe`, `thor-linux-64`, `thor-macosx`, `thor-util.exe`
4. **THOR working directory** (temp files)

## Testing Exclusions

After adding exclusions, verify they work:

```bash
# Quick test scan
thor64.exe --quick -a Filescan -p C:\Windows\Temp -e C:\thor-test
```

If this completes without hanging, exclusions are likely working.

## Performance Impact

AV/EDR can cause massive performance degradation even when scans don't freeze:

| Scenario | Typical Duration | With AV Interference |
|----------|------------------|----------------------|
| Quick scan | 10-20 min | 1-2 hours |
| Default scan | 1-3 hours | 6-24 hours |
| Intense scan | 4-8 hours | 24+ hours |

**Why this happens**: Real-time AV scans every file THOR opens. Since THOR may read thousands of files per minute, the AV overhead multiplies dramatically.

**Measurement approach**:
1. Run a quick scan with AV enabled, note duration
2. Add exclusions
3. Re-run same scan, compare times
4. A 3-10x improvement confirms AV was the bottleneck

## When Exclusions Aren't Possible

If you cannot add exclusions (policy restrictions):

```bash
# Skip memory-intensive operations
thor64.exe --noprocs --nomutex --nopipes -p C:\

# Use soft mode (less aggressive)
thor64.exe --soft -p C:\

# Scan during AV maintenance window
# (if AV has scheduled scan times with reduced real-time protection)
```

## Escalation

If issues persist after exclusions:

1. Collect `thor-util diagnostics` output
2. Note exact AV/EDR product and version
3. Document exclusions applied
4. Contact Nextron support with this information
