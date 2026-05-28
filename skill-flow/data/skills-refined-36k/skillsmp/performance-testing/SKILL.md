---
name: performance-testing
description: Use when the user asks to run performance tests, check for performance regressions, validate performance, or stress test event sourcing. Handles LOCAL mode (runs API locally) and REMOTE mode (targets deployed servidor API). Supports concurrent update tests, high-volume throughput tests, and combined stress tests. Delegates to the perf-test-runner sub-agent. Trigger phrases include "run perf test", "run remote perf test", "run concurrent perf tests", "run high-volume tests", "stress test event sourcing", "test concurrent updates", "validate throughput".
allowed-tools: ["Task"]
---

# Performance Testing Skill

This skill provides automated performance testing with intelligent script discovery, regression detection, and baseline comparison.

## When This Skill Activates

Use this skill when you detect the user wants to run performance tests. Common trigger phrases:

### General Performance Testing
- "Run performance tests"
- "Check performance"
- "Run perf tests"
- "Test performance"
- "Check for performance regressions"
- "Validate performance"
- "Execute performance tests"
- "Perf test"

### Remote Mode (Target Deployed API)
- "Run remote perf test"
- "Run remote performance test"
- "Test servidor performance"
- "Perf test against servidor"
- "Remote stress test"

### Event Sourcing Specific Tests
- "Test concurrent updates"
- "Run concurrent perf tests"
- "Stress test event sourcing"
- "Test optimistic concurrency"
- "Run high-volume tests"
- "High-volume perf test"
- "Test throughput"
- "Validate projection lag"
- "Run stress-full tests"
- "Full event sourcing stress test"

### Test Type Variations
- "Run concurrent-update test"
- "Run high-volume test"
- "Run stress-full test"
- "Test 500 VUs"
- "Progressive load test"

**Key indicators**:
1. Mentions "performance", "perf", "stress", "load", or "throughput"
2. Indicates testing or validation
3. May mention "remote", "servidor", "concurrent", "high-volume", "event sourcing"
4. May specify test scenarios like "500 VUs" or "progressive"

## What This Skill Does

When activated, immediately delegate to the `perf-test-runner` sub-agent by using the Task tool:

```
Use the Task tool with:
- subagent_type: "perf-test-runner"
- description: "Run performance tests"
- prompt: "Run performance tests using the run-performance-tests.sh script.

PREREQUISITES CHECK:
Before running tests, check if the test type requires k6-exec extension:
- If test type is 'high-volume', 'concurrent-update', or 'stress-full': Requires k6-exec
- If k6-exec not found at /tmp/k6-exec (or auto-detected locations):
  1. Install xk6: go install go.k6.io/xk6/cmd/xk6@latest
  2. Build k6-exec: ~/go/bin/xk6 build --with github.com/grafana/xk6-exec@latest --output /tmp/k6-exec
  3. Verify: ls -lh /tmp/k6-exec
- The script will auto-detect k6-exec in common locations (/tmp/k6-exec, ~/.local/bin/k6-exec, /usr/local/bin/k6-exec)

IMPORTANT: Analyze the user's request to determine:
1. MODE: Remote (--remote flag) vs Local (default, no flag)
   - If user mentions 'remote', 'servidor', or 'deployed API': Add --remote flag
   - Default: No flag (local mode)

2. TEST TYPE (-t flag):
   - If mentions 'concurrent updates' or 'optimistic concurrency': Use -t concurrent-update
   - If mentions 'high-volume' or 'throughput': Use -t high-volume
   - If mentions 'stress-full' or 'both tests': Use -t stress-full
   - Default: -t company (basic company test)

3. TEST SCENARIO (-s flag):
   - If mentions '500 VUs' or 'stress': Use -s stress_to_500vu
   - If mentions 'progressive' or 'ramp': Use -s high_volume_ramp_to_500vu (for high-volume) or concurrent_ramp_to_100vu (for concurrent)
   - Default: smoke_test

EXAMPLES:
- 'Run remote perf test' → ./run-performance-tests.sh --remote -t company -s smoke_test
- 'Run concurrent perf tests' → ./run-performance-tests.sh -t concurrent-update -s concurrent_ramp_to_100vu
- 'Stress test event sourcing against servidor' → ./run-performance-tests.sh --remote -t stress-full
- 'Test high-volume with 500 VUs remotely' → ./run-performance-tests.sh --remote -t high-volume -s high_volume_ramp_to_500vu

After running, analyze results for regressions, compare with baseline if available, and generate a comprehensive report."
```

## Why Delegate to Sub-agent?

The `perf-test-runner` sub-agent is specialized for this workflow and will:
1. **Smart script discovery**: Searches common locations and patterns
2. **Real-time monitoring**: Shows output as tests run
3. **Regression detection**: Parses output for regression keywords and metrics
4. **Baseline comparison**: Compares current results with saved baseline
5. **Comprehensive reporting**: Highlights regressions, improvements, and stable metrics
6. **Result persistence**: Saves timestamped results for history tracking

