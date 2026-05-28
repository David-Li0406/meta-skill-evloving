# Troubleshooting Guide - DSPy Optimization

Common issues and solutions when optimizing DSPy programs in skills-fleet.

## Low Quality Scores (<0.70)

### Symptom
After optimization, quality scores remain below 0.70, or improvement is minimal.

### Possible Causes & Solutions

**1. Insufficient Training Data**
```bash
# Check training set size
jq length config/training/trainset_v4.json

# Should be 50-100 examples minimum
```

✅ **Solution**: Expand training data
```bash
# Extract more examples
uv run python scripts/expand_training_data.py

# Generate synthetic examples
uv run python scripts/generate_synthetic_examples.py
```

**2. Training Data Not Diverse**
```bash
# Check category distribution
jq '[.[].expected_taxonomy_path] | group_by(.) | map({category: .[0], count: length})' config/training/trainset_v4.json
```

✅ **Solution**: Add examples from underrepresented categories

**3. Metric Too Strict**
```python
# Test metric on examples
def test_metric():
    from skill_fleet.core.dspy.metrics.enhanced_metrics import comprehensive_metric
    import dspy
    
    # Load examples
    examples = load_trainset("config/training/trainset_v4.json")
    
    # Test metric on first 10
    for ex in examples[:10]:
        # Create mock prediction matching example
        pred = dspy.Prediction(
            taxonomy_path=ex.expected_taxonomy_path,
            skill_metadata=MockMetadata(),
            skill_style=ex.expected_skill_style,
        )
        
        score = comprehensive_metric(ex, pred)
        print(f"Example score: {score:.3f}")
```

✅ **Solution**: Adjust metric weights or thresholds if too many examples score <0.5

**4. Signature Constraints Conflicting**
```python
# Check if OutputField constraints are contradictory
# Example: "concise, 1-2 words" AND "include detailed explanation"
```

✅ **Solution**: Review signature descriptions for consistency

## API Optimization Job Fails

### Symptom
POST `/optimization/start` returns error or job status shows "failed"

### Possible Causes & Solutions

**1. Trainset File Not Found**
```bash
# Check file exists
ls -la config/training/trainset_v4.json

# Check path is relative to repo root
pwd
```

✅ **Solution**: Use correct relative path from repo root

**2. Invalid JSON Structure**
```bash
# Validate JSON
jq . config/training/trainset_v4.json > /dev/null && echo "Valid JSON" || echo "Invalid JSON"

# Check required fields
jq '.[0] | keys' config/training/trainset_v4.json
# Should include: task_description
```

✅ **Solution**: Fix JSON structure or regenerate trainset

**3. API Server Not Running**
```bash
# Check if server is running
curl http://localhost:8000/health

# If not, start it
uv run skill-fleet serve
```

**4. Missing API Key**
```bash
# Check environment variable
echo $GOOGLE_API_KEY

# If empty, set it
export GOOGLE_API_KEY=your_api_key_here
```

✅ **Solution**: Set required environment variables in `.env`

**5. Memory/CPU Limits**
```bash
# Check system resources
top  # or htop

# Optimization is memory-intensive (can use 4-8GB RAM)
```

✅ **Solution**: 
- Close other applications
- Reduce `num_candidate_programs` (16 → 8)
- Use `auto="light"` instead of "medium"

## Type Errors in Signatures

### Symptom
```
error[invalid-type-form]: Function `callable` is not valid in a type expression
error[unresolved-reference]: Name `Literal` used when not defined
```

### Solutions

**1. Missing Import**
```python
# ✅ Add to imports
from __future__ import annotations
from typing import Literal, Callable
```

**2. Wrong Type Syntax**
```python
# ❌ Bad
def my_function() -> callable:
    pass

# ✅ Good
from typing import Callable

def my_function() -> Callable:
    pass
```

**3. Check with Type Checker**
```bash
# Run type checker
uv run ty check src/skill_fleet/core/dspy/ --quiet

# Fix errors before running optimization
```

## Optimization Too Slow

### Symptom
MIPROv2 optimization takes >30 minutes

### Solutions

**1. Use GEPA Instead**
```python
# GEPA is 5-10x faster than MIPROv2
optimizer = dspy.GEPA(metric=metric, num_candidates=5, num_iters=2)
optimized = optimizer.compile(program, trainset=trainset)
```

**2. Reduce MIPROv2 Search Space**
```python
optimizer = dspy.MIPROv2(
    metric=metric,
    auto="light",  # Instead of "medium" or "heavy"
)

optimized = optimizer.compile(
    program,
    trainset=trainset,
    max_bootstrapped_demos=2,  # Reduce from 4
    num_candidate_programs=8,  # Reduce from 16
)
```

**3. Use Smaller Training Set**
```python
# Use subset for initial experiments
trainset_small = trainset[:20]

# Optimize
optimized = optimizer.compile(program, trainset=trainset_small)

# Once working, scale up to full 50-100 examples
```

## Import Errors

### Symptom
```
ModuleNotFoundError: No module named 'skill_fleet.core.dspy.monitoring'
ImportError: cannot import name 'ModuleMonitor'
```

### Solutions

**1. Check Module Exists**
```bash
# Verify file exists
ls -la src/skill_fleet/core/dspy/monitoring/

# Check __init__.py has exports
cat src/skill_fleet/core/dspy/monitoring/__init__.py
```

**2. Reinstall Package**
```bash
# Sync dependencies
uv sync

# Install in editable mode
uv pip install -e .
```

**3. Check Python Path**
```python
import sys
print(sys.path)

# Should include project root
```

## Optimization Score Doesn't Improve

### Symptom
Optimized score ≈ baseline score (no meaningful improvement)

### Possible Causes & Solutions

**1. Metric Returns Same Score for All Outputs**
```python
# Debug metric
def debug_metric(example, pred, trace=None):
    score = your_metric(example, pred, trace)
    print(f"Metric score: {score:.3f} for prediction: {pred}")
    return score

# Should see variation in scores (not all 0.0 or all 1.0)
```

✅ **Solution**: Fix metric to provide gradient (range of scores)

**2. Training Data Too Similar**
```bash
# Check diversity
jq '[.[].task_description] | unique | length' config/training/trainset_v4.json

# Should be close to total count (little duplication)
```

✅ **Solution**: Add more diverse examples

**3. Program Already Optimal**
- Baseline score >0.85 means program is already good
- Diminishing returns after certain point

✅ **Solution**: Focus on other improvements (performance, monitoring)

## MLflow Warnings

### Symptom
```
warning[possibly-missing-attribute]: Member `log_params` may be missing on module `mlflow`
```

### Solution
**These are expected** - MLflow is an optional dependency. Warnings are safe to ignore if:
- You don't plan to use MLflow tracking
- The count is exactly 11 warnings (all from mlflow_logger.py)

To eliminate warnings:
```bash
# Install MLflow
uv pip install mlflow
```

Or suppress warnings:
```python
# Add type ignore comment
import mlflow  # type: ignore[import-untyped]
```

## Getting Help

**Check logs**:
```bash
# API server logs
tail -f logs/skill-fleet.log

# Background job logs
grep "optimization" logs/skill-fleet.log
```

**Enable debug logging**:
```python
import logging
logging.getLogger("skill_fleet.core.dspy").setLevel(logging.DEBUG)
```

**Run comprehensive tests**:
```bash
uv run python scripts/test_phase_implementation.py
```

**Check DSPy status**:
```python
import dspy
print(f"DSPy version: {dspy.__version__}")
print(f"Configured LM: {dspy.settings.lm}")
```
