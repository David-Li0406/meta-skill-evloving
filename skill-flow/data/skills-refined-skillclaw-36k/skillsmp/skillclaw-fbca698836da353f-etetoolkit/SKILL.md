---
name: etetoolkit
description: Use this skill when you need to manipulate and analyze phylogenetic trees, detect evolutionary events, and visualize results for phylogenomics.
---

# Skill body

## Overview

ETE (Environment for Tree Exploration) is a toolkit for phylogenetic and hierarchical tree analysis. It allows users to manipulate trees, analyze evolutionary events, visualize results, and integrate with biological databases for phylogenomic research and clustering analysis.

## Core Capabilities

### 1. Tree Manipulation and Analysis

Load, manipulate, and analyze hierarchical tree structures with support for:

- **Tree I/O**: Read and write Newick, NHX, PhyloXML, and NeXML formats.
- **Tree traversal**: Navigate trees using preorder, postorder, or levelorder strategies.
- **Topology modification**: Prune, root, collapse nodes, and resolve polytomies.
- **Distance calculations**: Compute branch lengths and topological distances between nodes.
- **Tree comparison**: Calculate Robinson-Foulds distances and identify topological differences.

**Common patterns:**

```python
from ete3 import Tree

# Load tree from file
tree = Tree("tree.nw", format=1)

# Basic statistics
print(f"Leaves: {len(tree)}")
print(f"Total nodes: {len(list(tree.traverse()))}")

# Prune to taxa of interest
taxa_to_keep = ["species1", "species2", "species3"]
tree.prune(taxa_to_keep, preserve_branch_length=True)

# Midpoint root
midpoint = tree.get_midpoint_outgroup()
tree.set_outgroup(midpoint)

# Save modified tree
tree.write(outfile="rooted_tree.nw")
```

Use `scripts/tree_operations.py` for command-line tree manipulation:

```bash
# Display tree statistics
python scripts/tree_operations.py stats tree.nw

# Convert format
python scripts/tree_operations.py convert tree.nw output.nw --in-format 0 --out-format 1

# Reroot tree
python scripts/tree_operations.py reroot tree.nw rooted.nw --midpoint

# Prune to specific taxa
python scripts/tree_operations.py prune tree.nw pruned.nw --keep-taxa "sp1,sp2,sp3"

# Show ASCII visualization
python scripts/tree_operations.py ascii tree.nw
```

### 2. Phylogenetic Analysis

Analyze gene trees with evolutionary event detection:

- **Sequence alignment integration**: Link trees to multiple sequence alignments (FASTA, Phylip).
- **Species naming**: Automatic or custom species extraction from gene names.
- **Evolutionary events**: Detect duplication and speciation events using species overlap or tree reconciliation.
- **Orthology detection**: Identify orthologous and paralogous relationships among genes.

### 3. Visualization

Generate visual representations of trees in various formats:

- **PDF/SVG**: Export trees for publication-quality graphics.
- **ASCII**: Display trees in a simple text format for quick inspection.

## License

This skill is licensed under the GPL-3.0 license.