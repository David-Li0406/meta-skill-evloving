# Best Practices - DSPy Optimization

Patterns and practices learned from successful Phase 1-3 implementation.

## Signature Design

### Use Literal Types for Enums

✅ **Good**:
```python
from typing import Literal

class AnalyzeIntent(dspy.Signature):
    """Analyze user intent."""
    task_description: str = dspy.InputField()
    domain: Literal["python", "web", "devops", "testing"] = dspy.OutputField()
    target_level: Literal["beginner", "intermediate", "advanced"] = dspy.OutputField()
```

❌ **Bad**:
```python
class AnalyzeIntent(dspy.Signature):
    task_description: str = dspy.InputField()
    domain: str = dspy.OutputField()  # Too generic
    target_level: str = dspy.OutputField()  # No constraints
```

**Why**: Literal types constrain outputs at the type level, improving consistency and making invalid states unrepresentable.

### Add Quality Indicators to OutputField Descriptions

✅ **Good**:
```python
skill_content: str = dspy.OutputField(
    desc="Production-ready SKILL.md content with quality score >0.80, "
    "includes 3-5 concrete examples, copy-paste ready code snippets"
)
```

❌ **Bad**:
```python
skill_content: str = dspy.OutputField(
    desc="The content of the skill"
)
```

**Why**: Specific constraints guide the LM toward better outputs and align with evaluation metrics.

### Keep Docstrings Concise and Actionable

✅ **Good**:
```python
class GenerateSkill(dspy.Signature):
    """Generate production-ready skill content with examples and best practices."""
    task: str = dspy.InputField()
    content: str = dspy.OutputField()
```

❌ **Bad**:
```python
class GenerateSkill(dspy.Signature):
    """This signature is used to generate skill content. The skill should be
    comprehensive and include examples. It should follow best practices and be
    ready for production use. The content should be well-structured..."""
```

**Why**: LMs respond better to concise directives. Save verbose explanations for field descriptions.

## Training Data

### Aim for 50-100 Diverse Examples

✅ **Good**:
- 50 examples across 18 categories
- Mix of comprehensive (38), navigation_hub (11), minimal (1) styles
- Combination of golden (15) + extracted (9) + synthetic (26)

