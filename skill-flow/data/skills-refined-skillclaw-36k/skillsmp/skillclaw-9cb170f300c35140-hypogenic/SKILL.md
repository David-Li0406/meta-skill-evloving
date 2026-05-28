---
name: hypogenic
description: Use this skill when you want to systematically explore hypotheses about patterns in empirical data, leveraging automated LLM-driven hypothesis generation and testing.
---

# Hypogenic

## Overview

Hypogenic provides automated hypothesis generation and testing using large language models to accelerate scientific discovery. The framework supports three approaches: HypoGeniC (data-driven hypothesis generation), HypoRefine (synergistic literature and data integration), and Union methods (mechanistic combination of literature and data-driven hypotheses).

## Quick Start

Get started with Hypogenic in minutes:

```bash
# Install the package
uv pip install hypogenic

# Clone example datasets
git clone https://github.com/ChicagoHAI/HypoGeniC-datasets.git ./data

# Run basic hypothesis generation
hypogenic_generation --config ./data/your_task/config.yaml --method hypogenic --num_hypotheses 20

# Run inference on generated hypotheses
hypogenic_inference --config ./data/your_task/config.yaml --hypotheses output/hypotheses.json
```

**Or use Python API:**

```python
from hypogenic import BaseTask

# Create task with your configuration
task = BaseTask(config_path="./data/your_task/config.yaml")

# Generate hypotheses
task.generate_hypotheses(method="hypogenic", num_hypotheses=20)

# Run inference
results = task.inference(hypothesis_bank="./output/hypotheses.json")
```

## When to Use This Skill

Use this skill when working on:
- Generating scientific hypotheses from observational datasets
- Testing multiple competing hypotheses systematically
- Combining literature insights with empirical patterns
- Accelerating research discovery through automated hypothesis ideation
- Domains requiring hypothesis-driven analysis: deception detection, AI-generated content identification, mental health indicators, predictive modeling, or other empirical research

## Key Features

**Automated Hypothesis Generation**
- Generate 10-20+ testable hypotheses from data in minutes
- Iterative refinement based on validation performance
- Support for both API-based (OpenAI, Anthropic) and local LLMs

**Literature Integration**
- Extract insights from research papers via PDF processing