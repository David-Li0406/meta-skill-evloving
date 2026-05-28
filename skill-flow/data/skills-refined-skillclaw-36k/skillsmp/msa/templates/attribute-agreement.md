# Attribute Agreement Analysis Template

## Study Information

| Field | Value |
|-------|-------|
| **Study Number** | AAA-[YYYY]-[SEQ] |
| **Date** | |
| **Conducted By** | |
| **Inspection Method** | |
| **Characteristic** | |
| **Acceptance Criteria** | |
| **Part Number** | |
| **Part Name** | |

---

## Study Parameters

| Parameter | Value |
|-----------|-------|
| Number of Appraisers | |
| Number of Samples | |
| Number of Trials | |
| Total Decisions | |

### Appraisers

| Appraiser | Name | Training Verified? |
|-----------|------|-------------------|
| A | | [ ] Yes |
| B | | [ ] Yes |
| C | | [ ] Yes |

### Reference Standard

| | Description |
|---|---|
| Expert/Referee | |
| Method | |
| Reference classification completed? | [ ] Yes |

---

## Sample Selection

| Sample # | Description | Reference Decision |
|----------|-------------|-------------------|
| 1 | | Good / Bad |
| 2 | | Good / Bad |
| 3 | | Good / Bad |
| 4 | | Good / Bad |
| 5 | | Good / Bad |
| 6 | | Good / Bad |
| 7 | | Good / Bad |
| 8 | | Good / Bad |
| 9 | | Good / Bad |
| 10 | | Good / Bad |
| 11 | | Good / Bad |
| 12 | | Good / Bad |
| 13 | | Good / Bad |
| 14 | | Good / Bad |
| 15 | | Good / Bad |
| 16 | | Good / Bad |
| 17 | | Good / Bad |
| 18 | | Good / Bad |
| 19 | | Good / Bad |
| 20 | | Good / Bad |
| 21 | | Good / Bad |
| 22 | | Good / Bad |
| 23 | | Good / Bad |
| 24 | | Good / Bad |
| 25 | | Good / Bad |
| 26 | | Good / Bad |
| 27 | | Good / Bad |
| 28 | | Good / Bad |
| 29 | | Good / Bad |
| 30 | | Good / Bad |

**Sample Distribution:**
- Good samples: ____
- Bad samples: ____
- Borderline samples: ____

---

## Appraisal Data

### Appraiser A

| Sample | Ref | Trial 1 | Trial 2 | Trial 3 | Within Match |
|--------|-----|---------|---------|---------|--------------|
| 1 | | | | | Y / N |
| 2 | | | | | Y / N |
| 3 | | | | | Y / N |
| 4 | | | | | Y / N |
| 5 | | | | | Y / N |
| 6 | | | | | Y / N |
| 7 | | | | | Y / N |
| 8 | | | | | Y / N |
| 9 | | | | | Y / N |
| 10 | | | | | Y / N |
| 11 | | | | | Y / N |
| 12 | | | | | Y / N |
| 13 | | | | | Y / N |
| 14 | | | | | Y / N |
| 15 | | | | | Y / N |
| 16 | | | | | Y / N |
| 17 | | | | | Y / N |
| 18 | | | | | Y / N |
| 19 | | | | | Y / N |
| 20 | | | | | Y / N |
| 21 | | | | | Y / N |
| 22 | | | | | Y / N |
| 23 | | | | | Y / N |
| 24 | | | | | Y / N |
| 25 | | | | | Y / N |
| 26 | | | | | Y / N |
| 27 | | | | | Y / N |
| 28 | | | | | Y / N |
| 29 | | | | | Y / N |
| 30 | | | | | Y / N |

### Appraiser B

| Sample | Ref | Trial 1 | Trial 2 | Trial 3 | Within Match |
|--------|-----|---------|---------|---------|--------------|
| 1 | | | | | Y / N |
| 2 | | | | | Y / N |
| ... | | | | | |
| 30 | | | | | Y / N |

