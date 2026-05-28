---
name: test-local-analysis
description: Run test_local.sh and analyze results including PNG outputs, execution logs, memory usage CSV, and performance metrics. Identifies issues like missing data points, memory spikes, or performance problems. Use after code changes to verify functionality.
allowed-tools: Bash, Read, Grep
---

# Test Local Analysis Skill

Run `test_local.sh` and perform comprehensive analysis of results.

## Step 1: Run test_local.sh

Execute the test script:
```bash
./test_local.sh
```

Capture:
- Exit code (must be 0 for success)
- Full stdout/stderr output
- Execution time

## Step 2: Analyze Test Output Log

Parse the console output to identify execution phases:

### Phase Detection Patterns

Look for these phase markers:
- `[PHASE @X.XXXs]` - Timestamped phase markers
- `Creating TercenStreamGenerator` - Data loading start
- `Cache HIT` / `Cache MISS` - Cache behavior (pagination)
- `Chunk X: Fetching rows Y-Z` - Data streaming progress
- `Rendering plot` - Render phase start
- `✓ Plot saved` - Success confirmation

### Phase Timing Analysis

Extract timing from phase markers:
1. **Initialization** - START to StreamGenerator creation
2. **Data Loading** - First chunk fetch to last chunk
3. **Rendering** - Render start to PNG saved
4. **Total** - START to completion

**Expected times** (475K rows, 2 pages):
- Page 1: ~2-4s per page (GPU) or 8-15s (CPU)
- Page 2: Should be faster with cache (30-50% speedup expected)

### Cache Behavior Analysis

For pagination tests (2 pages):

**Page 1 expectations**:
- All chunks show `Cache MISS - fetching and caching`
- Should see `Created disk cache at /tmp/ggrs_cache_*/`

**Page 2 expectations**:
- All chunks show `Cache HIT`
- NO fetching from Tercen
- Significantly faster (cache speedup)

**Red flags**:
- Cache MISS on page 2 → Cache broken
- No cache messages → Cache not created
- Cache errors → Disk/permission issues

### Error Detection

Search for error patterns:
- `error:` or `ERROR:` - Compilation/runtime errors
- `panic` - Rust panics
- `Failed to` - Operation failures
- `not found` - Missing resources
- Exit code != 0

## Step 3: Visual Analysis of PNG Outputs

Read generated PNG files:
- `plot.png` (single page) or
- `plot_1.png`, `plot_2.png` (multiple pages)

### Visual Inspection Checklist

**Plot Structure**:
- ✓ Facets arranged correctly (grid layout)
- ✓ Legend present and readable
- ✓ Axis labels visible
- ✓ No blank/empty panels (if data exists)

**Data Points**:
- ✓ Points visible and properly rendered
- ✓ Point density appears correct (~475K total for test data)
- ✓ Color mapping working (if using color aesthetic)
- ✓ No obvious missing data chunks

**Red flags**:
- Empty panels where data should exist
- Missing legend
- Garbled/corrupted image
- Extreme overplotting (all black) - might indicate duplicate rendering

### Compare Multiple Pages (Pagination Test)

If 2 pages generated:
- `plot_1.png` - Should show female data (facets 0-11)
- `plot_2.png` - Should show male data (facets 12-23)

**Verify**:
- Different data patterns between pages
- Both have similar point density (roughly equal male/female counts)
- No overlap in facet content

## Step 4: Memory Usage CSV Analysis

Read memory tracking CSV (e.g., `memory_usage_backend_cpu.csv`):

### CSV Structure
```csv
timestamp,memory_mb,label
0.000,45.2,Initialization
1.234,162.5,Loading Data
2.567,165.3,Rendering
...
```

### Memory Analysis

**Parse CSV**:
1. Extract all memory_mb values
2. Calculate: min, max, average, peak
3. Identify memory trend (stable, growing, spiking)

**Expected memory profiles**:

**GPU backend**:
- Baseline: ~50MB
- Peak during render: ~160-180MB
- Stable during streaming (no growth)

**CPU backend**:
- Baseline: ~30MB
- Peak during render: ~50-70MB
- Very stable (lower than GPU)

