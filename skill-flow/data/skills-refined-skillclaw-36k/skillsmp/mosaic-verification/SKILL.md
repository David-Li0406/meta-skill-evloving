---
name: mosaic-verification
description: Guidelines for tracking numerical claims in the MOSAIC paper. Use BEFORE adding any numbers to the paper.
allowed-tools:
  - Read
  - Edit
  - Write
  - Bash
---

# MOSAIC Paper Verification System

## GOLDEN RULE

**NEVER fabricate numbers.** Only use values that are:
1. Explicitly provided by the user
2. Calculated from user-provided values with shown formula
3. Read from cited sources

When uncertain, use placeholder `[VALUE NEEDED]` and ask the user.

## Project Structure

```
Verification/
├── config.py              # DATA and PAPER dicts (edit this for values)
├── functions.py           # All calc_* functions (edit for formulas)
├── verify_layer1.ipynb    # Layer 1: Exogenous Inputs (1.1-1.6)
├── verify_layer2.ipynb    # Layer 2: Calculated Values (2.1-2.7)
├── verify_layer3.ipynb    # Layer 3: Simulated Values (3.1-3.5)
├── verify_all.py          # Script to run all verifications
├── number_hierarchy.md    # Master list of all numbers
└── Data/                  # Source data files
```

## Verification Notebooks by Layer

| Notebook | Layer | Sections | Contents |
|----------|-------|----------|----------|
| `verify_layer1.ipynb` | 1 | 1.1-1.6 | Exogenous inputs: economy data, elasticity, scenarios, NIT design, funding, GAD |
| `verify_layer2.ipynb` | 2 | 2.1-2.7 | Calculated values: derivations, break-even, floors, Saez, VAT, funding totals |
| `verify_layer3.ipynb` | 3 | 3.1-3.5 | Simulated values: CES production, fiscal balance, poverty, Monte Carlo |

## The Core Verification Files

### 1. `Verification/config.py`
**Purpose:** Central configuration for all data values
**When to update:** When adding or changing any numerical value
**Contains:** DATA dict (external sources) and PAPER dict (paper values)

### 2. `Verification/functions.py`
**Purpose:** All calculation functions for verification
**When to update:** When adding new calculation formulas
**Contains:** verify(), calc_breakeven(), calc_nit_benefit(), etc.

### 3. `Verification/number_hierarchy.md`
**Purpose:** Master registry of every numerical claim
**When to update:** Immediately when adding ANY number to the paper
**Format:** | ID | Value | Description | Source | Status |

## Status Codes

| Symbol | Meaning |
|--------|---------|
| ✓ VERIFIED | Value confirmed with source |
| ⚠ NEEDS_SOURCE | Value used but needs citation |
| ⚠ NEEDS_CALC | Derived value, show calculation |
| ✗ INCORRECT | Value conflicts with source |

## Scenario Convention

**AGI is the decision-relevant scenario.** When adding scenario-specific numbers:

| Marker | Meaning |
|--------|---------|
| **AGI** | Decision-relevant (policy designed for this) |
| Baseline ⚑ | Non-decision-relevant (optimistic) |
| Strong ⚑ | Non-decision-relevant (intermediate) |
| All | Universal parameter, applies to all scenarios |

Always mark which scenario a number belongs to. If it's NOT AGI, mark it with ⚑.

## Workflow: Adding New Content

1. **User provides text** with numerical claims
2. **Extract all numbers** from the text
3. **For each number:**
   - Add row to `number_hierarchy.md` with status ⚠ NEEDS_SOURCE
   - **Mark the scenario** (AGI, Baseline ⚑, Strong ⚑, or All)
   - Add to PAPER dict in `config.py`
4. **Never invent numbers** not in user's text
5. **Run verification:** Run `python verify_all.py` or open relevant layer notebook

## Running Verification

Run all verification notebooks:

```bash
cd Verification && python verify_all.py        # Run all layers
cd Verification && python verify_all.py --quick # Quick import test only
cd Verification && python verify_all.py --layer 1  # Run specific layer
```

Or open individual notebooks:
- `verify_layer1.ipynb` - Exogenous inputs (1.1-1.6)
- `verify_layer2.ipynb` - Calculated values (2.1-2.7)
- `verify_layer3.ipynb` - Simulated values (3.1-3.5)

All items should show [PASS] or have documented explanations.

## Common Mistakes to Avoid

1. Making up employment decomposition numbers
2. Fabricating percentage ranges
3. Inventing fiscal projections
4. Creating source citations without verification

If you don't have a number, ASK. Don't guess.

## Checklist: Updating Data Values

When changing a verified data value (e.g., Y_0, L, u_0), update ALL of these files:

