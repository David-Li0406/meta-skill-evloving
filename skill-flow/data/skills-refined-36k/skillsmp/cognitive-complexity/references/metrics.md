# Cognitive Complexity Metrics

Detailed metrics for measuring code cognitive load beyond simple cyclomatic complexity.

## Module Depth Ratio

**Formula**: `Depth = Implementation Power / Interface Complexity`

### Measuring Interface Complexity

**Parameters** (0-10 scale):
- 0-2 params: 1 point
- 3-4 params: 2 points
- 5-6 params: 4 points
- 7+ params: 8 points

**Required knowledge** (0-10 scale):
- Self-explanatory from types: 1 point
- Must read docs: 3 points
- Must understand other modules: 6 points
- Must understand system architecture: 9 points

**Special cases** (0-10 scale):
- No special cases: 0 points
- 1-2 special cases: 2 points
- 3-5 special cases: 5 points
- 6+ special cases: 8 points

**Total interface complexity**: Sum / 3 (normalized 0-10)

### Measuring Implementation Power

**Lines of code** (0-10 scale):
- <50 lines: 2 points
- 50-100 lines: 4 points
- 100-200 lines: 6 points
- 200-500 lines: 8 points
- 500+ lines: 10 points

**Features provided** (0-10 scale):
- 1-2 features: 2 points
- 3-5 features: 5 points
- 6-10 features: 8 points
- 10+ features: 10 points

**Edge cases handled** (0-10 scale):
- Happy path only: 1 point
- Basic error handling: 3 points
- Comprehensive error handling: 6 points
- Errors + edge cases + recovery: 9 points

**Total implementation power**: Sum / 3 (normalized 0-10)

### Depth Targets

- **Deep module**: Ratio > 2.0 (good!)
- **Balanced**: Ratio 1.0-2.0 (acceptable)
- **Shallow module**: Ratio < 1.0 (refactor needed)

## Working Memory Load

### Parameter Count

```
Score = Parameters / 2 (capped at 10)
```

- 0-2 params: Low (1 point)
- 3-4 params: Moderate (2 points)
- 5-6 params: High (3 points)
- 7+ params: Very high (4+ points)

### Variable Lifespan

```
Score = (Lines from definition to last use) / 10
```

- 0-10 lines: Low (1 point)
- 11-25 lines: Moderate (2 points)
- 26-50 lines: High (3 points)
- 50+ lines: Very high (5+ points)

### Simultaneous Concerns

Count distinct "things" function manipulates:

```elixir
# 6 concerns
def process_order(user, items, payment, shipping, inventory, notifications) do
  # Must track all 6 simultaneously
end
```

- 1-2 concerns: Low (1 point)
- 3-4 concerns: Moderate (2 points)
- 5-6 concerns: High (3 points)
- 7+ concerns: Very high (5 points)

### Nesting Depth

```
Score = Maximum indentation level / 2
```

- 0-2 levels: Low (1 point)
- 3-4 levels: Moderate (2 points)
- 5-6 levels: High (3 points)
- 7+ levels: Very high (4+ points)

### Total Working Memory Score

```
Total = Parameter Score + Lifespan Score + Concerns Score + Nesting Score
```

- 0-5: Low load
- 6-10: Moderate load
- 11-15: High load
- 16+: Very high load (refactor!)

## Information Leakage

### Temporal Coupling Score

Count functions that must be called in specific order without enforcement:

```
Score = Number of ordered dependencies
```

- 0: No coupling (0 points)
- 1-2: Low coupling (2 points)
- 3-5: Moderate coupling (5 points)
- 6+: High coupling (10 points)

### Pass-Through Layers

Count how many layers a variable passes through unchanged:

```
Score = (Pass-through layers - 1) × 2
```

- 0-1 layers: Direct use (0 points)
- 2 layers: Acceptable (2 points)
- 3 layers: Getting complex (4 points)
- 4+ layers: Too complex (6+ points)

### Exposed Internals

Count abstraction violations:

- Returns internal data structure: 3 points each
- Requires knowledge of implementation: 2 points each
- Must coordinate with other modules: 2 points each

## Onboarding Difficulty

### Context Requirements

**Modules that must be understood** (0-10 scale):
- 0-1 modules: Self-contained (1 point)
- 2-3 modules: Low context (3 points)
- 4-6 modules: Moderate context (6 points)
- 7+ modules: High context (9 points)

**Domain knowledge required** (0-10 scale):
- Clear from code: 1 point
- Clear from docs: 3 points
- Requires domain expert: 6 points
- Requires tribal knowledge: 9 points

