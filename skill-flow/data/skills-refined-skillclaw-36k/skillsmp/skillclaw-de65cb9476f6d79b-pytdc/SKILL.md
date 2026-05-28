---
name: pytdc
description: Use this skill when you need access to AI-ready datasets and benchmarks for drug discovery and development, including molecular property predictions and drug-target interactions.
---

# PyTDC (Therapeutics Data Commons)

## Overview

PyTDC is an open-science platform providing AI-ready datasets and benchmarks for drug discovery and development. It offers curated datasets spanning the entire therapeutics pipeline with standardized evaluation metrics and meaningful data splits, organized into three categories: single-instance prediction (molecular/protein properties), multi-instance prediction (drug-target interactions, DDI), and generation (molecule generation, retrosynthesis).

## When to Use This Skill

This skill should be used when:
- Working with drug discovery or therapeutic ML datasets
- Benchmarking machine learning models on standardized pharmaceutical tasks
- Predicting molecular properties (ADME, toxicity, bioactivity)
- Predicting drug-target or drug-drug interactions
- Generating novel molecules with desired properties
- Accessing curated datasets with proper train/test splits (scaffold, cold-split)
- Using molecular oracles for property optimization

## Installation & Setup

Install PyTDC using pip:

```bash
pip install PyTDC
```

To upgrade to the latest version:

```bash
pip install PyTDC --upgrade
```

Core dependencies (automatically installed):
- numpy, pandas, tqdm, seaborn, scikit_learn, fuzzywuzzy

Additional packages are installed automatically as needed for specific features.

## Quick Start

The basic pattern for accessing any TDC dataset follows this structure:

```python
from tdc.<problem> import <Task>
data = <Task>(name='<Dataset>')
split = data.get_split(method='scaffold', seed=1, frac=[0.7, 0.1, 0.2])
df = data.get_data(format='df')
```

Where:
- `<problem>`: One of `single_pred`, `multi_pred`, or `generation`
- `<Task>`: Specific task category (e.g., ADME, DTI, MolGen)
- `<Dataset>`: Dataset name within that task

**Example - Loading ADME data:**

```python
from tdc.single_pred import ADME
data = ADME(name='Caco2_Wang')
split = data.get_split(method='scaffold')
# Returns dict with 'train', 'valid', 'test' DataFrames
```

## Single-Instance Prediction Tasks

Single-instance prediction involves forecasting properties of individual biomedical entities (molecules, proteins, etc.).

### Available Task Categories

#### 1. ADME (Absorption, Distribution, Metabolism, Excretion)
Predict pharmacokinetic properties of compounds.