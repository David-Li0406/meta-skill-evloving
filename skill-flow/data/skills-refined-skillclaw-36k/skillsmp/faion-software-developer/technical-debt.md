---
id: technical-debt
name: "Technical Debt"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Technical Debt

## Overview

Technical debt represents the implied cost of additional rework caused by choosing an easy or quick solution now instead of a better approach that would take longer. Managing technical debt involves identifying, tracking, and strategically paying it down.

## When to Use

- Planning sprint capacity for maintenance
- Evaluating trade-offs during implementation
- Prioritizing refactoring work
- Communicating costs to stakeholders
- Making architectural decisions

## Key Principles

- **Debt is not always bad**: Strategic debt can accelerate delivery
- **Track explicitly**: Make debt visible and measurable
- **Pay interest regularly**: Budget time for debt reduction
- **Prioritize by impact**: Fix high-impact debt first
- **Prevent accumulation**: Code reviews, standards, automation

## Best Practices

### Types of Technical Debt

```markdown
## Technical Debt Quadrant (Martin Fowler)

                   Reckless                     Prudent
              ┌─────────────────────┬─────────────────────┐
              │                     │                     │
   Deliberate │ "We don't have     │ "We must ship now   │
              │  time for design"   │  and deal with      │
              │                     │  consequences"      │
              │ [HIGH RISK]         │ [STRATEGIC]         │
              ├─────────────────────┼─────────────────────┤
              │                     │                     │
 Inadvertent  │ "What's            │ "Now we know how    │
              │  layering?"         │  we should have     │
              │                     │  done it"           │
              │ [INCOMPETENCE]      │ [LEARNING]          │
              │                     │                     │
              └─────────────────────┴─────────────────────┘

## Common Types
1. Code Debt: Messy code, duplication, poor naming
2. Design Debt: Poor architecture, tight coupling
3. Test Debt: Missing tests, flaky tests
4. Documentation Debt: Outdated or missing docs
5. Infrastructure Debt: Outdated dependencies, legacy systems
6. Process Debt: Missing CI/CD, manual deployments
```

### Tracking Technical Debt

```python
# Example: Technical Debt Register

"""
TECH_DEBT_REGISTER.md

## Active Technical Debt Items

### TD-001: User Service Monolith
- **Type**: Design Debt
- **Severity**: High
- **Impact**: Hard to scale, deployment coupling
- **Location**: src/services/user_service.py
- **Created**: 2024-01-15
- **Interest**: ~2 hours/week in deployment complexity
- **Estimated Fix**: 3 sprints to split into microservices
- **Business Impact**: Limits feature velocity by 20%

### TD-002: Missing Integration Tests for Payment Flow
- **Type**: Test Debt
- **Severity**: High
- **Impact**: Payment bugs found in production
- **Location**: tests/integration/
- **Created**: 2024-02-01
- **Interest**: ~4 hours/month debugging production issues
- **Estimated Fix**: 2 weeks
- **Business Impact**: 2 production incidents last quarter

### TD-003: Hardcoded Configuration
- **Type**: Code Debt
- **Severity**: Medium
- **Impact**: Difficult environment management
- **Location**: src/config.py, various files
- **Created**: 2024-01-01
- **Interest**: ~1 hour/deployment
- **Estimated Fix**: 3 days
- **Business Impact**: Deployment errors, security risk

### TD-004: Legacy jQuery in Dashboard
- **Type**: Infrastructure Debt
- **Severity**: Low
- **Impact**: Inconsistent UI, harder to maintain
- **Location**: frontend/legacy/
- **Created**: 2023-06-01
- **Interest**: ~2 hours/month
- **Estimated Fix**: 2 weeks
- **Business Impact**: Slower feature development for dashboard
"""

# Technical debt tracking in code
class TechnicalDebt:
    """Track technical debt items programmatically."""

    @staticmethod
    def register(
        id: str,
        description: str,
        severity: str,
        estimated_hours: int,
        file: str = None,
        line: int = None
    ):
        """
        Register technical debt.
        Can be called from code comments or tracked externally.
        """
        # In practice, this might write to a tracking system
        pass

# Usage in code comments
# TECH_DEBT(TD-005): This function has O(n^2) complexity.
# Should use a hash map for O(n). Low priority until data grows.
def find_duplicates(items: list) -> list:
    duplicates = []
    for i, item in enumerate(items):
        for j, other in enumerate(items):
            if i != j and item == other and item not in duplicates:
                duplicates.append(item)
    return duplicates
```