**Historical decisions** (0-10 scale):
- All documented: 1 point
- Mostly documented: 3 points
- Some documentation: 6 points
- Undocumented: 9 points

**Total context score**: Sum / 3 (normalized 0-10)

### State Complexity

**State count** (0-10 scale):
- 0-2 states: Simple (1 point)
- 3-4 states: Moderate (3 points)
- 5-8 states: Complex (6 points)
- 9+ states: Very complex (9 points)

**Transitions** (0-10 scale):
- All documented: 1 point
- Mostly documented: 3 points
- Some documented: 6 points
- Undocumented: 9 points

**Invariants** (0-10 scale):
- Clearly documented: 1 point
- Partially documented: 4 points
- Must infer from code: 7 points
- Unclear: 10 points

**Total state score**: Sum / 3 (normalized 0-10)

### Overall Onboarding Score

```
Onboarding Difficulty = (Context Score + State Score) / 2
```

- 0-3: Easy (new dev productive in days)
- 4-6: Moderate (new dev productive in 1-2 weeks)
- 7-8: Hard (new dev productive in 3-4 weeks)
- 9-10: Very hard (new dev productive in 1-2 months)

## Semantic Clarity

### Name Quality

**Generic names** (penalty points):
- `process`, `handle`, `manage`: -2 points each
- `do_*`, `perform_*`, `execute_*`: -2 points each
- `data`, `info`, `value`, `result`: -2 points each
- `helper`, `util`, `common`, `misc`: -3 points each
- Single letters beyond loop counters: -2 points each

**Clear names** (bonus points):
- Domain-specific verbs: +1 point each
- Specific nouns: +1 point each
- Purpose-revealing: +2 points each

**Target**: Net positive score

### Naming Consistency

Count concepts with multiple names:

```elixir
fetch_user(id)
get_user(id)
load_user(id)
retrieve_user(id)
# Same concept, 4 different names
```

```
Inconsistency Score = (Number of names - 1) per concept
```

**Target**: 0-1 inconsistencies per concept

## Composite Metrics

### Overall Cognitive Load

```
Cognitive Load = (
  (10 - Module Depth) × 2 +  # Shallow modules worse
  Information Leakage +
  Working Memory Load +
  (Onboarding Difficulty × 2)  # Onboarding impact higher
) / 6
```

- 0-3: Low cognitive load (maintainable)
- 4-6: Moderate cognitive load (acceptable)
- 7-8: High cognitive load (refactor soon)
- 9-10: Very high cognitive load (refactor now!)

### Code Comprehension Time

Estimated time for experienced developer to fully understand module:

```
Time (hours) = (
  (Lines of Code / 50) +
  (Onboarding Difficulty × 2) +
  (Working Memory Load / 2) +
  Information Leakage
)
```

**Targets**:
- <1 hour: Excellent
- 1-3 hours: Good
- 3-8 hours: Acceptable
- >8 hours: Too complex

### Change Difficulty

How hard to make typical change:

```
Change Difficulty = (
  (10 - Module Depth) +  # Shallow = many files to change
  Information Leakage +   # Leakage = ripple effects
  (Temporal Coupling × 2) # Ordering = hard to change
) / 4
```

- 0-2: Easy (localized changes)
- 3-5: Moderate (some coordination)
- 6-8: Hard (many files affected)
- 9-10: Very hard (system-wide impact)

## Measurement Process

1. **Select scope** (module, file, system)
2. **Measure all applicable metrics**
3. **Calculate composite scores**
4. **Identify outliers** (scores > 7)
5. **Prioritize** (by impact × frequency of change)
6. **Track over time** (trend up or down?)

## Reporting Format

```
Module: lib/my_app/feature.ex

Cognitive Complexity Analysis:
- Module Depth: 0.8 (shallow - refactor needed)
- Working Memory Load: 12 (high)
- Information Leakage: 8 (high)
- Onboarding Difficulty: 7 (hard)

Overall Cognitive Load: 7.2 (high - refactor soon)

Estimated comprehension time: 6 hours
Change difficulty: 7 (hard - many files affected)

Priority: High (changed frequently, high complexity)
```

## Benchmarks

Based on well-maintained Elixir codebases:

**Excellent modules**:
- Module Depth: > 3.0
- Working Memory: < 5
- Onboarding: < 4
- Cognitive Load: < 3

**Acceptable modules**:
- Module Depth: 1.5-3.0
- Working Memory: 5-8
- Onboarding: 4-6
- Cognitive Load: 3-6

**Needs refactoring**:
- Module Depth: < 1.0
- Working Memory: > 10
- Onboarding: > 7
- Cognitive Load: > 7