❌ **Bad**:
- 10-20 examples (insufficient)
- All from one category (not diverse)
- All one style (doesn't generalize)

**Why**: DSPy optimizers need 50-100 examples for robust optimization. Fewer examples lead to overfitting.

### Use Both Real and Synthetic Examples

```python
# Real examples (extracted from skills)
real_examples = extract_from_skills(skills_dir)

# Synthetic examples (for underrepresented categories)
synthetic_examples = generate_synthetic_examples(
    categories=["database", "architecture", "security"],
    count_per_category=3,
)

# Combine
trainset = real_examples + synthetic_examples
```

**Why**: Real examples provide grounding, synthetic examples fill gaps in category distribution.

### Validate Training Data Structure

```python
def validate_trainset(trainset: list[dict]) -> bool:
    """Validate trainset structure."""
    required_fields = ["task_description"]
    
    for i, example in enumerate(trainset):
        # Check required fields
        missing = [f for f in required_fields if f not in example]
        if missing:
            print(f"Example {i}: Missing fields {missing}")
            return False
        
        # Check field types
        if not isinstance(example["task_description"], str):
            print(f"Example {i}: task_description must be string")
            return False
    
    return True
```

**Why**: Invalid training data causes cryptic errors during optimization.

## Optimization Strategy

### Start with GEPA for Quick Iteration

```python
# Phase 1: Quick baseline with GEPA (2-5 minutes)
gepa = dspy.GEPA(metric=metric, num_candidates=5, num_iters=2)
baseline = gepa.compile(program, trainset=trainset)

# Evaluate
baseline_score = evaluate(baseline, testset)
print(f"GEPA baseline: {baseline_score:.3f}")
```

**Why**: GEPA is 5-10x faster than MIPROv2, good for initial experiments.

### Use MIPROv2 auto="medium" for Production

```python
# Phase 2: Production optimization with MIPROv2
mipro = dspy.MIPROv2(
    metric=metric,
    auto="medium",  # Balanced cost/quality
    num_threads=8,
)

optimized = mipro.compile(
    program,
    trainset=trainset,
    max_bootstrapped_demos=2,  # Conservative for speed
    max_labeled_demos=2,
    num_candidate_programs=8,  # Reduced from default 16
)
```

**Why**: `auto="medium"` provides 80% of the quality gains at 30% of the cost of `auto="heavy"`.

### Always Use Separate Test Set

```python
# ✅ Good: Separate train/test
trainset, testset = train_test_split(examples, test_size=0.2, random_state=42)

optimizer.compile(program, trainset=trainset)
test_score = evaluate(program, testset)  # Unbiased estimate
```

```python
# ❌ Bad: Evaluate on training set
optimizer.compile(program, trainset=examples)
score = evaluate(program, examples)  # Overly optimistic!
```

**Why**: Evaluating on training data gives inflated scores that don't reflect real performance.

## Monitoring & Observability

### Wrap Critical Modules with ModuleMonitor

```python
from skill_fleet.core.dspy.monitoring import ModuleMonitor, ExecutionTracer

tracer = ExecutionTracer(max_traces=1000)

# Wrap expensive modules
generator = GenerateSkillContentModule()
monitored_generator = ModuleMonitor(
    generator,
    name="skill_content_generator",
    tracer=tracer,
    quality_metric=lambda x: score_skill_quality(x.skill_content),
)

# Use normally
result = monitored_generator(task="Create async skill")

# Check metrics
metrics = monitored_generator.get_metrics()
print(f"Success rate: {metrics['success_rate']:.2%}")
print(f"Avg quality: {metrics['avg_quality_score']:.3f}")
```

**Why**: Production visibility helps identify bottlenecks and quality issues.

### Export Traces for Analysis

```python
# Collect traces during operation
for task in tasks:
    result = monitored_module(task=task)

# Periodically export
if execution_count % 100 == 0:
    tracer.export_traces(f"traces_{execution_count}.json")
    tracer.clear()  # Prevent memory growth
```

**Why**: Trace analysis helps identify patterns in failures and quality issues.

## Error Handling

### Use RobustModule for Critical Operations

```python
from skill_fleet.core.dspy.modules.error_handling import RobustModule

# Wrap unreliable module
unreliable = SomeExternalAPIModule()
robust = RobustModule(
    unreliable,
    name="external_api",
    max_retries=3,
    retry_delay=1.0,  # Exponential backoff
    fallback_fn=lambda **kwargs: safe_default_response(),
)

# Handles transient failures gracefully
result = robust(query="test")
```

**Why**: External APIs, LMs, and network calls can fail. Retries with backoff handle transient failures.

### Validate Outputs Before Returning

```python
from skill_fleet.core.dspy.modules.error_handling import ValidatedModule

def validate_skill_output(result):
    """Validate skill generation output."""
    if not hasattr(result, "skill_content"):
        raise ValueError("Missing skill_content field")
    
    if len(result.skill_content) < 100:
        raise ValueError("Skill content too short")
    
    if "# " not in result.skill_content:
        raise ValueError("Skill missing header")
    
    return True

validated = ValidatedModule(
    generator,
    validator=validate_skill_output,
    raise_on_invalid=True,
)
```

**Why**: Catch invalid outputs early before they propagate through the system.

## Ensemble Methods

### Use BestOfN for Critical Generations

```python
from skill_fleet.core.dspy.modules.ensemble import BestOfN

generator = dspy.ChainOfThought("task -> skill_content")

best_of_3 = BestOfN(
    module=generator,
    n=3,
    quality_fn=lambda x: score_skill_quality(x.skill_content),
)

# Generates 3 candidates, returns highest quality
result = best_of_3(task="Create async Python skill")
```

**Why**: Multiple attempts improve quality for critical outputs. 3-5 is optimal (diminishing returns after that).

### Use MajorityVote for Classification

```python
from skill_fleet.core.dspy.modules.ensemble import MajorityVote

classifiers = [model1, model2, model3]

voter = MajorityVote(
    modules=classifiers,
    vote_field="category",
    min_agreement=0.66,  # Require 2/3 agreement
)

result = voter(text="Sample skill description")
```

**Why**: Consensus reduces errors in classification tasks.

## Caching

### Cache Expensive Operations

```python
from skill_fleet.core.dspy.caching import CachedModule

expensive_module = LargeModelInference()

cached = CachedModule(
    expensive_module,
    cache_dir=".cache/inference",
    ttl_seconds=86400,  # 24 hour TTL
    use_memory=True,  # Memory + disk caching
)

# First call: executes module (slow)
result1 = cached(input="test")

# Second call with same input: cached (instant)
result2 = cached(input="test")

# Check cache stats
stats = cached.get_stats()
print(f"Hit rate: {stats['hit_rate']:.2%}")
```

**Why**: Caching can improve performance by 30-50% for deterministic operations.

## Versioning & A/B Testing

### Use ProgramRegistry for Version Management

```python
from skill_fleet.core.dspy.versioning import ProgramRegistry

registry = ProgramRegistry("config/optimized")

# Register new version after optimization
registry.register(
    program=optimized_v2,
    name="skill_generator_v2",
    optimizer="miprov2",
    quality_score=0.87,
    training_examples=50,
)

# Load for production
production_program = registry.load("skill_generator_v2")

# Compare versions
comparison = registry.compare(
    "skill_generator_v1",
    "skill_generator_v2",
)
print(f"Quality improvement: {comparison['quality_diff']:+.3f}")
```

**Why**: Track multiple versions, enable rollback, compare performance.

### Gradual Rollout with ABTestRouter

```python
from skill_fleet.core.dspy.versioning import ABTestRouter

router = ABTestRouter(
    variants={
        "v1": program_v1,  # Current production
        "v2": program_v2,  # New optimized version
    },
    weights={
        "v1": 0.9,  # 90% of traffic
        "v2": 0.1,  # 10% of traffic
    },
    strategy="weighted",
)

# Route requests
result = router(task="Generate skill", user_id=user_id)

# Monitor performance
stats = router.get_stats()
for variant, metrics in stats.items():
    print(f"{variant}: {metrics['success_rate']:.2%} success")
```

**Why**: Gradual rollout reduces risk when deploying new optimized versions.

## Common Pitfalls to Avoid

❌ **Don't optimize on <50 examples** - Leads to overfitting  
❌ **Don't skip baseline evaluation** - You need a comparison point  
❌ **Don't use auto="heavy" by default** - Usually not worth the cost  
❌ **Don't ignore type errors** - They cause runtime failures  
❌ **Don't skip monitoring** - You're flying blind without it  
❌ **Don't cache non-deterministic operations** - Defeats the purpose  
❌ **Don't deploy without version management** - Makes rollback impossible  
❌ **Don't forget train/test split** - Evaluation will be biased
