---
name: brenda-database
description: Access BRENDA enzyme database via SOAP API to retrieve kinetic parameters, reaction equations, organism data, and substrate-specific enzyme information for biochemical research and metabolic pathway analysis.
---

# BRENDA Database

## Overview

BRENDA (BRaunschweig ENzyme DAtabase) is the world's most comprehensive enzyme information system, containing detailed enzyme data from scientific literature. Query kinetic parameters (Km, kcat), reaction equations, substrate specificities, organism information, and optimal conditions for enzymes using the official SOAP API. Access over 45,000 enzymes with millions of kinetic data points for biochemical research, metabolic engineering, and enzyme discovery.

## When to Use This Skill

This skill should be used when:
- Searching for enzyme kinetic parameters (Km, kcat, Vmax)
- Retrieving reaction equations and stoichiometry
- Finding enzymes for specific substrates or reactions
- Comparing enzyme properties across different organisms
- Investigating optimal pH, temperature, and conditions
- Accessing enzyme inhibition and activation data
- Supporting metabolic pathway reconstruction and retrosynthesis
- Performing enzyme engineering and optimization studies
- Analyzing substrate specificity and cofactor requirements

## Core Capabilities

### 1. Kinetic Parameter Retrieval

Access comprehensive kinetic data for enzymes:

**Get Km Values by EC Number**:
```python
from brenda_client import get_km_values

# Get Km values for all organisms
km_data = get_km_values("<ec_number>")  # Example: "1.1.1.1"

# Get Km values for specific organism
km_data = get_km_values("<ec_number>", organism="<organism_name>")

# Get Km values for specific substrate
km_data = get_km_values("<ec_number>", substrate="<substrate_name>")
```

**Parse Km Results**:
```python
for entry in km_data:
    print(f"Km: {entry}")
```

**Extract Specific Information**:
```python
from scripts.brenda_queries import parse_km_entry, extract_organism_data

for entry in km_data:
    parsed = parse_km_entry(entry)
    organism = extract_organism_data(entry)
    print(f"Organism: {parsed['organism']}")
    print(f"Substrate: {parsed['substrate']}")
    print(f"Km value: {parsed['km_value']}")
    print(f"pH: {parsed.get('ph', 'N/A')}")
    print(f"Temperature: {parsed.get('temperature', 'N/A')}")
```

### 2. Reaction Information

Retrieve reaction equations and details:

**Get Reactions by EC Number**:
```python
from brenda_client import get_reactions

# Get all reactions for EC number
reactions = get_reactions("<ec_number>")

# Filter by organism
reactions = get_reactions("<ec_number>", organism="<organism_name>")

# Search specific reaction
reactions = get_reactions("<ec_number>", reaction="<reaction_string>")
```

**Process Reaction Data**:
```python
from scripts.brenda_queries import parse_reaction_entry, extract_substrate_products

for reaction in reactions:
    parsed = parse_reaction_entry(reaction)
    substrates, products = extract_substrate_products(reaction)

    print(f"Reaction: {parsed['reaction']}")
    print(f"Organism: {parsed['organism']}")
    print(f"Substrates: {substrates}")
    print(f"Products: {products}")
```

### 3. Enzyme Discovery

Find enzymes for specific biochemical transformations:

**Find Enzymes by Substrate**:
```python
from scripts.brenda_queries import search_enzymes_by_substrate

# Find enzymes that act on a specific substrate
enzymes = search_enzymes_by_substrate("<substrate_name>", limit=20)

for enzyme in enzymes:
    print(f"EC: {enzyme['ec_number']}")
    print(f"Name: {enzyme['enzyme_name']}")
    print(f"Reaction: {enzyme['reaction']}")
```

**Find Enzymes by Product**:
```python
from scripts.brenda_queries import search_enzymes_by_product

# Find enzymes that produce a specific product
enzymes = search_enzymes_by_product("<product_name>", limit=10)
```

**Search by Reaction Pattern**:
```python
from scripts.brenda_queries import search_by_pattern

# Find enzymes by reaction pattern
enzymes = search_by_pattern("<reaction_pattern>", limit=15)
```

### 4. Organism-Specific Enzyme Data

Compare enzyme properties across organisms:

**Get Enzyme Data for Multiple Organisms**:
```python
from scripts.brenda_queries import compare_across_organisms

organisms = ["<organism1>", "<organism2>", "<organism3>"]
comparison = compare_across_organisms("<ec_number>", organisms)

for org_data in comparison:
    print(f"Organism: {org_data['organism']}")
    print(f"Avg Km: {org_data['average_km']}")
    print(f"Optimal pH: {org_data['optimal_ph']}")
    print(f"Temperature range: {org_data['temperature_range']}")
```

**Find Organisms with Specific Enzyme**:
```python
from scripts.brenda_queries import get_organisms_for_enzyme

organisms = get_organisms_for_enzyme("<ec_number>")
print(f"Found {len(organisms)} organisms with this enzyme")
```

### 5. Environmental Parameters

