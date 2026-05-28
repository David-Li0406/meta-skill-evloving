---
name: mcp-workflow
description: Use this skill when compiling tests, running simulations, executing regression suites, or troubleshooting MCP integration in a UVM testing environment.
---

# MCP Workflow for DSIM UVM Testing

FastMCP + VS Code MCP integration workflow for the AXIUART_RV32I verification environment.

## When to Use This Skill

- Compiling or running UVM tests
- Executing regression test suites
- Troubleshooting MCP server connectivity
- Understanding VS Code task integration
- Configuring test timeout policies

## Primary Workflow (MANDATORY)

**Use FastMCP + VS Code MCP integration** - configured in `.vscode/mcp.json`

**Do not violate this rule.** MCP server provides structured JSON outputs, automatic timeout management, and integrated telemetry.

## Standard UVM Test Sequence

### 1. Check DSIM Environment

```bash
python mcp_server/mcp_client.py \
    --workspace e:\Nautilus\workspace\fpgawork\AXIUART_RV32I \
    --tool check_dsim_environment
```

**Verifies:**
- `DSIM_HOME`, `DSIM_ROOT`, `DSIM_LIB_PATH`, `DSIM_LICENSE` environment variables
- DSIM executable accessibility
- License validity

### 2. List Available Tests

```bash
python mcp_server/mcp_client.py \
    --workspace e:\Nautilus\workspace\fpgawork\AXIUART_RV32I \
    --tool list_available_tests
```

**Returns:** JSON list of all UVM tests in [sim/tests/](../../sim/tests/)

### 3. Compile Test

```bash
python mcp_server/mcp_client.py \
    --workspace e:\Nautilus\workspace\fpgawork\AXIUART_RV32I \
    --tool run_uvm_simulation \
    --test-name <test> \
    --mode compile \
    --verbosity UVM_LOW
```

**Example:**
```bash
python mcp_server/mcp_client.py \
    --workspace e:\Nautilus\workspace\fpgawork\AXIUART_RV32I \
    --tool run_uvm_simulation \
    --test-name axiuart_basic_test \
    --mode compile \
    --verbosity UVM_LOW
```

### 4. Run Simulation

```bash
python mcp_server/mcp_client.py \
    --workspace e:\Nautilus\workspace\fpgawork\AXIUART_RV32I \
    --tool run_uvm_simulation \
    --test-name <test> \
    --mode run \
    --verbosity UVM_MEDIUM \
    --waves
```

**Example:**
```bash
python mcp_server/mcp_client.py \
    --workspace e:\Nautilus\workspace\fpgawork\AXIUART_RV32I \
    --tool run_uvm_simulation \
    --test-name axiuart_basic_test \
    --mode run \
    --verbosity UVM_MEDIUM \
    --waves
```

## Timeout Policy (CRITICAL)

**NEVER specify `--timeout` parameter**

MCP server auto-selects timeout from [test_timing_config.json](../../mcp_)