---
name: data_fabric
description: Transforms and maps data between different stages of the pipeline (Miner -> Appraiser).
---

# Data Fabric Skill

This skill acts as the glue between the Miner and the Appraiser, transforming raw supplier data into a format ready for valuation.

## Capabilities

- Convert `CDR_MASTER_DB.csv` to `productos_listos_para_web.csv`.
- Apply initial markup/margin rules.

## Usage

```python
from src.skills.data_fabric.fabric import process_miner_output

process_miner_output("CDR_MASTER_DB.csv", "productos_listos_para_web.csv")
```
