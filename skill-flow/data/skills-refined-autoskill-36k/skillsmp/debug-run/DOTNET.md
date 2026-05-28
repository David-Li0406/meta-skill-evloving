# .NET Debugging Guide

This guide covers debugging .NET applications with debug-run using the vsdbg adapter.

## Prerequisites

### vsdbg Adapter

The vsdbg adapter is automatically detected if you have the VS Code C# extension installed:

```bash
npx debug-run list-adapters
# Should show: vsdbg - Status: installed (path)
```

If not installed, install the [C# extension](https://marketplace.visualstudio.com/items?itemName=ms-dotnettools.csharp) in VS Code.

### Alternative: netcoredbg

Open-source alternative (less stable on some platforms):

```bash
npx debug-run install-adapter netcoredbg
```

## Build Your Application

Before debugging, build your .NET application:

```bash
dotnet build
```

## Launch Mode (Debug New Process)

### Basic Debugging

```bash
npx debug-run ./bin/Debug/net8.0/MyApp.dll \
  -a vsdbg \
  -b "src/Services/OrderService.cs:42" \
  --pretty \
  -t 30s
```

### With Expression Evaluation

```bash
npx debug-run ./bin/Debug/net8.0/MyApp.dll \
  -a vsdbg \
  -b "src/Services/OrderService.cs:42" \
  -e "order.Total" \
  -e "order.Items.Count" \
  -e "this._inventory.Count" \
  --pretty \
  -t 30s
```

### With Assertions

```bash
npx debug-run ./bin/Debug/net8.0/MyApp.dll \
  -a vsdbg \
  -b "src/Services/OrderService.cs:42" \
  --assert "order.Total >= 0" \
  --assert "order.Items.Count > 0" \
  --assert "this._inventory != null" \
  --pretty \
  -t 30s
```

### Exception Handling

Break on all exceptions with chain flattening:

```bash
npx debug-run ./bin/Debug/net8.0/MyApp.dll \
  -a vsdbg \
  --break-on-exception all \
  --pretty \
  -t 30s
```

## Attach Mode (ASP.NET / Long-Running Services)

For debugging running ASP.NET applications or services:

### 1. Start Your Application

```bash
cd MyWebApi
dotnet run
# Note the process - find PID with: ps aux | grep dotnet
```

### 2. Attach debug-run

```bash
npx debug-run --attach --pid <PID> \
  -a vsdbg \
  -b "src/Controllers/OrderController.cs:28" \
  -e "request.OrderId" \
  --pretty \
  -t 60s
```

### Important Notes for Attach Mode

1. **Timing matters**: After `process_attached` event, wait 10-15 seconds before triggering the code path
2. **Breakpoints start unverified**: `verified: false` is normal; they verify when the code path is hit
3. **Process survives**: In attach mode, the debuggee keeps running after debug-run exits

### Example: Debug ASP.NET Endpoint

```bash
# Terminal 1: Start the API
cd samples/aspnet/SampleApi
dotnet run  # Runs on http://localhost:5009

# Terminal 2: Attach debugger
npx debug-run --attach --pid $(pgrep -f SampleApi) \
  -a vsdbg \
  -b "samples/aspnet/SampleApi/Program.cs:16" \
  --pretty \
  -t 60s

# Terminal 3: Trigger the endpoint
curl http://localhost:5009/orders
```

## Test Debugging (NUnit, xUnit, MSTest)

debug-run supports debugging .NET unit tests with automatic test runner orchestration:

### Quick Start

```bash
# Build the test project first
cd samples/nunit && dotnet build && cd ../..

# Debug tests
npx debug-run --test-project samples/nunit \
  -b "samples/nunit/CalculatorTests.cs:57" \
  --pretty \
  -t 60s
```

### Filter Specific Tests

```bash
npx debug-run --test-project samples/nunit \
  --test-filter "Add_TwoPositiveNumbers_ReturnsSum" \
  -b "samples/nunit/CalculatorTests.cs:57" \
  --pretty
```

### With Expression Evaluation

```bash
npx debug-run --test-project samples/nunit \
  -b "samples/nunit/CalculatorTests.cs:57" \
  -e "a" -e "b" -e "result" \
  --pretty
```

### How It Works

1. Launches `dotnet test --no-build` with `VSTEST_HOST_DEBUG=1`
2. Parses the testhost PID from the output
3. Automatically attaches the debugger to the testhost process
4. Sets breakpoints and captures variables

## Trace Mode

Follow execution flow after hitting a breakpoint:

```bash
# Basic trace
npx debug-run ./bin/Debug/net8.0/MyApp.dll \
  -a vsdbg \
  -b "src/Services/OrderService.cs:42" \
  --trace \
  --pretty

# Trace into function calls
npx debug-run ./bin/Debug/net8.0/MyApp.dll \
  -a vsdbg \
  -b "src/Services/OrderService.cs:42" \
  --trace \
  --trace-into \
  --trace-limit 50 \
  --pretty

# Trace with variable diffing
npx debug-run ./bin/Debug/net8.0/MyApp.dll \
  -a vsdbg \
  -b "src/Services/OrderService.cs:42" \
  --trace \
  --diff-vars \
  --pretty
```

## Sample Application

A sample .NET console application is included for testing:

```bash
# Build
cd samples/dotnet && dotnet build && cd ../..

# Debug
npx debug-run ./samples/dotnet/bin/Debug/net8.0/SampleApp.dll \
  -a vsdbg \
  -b "samples/dotnet/Program.cs:67" \
  --pretty \
  -t 30s
```

### Good Breakpoint Locations

| Line | Location | Description |
|------|----------|-------------|
| 67 | `ProcessOrder` | Inside order processing method |
| 51 | `Main` | After configuration setup |
| 78 | `CalculateDiscount` | Discount calculation logic |

## Token Efficiency for .NET

### Blocked Properties (Automatic)

debug-run automatically filters verbose .NET reflection metadata:
- `EqualityContract` - C# record equality (often 4KB+ of noise)
- `CustomAttributes`, `DeclaredConstructors`, `DeclaredMethods`
- `[More]`, `Raw View`, `Static members`, `Non-Public members`

### Service Type Compaction

Common service patterns are compacted by default:
```json
"_logger": { "type": "ILogger<OrderService>", "value": "{ILogger}" }
"_repository": { "type": "OrderRepository", "value": "{Repository}" }
```

Override with `--expand-services` if you need full expansion.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| vsdbg license warning | Informational only, can be ignored |
| netcoredbg SIGSEGV | Use vsdbg instead (`-a vsdbg`) |
| "Adapter not installed" | Install VS Code C# extension |
| Breakpoint not verified | Wait longer after attach, or check file path |
| Test not stopping | Ensure `--no-build` and build manually first |

### Debug Adapter Communication

Enable verbose DAP logging:

```bash
DEBUG_DAP=1 npx debug-run ./app.dll -a vsdbg -b "file.cs:10" --pretty
```
