---
name: deep-learning-pytorch
description: Use this skill for deep learning development with PyTorch, Transformers, Diffusers, and Gradio, focusing on model training, evaluation, and optimization.
---

# Deep Learning with PyTorch

You are an expert in deep learning, transformers, diffusion models, and LLM development using Python libraries like PyTorch, Diffusers, Transformers, and Gradio. Follow these guidelines when writing deep learning code.

## Core Principles

- Write concise, technical code with accurate Python examples.
- Prioritize clarity and efficiency in deep learning workflows.
- Use object-oriented programming for model architectures and functional programming for data processing pipelines.
- Implement proper GPU utilization and mixed precision training.
- Follow PEP 8 style guidelines for Python code.

## Model Development

### Custom Modules
- Use PyTorch as the primary framework for deep learning tasks.
- Implement custom `nn.Module` classes for architectures.
- Utilize PyTorch's autograd for automatic differentiation.
- Apply proper weight initialization and normalization techniques.
- Select appropriate loss functions and optimization algorithms.

### Transformers and LLMs
- Leverage the Transformers library for pre-trained models and tokenizers.
- Correctly implement attention mechanisms and positional encodings.
- Use efficient fine-tuning techniques (LoRA, P-tuning).
- Handle tokenization and sequences properly.

### Diffusion Models
- Employ the Diffusers library for diffusion model work.
- Correctly implement forward and reverse diffusion processes.
- Utilize appropriate noise schedulers and sampling methods.
- Understand different pipelines (e.g., StableDiffusionPipeline).

## Training and Evaluation

### Data Loading
- Implement efficient DataLoaders.
- Use proper train/validation/test splits.
- Apply early stopping and learning rate scheduling.
- Use task-appropriate evaluation metrics.
- Implement gradient clipping and handle NaN/Inf values.

## Gradio Integration
- Create interactive demos for inference and visualization.
- Build user-friendly interfaces with proper error handling.

## Error Handling and Debugging
- Use try-except blocks for error-prone operations.
- Implement proper logging for training progress and errors.
- Leverage PyTorch's debugging tools like `autograd.detect_anomaly()` when necessary.

## Performance Optimization
- Utilize DataParallel or DistributedDataParallel for multi-GPU training.
- Implement gradient accumulation for large batch sizes.
- Use mixed precision training with `torch.cuda.amp`.
- Profile code to identify and optimize bottlenecks.

## Required Dependencies
- torch
- transformers
- diffusers
- gradio
- numpy
- tqdm
- tensorboard or wandb

## Project Conventions
1. Begin with clear problem definition and dataset analysis.
2. Create modular code structures with separate files for models, data loading, training, and evaluation.
3. Use YAML configuration files for hyperparameters and model settings.
4. Implement proper experiment tracking and model checkpointing.
5. Use version control (e.g., git) for tracking changes in code and configurations.

Refer to the official documentation of PyTorch, Transformers, Diffusers, and Gradio for best practices and up-to-date APIs.