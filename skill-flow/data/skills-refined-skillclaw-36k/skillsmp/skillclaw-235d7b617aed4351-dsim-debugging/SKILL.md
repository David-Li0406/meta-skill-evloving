---
name: dsim-debugging
description: Use this skill when investigating compilation errors, runtime failures, waveform analysis, or DSIM environment issues in the Metrics DSIM simulator.
---

# DSIM Debugging and Troubleshooting

Debugging methodology for the Metrics DSIM simulator in the AXIUART_RV32I verification environment.

## When to Use This Skill

- Investigating compilation or simulation failures
- Analyzing waveform data
- Troubleshooting DSIM environment configuration
- Resolving timescale mismatches or structural errors
- Optimizing simulation performance

## DSIM Environment Variables

### Required Variables (MANDATORY)

```powershell
# Check current environment
$env:DSIM_HOME
$env:DSIM_ROOT
$env:DSIM_LIB_PATH
$env:DSIM_LICENSE
```

### Verification

```bash
python mcp_server/mcp_client.py --workspace . --tool check_dsim_environment
```

**Expected output:**
```json
{
  "valid": true,
  "DSIM_HOME": "C:\\Metrics\\dsim-20231215",
  "DSIM_ROOT": "C:\\Metrics\\dsim-20231215",
  "DSIM_LIB_PATH": "C:\\Metrics\\dsim-20231215\\lib",
  "DSIM_LICENSE": "27020@license-server.local",
  "executable": "C:\\Metrics\\dsim-20231215\\bin\\dsim.exe"
}
```

### Common Issues

**Missing DSIM_HOME:**
```powershell
$env:DSIM_HOME = "C:\Metrics\dsim-20231215"
$env:DSIM_ROOT = $env:DSIM_HOME
$env:DSIM_LIB_PATH = "$env:DSIM_HOME\lib"
```

**License errors:**
```powershell
$env:DSIM_LICENSE = "27020@license-server.local"
dsim -version  # Test license connectivity
```

## Waveform Strategy

### MXD vs VCD

**Default: MXD waveform format** (Metrics proprietary)

**MXD advantages:**
- Faster dump performance
- Smaller file size
- Better compression
- Native DSIM format

**Enable MXD in simulation:**
```systemverilog
initial begin
    $dumpfile("sim/logs/axiuart_basic_test.mxd");
    $dumpvars(0, tb_axiuart_top);
end
```

**VCD (compatibility mode):**
```systemverilog
initial begin
    $dumpfile("sim/logs/axiuart_basic_test.vcd");
    $dumpvars(0, tb_axiuart_top);
end
```

**Avoid VCD unless:**
- Sharing waveforms with non-DSIM tools
- Post-processing with standard VCD parsers

## Assertion-Driven Debugging

### Priority Workflow

**1. Assertions FIRST → 2. Waveforms SECOND**

Investigate assertion failures before opening the waveform viewer:

```bash
# Check assertion summary in log
grep "Assertion" sim/logs/axiuart_basic_test.log

# Filter for failures
grep "Assertion.*failed" sim/logs/axiuart_basic_test.log
```

### Assertion Error Analysis

**Example failure:**
```
** Err
```