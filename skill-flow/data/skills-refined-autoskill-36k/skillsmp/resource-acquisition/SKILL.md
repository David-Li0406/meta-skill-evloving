---
name: resource-acquisition
description: Find and acquire computational science resources autonomously. Use when you need force field parameters, pseudopotentials, crystal structures, or any other scientific data. You are a researcher - you find what you need.
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
  - WebSearch
  - WebFetch
---

# Resource Acquisition: Working Like a Researcher

You are a researcher. You have tools, you have a goal, you figure out the rest.

## The Researcher Mindset

When you need something (parameters, structures, files):
1. **Identify what you need** - Be specific
2. **Search for it** - Use all available tools
3. **Verify what you find** - Is this source authoritative? Are values consistent?
4. **Document the source** - Future you needs to know where this came from
5. **Cross-reference** - Check multiple sources when possible

**Never use a value without knowing where it came from.**

## Your Tools

- **WebSearch** - Find papers, databases, resources
- **WebFetch** - Download files, read web pages
- **Semantic Scholar** - Academic paper search (via MCP)
- **Playwright** - Browser automation for complex downloads (via MCP)
- **Materials Project API** - Crystal structures and properties

---

## 1. Force Field Parameters

### The Problem
Every MD simulation needs force field parameters (LJ epsilon/sigma, bond constants, etc.). These are NOT universal - they depend on:
- The material system
- The property you're calculating
- The conditions (temperature, pressure)

### How to Find Them

**Step 1: Identify what you need**
```
"I need Lennard-Jones parameters for liquid argon at 94.4 K"
"I need TIP4P water model parameters"
"I need EAM potential for copper"
```

**Step 2: Search literature**
```
Search queries that work:
- "[material] lennard-jones parameters molecular dynamics"
- "[material] force field parameters"
- "[model name] original paper" (e.g., "TIP4P original paper")
- "[material] interatomic potential"
```

**Step 3: Find the authoritative source**
For common systems, there are seminal papers:
- Argon LJ: Rahman 1964, or Allen & Tildesley textbook
- Water TIP4P: Jorgensen 1983 (J. Chem. Phys. 79, 926)
- Water SPC/E: Berendsen 1987
- Metals EAM: Daw & Baskes 1984, or specific parameterizations

**Step 4: Extract parameters**
- Read the paper abstract/methods section
- Check Table 1 or similar for parameter values
- If not in main text, check Supplementary Information
- Download SI if needed (use Playwright)

**Step 5: Convert units if necessary**
Common conversions:
- kJ/mol → kcal/mol: divide by 4.184
- eV → kcal/mol: multiply by 23.06
- Å → nm: divide by 10

**Step 6: Document your source**
In your input file:
```lammps
# Lennard-Jones parameters for argon
# Source: Rahman, Phys. Rev. 136, A405 (1964)
# ε = 0.238 kcal/mol, σ = 3.405 Å
pair_coeff 1 1 0.238 3.405
```

### Example: Finding Argon LJ Parameters

```
1. Search: "argon lennard-jones parameters molecular dynamics"
2. Find: Rahman 1964 is the seminal paper for liquid Ar MD
3. Also find: Allen & Tildesley give ε/kB = 119.8 K, σ = 3.405 Å
4. Convert: ε = 119.8 K × 0.001987 kcal/mol/K = 0.238 kcal/mol
5. Use: pair_coeff 1 1 0.238 3.405
```

---

## 2. Pseudopotentials for DFT

### The Problem
QE needs pseudopotential files (.UPF) for each element. These depend on:
- Exchange-correlation functional (LDA, PBE, etc.)
- Pseudopotential type (NC, US, PAW)
- Accuracy requirements

### Where to Find Them

**Primary Sources (in order of preference):**

1. **SSSP (Standard Solid State Pseudopotentials)**
   - URL: https://www.materialscloud.org/discover/sssp/table/efficiency
   - Best for: Production calculations, validated accuracy
   - Two versions: "efficiency" (faster) and "precision" (more accurate)

2. **PseudoDojo**
   - URL: http://www.pseudo-dojo.org/
   - Best for: High-accuracy calculations, many elements

3. **QE Pseudopotential Library**
   - URL: https://www.quantum-espresso.org/pseudopotentials
   - Best for: Quick access, many functionals

4. **Materials Cloud**
   - URL: https://www.materialscloud.org/
   - Best for: Curated, tested pseudopotentials

### How to Acquire Pseudopotentials

**Step 1: Determine what you need**
```
Element: Si
Functional: PBE (most common for solids)
Type: Usually US or PAW for efficiency
```

