---
description: 'Clinical decision support for prostate cancer: risk stratification (NCCN/EAU/CAPRA),
  LNI prediction (Briganti/Roach), PSADT/BCR assessment, salvage RT planning, and
  Polish NFZ drug programmes (B.56 for apalutamide/darolutamide/enzalutamide/olaparib/niraparib/talazoparib,
  C.87 for abiraterone). Covers mHSPC, nmCRPC, mCRPC eligibility, qualification criteria,
  dosing, and monitoring.'
name: prostate-cancer-calculator
routing_description: Clinical decision support for prostate cancer risk stratification,
  biochemical recurrence assessment, and Polish NFZ drug programme qualification across
  NCCN/EAU/CAPRA risk models and systemic therapy recommendations.
routing_keywords:
- prostate cancer
- psa
- gleason score
- grade group
- nccn risk
- eau risk
- capra score
- lni prediction
- biochemical recurrence
- psadt
- salvage radiation
- apalutamide
- darolutamide
- enzalutamide
- abiraterone
- mcrpc
- mhspc
- nmcrpc
- polish nfz
- briganti nomogram
- roach nomogram
- adt duration
---

# Prostate Cancer Clinical Calculator

## Overview

Comprehensive clinical decision support for prostate cancer across:

1. **Risk Stratification**: NCCN/EAU risk groups, LNI prediction nomograms
2. **Biochemical Recurrence**: EAU BCR risk, PSADT, salvage RT decisions
3. **Polish NFZ Drug Programmes**:
   - **B.56**: Apalutamide, Darolutamide, Enzalutamide, Olaparib, Niraparib+Abiraterone, Talazoparib
   - **C.87**: Abiraterone (C.87.a/C.87.b)

## Quick Start

Import and use the helper script:

```python
from helper import *

# Primary risk stratification
nccn = calculate_nccn_risk(psa=12, grade_group=3, t_stage="T2b", 
                            positive_cores=4, total_cores=12, psa_density=0.18)
eau = calculate_eau_risk(psa=12, grade_group=3, t_stage="T2b")

# LNI prediction
briganti = briganti_2017_lni(psa=15, t_stage="T2", grade_group=3, 
                              pct_positive_highest=50, pct_positive_lowest=25)
roach = roach_lni(psa=15, gleason=7)

# BCR assessment
psadt = calculate_psadt([(0, 0.15), (90, 0.35), (180, 0.72)])  # (days, PSA)
eau_bcr = eau_bcr_risk(psadt_months=8, grade_group=4, time_to_bcr_months=12)

# Salvage RT recommendations
pelvic_rec = pelvic_node_recommendation(pre_srt_psa=0.5, lni_risk=18)
adt_rec = adt_duration_recommendation(pre_srt_psa=0.8, grade_group=3, psadt_months=10)
```

## Reference Files

| File | Contents | When to Load |
|------|----------|--------------|
| [reference.md](reference.md) | Complete formulas, coefficients, thresholds | Building custom implementations, validating calculations |
| [examples.md](examples.md) | Clinical case examples with full calculations | Understanding clinical workflow, teaching |
| [scripts/helper.py](scripts/helper.py) | Python implementation | Execute directly - no need to load into context |
| [references/qualification-criteria.md](references/qualification-criteria.md) | B.56 drug qualification criteria | Drug eligibility assessment |
| [references/diagnostics.md](references/diagnostics.md) | Required tests by drug/indication | Qualification workup |
| [references/monitoring.md](references/monitoring.md) | Safety and efficacy monitoring | Ongoing treatment |
| [references/exclusion-criteria.md](references/exclusion-criteria.md) | Progression/exclusion criteria | Treatment discontinuation |

## Available Functions

### Risk Stratification

| Function | Description |
|----------|-------------|
| `calculate_nccn_risk()` | 8-tier NCCN risk classification |
| `calculate_eau_risk()` | EAU low/intermediate/high risk |
| `calculate_capra()` | CAPRA score (0-10) |
| `calculate_capra_s()` | CAPRA-S post-prostatectomy score (0-12) |

