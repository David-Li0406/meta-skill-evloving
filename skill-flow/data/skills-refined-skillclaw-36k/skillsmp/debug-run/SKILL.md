---
name: debug-run
description: Programmatically debug code using debug-run CLI with DAP. Use when debugging .NET, Python, or JavaScript/TypeScript applications, setting breakpoints, capturing variables, evaluating expressions, or attaching to running processes.
---

# debug-run Debugging Skill

Use the `debug-run` CLI tool to programmatically debug applications via the Debug Adapter Protocol (DAP). This skill enables you to set breakpoints, capture variable state, and evaluate expressions without interactive debugger sessions.

## When to Use This Skill

- Debugging .NET applications (using vsdbg adapter)
- Debugging Python applications (using debugpy adapter)
- Debugging JavaScript/TypeScript applications (using js-debug/node adapter)
- Capturing runtime state at specific code locations
- Evaluating expressions to inspect object properties
- Attaching to running processes for live debugging

## Prerequisites

debug-run is available via npx (no installation required) or can be installed globally:

```bash
# Run directly with npx
npx debug-run --help

# Or install globally
npm install -g debug-run
```

Check available adapters:

```bash
npx debug-run list-adapters
```

## Installing the Skill

To install this skill for AI coding assistants:

```bash
# Install to Claude Code (~/.claude/skills/)
npx debug-run install-skill --claude

# Install to GitHub Copilot (~/.copilot/skills/)
npx debug-run install-skill --copilot

# Install to project directory (for project-specific skills)
npx debug-run install-skill --claude --project
npx debug-run install-skill --copilot --project

# Install to custom directory
npx debug-run install-skill --dir /path/to/skills
```

## Language-Specific Guides

For detailed setup, examples, and troubleshooting for each language:

- [.NET Debugging Guide](DOTNET.md) - vsdbg adapter, ASP.NET attach mode, NUnit test debugging
- [Python Debugging Guide](PYTHON.md) - debugpy adapter, VS Code integration, sample app
- [TypeScript/JavaScript Debugging Guide](TYPESCRIPT.md) - js-debug adapter, source maps, Node.js

## Basic Usage

```bash
npx debug-run <program> -a <adapter> -b "<file:line>" [options]
```

### Quick Examples

```bash
# .NET
npx debug-run ./bin/Debug/net8.0/MyApp.dll -a vsdbg -b "src/Service.cs:42" --pretty

# Python
npx debug-run ./main.py -a python -b "src/processor.py:25" --pretty

# TypeScript/JavaScript
npx debug-run ./dist/index.js -a node -b "src/index.ts:100" --pretty
```

## Options Reference

### Core Options

| Option | Description |
|--------|-------------|
| `-a, --adapter <name>` | Debug adapter: `vsdbg` (.NET), `python`/`debugpy` (Python), `node`/`js` (JS/TS) |
| `-b, --breakpoint <loc>` | Breakpoint location as `file:line` (can specify multiple) |
| `-e, --eval <expr>` | Expression to evaluate at breakpoints (can specify multiple) |
| `--assert <expr>` | Invariant expression; halts on first violation (can specify multiple) |
| `-t, --timeout <time>` | Timeout duration: `30s`, `2m`, `5m` (default: 60s) |
| `--pretty` | Pretty-print JSON output |
| `-o, --output <file>` | Write events to file instead of stdout |

### Attach Mode

| Option | Description |
|--------|-------------|
| `--attach` | Attach to running process instead of launching |
| `--pid <id>` | Process ID for attach mode |

### Trace Mode

| Option | Description |
|--------|-------------|
| `--trace` | Enable trace mode - step through code after breakpoint |
| `--trace-into` | Use stepIn instead of stepOver (follow into functions) |
| `--trace-limit <N>` | Max steps in trace mode (default: 500) |
| `--trace-until <expr>` | Stop trace when expression is truthy |
| `--diff-vars` | Show only changed variables in trace steps |

### Token Efficiency

| Option | Description |
|--------|-------------|
| `--expand-services` | Fully expand service types (Logger, Repository, etc.) |
| `--show-null-props` | Include null/undefined properties in output |
| `--no-dedupe` | Disable content-based deduplication |

