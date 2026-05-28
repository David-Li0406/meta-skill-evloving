---
name: objective
description: "Create an objective.json for goal-driven autonomous iteration. Use when you want to optimize toward a measurable target (performance, accuracy, coverage) rather than implement a specific PRD. Triggers on: create objective, optimize for, improve accuracy, reduce latency, increase coverage, goal-driven."
---

# Objective Mode Setup

Create a measurable objective for autonomous goal-driven iteration. Unlike PRD mode (which executes a known plan), Objective mode explores approaches autonomously until a target is reached or diminishing returns are detected.

---

## The Job

1. Ask clarifying questions to understand what the user wants to optimize
2. Propose a verification approach (how to measure success)
3. Propose stopping conditions (when to stop iterating)
4. Generate `objective.json` after user approval

**Important:** Do NOT start implementing. Just create the objective.json.

---

## Step 1: Clarifying Questions

Ask questions to understand the optimization goal. Use lettered options where appropriate.

### Question 1: Objective Type

```
What kind of objective are you trying to achieve?

A. Performance - Reduce latency, improve throughput, decrease resource usage
B. Accuracy - Improve model accuracy, reduce errors, increase precision
C. Coverage - Increase test coverage, documentation coverage, feature coverage
D. Quality - Reduce bugs, improve code quality metrics, decrease technical debt
E. Other: [please specify your optimization goal]
```

### Question 2: Target Component

```
What component or system are you optimizing?

A. A specific endpoint or API
B. A machine learning model
C. The test suite
D. A specific module or subsystem
E. The entire application
F. Other: [please specify]
```

### Question 3: Current State

```
What is your current baseline? (This helps set realistic targets)

Please provide:
- Current metric value (e.g., "78% accuracy", "450ms latency")
- How it's measured (e.g., "pytest --cov", "benchmark script")
- Any known issues (e.g., "fails on edge cases", "slow on large inputs")
```

This question requires a free-form answer to capture specifics.

### Question 4: Target Value

```
What is your target? Choose one:

A. Specific target value: [e.g., "90% accuracy", "under 100ms"]
B. Percentage improvement: [e.g., "50% faster", "20% fewer errors"]
C. Best achievable within constraints (let the agent explore)
D. Match a benchmark: [e.g., "match competitor X", "industry standard"]
```

### Question 5: Constraints

```
What constraints must be respected? Select all that apply:

A. Performance bounds (e.g., "must not exceed 200ms latency")
B. Resource limits (e.g., "model under 500MB", "no GPU required")
C. API compatibility (e.g., "cannot change public interfaces")
D. No external dependencies (e.g., "cannot add new libraries")
E. Budget limits (e.g., "no paid services", "under $X")
F. Other: [please specify]
G. No constraints
```

For each selected constraint, ask for specific values.

---

## Adapting Questions by Objective Type

### For Performance Objectives (A)

Additional questions:
```
What is the performance bottleneck?

A. CPU-bound computation
B. I/O operations (disk, network)
C. Memory usage
D. External API calls
E. Unknown - needs profiling first
```

```
How do you measure performance?

A. I have an existing benchmark script
B. Use standard tools (e.g., pytest-benchmark, time command)
C. Create a benchmark for me
D. Measure via application logs/metrics
```

### For Accuracy Objectives (B)

Additional questions:
```
What type of accuracy problem?

A. Classification accuracy (correct predictions)
B. Regression accuracy (prediction error)
C. Detection accuracy (finding all relevant items)
D. Ranking accuracy (correct ordering)
E. Other: [please specify]
```

```
What evaluation data do you have?

A. Labeled validation/test set
B. Historical data with known outcomes
C. A/B test capability
D. Manual review process
E. Need to create evaluation data
```

### For Coverage Objectives (C)

Additional questions:
```
What kind of coverage?

A. Code coverage (lines/branches tested)
B. Feature coverage (functionality tested)
C. Documentation coverage
D. API endpoint coverage
E. Other: [please specify]
```

```
Current coverage tooling:

A. pytest-cov / coverage.py
B. jest --coverage
C. Other tool: [specify]
D. No coverage tool set up
```

### For Quality Objectives (D)

Additional questions:
```
What quality metrics matter most?

A. Bug count / error rate
B. Linting violations
C. Type coverage
D. Cyclomatic complexity
E. Technical debt score
F. Other: [please specify]
```

---

## Step 2: Verification Approach

Based on the answers, propose how success will be measured. **Adapt your proposals based on the objective type from Step 1.**