**Step 2: Search and navigate**
```
Use WebSearch: "silicon PBE pseudopotential SSSP"
Or navigate directly to SSSP table
```

**Step 3: Download the file**
Use Playwright or WebFetch to download:
```
The file will be something like:
Si.pbe-n-rrkjus_psl.1.0.0.UPF
```

**Step 4: Save to resources directory**
```
Save to: workspaces/resources/pseudopotentials/
Or to your project workspace
```

**Step 5: Reference in input**
```fortran
ATOMIC_SPECIES
Si  28.0855  Si.pbe-n-rrkjus_psl.1.0.0.UPF
```

### Recommended Cutoffs

When you download a pseudopotential, also note the recommended cutoffs:
- ecutwfc: wavefunction cutoff (typically 30-60 Ry)
- ecutrho: charge density cutoff (typically 4-12× ecutwfc)

SSSP provides these explicitly. If not available, test convergence.

---

## 3. Crystal Structures

### Sources

1. **Materials Project** (API available)
   - Best for: Computed structures, properties
   - Use: MP API with mp-id

2. **Crystallography Open Database (COD)**
   - URL: https://www.crystallography.net/
   - Best for: Experimental structures

3. **ICSD** (subscription required)
   - Best for: Authoritative experimental data

4. **Paper Supplementary Information**
   - Often contains CIF files for novel structures

### How to Acquire

**From Materials Project:**
```python
from mp_api.client import MPRester
import os

api_key = os.environ.get("MP_API_KEY")
with MPRester(api_key) as mpr:
    structure = mpr.get_structure_by_material_id("mp-149")  # Silicon
    structure.to("poscar", "POSCAR")  # Save as VASP format
```

**From COD or papers:**
- Download CIF file
- Convert using ASE or pymatgen:
```python
from pymatgen.core import Structure
struct = Structure.from_file("structure.cif")
```

---

## 4. Supplementary Information from Papers

### Why It Matters
The main paper often says "parameters in SI" or "see Supporting Information". You need to get these files.

### How to Download SI

**Step 1: Find the paper DOI**
From Semantic Scholar, Google Scholar, or the paper itself.

**Step 2: Navigate to publisher page**
Use Playwright to:
- Go to the DOI URL
- Find "Supporting Information" or "Supplementary Materials" link
- Download the file (usually PDF or ZIP)

**Step 3: Parse the SI**
- If PDF: Read and extract values manually
- If ZIP: Extract and read data files
- If Excel/CSV: Parse directly

### Example Workflow
```
1. Search Semantic Scholar for "TIP4P water Jorgensen 1983"
2. Get DOI: 10.1063/1.445869
3. Navigate to: https://doi.org/10.1063/1.445869
4. Find paper, check if SI exists
5. For this classic paper, parameters are in Table I of main text
6. Extract: ε = 0.1550 kcal/mol, σ = 3.1536 Å, etc.
```

---

## 5. Validation

### Always Cross-Reference

When you find parameters:
1. Search for at least 2 sources
2. Check if values agree
3. Note any discrepancies
4. Use the most authoritative/cited source

### Physical Reasonableness

Check that parameters make sense:
- LJ ε for noble gases: ~0.01-1 kcal/mol
- LJ σ for atoms: ~2-5 Å
- Bond lengths: ~1-2 Å for common bonds
- Cutoffs: Should be > 2.5σ for LJ

---

## 6. Resource Caching

### Directory Structure

```
workspaces/resources/
├── pseudopotentials/
│   ├── pbe/
│   │   ├── Si.pbe-n-rrkjus_psl.1.0.0.UPF
│   │   └── ...
│   └── lda/
├── potentials/
│   ├── eam/
│   └── tersoff/
├── structures/
│   ├── cif/
│   └── poscar/
└── parameters/
    └── force_fields.json  # Cache of found parameters
```

### Caching Found Parameters

When you find parameters, save them:
```json
{
  "argon_lj": {
    "epsilon_kcal_mol": 0.238,
    "sigma_angstrom": 3.405,
    "source": "Rahman 1964, Phys. Rev. 136, A405",
    "notes": "For liquid argon near triple point"
  }
}
```

---

## Key Mindset

**You are a researcher, not a script executor.**

- Don't wait to be told what parameters to use
- Don't use "typical" values without citation
- Don't give up if the first search doesn't work
- DO search multiple sources
- DO download what you need
- DO validate what you find
- DO document everything

**The goal is: given only a scientific question, you acquire everything needed to answer it.**
