# Common Pitfalls

## Fast "Empty" Scans on Network/USB Mounts

### Symptom

A scan against a mounted path (network folder, USB stick, mounted network drive) finishes unusually fast and produces almost no findings.

```bash
# This scan finishes in seconds with minimal output
./thor64 -a FileScan -p /mnt/mounted1
```

### Cause

THOR skips file systems that are not recognized as "local hard drives" by default. Depending on OS and mount type, network shares, USB drives, and other mounted volumes may be effectively ignored.

This is a safety feature to prevent accidental scanning of network resources during live endpoint scans, but it trips up forensic analysts scanning mounted evidence.

### Fix

Use `--alldrives` to include non-hard-drive file systems:

```bash
# Include network/USB/mounted drives
./thor64 -a FileScan --alldrives -p /mnt/mounted1
```

### Full Lab Command Example

```bash
# Mounted network share with evidence
./thor-linux-64 --lab --alldrives -p /mnt/evidence_share --virtual-map /mnt/evidence_share:C -j YOURHOSTNAME -e /reports
```

### Performance Considerations

When scanning remote shares:
- **Network I/O is slow** - Expect significantly longer scan times
- **Recommend copying evidence locally** when possible
- If you must scan over network, consider `--quick` mode to reduce I/O
- Watch for timeouts on slow connections

### Quick Checklist

If your scan finishes too fast:

1. Check the scan output - does it report the expected number of files?
2. Is the target path a mounted/network/USB drive?
3. Try adding `--alldrives`
4. Verify the mount is actually accessible: `ls -la /mnt/target`

## Other Common Pitfalls

### Scanning the Wrong Path

THOR's `-p` flag accepts multiple paths, but typos are easy:

```bash
# Typo: scanning current directory instead of /mnt/image1
./thor64 --lab -p /mnt/image1/  # Note trailing slash may cause issues on some systems

# Better: explicit path without trailing slash
./thor64 --lab -p /mnt/image1
```

### Missing Virtual Mapping

Without `--virtual-map`, findings report the forensic workstation's mount path rather than the original system path. This makes correlation difficult.

```bash
# BAD: Findings show /mnt/case123/Windows/System32/...
./thor64 --lab -p /mnt/case123

# GOOD: Findings show C:\Windows\System32\...
./thor64 --lab -p /mnt/case123 --virtual-map /mnt/case123:C
```

### Scanning Without Lab License on Mounted Images

Standard licenses don't include lab mode features. Running without `--lab`:

```bash
# This works but lacks key features
./thor64 -a Filescan --intense -p /mnt/image
```

Missing capabilities:
- No virtual mapping
- No cross-platform IOCs (won't detect Windows malware patterns on Linux)
- Single-threaded
- No hostname override

## Related

- See [lab-mode.md](../../thor-scan/reference/lab-mode.md) for complete lab scanning guidance
- See [stuck-scans.md](stuck-scans.md) for scans that hang rather than finish fast