### Type-Specific Verification Commands

Propose a verification command tailored to the objective type:

#### For Performance Objectives (Type A)

```markdown
## Proposed Verification

**Command:** `python scripts/benchmark_performance.py --endpoint [endpoint] --iterations 100`

This command will:
- Run [N] iterations of the target operation
- Measure: latency (p50, p95, p99), throughput (req/sec), memory usage
- Output JSON metrics for tracking

**Does this benchmark script exist?**
A. Yes, I have an existing benchmark at: [path]
B. No, please create a benchmark script for me (Recommended)
C. I'll use a standard tool (pytest-benchmark, hyperfine, wrk)
D. I need to modify an existing script: [path]
```

#### For Accuracy Objectives (Type B)

```markdown
## Proposed Verification

**Command:** `python scripts/evaluate_model.py --dataset validation --output-json`

This command will:
- Load the model and validation dataset
- Run predictions on [N] samples
- Calculate: accuracy, precision, recall, F1-score
- Output JSON metrics for tracking

**Does this evaluation script exist?**
A. Yes, I have an existing evaluation at: [path]
B. No, please create an evaluation script for me (Recommended)
C. I'll use a standard tool (sklearn metrics, pytest with assertions)
D. I need to modify an existing script: [path]
```

#### For Coverage Objectives (Type C)

```markdown
## Proposed Verification

**Command:** `pytest --cov=[source_dir] --cov-report=json --cov-report=term`

This command will:
- Run the test suite with coverage tracking
- Measure: line coverage, branch coverage, missing lines
- Output coverage.json for metric extraction

**Is your coverage tooling configured?**
A. Yes, pytest-cov is set up and working
B. No, please help me set up coverage (Recommended)
C. I use a different coverage tool: [specify]
D. I need to configure coverage for specific modules
```

#### For Quality Objectives (Type D)

```markdown
## Proposed Verification

**Command:** `./scripts/quality_metrics.sh`

This script will aggregate:
- Linting violations (ruff, eslint)
- Type coverage (pyright, tsc)
- Complexity metrics (radon, complexity-report)

**Do you have quality metric tooling?**
A. Yes, I have existing quality scripts at: [path]
B. No, please create a quality metrics script for me (Recommended)
C. I want to use specific tools: [list tools]
D. I only care about: [specific metric]
```

### Offer to Create Benchmark Scripts

If user selects "create for me" (option B), acknowledge this:

```markdown
**Benchmark Creation Plan:**

I'll create `scripts/benchmark_[type].py` that:
1. [Specific action for this objective type]
2. Outputs JSON with metrics: [list metrics]
3. Can be run with: `python scripts/benchmark_[type].py`

This will be created as part of the first iteration.

Proceed with benchmark creation? (yes/adjust/no)
```

### Propose Success Criteria

Based on the objective type and target value from Step 1:

```markdown
**Success Criteria:** `[metric] [operator] [value]`

```

Type-specific examples:
- **Performance:** `latency_p99 < 100` (milliseconds)
- **Accuracy:** `accuracy >= 0.90` (0-1 scale)
- **Coverage:** `line_coverage >= 80` (percentage)
- **Quality:** `linting_violations < 10` (count)

```markdown
Is this target realistic based on your current state?

A. Yes, this target is achievable
B. Too aggressive - adjust to: [suggest lower target]
C. Too conservative - adjust to: [suggest higher target]
D. I want a different metric entirely: [specify]
```

### Propose Metrics to Track

Propose metrics relevant to the objective type. The primary metric must match the success criteria.

#### Performance Metrics (Type A)
```markdown
**Recommended Metrics to Track:**
1. `latency_p99` (primary) - 99th percentile response time
2. `latency_p50` - Median response time
3. `throughput` - Requests per second
4. `memory_mb` - Peak memory usage

Add, remove, or reorder? (List changes or 'OK')
```

#### Accuracy Metrics (Type B)
```markdown
**Recommended Metrics to Track:**
1. `accuracy` (primary) - Overall correct predictions
2. `precision` - True positives / predicted positives
3. `recall` - True positives / actual positives
4. `f1_score` - Harmonic mean of precision and recall

Add, remove, or reorder? (List changes or 'OK')
```

#### Coverage Metrics (Type C)
```markdown
**Recommended Metrics to Track:**
1. `line_coverage` (primary) - Percentage of lines covered
2. `branch_coverage` - Percentage of branches covered
3. `missing_lines` - Count of uncovered lines
4. `files_covered` - Number of files with any coverage

Add, remove, or reorder? (List changes or 'OK')
```