### Appraiser C

| Sample | Ref | Trial 1 | Trial 2 | Trial 3 | Within Match |
|--------|-----|---------|---------|---------|--------------|
| 1 | | | | | Y / N |
| 2 | | | | | Y / N |
| ... | | | | | |
| 30 | | | | | Y / N |

---

## Results Calculations

### Within Appraiser Agreement

| Appraiser | Matches (all trials same) | Total | Agreement % |
|-----------|---------------------------|-------|-------------|
| A | | 30 | % |
| B | | 30 | % |
| C | | 30 | % |
| **Average** | | | **%** |

### Appraiser vs Standard

| Appraiser | Correct Decisions | Total Decisions | Effectiveness % |
|-----------|-------------------|-----------------|-----------------|
| A | | | % |
| B | | | % |
| C | | | % |
| **Average** | | | **%** |

### Between Appraiser Agreement

| Sample | All Same? | Ref | Notes |
|--------|-----------|-----|-------|
| 1 | Y / N | | |
| 2 | Y / N | | |
| ... | | | |
| 30 | Y / N | | |

**Total all appraisers agree:** ____ / 30 = ____%

### All Trials, All Appraisers

| Category | Count |
|----------|-------|
| All agree and match reference | |
| All agree but wrong | |
| Appraisers disagree | |
| **Total** | 30 |

---

## Effectiveness Analysis

### Error Types

| Error Type | Description | Count | Impact |
|------------|-------------|-------|--------|
| False Accept (Type II) | Bad called Good | | High - defects escape |
| False Reject (Type I) | Good called Bad | | Medium - scrap good parts |

### Effectiveness by Category

| Actual Status | Accepted | Rejected | Effectiveness |
|---------------|----------|----------|---------------|
| Good (reference) | | | % |
| Bad (reference) | | | % |

---

## Kappa Calculation

### Contingency Table (All Decisions)

|  | Reference: Good | Reference: Bad | Total |
|--|-----------------|----------------|-------|
| **Appraised: Good** | | | |
| **Appraised: Bad** | | | |
| **Total** | | | |

### Kappa Calculation

```
P_observed = (agree Good + agree Bad) / Total = ____
P_chance = (Expected Good agreement + Expected Bad agreement) / Total = ____

Kappa = (P_observed - P_chance) / (1 - P_chance)
Kappa = (_____ - _____) / (1 - _____)
Kappa = _____
```

---

## Results Summary

| Metric | Result | Target | Status |
|--------|--------|--------|--------|
| Within Appraiser Agreement | % | ≥90% | Pass / Fail |
| Between Appraiser Agreement | % | ≥90% | Pass / Fail |
| Appraiser vs Standard | % | ≥90% | Pass / Fail |
| Kappa | | ≥0.75 | Pass / Fail |
| False Accept Rate | % | <5% | Pass / Fail |

---

## Interpretation

### Kappa Interpretation

| Kappa Value | Assessment |
|-------------|------------|
| <0.20 | Poor agreement |
| 0.21-0.40 | Fair agreement |
| 0.41-0.60 | Moderate agreement |
| 0.61-0.80 | Substantial agreement |
| 0.81-1.00 | Almost perfect agreement |

**This study Kappa:** _______ = _______________ agreement

---

## Overall Conclusion

- [ ] **ACCEPTABLE** - Measurement system approved for use
- [ ] **CONDITIONALLY ACCEPTABLE** - Approved with improvement plan
- [ ] **UNACCEPTABLE** - Measurement system not approved

---

## Problem Samples (If Any)

| Sample # | Issue | Appraisers | Potential Cause |
|----------|-------|------------|-----------------|
| | | | |
| | | | |

---

## Actions Required (if applicable)

| Action | Responsible | Due Date | Status |
|--------|-------------|----------|--------|
| | | | |
| | | | |

---

## Approvals

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Study Conductor | | | |
| Quality Engineer | | | |
| Process Owner | | | |
