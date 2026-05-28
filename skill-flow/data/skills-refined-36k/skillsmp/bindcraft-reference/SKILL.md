---
name: bindcraft-reference
description: BindCraft protein binder design reference. Use when working with AF2 backpropagation, binder design, interface optimization, PyRosetta metrics, design filtering, or comparing with RFdiffusion approaches.
---

# BindCraft Reference Skill

> **Full documentation**: `docs/plans/2026-01-15-bindcraft-comprehensive-skill.md`

## Quick Reference

### Pipeline Overview
```
Target PDB → AF2 Hallucination → MPNN Sequences → AF2 Validation → PyRosetta Relax → Filtering
```

### Key Difference from RFdiffusion
- **BindCraft**: AF2 backpropagation (sequence+structure simultaneously)
- **RFdiffusion**: Diffusion model (backbone first, then MPNN)

### Design Algorithms
| Algorithm | Method | Speed |
|-----------|--------|-------|
| **4stage** | Logits→Softmax→One-hot→PSSM (default) | Medium |
| **3stage** | Logits→Softmax→One-hot | Faster |
| **2stage** | Logits→PSSM semi-greedy | Fastest |
| **greedy** | Random loss-reducing mutations | Slowest |

### Target Settings (JSON)
```json
{
    "design_path": "/path/to/output/",
    "binder_name": "MyBinder",
    "starting_pdb": "/path/to/target.pdb",
    "chains": "A",
    "target_hotspot_residues": "56,58,62",
    "lengths": [65, 150],
    "number_of_final_designs": 100
}
```

### Key Loss Weights
| Weight | Effect |
|--------|--------|
| `weights_con_inter` | Interface contacts (higher = more) |
| `weights_plddt` | Confidence optimization |
| `weights_helicity` | Negative = favor β-sheets |
| `weights_rg` | Compactness (radius of gyration) |
| `weights_iptm` | Interface pTM |

### Key Filters
| Filter | Good Value | Meaning |
|--------|------------|---------|
| `pLDDT` | ≥0.8 | Confidence |
| `i_pTM` | ≥0.5 | Interface confidence |
| `dG` | ≤0 | Binding energy (negative = good) |
| `ShapeComplementarity` | ≥0.6 | Surface fit |
| `n_InterfaceHbonds` | ≥3 | Hydrogen bonds |

### PyRosetta Interface Metrics
- `dG`: Binding free energy
- `dSASA`: Buried surface area
- `ShapeComplementarity`: Geometric fit
- `PackStat`: Packing quality
- `InterfaceHbonds`: H-bond count
- `InterfaceUnsatHbonds`: Buried polar without H-bonds

### Presets
| Preset | Use Case |
|--------|----------|
| `default_4stage_multimer` | Standard binders |
| `betasheet_4stage_multimer` | β-sheet rich |
| `peptide_3stage_multimer` | Short peptides |
| `*_hardtarget` | Difficult targets |
| `*_flexible` | Flexible interfaces |

### Concepts for Banta Lab
1. **Multi-stage optimization**: Soft → temp → hard → greedy
2. **Combined loss functions**: Multiple objectives
3. **Integrated AF2 validation**: After MPNN design
4. **PyRosetta interface scoring**: Add to validation pipeline
5. **Filter-based selection**: Multi-metric thresholds
6. **Acceptance rate monitoring**: Auto-terminate poor campaigns

### When to Use BindCraft vs RFdiffusion
| Use BindCraft | Use RFdiffusion |
|---------------|-----------------|
| Need high AF2 confidence | Need structural diversity |
| Integrated validation | Large-scale screening |
| Well-defined binding site | Novel fold exploration |
| Quality over quantity | Memory constrained |
