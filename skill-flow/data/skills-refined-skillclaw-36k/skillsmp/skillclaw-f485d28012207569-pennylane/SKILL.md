---
name: pennylane
description: Use this skill when you need a hardware-agnostic quantum machine learning framework for training quantum circuits via gradients, building hybrid quantum-classical models, or ensuring device portability across various quantum hardware platforms.
---

# PennyLane

## Overview

PennyLane is a quantum computing library that enables training quantum computers like neural networks. It provides automatic differentiation of quantum circuits, device-independent programming, and seamless integration with classical machine learning frameworks.

## Installation

Install using uv:

```bash
uv pip install pennylane
```

For quantum hardware access, install device plugins:

```bash
# IBM Quantum
uv pip install pennylane-qiskit

# Amazon Braket
uv pip install amazon-braket-pennylane-plugin

# Google Cirq
uv pip install pennylane-cirq

# Rigetti Forest
uv pip install pennylane-rigetti

# IonQ
uv pip install pennylane-ionq
```

## Quick Start

Build a quantum circuit and optimize its parameters:

```python
import pennylane as qml
from pennylane import numpy as np

# Create device
dev = qml.device('default.qubit', wires=2)

# Define quantum circuit
@qml.qnode(dev)
def circuit(params):
    qml.RX(params[0], wires=0)
    qml.RY(params[1], wires=1)
    qml.CNOT(wires=[0, 1])
    return qml.expval(qml.PauliZ(0))

# Optimize parameters
opt = qml.GradientDescentOptimizer(stepsize=0.1)
params = np.array([0.1, 0.2], requires_grad=True)

for i in range(100):
    params = opt.step(circuit, params)
```

## Core Capabilities

### 1. Quantum Circuit Construction

Build circuits with gates, measurements, and state preparation. Key features include:
- Single and multi-qubit gates
- Controlled operations and conditional logic
- Mid-circuit measurements and adaptive circuits
- Various measurement types (expectation, probability, samples)
- Circuit inspection and debugging

### 2. Quantum Machine Learning

Create hybrid quantum-classical models with capabilities such as:
- Integration with PyTorch, JAX, TensorFlow
- Quantum neural networks and variational classifiers
- Data encoding strategies (angle, amplitude, basis, IQP)
- Training hybrid models with backpropagation