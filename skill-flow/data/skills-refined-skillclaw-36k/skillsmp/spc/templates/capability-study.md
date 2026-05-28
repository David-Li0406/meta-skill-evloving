# Process Capability Study Template

## Study Information

| Field | Value |
|-------|-------|
| **Study Number** | CAP-[YYYY]-[SEQ] |
| **Date** | |
| **Conducted By** | |
| **Part Number** | |
| **Part Name** | |
| **Characteristic** | |
| **Specification** | |
| **Tolerance** | |
| **Cpk Requirement** | |

---

## Study Parameters

| Parameter | Value |
|-----------|-------|
| Sample Size | |
| Collection Method | |
| Collection Period | |
| Machine/Equipment | |
| Operator(s) | |
| Material Lot | |

---

## Pre-Study Verification

| Item | Status | Notes |
|------|--------|-------|
| MSA completed and acceptable | [ ] Yes [ ] No | %GR&R: ____ ndc: ____ |
| Gage calibrated | [ ] Yes [ ] No | Due date: |
| Process representative | [ ] Yes [ ] No | |
| Normal production conditions | [ ] Yes [ ] No | |

---

## Data Collection

### Raw Data

| # | Value | # | Value | # | Value | # | Value | # | Value |
|---|-------|---|-------|---|-------|---|-------|---|-------|
| 1 | | 11 | | 21 | | 31 | | 41 | |
| 2 | | 12 | | 22 | | 32 | | 42 | |
| 3 | | 13 | | 23 | | 33 | | 43 | |
| 4 | | 14 | | 24 | | 34 | | 44 | |
| 5 | | 15 | | 25 | | 35 | | 45 | |
| 6 | | 16 | | 26 | | 36 | | 46 | |
| 7 | | 17 | | 27 | | 37 | | 47 | |
| 8 | | 18 | | 28 | | 38 | | 48 | |
| 9 | | 19 | | 29 | | 39 | | 49 | |
| 10 | | 20 | | 30 | | 40 | | 50 | |

---

## Descriptive Statistics

| Statistic | Value |
|-----------|-------|
| Sample Size (n) | |
| Mean (X̄) | |
| Standard Deviation (s) | |
| Minimum | |
| Maximum | |
| Range | |

---

## Normality Assessment

### Histogram

[Attach histogram or describe shape]

Shape: [ ] Normal  [ ] Skewed Left  [ ] Skewed Right  [ ] Bimodal  [ ] Other

### Normality Test

| Test | Statistic | p-value | Normal? |
|------|-----------|---------|---------|
| Anderson-Darling | | | [ ] Yes [ ] No |

**Conclusion:** [ ] Data appears normal  [ ] Data is non-normal (see alternative analysis)

---

## Statistical Control Assessment

### Control Chart Type Used

[ ] X-bar/R  [ ] I-MR  [ ] Other: ___________

### Control Limits (for I-MR)

| Chart | LCL | CL | UCL |
|-------|-----|----|----|
| I | | | |
| MR | | | |

### Control Chart Assessment

| Criterion | Result |
|-----------|--------|
| Points outside limits | |
| Runs (7+ same side) | |
| Trends (6+ consecutive up/down) | |

**Process in Statistical Control?** [ ] Yes  [ ] No

If No, describe issues: _______________

---

## Capability Calculations

### Specification Information

| | Value |
|---|-------|
| USL | |
| LSL | |
| Target | |
| Tolerance (USL - LSL) | |

### Short-Term Capability (Cp, Cpk)

**σ̂ (within) calculation method:** [ ] R̄/d₂  [ ] S̄/c₄  [ ] Pooled

σ̂ = _______

```
Cp = (USL - LSL) / 6σ̂
Cp = (_____ - _____) / (6 × _____)
Cp = _____

Cpu = (USL - X̄) / 3σ̂
Cpu = (_____ - _____) / (3 × _____)
Cpu = _____

Cpl = (X̄ - LSL) / 3σ̂
Cpl = (_____ - _____) / (3 × _____)
Cpl = _____

Cpk = Min(Cpu, Cpl)
Cpk = _____
```

### Long-Term Performance (Pp, Ppk)

Using sample standard deviation (s) = _______

```
Pp = (USL - LSL) / 6s
Pp = (_____ - _____) / (6 × _____)
Pp = _____

Ppu = (USL - X̄) / 3s
Ppu = (_____ - _____) / (3 × _____)
Ppu = _____

Ppl = (X̄ - LSL) / 3s
Ppl = (_____ - _____) / (3 × _____)
Ppl = _____

Ppk = Min(Ppu, Ppl)
Ppk = _____
```

---

## Results Summary

| Index | Value | Requirement | Status |
|-------|-------|-------------|--------|
| Cp | | - | - |
| **Cpk** | | ≥ | [ ] PASS  [ ] FAIL |
| Pp | | - | - |
| **Ppk** | | ≥ | [ ] PASS  [ ] FAIL |

### Estimated PPM Defective

```
Z_upper = (USL - X̄) / σ = _____
Z_lower = (X̄ - LSL) / σ = _____

PPM_upper = _____ (from Z-table or calculator)
PPM_lower = _____ (from Z-table or calculator)
PPM_total = _____
```

---

## Process Centering Analysis

| Measure | Value |
|---------|-------|
| Target | |
| Mean | |
| Off-Center Amount | |
| Direction | [ ] Above Target  [ ] Below Target |

**Centering Assessment:**
- [ ] Well-centered (within 10% of tolerance from target)
- [ ] Slightly off-center (10-25% of tolerance)
- [ ] Significantly off-center (>25% of tolerance)

**If Cp > Cpk significantly:** Process could be improved by centering.

---

## Conclusions

### Capability Assessment

- [ ] **CAPABLE** - Cpk ≥ requirement, process acceptable
- [ ] **MARGINALLY CAPABLE** - Cpk close to requirement, monitor closely
- [ ] **NOT CAPABLE** - Cpk < requirement, improvement needed

### Key Findings

1.
2.
3.

### Recommendations

1.
2.
3.

---

## Action Plan (if not capable)

| Action | Responsible | Due Date | Status |
|--------|-------------|----------|--------|
| | | | |
| | | | |
| | | | |

---

## Follow-Up Study Required?

- [ ] No - Process is capable
- [ ] Yes - After improvement actions
- [ ] Scheduled - Next study date: __________

---

## Attachments

- [ ] Histogram
- [ ] Control chart
- [ ] Normal probability plot
- [ ] Raw data (electronic)
- [ ] Software analysis output

---

## Approvals

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Study Conductor | | | |
| Quality Engineer | | | |
| Process Owner | | | |
| Customer (if required) | | | |