#### Quality Metrics (Type D)
```markdown
**Recommended Metrics to Track:**
1. `linting_violations` (primary) - Total lint errors
2. `type_coverage` - Percentage of typed code
3. `cyclomatic_complexity` - Average function complexity
4. `tech_debt_hours` - Estimated remediation time

Add, remove, or reorder? (List changes or 'OK')
```

### User Adjustment Summary

After proposing verification approach, present a summary the user can adjust:

```markdown
## Verification Proposal Summary

| Aspect | Proposed Value | Adjust? |
|--------|---------------|---------|
| Command | `[command]` | A. Keep / B. Change to: ___ |
| Create benchmark? | [Yes/No] | A. Keep / B. Change |
| Success criteria | `[expression]` | A. Keep / B. Change to: ___ |
| Metrics to track | [list] | A. Keep / B. Add: ___ / C. Remove: ___ |

Enter adjustments (e.g., "B. Change command to pytest") or 'OK' to proceed to Step 3.
```

---

## Step 3: Stopping Conditions

Propose when the loop should stop. **Adapt defaults based on objective type from Step 1.**

### Type-Specific maxIterations Defaults

Choose the default based on objective complexity:

| Objective Type | Default maxIterations | Rationale |
|----------------|----------------------|-----------|
| **Performance (A)** | 12 iterations | Profiling + incremental optimizations, medium exploration |
| **Accuracy (B)** | 15 iterations | ML tuning needs more exploration, hyperparameter space |
| **Coverage (C)** | 10 iterations | Test writing is fairly predictable, lower variance |
| **Quality (D)** | 10 iterations | Refactoring is incremental, bounded scope |
| **Other/Complex** | 15 iterations | Unknown territory, allow more exploration |

### Proposing Stopping Conditions

Present the proposal with type-specific defaults filled in:

```markdown
## Proposed Stopping Conditions

### 1. Maximum Iterations
**Proposed:** [N] iterations (based on [objective type] objectives)

This is your iteration budget. The loop will stop after this many attempts,
regardless of whether the objective is achieved.

```
Adjust max iterations?

A. Keep [N] iterations (Recommended for [type] objectives)
B. Fewer: 8 iterations (faster, less exploration)
C. More: 20 iterations (thorough, more exploration)
D. Custom: [enter number]
```

### 2. Plateau Detection
Stops the loop when progress stagnates - no need to keep trying if we're stuck.

**Proposed settings:**
- **Metric to watch:** `[primary metric from success criteria]`
- **Minimum improvement:** 0.01 (1% change required between iterations)
- **Window size:** 3 iterations (check improvement over last 3 attempts)

**How it works:** If `[metric]` improves by less than 1% across 3 consecutive
iterations, the loop stops with a "plateau" status.

```
Adjust plateau detection?

A. Keep defaults (Recommended)
B. More sensitive: minImprovement=0.02, windowSize=2 (stop sooner if stuck)
C. Less sensitive: minImprovement=0.005, windowSize=5 (allow more experimentation)
D. Custom: minImprovement=[value], windowSize=[value]
E. Disable plateau detection (only stop on success or max iterations)
```

### 3. Consecutive Failures
Safety stop for experiments that are completely broken (not just not improving).

**Proposed:** 3 consecutive failures

A "failure" means the iteration couldn't produce valid metrics at all
(crashed, timed out, broke constraints).

```
Adjust consecutive failures limit?

A. Keep 3 failures (Recommended)
B. Stricter: 2 failures (fail fast)
C. Lenient: 5 failures (allow more retries for flaky systems)
D. Custom: [enter number]
```
```

### Stopping Conditions Summary Table

After getting user responses, present a summary:

```markdown
## Stopping Conditions Summary

| Parameter | Value | Meaning |
|-----------|-------|---------|
| Max Iterations | [N] | Stop after [N] attempts maximum |
| Plateau Metric | `[metric]` | Watch this metric for stagnation |
| Min Improvement | [value] | Require at least [value*100]% improvement |
| Window Size | [N] | Check improvement over last [N] iterations |
| Max Failures | [N] | Stop after [N] consecutive broken iterations |

**Estimated behavior:**
- Best case: Objective achieved in ~[N/3] iterations
- Typical case: Plateau detected around iteration [N*0.6]
- Worst case: Loop runs all [N] iterations

Confirm these settings? (yes/adjust/explain more)
```

### Explaining Parameters in Plain Language

