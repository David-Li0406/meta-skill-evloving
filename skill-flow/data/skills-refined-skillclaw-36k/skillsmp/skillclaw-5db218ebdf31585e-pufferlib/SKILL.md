---
name: pufferlib
description: Use this skill when you need a high-performance reinforcement learning framework optimized for speed and scale, particularly for fast parallel training and multi-agent systems.
---

# PufferLib - High-Performance Reinforcement Learning

## Overview

PufferLib is a high-performance reinforcement learning library designed for fast parallel environment simulation and training. It achieves training at millions of steps per second through optimized vectorization, native multi-agent support, and an efficient PPO implementation (PuffeRL). The library provides the Ocean suite of 20+ environments and seamless integration with Gymnasium, PettingZoo, and specialized RL frameworks.

## When to Use This Skill

Use this skill when:
- **Training RL agents** with PPO on any environment (single or multi-agent)
- **Creating custom environments** using the PufferEnv API
- **Optimizing performance** for parallel environment simulation (vectorization)
- **Integrating existing environments** from Gymnasium, PettingZoo, Atari, Procgen, etc.
- **Developing policies** with CNN, LSTM, or custom architectures
- **Scaling RL** to millions of steps per second for faster experimentation
- **Multi-agent RL** with native multi-agent environment support

## Core Capabilities

### 1. High-Performance Training (PuffeRL)

PuffeRL is PufferLib's optimized PPO+LSTM training algorithm achieving 1M-4M steps/second.

**Quick start training:**
```bash
# CLI training
puffer train procgen-coinrun --train.device cuda --train.learning-rate 3e-4

# Distributed training
torchrun --nproc_per_node=4 train.py
```

**Python training loop:**
```python
import pufferlib
from pufferlib import PuffeRL

# Create vectorized environment
env = pufferlib.make('procgen-coinrun', num_envs=256)

# Create trainer
trainer = PuffeRL(
    env=env,
    policy=my_policy,
    device='cuda',
    learning_rate=3e-4,
    batch_size=32768
)

# Training loop
for iteration in range(num_iterations):
    trainer.evaluate()  # Collect rollouts
    trainer.train()     # Train on batch
    trainer.mean_and_log()  # Log results
```