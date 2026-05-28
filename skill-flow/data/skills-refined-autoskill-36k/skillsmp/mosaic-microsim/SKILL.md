---
name: mosaic-microsim
description: Run MOSAIC microsimulation and extract formatted results for paper
allowed-tools:
  - Read
  - Bash
  - Grep
---

# MOSAIC Microsimulation Runner

Run the NIT microsimulation and extract key results.

## Quick Run Command

```bash
cd "C:\Users\shapi\Work\Mosaic\MOSAIC Model\Verification" && python -c "
import pandas as pd
from config import PAPER
from functions import calc_nit_benefit, calc_median_from_deciles

# Load CBS data
income_file = 'Data/average_monthly_income_by_percentiles_2022.xlsx'
df = pd.read_excel(income_file, header=None)

# Extract decile data
CBS_DECILES = []
for i in range(10):
    decile = 10 - i
    hh = float(df.iloc[7, 1+i]) * 1000
    std_persons = float(df.iloc[9, 1+i])
    income = float(df.iloc[14, 1+i])
    equiv_income = income / std_persons
    CBS_DECILES.append({
        'decile': decile,
        'households': hh,
        'equiv_income': equiv_income,
    })
CBS_DECILES = sorted(CBS_DECILES, key=lambda x: x['decile'])

# Parameters
taper = PAPER['taper_implemented']
disregard = PAPER['disregard']
poverty_line_pre = PAPER['poverty_line']

scenarios = [
    ('Baseline', PAPER['floor_baseline']),
    ('Strong', PAPER['floor_strong']),
    ('AGI', PAPER['floor_agi']),
]

print('=' * 80)
print('MOSAIC MICROSIMULATION RESULTS')
print('=' * 80)
print(f'Pre-NIT poverty line: z = {poverty_line_pre:,} NIS/mo (BTL2023Poverty)')
print()
print(f'{\"Scenario\":>10} {\"Floor\":>8} {\"Post-Med\":>10} {\"Post-z\":>8} {\"Delta-z\":>8} {\"M>z?\":>6}')
print('-' * 80)

for name, floor in scenarios:
    post_deciles = []
    for d in CBS_DECILES:
        benefit = calc_nit_benefit(d['equiv_income'], floor, taper, disregard)
        post_deciles.append({
            'decile': d['decile'],
            'households': d['households'],
            'equiv_income': d['equiv_income'] + benefit
        })

    post_median = calc_median_from_deciles(post_deciles)
    post_z = 0.50 * post_median
    delta_z = (post_z - poverty_line_pre) / poverty_line_pre * 100
    exceeds = 'Yes' if floor > post_z else 'No'

    print(f'{name:>10} {floor:>8,} {post_median:>10,.0f} {post_z:>8,.0f} {delta_z:>7.0f}% {exceeds:>6}')

print('=' * 80)
"
```

## Output Format

The command produces a table like:

```
================================================================================
MOSAIC MICROSIMULATION RESULTS
================================================================================
Pre-NIT poverty line: z = 3,324 NIS/mo (BTL2023Poverty)

  Scenario    Floor   Post-Med   Post-z  Delta-z   M>z?
--------------------------------------------------------------------------------
  Baseline    6,350      9,800    4,900     +47%    Yes
    Strong    8,250     11,700    5,850     +76%    Yes
       AGI   13,500     16,950    8,475    +155%    Yes
================================================================================
```

## Key Metrics Extracted

| Metric | Description | Used In |
|--------|-------------|---------|
| Post-Median | Post-NIT median equiv income | Table 3 |
| Post-z | Post-NIT poverty line (50% of post-median) | Table 3 |
| Delta-z | % change from pre-NIT z | Table 3 |
| M>z? | Floor exceeds post-poverty line | Key finding |

## Formatting for Paper

### LaTeX Table Row Format:
```latex
Scenario & Floor & Post-Median & Post-z' & Delta-z & Headcount \\
```

### Example:
```latex
Baseline & 6,350 & 9,800 & 4,900 & +47\% & 0\% \\
Strong & 8,250 & 11,700 & 5,850 & +76\% & 0\% \\
\textbf{AGI} & \textbf{13,500} & \textbf{16,950} & \textbf{8,475} & \textbf{+155\%} & \textbf{0\%} \\
```

## Additional Calculations

### Gini Coefficient
```python
from functions import calc_gini_from_deciles
gini = calc_gini_from_deciles(post_deciles)
```

### Poverty Headcount (using pre-NIT z)
```python
total_hh = sum(d['households'] for d in post_deciles)
poor_hh = sum(d['households'] for d in post_deciles if d['equiv_income'] < poverty_line_pre)
headcount = poor_hh / total_hh * 100
```

## Project Structure

```
Verification/
├── config.py              # PAPER dict with parameters
├── functions.py           # calc_nit_benefit, calc_median_from_deciles, etc.
├── verify_layer1.ipynb    # Layer 1: Exogenous Inputs
├── verify_layer2.ipynb    # Layer 2: Calculated Values
├── verify_layer3.ipynb    # Layer 3: Simulated Values (microsim here)
├── verify_all.py          # Script to run all verifications
└── Data/                  # Source data files
```

## When to Use This Skill

- After changing NIT parameters (floor, taper, disregard) in config.py
- After updating CBS income data
- When verifying paper claims against simulation
- Before finalizing Table 3 values
