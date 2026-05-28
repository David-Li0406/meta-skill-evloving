---
name: transformers
description: Use this skill when working with pre-trained transformer models for natural language processing, computer vision, audio, or multimodal tasks. It is suitable for tasks such as text generation, classification, question answering, translation, summarization, image classification, object detection, speech recognition, and fine-tuning models on custom datasets.
---

# Transformers

## Overview

The Hugging Face Transformers library provides access to thousands of pre-trained models for tasks across NLP, computer vision, audio, and multimodal domains. Use this skill to load models, perform inference, and fine-tune on custom data.

## Installation

Install transformers and core dependencies:

```bash
pip install torch transformers datasets evaluate accelerate
```

For vision tasks, add:

```bash
pip install timm pillow
```

For audio tasks, add:

```bash
pip install librosa soundfile
```

## Authentication

Many models on the Hugging Face Hub require authentication. Set up access:

```python
from huggingface_hub import login
login()  # Follow prompts to enter token
```

Or set the environment variable:

```bash
export HUGGINGFACE_TOKEN="your_token_here"
```

Get tokens at: https://huggingface.co/settings/tokens

## Quick Start

Use the Pipeline API for fast inference without manual configuration:

```python
from transformers import pipeline

# Text generation
generator = pipeline("text-generation", model="gpt2")
result = generator("The future of AI is", max_length=50)

# Text classification
classifier = pipeline("text-classification")
result = classifier("This movie was excellent!")

# Question answering
qa = pipeline("question-answering")
result = qa(question="What is AI?", context="AI is artificial intelligence...")
```

## Core Capabilities

### 1. Pipelines for Quick Inference

Use for simple, optimized inference across many tasks. Supports text generation, classification, NER, question answering, summarization, translation, image classification, object detection, audio classification, and more.

**When to use**: Quick prototyping, simple inference tasks, no custom preprocessing needed.

### 2. Model Loading and Management

Load pre-trained models with fine-grained control over configuration, device placement, and precision.

**When to use**: Custom model initialization, advanced device management, model inspection.