### LNI Prediction

| Function | Description |
|----------|-------------|
| `briganti_2017_lni()` | Briganti 2017 nomogram with published coefficients |
| `briganti_2012_lni()` | Briganti 2012 simplified version |
| `roach_lni()` | Roach formula: (2/3 × PSA) + [(GS-6) × 10] |
| `yale_lni()` | Yale formula with T-stage adjustment |
| `mskcc_lni()` | MSKCC nomogram approximation |

### BCR Assessment

| Function | Description |
|----------|-------------|
| `calculate_psadt()` | PSA doubling time from serial measurements |
| `eau_bcr_risk()` | EAU low/high risk BCR classification |
| `interpret_psadt()` | Clinical interpretation of PSADT value |

### Salvage RT Decisions

| Function | Description |
|----------|-------------|
| `pelvic_node_recommendation()` | Whether to include pelvic nodes (SPPORT-based) |
| `adt_duration_recommendation()` | ADT duration: none/short/long (trial-based) |
| `spport_eligible()` | RTOG 0534/SPPORT eligibility check |

### Polish NFZ Drug Programmes

| Function | Description |
|----------|-------------|
| `check_b56_eligibility()` | B.56 programme - check eligibility for all drugs |
| `check_apalutamide_eligibility()` | Apalutamide (mHSPC, nmCRPC) |
| `check_darolutamide_eligibility()` | Darolutamide ± docetaxel (mHSPC, nmCRPC) |
| `check_enzalutamide_eligibility()` | Enzalutamide (mHSPC, nmCRPC, mCRPC) |
| `check_olaparib_eligibility()` | Olaparib (mCRPC, requires BRCA) |
| `check_niraparib_abiraterone_eligibility()` | Niraparib+Abiraterone (mCRPC, requires BRCA) |
| `check_talazoparib_enzalutamide_eligibility()` | Talazoparib+Enzalutamide (mCRPC, requires HRR) |
| `check_abiraterone_eligibility_poland()` | C.87 programme - Abiraterone eligibility |
| `format_b56_eligibility_pl()` | Format B.56 results in Polish |
| `format_abiraterone_eligibility_pl()` | Format C.87 results in Polish |

## Key Thresholds

| Parameter | Threshold | Clinical Significance |
|-----------|-----------|----------------------|
| LNI risk (ePLND) | ≥7% | Extended pelvic lymph node dissection recommended |
| LNI risk (pelvic RT) | ≥15% | Consider pelvic nodal RT (Roach) |
| PSADT | <10-12 mo | EAU high-risk BCR |
| PSADT | <9 mo | EMBARK trial criteria (enzalutamide eligible) |
| Pre-SRT PSA | >0.35 ng/mL | Greatest benefit from pelvic nodal RT (SPPORT) |
| Pre-SRT PSA | ≥0.7 ng/mL | Consider long-term ADT (RTOG 9601) |

## Clinical Decision Algorithm

```
PRIMARY TREATMENT
├── Calculate NCCN + EAU risk group
├── If intermediate/high risk → Calculate LNI risk
│   ├── Briganti ≥7% → ePLND recommended
│   └── Roach ≥15% → Pelvic RT if definitive RT chosen
└── Document CAPRA score for prognosis

BIOCHEMICAL RECURRENCE (post-RP)
├── Calculate PSADT (≥3 values, ≥3 months)
├── Classify EAU BCR risk (low vs high)
├── If high-risk BCR:
│   ├── Pre-SRT PSA >0.35 → Add pelvic nodes to RT
│   ├── Pre-SRT PSA ≥0.7 → Consider long-term ADT (24 mo)
│   └── PSADT ≤9 mo + PSA ≥1 → Consider enzalutamide (EMBARK)
└── If low-risk BCR → Observation may be appropriate
```

## Important Notes

