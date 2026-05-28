# THOR Lite Limitations

THOR Lite is a free scanner with reduced capabilities compared to full THOR. This document covers what's different, how to recognize Lite, and workarounds for common expectations.

## Feature Comparison

| Capability | Full THOR | THOR Lite |
|------------|-----------|-----------|
| YARA rules | 30,000+ (private + open source) | ~4,000 (open source only) |
| Sigma rules | 4,000+ | Not available |
| Modules | ~31 | ~5 |
| Lab mode | Yes | No |
| Audit trail | Yes (v11) | No |
| Event log scanning | Yes | Limited |
| Registry analysis | Yes | Limited |
| Memory scanning | Yes | Limited |
| Commercial use | Licensed | Non-commercial only |

## How to Recognize THOR Lite

Check the first ~50 lines of scan output for these indicators:

**Version header:**
```
THOR Lite 10.x.x
```

**Startup notices:**
```
Some modules and features are not available in Lite version and will be disabled
```

**Disabled components list:**
```
Disabled components:
  - SigmaModule ... REASON: Component is not available in THOR Lite
  - RegistryChecks ... REASON: License restrictions
  - EventLogScanner ... REASON: Platform unavailable
```

If you see these messages, the user is running THOR Lite, not full THOR.

## Binary Names

| Platform | Scanner | Utility |
|----------|---------|---------|
| Windows | `thor64-lite.exe` | `thor-lite-util.exe` |
| Linux | `thor-lite-linux-64` | `thor-lite-util` |
| macOS | `thor-lite-macos` | `thor-lite-util` |

## Missing Features and Workarounds

### No Lab Mode

THOR Lite does not have the `--lab` switch. For "scan everything" behavior, use this flag combination:

```bash
# Windows
thor64-lite.exe -a Filescan --intense --norescontrol --cross-platform -p <path>

# Linux
./thor-lite-linux-64 -a Filescan --intense --norescontrol --cross-platform -p <path>

# macOS
./thor-lite-macos -a Filescan --intense --norescontrol --cross-platform -p <path>
```

**Flags explained:**
- `-a Filescan` – Run only the Filescan module (most comprehensive in Lite)
- `--intense` – Enable intense scanning mode
- `--norescontrol` – Disable resource control (no CPU/memory throttling)
- `--cross-platform` – Match signatures across all platforms
- `-p <path>` – Target path to scan

This approximates lab-like behavior but is not equal to full lab scanning.

### No Sigma Scanning

Sigma rules for event log analysis are not available in THOR Lite. If you need:
- Windows event log analysis with Sigma rules
- Detection of lateral movement patterns
- Advanced persistence detection via logs

You need full THOR.

### No Audit Trail (Blocks THOR Lens)

THOR Lite cannot generate audit trail output. This means:
- THOR Lens workflows are not possible with Lite
- No forensic timeline generation
- No interactive exploration via Lens UI

Audit trail requires THOR v11 full version.

### Limited Module Coverage

THOR Lite runs only ~5 modules compared to ~31 in full THOR. Missing modules include:
- Many persistence checks
- Advanced registry analysis
- Detailed process analysis
- Network connection analysis
- Scheduled task analysis

Scans may appear "too quiet" because fewer checks are running.

## When to Recommend Full THOR

Suggest upgrading from Lite when the user needs:

1. **Sigma/event log analysis** – Lite has no Sigma support
2. **Audit trail output** – Required for THOR Lens
3. **Comprehensive coverage** – Private signature set has 7x more YARA rules
4. **Full module set** – 31 vs 5 modules
5. **Commercial use** – Lite restricts commercial/paid engagements

## License Restrictions

THOR Lite is for non-commercial use only. The startup notice and EULA prohibit:
- Selling services that include THOR Lite scans
- Using Lite in paid engagements

If a user describes a commercial engagement, they need full THOR licensing.

## Update Server

THOR Lite uses a different update server:
- Full THOR: `update1.nextron-systems.com`, `update2.nextron-systems.com`
- THOR Lite: `update-lite.nextron-systems.com`

Update commands work the same way:
```bash
./thor-lite-util update
```

## Quick Decision Helper

**You're running THOR Lite if:**
- Binary name contains "lite"
- Startup shows "THOR Lite" version header
- Log mentions "not available in Lite version"

**Therefore these features will NOT work:**
- Lab mode (`--lab` flag)
- Sigma scanning
- Audit trail output
- THOR Lens integration
- Full module coverage (~5 instead of ~31 modules)
- Private signature database (open source rules only)
