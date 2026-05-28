# Phase 1 Implementation Guide

Complete walkthrough of Phase 1: Foundation (signatures, training data, monitoring).

## Overview

**Goal**: Prepare DSPy programs for effective optimization  
**Duration**: 1-2 days  
**Prerequisites**: Basic DSPy knowledge, Python 3.12+

**Deliverables**:
1. Enhanced signatures with Literal types
2. Training dataset with 50-100 examples
3. Monitoring infrastructure for production

## Task 1: Signature Enhancements

### Step 1: Add Literal Types

**Files to modify**: `src/skill_fleet/core/dspy/signatures/*.py`

**Pattern**:
```python
# Before
class MySignature(dspy.Signature):
    domain: str = dspy.OutputField()
    skill_type: str = dspy.OutputField()

# After
from typing import Literal

class MySignature(dspy.Signature):
    domain: Literal["python", "web", "devops", "testing"] = dspy.OutputField()
    skill_type: Literal["guide", "reference", "workflow"] = dspy.OutputField()
```

**Complete list of Literal types** (from our implementation):
- `Domain`: python, web, devops, testing, api, database, architecture, practices, domain, memory
- `TargetLevel`: beginner, intermediate, advanced
- `SkillType`: guide, reference, workflow, troubleshooting
- `SkillLength`: short, medium, long
- `SkillStyle`: comprehensive, navigation_hub, minimal

### Step 2: Add Specific Constraints to OutputFields

**Pattern**:
```python
# Before
skill_content: str = dspy.OutputField(desc="The generated skill content")

# After
skill_content: str = dspy.OutputField(
    desc="Production-ready SKILL.md content with quality score >0.80, "
    "includes 3-5 concrete examples, copy-paste ready code snippets, "
    "uses ✅/❌ good/bad contrast patterns"
)
```

**Quality indicators to include**:
- Score thresholds ("quality >0.80")
- Count expectations ("3-5 examples", "2-4 key insights")
- Format requirements ("copy-paste ready", "executable code")
- Pattern expectations ("✅/❌ contrast", "progressive disclosure")

### Step 3: Concise Docstrings

**Pattern**:
```python
# Before
class GenerateSkill(dspy.Signature):
    """This signature is used to generate skill content for the skills-fleet platform.
    The generated content should be comprehensive and include various sections such as
    examples, best practices, common mistakes, and should follow the Obra/superpowers
    quality standards..."""

# After
class GenerateSkill(dspy.Signature):
    """Generate production-ready skill content with examples and best practices."""
```

**Rule**: 1-2 sentences max, focus on WHAT not HOW.

### Verification

```bash
# Type check
uv run ty check src/skill_fleet/core/dspy/signatures/ --quiet

# Should pass with no errors (MLflow warnings OK)
```

## Task 2: Training Data Expansion

### Step 1: Extract from Existing Skills

**Script**: `scripts/expand_training_data.py`

```bash
# Run extraction
uv run python scripts/expand_training_data.py

# Output: config/training/trainset_v3.json
```

**What it does**:
- Scans `.skills/` and promoted `skills/` directories
- Parses SKILL.md frontmatter
- Extracts task_description, taxonomy_path, metadata
- Detects skill style (comprehensive, navigation_hub, minimal)

### Step 2: Generate Synthetic Examples

**Script**: `scripts/generate_synthetic_examples.py`

```bash
# Generate 26 synthetic examples
uv run python scripts/generate_synthetic_examples.py

# Output: Added to trainset_v4.json
```

**Categories to cover**:
- Underrepresented domains (security, ml, data)
- Different target levels (beginner, advanced)
- All 3 skill styles
- Various skill types (guide, reference, troubleshooting)

### Step 3: Validate Final Dataset

```bash
# Check size (should be 50-100)
jq length config/training/trainset_v4.json

# Check diversity
jq '[.[].expected_skill_style] | group_by(.) | map({style: .[0], count: length})' config/training/trainset_v4.json

# Validate structure
uv run python -c "
import json
with open('config/training/trainset_v4.json') as f:
    data = json.load(f)
    print(f'✅ Valid JSON with {len(data)} examples')
    assert all('task_description' in ex for ex in data)
    print('✅ All examples have task_description')
"
```