- Briganti 2017 uses published beta coefficients; other Briganti versions require lookup tables
- Roach formula overestimates contemporary LNI rates but remains useful for RT field decisions
- PSADT calculation requires ≥3 PSA values over ≥3 months, all rising, same assay
- ADT recommendations integrate GETUG-AFU 16, RTOG 9601, and RADICALS-HD evidence
- Always document genomic classifier (Decipher) when available—modifies ADT recommendations

---

## Polish NFZ Programme B.56 - Drug Selection Guide

### Drug Availability by Disease Stage

| Stage | Available Drugs |
|-------|-----------------|
| **mHSPC** | Apalutamide, Darolutamide (+docetaxel), Enzalutamide |
| **nmCRPC** | Apalutamide, Darolutamide, Enzalutamide |
| **mCRPC** | Enzalutamide, Olaparib*, Niraparib+Abi*, Talazoparib+Enza* |

*Requires BRCA1/2 or HRR gene mutations

### Key Programme Rules

1. **ONE new-generation hormonal therapy line** allowed per patient
2. **ONE PARP inhibitor line** allowed per patient
3. One-time use of non-steroidal antiandrogen AND PARP inhibitor permitted
4. All patients must maintain castration (LHRH agonist/antagonist or orchiectomy)

### Performance Status Requirements

| ECOG 0-1 Required | ECOG 0-2 Allowed |
|-------------------|------------------|
| Apalutamide (nmCRPC) | Apalutamide (mHSPC) |
| Darolutamide (nmCRPC) | Darolutamide (mHSPC) |
| Enzalutamide (nmCRPC, mCRPC pre-chemo) | Enzalutamide (mHSPC, mCRPC post-chemo) |
| | Olaparib, Niraparib+Abi, Talazoparib+Enza |

### Dosing Quick Reference

| Drug | Daily Dose | Notes |
|------|-----------|-------|
| Apalutamide | 240 mg | Once daily |
| Darolutamide | 1200 mg | 600 mg BID with food |
| Enzalutamide | 160 mg | Once daily |
| Olaparib | 600 mg | 300 mg BID |
| Niraparib+Abi | 200 mg + 1000 mg | Combination tablet + prednisone 10 mg |
| Talazoparib+Enza | 0.5 mg + 160 mg | Both once daily |

### Common Exclusion Criteria

- Prior abiraterone (except specific exceptions for Niraparib+Abi)
- Prior novel hormonal agent (for PARP inhibitor combinations)
- Seizure history (Apalutamide, Enzalutamide)
- CrCl ≤30 mL/min (PARP inhibitors)

### Decision Tree

```
PATIENT PRESENTS
├── mHSPC?
│   ├── Can receive docetaxel? → Darolutamide + Docetaxel
│   └── Cannot/prefers not → Apalutamide OR Enzalutamide
│
├── nmCRPC? (M0, PSADT ≤10 mo, testosterone ≤50 ng/dL)
│   └── Apalutamide / Darolutamide / Enzalutamide
│
└── mCRPC?
    ├── BRCA1/2 mutation?
    │   ├── Progressed on hormonal therapy → Olaparib
    │   └── 1st line, no chemo indication → Niraparib+Abiraterone
    ├── HRR mutation (BRCA2, ATM, CDK12, etc.)?
    │   └── 1st line, no chemo indication → Talazoparib+Enzalutamide
    └── No targetable mutation → Enzalutamide
```

---

## Polish NFZ Programme C.87 - Abiraterone

### Attachment C.87.a (High-intensity settings)

1. **mHSPC high-risk** (≥2 of: Gleason ≥8, ≥3 bone mets, visceral mets)
2. **mCRPC pre-chemotherapy** (asymptomatic/oligosymptomatic)
3. **mCRPC post-docetaxel** (after chemotherapy failure)

### Attachment C.87.b (Standard settings)

1. **mCSPC** (not meeting C.87.a high-risk criteria)
2. **nmCRPC** (PSADT ≤10 months)
3. **Adjuvant post-RT** (high-risk: N+ or ≥2 of T3-4, Gleason 8-10, PSA ≥40)
