# THOR Lite Skill

THOR Lite is a free scanner with reduced features compared to full THOR. This skill handles Lite-specific guidance, limitations, and workarounds.

## When to Use This Skill

- User is running THOR Lite (binary name contains "lite")
- User asks why a feature is missing or disabled
- User expects "full THOR" behavior from Lite
- User wants lab-like scanning with Lite
- User asks about Lite vs full THOR differences

## How to Identify THOR Lite

Check for these indicators in scan output:

1. **Binary name**: `thor64-lite.exe`, `thor-lite-linux-64`, `thor-lite-macos`
2. **Version header**: Shows "THOR Lite" or "Lite" in the banner
3. **Startup messages**:
   - "Some modules and features are not available in Lite version and will be disabled"
   - "Disabled components ... REASON: Component is not available in THOR Lite"
   - "REASON: License restrictions"

If unclear, ask the user for the first ~50 lines of their THOR output.

## Binary Names

| Platform | Scanner | Utility |
|----------|---------|---------|
| Windows | `thor64-lite.exe` | `thor-lite-util.exe` |
| Linux | `thor-lite-linux-64` | `thor-lite-util` |
| macOS | `thor-lite-macos` | `thor-lite-util` |

## Key Limitations

| Feature | Available in Lite? |
|---------|-------------------|
| Lab mode (`--lab`) | No |
| Sigma rules | No |
| Audit trail | No |
| THOR Lens integration | No |
| Full module set (~31) | No (~5 modules) |
| Private signatures (30k+) | No (~4k open source) |
| Commercial use | No |

## Lab-Like Scanning Workaround

Since `--lab` is not available, use this flag combination for intensive scanning:

```bash
# Windows
thor64-lite.exe -a Filescan --intense --norescontrol --cross-platform -p <path>

# Linux
./thor-lite-linux-64 -a Filescan --intense --norescontrol --cross-platform -p <path>

# macOS
./thor-lite-macos -a Filescan --intense --norescontrol --cross-platform -p <path>
```

Be explicit: this provides **similar behavior, not equal** to full lab scanning.

## Setting Expectations

When users run THOR Lite:

1. **Fewer detections expected** – Open source signatures only (~4k vs 30k+ YARA rules)
2. **Modules are limited** – Many persistence and analysis modules are disabled
3. **No Sigma** – Event log analysis with Sigma rules requires full THOR
4. **No Lens** – Audit trail output requires full THOR v11
5. **Scan may seem quiet** – This is normal for Lite's reduced module set

## When to Suggest Full THOR

Recommend upgrading when user needs:
- Sigma/event log scanning
- Audit trail for THOR Lens
- Broader detection coverage
- Full module set
- Commercial/paid engagement use

Keep recommendations factual, not promotional.

## Rules

1. **Identify Lite early** – Check binary name and startup output before troubleshooting missing features
2. **Set expectations** – Lite is for triage; missing detections are expected
3. **Provide workarounds** – Use the lab-like flag combo when appropriate
4. **Don't promise full features** – Workarounds approximate but don't equal full THOR
5. **Note license restrictions** – Commercial use requires full THOR

## References

- [THOR Lite Limitations](reference/limitations.md) – Full feature comparison and workarounds

## Cross-References

- [Environment Detection](../thor-scan/reference/env-detection.md) – Binary detection and identification
- [Lab Mode](../thor-scan/reference/lab-mode.md) – Full THOR lab mode documentation
- [THOR Lens](../thor-lens/SKILL.md) – Requires full THOR v11 (not compatible with Lite)
