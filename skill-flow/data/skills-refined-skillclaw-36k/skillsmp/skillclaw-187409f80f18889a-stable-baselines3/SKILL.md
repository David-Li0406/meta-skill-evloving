---
name: stable-baselines3
description: Use this skill when you need to implement and train reinforcement learning agents using the Stable Baselines3 library with Gymnasium environments.
---

# Stable Baselines3

## Overview

Stable Baselines3 (SB3) is a PyTorch-based library providing reliable implementations of reinforcement learning algorithms. This skill offers comprehensive guidance for training RL agents, creating custom environments, implementing callbacks, and optimizing training workflows using SB3's unified API.

## Core Capabilities

### 1. Training RL Agents

**Basic Training Pattern:**

```python
import gymnasium as gym
from stable_baselines3 import PPO

# Create environment
env = gym.make("CartPole-v1")

# Initialize agent
model = PPO("MlpPolicy", env, verbose=1)

# Train the agent
model.learn(total_timesteps=10000)

# Save the model
model.save("ppo_cartpole")

# Load the model (without prior instantiation)
model = PPO.load("ppo_cartpole", env=env)
```

**Important Notes:**
- `total_timesteps` is a lower bound; actual training may exceed this due to batch collection.
- Use `model.load()` as a static method, not on an existing instance.
- The replay buffer is NOT saved with the model to save space.

**Algorithm Selection:**
Quick reference for algorithm characteristics:
- **PPO/A2C**: General-purpose, supports all action space types, good for multiprocessing.
- **SAC/TD3**: Continuous control, off-policy, sample-efficient.
- **DQN**: Discrete actions, off-policy.
- **HER**: Goal-conditioned tasks.

### 2. Custom Environments

**Requirements:**
Custom environments must inherit from `gymnasium.Env` and implement:
- `__init__()`: Define action_space and observation_space.
- `reset(seed, options)`: Return initial observation and info dict.
- `step(action)`: Return observation, reward, terminated, truncated, info.
- `render()`: Visualization (optional).
- `close()`: Cleanup resources.

**Key Constraints:**
- Image observations must be `np.uint8` in range [0, 255].
- Use channel-first format when possible (channels, height, width).