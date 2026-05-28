---
name: mosaic-sync-number
description: Synchronize a verified number across all MOSAIC project files (paper, notebook, hierarchy)
allowed-tools:
  - Read
  - Edit
  - Write
  - Grep
  - Glob
  - Bash
---

# MOSAIC Number Synchronization

Use this skill when updating a verified data value across the project.

## Required Information

Before starting, gather:
1. **Number ID** (e.g., PL01, D06, SF01)
2. **New value**
3. **Source citation** (e.g., BTL2023Poverty, CBS2024)
4. **Old value** (to search and replace)

## Update Checklist

### Step 1: Update config.py

**Location:** `Verification/config.py`

1. **DATA dict:** Add/update the value with source comment
   ```python
   "key_name": value,  # Source: citation
   ```

2. **PAPER dict:** Add/update to match
   ```python
   "key_name": value,  # Source
   ```

### Step 2: Update number_hierarchy.md

**Location:** `Verification/number_hierarchy.md`

Find the ID in the appropriate section and update:
- Value column
- Method/Source column
- Status to `VERIFIED` if confirmed

### Step 3: Update Paper

**Location:** `Paper/The Mosaic Model.tex`

1. **Search for old value:**
   ```bash
   grep -n "OLD_VALUE" "Paper/The Mosaic Model.tex"
   ```

2. **Update each occurrence** with new value and citation

3. **Common locations:**
   - Section 5 (Results): Tables and text
   - Appendix C: Methodology notes
   - Table footnotes

### Step 4: Update BibFile (if new source)

**Location:** `Paper/BibFile.bib`

If citing a new source, add entry:
```bibtex
@online{CitationKey,
  author = {{Organization}},
  title = {Title},
  year = {2024},
  note = {Key value: X. Retrieved DATE},
  url = {URL}
}
```

### Step 5: Verify Consistency

Run:
```bash
grep -rn "OLD_VALUE" Verification/ Paper/
```

Should return no matches for old value.

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

## Number ID Conventions

| Prefix | Category | Example |
|--------|----------|---------|
| D | Data inputs | D06 (labor share) |
| PL | Poverty lines | PL01 (pre-NIT z) |
| SF | Scenario floors | SF01-SF03 |
| PV | Poverty results | PV01-PV13 |
| FI | Fiscal items | FI01-FI11 |
| N | NIT parameters | N01-N06 |

## Example: Updating Poverty Line

```
ID: PL01
Old: 3,708
New: 3,324
Source: BTL2023Poverty

1. config.py:
   DATA["poverty_line"] = 3324  # BTL2023Poverty
   PAPER["poverty_line"] = 3324

2. number_hierarchy.md:
   | PL01 | 3,324 | Pre-NIT poverty line | BTL2023Poverty | VERIFIED |

3. Paper (grep for 3,708 or 3708):
   - Table footnotes
   - Appendix methodology

4. Derived values may need recalculation (e.g., delta z percentages)
```

## Final Commit Message Template

```
Update [ID] to [VALUE] from [SOURCE]

- Update config.py DATA/PAPER dicts
- Update number_hierarchy.md
- Update Paper text/tables
- [Any derived value changes]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```