Always include this explanation with the initial proposal:

```markdown
**What these mean (in plain language):**

📊 **Max Iterations** = Your budget
   Think of each iteration as one attempt to improve. This is the maximum
   number of attempts before giving up. More iterations = more chances to
   find improvements, but also more time/resources.

📈 **Plateau Detection** = "Are we stuck?"
   If the metric barely changes for several attempts in a row, we're probably
   stuck and should stop. The window size is how many attempts to look back,
   and min improvement is how much change counts as "real progress."

   Example: With windowSize=3 and minImprovement=0.01, if accuracy goes from
   0.85 → 0.851 → 0.852 over 3 iterations, that's a plateau (only 0.002 total
   improvement, less than 0.01).

❌ **Consecutive Failures** = "Is something broken?"
   Different from plateau. A failure means the experiment completely broke
   (couldn't even measure the metric). 3 failures in a row suggests
   something fundamental is wrong, not just slow progress.
```

### Handling User Adjustments

If user provides adjustments (e.g., "B, C, A"):

1. Parse each response to the corresponding parameter
2. Apply the changes
3. Re-present the summary table with updated values
4. Confirm again

If user asks "explain more", provide the plain language explanation above.

---

## Step 4: Generate objective.json

**CRITICAL:** Present the complete plan and wait for user approval BEFORE writing any files. Do NOT create objective.json until the user explicitly approves.

### Present the Complete Plan Summary

```markdown
## Complete Plan Summary

**Objective:** [description from Step 1]
**Target:** [success criteria from Step 2]
**Verification:** `[command from Step 2]`

**Constraints:**
- [constraint 1]
- [constraint 2]
- (or "None specified" if no constraints)

**Stopping Conditions:**
- Max iterations: [N]
- Plateau: [metric] improving < [threshold] over [window] iterations
- Max consecutive failures: [N]

**Metrics to track:** [list from Step 2]

---

Ready to create objective.json? (yes/no/adjust)
```

### Handling User Responses

**On "adjust" or similar ("change", "modify", "fix"):**
```
What would you like to adjust?

A. Objective description or constraints
B. Verification command or success criteria
C. Stopping conditions (iterations, plateau, failures)
D. Metrics to track

Enter your choice, or describe what you want to change:
```

After user specifies adjustments:
1. Make the requested changes
2. Re-present the Complete Plan Summary
3. Ask for approval again

**On "no" or similar ("cancel", "stop", "never mind"):**
```
Objective creation cancelled. No files were created.

You can restart with /objective when you're ready.
```

**On explicit approval - ONLY these trigger file creation:**
- "yes", "y"
- "create it", "create"
- "generate", "generate it"
- "do it", "go ahead"
- "looks good", "lgtm"
- "approved", "approve"

Any other response should be treated as a request for adjustment or clarification.

### Write objective.json After Approval

Only after receiving explicit approval, write the file to project root:

```json
{
  "objective": {
    "description": "[from answers]",
    "context": "[current state and known issues]",
    "constraints": [
      "[constraint 1]",
      "[constraint 2]"
    ]
  },
  "verification": {
    "command": "[verification command]",
    "successCriteria": "[metric expression]",
    "metricsToTrack": ["metric1", "metric2", "metric3"]
  },
  "stopping": {
    "maxIterations": [N],
    "plateauThreshold": {
      "metric": "[primary metric]",
      "minImprovement": 0.01,
      "windowSize": 3
    },
    "maxConsecutiveFailures": 3
  },
  "status": {
    "state": "pending",
    "iterations": 0,
    "bestMetrics": {},
    "metricHistory": []
  }
}
```

---

## After Approval

Print confirmation and next steps in this EXACT format:

```
✅ objective.json created successfully!

Next steps:
1. Review the generated objective.json
2. Ensure the verification command works: [command]
3. To start: ./angainor.sh --objective

The agent will iterate autonomously, trying different approaches until:
- ✓ Success criteria are met
- ⏸ Progress plateaus (no improvement in consecutive iterations)
- ⏱ Max iterations reached
- ✗ The objective is determined impossible
```

**Note:** The `./angainor.sh --objective` command uses the maxIterations from the objective.json by default. Users can override with: `./angainor.sh --objective 20`

---

## Benchmark Script Creation

When the user selects "Create a benchmark for me" (option B) in Step 2, you MUST create a benchmark script. This section provides templates for common objective types.

