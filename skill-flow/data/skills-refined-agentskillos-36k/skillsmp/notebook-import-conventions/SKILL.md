---
name: notebook-import-conventions
description: "Correct import patterns and file paths for maxfuse Jupyter notebooks"
author: smith6jt
date: 2024-12-28
---

# Notebook Import Conventions - Research Notes

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2024-12-28 |
| **Goal** | Fix all notebook imports and file paths to use the maxfuse package correctly |
| **Environment** | Python 3.12, maxfuse package installed from src/maxfuse/ |
| **Status** | Success |

## Context
After reorganizing the maxfuse package, notebooks still had outdated imports referencing the old `mario-py/` directory structure. Additionally, file paths were inconsistent - some using relative paths from the notebooks directory, others assuming files were in the current working directory.

## Verified Import Patterns

### Correct Imports for MaxFuse Package
```python
# Main classes (most common usage)
from maxfuse import Fusor, Mario

# Submodule access
from maxfuse.core import model as mf_model
from maxfuse.core import spatial_utils
from maxfuse.mario.match import pipelined_mario

# Namespace import
import maxfuse as mf
```

### Package Structure Reference
```
src/maxfuse/
├── __init__.py          # Exports: Fusor, Mario, core, mario
├── core/
│   ├── model.py         # Fusor class
│   ├── spatial_utils.py # Spatial utilities
│   ├── match_utils.py   # Matching algorithms
│   ├── graph.py         # Graph construction
│   └── utils.py         # Numerical utilities
└── mario/
    ├── match.py         # Mario class, pipelined_mario function
    ├── match_utils.py   # MARIO matching utilities
    ├── cluster.py       # Clustering algorithms
    └── embed.py         # Embedding utilities
```

## Verified File Path Conventions

### Repository Structure
```
repo/
├── data/                 # Data files (gitignored)
│   ├── 1904CC2B_cells.tsv
│   ├── protein_gene_conversion.csv
│   └── raw_feature_bc_matrix/
├── results/              # Output files (gitignored)
├── notebooks/            # Jupyter notebooks
└── src/maxfuse/          # Package source
```

### Correct Paths (from repo root working directory)
VS Code/Jupyter typically sets the working directory to the repo root, not the notebooks folder.

| File Type | Correct Path |
|-----------|--------------|
| CODEX TSV | `data/1904CC2B_cells.tsv` |
| RNA matrix | `data/raw_feature_bc_matrix/matrix.mtx.gz` |
| Correspondence table | `data/protein_gene_conversion.csv` |
| Results output | `results/` |

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| `sys.path.insert(0, '../mario-py/src')` | Directory no longer exists after reorganization | MARIO is now part of maxfuse package |
| `from mario.match import Mario` | Module not found - mario is not a top-level package | Use `from maxfuse import Mario` |
| `from maxfuse import model` | model is in core subpackage | Use `from maxfuse.core import model` |
| `from maxfuse import spatial_utils` | spatial_utils is in core subpackage | Use `from maxfuse.core import spatial_utils` |
| `pd.read_csv('../1904CC2B_cells.tsv')` | File is in data/ subdirectory | Use `data/1904CC2B_cells.tsv` |
| `pd.read_csv('protein_gene_conversion.csv')` | File is in data/ not notebooks/ | Use `data/protein_gene_conversion.csv` |
| `'../docs/protein_gene_conversion.csv'` | File is in data/ not docs/ | Use `data/protein_gene_conversion.csv` |
| `'../data/...'` paths | Working directory is repo root, not notebooks/ | Use `data/...` without `../` prefix |

## Quick Reference: Before/After

### Import Fixes
```python
# WRONG (old mario-py approach)
sys.path.insert(0, '../mario-py/src')
from mario.match import Mario, pipelined_mario

# CORRECT (maxfuse package)
from maxfuse import Mario
from maxfuse.mario.match import pipelined_mario
```

```python
# WRONG (direct submodule import)
from maxfuse import model
from maxfuse import spatial_utils

# CORRECT (through core subpackage)
from maxfuse.core import model
from maxfuse.core import spatial_utils
```

### Path Fixes
```python
# WRONG (assumes notebooks/ working directory or wrong location)
codex_df = pd.read_csv('../1904CC2B_cells.tsv', sep='\t')
codex_df = pd.read_csv('../data/1904CC2B_cells.tsv', sep='\t')
rna_mtx = mmread("raw_feature_bc_matrix/matrix.mtx.gz")

# CORRECT (working directory is repo root)
codex_df = pd.read_csv('data/1904CC2B_cells.tsv', sep='\t')
rna_mtx = mmread("data/raw_feature_bc_matrix/matrix.mtx.gz")
```

## Key Insights
- The `__init__.py` in maxfuse exports `Fusor` and `Mario` at the top level for convenience
- Submodules like `spatial_utils` must be accessed through `maxfuse.core`
- All data files should go in the `data/` directory at repo root
- **VS Code/Jupyter sets working directory to repo root**, not the notebooks folder
- Use `data/filename.tsv` paths (no `../` prefix) since working directory is repo root
- The `mario-py/` directory was removed; all MARIO functionality is now in `maxfuse.mario`

## Notebooks Fixed
1. `1_preprocessing.ipynb` - imports and CODEX/RNA paths
2. `2_integration.ipynb` - correspondence table path
3. `3_visualization.ipynb` - no changes needed
4. `4_multi_sample.ipynb` - imports and sample config paths
5. `5_analysis.ipynb` - spatial_utils import
6. `codex_rnaseq_integration.ipynb` - imports and all data paths

## References
- Package structure: See `src/maxfuse/__init__.py` for exports
- CLAUDE.md: Repository structure documentation
