# Gage R&R Study Template

## Study Information

| Field | Value |
|-------|-------|
| **Study Number** | GRR-[YYYY]-[SEQ] |
| **Date** | |
| **Conducted By** | |
| **Gage ID** | |
| **Gage Description** | |
| **Gage Resolution** | |
| **Characteristic** | |
| **Specification** | |
| **Tolerance** | |
| **Part Number** | |
| **Part Name** | |

---

## Study Parameters

| Parameter | Value |
|-----------|-------|
| Number of Operators | |
| Number of Parts | |
| Number of Trials | |
| Total Measurements | |

### Operators

| Operator | Name | Training Verified? |
|----------|------|-------------------|
| A | | [ ] Yes |
| B | | [ ] Yes |
| C | | [ ] Yes |

---

## Measurement Data

### Part Numbering Key (Keep Hidden from Operators)

| Part # | Identifying Mark |
|--------|------------------|
| 1 | |
| 2 | |
| 3 | |
| 4 | |
| 5 | |
| 6 | |
| 7 | |
| 8 | |
| 9 | |
| 10 | |

### Measurement Records

| Part | Op A T1 | Op A T2 | Op A T3 | Op B T1 | Op B T2 | Op B T3 | Op C T1 | Op C T2 | Op C T3 |
|------|---------|---------|---------|---------|---------|---------|---------|---------|---------|
| 1 | | | | | | | | | |
| 2 | | | | | | | | | |
| 3 | | | | | | | | | |
| 4 | | | | | | | | | |
| 5 | | | | | | | | | |
| 6 | | | | | | | | | |
| 7 | | | | | | | | | |
| 8 | | | | | | | | | |
| 9 | | | | | | | | | |
| 10 | | | | | | | | | |

---

## Calculations

### Range Calculations (Per Part, Per Operator)

| Part | Op A Range | Op B Range | Op C Range |
|------|------------|------------|------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| 6 | | | |
| 7 | | | |
| 8 | | | |
| 9 | | | |
| 10 | | | |
| **Average (R̄)** | | | |

**Overall R̄** = ________

### Operator Averages

| Operator | Average |
|----------|---------|
| A (X̄_A) | |
| B (X̄_B) | |
| C (X̄_C) | |
| **X̄_diff** | |

### Part Averages

| Part | Average |
|------|---------|
| 1 | |
| 2 | |
| 3 | |
| 4 | |
| 5 | |
| 6 | |
| 7 | |
| 8 | |
| 9 | |
| 10 | |
| **R_p** | |

---

## Variance Component Calculations

### Constants Used

| Parameter | Value | Constant | Value |
|-----------|-------|----------|-------|
| Trials | | K₁ | |
| Operators | | K₂ | |
| Parts | | K₃ | |

*K₁: 2 trials=4.56, 3 trials=3.05*
*K₂: 2 operators=3.65, 3 operators=2.70*
*K₃: 10 parts=1.62*

### Repeatability (Equipment Variation - EV)

```
EV = R̄ × K₁ = _______ × _______ = _______
```

### Reproducibility (Appraiser Variation - AV)

```
AV = √[(X̄_diff × K₂)² - (EV²/(n×r))]
AV = √[(___ × ___)² - (___²/(___ × ___))]
AV = _______
```
*(If value under radical is negative, AV = 0)*

### Gage R&R

```
GR&R = √(EV² + AV²)
GR&R = √(___² + ___²)
GR&R = _______
```

### Part Variation (PV)

```
PV = R_p × K₃
PV = _______ × _______
PV = _______
```

### Total Variation (TV)

```
TV = √(GR&R² + PV²)
TV = √(___² + ___²)
TV = _______
```

---

## Results Summary

### Percentage Analysis

| Component | Value | Formula | % of Total |
|-----------|-------|---------|------------|
| Repeatability (EV) | | (EV/TV)×100 | % |
| Reproducibility (AV) | | (AV/TV)×100 | % |
| **Gage R&R** | | (GR&R/TV)×100 | **%** |
| Part Variation (PV) | | (PV/TV)×100 | % |
| Total Variation (TV) | | | 100% |

### Number of Distinct Categories (ndc)

```
ndc = 1.41 × (PV/GR&R)
ndc = 1.41 × (___/___)
ndc = _______
```

---

## Acceptance Criteria

| Metric | Result | Criteria | Status |
|--------|--------|----------|--------|
| %GR&R | % | <10%: Acceptable, 10-30%: Marginal, >30%: Unacceptable | |
| ndc | | ≥5: Acceptable, 3-4: Marginal, <3: Unacceptable | |

---

## Interpretation

### %GR&R Assessment

- [ ] **<10%** - Measurement system is acceptable
- [ ] **10-30%** - Measurement system is marginally acceptable
- [ ] **>30%** - Measurement system is unacceptable

### ndc Assessment

- [ ] **≥5** - Measurement system can adequately distinguish between parts
- [ ] **3-4** - Measurement system has limited discrimination
- [ ] **<3** - Measurement system cannot adequately distinguish parts

### Dominant Variation Source

- [ ] Repeatability dominant - Focus on gage condition, resolution, technique
- [ ] Reproducibility dominant - Focus on operator training, method standardization
- [ ] Part variation dominant - Measurement system is good relative to process

---

## Overall Conclusion

- [ ] **ACCEPTABLE** - Measurement system approved for use
- [ ] **CONDITIONALLY ACCEPTABLE** - Approved with customer concurrence, improvement plan required
- [ ] **UNACCEPTABLE** - Measurement system not approved, improvement required

---

## Actions Required (if applicable)

| Action | Responsible | Due Date | Status |
|--------|-------------|----------|--------|
| | | | |
| | | | |
| | | | |

---

## Follow-up Study Required?

- [ ] No - Measurement system acceptable
- [ ] Yes - After improvement actions
- [ ] Scheduled - Next study date: __________

---

## Approvals

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Study Conductor | | | |
| Quality Engineer | | | |
| Process Owner | | | |

---

## Attachments

- [ ] Raw data (if electronic)
- [ ] Software analysis output
- [ ] Control charts
- [ ] Previous study results (if re-study)
