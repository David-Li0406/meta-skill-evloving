---
name: rfd3-reference
description: RFdiffusion3 protein design reference. Use when working with RFD3, contigs, symmetry, hotspots, fixed atoms, RASA conditioning, H-bond conditioning, or Foundry API. Covers all input parameters, design types, and best practices.
---

# RFdiffusion3 Reference Skill

> **Full documentation**: `docs/plans/2026-01-15-rfd3-comprehensive-skill.md`

## Quick Reference

### Contig Syntax
```
"60-80"              → Single chain, 60-80 residues
"60-80,/0,60-80"     → Two chains
"A10-50,/0,40-60"    → Keep A10-50, add new chain
"5-12,A10,3-8,A15"   → Scaffold around fixed residues
```

### Key Parameters
| Parameter | Purpose |
|-----------|---------|
| `select_fixed_atoms` | Fix backbone/sidechain atoms during diffusion |
| `select_hotspots` | Preserve key interface residues |
| `select_buried` | Force burial (low RASA) |
| `select_exposed` | Force exposure (high RASA) |
| `select_hbond_donor` | H-bond conditioning (donors) |
| `select_hbond_acceptor` | H-bond conditioning (acceptors) |
| `symmetry` | Point group symmetry (c2, c3, d2, etc.) |

### Symmetry Types
- **Cyclic**: c2, c3, c4, ... (n copies around axis)
- **Dihedral**: d2, d3, d4, ... (2n copies)
- **Platonic**: t, o, i (use `low_memory_mode=True`)

### CRITICAL: Guiding Potentials NOT SUPPORTED
`substrate_contacts`, `olig_contacts`, `monomer_ROG` are RFdiffusion v1/v2 CLI features - **NOT available in Foundry API**.

### Design Types
1. **Small molecule binder**: Fix ligand atoms + hotspots
2. **Protein binder**: Target chain + hotspot residues
3. **Enzyme design**: Scaffold around fixed catalytic residues
4. **Symmetric oligomer**: Single monomer + symmetry flag
5. **Metal binding**: Fix coordinating atoms + metal

### Example: Protein Binder
```python
{
    "contig": "B1-200,/0,60-100",
    "select_hotspots": {"B": "45,48,52,89,93"},
    "num_designs": 100
}
```

### Best Practices
- Always `diffusion_batch_size=1` for symmetry
- Pre-symmetrize motifs to canonical axes
- H-bond success rate ~37% (expected)
- Generate many designs for diversity
