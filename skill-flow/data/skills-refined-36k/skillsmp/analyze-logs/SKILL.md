---
name: analyze-logs
description: Analyze, compare, and debug Applitools test logs. Use when comparing log files, finding test failures, identifying performance bottlenecks, or preparing logs for analysis.
argument-hint: <command> [files...] [options]
allowed-tools: Bash(cargo run:*), Bash(./target/release/log-analyzer:*), Bash(log-analyzer:*), Read, Glob, Grep
context: fork
---

# Log Analyzer Skill

Analyze JSON logs from Applitools testing framework using the log-analyzer CLI tool.

## Commands Overview

| Command | Purpose | Example |
|---------|---------|---------|
| `diff` | Show differences between two log files | `/analyze-logs diff file1.log file2.log` |
| `compare` | Full comparison with all matches | `/analyze-logs compare file1.log file2.log` |
| `info` | Analyze structure of a single log | `/analyze-logs info test.log --samples` |
| `perf` | Find performance bottlenecks | `/analyze-logs perf test.log --threshold-ms 500` |
| `llm` | Generate LLM-friendly output | `/analyze-logs llm test.log` |
| `llm-diff` | LLM-friendly diff output | `/analyze-logs llm-diff file1.log file2.log` |

See [reference.md](reference.md) for complete command documentation.

## Quick Start

### Installation

Install the latest release binary (recommended):
```bash
./scripts/install.sh
```

Or build from source:
```bash
cargo build --release
```

### Running Commands

If installed via `scripts/install.sh`:
```bash
log-analyzer <command> [options]
```

If built from source:
```bash
./target/release/log-analyzer <command> [options]
```

Or during development:
```bash
cargo run -- <command> [options]
```

## Task Instructions

When the user invokes this skill:

1. **Check if log-analyzer is available**:
   ```bash
   # Check if binary is installed
   command -v log-analyzer || which log-analyzer || [ -f ./target/release/log-analyzer ]
   ```

   If not available, inform the user:
   ```
   The log-analyzer tool is not installed. Install it with:
     ./scripts/install.sh

   Or build from source:
     cargo build --release
   ```

2. **Parse the request** to determine:
   - Which command is needed (diff, compare, info, perf, llm)
   - Which log files to analyze
   - Any filtering options (component, level, text)

3. **Find log files** if not specified:
   ```bash
   # Look for .log files in the project
   find . -name "*.log" -type f 2>/dev/null | head -10
   ```

4. **Build the command** with appropriate options:
   - Use `log-analyzer` if installed, otherwise `./target/release/log-analyzer` or `cargo run --`
   - For debugging failures: use `diff` with `--diff-only`
   - For performance issues: use `perf` with appropriate threshold
   - For understanding logs: use `info` with `--samples --payloads`

5. **Execute and interpret**:
   - Run the log-analyzer command
   - Summarize key findings in plain language
   - Highlight actionable items (errors, slow operations, differences)
   - Suggest next steps if issues are found

## Common Workflows

### Debug Test Failure
```bash
# Quick diff to see what changed
log-analyzer diff passing.log failing.log

# Focus on errors only
log-analyzer diff passing.log failing.log -f "l:ERROR"

# Focus on specific component
log-analyzer diff passing.log failing.log -f "c:core-universal"

# Combined filters
log-analyzer diff passing.log failing.log -f "c:core l:ERROR !t:timeout"
```

### Performance Investigation
```bash
# Find operations taking > 2 seconds
log-analyzer perf test.log --threshold-ms 2000

# Find orphan operations (started but never finished)
log-analyzer perf test.log --orphans-only

# Focus on requests only
log-analyzer perf test.log --op-type Request --top-n 30
```

### Log Exploration
```bash
# Full overview with samples
log-analyzer info test.log --samples --payloads --timeline

# JSON output for further processing
log-analyzer info test.log -j
```

### Prepare for LLM Analysis
```bash
# Sanitized, compact output
log-analyzer llm test.log --limit 100 -o context.json

# Diff for LLM
log-analyzer llm-diff file1.log file2.log -o diff.json
```

## Filter Expression Syntax

Use `-f, --filter` with unified expression syntax:

```bash
-f "type:value [!type:value] ..."
```

**Filter types (with aliases):**
| Type | Aliases | Description |
|------|---------|-------------|
| `component` | `comp`, `c` | Filter by component name |
| `level` | `lvl`, `l` | Filter by log level |
| `text` | `t` | Filter by text in message |
| `direction` | `dir`, `d` | Filter by direction |

**Prefix with `!` to exclude.** Examples:
```bash
-f "c:core-universal"           # Only core-universal component
-f "l:ERROR"                    # Only ERROR level logs
-f "c:core !l:DEBUG"            # Core component, exclude DEBUG
-f "t:timeout d:incoming"       # Contains 'timeout', incoming only
```

## Output Formats

- `-F text` - Human-readable colored output (default)
- `-F json` - Structured JSON output
- `-j, --json` - JSON output shorthand (implies `-F json -c`)
- `-c, --compact` - Shortened keys for compact output
- `-o, --output <path>` - Save to file

## Interpreting Results

### Diff Output
- **unique_to_log1** / **unique_to_log2**: Events only in one file
- **shared_comparisons**: Matching events with field differences
- Focus on configuration changes, error status changes, and timing differences

### Perf Output
- **Slowest Operations**: Operations exceeding threshold
- **Orphan Operations**: Started but never completed (potential hangs)
- **Statistics**: P50, P95, P99 latencies per operation type

### Info Output
- **Components**: All log sources in the file
- **Event Types**: Categorized operations
- **Timeline**: Distribution of events over time
