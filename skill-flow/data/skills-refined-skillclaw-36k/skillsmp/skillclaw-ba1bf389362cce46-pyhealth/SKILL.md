---
name: pyhealth
description: Use this skill when developing, testing, and deploying machine learning models with clinical data, particularly in healthcare settings involving electronic health records (EHR) and clinical prediction tasks.
---

# PyHealth: Healthcare AI Toolkit

## Overview

PyHealth is a comprehensive Python library designed for healthcare AI, providing specialized tools, models, and datasets for clinical machine learning. This skill is essential for developing healthcare prediction models, processing clinical data, and deploying AI solutions in healthcare environments.

## When to Use This Skill

Invoke this skill when:

- **Working with healthcare datasets**: MIMIC-III, MIMIC-IV, eICU, OMOP, sleep EEG data, medical images
- **Clinical prediction tasks**: Mortality prediction, hospital readmission, length of stay, drug recommendation
- **Medical coding**: Translating between ICD-9/10, NDC, RxNorm, ATC coding systems
- **Processing clinical data**: Sequential events, physiological signals, clinical text, medical images
- **Implementing healthcare models**: RETAIN, SafeDrug, GAMENet, StageNet, Transformer for EHR
- **Evaluating clinical models**: Fairness metrics, calibration, interpretability, uncertainty quantification

## Core Capabilities

PyHealth operates through a modular 5-stage pipeline optimized for healthcare AI:

1. **Data Loading**: Access 10+ healthcare datasets with standardized interfaces.
2. **Task Definition**: Apply 20+ predefined clinical prediction tasks or create custom tasks.
3. **Model Selection**: Choose from 33+ models (baselines, deep learning, healthcare-specific).
4. **Training**: Train with automatic checkpointing, monitoring, and evaluation.
5. **Deployment**: Calibrate, interpret, and validate for clinical use.

**Performance**: 3x faster than pandas for healthcare data processing.

## Quick Start Workflow

```python
from pyhealth.datasets import MIMIC4Dataset
from pyhealth.tasks import mortality_prediction_mimic4_fn
from pyhealth.datasets import split_by_patient, get_dataloader
from pyhealth.models import Transformer
from pyhealth.trainer import Trainer

# 1. Load dataset and set task
dataset = MIMIC4Dataset(root="path/to/dataset")
task = mortality_prediction_mimic4_fn()
dataloader = get_dataloader(dataset, task)
trainer = Trainer(model=Transformer(), dataloader=dataloader)

# 2. Train the model
trainer.train()

# 3. Evaluate the model
trainer.evaluate()
```