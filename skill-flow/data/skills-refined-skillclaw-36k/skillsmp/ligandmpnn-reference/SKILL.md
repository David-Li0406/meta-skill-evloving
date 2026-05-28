---
name: ligandmpnn-reference
description: LigandMPNN sequence design reference. Use when working with LigandMPNN, ProteinMPNN, sequence design, amino acid biasing, fixed residues, temperature, side chain packing, or membrane protein design.
---

# LigandMPNN Reference Skill

> **Full documentation**: `docs/plans/2026-01-15-ligandmpnn-comprehensive-skill.md`

## Quick Reference

### Model Types
| Model | Use Case |
|-------|----------|
| `protein_mpnn` | General protein design |
| `ligand_mpnn` | Ligand-aware design (metals, small molecules) |
| `soluble_mpnn` | Soluble proteins only |
| `global_label_membrane_mpnn` | Membrane (global label) |
| `per_residue_label_membrane_mpnn` | Membrane (per-residue) |

### Key Parameters
```bash
--model_type ligand_mpnn          # Model selection
--temperature 0.1                  # Sampling diversity (0.1 = default)
--fixed_residues "A10 A15 B20"    # Keep these positions unchanged
--bias_AA "H:5.0,D:3.0,E:3.0"     # Favor specific amino acids
--omit_AA "C,M"                    # Never use these amino acids
--ligand_mpnn_use_atom_context 1   # Enable ligand context
--pack_side_chains 1               # Enable side chain packing
```

### Residue Format
```
A12       → Chain A, residue 12
B82A      → Chain B, residue 82, insertion code A
"A10 A15" → Space-separated list
```

### Common Bias Presets
```bash
# Metal binding (Zn, Fe, Cu)
--bias_AA "H:5.0,C:4.0,D:3.0,E:3.0" --omit_AA "P,G"

# Lanthanide binding (Tb, Gd, Eu)
--bias_AA "D:6.0,E:4.0,N:1.0,Q:1.0" --omit_AA "C,H"

# Small molecule (aromatic)
--bias_AA "W:3.0,Y:2.0,F:2.0,H:1.5"

# Nucleotide binding
--bias_AA "R:4.0,K:3.0,N:2.0,Q:2.0,S:1.5,T:1.5"
```

### Temperature Guide
| Temp | Effect |
|------|--------|
| 0.05 | Very deterministic |
| 0.1  | Low diversity (default) |
| 0.2  | Moderate diversity |
| 0.5  | High diversity |

### Output Metrics
- `overall_confidence`: Average confidence (0-1)
- `ligand_confidence`: Near-ligand confidence
- `seq_rec`: Sequence recovery vs original

### Example: Metal Site Design
```bash
python run.py \
    --model_type ligand_mpnn \
    --pdb_path ./protein_with_metal.pdb \
    --fixed_residues "A10 A15 A20 A25" \
    --bias_AA "D:5.0,E:4.0,H:3.0" \
    --ligand_mpnn_use_atom_context 1 \
    --temperature 0.1 \
    --out_folder ./output/
```

### Best Practices
- Always fix catalytic/coordinating residues
- Use `--ligand_mpnn_use_side_chain_context 1` for fixed residue context
- Lower temperature = higher confidence, less diversity
- Check `ligand_confidence` for binding site quality