### Expected Distribution

**Size**: 50 examples  
**Styles**: ~70% comprehensive, ~20% navigation_hub, ~10% minimal  
**Categories**: Represent all major domains (aim for 10+ categories)  
**Sources**: Mix of golden (30%), extracted (20%), synthetic (50%)

## Task 3: Monitoring Infrastructure

### Step 1: Create Monitoring Package

**Directory**: `src/skill_fleet/core/dspy/monitoring/`

**Files to create**:
1. `__init__.py` - Package exports
2. `module_monitor.py` - ModuleMonitor class
3. `execution_tracer.py` - ExecutionTracer and TraceEntry
4. `mlflow_logger.py` - MLflowLogger (optional)
5. `README.md` - Usage documentation

### Step 2: Implement ModuleMonitor

```python
# src/skill_fleet/core/dspy/monitoring/module_monitor.py

class ModuleMonitor(dspy.Module):
    def __init__(self, module, name, tracer=None, quality_metric=None):
        super().__init__()
        self.module = module
        self.name = name
        self.tracer = tracer or ExecutionTracer()
        self.quality_metric = quality_metric
    
    def forward(self, **kwargs):
        trace = self.tracer.start_trace(self.name, inputs=kwargs)
        
        try:
            result = self.module(**kwargs)
            
            if self.quality_metric:
                trace.quality_score = self.quality_metric(result)
            
            self.tracer.end_trace(trace, success=True)
            return result
        
        except Exception as e:
            self.tracer.end_trace(trace, success=False, error=str(e))
            raise
```

### Step 3: Use in Production

```python
from skill_fleet.core.dspy.monitoring import ModuleMonitor, ExecutionTracer

# Create shared tracer
tracer = ExecutionTracer(max_traces=1000)

# Wrap critical modules
generator = GenerateSkillContentModule()
monitored = ModuleMonitor(
    generator,
    name="skill_generator",
    tracer=tracer,
    quality_metric=lambda x: score_quality(x.skill_content),
)

# Use normally
result = monitored(task="Create skill")

# Check metrics anytime
metrics = monitored.get_metrics()
print(f"Success rate: {metrics['success_rate']:.2%}")
print(f"Avg quality: {metrics['avg_quality_score']:.3f}")

# Export for analysis
tracer.export_traces("production_traces.json")
```

## Verification Checklist

After completing Phase 1:

- [ ] All signatures have Literal types where appropriate
- [ ] OutputField descriptions include quality indicators
- [ ] Docstrings are concise (1-2 sentences)
- [ ] Training data has 50-100 examples
- [ ] Training data covers all major categories
- [ ] Training data includes all 3 skill styles
- [ ] JSON structure validated
- [ ] Monitoring package created and tested
- [ ] ModuleMonitor successfully wraps test module
- [ ] ExecutionTracer collects and exports traces
- [ ] All type checks pass (`uv run ty check src/`)

## Next Steps

After Phase 1 completion:
1. **Baseline Evaluation**: Test unoptimized program on held-out test set
2. **Phase 2**: Run optimization with improved signatures and training data
3. **Monitoring**: Integrate ModuleMonitor into production workflow
4. **Documentation**: Update project docs with new patterns

## Estimated Timeline

- Signature enhancements: 2-4 hours
- Training data expansion: 3-5 hours
- Monitoring infrastructure: 2-3 hours
- **Total**: 1-2 days for complete Phase 1

## Common Issues

**Type errors after adding Literals**:
- Add `from __future__ import annotations`
- Import from `typing` module
- Run type checker to verify

**Training data extraction fails**:
- Check SKILL.md files have valid YAML frontmatter
- Verify frontmatter includes `name` and `description`
- Check file encoding is UTF-8

**Monitoring overhead too high**:
- Set `log_inputs=False, log_outputs=False`
- Remove quality_metric parameter
- Reduce max_traces limit