## Test Modes and Types

### Local Mode (Default)
Runs the API locally, then executes performance tests against it.
```
User: "Run perf tests"
→ Starts API on localhost, runs tests
```

### Remote Mode (--remote)
Targets an already-deployed API on servidor (skips local API startup).
```
User: "Run remote perf test"
→ Tests against servidor:5214 (deployed API)
```

### Test Types

#### 1. Company Tests (Default)
Basic CRUD operations for companies.
```
User: "Run perf test"
→ -t company
```

#### 2. Concurrent Update Tests
Multiple VUs updating THE SAME entity - tests optimistic concurrency.
```
User: "Run concurrent perf tests"
User: "Test optimistic concurrency"
→ -t concurrent-update

Scenarios:
- concurrent_ramp_to_100vu (14 min) - Progressive: 10→100 VUs
- stress_to_500vu (21 min) - Find breaking point: 10→500 VUs
- concurrent_spike (10 min) - Spike recovery
- sustained_concurrency (15 min) - Stability test
```

#### 3. High-Volume Tests
Many VUs creating/updating DIFFERENT entities - tests throughput and projection lag.
```
User: "Run high-volume perf test"
User: "Test throughput"
→ -t high-volume

Scenarios:
- high_volume_ramp_to_500vu (25 min) - Progressive: 10→500 VUs
- sustained_1000_events_per_sec (10 min) - Constant 1000 events/sec
- stress_find_limit (16 min) - Find limit: 100→2500 events/sec
```

#### 4. Stress-Full (Combined)
Runs both concurrent-update AND high-volume tests.
```
User: "Stress test event sourcing"
User: "Run stress-full test"
→ -t stress-full
```

## User Experience

**Before this skill:**
```
User: "Run performance tests"
Claude: [Asks where the script is, runs manually, hard to interpret results]
```

**With this skill:**
```
User: "Run performance tests"
Skill: [Auto-activates]
Sub-agent: [Finds script, runs tests, analyzes, reports regressions]
Result: ✅ Clear report with actionable insights
```

**New: Remote mode with event sourcing tests:**
```
User: "Run remote concurrent perf tests"
Skill: [Auto-activates, detects remote + concurrent-update]
Sub-agent: [Runs --remote -t concurrent-update against servidor]
Result: ✅ Report with concurrency conflict rates, retry success, response times
```

## Features

### Intelligent Script Discovery

Searches in priority order:
1. `./run-performance-tests.sh`
2. `./scripts/run-performance-tests.sh`
3. `./test/performance/run-tests.sh`
4. `./perf-test.sh`
5. Project-wide search for `*performance*.sh` and `*perf*.sh`

If multiple found, asks user which to use.

### Regression Detection

**Keyword-based**:
- Searches output for: regression, slower, degraded, failed, timeout, error
- Extracts context around matches
- Includes in report

**Metric-based** (when baseline exists):
- Compares current metrics vs baseline
- Calculates percentage change
- Flags changes > 5% threshold
- Categorizes as: Regression, Improvement, or Stable

### Baseline Management

- **First run**: Automatically creates baseline
- **Subsequent runs**: Compares against baseline
- **Update baseline**: User can request baseline update
- **Trend analysis**: Can show performance over multiple runs

### Result Persistence

Saves to `.perf-results/` directory:
```
.perf-results/
├── 2025-10-23-145230.log       # Full test output
├── 2025-10-23-145230.json      # Parsed results
├── latest.json                  # Symlink to latest
├── baseline.json                # Current baseline
└── history.json                 # Summary of all runs
```

### Comprehensive Reports

```
📊 Performance Test Results

Status: ✅ PASSED (with 2 warnings)

Regressions:
⚠️ API response time: 250ms → 320ms (+28%)
⚠️ Memory usage: 512MB → 580MB (+13%)

Improvements:
✅ Database queries: 45ms → 38ms (-15%)
✅ Cache hit rate: 85% → 92% (+8%)

Stable:
• Health check: 45ms (no change)

Results saved: .perf-results/2025-10-23-145230.json
```

## Safety Features

- **Non-destructive**: Only runs tests, never modifies code
- **Warning on uncommitted changes**: Alerts if working directory is dirty
- **Exit code validation**: Checks script exit code for failures
- **Graceful degradation**: Works even without baseline

## Supporting Files

This skill directory includes:
- `SKILL.md` (this file) - Skill definition and activation logic
- `README.md` - Detailed workflow documentation and examples

## Configuration

### Optional: Custom Configuration

