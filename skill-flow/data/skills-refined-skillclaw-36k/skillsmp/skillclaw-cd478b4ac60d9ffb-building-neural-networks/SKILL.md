---
name: building-neural-networks
description: Use this skill when you need to create or modify neural network architectures for specific machine learning tasks using the neural-network-builder plugin.
---

# Skill body

## Overview

This skill empowers Claude to design and implement neural networks tailored to specific tasks. It leverages the neural-network-builder plugin to automate the process of defining network architectures, configuring layers, and setting training parameters, ensuring efficient and accurate creation of neural network models.

## How It Works

1. **Analyzing Requirements**: Claude analyzes the user's request to understand the desired neural network architecture, task, and performance goals.
2. **Generating Configuration**: Based on the analysis, Claude generates the appropriate configuration for the neural-network-builder plugin, specifying the layers, activation functions, and other relevant parameters.
3. **Executing Build**: Claude executes the `build-nn` command, triggering the neural-network-builder plugin to construct the neural network based on the generated configuration.

## When to Use This Skill

This skill activates when you need to:
- Create a new neural network architecture for a specific machine learning task.
- Modify an existing neural network's layers, parameters, or training process.
- Design a neural network using specific layer types, such as convolutional, recurrent, or transformer layers.

## Examples

### Example 1: Image Classification

User request: "Build a convolutional neural network for image classification with three convolutional layers and two fully connected layers."

The skill will:
1. Analyze the request and determine the required CNN architecture.
2. Generate the configuration for the `build-nn` command, specifying the layer types, filter sizes, and activation functions.

### Example 2: Text Generation

User request: "Define an RNN architecture for text generation with LSTM cells and an embedding layer."

The skill will:
1. Analyze the request and determine the required RNN architecture.
2. Generate the configuration for the `build-nn` command, specifying the necessary layers and parameters.