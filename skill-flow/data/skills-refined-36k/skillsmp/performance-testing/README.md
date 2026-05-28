# Performance Testing Skill

Automated performance testing with intelligent script discovery, regression detection, and baseline comparison.

## Overview

This skill streamlines performance testing by:
1. Intelligently finding your performance test script
2. Running tests with real-time monitoring
3. Analyzing results for regressions
4. Comparing against baseline metrics
5. Generating comprehensive, actionable reports
6. Tracking results history for trend analysis

## Quick Start

Simply say:
```
"Run performance tests"
```

The skill auto-activates and handles everything.

## The Problem This Solves

### Before (Manual Process)

```
You: "Where's my performance test script again?"
You: "Let me run it manually..."
You: *Waits for completion*
You: *Reads hundreds of lines of output*
You: "Are these results good? Hard to tell..."
You: "What was the baseline? I forgot..."
Result: Time wasted, unclear if there are regressions
```

### After (With This Skill)

```
You: "Run performance tests"
Skill: ✅ Found script, ran tests, compared with baseline, highlighted 2 regressions
Result: Clear, actionable report in minutes
```

## How It Works

### Architecture

```
User Request
    ↓
[performance-testing Skill] ← Auto-activates
    ↓
[perf-test-runner Sub-agent] ← Intelligent executor
    ↓
Script Discovery → Execute → Analyze → Compare → Report
```

### Script Discovery Flow

```
1. Check ./run-performance-tests.sh
   ↓ not found
2. Check ./scripts/run-performance-tests.sh
   ↓ not found
3. Check ./test/performance/run-tests.sh
   ↓ not found
4. Check ./perf-test.sh
   ↓ not found
5. Search project for *performance*.sh, *perf*.sh
   ↓ found multiple
6. Ask user which to use
   ↓ user selects #2
7. Run ./scripts/my-perf-tests.sh
```

### Analysis Pipeline

```
Test Output
    ↓
Parse for Keywords ──→ Detect: "regression", "slower", "failed"
    ↓
Extract Metrics ────→ Find: "API: 250ms", "Memory: 512MB"
    ↓
Compare Baseline ───→ Calculate: 250ms vs 200ms = +25%
    ↓
Categorize ─────────→ Regression / Improvement / Stable
    ↓
Generate Report
```

## Components

### 1. Skill (This Directory)
**File**: `~/.claude/skills/performance-testing/SKILL.md`

**Purpose**: Auto-activation and delegation

**Trigger Phrases**:
- "Run performance tests"
- "Check performance"
- "Run perf tests"
- "Test performance"

### 2. Sub-agent
**File**: `~/.claude/agents/perf-test-runner.md`

**Purpose**: Script discovery, execution, and analysis

**Capabilities**:
- Intelligent script search
- Real-time monitoring
- Keyword parsing
- Metric extraction
- Baseline comparison
- Report generation

### 3. Results Directory
**Location**: `.perf-results/` (created automatically)

**Contents**:
```
.perf-results/
├── 2025-10-23-145230.log       # Full test output
├── 2025-10-23-145230.json      # Parsed results
├── latest.json                  # Symlink to latest
├── baseline.json                # Current baseline
└── history.json                 # All run summaries
```

## Features

### Intelligent Script Discovery

**Common locations checked**:
1. `./run-performance-tests.sh`
2. `./scripts/run-performance-tests.sh`
3. `./test/performance/run-tests.sh`
4. `./perf-test.sh`

**Pattern search**:
- `*performance*.sh`
- `*perf*.sh`

**Exclusions**:
- `node_modules/`
- `.git/`
- `bin/`, `obj/`

**Multiple scripts handling**:
```
🔍 Found multiple performance test scripts:
1. ./run-performance-tests.sh
2. ./scripts/perf-test.sh
3. ./test/performance-suite.sh

Which script should I run? (Enter 1-3)
```

### Real-Time Monitoring

