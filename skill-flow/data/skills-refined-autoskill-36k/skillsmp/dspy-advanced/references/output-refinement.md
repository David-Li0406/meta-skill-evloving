# DSPy Output Refinement

Improve output quality through multiple attempts (BestOfN) or iterative refinement (Refine). This guide covers refinement strategies and patterns.

## Table of Contents

- [Output Refinement Overview](#output-refinement-overview)
- [BestOfN](#bestofn)
- [Refine](#refine)
- [Comparison](#comparison)
- [Reward Functions](#reward-functions)
- [Best Practices](#best-practices)

## Output Refinement Overview

### Why Refine Output?

- **Better quality**: Higher quality outputs through multiple attempts
- **Robustness**: Handle edge cases better
- **Consistency**: More reliable results
- **Confidence**: Select best from multiple candidates

### Refinement Strategies

1. **BestOfN**: Generate N candidates and select best
2. **Refine**: Iteratively improve with feedback loop

## BestOfN

### Basic BestOfN

Generate multiple candidates and select the best based on reward function:

```python
import dspy

def one_word_answer(args, pred: dspy.Prediction) -> float:
    """Reward function: 1.0 for single word, 0.0 otherwise."""
    return 1.0 if len(pred.answer.split()) == 1 else 0.0

best_of_3 = dspy.BestOfN(
    module=dspy.ChainOfThought("question -> answer"),
    N=3,
    reward_fn=one_word_answer,
    threshold=1.0
)

result = best_of_3(question="What is the capital of Belgium?")
print(result.answer)  # Brussels
```

### How BestOfN Works

1. **Generate N candidates**: Run module N times with different rollout IDs
2. **Score each candidate**: Apply reward function to each prediction
3. **Select best**: Return first prediction that meets threshold or highest-scoring result

### BestOfN Parameters

- `module`: Base module to refine
- `N`: Number of candidates to generate
- `reward_fn`: Function to score predictions (returns float)
- `threshold`: Minimum score to accept (optional)

### BestOfN Without Threshold

```python
best_of_5 = dspy.BestOfN(
    module=dspy.ChainOfThought("question -> answer"),
    N=5,
    reward_fn=accuracy_reward_fn
)

result = best_of_5(question="What is 2+2?")
# Returns highest-scoring prediction, even if below 1.0
```

## Refine

### Basic Refine

Iteratively improve output with automatic feedback loop:

```python
def one_word_answer(args, pred: dspy.Prediction) -> float:
    """Reward function: 1.0 for single word, 0.0 otherwise."""
    return 1.0 if len(pred.answer.split()) == 1 else 0.0

refine = dspy.Refine(
    module=dspy.ChainOfThought("question -> answer"),
    N=3,
    reward_fn=one_word_answer,
    threshold=1.0
)

result = refine(question="What is the capital of Belgium?")
print(result.answer)  # Brussels
```

### How Refine Works

1. **Generate candidate**: Run module to get initial prediction
2. **Score candidate**: Apply reward function
3. **Generate feedback**: If score below threshold, generate detailed feedback
4. **Refine**: Use feedback as hints for next attempt
5. **Iterate**: Repeat until threshold met or N attempts exhausted

### Refine Parameters

- `module`: Base module to refine
- `N`: Maximum number of refinement attempts
- `reward_fn`: Function to score predictions
- `threshold`: Minimum score to accept
- `fail_count`: Stop after N failed attempts (optional)

### Refine with Custom Feedback

```python
def factuality_reward(args, pred: dspy.Prediction) -> float:
    """Reward function for factual correctness."""
    # Use LLM to judge factuality
    judge = dspy.Predict(FactualityJudge)
    result = judge(
        statement=pred.answer,
        context=args.context
    )
    return 1.0 if result.is_factual else 0.0

refine = dspy.Refine(
    module=dspy.ChainOfThought("question -> answer"),
    N=3,
    reward_fn=factuality_reward,
    threshold=1.0
)
```

## Comparison

### BestOfN vs Refine

| Aspect | BestOfN | Refine |
|---------|----------|---------|
| **Strategy** | Generate N independent candidates | Iterate with feedback loop |
| **Speed** | Faster (parallel candidates) | Slower (sequential with feedback) |
| **Quality** | Good for simple improvements | Better for complex refinements |
| **Feedback** | No feedback between attempts | Automatic feedback generation |
| **Use Case** | Select best from multiple candidates | Iteratively improve with learning |

### When to Use BestOfN

- Need to generate multiple candidates quickly
- Independent attempts are sufficient
- Simple reward functions
- Parallel processing available

### When to Use Refine

- Need iterative improvement
- Want feedback between attempts
- Complex reward functions
- Sequential refinement preferred

## Reward Functions

### Exact Match Reward

```python
def exact_match_reward(args, pred: dspy.Prediction) -> float:
    """1.0 for exact match, 0.0 otherwise."""
    return 1.0 if args.expected == pred.answer else 0.0
```

### Length Constraint Reward

```python
def length_reward(args, pred: dspy.Prediction) -> float:
    """Reward based on answer length."""
    target_length = getattr(args, 'target_length', 50)
    actual_length = len(pred.answer)

    if actual_length == target_length:
        return 1.0
    elif actual_length < target_length * 1.5:
        return 0.5
    else:
        return 0.0
```

### Keyword Presence Reward

```python
def keyword_reward(args, pred: dspy.Prediction) -> float:
    """Reward based on keyword presence."""
    required_keywords = args.keywords
    answer = pred.answer.lower()

    keyword_count = sum(1 for kw in required_keywords if kw.lower() in answer)
    return keyword_count / len(required_keywords)
```

### Factual Correctness Reward

```python
class FactualityJudge(dspy.Signature):
    """Judge if statement is factually correct."""
    statement = dspy.InputField(desc="Statement to evaluate")
    context = dspy.InputField(desc="Context for evaluation")
    is_factual = dspy.OutputField(desc="True if factual, False otherwise")

def factuality_reward(args, pred: dspy.Prediction) -> float:
    """Reward based on factual correctness."""
    judge = dspy.Predict(FactualityJudge)
    result = judge(
        statement=pred.answer,
        context=args.context
    )
    return 1.0 if result.is_factual else 0.0
```

### Multi-Criteria Reward

```python
def multi_criteria_reward(args, pred: dspy.Prediction) -> float:
    """Weighted average of multiple criteria."""
    criteria = {
        'accuracy': args.expected == pred.answer,
        'length': 10 <= len(pred.answer) <= 1000,
        'format': '|' in pred.answer  # Check for specific format
    }

    weights = {'accuracy': 0.5, 'length': 0.3, 'format': 0.2}
    score = sum(criteria[k] * weights[k] for k in criteria)

    return score
```

## Best Practices

### 1. Define Clear Reward Functions

```python
# Good: Clear, specific reward function
def single_word_reward(args, pred: dspy.Prediction) -> float:
    """
    Reward single-word answers.

    Returns:
        float: 1.0 for single word, 0.0 otherwise
    """
    return 1.0 if len(pred.answer.split()) == 1 else 0.0

# Bad: Ambiguous reward function
def vague_reward(args, pred: dspy.Prediction) -> float:
    """Reward good answers."""
    return 1.0 if "good" in pred.answer else 0.0
```

### 2. Use Appropriate Thresholds

```python
# Good: Appropriate threshold based on task
refine = dspy.Refine(
    module=module,
    N=3,
    reward_fn=factuality_reward,
    threshold=1.0  # Require factual correctness
)

# Bad: Too low threshold
refine = dspy.Refine(
    module=module,
    N=3,
    reward_fn=factuality_reward,
    threshold=0.1  # Too lenient
)
```

### 3. Set Reasonable N Values

```python
# Good: Appropriate N for task complexity
best_of_3 = dspy.BestOfN(module=module, N=3, reward_fn=reward_fn)

# Bad: Too high N (wasteful)
best_of_10 = dspy.BestOfN(module=module, N=10, reward_fn=reward_fn)
```

### 4. Use fail_count for Refine

```python
# Good: Stop after first error
refine = dspy.Refine(
    module=module,
    N=3,
    reward_fn=reward_fn,
    threshold=1.0,
    fail_count=1  # Stop after first error
)
```

### 5. Test Reward Functions

```python
# Good: Test reward function before using
def test_reward_function():
    class Args:
        expected = "Brussels"
        context = "Capital of Belgium"

    class Pred:
        answer = "Paris"

    pred = Pred()
    score = exact_match_reward(Args(), pred)
    assert score == 0.0  # Should fail for wrong answer

test_reward_function()
```

## Common Issues and Solutions

### Issue: All Candidates Fail Threshold

**Problem**: No candidate meets threshold, returns best (or last) candidate

**Solution**:
1. Lower threshold
2. Increase N (more candidates)
3. Improve reward function
4. Check if task is feasible

### Issue: Refine Doesn't Improve

**Problem**: Refine iterations don't improve output

**Solution**:
1. Check reward function provides useful feedback
2. Improve feedback generation in Refine
3. Increase N (more attempts)
4. Try different module or signature

### Issue: Slow Refinement

**Problem**: BestOfN or Refine takes too long

**Solution**:
1. Reduce N (fewer candidates/iterations)
2. Use simpler base module (without ChainOfThought)
3. Cache expensive reward function calculations
4. Parallelize BestOfN candidates

### Issue: Reward Function Biases Output

**Problem**: Reward function leads to biased or unexpected outputs

**Solution**:
1. Review reward function for unintended incentives
2. Add multiple criteria
3. Test with diverse examples
4. Use human evaluation samples
