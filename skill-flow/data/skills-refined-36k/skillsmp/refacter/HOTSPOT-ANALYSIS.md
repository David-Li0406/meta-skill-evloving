# Hotspot Analysis

Identify high-risk code areas using code churn + complexity analysis.

**Principle**: Code that changes frequently AND is complex → highest risk for bugs.

**Source**: "Your Code as a Crime Scene" by Adam Tornhill

---

## What is a Hotspot?

**Definition**: A file or function with BOTH:
1. **High Code Churn**: Changed frequently (many commits)
2. **High Complexity**: Cyclomatic complexity > 10

**Why Hotspots Matter:**
- 🐛 Most bugs occur in hotspots (research: 4-5x more bugs than other code)
- ⏱️ Highest maintenance cost (complex + constantly changing)
- 🎯 Best ROI for refactoring (fix once, benefit repeatedly)

---

## The Hotspot Matrix

```
         │ Low Complexity  │ High Complexity
─────────┼─────────────────┼──────────────────
High     │  P1 Monitor     │  P0 CRITICAL
Churn    │  (Add tests)    │  (Refactor NOW)
─────────┼─────────────────┼──────────────────
Low      │  P3 Ignore      │  P2 Tech Debt
Churn    │  (Stable code)  │  (Refactor later)
```

### Priority Levels

**P0 - Critical Hotspots** (High Churn + High Complexity)
- **Risk**: Very High (bugs likely, hard to fix)
- **Action**: Immediate refactoring
- **Example**: `workflow_nodes.py` changed 45 times, CC = 15

**P1 - Monitor** (High Churn + Low Complexity)
- **Risk**: Medium (might become complex)
- **Action**: Add tests, watch complexity
- **Example**: `api.py` changed 30 times, CC = 5

**P2 - Technical Debt** (Low Churn + High Complexity)
- **Risk**: Medium (complex but stable)
- **Action**: Refactor when you need to change it
- **Example**: `legacy_parser.py` changed 2 times, CC = 20

**P3 - Stable Code** (Low Churn + Low Complexity)
- **Risk**: Low
- **Action**: No action needed
- **Example**: `utils.py` changed 3 times, CC = 4

---

## Code Churn Metrics

### What is Code Churn?

**Definition**: Number of times a file has been modified in git history.

```bash
# Count commits touching a file (last 6 months)
git log --since="6 months ago" --oneline --follow src/workflow/workflow_nodes.py | wc -l

# Output: 45 commits → High churn
```

### Churn Thresholds

| Commits (6 months) | Rating | Interpretation |
|--------------------|--------|----------------|
| 1-5 | Low | Stable, rarely changes |
| 6-15 | Moderate | Normal activity |
| 16-30 | High | Frequent changes |
| 31+ | Very High | Hotspot candidate |

---

## Identifying Hotspots

### Using analyze_hotspots.py Script

```bash
# Analyze hotspots (last 6 months)
python .claude/skills/refacter/scripts/analyze_hotspots.py src/

# Custom time range
python .claude/skills/refacter/scripts/analyze_hotspots.py src/ --since "3 months ago"

# Show top 10 hotspots
python .claude/skills/refacter/scripts/analyze_hotspots.py src/ --top 10

# JSON output for dashboards
python .claude/skills/refacter/scripts/analyze_hotspots.py src/ --json > hotspots.json
```

### Example Output

```
====================================================
HOTSPOT ANALYSIS (Last 6 Months)
====================================================

P0 - CRITICAL HOTSPOTS (High Churn + High Complexity):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🔥 src/workflow/workflow_nodes.py
     Commits: 45 | Avg CC: 12.3 | Max CC: 18
     Top complex functions:
       • score_report (line 248) - CC: 18
       • generate_report (line 192) - CC: 11
     🚨 Action: PRIORITY REFACTOR

  🔥 src/agent/ticker_analysis.py
     Commits: 38 | Avg CC: 10.8 | Max CC: 15
     Top complex functions:
       • analyze_ticker (line 67) - CC: 15
     🚨 Action: Extract method, add tests


P1 - MONITOR (High Churn + Low Complexity):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ⚠️  src/api/telegram_api.py
     Commits: 32 | Avg CC: 4.2 | Max CC: 7
     Action: Add integration tests, monitor complexity


P2 - TECHNICAL DEBT (Low Churn + High Complexity):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📝 src/data/news_fetcher.py
     Commits: 4 | Avg CC: 14.5 | Max CC: 17
     Action: Refactor when modifying


Summary:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Total Files Analyzed: 47
  P0 Critical: 2 files (4.3%)
  P1 Monitor: 1 file (2.1%)
  P2 Tech Debt: 1 file (2.1%)
  P3 Stable: 43 files (91.5%)

Recommendations:
  🔥 URGENT: Refactor workflow_nodes.py (45 commits, CC 18)
  🔥 URGENT: Refactor ticker_analysis.py (38 commits, CC 15)
  ⚠️  Add tests to telegram_api.py before complexity increases
```

