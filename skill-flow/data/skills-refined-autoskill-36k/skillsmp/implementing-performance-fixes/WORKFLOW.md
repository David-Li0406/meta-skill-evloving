# Fix Implementation Workflow

Detailed procedures for implementing and validating performance fixes.

## Phase 1: Load Verified Theory

**Objective**: Understand the issue to fix

### Process

1. **Read PERFORMANCE_THEORIES.md**
   - Find theories with `Status: verified`
   - Select the highest-severity verified theory

2. **Extract theory details**
   - Root cause from verification evidence
   - Affected code locations (file:line)
   - Quantified impact (frequency, time%, allocations)
   - Tool evidence that proved the theory

3. **Read affected source files**
   - Understand current implementation
   - Identify modification points

### Output

- Theory to fix with full context
- Source code loaded and understood
- Clear problem statement

## Phase 2: Design Fix Approach

**Objective**: Determine the best fix strategy

### Process

1. **Evaluate fix options**

   For each potential fix, assess:
   - **Effectiveness**: Will it address the root cause?
   - **Scope**: How much code changes?
   - **Risk**: Could it break functionality or other optimizations?
   - **Complexity**: Implementation difficulty

2. **Consider architectural changes**

   Architectural changes are allowed when cost-benefit fits:

   **Good candidates for architectural change:**
   - Fix enables multiple optimizations
   - Current design fundamentally prevents optimization
   - Change improves code maintainability
   - Performance gain is substantial (>50% on affected benchmarks)

   **Poor candidates:**
   - Marginal gains (<10%)
   - High risk of regressions
   - Requires changes across many unrelated files
   - Unclear if it addresses root cause

3. **Select fix approach**

   Document:
   - Chosen approach
   - Why this approach over alternatives
   - Expected performance impact
   - Files to modify

## Phase 3: Implement Fix

**Objective**: Apply the fix to the codebase

### Process

1. **Create backup point**
   ```bash
   git stash  # or note current commit hash
   ```

2. **Apply changes**
   - Modify files according to fix design
   - Follow existing code conventions
   - Add comments explaining non-obvious optimizations

3. **Verify compilation**
   - Build the project
   - Fix any compilation errors
   - Ensure no new warnings

4. **Run basic sanity check**
   - Execute one benchmark to verify nothing is broken
   - Check output correctness

### Output

- Fix implemented
- Code compiles
- Basic functionality verified

## Phase 4: Validate with Relevant Benchmarks

**Objective**: Determine if fix improves performance

### Process

1. **Select 3 relevant benchmarks**

   From BENCHMARK_BASELINE.md:
   - Read each benchmark's **Rationale** field
   - Select benchmarks whose focus matches the fixed code path

   Example selection logic:
   - Theory fixed: "Missing specialization in arithmetic operations"
   - Select: benchmarks with rationale mentioning "arithmetic", "numeric", "computation"

2. **Run selected benchmarks**

   Use the execution commands from BENCHMARK_BASELINE.md:
   ```bash
   <language-launcher> <harness> <benchmark> <iterations> <inner-iterations>
   ```

3. **Compare results**

   | Benchmark | Baseline | After Fix | Change |
   |-----------|----------|-----------|--------|
   | bench1    | X ms     | Y ms      | Z%     |

4. **Evaluate outcome**

   **Performance Improved** (proceed to Phase 5a):
   - At least one benchmark shows >5% improvement
   - No benchmark shows >5% regression

   **Performance Degraded** (proceed to Phase 5b):
   - Any benchmark shows >5% regression without compensating improvement
   - Or all benchmarks show no change (fix ineffective)

## Phase 5a: Fix Successful - Finalize

**Objective**: Complete the fix, update all tracking files

### Process

1. **Run ALL benchmarks**
   - Execute every benchmark in BENCHMARK_BASELINE.md
   - Collect all timing data

2. **Update BENCHMARK_BASELINE.md**

   Add new column to results table:

   ```markdown
   ### Benchmarks Game Results

   | Benchmark | Date | Iterations | Total Time | Avg Time | After Fix #N |
   |-----------|------|------------|------------|----------|--------------|
   | fannkuch  | ... | 100 | 12.54s | 125.4ms | 98.2ms (-22%) |
   ```

3. **Update PERFORMANCE_THEORIES.md**

   Find the fixed theory and update:

   ```markdown
   ## Theory N: [Title]

   **Status**: fixed  <!-- was: verified -->
   **Fix Applied**: [Date]
   **Fix Description**: [What was changed]
   **Performance Impact**:
   - queens: -25% (32ms → 24ms)
   - nbody: -18% (150ms → 123ms)
   **Files Modified**:
   - `src/operations/ArithmeticOps.java`
   ```

### Output

- All benchmarks run with new results
- BENCHMARK_BASELINE.md updated with new column
- PERFORMANCE_THEORIES.md theory marked as `fixed`

## Phase 5b: Fix Failed - Revert

**Objective**: Revert changes, document failure

### Process

1. **Revert code changes**
   ```bash
   git checkout -- .  # or git stash pop
   ```

2. **Update PERFORMANCE_THEORIES.md**

   Find the theory and update:

   ```markdown
   ## Theory N: [Title]

   **Status**: fix-failed  <!-- was: verified -->
   **Fix Attempted**: [Date]
   **Attempted Fix**: [What was tried]
   **Reason for Failure**: [Why it didn't work]
   - bench1: +5% regression
   - bench2: no change
   **Next Steps**: [Alternative approaches to consider]
   ```

3. **Document learnings**
   - Why did the expected fix not work?
   - What does this reveal about the actual problem?
   - Should the theory be re-evaluated?

### Output

- Code reverted to pre-fix state
- PERFORMANCE_THEORIES.md theory marked as `fix-failed`
- Failure documented for future reference
