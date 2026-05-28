---
name: fluidsim
description: Use this skill when running fluid dynamics simulations, including Navier-Stokes equations (2D/3D), shallow water equations, and analyzing turbulence or vortex dynamics. It provides a comprehensive framework for computational fluid dynamics simulations using Python.
---

# FluidSim

## Overview

FluidSim is an object-oriented Python framework for high-performance computational fluid dynamics (CFD) simulations. It provides solvers for periodic-domain equations using pseudospectral methods with FFT, delivering performance comparable to Fortran/C++ while maintaining Python's ease of use.

**Key strengths**:
- Multiple solvers: 2D/3D Navier-Stokes, shallow water, stratified flows
- High performance: Pythran/Transonic compilation, MPI parallelization
- Complete workflow: Parameter configuration, simulation execution, output analysis
- Interactive analysis: Python-based post-processing and visualization

## Core Capabilities

### 1. Installation and Setup

Install FluidSim using pip with appropriate feature flags:

```bash
# Basic installation
pip install fluidsim

# With FFT support (required for most solvers)
pip install "fluidsim[fft]"

# With MPI for parallel computing
pip install "fluidsim[fft,mpi]"
```

Set environment variables for output directories (optional):

```bash
export FLUIDSIM_PATH=/path/to/simulation/outputs
export FLUIDDYN_PATH_SCRATCH=/path/to/working/directory
```

No API keys or authentication required.

### 2. Running Simulations

The standard workflow consists of five steps:

**Step 1**: Import solver
```python
from fluidsim.solvers.ns2d.solver import Simul
```

**Step 2**: Create and configure parameters
```python
params = Simul.create_default_params()
params.oper.nx = params.oper.ny = 256
params.oper.Lx = params.oper.Ly = 2 * 3.14159
params.nu_2 = 1e-3
params.time_stepping.t_end = 10.0
params.init_fields.type = "noise"
```

**Step 3**: Instantiate simulation
```python
sim = Simul(params)
```

**Step 4**: Execute
```python
sim.time_stepping.start()
```

**Step 5**: Analyze results
```python
sim.output.phys_fields.plot("vorticity")
sim.output.spatial_means.plot()
```