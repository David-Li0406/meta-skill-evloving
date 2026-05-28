# HELM Benchmark Onboarder Skill

A Claude Code skill for onboarding AI creativity benchmarks into HELM-compliant Scenario implementations.

## Installation

Copy this folder to your project's `.claude/skills/` directory:

```
.claude/skills/benchmark-onboarder/
├── SKILL.md           # Main skill instructions
├── helm-template.md   # HELM Scenario code patterns
├── benchmarks.json    # Queue of benchmarks to onboard
└── examples/
    ├── brainteaser.py # Lateral thinking puzzles, 4-choice MC
    ├── analobench.py  # Analogical reasoning, 4-choice MC
    └── riddlesense.py # Riddles + commonsense, 5-choice MC
```

## Usage

Once installed, Claude will automatically activate this skill when you say things like:

- "Onboard the BRAINTEASER benchmark"
- "Create a HELM scenario for this paper"
- "Process this benchmark into evaluation code"

Or invoke directly with `/benchmark-onboarder`.

## What It Does

1. **Qualifies** benchmarks (creativity-focused, has prompts, has evaluation)
2. **Extracts** the exact prompt from the paper (never invents prompts)
3. **Examines** the dataset structure
4. **Generates** a HELM-compliant `scenario.py` file
5. **Verifies** the code works before delivery

## Output Format

Generated scenarios follow HELM conventions:

```python
from helm.benchmark.scenarios.scenario import (
    Scenario, Instance, Input, Output, Reference,
    CORRECT_TAG, TEST_SPLIT
)

class MyBenchmarkScenario(Scenario):
    name = "my_benchmark"
    description = "source/dataset-name"
    tags = ["creativity", "relevant_tag"]

    def get_instances(self, output_path):
        # Load data and return Instance objects
        ...
```

## Benchmark Queue

See `benchmarks.json` for the current list of benchmarks. Each entry contains:
- `name`: Benchmark name
- `paper_id`: Semantic Scholar paper ID
- `url`: Dataset or repo URL
- `status`: "completed" or absent (pending)
- `scenario_file`: Path to generated scenario (if completed)

## Requirements

- Claude Code CLI or VS Code extension
- Python 3.8+
- `datasets` library for HuggingFace datasets
- `helm` package for HELM integration
