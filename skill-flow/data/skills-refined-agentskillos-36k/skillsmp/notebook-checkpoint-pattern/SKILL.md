---
name: notebook-checkpoint-pattern
description: "Pattern for connecting Jupyter notebooks in a pipeline via checkpoint files. Trigger: connecting notebooks, saving outputs, multi-notebook pipelines"
author: Claude Code
date: 2026-01-06
---

# Notebook Checkpoint Pattern

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2026-01-06 |
| **Goal** | Connect multiple Jupyter notebooks in a pipeline via saved checkpoint files |
| **Environment** | Python, Jupyter, scanpy/anndata for single-cell data |
| **Status** | Success |

## Context
Scientific analysis pipelines often span multiple notebooks:
- `1_preprocessing.ipynb` - Data loading and QC filtering
- `2_integration.ipynb` - Cross-modal integration
- `3_visualization.ipynb` - Results visualization

Without checkpoints:
- Must run all notebooks in sequence in one session
- Memory issues with large datasets
- Can't restart from intermediate steps
- Difficult to share intermediate results

## Verified Workflow

### Directory Structure

```
project/
├── notebooks/
│   ├── 1_preprocessing.ipynb
│   ├── 2_integration.ipynb
│   └── 3_visualization.ipynb
├── results/
│   ├── 1_preprocessing/
│   │   ├── protein_adata.h5ad
│   │   ├── rna_adata.h5ad
│   │   └── preprocessing_params.json
│   ├── 2_integration/
│   │   ├── matching.pkl
│   │   ├── matching.csv
│   │   ├── arrays.npy
│   │   └── integration_params.json
│   └── 3_visualization/
│       └── figures/
└── data/
    └── (raw input files)
```

### Save Cell Pattern (End of Notebook)

```python
# Save outputs to results directory
import os
import json
from datetime import datetime

results_dir = 'results/1_preprocessing'
os.makedirs(results_dir, exist_ok=True)

# Save AnnData objects
protein_adata.write_h5ad(f'{results_dir}/protein_adata.h5ad')
rna_adata.write_h5ad(f'{results_dir}/rna_adata.h5ad')

# Save parameters as JSON (human-readable, version-controllable)
params = {
    'timestamp': datetime.now().isoformat(),
    'filtering_params': {
        'min_counts': MIN_COUNTS,
        'max_counts': MAX_COUNTS,
    },
    'data_shapes': {
        'n_cells': adata.n_obs,
        'n_features': adata.n_vars
    }
}
with open(f'{results_dir}/params.json', 'w') as f:
    json.dump(params, f, indent=2)

print(f"Saved to {results_dir}/")
print(f"Run next_notebook.ipynb next.")
```

### Load Cell Pattern (Start of Notebook)

```python
# Load results from previous notebook
import os
import json
import pickle

results_dir = 'results/1_preprocessing'

if not os.path.exists(results_dir):
    raise FileNotFoundError(
        f"Results directory '{results_dir}' not found. "
        f"Run 1_preprocessing.ipynb first."
    )

# Load AnnData objects
protein_adata = sc.read_h5ad(f'{results_dir}/protein_adata.h5ad')
rna_adata = sc.read_h5ad(f'{results_dir}/rna_adata.h5ad')

# Load parameters
with open(f'{results_dir}/params.json', 'r') as f:
    prev_params = json.load(f)

print(f"Loaded from {results_dir}/")
print(f"Previous run: {prev_params['timestamp']}")
```

### Format Recommendations

| Data Type | Format | Why |
|-----------|--------|-----|
| AnnData objects | `.h5ad` | Native scanpy, preserves obs/var/uns |
| NumPy arrays | `.npy` | Fast, compact, preserves dtype |
| Sparse matrices | `.npz` | Efficient for sparse data |
| DataFrames | `.parquet` | Fast, compressed, schema preserved |
| Small DataFrames | `.csv` | Human-readable for inspection |
| Python objects | `.pkl` | Arbitrary objects (dicts, lists) |
| Parameters | `.json` | Human-readable, git-friendly |

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Save to `data/` directory | Mixed raw and processed data | Use separate `results/` directory |
| Single flat `results/` folder | Files from different notebooks overlap | Use subdirectories per notebook |
| Only save final outputs | Can't restart from intermediate steps | Save after each major notebook |
| Save everything to pickle | Can't inspect without loading | Use JSON for params, h5ad for AnnData |
| Hardcode absolute paths | Breaks on different machines | Use relative paths from notebook |
| No timestamps | Can't tell which run produced outputs | Include timestamp in params JSON |

## Key Insights

- **Clear directory structure**: `results/{notebook_name}/` keeps outputs organized
- **Fail fast on missing inputs**: Check directory exists before loading
- **Human-readable params**: JSON for parameters enables inspection and version control
- **Include timestamps**: Know when outputs were generated
- **Print next steps**: Tell user which notebook to run next
- **Separate raw from processed**: Never overwrite raw data in `data/`

## Git Integration

Add to `.gitignore`:
```gitignore
# Large result files
results/**/*.h5ad
results/**/*.npy
results/**/*.pkl
results/**/*.parquet

# Keep param files for reproducibility
!results/**/*.json
!results/**/*.csv
```

## References
- AnnData file format: https://anndata.readthedocs.io/en/latest/fileformat-prose.html
- Scanpy I/O: https://scanpy.readthedocs.io/en/stable/api.html#reading
- Project-data separation skill: `.skills_registry/plugins/scientific/project-data-separation/`