Access optimal conditions and environmental parameters:

**Get pH and Temperature Data**:
```python
from scripts.brenda_queries import get_environmental_parameters

params = get_environmental_parameters("<ec_number>")

print(f"Optimal pH range: {params['ph_range']}")
print(f"Optimal temperature: {params['optimal_temperature']}")
print(f"Stability pH: {params['stability_ph']}")
print(f"Temperature stability: {params['temperature_stability']}")
```

**Cofactor Requirements**:
```python
from scripts.brenda_queries import get_cofactor_requirements

cofactors = get_cofactor_requirements("<ec_number>")
for cofactor in cofactors:
    print(f"Cofactor: {cofactor['name']}")
    print(f"Type: {cofactor['type']}")
    print(f"Concentration: {cofactor['concentration']}")
```

### 6. Substrate Specificity

Analyze enzyme substrate preferences:

**Get Substrate Specificity Data**:
```python
from scripts.brenda_queries import get_substrate_specificity

specificity = get_substrate_specificity("<ec_number>")

for substrate in specificity:
    print(f"Substrate: {substrate['name']}")
    print(f"Km: {substrate['km']}")
    print(f"Vmax: {substrate['vmax']}")
    print(f"kcat: {substrate['kcat']}")
    print(f"Specificity constant: {substrate['kcat_km_ratio']}")
```

**Compare Substrate Preferences**:
```python
from scripts.brenda_queries import compare_substrate_affinity

comparison = compare_substrate_affinity("<ec_number>")
sorted_by_km = sorted(comparison, key=lambda x: x['km'])

for substrate in sorted_by_km[:5]:  # Top 5 lowest Km
    print(f"{substrate['name']}: Km = {substrate['km']}")
```

### 7. Inhibition and Activation

Access enzyme regulation data:

**Get Inhibitor Information**:
```python
from scripts.brenda_queries import get_inhibitors

inhibitors = get_inhibitors("<ec_number>")

for inhibitor in inhibitors:
    print(f"Inhibitor: {inhibitor['name']}")
    print(f"Type: {inhibitor['type']}")
    print(f"Ki: {inhibitor['ki']}")
    print(f"IC50: {inhibitor['ic50']}")
```

**Get Activator Information**:
```python
from scripts.brenda_queries import get_activators

activators = get_activators("<ec_number>")

for activator in activators:
    print(f"Activator: {activator['name']}")
    print(f"Effect: {activator['effect']}")
    print(f"Mechanism: {activator['mechanism']}")
```

### 8. Enzyme Engineering Support

Find engineering targets and alternatives:

**Find Thermophilic Homologs**:
```python
from scripts.brenda_queries import find_thermophilic_homologs

thermophilic = find_thermophilic_homologs("<ec_number>", min_temp=50)

for enzyme in thermophilic:
    print(f"Organism: {enzyme['organism']}")
    print(f"Optimal temp: {enzyme['optimal_temperature']}")
    print(f"Km: {enzyme['km']}")
```

**Find Alkaline/ Acid Stable Variants**:
```python
from scripts.brenda_queries import find_ph_stable_variants

alkaline = find_ph_stable_variants("<ec_number>", min_ph=8.0)
acidic = find_ph_stable_variants("<ec_number>", max_ph=6.0)
```

### 9. Kinetic Modeling

Prepare data for kinetic modeling:

**Get Kinetic Parameters for Modeling**:
```python
from scripts.brenda_queries import get_modeling_parameters

model_data = get_modeling_parameters("<ec_number>", substrate="<substrate_name>")

print(f"Km: {model_data['km']}")
print(f"Vmax: {model_data['vmax']}")
print(f"kcat: {model_data['kcat']}")
print(f"Enzyme concentration: {model_data['enzyme_conc']}")
print(f"Temperature: {model_data['temperature']}")
print(f"pH: {model_data['ph']}")
```

**Generate Michaelis-Menten Plots**:
```python
from scripts.brenda_visualization import plot_michaelis_menten

# Generate kinetic plots
plot_michaelis_menten("<ec_number>", substrate="<substrate_name>")
```

## Installation Requirements

```bash
uv pip install zeep requests pandas matplotlib seaborn
```

## Authentication Setup

BRENDA requires authentication credentials:

1. **Create .env file**:
```
BRENDA_EMAIL=your.email@example.com
BRENDA_PASSWORD=your_brenda_password
```

2. **Or set environment variables**:
```bash
export BRENDA_EMAIL="your.email@example.com"
export BRENDA_PASSWORD="your_brenda_password"
```

3. **Register for BRENDA access**:
   - Visit https://www.brenda-enzymes.org/
   - Create an account
   - Check your email for credentials
   - Note: There's also `BRENDA_EMIAL` (note the typo) for legacy support

## Helper Scripts

This skill includes comprehensive Python scripts for BRENDA database queries:

### scripts/brenda_queries.py

Provides high-level functions for enzyme data analysis:

