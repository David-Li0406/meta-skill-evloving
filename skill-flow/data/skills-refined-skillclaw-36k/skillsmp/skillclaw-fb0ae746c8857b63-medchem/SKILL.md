---
name: medchem
description: Use this skill when you need to apply drug-likeness rules, structural alerts, and complexity metrics for compound prioritization and library filtering in drug discovery workflows.
---

# Medchem

## Overview

Medchem is a Python library for molecular filtering and prioritization in drug discovery workflows. It allows the application of hundreds of well-established and novel molecular filters, structural alerts, and medicinal chemistry rules to efficiently triage and prioritize compound libraries at scale. Rules and filters are context-specific—use them as guidelines combined with domain expertise.

## When to Use This Skill

This skill should be used when:
- Applying drug-likeness rules (Lipinski, Veber, etc.) to compound libraries.
- Filtering molecules by structural alerts or PAINS patterns.
- Prioritizing compounds for lead optimization.
- Assessing compound quality and medicinal chemistry properties.
- Detecting reactive or problematic functional groups.
- Calculating molecular complexity metrics.

## Installation

```bash
pip install medchem
```

## Core Capabilities

### 1. Medicinal Chemistry Rules

Apply established drug-likeness rules to molecules using the `medchem.rules` module.

**Available Rules:**
- Rule of Five (Lipinski)
- Rule of Oprea
- Rule of CNS
- Rule of leadlike (soft and strict)
- Rule of three
- Rule of Reos
- Rule of drug
- Rule of Veber
- Golden triangle
- PAINS filters

**Single Rule Application:**

```python
import medchem as mc

# Apply Rule of Five to a SMILES string
smiles = "CC(=O)OC1=CC=CC=C1C(=O)O"  # Aspirin
passes = mc.rules.basic_rules.rule_of_five(smiles)
# Returns: True

# Check specific rules
passes_oprea = mc.rules.basic_rules.rule_of_oprea(smiles)
passes_cns = mc.rules.basic_rules.rule_of_cns(smiles)
```

**Multiple Rules with RuleFilters:**

```python
import datamol as dm
import medchem as mc

# Load molecules
mols = [dm.to_mol(smiles) for smiles in smiles_list]

# Create filter with multiple rules
rfilter = mc.rules.RuleFilters(
    rule_list=[
        "rule_of_five",
        "rule_of_oprea",
        "rule_of_cns",
        "rule_of_leadlike_soft"
    ]
)

# Apply filters with parallelization
results = rfilter(
    mols=mols,
    n_jobs=-1,  # Use all CPU cores
    progress=True
)
```

**Result Format:**
Results are returned as dictionaries with pass/fail status and detailed information for each rule.

### 2. Structural Alert Filters

Detect potentially problematic structural patterns using the `medchem.structural_alerts` module.