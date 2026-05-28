# DSPy Metrics

Metrics evaluate how well your DSPy program performs on test data. This guide covers common metrics and custom metric patterns.

## Table of Contents

- [Defining Metrics](#defining-metrics)
- [Common Metrics](#common-metrics)
- [Semantic Metrics](#semantic-metrics)
- [Custom Metrics](#custom-metrics)
- [Multi-Criteria Metrics](#multi-criteria-metrics)
- [Best Practices](#best-practices)

## Defining Metrics

### Metric Function Signature

A metric function evaluates program performance:

```python
def my_metric(example, pred, trace=None):
    """
    Custom metric for evaluation.

    Args:
        example: The ground truth example
        pred: The program's prediction
        trace: Optional execution trace for debugging

    Returns:
        bool or float: True/1.0 for success, False/0.0 for failure
    """
    return example.output == pred.output
```

### Using Metrics in Optimization

```python
# Define metric
def quality_metric(example, pred, trace=None):
    return example.quality_score >= pred.quality_score

# Use in teleprompter
teleprompter = dspy.BootstrapFewShot(
    metric=quality_metric,
    max_labeled_demos=5
)

compiled = teleprompter.compile(program, trainset=trainset)
```

## Common Metrics

### Exact Match

```python
def exact_match(example, pred, trace=None):
    """Exact string matching."""
    return example.output == pred.output
```

### Case-Insensitive Match

```python
def case_insensitive_match(example, pred, trace=None):
    """Case-insensitive string matching."""
    return example.output.lower() == pred.output.lower()
```

### Keyword Match

```python
def keyword_match(example, pred, trace=None):
    """Check if required keywords are present."""
    required_keywords = example.keywords
    output = pred.output.lower()
    return all(keyword.lower() in output for keyword in required_keywords)
```

## Semantic Metrics

### Semantic Similarity

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def semantic_similarity(example, pred, trace=None):
    """
    Semantic similarity using sentence embeddings.
    Returns float between 0 and 1.
    """
    emb1 = model.encode(example.output)
    emb2 = model.encode(pred.output)
    similarity = (emb1 @ emb2.T).item()
    return similarity > 0.8  # Threshold
```

### SemanticF1 with Decompositional Mode

```python
from dspy.evaluate import SemanticF1

# Instantiate the metric
metric = SemanticF1(decompositional=True)

# Produce a prediction
pred = program(**example.inputs())

# Evaluate
score = metric(example, pred)
```

**When to use SemanticF1:**
- Need semantic overlap rather than exact match
- Want to measure coverage of key facts
- Complex answers with multiple components

**Parameters:**
- `decompositional`: Enable decompositional mode for better coverage
- `model`: Custom sentence transformer model (optional)

## Custom Metrics

### Structured Evaluation

```python
def structured_metric(example, pred, trace=None):
    """Multi-field structured evaluation."""
    score = 0

    # Check required fields
    if hasattr(pred, 'summary') and pred.summary:
        score += 0.3

    if hasattr(pred, 'keywords') and pred.keywords:
        score += 0.3

    # Check quality
    if hasattr(pred, 'confidence') and pred.confidence > 0.7:
        score += 0.4

    return score >= 0.7  # Threshold
```

### Format Validation

```python
def format_metric(example, pred, trace=None):
    """Validate output format."""
    try:
        # Parse output as JSON
        import json
        data = json.loads(pred.output)

        # Check required keys
        if 'answer' not in data:
            return False

        if 'confidence' not in data:
            return False

        return True
    except json.JSONDecodeError:
        return False
```

### Length Constraints

```python
def length_metric(example, pred, trace=None):
    """Ensure output meets length constraints."""
    min_length = getattr(example, 'min_length', 10)
    max_length = getattr(example, 'max_length', 1000)

    output_length = len(pred.output)

    return min_length <= output_length <= max_length
```

## Multi-Criteria Metrics

### Weighted Average

```python
def multi_criteria_metric(example, pred, trace=None):
    """Multi-criteria metric with weighted average."""
    criteria = {
        'accuracy': example.output == pred.output,
        'completeness': len(pred.output) >= len(example.output) * 0.8,
        'relevance': any(keyword in pred.output for keyword in example.keywords)
    }

    # Weighted average
    weights = {'accuracy': 0.5, 'completeness': 0.3, 'relevance': 0.2}
    score = sum(criteria[k] * weights[k] for k in criteria)

    return score >= 0.6  # Threshold
```

### All Criteria Must Pass

```python
def strict_metric(example, pred, trace=None):
    """All criteria must pass."""
    criteria = {
        'accuracy': example.output == pred.output,
        'format': '|' in pred.output,  # Check format
        'length': 10 < len(pred.output) < 1000
    }

    return all(criteria.values())
```

### At Least One Criteria Must Pass

```python
def lenient_metric(example, pred, trace=None):
    """At least one criterion must pass."""
    criteria = {
        'exact_match': example.output == pred.output,
        'semantic_match': semantic_similarity(example, pred),
        'keyword_match': keyword_match(example, pred)
    }

    return any(criteria.values())
```

## Best Practices

### 1. Return Float Scores

```python
# Good: Return float score
def quality_metric(example, pred, trace=None):
    score = 0.0
    if example.output == pred.output:
        score += 0.5
    if len(pred.output) > 50:
        score += 0.5
    return score

# Bad: Return only bool
def bad_metric(example, pred, trace=None):
    return example.output == pred.output
```

### 2. Use Trace for Debugging

```python
def debug_metric(example, pred, trace=None):
    """Metric with debugging information."""
    if trace:
        print(f"Trace: {trace}")

    result = example.output == pred.output

    if not result:
        print(f"Expected: {example.output}")
        print(f"Got: {pred.output}")

    return result
```

### 3. Handle Missing Attributes

```python
def robust_metric(example, pred, trace=None):
    """Handle missing attributes gracefully."""
    # Check if attribute exists
    if hasattr(pred, 'quality_score'):
        return pred.quality_score > 0.8

    # Fallback metric
    return example.output == pred.output
```

### 4. Document Metrics

```python
def factuality_metric(example, pred, trace=None):
    """
    Metric for factual correctness.

    Uses LLM to evaluate if prediction is factually correct
    based on the ground truth.

    Args:
        example: Must have 'output' and 'context' fields
        pred: Must have 'output' field

    Returns:
        float: Score between 0 and 1
    """
    # Implementation
    pass
```

### 5. Use Consistent Thresholds

```python
# Define thresholds at module level
ACCURACY_THRESHOLD = 0.8
CONFIDENCE_THRESHOLD = 0.7
LENGTH_MIN = 10
LENGTH_MAX = 1000

def combined_metric(example, pred, trace=None):
    """Use consistent thresholds."""
    accuracy = example.output == pred.output
    confidence = getattr(pred, 'confidence', 0)
    length = LENGTH_MIN <= len(pred.output) <= LENGTH_MAX

    return accuracy and confidence > CONFIDENCE_THRESHOLD and length
```

## Common Issues and Solutions

### Issue: Metric Too Strict

**Problem**: No examples pass the metric

**Solution**:
1. Lower thresholds
2. Use lenient criteria (at least one must pass)
3. Debug which criteria are failing
4. Check example data quality

### Issue: Metric Too Lenient

**Problem**: All examples pass the metric

**Solution**:
1. Raise thresholds
2. Add more criteria
3. Use strict mode (all must pass)
4. Add negative test cases

### Issue: Slow Metric Evaluation

**Problem**: Metrics take too long to evaluate

**Solution**:
1. Cache expensive computations
2. Use approximate metrics
3. Parallelize metric evaluation
4. Reduce dataset size for tuning

### Issue: Metric Not Aligned with Task

**Problem**: Good metric score but poor task performance

**Solution**:
1. Review metric definition with domain experts
2. Add human evaluation samples
3. Correlate metric with human judgments
4. Use multiple metrics for different aspects
