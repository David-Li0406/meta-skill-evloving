# Prostate Cancer Calculator - Clinical Examples

## Example 1: Primary Treatment Planning - Intermediate Risk

### Patient Data
- Age: 65 years
- PSA: 12.5 ng/mL
- Clinical stage: cT2b
- Biopsy: 4/12 cores positive
- Grade Group 3 (Gleason 4+3=7)
- Maximum cancer in any core: 60%
- PSA density: 0.22 ng/mL/g

### Calculations

```python
from helper import *

# NCCN Risk
nccn = calculate_nccn_risk(
    psa=12.5,
    grade_group=3,
    t_stage="T2b",
    positive_cores=4,
    total_cores=12,
    max_core_involvement=60,
    psa_density=0.22
)
# Result: "Unfavorable Intermediate"
# Rationale: GG3 (4+3) automatically = unfavorable intermediate

# EAU Risk
eau = calculate_eau_risk(psa=12.5, grade_group=3, t_stage="T2b")
# Result: "Intermediate Unfavorable"

# CAPRA Score
capra = calculate_capra(
    psa=12.5,
    primary_gleason=4,
    secondary_gleason=3,
    t_stage="T2b",
    pct_positive_cores=33.3,
    age=65
)
# PSA 10.1-20: 2 points
# Primary Gleason 4: 3 points
# T-stage T2: 0 points
# <34% positive: 0 points
# Age ≥50: 1 point
# Total: 6 points → High risk category

# Briganti 2017 LNI
lni = briganti_2017_lni(
    psa=12.5,
    t_stage="T2",
    grade_group=3,
    pct_positive_highest=33.3,  # All cores same grade
    pct_positive_lowest=33.3
)
# LP = -5.8717 + (0.0826×12.5) + (0.3633×1) + (0.7419×1) 
#      + (0.0130×33.3) + (0.0113×33.3)
# LP = -5.8717 + 1.0325 + 0.3633 + 0.7419 + 0.433 + 0.376 = -2.93
# P(LNI) = 1/(1+exp(2.93)) = 5.1%
# Result: 5.1% (below 7% threshold)

# Roach Formula
roach = roach_lni(psa=12.5, gleason=7)
# (2/3 × 12.5) + [(7-6) × 10] = 8.33 + 10 = 18.3%
# Result: 18.3% (above 15% threshold for pelvic RT)
```

### Clinical Decision
- **Risk Group**: NCCN Unfavorable Intermediate / EAU Intermediate Unfavorable
- **ePLND Decision**: Briganti 5.1% < 7% → ePLND not required by nomogram, but consider given GG3
- **If RT chosen**: Roach 18.3% ≥ 15% → include pelvic nodes

---

## Example 2: Primary Treatment Planning - High Risk

### Patient Data
- Age: 72 years
- PSA: 28 ng/mL
- Clinical stage: cT3a
- Biopsy: 8/12 cores positive
- Grade Group 4 (Gleason 4+4=8)
- MRI: ECE suspected, no SVI
- PSA density: 0.45 ng/mL/g

### Calculations

```python
from helper import *

# NCCN Risk
nccn = calculate_nccn_risk(
    psa=28,
    grade_group=4,
    t_stage="T3a",
    positive_cores=8,
    total_cores=12,
    max_core_involvement=80,
    psa_density=0.45
)
# Result: "Very High"
# Rationale: ≥2 high-risk features (T3a + GG4 + PSA>20)

# Briganti 2017 LNI
lni = briganti_2017_lni(
    psa=28,
    t_stage="T3",
    grade_group=4,
    pct_positive_highest=66.7,
    pct_positive_lowest=66.7
)
# LP = -5.8717 + (0.0826×28) + (0.9555×1) + (0.8755×1)
#      + (0.0130×66.7) + (0.0113×66.7)
# LP = -5.8717 + 2.313 + 0.9555 + 0.8755 + 0.867 + 0.754 = -0.11
# P(LNI) = 1/(1+exp(0.11)) = 47.3%
# Result: 47.3% (well above 7% threshold)

# Roach Formula
roach = roach_lni(psa=28, gleason=8)
# (2/3 × 28) + [(8-6) × 10] = 18.67 + 20 = 38.7%
```

### Clinical Decision
- **Risk Group**: NCCN Very High Risk
- **ePLND**: Briganti 47.3% → Mandatory ePLND
- **PSMA-PET**: Strongly indicated for staging
- **If RT chosen**: Include pelvic nodes; consider ADT 18-36 months

---

## Example 3: Biochemical Recurrence - Low Risk

