# thor-util Update vs Upgrade vs Download

thor-util has three distinct commands for getting new content. Understanding the difference is critical.

## Command Comparison

| Command | Gets Program Files | Gets Signatures | Preserves Config |
|---------|-------------------|-----------------|------------------|
| `update` | No | Yes | Yes |
| `upgrade` | Yes | Yes | Yes |
| `download` | Yes | Yes | No |

## update

**Purpose**: Get new signatures only. Program files unchanged.

```bash
thor-util update
```

**What it does:**
- Downloads latest signature pack
- Updates YARA, Sigma, IOC, STIX files
- Does NOT modify THOR binaries
- Does NOT modify config files

**Use when:**
- Regular signature updates (daily/weekly)
- You don't want to risk program changes
- Troubleshooting signature-specific issues

### Signature Variants

```bash
# Stable signatures (default, tested)
thor-util update

# SigDev signatures (newest, untested)
thor-util update --sigdev

# Force stable (reset from sigdev)
thor-util update --force
```

**Warning**: SigDev signatures may have higher false positive rates. Use only when hunting for very recent threats.

## upgrade

**Purpose**: Get new program files AND signatures, preserve configuration.

```bash
thor-util upgrade
```

**What it does:**
- Downloads new THOR binaries
- Downloads new signatures
- Preserves: `thor.yml`, `false_positive_filters.cfg`, `directory-excludes.cfg`
- Preserves: Custom signatures in `./custom-signatures/`

**Use when:**
- Regular maintenance updates
- New THOR version available
- Need new features or bug fixes

### TechPreview Version

```bash
# Upgrade to THOR v11 TechPreview
thor-util upgrade --techpreview
```

**Warning**: TechPreview is not production-stable. Test before deploying widely.

## download

**Purpose**: Get complete package including config files. For fresh installations.

```bash
thor-util download -t thor10-win
```

**What it does:**
- Downloads complete THOR package
- Includes all binaries
- Includes all signatures
- Includes default config files (OVERWRITES existing)

**Available package types:**
- `thor10-win` – Windows
- `thor10-linux` – Linux
- `thor10-macos` – macOS

**Use when:**
- Initial installation
- Offline deployment preparation
- Need to reset to default configuration

### TechPreview Download

```bash
thor-util download -t thor10-win --techpreview
```

## Proxy Configuration

All commands support proxy settings:

```bash
# Basic proxy
thor-util upgrade -a https://proxy.company.net:8080

# Proxy with authentication
thor-util upgrade -a https://proxy.company.net:8080 -n domain\user -p password

# NTLM authentication
thor-util upgrade -a https://proxy.local:8080 --ntlm -n domain\user -p password
```

## Configuration File

Set defaults in `./config/thor-util.yml`:

```yaml
proxy: http://myproxy:8080
techpreview: false
```

## Update Servers

- Full THOR: `update1.nextron-systems.com`, `update2.nextron-systems.com`
- THOR Lite: `update-lite.nextron-systems.com`
- Server info: https://update1.nextron-systems.com/info.php

**Important**: Cannot update/download from ASGARD Management Center licenses. Must use Nextron Customer Portal.

## Report Generation

Generate HTML reports from existing log files:

```bash
# From single log file
thor-util report --logfile system-xyz_thor.txt

# From directory of logs
thor-util report --logdir ./logs
```

## Log Conversion

Convert between log formats:

```bash
# Text to JSON
thor-util logconvert --from-log --to-json -f thor.txt -o thor.json

# Text to CSV
thor-util logconvert --from-log --to-csv -f thor.txt -o thor.csv

# JSON to Text
thor-util logconvert --from-json --to-log -f thor.json -o thor.txt
```

## Verify Binaries

Verify THOR binary authenticity:

```bash
# Download public key from https://www.nextron-systems.com/pki/
openssl dgst -sha256 -verify codesign.pem -signature thor-util.exe.sig thor-util.exe
```

## Quick Reference

| Task | Command |
|------|---------|
| Update signatures | `thor-util update` |
| Upgrade everything | `thor-util upgrade` |
| Get v11 TechPreview | `thor-util upgrade --techpreview` |
| Fresh download | `thor-util download -t thor10-win` |
| Generate reports | `thor-util report --logdir ./logs` |
| Get newest (risky) sigs | `thor-util update --sigdev` |
| Reset to stable sigs | `thor-util update --force` |
