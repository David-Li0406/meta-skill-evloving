---
name: qutip
description: Use this skill when simulating and analyzing open quantum systems, particularly for studying master equations, Lindblad dynamics, decoherence, and quantum optics.
---

# QuTiP: Quantum Toolbox in Python

## Overview

QuTiP provides comprehensive tools for simulating and analyzing quantum mechanical systems. It handles both closed (unitary) and open (dissipative) quantum systems with multiple solvers optimized for different scenarios.

## Installation

```bash
uv pip install qutip
```

Optional packages for additional functionality:

```bash
# Quantum information processing (circuits, gates)
uv pip install qutip-qip

# Quantum trajectory viewer
uv pip install qutip-qtrl
```

## Quick Start

```python
from qutip import *
import numpy as np
import matplotlib.pyplot as plt

# Create quantum state
psi = basis(2, 0)  # |0⟩ state

# Create operator
H = sigmaz()  # Hamiltonian

# Time evolution
tlist = np.linspace(0, 10, 100)
result = sesolve(H, psi, tlist, e_ops=[sigmaz()])

# Plot results
plt.plot(tlist, result.expect[0])
plt.xlabel('Time')
plt.ylabel('⟨σz⟩')
plt.show()
```

## Core Capabilities

### 1. Quantum Objects and States

Create and manipulate quantum states and operators:

```python
# States
psi = basis(N, n)  # Fock state |n⟩
psi = coherent(N, alpha)  # Coherent state |α⟩
rho = thermal_dm(N, n_avg)  # Thermal density matrix

# Operators
a = destroy(N)  # Annihilation operator
H = num(N)  # Number operator
sx, sy, sz = sigmax(), sigmay(), sigmaz()  # Pauli matrices

# Composite systems
psi_AB = tensor(psi_A, psi_B)  # Tensor product
```

### 2. Time Evolution and Dynamics

Multiple solvers for different scenarios:

```python
# Closed systems (unitary evolution)
result = sesolve(H, psi0, tlist, e_ops=[num(N)])

# Open systems (dissipation)
c_ops = [np.sqrt(0.1) * destroy(N)]  # Collapse operators
result = mesolve(H, psi0, tlist, c_ops, e_ops=[num(N)])

# Quantum trajectories (Monte Carlo)
result = mcsolve(H, psi0, tlist, c_ops, ntraj=500, e_ops=[num(N)])
```

**Solver selection guide:**
- `sesolve`: Pure states, unitary evolution
- `mesolve`: Open systems with dissipation
- `mcsolve`: Quantum trajectories (Monte Carlo)