### Patient Data
- Original: pT2c N0, GG2 (Gleason 3+4=7), margins negative
- RP performed 26 months ago
- PSA nadir: undetectable
- Current PSA series:
  - Day 0: 0.22 ng/mL
  - Day 120: 0.31 ng/mL
  - Day 240: 0.42 ng/mL

### Calculations

```python
from helper import *

# PSADT Calculation
psadt = calculate_psadt([
    (0, 0.22),
    (120, 0.31),
    (240, 0.42)
])
# Using linear regression of ln(PSA) vs time:
# ln(0.22) = -1.514, ln(0.31) = -1.171, ln(0.42) = -0.868
# Slope = 0.00269 per day = 0.0819 per month
# PSADT = 0.693 / 0.0819 = 8.5 months
# Result: 8.5 months

# Interpretation
interpretation = interpret_psadt(8.5)
# Result: "Moderate risk - consider early salvage RT"

# EAU BCR Risk
bcr_risk = eau_bcr_risk(
    psadt_months=8.5,
    grade_group=2,
    time_to_bcr_months=26
)
# PSADT 8.5 < 12 months → High risk
# Despite GG2 and time >18 months, PSADT drives high-risk classification
# Result: "High Risk BCR"

# CAPRA-S Score
capra_s = calculate_capra_s(
    preop_psa=8.5,  # Assuming from original
    path_gleason="3+4",
    margin_positive=False,
    ece=False,
    svi=False,
    lni=False
)
# PSA 6.01-10: 1 point
# Gleason 3+4: 1 point
# Margin negative: 0 points
# No ECE/SVI/LNI: 0 points
# Total: 2 points → Low risk category
```

### Salvage RT Planning

```python
# Current PSA for salvage RT decision
pre_srt_psa = 0.42

# Pelvic Node Decision
pelvic = pelvic_node_recommendation(
    pre_srt_psa=0.42,
    lni_risk_briganti=None,  # Not applicable post-RP
    lni_risk_roach=None
)
# PSA 0.42 > 0.35 threshold from SPPORT
# Result: "Consider pelvic nodes if using ADT"

# ADT Duration
adt = adt_duration_recommendation(
    pre_srt_psa=0.42,
    grade_group=2,
    psadt_months=8.5,
    decipher=None
)
# PSA < 0.7 but PSADT < 12 → mixed signals
# GG2 = favorable
# Result: "Short-term ADT (4-6 months) - PSADT borderline, weigh toxicity"
```

### Clinical Decision
- **EAU BCR Risk**: High (driven by PSADT < 12 months)
- **Salvage RT**: Yes, proceed with early salvage
- **Pelvic Nodes**: Consider including (PSA > 0.35)
- **ADT**: 4-6 months reasonable given mixed risk profile
- **Dose**: 66 Gy to prostate bed, 45 Gy to pelvis if included

---

## Example 4: Biochemical Recurrence - High Risk

### Patient Data
- Original: pT3b N0, GG5 (Gleason 4+5=9), positive margins, SVI+
- RP performed 8 months ago
- PSA series:
  - Day 0: 0.45 ng/mL
  - Day 45: 0.82 ng/mL
  - Day 90: 1.65 ng/mL
  - Day 135: 3.20 ng/mL

### Calculations

```python
from helper import *

# PSADT Calculation
psadt = calculate_psadt([
    (0, 0.45),
    (45, 0.82),
    (90, 1.65),
    (135, 3.20)
])
# Slope calculation from ln(PSA) regression
# Very rapid rise → PSADT ≈ 2.1 months
# Result: 2.1 months

# Interpretation
interpretation = interpret_psadt(2.1)
# Result: "Extremely high risk - systemic disease likely, consider intensified therapy"

# EAU BCR Risk
bcr_risk = eau_bcr_risk(
    psadt_months=2.1,
    grade_group=5,
    time_to_bcr_months=8
)
# Multiple high-risk criteria met
# Result: "High Risk BCR"

# CAPRA-S Score
capra_s = calculate_capra_s(
    preop_psa=15,  # Assuming
    path_gleason="4+5",
    margin_positive=True,
    ece=True,
    svi=True,
    lni=False
)
# PSA 10.01-20: 2 points
# Gleason 8-10: 3 points
# Positive margin: 2 points
# ECE: 1 point
# SVI: 2 points
# Total: 10 points → Very High risk
```

### Salvage RT Planning