### Event Filtering

| Option | Description |
|--------|-------------|
| `--include <types...>` | Only emit these event types |
| `--exclude <types...>` | Suppress these event types |

### Exception Handling

| Option | Description |
|--------|-------------|
| `--break-on-exception <filter>` | Break on exceptions: `all`, `uncaught`, `raised` |
| `--no-flatten-exceptions` | Disable exception chain analysis |
| `--exception-chain-depth <n>` | Max depth to traverse (default: 10) |

## Assertions

Use `--assert` to declare invariants. The debugger halts immediately when any assertion fails:

```bash
npx debug-run ./app.dll -a vsdbg \
  -b "src/OrderService.cs:42" \
  --assert "order.Total >= 0" \
  --assert "order.Items.Count > 0" \
  --pretty
```

Assertions are checked at every breakpoint hit, trace step, and regular step.

## Trace Mode

Trace mode automatically steps through code after hitting a breakpoint:

```bash
# Basic trace
npx debug-run ./app.dll -a vsdbg -b "src/Service.cs:42" --trace --pretty

# Trace into function calls with limit
npx debug-run ./app.dll -a vsdbg -b "src/Service.cs:42" --trace --trace-into --trace-limit 100 --pretty

# Trace until condition
npx debug-run ./app.dll -a vsdbg -b "src/Service.cs:42" --trace --trace-until "total > 100" --pretty

# Trace with variable diffing (shows only changes)
npx debug-run ./app.dll -a vsdbg -b "src/Service.cs:42" --trace --diff-vars --pretty
```

## Output Format

debug-run outputs NDJSON (newline-delimited JSON) events:

### Event Types

| Event | Description |
|-------|-------------|
| `session_start` | Debug session initialized |
| `breakpoint_set` | Breakpoint configured (check `verified` field) |
| `process_launched` | Debuggee process started |
| `process_attached` | Attached to running process |
| `breakpoint_hit` | Breakpoint was hit with locals and evaluations |
| `assertion_failed` | Assertion violation with context |
| `trace_started` | Trace mode began |
| `trace_step` | Single trace step (with `changes` if `--diff-vars`) |
| `trace_completed` | Trace finished |
| `exception_thrown` | Exception occurred |
| `program_output` | stdout/stderr from debuggee |
| `process_exited` | Program terminated |
| `session_end` | Summary with statistics |

### breakpoint_hit Example

```json
{
  "type": "breakpoint_hit",
  "timestamp": "...",
  "location": {
    "file": "src/Services/OrderService.cs",
    "line": 42,
    "function": "ProcessOrder"
  },
  "stackTrace": [...],
  "locals": {
    "order": { "type": "Order", "value": {...} },
    "this": {...}
  },
  "evaluations": {
    "order.Total": { "result": "125.50" },
    "order.Items.Count": { "result": "3" }
  }
}
```

## Token Efficiency

debug-run includes automatic optimizations for enterprise applications:

### Service Type Compaction (default)
Types like `Logger`, `Repository`, `Service` are shown in compact form:
```json
"logger": { "type": "Logger", "value": "{Logger}" }
```

### Null Property Omission (default)
Properties with null/undefined values are omitted.

### Content-Based Deduplication (default)
Repeated object content references the first occurrence:
```json
"loyaltyService._features": { "value": "[see: discountService._features]", "deduplicated": true }
```

## Best Practices

1. **Use relative paths for breakpoints**: `-b "src/MyFile.cs:42"` not `-b "MyFile.cs:42"`

2. **Expression timing**: Expressions evaluate BEFORE the breakpoint line executes. Variables assigned on that line will be null/unset.

3. **Unverified breakpoints**: In attach mode, breakpoints start as `verified: false`. They verify when the code path is hit.

4. **Long-running processes**: Use appropriate timeouts (`-t 5m`) and trigger the code path while debug-run is waiting.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Adapter not installed" | Run `list-adapters` to check available adapters |
| Breakpoint not hitting | Verify path is relative to working directory and line has executable code |
| Session timeout | Increase timeout with `-t 2m` or `-t 5m` |

For language-specific troubleshooting, see the language guides linked above.
