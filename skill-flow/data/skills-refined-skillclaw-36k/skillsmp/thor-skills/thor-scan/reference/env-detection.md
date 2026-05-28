# Environment Detection

Before running THOR, verify the environment.

## Binary Names by Platform

### Full THOR

| Platform | 64-bit Binary | 32-bit Binary |
|----------|---------------|---------------|
| Windows | `thor64.exe` | `thor.exe` |
| Linux | `thor-linux-64` | `thor-linux` |
| macOS | `thor-macosx` | N/A |

Always prefer 64-bit binaries. 32-bit versions have lower memory visibility and different registry/folder views on 64-bit systems.

### THOR Lite (Free Version)

| Platform | Scanner Binary | Utility Binary |
|----------|----------------|----------------|
| Windows | `thor64-lite.exe` | `thor-lite-util.exe` |
| Linux | `thor-lite-linux-64` | `thor-lite-util` |
| macOS | `thor-lite-macos` | `thor-lite-util` |

THOR Lite is a free scanner with reduced features. See [THOR Lite Limitations](../../thor-lite/reference/limitations.md) for details on what's available.

**How to identify THOR Lite:**
- Binary name contains "lite"
- Startup banner shows "Lite" in version header
- Log output includes: "Some modules and features are not available in Lite version and will be disabled"
- Disabled components listed with reasons like "Component is not available in THOR Lite" or "License restrictions"

## Minimum OS Versions

- **Windows**: 7 x86/x64, Server 2008 R2+
- **Linux**: RHEL/CentOS 6, SUSE SLES 11, Ubuntu 16 LTS, Debian 9
- **macOS**: 10.14 (Mojave), 11 (Intel and ARM M1)
- **Legacy** (requires special license): Windows XP SP3, Server 2003 SP2+

## Required Privileges

- **Windows**: LOCAL_SYSTEM or Administrator
- **Linux/macOS**: root

Use `--require-admin` to exit immediately if not running with sufficient privileges.

## License Files

THOR requires a valid `.lic` file. Locations checked (in order):
1. THOR program folder
2. Subfolders of THOR program folder
3. Path specified via `--licensepath <path>`
4. Environment variable `THOR_LICENSE` (base64-encoded content)

License types:
- **THOR Workstation** – Windows workstations, macOS only
- **THOR Server & Workstation** – All systems
- **THOR Forensic Lab** – Lab mode features (mounted images, memory dumps, multi-threading)
- **THOR Incident Response**
- **THOR Thunderstorm**

## macOS Full Disk Access

macOS requires Full Disk Access (FDA) to scan Mail, Messages, and admin settings. Grant via System Settings > Privacy & Security > Full Disk Access, or THOR will prompt on first run.

## Companion Binary: thor-util

Check for `thor-util` (or `thor-util.exe` on Windows) in the THOR folder. It handles:
- Signature updates (`thor-util update`)
- Program upgrades (`thor-util upgrade`)
- Diagnostics (`thor-util diagnostics`)
- Report generation (`thor-util report`)

## AV/EDR Exclusions

Exclude THOR from AV/EDR scanning to prevent interference:
```powershell
# Windows Defender example
Add-MpPreference -ExclusionProcess 'C:\path\to\thor64.exe'
```

Known issues:
- **SentinelOne**: Process memory pollution causes false positives
- **McAfee**: Complex exclusion requirements (see ASGARD manual)