Tests run with live output:
```
📊 Running performance tests...
   Script: ./scripts/run-performance-tests.sh
   Started: 2025-10-23 14:52:30

Starting performance test suite...
[TEST 1] API endpoint response time... 245ms ✓
[TEST 2] Database query performance... 42ms ✓
[TEST 3] Memory usage under load... 505MB ✓
...
All tests completed successfully!

⏱️ Tests completed in 2m 34s
```

### Regression Detection

**Two methods**:

**1. Keyword Detection**

Searches output for:
- `regression`
- `slower`
- `degraded`
- `failed`
- `timeout`
- `error`

Example match:
```
[Output]: "Warning: API response time regression detected: 320ms vs 250ms baseline"

[Report]: ⚠️ Regression keyword detected in output:
         "Warning: API response time regression detected: 320ms vs 250ms baseline"
```

**2. Metric Comparison**

Extracts metrics and compares with baseline:

```
Metric: api_response_time_ms
Baseline: 250
Current: 320
Change: +70ms (+28%)
Threshold: 5%
Result: ⚠️ REGRESSION (exceeds threshold)
```

### Baseline Management

**First run** (no baseline exists):
```
ℹ️  No baseline found. Creating baseline from this run.

Baseline metrics:
• API response time: 245ms
• Database queries: 42ms
• Memory usage: 505MB

Future runs will be compared against this baseline.
```

**Subsequent runs** (baseline exists):
```
📈 Comparing with baseline from 2025-10-22...

Baseline date: 2025-10-22T10:30:00Z
Current date:  2025-10-23T14:52:30Z

Metrics compared: 12
Regressions: 2
Improvements: 3
Stable: 7
```

**Updating baseline**:
```
You: "Update the performance baseline"

Agent:
Updating baseline with latest results...

Old baseline: 2025-10-22-103045.json
New baseline: 2025-10-23-145230.json

✅ Baseline updated successfully
```

### Comprehensive Reporting

**Clean run** (no regressions):
```
📊 Performance Test Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Script:   ./run-performance-tests.sh
Duration: 1m 12s
Status:   ✅ ALL PASSING

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Metrics vs Baseline
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

All metrics stable (within 5% threshold):
• API response time: 245ms (vs 250ms, -2%)
• Database queries: 42ms (vs 45ms, -6%)
• Memory usage: 505MB (vs 512MB, -1%)
• Cache hit rate: 88% (vs 85%, +3%)

✅ SAFE TO MERGE - No performance regressions detected

Results saved: .perf-results/2025-10-23-145230.json
```

**Run with regressions**:
```
📊 Performance Test Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Script:   ./scripts/run-performance-tests.sh
Duration: 2m 45s
Status:   ⚠️ PASSED (with 3 regressions)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📉 Regressions Detected (3)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ Login endpoint response time
   Baseline: 180ms
   Current:  280ms
   Change:   +100ms (+55%) ⚠️ CRITICAL REGRESSION

⚠️ Search query latency
   Baseline: 95ms
   Current:  150ms
   Change:   +55ms (+58%) ⚠️ CRITICAL REGRESSION

⚠️ Memory usage under load
   Baseline: 450MB
   Current:  680MB
   Change:   +230MB (+51%) ⚠️ CRITICAL REGRESSION

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 Improvements (2)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Cache hit rate
   Baseline: 85%
   Current:  92%
   Change:   +7% (+8%)

✅ Database connection pool
   Baseline: 120ms
   Current:  95ms
   Change:   -25ms (-20%)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💾 Results Saved
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Full log: .perf-results/2025-10-23-145230.log
JSON:     .perf-results/2025-10-23-145230.json
Latest:   .perf-results/latest.json
Baseline: .perf-results/baseline.json

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ RECOMMENDATION: DO NOT MERGE

Critical performance regressions detected. Please investigate:
1. Recent code changes affecting login/search endpoints
2. Potential memory leak in application
3. Database query optimization opportunities
```

## Example Workflows

