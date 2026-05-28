---
name: pytorch-lightning
description: Use this skill when building, training, or deploying neural networks with PyTorch Lightning, organizing code into LightningModules, and configuring multi-GPU/TPU training.
---

# PyTorch Lightning

## Overview

PyTorch Lightning is a deep learning framework that organizes PyTorch code to eliminate boilerplate while maintaining full flexibility. It automates training workflows, manages multi-device orchestration, and implements best practices for neural network training and scaling across multiple GPUs/TPUs.

## When to Use This Skill

This skill should be used when:
- Building, training, or deploying neural networks using PyTorch Lightning
- Organizing PyTorch code into LightningModules
- Configuring Trainers for multi-GPU/TPU training
- Implementing data pipelines with LightningDataModules
- Working with callbacks, logging, and distributed training strategies (DDP, FSDP, DeepSpeed)
- Structuring deep learning projects professionally

## Core Capabilities

### 1. LightningModule - Model Definition

Organize PyTorch models into six logical sections:

1. **Initialization** - `__init__()` and `setup()`
2. **Training Loop** - `training_step(batch, batch_idx)`
3. **Validation Loop** - `validation_step(batch, batch_idx)`
4. **Test Loop** - `test_step(batch, batch_idx)`
5. **Prediction** - `predict_step(batch, batch_idx)`
6. **Optimizer Configuration** - `configure_optimizers()`

### 2. Trainer - Training Automation

The Trainer automates the training loop, device management, gradient operations, and callbacks. Key features include:

- Multi-GPU/TPU support with strategy selection (DDP, FSDP, DeepSpeed)
- Automatic mixed precision training
- Gradient accumulation and clipping
- Checkpointing and early stopping
- Progress bars and logging

### 3. LightningDataModule - Data Pipeline Organization

Encapsulate all data processing steps in a reusable class, including methods for preparing and loading data.

## Additional Resources

For quick setup references and detailed documentation, refer to the official PyTorch Lightning documentation.