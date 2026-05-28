---
name: materials-database
description: Query materials databases for structures and properties. Use when asked to get crystal structures, material properties, phase diagrams, or thermodynamic data. Primary source is Materials Project, with NIST, PubChem as secondary.
allowed-tools:
  - Read
  - Write
  - Bash
  - WebSearch
  - WebFetch
---

# Materials Database Access

You are querying materials databases for structures and properties.

## Available Databases

### Materials Project (Primary)
- 150,000+ inorganic materials
- DFT-calculated properties
- Crystal structures
- Band gaps, formation energies
- Phase diagrams
- API: https://api.materialsproject.org/

### NIST Chemistry WebBook
- Thermodynamic data
- Spectroscopic data
- Phase change data
- URL: https://webbook.nist.gov/chemistry/

### PubChem
- Chemical compounds
- Molecular structures
- Properties
- URL: https://pubchem.ncbi.nlm.nih.gov/

### AFLOW
- Crystal structure database
- Calculated properties
- URL: http://aflowlib.org/

### Crystallography Open Database (COD)
- Experimental crystal structures
- URL: http://www.crystallography.net/cod/

## Materials Project API

### Using pymatgen (Recommended)

```python
import os
from mp_api.client import MPRester

# Initialize with API key from environment
api_key = os.environ.get("MP_API_KEY")
with MPRester(api_key) as mpr:
    # Get structure by formula
    docs = mpr.materials.summary.search(formula="TiO2")

    # Get by material ID
    structure = mpr.get_structure_by_material_id("mp-2657")

    # Search with properties
    results = mpr.materials.summary.search(
        band_gap=(1.0, 2.0),
        is_stable=True
    )
```

### Direct API Access

```bash
# Search for materials
curl -H "X-API-KEY: YOUR_KEY" \
  "https://api.materialsproject.org/materials/summary/?formula=Fe2O3"

# Get specific material
curl -H "X-API-KEY: YOUR_KEY" \
  "https://api.materialsproject.org/materials/mp-19770/"
```

## Common Queries

### Get Crystal Structure
1. Search by formula (e.g., "Fe2O3")
2. Get material ID (e.g., "mp-19770")
3. Download structure (CIF, POSCAR, etc.)

### Get Properties
- Band gap
- Formation energy
- Density
- Magnetic properties
- Elastic constants

### Phase Diagrams
- Stability of compositions
- Competing phases
- Synthesis guidance

## Structure File Formats

### CIF (Crystallographic Information File)
Standard format for crystal structures:
```
data_TiO2
_cell_length_a   4.5937
_cell_length_b   4.5937
_cell_length_c   2.9587
_cell_angle_alpha   90.000
_cell_angle_beta    90.000
_cell_angle_gamma   90.000
_symmetry_space_group_name_H-M   'P 42/m n m'
...
```

### POSCAR (VASP format)
```
TiO2 rutile
1.0
4.5937  0.0000  0.0000
0.0000  4.5937  0.0000
0.0000  0.0000  2.9587
Ti O
2 4
Direct
0.0000  0.0000  0.0000
0.5000  0.5000  0.5000
...
```

### XYZ
Simple atomic coordinates:
```
6
TiO2 unit cell
Ti  0.000  0.000  0.000
Ti  2.297  2.297  1.479
O   1.396  1.396  0.000
...
```

## Converting Structures

### Using ASE (Python)
```python
from ase.io import read, write

# Read CIF, write POSCAR
atoms = read('structure.cif')
write('POSCAR', atoms, format='vasp')

# Read CIF, write LAMMPS data
write('structure.data', atoms, format='lammps-data')
```

### Using pymatgen
```python
from pymatgen.core import Structure
from pymatgen.io.lammps.data import LammpsData

# Read CIF
struct = Structure.from_file('structure.cif')

# Write LAMMPS data file
lammps_data = LammpsData.from_structure(struct)
lammps_data.write_file('structure.data')
```

## Workflow

### Getting a Structure for Simulation

1. **Search Database**
   - Find material by formula or name
   - Check that it's the correct polymorph/phase

2. **Download Structure**
   - Get CIF or POSCAR format
   - Verify structure looks correct

3. **Convert for Simulation**
   - Convert to LAMMPS data or QE input format
   - May need to create supercell

4. **Add Force Field** (for MD)
   - Assign atom types
   - Apply force field parameters

### Getting Material Properties

1. **Search by Material ID or Formula**
2. **Check Data Quality**
   - Is it experimentally verified?
   - What level of theory (GGA, GGA+U, etc.)?
3. **Extract Relevant Properties**
4. **Document Source and Methodology**

## Data Quality Notes

### Materials Project
- Properties are DFT-calculated (GGA/GGA+U)
- Band gaps are typically underestimated
- Formation energies are referenced to elemental phases
- Stability is based on convex hull analysis

### Experimental vs Computed
- Always note whether data is experimental or computed
- Computed properties may differ from experiment
- Cross-reference when possible

## Saving Results

Save database queries to:
```
workspaces/project-name/
├── structures/
│   ├── mp-19770_Fe2O3.cif
│   ├── mp-19770_Fe2O3.vasp
│   └── mp-19770_Fe2O3.data
├── properties/
│   └── Fe2O3_properties.json
└── README.md  # Document sources
```

## Common Materials

### Oxides
- TiO2 (rutile: mp-2657, anatase: mp-390)
- Fe2O3 (hematite: mp-19770)
- ZnO (wurtzite: mp-2133)
- Al2O3 (corundum: mp-1143)

### Metals
- Fe (bcc: mp-13)
- Cu (fcc: mp-30)
- Al (fcc: mp-134)
- Pt (fcc: mp-126)

### Semiconductors
- Si (diamond: mp-149)
- GaAs (zincblende: mp-2534)
- GaN (wurtzite: mp-804)
