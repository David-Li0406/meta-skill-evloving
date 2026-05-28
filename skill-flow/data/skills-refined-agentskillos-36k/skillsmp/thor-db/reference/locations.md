# ThorDB Locations

## Default Paths

### Windows

| Context | Path |
|---------|------|
| Admin/SYSTEM | `C:\ProgramData\thor\thor10.db` |
| User | `%LOCALAPPDATA%\thor\thor10.db` |

### Linux

| Context | Path |
|---------|------|
| Root | `/var/lib/thor/thor10.db` |
| User | `~/.local/state/thor/thor10.db` |

### macOS

| Context | Path |
|---------|------|
| Root | `/var/lib/thor/thor10.db` |
| User | `~/Library/Application Support/thor/thor10.db` |

## THOR 11

Replace `thor10.db` with `thor11.db` for THOR v11.

## Finding the Database

### Quick Check

```bash
# Windows
dir C:\ProgramData\thor\thor*.db
dir %LOCALAPPDATA%\thor\thor*.db

# Linux/macOS
ls -la /var/lib/thor/thor*.db
ls -la ~/.local/state/thor/thor*.db
```

### From Binary Strings

```bash
strings ./thor-linux-64 | grep -E 'thor[0-9]+\.db'
```

### Via Strace (Linux)

```bash
strace -f -e openat ./thor-linux-64 --quick -p /tmp 2>&1 | grep -E 'thor[0-9]+\.db'
```

### Via dtruss (macOS)

```bash
sudo dtruss -f ./thor-macosx --quick -p /tmp 2>&1 | grep -E 'thor[0-9]+\.db'
```

### Via Process Monitor (Windows)

Use Sysinternals Process Monitor, filter by:
- Process Name: `thor64.exe`
- Path contains: `thor`
- Operation: `CreateFile`

## Disabling ThorDB

```bash
thor64.exe --exclude-component ThorDB -p C:\
```

Or legacy flag:
```bash
thor64.exe --nothordb -p C:\
```

When disabled:
- No timing telemetry collected
- `--resume` and `--diff` modes unavailable
- Slightly faster scan startup

## Database Size

Typical sizes:
- Fresh install: < 1 MB
- After several scans: 5-50 MB
- Heavy use with many resumes: 50-200 MB

If database grows excessively, it can be safely deleted. THOR will recreate it on next scan.