### Measuring Technical Debt

```python
# Metrics for tracking debt

"""
## Technical Debt Metrics

### Code Quality Metrics
- Cyclomatic complexity (target: < 10 per function)
- Code duplication % (target: < 5%)
- Test coverage % (target: > 80%)
- Linting violations (target: 0 blocking)

### Velocity Metrics
- Time to implement features (trending up = debt)
- Bug fix time (trending up = debt)
- Deployment frequency (trending down = debt)
- Lead time for changes (trending up = debt)

### Operational Metrics
- Production incidents/month
- Mean time to recovery (MTTR)
- Deployment failure rate
- Rollback frequency

### Tracking Over Time
- Tech debt items created vs resolved
- Debt severity distribution
- Time spent on debt vs features
"""

# Example: Automated debt detection
from radon.complexity import cc_visit
from radon.metrics import mi_visit
import ast

def analyze_complexity(source_code: str) -> dict:
    """Analyze code complexity as proxy for debt."""
    results = {
        "high_complexity_functions": [],
        "maintainability_index": 0,
        "total_complexity": 0
    }

    # Cyclomatic complexity
    for item in cc_visit(source_code):
        if item.complexity > 10:  # Threshold
            results["high_complexity_functions"].append({
                "name": item.name,
                "complexity": item.complexity,
                "line": item.lineno
            })
        results["total_complexity"] += item.complexity

    # Maintainability index
    results["maintainability_index"] = mi_visit(source_code, True)

    return results

def generate_debt_report(directory: str) -> dict:
    """Generate technical debt report for codebase."""
    report = {
        "complexity_issues": [],
        "test_coverage_gaps": [],
        "outdated_dependencies": [],
        "total_debt_score": 0
    }

    # Analyze each file
    for file_path in Path(directory).rglob("*.py"):
        source = file_path.read_text()
        analysis = analyze_complexity(source)

        if analysis["high_complexity_functions"]:
            report["complexity_issues"].append({
                "file": str(file_path),
                "functions": analysis["high_complexity_functions"]
            })

    return report
```

### Prioritizing Debt Payoff

```markdown
## Debt Prioritization Matrix

### Factors to Consider
1. **Impact on Velocity**: How much does it slow development?
2. **Risk**: What's the probability and impact of failure?
3. **Interest Rate**: How much ongoing cost does it incur?
4. **Fix Cost**: How long to pay off?
5. **Dependencies**: Does other work depend on this fix?

### Priority Calculation
Priority Score = (Impact × Risk × Interest) / Fix Cost

### Example Scoring

| Item | Impact | Risk | Interest | Cost | Score | Priority |
|------|--------|------|----------|------|-------|----------|
| TD-001 | 5 | 4 | 4 | 60h | 1.33 | Medium |
| TD-002 | 5 | 5 | 5 | 40h | 3.13 | High |
| TD-003 | 3 | 3 | 3 | 24h | 1.13 | Medium |
| TD-004 | 2 | 1 | 2 | 80h | 0.05 | Low |

### When to Pay Off Debt

**Pay Now (High Priority)**
- Security vulnerabilities
- Data integrity risks
- Blocking other development
- High ongoing maintenance cost

**Pay Soon (Medium Priority)**
- Slowing feature development
- Causing frequent bugs
- Complexity spreading

**Pay Later (Low Priority)**
- Cosmetic issues
- Low-traffic areas
- Stable legacy code
```

### Strategies for Paying Down Debt

