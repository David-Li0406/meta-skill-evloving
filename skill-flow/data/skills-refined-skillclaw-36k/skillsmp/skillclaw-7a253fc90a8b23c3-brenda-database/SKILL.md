---
name: brenda-database
description: Use this skill when you need to access the BRENDA enzyme database via SOAP API to retrieve kinetic parameters, reaction equations, and organism-specific enzyme information for biochemical research and metabolic pathway analysis.
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
km_data = get_km_values("1.1.1.1")  # Alcohol dehydrogenase

# Get Km values for specific organism
km_data = get_km_values("1.1.1.1", organism="Saccharomyces cerevisiae")

# Get Km values for specific substrate
km_data = get_km_values("1.1.1.1", substrate="ethanol")
```

**Parse Km Results**:
```python
for entry in km_data:
    print(f"Km: {entry}")
    # Example output: "organism*Homo sapiens#substrate*ethanol#kmValue*1.2#commentary*"
```

**Extract Specific Information**:
```python
from brenda_client import parse_km_entry, extract_organism_data

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

Retrieve reaction equations and stoichiometry for enzymes as needed.