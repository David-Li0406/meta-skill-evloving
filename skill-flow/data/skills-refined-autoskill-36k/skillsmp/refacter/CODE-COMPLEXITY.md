# Code Complexity Metrics

Understanding and measuring code complexity to guide refactoring decisions.

**Tools**: radon (cyclomatic & cognitive complexity), pylint (maintainability index)

---

## Why Complexity Matters

**High complexity → More bugs**: Research shows functions with cyclomatic complexity > 10 have 2-3x more bugs.

**Complexity metrics predict:**
- 🐛 Bug density (more complex = more bugs)
- ⏱️ Time to understand (cognitive load)
- 🔧 Maintenance cost (harder to change)
- 🧪 Test coverage difficulty (exponential paths)

---

## Cyclomatic Complexity

**Definition**: Number of linearly independent paths through code (McCabe's metric).

### How to Calculate

**Formula**: `CC = E - N + 2P`
- E = edges in control flow graph
- N = nodes
- P = connected components

**Practical shortcut**: Count decision points + 1

```python
# Cyclomatic Complexity = 1 (no branches)
def simple():
    return "hello"

# Cyclomatic Complexity = 2 (one if)
def single_if(x):
    if x > 0:
        return "positive"
    return "zero or negative"

# Cyclomatic Complexity = 4 (three ifs)
def multiple_ifs(x, y, z):
    if x > 0:  # +1
        return "x positive"
    if y > 0:  # +1
        return "y positive"
    if z > 0:  # +1
        return "z positive"
    return "all non-positive"
```

### Decision Points That Add Complexity

```python
if condition:        # +1
elif other:          # +1
for item in list:    # +1
while condition:     # +1
except Exception:    # +1
and / or             # +1 each (short-circuit evaluation)
? : (ternary)        # +1
```

### Complexity Thresholds

| CC Score | Rating | Interpretation | Action |
|----------|--------|----------------|--------|
| 1-5 | A (Simple) | Low risk, easy to maintain | ✅ No action |
| 6-10 | B (More Complex) | Moderate risk | ⚠️ Monitor |
| 11-20 | C (Complex) | High risk, hard to test | 🔧 Refactor recommended |
| 21-50 | D (Very Complex) | Very high risk | 🚨 Refactor required |
| 51+ | F (Extremely Complex) | Unmaintainable | 🔥 Urgent refactor |

**Industry Standard**: Keep cyclomatic complexity ≤ 10

---

## Cognitive Complexity

**Definition**: How difficult code is for humans to understand (SonarSource metric).

**Difference from Cyclomatic Complexity:**
- **Cyclomatic**: Measures control flow paths (good for testing)
- **Cognitive**: Measures mental effort to understand (good for readability)

### What Increases Cognitive Complexity

```python
# ❌ BAD: High cognitive complexity (deeply nested)
def process_orders(orders):
    for order in orders:               # +1 (nesting level 0 → 1)
        if order.is_valid():           # +2 (nesting level 1 → 2)
            for item in order.items:   # +3 (nesting level 2 → 3)
                if item.in_stock():    # +4 (nesting level 3 → 4)
                    item.ship()
                else:
                    if item.backorderable():  # +5 (nesting level 4 → 5)
                        item.backorder()
# Cognitive Complexity = 15 (very hard to understand)

# ✅ GOOD: Low cognitive complexity (early returns, flat structure)
def process_orders_improved(orders):
    for order in orders:                # +1
        if not order.is_valid():        # +2, but early return
            continue

        for item in order.items:        # +2
            if not item.in_stock():     # +3, but early return
                if item.backorderable():
                    item.backorder()
                continue

            item.ship()
# Cognitive Complexity = 8 (much easier to follow)
```

### Cognitive Complexity Rules

**Increment for:**
- Nesting level (each additional level adds +1 per nested decision)
- Recursion (+1)
- Break/continue in loops (+1)
- Sequences of logical operators (`and`, `or`) (+1)

**Do NOT increment for:**
- Straight-line code (no branches)
- Simple if-return (no nesting)

### Cognitive Complexity Thresholds

| Score | Interpretation | Action |
|-------|----------------|--------|
| 1-10 | Simple, easy to understand | ✅ No action |
| 11-15 | Moderate, requires focus | ⚠️ Monitor |
| 16-25 | Complex, hard to follow | 🔧 Refactor recommended |
| 26+ | Very complex, confusing | 🚨 Refactor required |

**Industry Standard**: Keep cognitive complexity ≤ 15

---

## Lines of Code (LOC)

**Metric**: Physical lines of code in a function or file.

### Why LOC Matters

- Short functions easier to understand
- Long functions likely do multiple things (violate Single Responsibility)
- Harder to name long functions (cognitive signal)

### LOC Thresholds

| Lines | Interpretation | Action |
|-------|----------------|--------|
| 1-25 | Ideal function length | ✅ No action |
| 26-50 | Acceptable | ⚠️ Consider Extract Method |
| 51-100 | Too long | 🔧 Extract multiple methods |
| 101+ | Way too long | 🚨 Major refactor needed |

**Industry Standard**: Functions should be ≤ 50 lines

---

## Maintainability Index (MI)

**Definition**: Composite metric combining cyclomatic complexity, LOC, and Halstead volume.

**Formula (simplified):**
```
MI = 171 - 5.2 * ln(Halstead Volume) - 0.23 * CC - 16.2 * ln(LOC)
```

### MI Thresholds

| Score | Rating | Interpretation |
|-------|--------|----------------|
| 85-100 | A (Highly Maintainable) | Excellent code quality |
| 65-84 | B (Maintainable) | Good code quality |
| 50-64 | C (Moderately Maintainable) | Needs improvement |
| 25-49 | D (Poorly Maintainable) | Significant refactoring needed |
| 0-24 | F (Unmaintainable) | Urgent refactoring required |

---

## Measuring Complexity with Radon

### Installation

```bash
pip install radon
```

### Basic Usage

```bash
# Cyclomatic complexity for directory
radon cc src/ -a

# Show only functions with CC > 10
radon cc src/ -a --min B

# Cognitive complexity
radon cc src/ -a --cognitive

# Maintainability Index
radon mi src/ -a

# Raw metrics (LOC, comments, etc.)
radon raw src/
```

### Example Output

```bash
$ radon cc src/workflow/workflow_nodes.py -a

src/workflow/workflow_nodes.py
    M 143:4 WorkflowNodes.analyze_technical - A (3)
    M 167:4 WorkflowNodes.fetch_news - A (2)
    M 192:4 WorkflowNodes.generate_report - B (8)
    M 248:4 WorkflowNodes.score_report - C (11)  # ⚠️ Refactor candidate
```

### Interpreting Results

```
M 248:4 WorkflowNodes.score_report - C (11)
│  │    │                            │  │
│  │    │                            │  └─ Cyclomatic Complexity = 11
│  │    │                            └─ Rating: C (Complex)
│  │    └─ Method name
│  └─ Line 248, column 4
└─ M = Method (F = Function, C = Class)
```

---

## Using Complexity Analysis Script

### Basic Usage

```bash
# Analyze directory
python .claude/skills/refacter/scripts/analyze_complexity.py src/

# With thresholds
python .claude/skills/refacter/scripts/analyze_complexity.py src/ \
  --max-cc 10 \
  --max-cognitive 15

# JSON output
python .claude/skills/refacter/scripts/analyze_complexity.py src/ --json
```

### Example Output

```
====================================================
CODE COMPLEXITY ANALYSIS
====================================================

Analyzing: src/

High Complexity Functions (CC > 10):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📄 src/workflow/workflow_nodes.py
     🔧 score_report (line 248) - CC: 11, Cognitive: 14
        Action: Extract scoring logic into separate methods

  📄 src/agent/ticker_analysis.py
     🔧 analyze_ticker (line 67) - CC: 13, Cognitive: 18
        Action: Simplify conditional branches

Summary:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Total Functions: 42
  High Complexity (CC > 10): 2 (4.8%)
  Average CC: 5.3
  Max CC: 13

Recommendations:
  🔧 Refactor 2 functions to reduce complexity
  ⚠️ Monitor cognitive complexity in analyze_ticker
```

---

## Refactoring Based on Complexity

### High Cyclomatic Complexity (> 10)

**Root Cause**: Too many decision points

**Solutions:**
1. **Extract Method**: Pull complex conditionals into separate functions
2. **Strategy Pattern**: Replace conditionals with polymorphism
3. **Guard Clauses**: Use early returns to reduce nesting

### High Cognitive Complexity (> 15)

**Root Cause**: Too much nesting, hard to follow

**Solutions:**
1. **Flatten Nesting**: Use early returns
2. **Extract Conditional**: Pull complex conditions into named functions
3. **Simplify Boolean Logic**: Use De Morgan's laws

### High LOC (> 50 lines)

**Root Cause**: Function does too many things

**Solutions:**
1. **Extract Method**: Break into smaller functions
2. **Extract Class**: If related methods, create new class
3. **Single Responsibility**: Each function should do ONE thing

---

## Real-World Example

### Before Refactoring

```python
# Cyclomatic Complexity: 14
# Cognitive Complexity: 22
# LOC: 78
def process_market_data(ticker, start_date, end_date):
    data = []
    if ticker:
        if start_date:
            if end_date:
                if end_date > start_date:
                    raw_data = fetch_data(ticker, start_date, end_date)
                    if raw_data:
                        for row in raw_data:
                            if row['volume'] > 0:
                                if row['price'] is not None:
                                    if row['price'] > 0:
                                        adjusted_price = row['price'] * row['adj_factor']
                                        if adjusted_price > 0:
                                            data.append({
                                                'date': row['date'],
                                                'price': adjusted_price,
                                                'volume': row['volume']
                                            })
    return data
```

### After Refactoring

```python
# Cyclomatic Complexity: 3 (per function, max 3)
# Cognitive Complexity: 4 (per function, max 4)
# LOC: 15-20 (per function)

def process_market_data(ticker, start_date, end_date):
    """Main entry point - orchestrates data processing"""
    if not _validate_inputs(ticker, start_date, end_date):
        return []

    raw_data = fetch_data(ticker, start_date, end_date)
    return _filter_and_transform(raw_data)

def _validate_inputs(ticker, start_date, end_date):
    """Validate input parameters"""
    return (ticker and start_date and end_date and end_date > start_date)

def _filter_and_transform(raw_data):
    """Filter valid rows and transform data"""
    if not raw_data:
        return []

    return [
        _transform_row(row)
        for row in raw_data
        if _is_valid_row(row)
    ]

def _is_valid_row(row):
    """Check if row has valid data"""
    return (
        row.get('volume', 0) > 0
        and row.get('price') is not None
        and row.get('price', 0) > 0
    )

def _transform_row(row):
    """Transform raw row to output format"""
    adjusted_price = row['price'] * row['adj_factor']
    return {
        'date': row['date'],
        'price': adjusted_price,
        'volume': row['volume']
    }
```

**Improvements:**
- ✅ Reduced cyclomatic complexity from 14 → 3 (per function)
- ✅ Reduced cognitive complexity from 22 → 4 (per function)
- ✅ Reduced max function LOC from 78 → 20
- ✅ Each function has clear single responsibility
- ✅ Easier to test (can test validation, filtering, transformation separately)

---

## Quick Reference Card

| Metric | Threshold | Tool Command | Fix |
|--------|-----------|--------------|-----|
| **Cyclomatic Complexity** | ≤ 10 | `radon cc src/` | Extract method, simplify conditionals |
| **Cognitive Complexity** | ≤ 15 | `radon cc src/ --cognitive` | Flatten nesting, early returns |
| **LOC** | ≤ 50 | `radon raw src/` | Extract method, extract class |
| **Maintainability Index** | ≥ 65 | `radon mi src/` | Reduce complexity, improve structure |

---

## References

- **Cyclomatic Complexity**: [McCabe (1976)](https://www.literateprogramming.com/mccabe.pdf) - Original paper
- **Cognitive Complexity**: [SonarSource White Paper](https://www.sonarsource.com/docs/CognitiveComplexity.pdf)
- **radon Documentation**: https://radon.readthedocs.io/
- **Refactoring patterns**: See [REFACTORING-PATTERNS.md](REFACTORING-PATTERNS.md)