---

## Manual Hotspot Analysis

### Step 1: Identify High Churn Files

```bash
# Top 10 most changed files (last 6 months)
git log --since="6 months ago" --pretty=format: --name-only src/ \
  | sort | uniq -c | sort -rn | head -10

# Example output:
#  45 src/workflow/workflow_nodes.py
#  38 src/agent/ticker_analysis.py
#  32 src/api/telegram_api.py
#  28 src/data/news_fetcher.py
```

### Step 2: Measure Complexity

```bash
# Check complexity of high-churn files
radon cc src/workflow/workflow_nodes.py -a --min B
radon cc src/agent/ticker_analysis.py -a --min B
```

### Step 3: Cross-Reference

| File | Commits | Max CC | Priority | Action |
|------|---------|--------|----------|--------|
| workflow_nodes.py | 45 | 18 | **P0** | Refactor NOW |
| ticker_analysis.py | 38 | 15 | **P0** | Refactor NOW |
| telegram_api.py | 32 | 7 | P1 | Add tests |
| news_fetcher.py | 28 | 17 | P0 | Refactor NOW |

---

## Visualizing Hotspots

### ASCII Heatmap

```
Complexity (CC) →
          5    10   15   20   25
Churn ┌────┬────┬────┬────┬────┐
  5   │ OK │ OK │ P2 │ P2 │ P2 │
─────┼────┼────┼────┼────┼────┤
 15   │ P1 │ P1 │ P0 │ P0 │ P0 │
─────┼────┼────┼────┼────┼────┤
 30   │ P1 │ P1 │ P0 │ P0 │ P0 │ ← High churn
─────┼────┼────┼────┼────┼────┤
 45   │ P1 │ P0 │ P0 │ P0 │ P0 │ ← Very high churn
     └────┴────┴────┴────┴────┘
           Low  Med  High Very  Extreme
                Complexity →
```

**Reading the heatmap:**
- **P0 (Red zone)**: Urgent refactoring needed
- **P1 (Yellow zone)**: Monitor and add tests
- **P2 (Blue zone)**: Technical debt (refactor when touching)
- **OK (Green zone)**: Healthy code

---

## Refactoring Hotspots

### Strategy: Incremental Improvement

**DO NOT**: Rewrite entire hotspot file in one go (high risk)

**DO**: Refactor incrementally with tests

```
1. Add characterization tests (lock current behavior)
2. Extract one complex method
3. Run tests
4. Commit
5. Repeat until complexity acceptable
```

### Example: Refactoring workflow_nodes.py

```python
# BEFORE: Hotspot (45 commits, CC 18)
class WorkflowNodes:
    def score_report(self, state: AgentState) -> AgentState:
        # 78 lines, cyclomatic complexity 18
        # Complex nested conditionals...
        ...

# STEP 1: Add tests
def test_score_report_happy_path():
    state = {...}
    result = workflow.score_report(state)
    assert result['faithfulness_score']['score'] > 0

# STEP 2: Extract one method
class WorkflowNodes:
    def score_report(self, state: AgentState) -> AgentState:
        # 60 lines, cyclomatic complexity 14 (-4!)
        faithfulness = self._score_faithfulness(state)  # Extracted
        completeness = self._score_completeness(state)
        ...

    def _score_faithfulness(self, state: AgentState) -> dict:
        # 15 lines, cyclomatic complexity 4
        # Extracted logic...

# STEP 3: Commit
git add src/workflow/workflow_nodes.py tests/test_workflow.py
git commit -m "refactor: Extract _score_faithfulness from score_report

Reduces cyclomatic complexity from 18 → 14.
Improves testability (can test faithfulness scoring separately)."

# STEP 4: Repeat for other methods
```

