---
name: b56-prostate-cancer-programme
description: "Polish NFZ drug programme B.56 for prostate cancer (ICD-10 C61). Use when helping clinicians with patient qualification, drug selection, dosing, monitoring, or follow-up for mHSPC, nmCRPC, or mCRPC treatment with apalutamide, darolutamide, enzalutamide, olaparib, niraparib+abiraterone, or talazoparib. Covers eligibility criteria, required diagnostics, treatment duration, and exclusion criteria."
---

# B.56 Programme - Prostate Cancer Treatment (ICD-10: C61)

## Quick Reference: Drug Selection by Disease Stage

| Stage | Available Treatments |
|-------|---------------------|
| **mHSPC** | Apalutamide, Darolutamide (+docetaxel), Enzalutamide |
| **nmCRPC** | Apalutamide, Darolutamide, Enzalutamide |
| **mCRPC** | Enzalutamide, Olaparib*, Niraparib+Abiraterone*, Talazoparib+Enzalutamide* |

*Requires BRCA1/2 or HRR gene mutations

## Programme Rules

- **ONE new-generation hormonal therapy line** allowed
- **ONE PARP inhibitor line** allowed
- One-time use of non-steroidal antiandrogen AND PARP inhibitor permitted

## General Qualification Criteria (All Drugs)

All patients must meet:
1. Histologically confirmed prostate adenocarcinoma
2. Age ≥18 years
3. Performance status per drug-specific requirements (see below)
4. Adequate organ function per SmPC
5. No contraindications per SmPC
6. No uncontrolled other malignancies
7. No neuroendocrine/small-cell/ductal prostate cancer

### Performance Status Requirements

| Drug/Setting | ECOG |
|--------------|------|
| Apalutamide (nmCRPC), Darolutamide (nmCRPC), Enzalutamide (nmCRPC, mCRPC pre-docetaxel) | 0-1 |
| Apalutamide (mHSPC), Darolutamide (mHSPC), Enzalutamide (mHSPC, mCRPC post-docetaxel), Olaparib, Niraparib+Abiraterone, Talazoparib+Enzalutamide | 0-2 |

## Drug Dosing

| Drug | Dose | Notes |
|------|------|-------|
| **Apalutamide** | 240 mg/day | With or without food |
| **Darolutamide** | 600 mg BID (1200 mg/day) | With food. In mHSPC: start with docetaxel |
| **Enzalutamide** | 160 mg/day | With or without food |
| **Olaparib** | 300 mg BID (600 mg/day) | With or without food, monotherapy |
| **Niraparib+Abiraterone** | 200 mg nira + 1000 mg abi daily + prednisone 10 mg | MUST use combination tablet |
| **Talazoparib** | 0.5 mg/day + enzalutamide 160 mg/day | With or without food |

## Mandatory Castration Maintenance

All patients (except post-orchiectomy) must maintain androgen suppression with LHRH agonists/antagonists.

## Decision Trees

### For mHSPC Patients
```
mHSPC confirmed?
├─ Can receive docetaxel?
│   ├─ Yes → Darolutamide + Docetaxel OR Apalutamide/Enzalutamide
│   └─ No (documented reason) → Apalutamide OR Enzalutamide
├─ Prior ADT ≤6 months on metastatic disease? → Eligible
├─ Prior abiraterone? → NOT eligible
└─ Prior radical treatment + adjuvant HT ≤3 years (finished ≥1 year ago)? → Eligible
```

### For nmCRPC Patients
```
nmCRPC criteria:
├─ Testosterone ≤50 ng/dL (≤1.7 nmol/L)?
├─ PSA progression (3 rises, ≥1 week apart, 2×≥50% from nadir, PSA >2)?
├─ No distant metastases (M0, only N1 <2cm below aortic bifurcation)?
├─ PSA doubling time ≤10 months?
└─ No prior abiraterone?
All YES → Eligible for Apalutamide/Darolutamide/Enzalutamide

Note: Apalutamide/Enzalutamide - exclude if seizure history or risk factors
```

### For mCRPC Patients
```
mCRPC criteria:
├─ Testosterone ≤50 ng/dL (≤1.7 nmol/L)?
├─ PSA progression OR radiological progression?
│
├─ BRCA1/2 mutation present?
│   ├─ Yes + prior new-gen hormonal therapy progression → Olaparib eligible
│   └─ Yes + no chemo indication in 1st line mCRPC + no prior abiraterone → Niraparib+Abi eligible
│
├─ HRR mutation (BRCA2, ATM, CDK12, CHEK2, BRCA1, PALB2, RAD51C)?
│   └─ Yes + no chemo indication + no prior abiraterone → Talazoparib+Enzalutamide eligible
│
└─ No targetable mutation?
    └─ Enzalutamide (pre- or post-docetaxel)
```

## Required Diagnostics

See [references/diagnostics.md](references/diagnostics.md) for complete lists.

### At Qualification
- Histology confirmation
- CBC with differential
- PSA, testosterone
- Creatinine (+ eGFR for olaparib/talazoparib)
- Bilirubin, ALT, AST
- Bone scan
- Imaging (CT/MRI) per clinical indication
- CT abdomen/pelvis (for nmCRPC drugs)
- Chest imaging (for nmCRPC drugs)

**Imaging must be ≤3 months before enrolment and allow RECIST/PCWG evaluation.**

## Monitoring Schedule

See [references/monitoring.md](references/monitoring.md) for complete protocol.

### Safety Monitoring
- CBC: every 2-3 months (monthly for PARP inhibitors)
- Creatinine + eGFR: monthly for olaparib/niraparib+abi/talazoparib
- For darolutamide+docetaxel phase: labs before each docetaxel dose

### Efficacy Monitoring
- PSA: minimum every 3 months
- Imaging (per baseline modality): minimum every 6 months
- Bone scan: minimum every 6 months

## Exclusion Criteria

See [references/exclusion-criteria.md](references/exclusion-criteria.md) for details.

### Progression Definitions
**PSA progression**: 3 consecutive rises (≥1 week apart), 2 rises ≥50% above nadir, PSA >2 ng/mL
- Exception: continue if documented clinical benefit and no next-line option

**Radiological progression**: per RECIST (soft tissue) or PCWG (bone)

### Other Exclusion Triggers
- ECOG deterioration (drug-specific thresholds)
- Hypersensitivity to drug/excipients
- Unmanageable toxicity per SmPC/physician judgment
- Conditions precluding treatment
- Significant QoL deterioration
- Non-compliance with follow-up

## Special Populations

### Renal Impairment (Olaparib, Talazoparib)
- CrCl 31-50 mL/min: dose reduction per SmPC
- CrCl ≤30 mL/min: **contraindicated**

### Patients Continuing from Other Funding
Patients previously on programme drugs via other funding (except ongoing clinical trials) may qualify if they met criteria at treatment initiation.