### Scenario 1: Clean Performance Check

```bash
# You made some changes and want to verify performance
git status
# M  src/UserService.cs
```

```
You: "Run performance tests"

Skill Output:
🔍 Found performance test script: ./run-performance-tests.sh

⚠️ Warning: You have uncommitted changes
   These changes may affect performance test results.
   Continuing anyway...

📊 Running performance tests...
   Started: 2025-10-23 14:52:30

[Real-time test output]

⏱️ Tests completed in 1m 18s

📈 Analyzing results...
   Comparing with baseline from 2025-10-22...

📊 Performance Test Results

Status: ✅ ALL PASSING

All metrics stable:
• API endpoints: 240-255ms (baseline range)
• Database queries: 40-48ms (baseline range)
• Memory usage: 500-515MB (baseline range)

✅ SAFE TO MERGE - No regressions detected

Results saved: .perf-results/2025-10-23-145230.json
```

### Scenario 2: Regression Detected

```
You: "Run performance tests"

Skill Output:
🔍 Found performance test script: ./scripts/run-performance-tests.sh

📊 Running performance tests...
   Started: 2025-10-23 15:30:00

[Test output shows some concerning numbers]

⏱️ Tests completed in 2m 34s

📈 Analyzing results...
   Comparing with baseline from 2025-10-22...

📊 Performance Test Results

Status: ⚠️ PASSED (with 2 regressions)

Regressions:
⚠️ API response time: 250ms → 380ms (+52%)
⚠️ Memory usage: 512MB → 720MB (+40%)

Improvements:
✅ Cache hit rate: 85% → 94% (+10%)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ RECOMMENDATION: Investigate before merging

Significant regressions detected. Check:
1. Recent changes to API endpoint handlers
2. Potential memory leak
3. Caching improvements may have memory trade-off

Results: .perf-results/2025-10-23-153000.json
```

**Next steps**:
```
You: "Show me the full performance test log"

Agent: Displays .perf-results/2025-10-23-153000.log

You: "What changed between baseline and now?"

Agent: Compares metrics in detail, suggests investigation areas
```

### Scenario 3: Multiple Scripts Found

```
You: "Run performance tests"

Skill Output:
🔍 Searching for performance test script...

Found multiple scripts:
1. ./run-performance-tests.sh (full suite)
2. ./scripts/quick-perf.sh (smoke tests)
3. ./test/perf/load-test.sh (load testing)

Which script should I run?
```

```
You: "Run the full suite (#1)"

Skill Output:
✅ Using: ./run-performance-tests.sh

📊 Running performance tests...
[continues with execution]
```

### Scenario 4: First Run (Creating Baseline)

```
You: "Run performance tests"

Skill Output:
🔍 Found performance test script: ./run-performance-tests.sh

📊 Running performance tests...
   Started: 2025-10-23 10:00:00

[Test output]

⏱️ Tests completed in 1m 45s

ℹ️  No baseline found. Creating baseline from this run.

Baseline metrics captured:
• API response time: 245ms
• Database queries: 42ms
• Memory usage: 505MB
• Cache hit rate: 88%
• Throughput: 1200 req/s

✅ Baseline created: .perf-results/baseline.json

Future runs will be compared against this baseline.
To update baseline later: "Update the performance baseline"

Results saved: .perf-results/2025-10-23-100000.json
```

## Configuration

### Required: Performance Test Script

Your project must have a performance test script. Common patterns:

**Bash script example**:
```bash
#!/bin/bash
# run-performance-tests.sh

echo "Starting performance test suite..."

# API endpoint test
response_time=$(curl -w "%{time_total}" -s -o /dev/null https://api.example.com/health)
echo "API response time: ${response_time}s"

# Database query test
db_time=$(measure_db_query_time)
echo "Database query: ${db_time}ms"

# Memory test
memory_usage=$(ps aux | grep myapp | awk '{print $6}')
echo "Memory usage: ${memory_usage}MB"

echo "All tests completed successfully!"
exit 0
```

