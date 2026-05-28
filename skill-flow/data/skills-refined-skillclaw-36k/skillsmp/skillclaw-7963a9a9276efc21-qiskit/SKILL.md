---
name: qiskit
description: Use this skill when targeting IBM Quantum hardware, working with Qiskit Runtime for production workloads, or needing IBM optimization tools.
---

# Qiskit

## Overview

Qiskit is the world's most popular open-source quantum computing framework with over 13 million downloads. It allows users to build quantum circuits, optimize for hardware, execute on simulators or real quantum computers, and analyze results. Qiskit supports IBM Quantum (100+ qubit systems), IonQ, Amazon Braket, and other providers.

**Key Features:**
- 83x faster transpilation than competitors
- 29% fewer two-qubit gates in optimized circuits
- Backend-agnostic execution (local simulators or cloud hardware)
- Comprehensive algorithm libraries for optimization, chemistry, and machine learning

## Quick Start

### Installation

To install Qiskit, run the following commands:

```bash
pip install qiskit
pip install "qiskit[visualization]" matplotlib
```

### First Circuit

Here’s how to create and run a simple quantum circuit that generates a Bell state:

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

# Create Bell state (entangled qubits)
qc = QuantumCircuit(2)
qc.h(0)           # Hadamard on qubit 0
qc.cx(0, 1)       # CNOT from qubit 0 to 1
qc.measure_all()  # Measure both qubits

# Run locally
sampler = StatevectorSampler()
result = sampler.run([qc], shots=1024).result()
counts = result[0].data.meas.get_counts()
print(counts)  # {'00': ~512, '11': ~512}
```

### Visualization

To visualize the circuit and results, use the following code:

```python
from qiskit.visualization import plot_histogram

qc.draw('mpl')           # Circuit diagram
plot_histogram(counts)   # Results histogram
```

## Core Capabilities

### 1. Setup and Installation
For detailed installation, authentication, and IBM Quantum account setup, refer to the setup documentation.

### 2. Building Quantum Circuits
Learn how to construct quantum circuits with gates, measurements, and composition. Topics include:
- Creating circuits with `QuantumCircuit`
- Single-qubit gates (H, X, Y, Z, rotations, phase gates)
- Multi-qubit gates (CNOT, SWAP, Toffoli)
- Measurements and barriers
- Circuit composition and properties