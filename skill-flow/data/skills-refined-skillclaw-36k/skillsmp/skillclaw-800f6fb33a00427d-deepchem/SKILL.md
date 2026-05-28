---
name: deepchem
description: Use this skill when you need to apply machine learning techniques to molecular data for tasks such as property prediction, drug discovery, and materials design.
---

# Skill body

## Overview

DeepChem is a comprehensive Python library designed for applying machine learning to chemistry, materials science, and biology. It enables molecular property prediction, drug discovery, materials design, and biomolecule analysis through specialized neural networks, molecular featurization methods, and pretrained models.

## When to Use This Skill

This skill should be used when:
- Loading and processing molecular data (SMILES strings, SDF files, protein sequences)
- Predicting molecular properties (solubility, toxicity, binding affinity, ADMET properties)
- Training models on chemical/biological datasets
- Using MoleculeNet benchmark datasets (Tox21, BBBP, Delaney, etc.)
- Converting molecules to ML-ready features (fingerprints, graph representations, descriptors)
- Implementing graph neural networks for molecules (GCN, GAT, MPNN, AttentiveFP)
- Applying transfer learning with pretrained models (ChemBERTa, GROVER, MolFormer)
- Predicting crystal/materials properties (bandgap, formation energy)
- Analyzing protein or DNA sequences

## Core Capabilities

### 1. Molecular Data Loading and Processing

DeepChem provides specialized loaders for various chemical data formats:

```python
import deepchem as dc

# Load CSV with SMILES
featurizer = dc.feat.CircularFingerprint(radius=2, size=2048)
loader = dc.data.CSVLoader(
    tasks=['solubility', 'toxicity'],
    feature_field='smiles',
    featurizer=featurizer
)
dataset = loader.create_dataset('molecules.csv')

# Load SDF files
loader = dc.data.SDFLoader(tasks=['activity'], featurizer=featurizer)
dataset = loader.create_dataset('compounds.sdf')

# Load protein sequences
loader = dc.data.FASTALoader()
dataset = loader.create_dataset('proteins.fasta')
```

**Key Loaders**:
- `CSVLoader`: For tabular data with molecular identifiers
- `SDFLoader`: For molecular structure files
- `FASTALoader`: For protein/DNA sequences
- `ImageLoader`: For molecular images
- `JsonLoader`: For JSON-formatted datasets

### 2. Molecular Featurization

DeepChem allows conversion of molecules into various feature representations suitable for machine learning tasks. This includes generating fingerprints, graph representations, and other descriptors necessary for model training and evaluation.