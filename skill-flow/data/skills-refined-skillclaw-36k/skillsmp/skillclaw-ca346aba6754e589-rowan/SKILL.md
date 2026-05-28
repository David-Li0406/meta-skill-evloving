---
name: rowan
description: Use this skill when you need to perform quantum chemistry calculations, including molecular property predictions, geometry optimizations, and protein-ligand docking, without local computational resources.
---

# Rowan: Cloud-Based Quantum Chemistry Platform

## Overview

Rowan is a cloud-based computational chemistry platform that provides programmatic access to quantum chemistry workflows through a Python API. It enables automation of complex molecular simulations without requiring local computational resources or expertise in multiple quantum chemistry packages.

**Key Capabilities:**
- Molecular property prediction (pKa, redox potential, solubility, ADMET-Tox)
- Geometry optimization and conformer searching
- Protein-ligand docking with AutoDock Vina
- AI-powered protein cofolding with Chai-1 and Boltz models
- Access to DFT, semiempirical, and neural network potential methods
- Cloud compute with automatic resource allocation

**Why Rowan:**
- No local compute cluster required
- Unified API for dozens of computational methods
- Results viewable in web interface at labs.rowansci.com
- Automatic resource scaling

## Installation and Authentication

### Installation

```bash
pip install rowan-python
```

### Authentication

Generate an API key at [labs.rowansci.com/account/api-keys](https://labs.rowansci.com/account/api-keys).

**Option 1: Direct assignment**
```python
import rowan
rowan.api_key = "your_api_key_here"
```

**Option 2: Environment variable (recommended)**
```bash
export ROWAN_API_KEY="your_api_key_here"
```

The API key is automatically read from `ROWAN_API_KEY` on module import.

### Verify Setup

```python
import rowan

# Check authentication
user = rowan.whoami()
print(f"Logged in as: {user.username}")
print(f"Credits available: {user.credits}")
```

## Core Workflows

### 1. pKa Prediction

Calculate the acid dissociation constant for molecules:

```python
import rowan
import stjames

# Create molecule from SMILES
mol = rowan.Molecule.from_smiles("CC(=O)O")
pKa = rowan.calculate_pKa(mol)
print(f"The pKa of the molecule is: {pKa}")
```

### 2. Geometry Optimization

Optimize the geometry of a molecule:

```python
optimized_mol = rowan.optimize_geometry(mol)
print(f"Optimized geometry: {optimized_mol}")
```

### 3. Protein-Ligand Docking

Perform docking of a ligand to a protein:

```python
docking_results = rowan.dock(protein, ligand)
print(f"Docking results: {docking_results}")
```