**Output format** (for metric extraction):
```
Metric name: <value><unit>

Examples:
- "API response time: 245ms"
- "Database queries: 42ms"
- "Memory usage: 505MB"
- "Cache hit rate: 88%"
- "Throughput: 1200 req/s"
```

### Optional: Custom Configuration

Create `.perf-config.json` in project root:

```json
{
  "script": "./custom/path/to/perf-script.sh",
  "regressionThreshold": 10,
  "improvementThreshold": 5,
  "metrics": {
    "api_response_time": {
      "unit": "ms",
      "lowerIsBetter": true,
      "threshold": 5,
      "critical": 20
    },
    "memory_usage": {
      "unit": "MB",
      "lowerIsBetter": true,
      "threshold": 10,
      "critical": 25
    },
    "cache_hit_rate": {
      "unit": "%",
      "lowerIsBetter": false,
      "threshold": 3,
      "critical": 10
    }
  }
}
```

**Configuration options**:
- `script`: Path to performance test script
- `regressionThreshold`: Default threshold for regression detection (%)
- `improvementThreshold`: Default threshold for improvement detection (%)
- `metrics`: Per-metric configuration with custom thresholds

### Optional: .gitignore Entry

Add to `.gitignore`:
```
# Performance test results
.perf-results/
*.perf.log
```

## Troubleshooting

### Script Not Found

**Problem**: "No performance test script found"

**Solutions**:
1. Create a performance test script in your project
2. Name it with "performance" or "perf": `run-performance-tests.sh`
3. Place in common location: root, `./scripts/`, `./test/`
4. Make executable: `chmod +x run-performance-tests.sh`
5. Or specify path in `.perf-config.json`

### No Metrics Extracted

**Problem**: "No metrics extracted from test output"

**Causes**:
- Script doesn't output metrics in recognizable format
- Metrics use unsupported format

**Solutions**:
1. Update script to output metrics like: `"Metric: 123ms"`
2. Supported formats:
   - `Response time: 245ms`
   - `API: 1.5s`
   - `Memory: 512MB`
   - `Throughput: 1000 req/s`
   - `Cache hit rate: 88%`
3. Check `.perf-results/latest.log` to see actual output

### False Positives

**Problem**: Regressions reported but performance is actually fine

**Solutions**:
1. Check if baseline is stale: compare baseline date
2. Update baseline if needed: "Update the performance baseline"
3. Adjust threshold in `.perf-config.json`
4. Environment differences (local vs CI) can cause variance

### Tests Fail to Complete

**Problem**: Script hangs or fails

**Solutions**:
1. Check `.perf-results/latest.log` for errors
2. Run script manually: `./run-performance-tests.sh`
3. Ensure all dependencies are installed
4. Check for resource constraints (memory, CPU)

## Advanced Usage

### Trend Analysis

```
You: "Show performance trend over last 5 runs"

Agent:
📊 Performance Trend Analysis (Last 5 Runs)

API Response Time:
2025-10-19: 240ms ━━━━━━━━━━━━━━━━━━━━
2025-10-20: 245ms ━━━━━━━━━━━━━━━━━━━━━
2025-10-21: 250ms ━━━━━━━━━━━━━━━━━━━━━━
2025-10-22: 255ms ━━━━━━━━━━━━━━━━━━━━━━━
2025-10-23: 320ms ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ⚠️

Trend: Gradually increasing with spike today (+25% vs yesterday)

Memory Usage:
2025-10-19: 500MB ━━━━━━━━━━━━━━━━━━━━
2025-10-20: 505MB ━━━━━━━━━━━━━━━━━━━━
2025-10-21: 510MB ━━━━━━━━━━━━━━━━━━━━━
2025-10-22: 512MB ━━━━━━━━━━━━━━━━━━━━━
2025-10-23: 580MB ━━━━━━━━━━━━━━━━━━━━━━━━━ ⚠️

Trend: Steady increase, investigate potential leak
```