```python
# Strategy 1: Boy Scout Rule - Leave code better than you found it

# Before (encountered during feature work)
def process_data(d):
    r = []
    for x in d:
        if x > 0:
            r.append(x * 2)
    return r

# After (small improvement while working on related code)
def process_data(data: list[int]) -> list[int]:
    """Double positive numbers in the input list."""
    return [x * 2 for x in data if x > 0]


# Strategy 2: Dedicated Debt Sprints

"""
## Sprint Allocation Strategies

### Continuous (Recommended)
- 20% of each sprint for debt
- Every sprint has some debt work
- Debt never builds up too much

### Periodic
- Every 4th sprint is "tech debt sprint"
- Good for larger refactoring
- Risk: debt builds between sprints

### Triggered
- Debt sprint when threshold exceeded
- Reactive rather than proactive
- Can lead to crisis mode

### Hybrid
- 15% continuous + quarterly debt sprint
- Best of both approaches
- Handles both small and large debt
"""


# Strategy 3: Feature-Attached Debt Payoff

"""
## Attach Debt to Features

When planning a feature that touches debt-ridden code:

1. Identify debt in affected area
2. Include debt payoff in feature estimate
3. Pay debt as part of feature work
4. Prevents adding debt on top of debt

Example:
- Feature: Add subscription tiers
- Affected code: User billing module (has TD-003)
- Approach: Fix TD-003 first, then build feature
- Benefit: Clean foundation for new feature
"""


# Strategy 4: Strangler Fig Pattern for Large Debt

class LegacyOrderProcessor:
    """Old, debt-ridden implementation."""
    def process(self, order):
        # Complex, hard to maintain code
        pass

class ModernOrderProcessor:
    """New, clean implementation."""
    def process(self, order: Order) -> ProcessingResult:
        # Clean, well-tested code
        pass

class OrderProcessorFacade:
    """Gradually migrate from legacy to modern."""

    def __init__(self):
        self.legacy = LegacyOrderProcessor()
        self.modern = ModernOrderProcessor()

    def process(self, order):
        # Route to appropriate implementation based on feature flags
        if self._should_use_modern(order):
            return self.modern.process(order)
        return self.legacy.process(order)

    def _should_use_modern(self, order) -> bool:
        # Gradually increase modern usage
        return (
            feature_flags.is_enabled("modern_orders") and
            order.type in ["standard", "premium"]  # Start with subset
        )
```

### Preventing Debt Accumulation

```yaml
# .github/workflows/quality-gates.yml
name: Quality Gates

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check complexity
        run: |
          pip install radon
          radon cc src/ -a -nc  # Fail on complexity > 10

      - name: Check coverage
        run: |
          pytest --cov=src --cov-fail-under=80

      - name: Check duplication
        run: |
          pip install pylint
          pylint src/ --disable=all --enable=duplicate-code

      - name: Check dependencies
        run: |
          pip install safety
          safety check -r requirements.txt

      - name: Check TODO/FIXME count
        run: |
          count=$(grep -r "TODO\|FIXME\|HACK\|XXX" src/ | wc -l)
          if [ "$count" -gt 50 ]; then
            echo "Too many TODOs: $count"
            exit 1
          fi
```

```python
# Pre-commit hooks for debt prevention
# .pre-commit-config.yaml

repos:
  - repo: local
    hooks:
      - id: check-complexity
        name: Check cyclomatic complexity
        entry: python scripts/check_complexity.py
        language: python
        types: [python]

      - id: check-debt-comments
        name: Check debt comments have tickets
        entry: python scripts/check_debt_comments.py
        language: python
        types: [python]

# scripts/check_debt_comments.py
import re
import sys

DEBT_PATTERN = r'(TODO|FIXME|HACK|XXX|TECH_DEBT)'
TICKET_PATTERN = r'(TODO|FIXME|HACK|XXX|TECH_DEBT)\s*\([A-Z]+-\d+\)'

def check_file(filepath):
    with open(filepath) as f:
        content = f.read()

    debt_comments = re.findall(DEBT_PATTERN, content)
    ticketed_comments = re.findall(TICKET_PATTERN, content)

    if len(debt_comments) > len(ticketed_comments):
        print(f"{filepath}: Debt comments must include ticket reference")
        print("Example: TODO(PROJ-123): description")
        return False
    return True

if __name__ == "__main__":
    all_good = all(check_file(f) for f in sys.argv[1:])
    sys.exit(0 if all_good else 1)
```

## Anti-patterns

- **Ignoring debt**: Pretending it doesn't exist
- **Gold plating**: Over-engineering to avoid all debt
- **Debt denial**: "It's not debt, it's just how we do things"
- **Big bang payoff**: Trying to fix everything at once
- **No tracking**: Debt invisible to stakeholders
- **Blame culture**: Punishing debt creation vs. managing it

## References

- [Technical Debt - Martin Fowler](https://martinfowler.com/bliki/TechnicalDebt.html)
- [Managing Technical Debt](https://www.amazon.com/Managing-Technical-Debt-Reducing-Development/dp/0135645824)
- [The Pragmatic Programmer](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/)
- [Refactoring: Improving the Design of Existing Code](https://refactoring.com/)
