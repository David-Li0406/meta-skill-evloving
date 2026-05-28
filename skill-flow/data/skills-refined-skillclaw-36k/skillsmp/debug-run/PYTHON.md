# Python Debugging Guide

This guide covers debugging Python applications with debug-run using the debugpy adapter.

## Prerequisites

### debugpy Adapter

The debugpy adapter is automatically detected from two sources:

1. **VS Code Python Extension** (recommended) - debugpy is bundled with it
2. **pip installation** - `pip install debugpy`

Check availability:

```bash
npx debug-run list-adapters
# Should show: debugpy - Status: installed (VS Code Python extension or pip)
```

### Installing debugpy

**Option 1: VS Code Python Extension (Recommended)**
- Install the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) in VS Code
- debugpy is bundled automatically

**Option 2: pip**
```bash
pip install debugpy
# or
pip3 install debugpy
```

## Launch Mode (Debug Python Script)

### Basic Debugging

```bash
npx debug-run ./main.py \
  -a python \
  -b "src/processor.py:25" \
  --pretty \
  -t 30s
```

### With Expression Evaluation

```bash
npx debug-run ./main.py \
  -a python \
  -b "src/processor.py:42" \
  -e "subtotal" \
  -e "tax" \
  -e "order.order_id" \
  -e "len(order.items)" \
  --pretty \
  -t 30s
```

### With Assertions

```bash
npx debug-run ./main.py \
  -a python \
  -b "src/processor.py:42" \
  --assert "subtotal >= 0" \
  --assert "len(order.items) > 0" \
  --assert "customer is not None" \
  --pretty \
  -t 30s
```

### Exception Handling

Break on raised or uncaught exceptions:

```bash
# Break on all raised exceptions
npx debug-run ./main.py \
  -a python \
  --break-on-exception raised \
  --pretty \
  -t 30s

# Break on uncaught exceptions only
npx debug-run ./main.py \
  -a python \
  --break-on-exception uncaught \
  --pretty \
  -t 30s
```

## Adapter Aliases

Both `-a python` and `-a debugpy` work identically:

```bash
# These are equivalent
npx debug-run ./main.py -a python -b "main.py:10" --pretty
npx debug-run ./main.py -a debugpy -b "main.py:10" --pretty
```

## Sample Application

A sample Python application is included for testing:

```bash
# Debug the sample app
npx debug-run samples/python/sample_app.py \
  -a python \
  -b "samples/python/sample_app.py:185" \
  --pretty \
  -t 30s
```

### With Expression Evaluation

```bash
npx debug-run samples/python/sample_app.py \
  -a python \
  -b "samples/python/sample_app.py:188" \
  -e "subtotal" \
  -e "tax" \
  -e "discount" \
  -e "order.order_id" \
  --pretty \
  -t 30s
```

### Good Breakpoint Locations (Sample App)

| Line | Location | Description |
|------|----------|-------------|
| 185 | `process_order` | After variable setup, before loyalty points |
| 140 | `calculate_discount` | After discount rate calculation |
| 298 | `main` | Before processing first order |
| 178 | `process_order` | Inside inventory loop |

## Trace Mode

Follow execution flow after hitting a breakpoint:

```bash
# Basic trace
npx debug-run ./main.py \
  -a python \
  -b "src/processor.py:25" \
  --trace \
  --pretty

# Trace into function calls
npx debug-run ./main.py \
  -a python \
  -b "src/processor.py:25" \
  --trace \
  --trace-into \
  --trace-limit 50 \
  --pretty

# Trace with variable diffing
npx debug-run ./main.py \
  -a python \
  -b "src/processor.py:25" \
  --trace \
  --diff-vars \
  --pretty
```

## Python-Specific Notes

### Breakpoint Timing

Breakpoints are set AFTER launch for Python (debugpy's DAP flow differs from .NET). This is handled automatically by debug-run.

### Dataclass Variables

Python dataclasses show a `special variables` section in locals containing class metadata. This is normal debugpy behavior. The actual instance fields are shown alongside.

```json
{
  "customer": {
    "type": "Customer",
    "value": {
      "special variables": {...},  // Class metadata
      "id": { "type": "str", "value": "CUST-001" },
      "name": { "type": "str", "value": "Alice" },
      "email": { "type": "str", "value": "alice@example.com" }
    }
  }
}
```

### justMyCode

By default, debug-run sets `justMyCode: false` to allow stepping into library code. The default Python debugger behavior only stops in user code.

### Expression Syntax

Use Python syntax for expressions:

```bash
# Python expressions
-e "len(items)"
-e "order.items[0].price"
-e "sum(item.quantity for item in order.items)"
-e "customer.loyalty_tier.value"
```

## Working with Virtual Environments

If your project uses a virtual environment, activate it before running debug-run:

```bash
# Activate venv
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows

# Then debug
npx debug-run ./main.py -a python -b "main.py:10" --pretty
```

debug-run uses the active Python interpreter, which will have access to your virtual environment's packages.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "debugpy not found" | Install VS Code Python extension or `pip install debugpy` |
| "python not found" | Ensure Python 3 is in PATH (`python3 --version`) |
| Variables show as "not defined" | Expression is evaluated BEFORE the line executes |
| Breakpoint not hitting | Check file path is correct and line has executable code |
| Timeout before breakpoint | Increase timeout with `-t 60s` or `-t 2m` |

### Debug Adapter Communication

Enable verbose DAP logging to troubleshoot:

```bash
DEBUG_DAP=1 npx debug-run ./main.py -a python -b "main.py:10" --pretty
```

### Verify debugpy Installation

```bash
# Check if debugpy is importable
python3 -c "import debugpy; print(debugpy.__version__)"

# Check adapter detection
npx debug-run list-adapters
```

## Common Patterns

### Debug a Flask/Django App

```bash
# Flask
npx debug-run app.py \
  -a python \
  -b "app.py:25" \
  --pretty \
  -t 120s

# Django (using manage.py)
npx debug-run manage.py runserver \
  -a python \
  -b "myapp/views.py:42" \
  --pretty \
  -t 120s
```

### Debug with Arguments

```bash
npx debug-run ./script.py -- --input data.json --verbose \
  -a python \
  -b "script.py:15" \
  --pretty
```

Arguments after `--` are passed to your Python script.
