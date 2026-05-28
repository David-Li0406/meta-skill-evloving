# Lab Mode

Lab mode (`--lab`) is designed for forensic analysis of mounted disk images and memory dumps. **Requires a Forensic Lab License.**

## License Requirement

Before using `--lab`, verify you have a Forensic Lab license:

```bash
# Check license file for "forensiclab" string
grep -i forensiclab *.lic
```

If the license contains "forensiclab", you can use `--lab`. Otherwise, use the [alternative flag combination](#without-a-lab-license) below.

**THOR Lite users:** The `--lab` flag is not available. Use the alternative flags.

## What `--lab` Enables Automatically

- **Intense mode** (every file scanned, 200MB limit) - do NOT add `--intense`, it's redundant
- Multi-threading (all CPU cores)
- No resource control (`--norescontrol`)
- No double-check for other THOR instances (`--nodoublecheck`)
- No ThorDB
- Cross-platform IOC application
- Sigma minimum level: Medium

**Important:** Never combine `--lab --intense` - the `--lab` flag already includes intense mode. Adding `--intense` is redundant.

## Key Lab Mode Flags

### Virtual Drive Mapping (`--virtual-map`)

Maps mounted image paths to original paths for accurate reporting.

```bash
# Windows: F: drive was originally C:
--virtual-map F:C

# Linux: mount point to original root
--virtual-map /mnt/image1:/

# Windows image mounted on Linux
--virtual-map /mnt/image1:C
```

### Hostname Override (`-j`)

Replace forensic workstation hostname with original system name in logs.

```bash
-j YOURHOST
```

### Output Directory (`-e`)

Write all outputs (HTML, TXT, CSV, JSON) to specified folder.

```bash
-e /path/to/reports
```

## Standard Lab Command Templates

### Mounted Windows Image (on Windows)
```bash
thor64.exe --lab -p S:\ --virtual-map S:C -j YOURHOSTNAME -e C:\reports
```

### Mounted Windows Image (on Linux)
```bash
./thor-linux-64 --lab -p /mnt/image --virtual-map /mnt/image:C -j YOURHOSTNAME -e /reports
```

**Note**: If the scan finishes too fast with minimal output, the mount may not be recognized as a local drive. Add `--alldrives` to include network/USB/mounted drives. See [common-pitfalls.md](../../thor-troubleshooting/reference/common-pitfalls.md) for details.

### Mounted Linux Image (on Linux)
```bash
./thor-linux-64 --lab -p /mnt/image --virtual-map /mnt/image:/ -j YOURHOSTNAME -e /reports
```

## Memory Dump Scanning

### Direct Memory Image Analysis
```bash
./thor-linux-64 --lab --image_file /path/to/memory.dmp -j YOURHOSTNAME -e /reports
```

DeepDive processes overlapping 3MB chunks and reports byte offsets.

### Extracted Process Dumps (from Volatility)
```bash
# First extract with Volatility:
# vol.py -f image.mem --profile=Profile memdump -D procs/

# Then scan extracted dumps:
./thor-linux-64 --lab -p /path/to/extracted/procs/ -j YOURHOSTNAME -e /reports
```

### Restore PE Files (`-r`)
```bash
./thor-linux-64 --lab --image_file memory.dmp -r /restored_files/ -e /reports
```

Restores PE files matching YARA rules to the specified directory.

## Without a Lab License

If you don't have a Forensic Lab license (or are using THOR Lite), use this flag combination for lab-like behavior:

```bash
# Windows (full THOR)
thor64.exe -a Filescan --intense --norescontrol --cross-platform -p <path>

# Windows (THOR Lite)
thor64-lite.exe -a Filescan --intense --norescontrol --cross-platform -p <path>

# Linux (full THOR)
./thor-linux-64 -a Filescan --intense --norescontrol --cross-platform -p <path>

# Linux (THOR Lite)
./thor-lite-linux-64 -a Filescan --intense --norescontrol --cross-platform -p <path>

# macOS (full THOR)
./thor-macosx -a Filescan --intense --norescontrol --cross-platform -p <path>

# macOS (THOR Lite)
./thor-lite-macos -a Filescan --intense --norescontrol --cross-platform -p <path>
```

**Flags explained:**

- `-a Filescan` – Run only the Filescan module (most comprehensive for file analysis)
- `--intense` – Maximum thoroughness, all files scanned regardless of extension
- `--norescontrol` – Disable CPU/memory throttling
- `--cross-platform` – Apply signatures from all platforms (Windows IOCs on Linux, etc.)

**What this alternative lacks compared to real `--lab`:**

- `--virtual-map` support (path remapping for forensic reports)
- `-j` hostname override
- Automatic multi-threading optimization
- Some lab-specific module behaviors

**Note:** This provides **similar behavior, not equal** to full lab mode. For complete forensic lab capabilities, a Forensic Lab license is required.

## Related Lab Features

### Drop Zone Mode (`--dropzone`)
Monitor a folder for new files and auto-scan them.
```bash
thor64.exe --dropzone -p /watch/folder
```
Options: `--dropdelete` (remove after scan), `--dropzone-delay <seconds>`.

### Artifact Collector (`--collector`)
Collect system artifacts into ZIP (requires "THOR Deep Forensics" license).
```bash
thor64.exe --lab --collector -p S:\ --collector-output /artifacts/
```

## Running Multiple Lab Scans

On a multi-core forensic workstation running multiple parallel scans:
- Use `--threads 4` per scan on a 16-core system with 4 parallel scans
- Memory scales with threads × max_file_size