**IMPORTANT:** Create benchmark scripts in `scripts/` directory with descriptive names. Scripts must:
1. Be executable (include shebang `#!/usr/bin/env python3`)
2. Output JSON to stdout with metrics matching `metricsToTrack`
3. Accept command-line arguments for configuration
4. Handle errors gracefully and return non-zero exit code on failure

### API Latency Benchmark Template (Performance)

Create `scripts/benchmark_latency.py`:

```python
#!/usr/bin/env python3
"""
API Latency Benchmark - Measures endpoint performance.
Outputs JSON metrics for Angainor objective tracking.

Usage: python scripts/benchmark_latency.py --url URL [--iterations N]
"""

import argparse
import json
import statistics
import sys
import time
import urllib.request
import urllib.error


def measure_latency(url: str, iterations: int = 100) -> dict:
    """Measure latency statistics for a URL."""
    latencies = []
    errors = 0

    for i in range(iterations):
        start = time.perf_counter()
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                _ = response.read()
            latency_ms = (time.perf_counter() - start) * 1000
            latencies.append(latency_ms)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
            errors += 1
            sys.stderr.write(f"Request {i+1} failed: {e}\n")

    if not latencies:
        return {"error": "All requests failed", "success_rate": 0}

    latencies.sort()
    n = len(latencies)

    return {
        "latency_p50": round(latencies[int(n * 0.50)], 2),
        "latency_p95": round(latencies[int(n * 0.95)], 2),
        "latency_p99": round(latencies[int(n * 0.99)], 2),
        "latency_avg": round(statistics.mean(latencies), 2),
        "throughput": round(n / (sum(latencies) / 1000), 2),
        "success_rate": round((iterations - errors) / iterations, 3),
        "iterations": iterations
    }


def main():
    parser = argparse.ArgumentParser(description="Measure API endpoint latency")
    parser.add_argument("--url", required=True, help="URL to benchmark")
    parser.add_argument("--iterations", type=int, default=100, help="Number of requests")
    args = parser.parse_args()

    metrics = measure_latency(args.url, args.iterations)

    if "error" in metrics:
        print(json.dumps(metrics), file=sys.stderr)
        sys.exit(1)

    print(json.dumps(metrics))


if __name__ == "__main__":
    main()
```

**Verification command for objective.json:**
```
python scripts/benchmark_latency.py --url http://localhost:3000/api/endpoint --iterations 100
```

### Model Accuracy Benchmark Template (Accuracy)

Create `scripts/benchmark_accuracy.py`:

```python
#!/usr/bin/env python3
"""
Model Accuracy Benchmark - Evaluates model predictions against ground truth.
Outputs JSON metrics for Angainor objective tracking.

Usage: python scripts/benchmark_accuracy.py --model MODEL_PATH --data DATA_PATH
"""

import argparse
import json
import sys
from pathlib import Path


def calculate_metrics(predictions: list, ground_truth: list) -> dict:
    """Calculate classification metrics."""
    if len(predictions) != len(ground_truth):
        raise ValueError("Predictions and ground truth must have same length")

    n = len(predictions)
    if n == 0:
        return {"error": "No samples to evaluate"}

    # Calculate basic metrics
    correct = sum(1 for p, g in zip(predictions, ground_truth) if p == g)
    accuracy = correct / n

    # For binary classification, calculate precision/recall
    # Assumes positive class is 1 or True
    tp = sum(1 for p, g in zip(predictions, ground_truth) if p == 1 and g == 1)
    fp = sum(1 for p, g in zip(predictions, ground_truth) if p == 1 and g == 0)
    fn = sum(1 for p, g in zip(predictions, ground_truth) if p == 0 and g == 1)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    return {
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1_score, 4),
        "samples": n,
        "correct": correct
    }


def load_data(path: str) -> tuple:
    """Load predictions and ground truth from JSON file."""
    data = json.loads(Path(path).read_text())
    return data.get("predictions", []), data.get("ground_truth", [])


def main():
    parser = argparse.ArgumentParser(description="Evaluate model accuracy")
    parser.add_argument("--data", required=True, help="Path to JSON with predictions and ground_truth")
    parser.add_argument("--predictions-key", default="predictions", help="Key for predictions in JSON")
    parser.add_argument("--ground-truth-key", default="ground_truth", help="Key for ground truth in JSON")
    args = parser.parse_args()

    try:
        data = json.loads(Path(args.data).read_text())
        predictions = data.get(args.predictions_key, [])
        ground_truth = data.get(args.ground_truth_key, [])

        metrics = calculate_metrics(predictions, ground_truth)

        if "error" in metrics:
            print(json.dumps(metrics), file=sys.stderr)
            sys.exit(1)

        print(json.dumps(metrics))

    except FileNotFoundError:
        print(json.dumps({"error": f"Data file not found: {args.data}"}), file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON: {e}"}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
```