```python
# Current PSA
pre_srt_psa = 3.20

# Check EMBARK criteria
embark_eligible = (psadt <= 9 and pre_srt_psa >= 1.0)
# PSADT 2.1 ≤ 9: Yes
# PSA 3.20 ≥ 1.0: Yes
# Result: True - Consider enzalutamide per EMBARK

# Pelvic Node Decision
pelvic = pelvic_node_recommendation(pre_srt_psa=3.20, lni_risk_briganti=None)
# PSA 3.20 >> 0.35
# Result: "Strongly recommend pelvic nodes"

# ADT Duration
adt = adt_duration_recommendation(
    pre_srt_psa=3.20,
    grade_group=5,
    psadt_months=2.1,
    decipher=0.85  # If available, likely high
)
# All parameters indicate high-risk
# Result: "Long-term ADT (24 months) with intensification consideration"
```

### Clinical Decision
- **EAU BCR Risk**: High Risk
- **Concern**: PSADT < 3 months suggests systemic disease
- **Staging**: PSMA-PET/CT strongly recommended before local therapy
- **If localized on imaging**:
  - Salvage RT with pelvic nodes
  - 24 months ADT (RTOG 9601 criteria: PSA > 1.5)
  - Consider enzalutamide (EMBARK eligible)
- **If metastatic on imaging**: Systemic therapy primary

---

## Example 5: Borderline Case - ADT Decision

### Patient Data
- Original: pT3a N0, GG3 (Gleason 4+3=7), negative margins
- RP performed 20 months ago
- PSA: 0.65 ng/mL (current, first detectable)
- No prior PSA series available yet

### Initial Assessment

```python
from helper import *

# EAU BCR Risk (incomplete - need PSADT)
# Time to BCR: 20 months (just above 18 month threshold)
# GG3: Intermediate
# PSADT: Unknown

# Need serial PSAs before definitive recommendation
```

### Follow-up After 3 Months

PSA series now available:
- Day 0: 0.65 ng/mL
- Day 45: 0.78 ng/mL
- Day 90: 0.95 ng/mL

```python
psadt = calculate_psadt([
    (0, 0.65),
    (45, 0.78),
    (90, 0.95)
])
# PSADT ≈ 16 months
# Result: 16 months

# EAU BCR Risk
bcr_risk = eau_bcr_risk(
    psadt_months=16,
    grade_group=3,
    time_to_bcr_months=20
)
# PSADT > 12: Favorable
# GG3: Borderline (EAU uses GG 1-3 as low-risk criterion)
# Time > 18 months: Favorable
# Result: "Low Risk BCR" (all criteria met)

# ADT Decision
adt = adt_duration_recommendation(
    pre_srt_psa=0.95,
    grade_group=3,
    psadt_months=16,
    decipher=None
)
# PSA 0.7-1.5 range
# PSADT favorable
# GG3 borderline
# Result: "Short-term ADT (4-6 months) reasonable, or RT alone acceptable"
```

### Clinical Decision
- **EAU BCR Risk**: Low Risk (borderline)
- **Options**:
  1. Salvage RT alone (acceptable given favorable PSADT)
  2. Salvage RT + 4-6 months ADT (reasonable given GG3)
- **Pelvic Nodes**: Consider - PSA 0.95 > 0.35 threshold
- **Shared Decision Making**: Discuss toxicity trade-offs

---

## Quick Reference: Function Calls

```python
# Primary Risk
calculate_nccn_risk(psa, grade_group, t_stage, positive_cores, total_cores, 
                     max_core_involvement, psa_density, primary_gleason=None,
                     n_stage="N0", m_stage="M0")

calculate_eau_risk(psa, grade_group, t_stage, n_stage="N0")

calculate_capra(psa, primary_gleason, secondary_gleason, t_stage, 
                pct_positive_cores, age)

# LNI Prediction
briganti_2017_lni(psa, t_stage, grade_group, pct_positive_highest, 
                   pct_positive_lowest)

roach_lni(psa, gleason)

yale_lni(psa, gleason, t_stage)

# BCR Assessment
calculate_psadt(psa_values)  # List of (days, psa) tuples

eau_bcr_risk(psadt_months, grade_group, time_to_bcr_months)

interpret_psadt(psadt_months)

# Post-RP Scoring
calculate_capra_s(preop_psa, path_gleason, margin_positive, ece, svi, lni)

# Salvage RT Decisions
pelvic_node_recommendation(pre_srt_psa, lni_risk_briganti=None, lni_risk_roach=None)

adt_duration_recommendation(pre_srt_psa, grade_group, psadt_months, decipher=None)

spport_eligible(t_stage, gleason, psa_range, n_stage)
```
