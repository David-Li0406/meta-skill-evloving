---
name: setting-up-experiment-tracking
description: Use this skill when you need to automate the setup of machine learning experiment tracking using tools like MLflow or Weights & Biases (W&B).
---

# Skill body

## Overview

This skill streamlines the process of setting up experiment tracking for machine learning projects. It automates environment configuration, tool initialization, and provides code examples to get you started quickly.

## How It Works

1. **Analyze Context**: The skill analyzes the current project context to determine the appropriate experiment tracking tool (MLflow or W&B) based on user preference or existing project configuration.
2. **Configure Environment**: It configures the environment by installing necessary Python packages and setting environment variables.
3. **Initialize Tracking**: The skill initializes the chosen tracking tool, potentially starting a local MLflow server or connecting to a W&B project.
4. **Provide Code Snippets**: It provides code snippets demonstrating how to log experiment parameters, metrics, and artifacts within your ML code.

## When to Use This Skill

This skill activates when you need to:
- Start tracking machine learning experiments in a new project.
- Integrate experiment tracking into an existing ML project.
- Quickly set up MLflow or Weights & Biases for experiment management.
- Automate the process of logging parameters, metrics, and artifacts.

## Examples

### Example 1: Starting a New Project with MLflow

User request: "track experiments using mlflow"

The skill will:
1. Install the `mlflow` Python package.
2. Generate example code for logging parameters, metrics, and artifacts to an MLflow server.

### Example 2: Integrating W&B into an Existing Project

User request: "setup experiment tracking with wandb"

The skill will:
1. Install the `wandb` Python package.
2. Generate example code for initializing W&B and logging experiment data.

## Best Practices

- **Tool Selection**: Consider the scale and complexity of your project when choosing between MLflow and W&B. MLflow is well-suited for local tracking, while W&B offers cloud-based solutions for collaboration and visualization.