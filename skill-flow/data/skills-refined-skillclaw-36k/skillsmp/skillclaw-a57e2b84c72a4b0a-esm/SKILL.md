---
name: esm
description: Use this skill when working with protein sequences, structures, or function prediction; designing novel proteins; generating protein embeddings; performing inverse folding; or conducting protein engineering tasks.
---

# ESM: Evolutionary Scale Modeling

## Overview

ESM provides state-of-the-art protein language models for understanding, generating, and designing proteins. This skill enables working with two model families: ESM3 for generative protein design across sequence, structure, and function, and ESM C for efficient protein representation learning and embeddings.

## Core Capabilities

### 1. Protein Sequence Generation with ESM3

Generate novel protein sequences with desired properties using multimodal generative modeling.

**When to use:**
- Designing proteins with specific functional properties
- Completing partial protein sequences
- Generating variants of existing proteins
- Creating proteins with desired structural characteristics

**Basic usage:**

```python
from esm.models.esm3 import ESM3
from esm.sdk.api import ESM3InferenceClient, ESMProtein, GenerationConfig

# Load model locally
model: ESM3InferenceClient = ESM3.from_pretrained("esm3-sm-open-v1").to("cuda")

# Create protein prompt
protein = ESMProtein(sequence="MPRT___KEND")  # '_' represents masked positions

# Generate completion
protein = model.generate(protein, GenerationConfig(track="sequence", num_steps=8))
print(protein.sequence)
```

**For remote/cloud usage via Forge API:**

```python
from esm.sdk.forge import ESM3ForgeInferenceClient
from esm.sdk.api import ESMProtein, GenerationConfig

# Connect to Forge
model = ESM3ForgeInferenceClient(model="esm3-medium-2024-08", url="https://forge.evolutionaryscale.ai", token="<token>")

# Generate
protein = model.generate(protein, GenerationConfig(track="sequence", num_steps=8))
```

### 2. Structure Prediction and Inverse Folding

Use ESM3's structure track for structure prediction from sequence or inverse folding (sequence design from structure).

**Structure prediction:**

```python
# Example code for structure prediction will go here
```

**Inverse folding:**

```python
# Example code for inverse folding will go here
```

See `references/esm3-api.md` for detailed ESM3 model specifications, advanced generation configurations, and multimodal prompting examples.