**Verification command for objective.json:**
```
python scripts/benchmark_accuracy.py --data data/validation_results.json
```

### Test Coverage Benchmark Template (Coverage)

Create `scripts/benchmark_coverage.py`:

```python
#!/usr/bin/env python3
"""
Test Coverage Benchmark - Parses coverage.json and outputs metrics.
Outputs JSON metrics for Angainor objective tracking.

Usage: python scripts/benchmark_coverage.py [--coverage-file PATH]

Requires: Run pytest with coverage first:
  pytest --cov=src --cov-report=json
"""

import argparse
import json
import sys
from pathlib import Path


def parse_coverage(coverage_path: str = "coverage.json") -> dict:
    """Parse coverage.json and extract metrics."""
    path = Path(coverage_path)

    if not path.exists():
        return {"error": f"Coverage file not found: {coverage_path}. Run pytest --cov first."}

    data = json.loads(path.read_text())

    totals = data.get("totals", {})
    files = data.get("files", {})

    # Calculate metrics
    line_coverage = totals.get("percent_covered", 0)
    covered_lines = totals.get("covered_lines", 0)
    missing_lines = totals.get("missing_lines", 0)
    total_lines = covered_lines + missing_lines

    # Branch coverage (if available)
    branch_coverage = totals.get("percent_covered_branches", 0) if "covered_branches" in totals else None

    # Files with coverage
    files_with_coverage = sum(1 for f in files.values() if f.get("summary", {}).get("percent_covered", 0) > 0)
    total_files = len(files)

    metrics = {
        "line_coverage": round(line_coverage, 2),
        "covered_lines": covered_lines,
        "missing_lines": missing_lines,
        "total_lines": total_lines,
        "files_covered": files_with_coverage,
        "total_files": total_files
    }

    if branch_coverage is not None:
        metrics["branch_coverage"] = round(branch_coverage, 2)

    return metrics


def main():
    parser = argparse.ArgumentParser(description="Parse test coverage metrics")
    parser.add_argument("--coverage-file", default="coverage.json", help="Path to coverage.json")
    args = parser.parse_args()

    metrics = parse_coverage(args.coverage_file)

    if "error" in metrics:
        print(json.dumps(metrics), file=sys.stderr)
        sys.exit(1)

    print(json.dumps(metrics))


if __name__ == "__main__":
    main()
```

**Verification command for objective.json:**
```
pytest --cov=src --cov-report=json && python scripts/benchmark_coverage.py
```

### Benchmark Creation Workflow

When creating a benchmark script:

1. **Determine the benchmark type** based on objective type from Step 1:
   - Performance (A) → `scripts/benchmark_latency.py`
   - Accuracy (B) → `scripts/benchmark_accuracy.py`
   - Coverage (C) → `scripts/benchmark_coverage.py`
   - Quality (D) → Use existing tools (ruff, pylint), no script needed

2. **Use the template above** as a starting point, customizing:
   - Command-line arguments for the specific use case
   - Metric names to match `metricsToTrack` in objective.json
   - Input data paths or URLs for the specific project

3. **Create the script** in `scripts/` directory:
   ```
   Write the script to: scripts/benchmark_[type].py
   Make it executable: chmod +x scripts/benchmark_[type].py
   ```

4. **Verify it works** before finalizing objective.json:
   ```
   Run: python scripts/benchmark_[type].py --help
   Test: python scripts/benchmark_[type].py [args]
   ```

5. **Update objective.json** with the correct verification command.

**After creating the benchmark:**
```
✅ Benchmark script created: scripts/benchmark_[type].py

The script outputs JSON metrics including: [list metrics]

Test the script:
  python scripts/benchmark_[type].py --help
  python scripts/benchmark_[type].py [example args]
```

---

## Checklist

Before saving objective.json:

- [ ] Asked about objective type, target, constraints
- [ ] Adapted follow-up questions based on objective type
- [ ] Proposed verification command (create if needed)
- [ ] If user selected "create benchmark for me": created executable script in `scripts/`
- [ ] Proposed realistic success criteria
- [ ] Proposed sensible stopping conditions
- [ ] Got explicit user approval
- [ ] Wrote objective.json with all fields populated
- [ ] Printed next steps
