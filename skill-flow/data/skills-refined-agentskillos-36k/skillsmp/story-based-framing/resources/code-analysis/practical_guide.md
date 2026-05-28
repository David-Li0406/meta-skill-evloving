# Practical Guide: Story-Based Framing for Code Analysis

This guide shows how to apply story-based framing to common code analysis tasks: linting, code review, refactoring, and architectural analysis.

## Use Case 1: Automated Linting Detection

### Objective

Identify code anti-patterns during automated linting/static analysis.

### Applying Story-Based Framing

**Traditional checklist approach**:

```yaml
rules:
  - check: Generic[T] class exists
  - check: Union types in fields
  - check: isinstance() checks present
  - check: type: ignore comments exist
```

**Story-based approach**:

```yaml
pattern: "The Fake Generic"
act1_promise: "Class inherits Generic[T]"
act2_betrayal: "Constructor accepts Union instead of T"
act3_consequences: "isinstance() checks AND type suppressions"
act4_source: "Values from heterogeneous storage"
```

**Why it's better**: Acts 1+2 uniquely identify the pattern immediately, Acts 3+4 verify it's not a false positive.

### Implementation Example

```python
def detect_fake_generic_pattern(tree: ast.Module) -> list[Detection]:
    """Detect union-polluted Generic[T] classes using story-based criteria."""

    # Act 1: Find Generic[T] declarations (most distinctive)
    generic_classes = find_classes_inheriting_from(tree, "Generic")

    for cls in generic_classes:
        # Act 2: Check if constructor accepts union (second most distinctive)
        constructor = get_init_method(cls)
        if not has_union_parameter(constructor):
            continue  # Not this pattern, move to next

        # Acts 3+4: Verify symptoms and source
        if has_isinstance_checks(cls) and has_type_suppressions(cls):
            # Pattern confirmed
            yield Detection(
                class_name=cls.name,
                promise="Declares Generic[T]",
                betrayal=f"Constructor accepts {get_union_type(constructor)}",
                consequences=count_isinstance_and_suppressions(cls),
                source=find_heterogeneous_storage_origin(cls)
            )
```

## Use Case 2: Code Review Automation

### Objective

Create automated code review comments that explain WHY something is problematic.

### Applying Story-Based Framing

**Traditional review comment**:

> ❌ "This code has type: ignore comments and uses isinstance() checks. Please fix."

**Story-based review comment**:

> ⚠️ **Pattern Detected: "The Fake Generic"**
>
> **The Promise**: `TemplateExpander` declares `Generic[T]` suggesting it will preserve type information.
>
> **The Betrayal**: But the constructor accepts `raw_value: ConfigValue` (a union type) instead of `raw_value: T`, losing type safety.
>
> **The Consequences**: This forces methods to use runtime `isinstance()` checks (lines 369, 520, 558) and requires 5 `# type: ignore` suppressions to satisfy the type checker.
>
> **The Source**: Values come from `BuildConfig._values: dict[str, str | list[str]]` where specific type information is lost.
>
> **Suggested Fix**: Use TypeGuard to narrow the union BEFORE instantiation:
>
> ```python
> def get_expander(self, key: str) -> TemplateExpander[str] | TemplateExpander[list[str]]:
>     value = self._values[key]
>     if is_str(value):
>         return TemplateExpander(value, self)  # T = str
>     else:
>         return TemplateExpander(value, self)  # T = list[str]
> ```

**Why it's better**: Explains the causal chain from promise → betrayal → consequences → source, helping developers understand the root cause.

## Use Case 3: Refactoring Prioritization

### Objective

Prioritize which code smells to fix first based on how distinctive they are.

### Applying Story-Based Framing

**Act 1 patterns** (most distinctive, highest priority):

- Structural violations that uniquely identify the problem
- Example: Generic[T] with union storage

**Act 2 patterns** (medium priority):

- Implementation violations
- Example: Mutable default arguments

**Act 3 patterns** (lower priority):

- Symptom cleanup after fixing Acts 1-2
- Example: Removing isinstance() checks that are no longer needed

**Refactoring workflow**:

```python
# Priority 1: Fix Act 1+2 (structural issue)
1. Change constructor signature: raw_value: ConfigValue → raw_value: T
2. Add TypeGuards at call sites

# Priority 2: Fix Act 4 (source)
3. Consider if heterogeneous storage design needs refactoring

# Priority 3: Cleanup Act 3 (consequences)
4. Remove isinstance() checks that are now unnecessary
5. Remove type: ignore comments
6. Remove @overload bandaids
```

## Use Case 4: Architecture Analysis

### Objective

Identify systemic issues vs. isolated mistakes.

### Applying Story-Based Framing

**Isolated Pattern**:

- Act 4 (Source): "Added during emergency hotfix 6 months ago"
- **Action**: Local fix, no broader architectural changes needed

**Systemic Pattern**:

- Act 4 (Source): "All services store configuration in heterogeneous dicts"
- **Action**: Requires architectural refactoring across multiple services

### Detection Strategy

```python
def analyze_pattern_scope(detections: list[Detection]) -> ArchitectureReport:
    """Determine if pattern is isolated or systemic using Act 4."""

    sources = [d.source for d in detections]

    # Check if Act 4 sources point to same root cause
    if same_architectural_decision(sources):
        return ArchitectureReport(
            scope="SYSTEMIC",
            impact="HIGH",
            recommendation="Refactor storage layer across all services",
            affected_components=get_affected_components(sources)
        )
    else:
        return ArchitectureReport(
            scope="ISOLATED",
            impact="MEDIUM",
            recommendation="Fix individual occurrences locally",
            affected_components=get_affected_files(detections)
        )
```

## Integration with CI/CD

### Pre-Commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Run story-based pattern detector
python scripts/detect_patterns.py --style narrative

# Exit code:
# 0 = no patterns detected
# 1 = patterns detected, block commit
# 2 = patterns detected, warn but allow
```

### GitHub Actions Workflow

```yaml
name: Code Pattern Analysis

on: [pull_request]

jobs:
  detect-patterns:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Run story-based pattern detector
        run: |
          python scripts/detect_patterns.py \
            --format github-review-comment \
            --pr-number ${{ github.event.pull_request.number }}

      - name: Post review comments
        uses: actions/github-script@v6
        with:
          script: |
            // Read detection results and post as review comments
            // Each comment includes full 4-act narrative
```

## Best Practices for Code Analysis

### 1. Start with Acts 1-2 (Most Distinctive)

Don't search for symptoms first:

- ❌ Search for: "type: ignore comments"
- ✅ Search for: "Generic[T] with union constructor"

### 2. Use Acts 3-4 for Verification

After finding Act 1-2 matches, verify with Acts 3-4:

```python
# Found Generic[T] with union constructor
if has_isinstance_checks(cls):  # Act 3
    if from_heterogeneous_storage(cls):  # Act 4
        # Confirmed pattern
```

### 3. Provide Full Narrative in Reports

Never just list symptoms:

- ❌ "5 type: ignore comments found"
- ✅ "Generic[T] promises type safety → stores Union → requires 5 suppressions → from dict with union values"

### 4. Prioritize by Act

Fix in order:

1. Act 2 (betrayal) - Core violation
2. Act 4 (source) - Root cause
3. Act 3 (consequences) - Cleanup symptoms

### 5. Track Pattern Evolution

Monitor how patterns spread:

```python
# Track pattern instances over time
commit_1: 1 instance (Act 4: "Emergency hotfix")
commit_50: 5 instances (Act 4: "Copy-pasted from original")
commit_100: 15 instances (Act 4: "Became standard pattern")
# → Time to address systemically
```

## Tools and Libraries

### Recommended Stack

```python
# Pattern detection
import ast  # Parse Python code
from typing import TypeGuard  # For fix suggestions

# Static analysis integration
import mypy.api
import ruff

# Reporting
from dataclasses import dataclass

@dataclass
class StoryBasedDetection:
    """Detection result using four-act structure."""
    location: str
    act1_promise: str
    act2_betrayal: str
    act3_consequences: list[str]
    act4_source: str
    suggested_fix: str
```

### Integration Points

1. **Pre-commit**: Fast local detection before commit
2. **CI/CD**: Automated detection on PR/MR
3. **IDE plugins**: Real-time detection while coding
4. **Code review tools**: Automated review comments

## Metrics and Measurement

Track effectiveness of story-based approach:

```python
# Before story-based framing
average_false_positives = 45  # per 100 detections
average_fix_time = 2.5  # hours per issue
developer_understanding = 65  # % who understand why it's wrong

# After story-based framing
average_false_positives = 12  # 73% reduction
average_fix_time = 0.8  # 68% faster
developer_understanding = 92  # 42% improvement
```

## Common Pitfalls

### Pitfall 1: Starting with Act 3

❌ "Find all isinstance() checks"

- Result: Too many matches, many false positives

✅ "Find Generic[T] with union storage, THEN check for isinstance()"

- Result: Targeted, accurate matches

### Pitfall 2: Ignoring Act 4

❌ "Fix each occurrence individually"

- Result: Pattern keeps recurring

✅ "Identify Act 4 source, fix root cause"

- Result: Pattern stops spreading

### Pitfall 3: Incomplete Narrative

❌ "Code has type errors"

- Result: Developer doesn't know WHY or HOW to fix

✅ "Generic[T] promises type safety but stores Union, causing type errors from heterogeneous dict"

- Result: Developer understands causal chain and proper fix

## Further Reading

- See `experiment_results.md` for validation data
- See `example_patterns.md` for more code pattern examples
- See parent `SKILL.md` for general story-based framing principles
