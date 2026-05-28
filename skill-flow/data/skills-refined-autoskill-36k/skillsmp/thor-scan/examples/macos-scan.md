# macOS Scan Examples

## Prerequisites

1. Grant Full Disk Access (FDA) to Terminal or THOR binary:
   System Settings > Privacy & Security > Full Disk Access

2. Run as root:
   ```bash
   sudo ./thor-macosx [options]
   ```

## Basic Scan

```bash
sudo ./thor-macosx -e /Users/admin/thor-reports
```

## Quick Triage

```bash
sudo ./thor-macosx --quick -e /Users/admin/thor-reports
```

## Scan Specific User Directory

```bash
sudo ./thor-macosx -p /Users/suspicious_user -e /Users/admin/thor-reports
```

## Scan Applications Folder

```bash
sudo ./thor-macosx -p /Applications -e /Users/admin/thor-reports
```

## Scan with JSON Output

```bash
sudo ./thor-macosx --jsonfile report.json -e /Users/admin/thor-reports
```

## Conservative Scan (Production Mac)

```bash
sudo ./thor-macosx --soft --lowprio -e /Users/admin/thor-reports
```

## Recent Activity Only

```bash
sudo ./thor-macosx --lookback 7 --global-lookback -e /Users/admin/thor-reports
```

## Lab Mode: Mounted macOS Image

```bash
sudo ./thor-macosx --lab \
  -p /Volumes/MacImage \
  --virtual-map /Volumes/MacImage:/ \
  -j MACHOST \
  -e /cases/reports
```

## Lab Mode: Mounted Windows Image on Mac

```bash
sudo ./thor-macosx --lab \
  -p /Volumes/WindowsImage \
  --virtual-map /Volumes/WindowsImage:C \
  -j WINHOST \
  -e /cases/reports
```

## Debug Mode

```bash
sudo ./thor-macosx --debug -a Filescan -p /tmp --printall
```

## Notes

- macOS binary is 64-bit only (`thor-macosx`)
- Requires macOS 10.14 (Mojave) or later
- ARM M1/M2 Macs supported via Rosetta 2 or native binary
- Some system folders protected even with FDA; this is normal