### Compare Specific Runs

```
You: "Compare performance results from Oct 20 and Oct 23"

Agent:
📊 Performance Comparison

Run 1: 2025-10-20-141500.json
Run 2: 2025-10-23-145230.json
Δ Time: 3 days

Metrics:
• API response time: 245ms → 320ms (+30%)
• Database queries: 44ms → 38ms (-13%)
• Memory usage: 505MB → 580MB (+14%)
• Cache hit rate: 86% → 92% (+6%)

Summary: 1 improvement, 2 regressions
```

### Update Baseline After Intentional Changes

```
You: "I optimized the database queries, update the baseline"

Agent:
📊 Running performance tests first...

[Runs tests]

✅ Tests completed - improvements detected!

Database queries: 45ms → 32ms (-28%) ✅

Updating baseline with these improvements...

Old baseline: 2025-10-22-103045.json
New baseline: 2025-10-23-160000.json

✅ Baseline updated. Future runs will compare against new optimized metrics.
```

### Run Without Baseline Comparison

```
You: "Run performance tests without comparing to baseline"

Agent:
📊 Running performance tests (no baseline comparison)...

[Runs tests, shows metrics without comparison]

Results:
• API response time: 245ms
• Database queries: 42ms
• Memory usage: 505MB

No baseline comparison performed.
Results saved: .perf-results/2025-10-23-145230.json
```

## Integration with Other Workflows

### With CodeRabbit Workflow

```
Workflow: Fix issues → Run perf tests → Verify no regressions → Push

You: "Address latest coderabbit issues on PR #123"
[CodeRabbit fixes applied]

You: "Run performance tests"
[Tests show no regressions]

You: "Safe to push"
```

### With CI/CD

Add to your CI pipeline:
```yaml
- name: Performance Tests
  run: |
    # Claude Code skill will handle this
    claude-code "run performance tests"

    # Or run script directly
    ./run-performance-tests.sh

    # Check results
    cat .perf-results/latest.json
```

### Pre-Merge Validation

```
You: "Before merging, run integration tests and performance tests"

Agent:
Running integration tests...
✅ Integration tests passed

Running performance tests...
✅ Performance tests passed (no regressions)

Safe to merge!
```

## File Locations

```
~/.claude/
├── agents/
│   └── perf-test-runner.md         # Sub-agent definition
└── skills/
    └── performance-testing/
        ├── SKILL.md                 # Skill activation logic
        └── README.md                # This file

Project directory:
.perf-results/                       # Results (gitignored)
├── 2025-10-23-145230.log           # Test output
├── 2025-10-23-145230.json          # Parsed results
├── latest.json                      # Latest run
├── baseline.json                    # Baseline metrics
└── history.json                     # All runs

.perf-config.json                    # Optional config
run-performance-tests.sh             # Your test script
```

## Best Practices

### 1. Consistent Test Environment

Run performance tests in consistent conditions:
- Same hardware
- Same load
- Same data set
- Same time of day (if testing production)

### 2. Regular Baseline Updates

Update baseline after:
- Intentional performance optimizations
- Infrastructure upgrades
- Significant feature changes

### 3. Trend Monitoring

Regularly review trends:
```
You: "Show performance trend over last month"
```

Catch gradual degradation early.

### 4. CI Integration

Run performance tests in CI:
- On every PR
- Before merging to main
- Nightly on main branch

### 5. Document Regressions

When regressions occur:
1. Document why regression is acceptable (if it is)
2. Create issue to optimize later
3. Update baseline if intentional trade-off

## Tips

- **Run tests before and after changes** to catch regressions early
- **Keep test scripts fast** (<5 minutes ideal)
- **Use realistic data** that represents production
- **Version your test scripts** along with code
- **Review trends regularly** to catch gradual degradation
- **Update baseline intentionally** when you make performance improvements

---

**Happy performance testing! 🚀📊**