**Key Functions**:
- `parse_km_entry(entry)`: Parse BRENDA Km data entries
- `parse_reaction_entry(entry)`: Parse reaction data entries
- `extract_organism_data(entry)`: Extract organism-specific information
- `search_enzymes_by_substrate(substrate, limit)`: Find enzymes for substrates
- `search_enzymes_by_product(product, limit)`: Find enzymes producing products
- `compare_across_organisms(ec_number, organisms)`: Compare enzyme properties
- `get_environmental_parameters(ec_number)`: Get pH and temperature data
- `get_cofactor_requirements(ec_number)`: Get cofactor information
- `get_substrate_specificity(ec_number)`: Analyze substrate preferences
- `get_inhibitors(ec_number)`: Get enzyme inhibition data
- `get_activators(ec_number)`: Get enzyme activation data
- `find_thermophilic_homologs(ec_number, min_temp)`: Find heat-stable variants
- `get_modeling_parameters(ec_number, substrate)`: Get parameters for kinetic modeling
- `export_kinetic_data(ec_number, format, filename)`: Export data to file

**Usage**:
```python
from scripts.brenda_queries import search_enzymes_by_substrate, compare_across_organisms

# Search for enzymes
enzymes = search_enzymes_by_substrate("<substrate_name>", limit=20)

# Compare across organisms
comparison = compare_across_organisms("<ec_number>", ["<organism1>", "<organism2>"])
```

### scripts/brenda_visualization.py

Provides visualization functions for enzyme data:

**Key Functions**:
- `plot_kinetic_parameters(ec_number)`: Plot Km and kcat distributions
- `plot_organism_comparison(ec_number, organisms)`: Compare organisms
- `plot_pH_profiles(ec_number)`: Plot pH activity profiles
- `plot_temperature_profiles(ec_number)`: Plot temperature activity profiles
- `plot_substrate_specificity(ec_number)`: Visualize substrate preferences
- `plot_michaelis_menten(ec_number, substrate)`: Generate kinetic curves
- `create_heatmap_data(enzymes, parameters)`: Create data for heatmaps
- `generate_summary_plots(ec_number)`: Create comprehensive enzyme overview

**Usage**:
```python
from scripts.brenda_visualization import plot_kinetic_parameters, plot_michaelis_menten

# Plot kinetic parameters
plot_kinetic_parameters("<ec_number>")

# Generate Michaelis-Menten curve
plot_michaelis_menten("<ec_number>", substrate="<substrate_name>")
```

### scripts/enzyme_pathway_builder.py

Build enzymatic pathways and retrosynthetic routes:

**Key Functions**:
- `find_pathway_for_product(product, max_steps)`: Find enzymatic pathways
- `build_retrosynthetic_tree(target, depth)`: Build retrosynthetic tree
- `suggest_enzyme_substitutions(ec_number, criteria)`: Suggest enzyme alternatives
- `calculate_pathway_feasibility(pathway)`: Evaluate pathway viability
- `optimize_pathway_conditions(pathway)`: Suggest optimal conditions
- `generate_pathway_report(pathway, filename)`: Create detailed pathway report

**Usage**:
```python
from scripts.enzyme_pathway_builder import find_pathway_for_product, build_retrosynthetic_tree

# Find pathway to product
pathway = find_pathway_for_product("<product_name>", max_steps=3)

# Build retrosynthetic tree
tree = build_retrosynthetic_tree("<product_name>", depth=2)
```

## API Rate Limits and Best Practices

**Rate Limits**:
- BRENDA API has moderate rate limiting
- Recommended: 1 request per second for sustained usage
- Maximum: 5 requests per 10 seconds

**Best Practices**:
1. **Cache results**: Store frequently accessed enzyme data locally
2. **Batch queries**: Combine related requests when possible
3. **Use specific searches**: Narrow down by organism, substrate when possible
4. **Handle missing data**: Not all enzymes have complete data
5. **Validate EC numbers**: Ensure EC numbers are in correct format
6. **Implement delays**: Add delays between consecutive requests
7. **Use wildcards wisely**: Use '*' for broader searches when appropriate
8. **Monitor quota**: Track your API usage

**Error Handling**:
```python
from brenda_client import get_km_values, get_reactions
from zeep.exceptions import Fault, TransportError

try:
    km_data = get_km_values("<ec_number>")
except RuntimeError as e:
    print(f"Authentication error: {e}")
except Fault as e:
    print(f"BRENDA API error: {e}")
except TransportError as e:
    print(f"Network error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Common Workflows

### Workflow 1: Enzyme Discovery for New Substrate

Find suitable enzymes for a specific substrate:

```python
from brenda_client import get_km_values
from scripts.brenda_queries import search_enzymes_by_substrate, compare_substrate_affinity

# Search for enzymes that act on substrate
substrate = "<substrate_name>"
enzymes = search_enzymes_by_substrate(substrate, limit=15)

print(f"Found {len(enzymes)} enzymes for {substrate}")
for enzyme in enzymes:
    print(f"EC {enzyme['ec_number']}: {enzyme['enzyme_name']}")

# Get kinetic