Create `.perf-config.json` in project root:
```json
{
  "script": "./custom/path/to/perf-script.sh",
  "regressionThreshold": 10,
  "metrics": {
    "api_response_time": {
      "unit": "ms",
      "lowerIsBetter": true,
      "threshold": 5
    }
  }
}
```

### Required: Performance Test Script

Must have a performance test script in your project:
- Named one of: `run-performance-tests.sh`, `perf-test.sh`, etc.
- Located in: root, `./scripts/`, `./test/performance/`, or similar
- Executable (`chmod +x`)
- Outputs metrics in recognizable format

### Required: k6-exec Extension (for event sourcing tests)

High-volume and concurrent update tests require k6 with the exec extension for projection lag measurement:

**Installation:**
```bash
# 1. Install xk6 build tool
go install go.k6.io/xk6/cmd/xk6@latest

# 2. Build k6 with exec extension
~/go/bin/xk6 build --with github.com/grafana/xk6-exec@latest --output /tmp/k6-exec

# 3. Verify installation
/tmp/k6-exec version
```

**Auto-Detection:**
The script automatically detects k6-exec in these locations (in priority order):
1. `/tmp/k6-exec` (default build location)
2. `~/.local/bin/k6-exec`
3. `/usr/local/bin/k6-exec`
4. Anywhere in PATH as `k6-exec`

**Required for:**
- `concurrent-update` tests (optimistic concurrency testing)
- `high-volume` tests (throughput and projection lag)
- `stress-full` tests (both combined)
- Any test with projection lag measurement

## Troubleshooting

### k6-exec Not Found

**Problem**: "k6-exec binary not found at /tmp/k6-exec"

**Solutions**:
```bash
# Install xk6 and build k6-exec
go install go.k6.io/xk6/cmd/xk6@latest
~/go/bin/xk6 build --with github.com/grafana/xk6-exec@latest --output /tmp/k6-exec
```

**Alternative**: Use concurrent-update test which doesn't require exec extension:
```bash
./run-performance-tests.sh --remote -t concurrent-update -s concurrent_ramp_to_100vu
```

### Script Not Found

**Problem**: "No performance test script found"

**Solutions**:
- Ensure script exists in common locations
- Name it with "performance" or "perf" in the filename
- Make it executable: `chmod +x script-name.sh`
- Specify path in `.perf-config.json`

### No Metrics Detected

**Problem**: "No metrics extracted from test output"

**Solutions**:
- Ensure script outputs metrics in recognizable format:
  - "Metric name: 123ms"
  - "Response time: 1.5s"
  - "Memory: 512MB"
- Check `.perf-results/latest.log` for actual output

### False Regressions

**Problem**: Regressions reported but performance is actually fine

**Solutions**:
- Check if baseline is stale
- Update baseline: "Update the performance baseline"
- Adjust threshold in `.perf-config.json`

## Advanced Usage

### Update Baseline

```
You: "Update the performance baseline with latest results"

Sub-agent: Updates baseline.json with current run
```

### Trend Analysis

```
You: "Show performance trend over last 5 runs"

Sub-agent: Displays metric trends from history.json
```

### Custom Script Path

```
You: "Run performance tests using ./custom/perf.sh"

Sub-agent: Uses specified script instead of searching
```

## Integration with Other Workflows

This skill complements:
- **CI/CD pipelines**: Run perf tests before merge
- **CodeRabbit workflow**: Check performance after fixes
- **Post-merge cleanup**: Validate performance on main branch
- **Feature development**: Continuous performance monitoring

---

## Quick Reference: All Supported Variations

### Local Mode (Default)
```
"Run perf test"
"Run performance tests"
"Check performance"
"Run concurrent perf tests"
"Run high-volume tests"
"Stress test event sourcing"
```

### Remote Mode (Servidor)
```
"Run remote perf test"
"Run remote performance test"
"Test servidor performance"
"Perf test against servidor"
"Run remote concurrent perf tests"
"Remote high-volume test"
"Stress test event sourcing against servidor"
```

### Specific Test Types
```
"Run concurrent-update test"           → Tests optimistic concurrency
"Run high-volume test"                 → Tests throughput & projection lag
"Run stress-full test"                 → Runs both tests
"Test concurrent updates"              → Concurrent-update
"Test throughput"                      → High-volume
"Validate projection lag"              → High-volume
```

### With Scenarios
```
"Run concurrent test with 500 VUs"     → concurrent-update with stress_to_500vu
"Test high-volume progressive load"    → high-volume with high_volume_ramp_to_500vu
"Stress test with 500 users"          → stress-full
```

### Combined Examples
```
"Run remote concurrent perf tests"
→ ./run-performance-tests.sh --remote -t concurrent-update

"Test high-volume with 500 VUs remotely"
→ ./run-performance-tests.sh --remote -t high-volume -s high_volume_ramp_to_500vu

"Stress test event sourcing against servidor"
→ ./run-performance-tests.sh --remote -t stress-full
```
