# HELM Scenario Template

Reference for generating HELM-compliant Scenario classes.

## Basic Structure

```python
from helm.benchmark.scenarios.scenario import (
    Scenario, Instance, Input, Output, Reference,
    CORRECT_TAG, TEST_SPLIT
)
from datasets import load_dataset

class MyScenario(Scenario):
    name = "my_benchmark"
    description = "source/dataset-name"
    tags = ["creativity"]

    def get_instances(self, output_path):
        dataset = load_dataset("source/dataset", split="test")

        instances = []
        for item in dataset:
            # Format prompt inline
            prompt = f"Question: {item['question']}"

            # Build references inline (see patterns below)
            references = [Reference(Output(text=item['answer']), tags=[CORRECT_TAG])]

            instances.append(Instance(
                input=Input(text=prompt),
                references=references,
                split=TEST_SPLIT
            ))
        return instances
```

## Reference Patterns

### Multiple Choice
ALL choices become References. Only correct one gets CORRECT_TAG.

```python
references = []
for i, choice in enumerate(choices):
    letter = chr(65 + i)  # A, B, C, D
    is_correct = (i == correct_index)
    tags = [CORRECT_TAG] if is_correct else []
    references.append(Reference(Output(text=letter), tags=tags))
```

### Binary (Yes/No)
Both options are References.

```python
references = [
    Reference(Output(text="Yes"), tags=[CORRECT_TAG] if label == 1 else []),
    Reference(Output(text="No"), tags=[CORRECT_TAG] if label == 0 else [])
]
```

### Single Answer
```python
references = [Reference(Output(text=str(answer)), tags=[CORRECT_TAG])]
```

### Open-Ended (No Correct Answer)
```python
references = []  # Empty is fine for divergent thinking tasks
```

## Key Rules

1. `name` = lowercase with underscores
2. `description` = data source reference (NOT task description)
3. `tags` = include "creativity" plus relevant category
4. Always use `CORRECT_TAG` for correct answers
5. Always specify `split` (usually `TEST_SPLIT`)