---

## Temporal Coupling Analysis

**Principle**: Files that change together often → hidden dependencies.

### Detecting Temporal Coupling

```bash
# Find files that changed together (last 6 months)
git log --since="6 months ago" --pretty=format: --name-only \
  | grep -v '^$' \
  | awk 'NR%2{file=$0; next} {print file, $0}' \
  | sort | uniq -c | sort -rn | head -20

# Example output:
#  18 src/workflow/workflow_nodes.py src/agent/ticker_analysis.py
#  12 src/api/telegram_api.py src/workflow/workflow_nodes.py
```

**Interpretation:**
- `workflow_nodes.py` and `ticker_analysis.py` changed together 18 times
- Strong temporal coupling → consider refactoring to reduce dependencies

---

## Preventing Future Hotspots

### Code Review Checklist

When reviewing changes to existing hotspots (P0/P1 files):

- [ ] Does this change increase complexity? (run `radon cc`)
- [ ] Are new tests added for new branches?
- [ ] Can logic be extracted to reduce nesting?
- [ ] Is this file becoming a "God Object"? (too many responsibilities)

### Pre-Commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash

# Check complexity of modified files
MODIFIED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$')

for file in $MODIFIED_FILES; do
  MAX_CC=$(radon cc "$file" -a --json | jq '[.[] | .complexity] | max')

  if [ "$MAX_CC" -gt 15 ]; then
    echo "❌ BLOCKED: $file has cyclomatic complexity > 15 ($MAX_CC)"
    echo "   Please refactor before committing."
    exit 1
  fi
done

echo "✅ Complexity check passed"
```

---

## Real-World Case Study

### The Workflow Hotspot

**Initial State:**
- File: `src/workflow/workflow_nodes.py`
- Commits (6 months): 45
- Max Cyclomatic Complexity: 18
- Priority: **P0 - Critical**

**Problem:**
- `score_report()` method had 78 lines, CC 18
- Every bug fix introduced new bugs
- Tests took 15+ minutes to run (too many paths)

**Refactoring Steps:**
1. **Week 1**: Add characterization tests (no refactoring)
2. **Week 2**: Extract `_score_faithfulness()` (CC 18 → 14)
3. **Week 3**: Extract `_score_completeness()` (CC 14 → 10)
4. **Week 4**: Extract `_validate_scoring_inputs()` (CC 10 → 7)

**Results After 4 Weeks:**
- Max CC: 18 → 7 (61% reduction)
- Function LOC: 78 → 25 (68% reduction)
- Test execution: 15 min → 5 min (67% faster)
- Bug rate: 2.3 bugs/month → 0.4 bugs/month (83% reduction)
- Still a hotspot (high churn), but low complexity → **P1 (Monitor)**

---

## Quick Reference

### Hotspot Detection

```bash
# Run hotspot analysis
python .claude/skills/refacter/scripts/analyze_hotspots.py src/

# Top 10 most changed files
git log --since="6 months ago" --pretty=format: --name-only src/ \
  | sort | uniq -c | sort -rn | head -10

# Complexity of specific file
radon cc src/workflow/workflow_nodes.py -a --min B
```

### Priority Matrix

| Churn | Complexity | Priority | Action |
|-------|------------|----------|--------|
| High (> 15) | High (> 10) | **P0** | Refactor now |
| High (> 15) | Low (≤ 10) | P1 | Add tests, monitor |
| Low (≤ 15) | High (> 10) | P2 | Tech debt |
| Low (≤ 15) | Low (≤ 10) | P3 | Ignore |

---

## References

- **Your Code as a Crime Scene** by Adam Tornhill - Original hotspot analysis concept
- **Code Maat**: https://github.com/adamtornhill/code-maat - Hotspot analysis tool
- **Complexity Metrics**: See [CODE-COMPLEXITY.md](CODE-COMPLEXITY.md)
- **Refactoring Techniques**: See [REFACTORING-PATTERNS.md](REFACTORING-PATTERNS.md)
