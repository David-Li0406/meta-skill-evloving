# Prostate Cancer Calculator - Complete Reference

## Table of Contents

1. [NCCN Risk Classification](#nccn-risk-classification)
2. [EAU Risk Classification](#eau-risk-classification)
3. [CAPRA Scores](#capra-scores)
4. [LNI Nomograms](#lni-nomograms)
5. [PSADT Calculation](#psadt-calculation)
6. [EAU BCR Risk Classification](#eau-bcr-risk-classification)
7. [Salvage RT Evidence](#salvage-rt-evidence)
8. [ADT Duration Evidence](#adt-duration-evidence)

---

## NCCN Risk Classification

Eight-tier system using PSA, Grade Group, clinical T-stage, and biopsy characteristics.

### Criteria

**Very Low Risk** - ALL criteria required:
- cT1c
- Grade Group 1
- PSA < 10 ng/mL
- < 3 positive biopsy cores
- ≤ 50% cancer in each core
- PSA density < 0.15 ng/mL/g

**Low Risk** - ALL criteria:
- cT1-cT2a
- Grade Group 1
- PSA < 10 ng/mL
- Does not meet Very Low criteria

**Favorable Intermediate Risk** - ALL criteria:
- 1 intermediate risk factor only (cT2b-cT2c OR GG2-3 OR PSA 10-20)
- Grade Group 1 or 2
- < 50% positive biopsy cores

**Unfavorable Intermediate Risk** - ANY criteria:
- 2-3 intermediate risk factors
- Grade Group 3 (Gleason 4+3=7)
- ≥ 50% positive biopsy cores

**High Risk** - exactly ONE feature:
- cT3a
- Grade Group 4-5
- PSA > 20 ng/mL

**Very High Risk** - ANY criteria:
- cT3b-cT4
- Primary Gleason pattern 5
- > 4 cores with Grade Group 4-5
- ≥ 2 high-risk features

**Regional (N1)**: Pathologically confirmed lymph node metastasis

**Metastatic**: M1a (non-regional nodes), M1b (bone), M1c (visceral)

### Implementation Logic

```python
def get_nccn_risk(psa, grade_group, t_stage, positive_cores, total_cores, 
                   max_core_involvement, psa_density, primary_gleason=None,
                   n_stage="N0", m_stage="M0"):
    
    if m_stage != "M0":
        return "Metastatic"
    if n_stage == "N1":
        return "Regional"
    
    pct_positive = (positive_cores / total_cores * 100) if total_cores > 0 else 0
    
    # Count risk factors
    intermediate_factors = sum([
        t_stage in ["T2b", "T2c"],
        grade_group in [2, 3],
        10 <= psa <= 20
    ])
    
    high_risk_factors = sum([
        t_stage == "T3a",
        grade_group >= 4,
        psa > 20
    ])
    
    # Very High Risk checks
    if t_stage in ["T3b", "T4"]:
        return "Very High"
    if primary_gleason == 5:
        return "Very High"
    if positive_cores > 4 and grade_group >= 4:
        return "Very High"
    if high_risk_factors >= 2:
        return "Very High"
    
    # High Risk
    if high_risk_factors == 1:
        return "High"
    
    # Unfavorable Intermediate
    if intermediate_factors >= 2 or grade_group == 3 or pct_positive >= 50:
        return "Unfavorable Intermediate"
    
    # Favorable Intermediate
    if intermediate_factors == 1 and grade_group <= 2 and pct_positive < 50:
        return "Favorable Intermediate"
    
    # Low vs Very Low
    if t_stage in ["T1a", "T1b", "T1c", "T2a"] and grade_group == 1 and psa < 10:
        if (t_stage == "T1c" and positive_cores < 3 and 
            max_core_involvement <= 50 and psa_density < 0.15):
            return "Very Low"
        return "Low"
    
    return "Unable to classify"
```

---

## EAU Risk Classification

Three-tier system with intermediate subdivision.

### Criteria

**Low Risk** - ALL required:
- Grade Group 1
- PSA < 10 ng/mL
- cT1-cT2a

**Intermediate Favorable**:
- GG2 with PSA < 10 and cT1-cT2b
- OR GG1 with PSA 10-20

**Intermediate Unfavorable**:
- GG2 with PSA 10-20
- OR GG3 at any PSA ≤ 20

**High-Risk Localized** - ANY:
- Grade Group 4-5
- PSA > 20 ng/mL
- cT2c

**High-Risk Locally Advanced**:
- cT3-cT4
- OR cN+

### Key Difference from NCCN

EAU classifies cT2c as high-risk; NCCN considers it intermediate.

---

## CAPRA Scores

### CAPRA (Pre-treatment)

Score range: 0-10 points

| Variable | Criteria | Points |
|----------|----------|--------|
| PSA (ng/mL) | 2.1-6.0 | 0 |
| | 6.1-10.0 | 1 |
| | 10.1-20.0 | 2 |
| | 20.1-30.0 | 3 |
| | > 30 | 4 |
| Gleason pattern | No 4 or 5 | 0 |
| | Secondary 4 or 5 | 1 |
| | Primary 4 or 5 | 3 |
| Clinical T-stage | T1-T2 | 0 |
| | T3a | 1 |
| % Positive cores | < 34% | 0 |
| | ≥ 34% | 1 |
| Age | < 50 years | 0 |
| | ≥ 50 years | 1 |

**Risk Groups**: Low (0-2), Intermediate (3-5), High (6-10)

**Interpretation**: Each 2-point increase ≈ doubles recurrence risk (c-index 0.66)

### CAPRA-S (Post-prostatectomy)

Score range: 0-12 points

| Variable | Criteria | Points |
|----------|----------|--------|
| Pre-op PSA | ≤ 6 ng/mL | 0 |
| | 6.01-10 | 1 |
| | 10.01-20 | 2 |
| | > 20 | 3 |
| Pathologic Gleason | ≤ 3+3 | 0 |
| | 3+4 | 1 |
| | 4+3 | 2 |
| | 8-10 | 3 |
| Surgical margin | Negative | 0 |
| | Positive | 2 |
| ECE | Absent | 0 |
| | Present | 1 |
| SVI | Absent | 0 |
| | Present | 2 |
| LNI | Absent | 0 |
| | Present | 1 |

**Risk Groups**: Low (0-2), Intermediate (3-5), High (≥6)

**Interpretation**: Each point increases recurrence hazard by 1.54-fold (c-index 0.77)

---

## LNI Nomograms

### Briganti 2017 Nomogram

The only version with published beta coefficients. Developed from 2,872 patients, 11.1% LNI rate, c-statistic 0.908.

**Formula**:
```
LP = -5.8717 
     + (0.0826 × PSA)
     + (0.3633 × cT2)      # 1 if T2, else 0
     + (0.9555 × cT3)      # 1 if T3, else 0
     + (0.3293 × GG2)      # 1 if Grade Group 2, else 0
     + (0.7419 × GG3)      # 1 if Grade Group 3, else 0
     + (0.8755 × GG4)      # 1 if Grade Group 4, else 0
     + (1.2809 × GG5)      # 1 if Grade Group 5, else 0
     + (0.0130 × %highest) # % cores with highest grade
     + (0.0113 × %lowest)  # % cores with lowest grade

P(LNI) = 1 / (1 + exp(-LP))
```

**Threshold**: ≥7% → recommend ePLND

**Note**: T1 is reference category (both cT2 and cT3 = 0). GG1 is reference (all GG indicators = 0).

### Briganti 2012 Nomogram

Uses PSA, clinical stage, primary and secondary Gleason grade, % positive cores. AUC 87.6%.

Coefficients not publicly available—use lookup tables or online calculator.

### Roach Formula (1994)

```
LNI Risk (%) = (2/3 × PSA) + [(Gleason Score - 6) × 10]
```

**Example**: PSA 15, GS 7 → (2/3 × 15) + [(7-6) × 10] = 10 + 10 = 20%

**Threshold**: ≥15% → consider pelvic nodal RT

**Limitations**: Overestimates contemporary LNI by 2.5-16 fold but validated for RT field decisions.

### Yale Formula

```
LNI Risk (%) = (Gleason Score - 5) × [PSA/3 + 1.5 × T]
```

Where T = 0 (cT1c), 1 (cT2a), 2 (cT2b/c)

### MSKCC/Partin Tables

Lookup-based using PSA strata, clinical stage, and Grade Group. AUC 0.918 for LNI.

**PSA Strata**: 0-2.5, 2.6-4.0, 4.1-6.0, 6.1-10.0, >10.0 ng/mL

**Clinical Stage**: T1c, T2a, T2b/c

Available at: https://www.mskcc.org/nomograms/prostate

### ABS PSMA-PET Nomogram

First PSMA-PET era tool. Incorporates imaging status alongside PSA, MRI T-stage, Grade Group, biopsy technique, % significant cores.

**Threshold**: ≥8% → ePLND recommended (if not using this threshold, 15% of patients could avoid ePLND without missing LNI)

AUC 0.81 with PSMA-PET inclusion.

---

## PSADT Calculation

### Formula

Using linear regression of ln(PSA) vs time:

```
PSADT = ln(2) / slope = 0.693 / slope
```

For two values:
```
PSADT = [0.693 × (t₂ - t₁)] / [ln(PSA₂) - ln(PSA₁)]
```

Where time is in months (or same unit as desired PSADT output).

### Requirements

- Minimum 3 PSA values
- ≥ 3 months observation period
- All values ≥ 0.20 ng/mL
- All values rising (PSA₂ > PSA₁)
- Same laboratory/assay
- Testosterone stable during measurement
- Maximum 12 months of values (reflects current disease activity)

### Clinical Thresholds

| PSADT | Interpretation |
|-------|----------------|
| < 3 months | Extremely high risk; PCa mortality ~100%, median survival 5-6 years |
| < 6 months | Rapid progression; consider systemic therapy |
| < 9 months | EMBARK trial criteria; qualifies for enzalutamide |
| < 10-12 months | EAU high-risk BCR |
| > 15 months | Favorable prognosis; observation may be appropriate |

### Implementation

```python
import numpy as np
from scipy import stats

def calculate_psadt(psa_values):
    """
    Args:
        psa_values: list of (time_in_days, psa_value) tuples
    Returns:
        PSADT in months, or None if invalid
    """
    if len(psa_values) < 3:
        return None
    
    times = np.array([t for t, _ in psa_values])
    psas = np.array([p for _, p in psa_values])
    
    # Validate rising PSA
    if not all(psas[i] < psas[i+1] for i in range(len(psas)-1)):
        return None
    
    # Convert to months and take log
    times_months = times / 30.44
    ln_psa = np.log(psas)
    
    # Linear regression
    slope, _, _, _, _ = stats.linregress(times_months, ln_psa)
    
    if slope <= 0:
        return None
    
    return 0.693 / slope
```

---

## EAU BCR Risk Classification

After radical prostatectomy, classify biochemical recurrence into low-risk vs high-risk.

### Low-Risk BCR (ALL required)

- PSADT > 12 months
- Grade Group 1-3 (pathologic)
- Time from RP to BCR > 18 months

**Management**: Monitoring may be appropriate

### High-Risk BCR (ANY criterion)

- PSADT ≤ 12 months
- Grade Group 4-5 (pathologic)

**Management**: Early salvage RT recommended

### Special High-Risk Criteria (M0, post-RP)

If PSADT ≤ 9 months AND PSA ≥ 1 ng/mL:
→ Strongly consider enzalutamide ± ADT (EMBARK trial)

---

## Salvage RT Evidence

### RTOG 0534 / SPPORT Trial

**Design**: 1,792 patients with post-RP PSA 0.1-2.0 ng/mL randomized to:
1. Prostate bed RT alone
2. Prostate bed RT + 4-6 months ADT
3. Prostate bed RT + pelvic nodes + 4-6 months ADT

**Eligibility**:
- pT2-pT3 disease
- Gleason ≤ 9
- No palpable fossa mass
- N0 or Nx

**Results** (5-year freedom from progression):
- RT alone: 71%
- RT + ADT: 81%
- RT + pelvic nodes + ADT: 87%

**Key Findings**:
- Pelvic nodal RT reduced distant metastasis (HR 0.52)
- Pelvic nodal RT reduced prostate cancer death (HR 0.51)
- Greatest benefit in patients with PSA > 0.35 ng/mL

**Pelvic CTV**: Obturator, external iliac, proximal internal iliac, presacral, common iliac nodes to L5-S1. Dose: 45 Gy at 1.8 Gy/fraction.

### Pelvic Node Coverage Decision Algorithm

```
IF using ADT AND (pre-SRT PSA > 0.35 OR LNI risk ≥ 15%):
    → Include pelvic nodes
ELSE IF pre-SRT PSA ≤ 0.35 AND LNI risk < 15%:
    → Prostate bed only may be sufficient
```

---

## ADT Duration Evidence

### GETUG-AFU 16

**Design**: 743 patients, PSA 0.2-2.0 ng/mL, randomized to:
- Salvage RT alone
- Salvage RT + 6 months goserelin

**Results** (10-year):
- PFS: 49% vs 64% (HR 0.54)
- MFS: 69% vs 75% (HR 0.73)
- OS: No difference

**Conclusion**: 6 months ADT improves PFS and MFS but not OS

### RTOG 9601

**Design**: 760 patients, PSA 0.2-4.0 ng/mL, randomized to:
- Salvage RT + placebo
- Salvage RT + 24 months bicalutamide 150mg

**Results** (12-year):
- OS: 71.3% vs 76.3% (HR 0.77, p=0.04)
- PCa mortality: 13.4% vs 5.8%
- Metastases: 23% vs 14.5%

**Critical PSA Subgroup Analysis**:

| Pre-SRT PSA | OS Benefit | HR | Recommendation |
|-------------|------------|-----|----------------|
| > 1.5 ng/mL | +25% absolute | 0.45 | Strong benefit from 24mo ADT |
| 0.7-1.5 ng/mL | Moderate | 0.61 | Consider 24mo ADT |
| < 0.7 ng/mL | None | NS | No benefit; potential harm (cardiac) |

### RADICALS-HD

**Design**: 2,839 patients, three arms:
- No ADT
- 6 months ADT
- 24 months ADT

**Results**:
- 6mo vs none: No MFS improvement
- 24mo vs 6mo: 78.1% vs 71.9% 10-year MFS (HR 0.77, p=0.029)
- OS: No difference
- Grade ≥3 toxicity: 14% (6mo) vs 19% (24mo)

### ADT Duration Decision Algorithm

```
LOW-RISK PROFILE (all of):
  - Pre-SRT PSA < 0.7 ng/mL
  - Grade Group 1-3
  - PSADT > 12 months
  - Favorable/low Decipher
  → RT ALONE (ADT may cause harm)

INTERMEDIATE-RISK PROFILE:
  - Pre-SRT PSA 0.7-1.5 ng/mL
  - Single high-risk feature
  → SHORT-TERM ADT (4-6 months)

HIGH-RISK PROFILE (any of):
  - Pre-SRT PSA > 1.5 ng/mL
  - Grade Group 4-5
  - PSADT ≤ 6 months
  - Multiple adverse pathology features
  - Decipher ≥ 0.6
  - pN1 disease
  → LONG-TERM ADT (18-24 months)
```

### Prostate Bed RT Dose

- Standard: 64-66 Gy
- SAKK 09/10 showed no benefit from 70 Gy escalation
- Pelvic nodes when included: 45 Gy

---

## Stephenson/Tendulkar Nomogram

Predicts progression-free survival after salvage RT.

**Variables** (11 parameters):
1. Pre-SRT PSA level
2. Prostatectomy Gleason grade
3. PSADT
4. Surgical margins (positive/negative)
5. ADT use (yes/no)
6. Lymph node status
7. Time from surgery to SRT
8. Seminal vesicle invasion
9. Extracapsular extension
10. Pre-prostatectomy PSA
11. Persistently elevated post-op PSA

**Performance**: c-index 0.69

**Key Finding**: Patients treated at PSA ≤ 0.50 ng/mL achieved 48% 6-year DFS

Tendulkar 2016 update provides 5-year and 10-year predictions for BCR and distant metastases.

---

## Decipher Genomic Classifier Integration

When Decipher score available, modify ADT recommendations:

| Decipher | Pre-SRT PSA | Recommendation |
|----------|-------------|----------------|
| Low (< 0.45) | < 0.7 ng/mL | RT alone; ADT unlikely to benefit |
| Low | ≥ 0.7 ng/mL | Short-term ADT (4-6 mo) |
| Intermediate (0.45-0.6) | Any | Short-term ADT (4-6 mo) |
| High (≥ 0.6) | Any | Long-term ADT (18-24 mo) |
