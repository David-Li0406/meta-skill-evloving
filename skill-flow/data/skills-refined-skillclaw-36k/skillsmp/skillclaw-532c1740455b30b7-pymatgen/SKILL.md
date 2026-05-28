---
name: pymatgen
description: Use this skill when you need to analyze and manipulate crystal structures, compute phase diagrams, or access materials data for computational materials science.
---

# Pymatgen - Python Materials Genomics

## Overview

Pymatgen is a comprehensive Python library for materials analysis that powers the Materials Project. It allows users to create, analyze, and manipulate crystal structures and molecules, compute phase diagrams and thermodynamic properties, analyze electronic structure (band structures, density of states), generate surfaces and interfaces, and access the Materials Project's database of computed materials. The library supports over 100 file formats from various computational codes.

## When to Use This Skill

This skill should be used when:
- Working with crystal structures or molecular systems in materials science.
- Converting between structure file formats (CIF, POSCAR, XYZ, etc.).
- Analyzing symmetry, space groups, or coordination environments.
- Computing phase diagrams or assessing thermodynamic stability.
- Analyzing electronic structure data (band gaps, density of states, band structures).
- Generating surfaces, slabs, or studying interfaces.
- Accessing the Materials Project database programmatically.
- Setting up high-throughput computational workflows.
- Analyzing diffusion, magnetism, or mechanical properties.
- Working with VASP, Gaussian, Quantum ESPRESSO, or other computational codes.

## Quick Start Guide

### Installation

```bash
# Core pymatgen
pip install pymatgen

# With Materials Project API access
pip install pymatgen mp-api

# Optional dependencies for extended functionality
pip install pymatgen[analysis]  # Additional analysis tools
pip install pymatgen[vis]       # Visualization tools
```

### Basic Structure Operations

```python
from pymatgen.core import Structure, Lattice

# Read structure from file (automatic format detection)
struct = Structure.from_file("POSCAR")

# Create structure from scratch
lattice = Lattice.cubic(3.84)
struct = Structure(lattice, ["Si", "Si"], [[0, 0, 0], [0.25, 0.25, 0.25]])

# Write to different format
struct.to(filename="structure.cif")

# Basic properties
print(f"Formula: {struct.composition.reduced_formula}")
print(f"Space group: {struct.get_space_group_info()}")
print(f"Density: {struct.density:.2f} g/cm³")
```

### Materials Project Integration

```bash
# Set up API key
export MP_API_KEY="your_api_key_here"
```

```python
from mp_api.client import MPRester

with MPRester() as mpr:
    # Example of accessing materials data
    data = mpr.get_data("mp-12345")  # Replace with a valid material ID
```