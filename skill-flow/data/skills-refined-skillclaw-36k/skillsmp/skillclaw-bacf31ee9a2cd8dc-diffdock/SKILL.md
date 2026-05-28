---
name: diffdock
description: Use this skill when you need to predict protein-ligand binding poses using diffusion-based molecular docking for structure-based drug design.
---

# DiffDock: Molecular Docking with Diffusion Models

## Overview

DiffDock is a diffusion-based deep learning tool for molecular docking that predicts 3D binding poses of small molecule ligands to protein targets. It represents the state-of-the-art in computational docking, crucial for structure-based drug discovery and chemical biology.

**Core Capabilities:**
- Predict ligand binding poses with high accuracy using deep learning.
- Support protein structures (PDB files) or sequences (via ESMFold).
- Process single complexes or batch virtual screening campaigns.
- Generate confidence scores to assess prediction reliability.
- Handle diverse ligand inputs (SMILES, SDF, MOL2).

**Key Distinction:** DiffDock predicts **binding poses** (3D structure) and **confidence** (prediction certainty), NOT binding affinity (ΔG, Kd). Always combine with scoring functions (GNINA, MM/GBSA) for affinity assessment.

## When to Use This Skill

This skill should be used when:
- You need to "dock this ligand to a protein" or "predict binding pose."
- You want to "run molecular docking" or "perform protein-ligand docking."
- You are conducting "virtual screening" or "screening a compound library."
- You need to determine "where this molecule binds" or "predict binding site."
- You are involved in structure-based drug design or lead optimization tasks.
- You are working with PDB files + SMILES strings or ligand structures.
- You need to perform batch docking of multiple protein-ligand pairs.

## Installation and Environment Setup

### Check Environment Status

Before proceeding with DiffDock tasks, verify the environment setup:

```bash
# Use the provided setup checker
python scripts/setup_check.py
```

This script validates Python version, PyTorch with CUDA, PyTorch Geometric, RDKit, ESM, and other dependencies.

### Installation Options

**Option 1: Conda (Recommended)**
```bash
git clone https://github.com/gcorso/DiffDock.git
cd DiffDock
conda env create --file environment.yml
conda activate diffdock
```

**Option 2: Docker**
```bash
docker pull rbgcsail/diffdock
docker run -it --gpus all --entrypoint /bin/bash rbgcsail/diffdock
micromamba activate diffdock
```

**Important Notes:**
- GPU is strongly recommended (10-100x speedup vs CPU).
- The first run pre-computes SO(2)/SO(3) lookup tables (~2-5 minutes).
- Model checkpoints (~500MB) download automatically if not present.