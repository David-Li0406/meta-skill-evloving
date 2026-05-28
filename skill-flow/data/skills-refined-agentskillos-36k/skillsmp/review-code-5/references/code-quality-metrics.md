<overview>
Quantitative code quality metrics for informed review decisions. Includes cognitive complexity, cyclomatic complexity, maintainability index, and technical debt indicators.
</overview>

<cognitive_complexity>
<definition>
**What it measures**: Mental effort required to understand code
</definition>

<targets>
Target complexity levels:

- Per function: <15 (ideal <10)
- Per module: <50
- Per file: <100
  </targets>

<complexity_factors>
Factors that increase complexity:

- Each nesting level (+1 per level)
- Logical operators (&&, ||)
- Recursion
- Breaks in linear flow (break, continue, goto)
  </complexity_factors>

<reduction_example>
Reducing cognitive complexity:

```javascript
// HIGH COMPLEXITY (nested conditionals)
function process(data) {
  if (data) {
    if (data.valid) {
      if (data.items.length > 0) {
        for (const item of data.items) {
          if (item.active) {
            // process
          }
        }
      }
    }
  }
}

// LOW COMPLEXITY (guard clauses + extraction)
function process(data) {
  if (!data?.valid) return;
  if (!data.items?.length) return;

  processActiveItems(data.items);
}

function processActiveItems(items) {
  const active = items.filter((item) => item.active);
  active.forEach(processItem);
}
```

</reduction_example>
</cognitive_complexity>

<cyclomatic_complexity>
<definition>
**What it measures**: Number of independent paths through code
</definition>

<formula>
**Formula**: 1 + (if + while + for + case + catch + && + ||)
</formula>

<targets>
| Score | Risk | Action |
|-------|------|--------|
| 1-4 | Low | Good |
| 5-7 | Moderate | Consider simplifying |
| 8-10 | High | Refactor recommended |
| >10 | Very High | Must refactor |
</targets>
</cyclomatic_complexity>

<function_size_metrics>
| Metric | Target | Warning | Critical |
|--------|--------|---------|----------|
| Lines | <20 | >30 | >50 |
| Parameters | ≤3 | 4 | >5 |
| Nesting depth | ≤2 | 3 | >3 |
| Return statements | 1-2 | 3-4 | >4 |
</function_size_metrics>

<maintainability_index>
<formula>
Microsoft's formula:

```
MI = MAX(0, (171 - 5.2*ln(HalsteadVolume) - 0.23*CC - 16.2*ln(LOC)) * 100/171)
```

</formula>

<interpretation>
| Score | Maintainability |
|-------|-----------------|
| 80-100 | High - easy to maintain |
| 60-79 | Moderate - some concerns |
| 40-59 | Low - refactoring recommended |
| <40 | Very Low - significant refactoring needed |
</interpretation>
</maintainability_index>

<technical_debt_indicators>
| Indicator | Healthy | Warning |
|-----------|---------|---------|
| Code duplication | <5% | >10% |
| Test coverage | >80% | <60% |
| Cyclomatic complexity avg | <5 | >8 |
| TODO/FIXME count | Stable | Growing |
| Dependency age | <6 months | >12 months |
</technical_debt_indicators>

<code_churn>
<definition>
**What it measures**: Frequency of code changes
</definition>

<warning_signs>
Signs of problematic churn:

- Same file changed in >50% of recent commits
- High churn + low test coverage = risk
- Late-project churn indicates instability
  </warning_signs>
  </code_churn>

<review_thresholds>
<must_comment>
Always comment on:

- Function complexity >15
- Nesting >3 levels
- Function >50 lines
- > 3 parameters without object
  > </must_comment>

<consider_commenting>
Consider commenting on:

- Duplicated blocks >10 lines
- Method doing multiple things
- Unclear naming
  </consider_commenting>

<dont_comment>
Skip commenting on:

- Slightly suboptimal but working code
- Style preferences
- Minor naming improvements
  </dont_comment>
  </review_thresholds>

<measurement_tools>
| Language | Tool |
|----------|------|
| JavaScript/TypeScript | ESLint (complexity rules), SonarQube |
| Python | Radon, Pylint |
| Java | SonarQube, PMD |
| Go | gocyclo, golangci-lint |
| General | SonarQube, CodeClimate |
</measurement_tools>

<sources>
- [SonarQube Cognitive Complexity](https://www.sonarsource.com/docs/CognitiveComplexity.pdf)
- [Microsoft Maintainability Index](https://learn.microsoft.com/en-us/visualstudio/code-quality/code-metrics-maintainability-index-range-and-meaning)
- [Cyclomatic Complexity](https://en.wikipedia.org/wiki/Cyclomatic_complexity)
</sources>