### Required Updates

| File | What to Update |
|------|----------------|
| `Verification/config.py` | Update DATA and/or PAPER dict |
| `Verification/functions.py` | Add calc_* function (if new calculation) |
| `Verification/verify_layer*.ipynb` | Add verification cell to appropriate layer notebook |
| `Verification/number_hierarchy.md` | Update value, source, status |
| `Paper/The Mosaic Model.tex` | Update value in text/tables, add citation |
| `Paper/BibFile.bib` | Add/update source citation (if new source) |

### Verification Steps

1. Search for old value across all files: `grep -r "OLD_VALUE" .`
2. Update each file systematically
3. **Do NOT recalculate derived values** - the author will run `python verify_all.py` to regenerate calculations
4. Review any "KNOWN ISSUES" in number_hierarchy.md that may be resolved

### Files to Ignore

- `Daniel/` - Historical working documents, not part of verification system

---

## Adding New Calculations

**IMPORTANT:** When adding a new standalone calculation function, you MUST complete ALL 4 steps below. The appropriate layer notebook must be updated to include a cell that tests the new function.

The verification system is organized by `number_hierarchy.md` layers:
- **Layer 1:** Exogenous Inputs (1.1-1.6) → `verify_layer1.ipynb`
- **Layer 2:** Calculated Values (2.1-2.7) → `verify_layer2.ipynb`
- **Layer 3:** Simulated Values (3.1-3.5) → `verify_layer3.ipynb`

### Step 1: Add function to functions.py

Location: `Verification/functions.py`

Template:
```python
def calc_<name>(<inputs>) -> <output_type>:
    """<One-line description>.

    Formula: <plain text formula>

    Inputs:
        <param>: <description>
        ...

    Output: <description with units>
    """
    return <formula>
```

### Step 2: Add value to config.py

Location: `Verification/config.py` - add to PAPER dict under appropriate layer section.

### Step 3: Add verification cell to notebook (MANDATORY)

Location: Choose the appropriate layer notebook:
- `Verification/verify_layer1.ipynb` - for exogenous inputs (sections 1.x)
- `Verification/verify_layer2.ipynb` - for calculated values (sections 2.x)
- `Verification/verify_layer3.ipynb` - for simulated values (sections 3.x)

**This step is REQUIRED for any new calculation function.** The notebook serves as the executable verification that all calculations match paper values.

First import the function (if not using `from functions import *`):
```python
from functions import calc_<name>
```

Then add verification code:
```python
print("=" * 60)
print("X.Ya <DESCRIPTION> (<ID>)")
print("=" * 60)

result = calc_<name>(<args from PAPER dict>)
print(f"  <formula> = {result}")
verify("<key>", result, PAPER["<key>"])
```

For scenario-dependent calculations, loop through all three scenarios (see Simulation Guidelines below).

### Step 4: Update number_hierarchy.md

Add entry to appropriate layer table:
```markdown
| ID | Value | Description | Formula | Inputs | Function |
```

### Verification function signature

```python
verify(name: str, calculated: float, paper: float,
       tolerance: float = 0.01, is_data: bool = False)
```

- `tolerance=0.01` means 1% relative difference allowed
- `is_data=True` also checks against DATA dict

---

## Simulation Guidelines

When adding simulations to a verification notebook (typically `verify_layer3.ipynb`):

### Always Use All 3 Scenarios

For any scenario-dependent calculation, loop through all scenarios:

```python
scenarios = [
    ("Baseline", PAPER["<param>_baseline"]),
    ("Strong", PAPER["<param>_strong"]),
    ("AGI", PAPER["<param>_agi"]),
]

for name, value in scenarios:
    result = calc_function(value)
    print(f"  {name}: {result}")
```

### Never Hard-code Scenario Values

- **BAD:** `post_headcount = PAPER["poverty_agi"]`
- **GOOD:** Loop through all scenarios with values from PAPER dict

### Use Given Values

- Don't recalculate values that are given (e.g., initial poverty gap = 39.5%)
- Only calculate derived/post-NIT values
- State given values explicitly: `print(f"Initial: {value}% (source - given)")`

### Define Formula Parameters

When showing a formula, always define what each variable means:

```markdown
**Formula:** $<LaTeX formula>$

**Parameters:**
- $N$ = <description>
- $z$ = <description>
- ...
```

Example:
```markdown
**Formula:**
$$PG = \frac{1}{N} \sum_{i=1}^{q} \left( \frac{z - y_i}{z} \right)$$

**Parameters:**
- $N$ = Total population (households)
- $q$ = Number of poor households (income < z)
- $z$ = Poverty line = 50% of median equivalized income
- $y_i$ = Income of poor household $i$
```