**Red flags**:
- Memory continuously growing → Memory leak
- Spikes > 300MB → Excessive buffering
- Large fluctuations → Inefficient chunk handling
- Not releasing memory after render → Cache not cleared

### Timing Analysis from CSV

Calculate phase durations:
1. Group by label (if CSV has phase labels)
2. Calculate time spent in each phase
3. Identify slow phases

**Red flags**:
- Single chunk taking >2s → Network issues
- Render phase >60s for 475K rows → Performance problem
- Total time >120s for 2 pages → Unexpected slowdown

## Step 5: Memory Chart Analysis

Read memory usage PNG (e.g., `memory_usage_backend_cpu.png`):

**Visual patterns to check**:
- Smooth curve (good) vs jagged spikes (bad)
- Memory returns to baseline after render (good)
- Flat line during streaming (good - not accumulating)
- Sharp spike then plateau (acceptable - allocation then stable)

**Red flags**:
- Staircase pattern (growing with each chunk → leak)
- Never returns to baseline (not cleaning up)
- Extreme spikes (>500MB)

## Step 6: Generate Report

Provide comprehensive summary:

### Success Criteria
- ✅ Exit code 0
- ✅ All phases completed
- ✅ PNG(s) generated successfully
- ✅ Visual inspection passed
- ✅ Memory within expected range
- ✅ Performance within expected time
- ✅ Cache working (if pagination)

### Example Report Format

```
## Test Results: PASS

### Execution Summary
- Exit code: 0 ✅
- Total time: 8.5s
- Backend: CPU
- Pages: 2

### Phase Timing
- Page 1: 4.2s (baseline)
- Page 2: 2.1s (50% faster with cache ✅)

### Cache Performance
- Page 1: 32 cache MISSes (expected)
- Page 2: 32 cache HITs (100% hit rate ✅)
- Speedup: 50% (expected 30-50%)

### Visual Analysis
- plot_1.png: ✅ All panels populated, legend visible
- plot_2.png: ✅ Different data pattern, no overlap

### Memory Profile
- Peak: 165MB (within expected 160-180MB for GPU)
- Baseline: 48MB
- Stable during streaming ✅
- No leaks detected ✅

### Issues Found
None - all checks passed!
```

### If Issues Found

List each issue with:
- **Severity**: Critical / Warning / Info
- **Phase**: Where it occurred
- **Description**: What's wrong
- **Evidence**: Log snippet, CSV values, or visual observation
- **Recommendation**: How to fix

### Example Issue Report

```
## Test Results: FAIL

### Issues Found

1. **CRITICAL - Cache Not Working**
   - Phase: Page 2 rendering
   - Evidence: All chunks show "Cache MISS" on page 2
   - Log: `✗ Cache MISS for chunk 1 (rows 0-15000) - fetching and caching`
   - Impact: No performance improvement (page 2 took 4.1s, same as page 1)
   - Recommendation: Check DataCache creation in main.rs

2. **WARNING - Memory Spike**
   - Phase: Rendering
   - Evidence: memory_usage_backend_gpu.csv shows peak of 324MB
   - Expected: ~160-180MB
   - Impact: 2x expected memory usage
   - Recommendation: Check for buffering or duplicate allocations

3. **INFO - Empty Panel**
   - Visual: plot_1.png panel (2,3) is blank
   - Expected: Should have data points
   - Possible cause: Data filtering issue or no data for that facet
   - Recommendation: Check facet indices and data distribution
```

## Step 7: Provide Actionable Next Steps

Based on findings, suggest:
- If all passed: "Ready for commit" or "Test with different data"
- If cache failed: "Review cache implementation in render.rs"
- If memory issue: "Profile memory usage with valgrind"
- If performance issue: "Check chunk size or network latency"
- If visual issue: "Inspect GGRS rendering or data filtering"

## Edge Cases

- If test_local.sh doesn't exist: Report and exit
- If no PNG generated: Critical failure, check logs for errors
- If CSV missing: Memory tracking disabled, skip memory analysis
- If test times out (>180s): Kill and report timeout
- If multiple backends tested: Analyze each separately
