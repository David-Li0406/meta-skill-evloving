# Verification Methods Reference

## Overview

Verification is critical in 8D problem solving. This reference covers methods for verifying root cause and validating corrective action effectiveness.

---

## Root Cause Verification

### Why Verify Root Cause?

| Risk | Consequence |
|------|-------------|
| Wrong root cause | Corrective actions don't work |
| Multiple causes missed | Problem only partially solved |
| Symptom treated as cause | Problem recurs |
| Wasted resources | Time and money on wrong fixes |

### Verification Hierarchy

| Method | Confidence | Description |
|--------|------------|-------------|
| **Reproduction** | Highest | Re-create defect by applying cause |
| **Elimination** | High | Remove cause, verify defect stops |
| **Statistical correlation** | Medium-High | Data shows cause-effect relationship |
| **Physical evidence** | Medium-High | Forensic analysis confirms mechanism |
| **Expert judgment** | Medium | SME consensus on mechanism |

---

## Reproduction Verification

### Principle

If the identified cause truly creates the defect, deliberately applying that cause should reproduce the defect.

### Steps

1. **Control the test environment** - Same equipment, material, conditions
2. **Apply the suspected cause** - Deliberately introduce the condition
3. **Observe the result** - Does the same defect occur?
4. **Repeat** - Confirm reproducibility (3+ times)

### Example

**Problem:** Dimension out of spec (25.08mm vs 25.00 ±0.03mm)

**Suspected cause:** Operator bypassed wear offset update

**Reproduction test:**
1. Set machine to known good condition
2. Run 50 parts with proper offset updates → All good
3. Deliberately skip offset update for 20 parts → 8 parts out of spec
4. Defect matches original (oversize OD)

**Conclusion:** Root cause verified by reproduction

### When Reproduction Is Not Possible

| Situation | Alternative |
|-----------|-------------|
| Destructive failure | Accelerated testing, simulation |
| Rare event | Statistical analysis, FMEA |
| Safety risk | Simulation, controlled environment |
| Cost prohibitive | Expert analysis, physical evidence |

---

## Elimination Verification

### Principle

If the identified cause is removed or corrected, the defect should stop occurring.

### Steps

1. **Implement temporary fix** - Address only the suspected cause
2. **Monitor results** - Track defect occurrence
3. **Compare before/after** - Statistical comparison
4. **Confirm no other changes** - Isolate the variable

### Example

**Problem:** Surface finish out of spec (Ra 4.2 vs max 3.2)

**Suspected cause:** Coolant concentration too low (2% vs spec 5%)

**Elimination test:**
1. Day 1-3: Continue at 2% coolant → 15% defect rate
2. Day 4: Adjust coolant to 5%
3. Day 5-7: Monitor at 5% → 0% defect rate
4. No other changes made

**Conclusion:** Root cause verified by elimination

### Confirmation Period

| Defect Rate | Minimum Monitoring |
|-------------|-------------------|
| >10% | 3-5 days |
| 1-10% | 1-2 weeks |
| <1% | 3-4 weeks |
| Very rare | Statistical sample |

---

## Statistical Correlation

### Principle

Data analysis shows statistically significant relationship between cause and effect.

### Methods

| Method | Use Case |
|--------|----------|
| Correlation analysis | Continuous variables |
| Chi-square test | Categorical variables |
| Regression | Predictive relationship |
| Control chart analysis | Time-series patterns |
| DOE | Multiple factors |

### Example: Correlation Analysis

**Problem:** Intermittent dimensional variation

**Data collected:** 200 parts with material hardness and dimension

**Analysis:**
- Correlation coefficient: r = 0.87
- P-value: <0.001
- Relationship: Higher hardness → larger dimension

**Conclusion:** Statistically significant relationship supports material hardness as contributing factor

### Caution

Correlation ≠ Causation

Always combine statistical analysis with physical understanding of the mechanism.

---

## Physical Evidence Verification

### Principle

Forensic analysis of failed parts confirms the failure mechanism matches the suspected cause.

### Analysis Types

| Analysis | What It Reveals |
|----------|-----------------|
| Visual inspection | Surface conditions, damage patterns |
| Dimensional | Deviations from spec |
| Metallurgical | Material structure, heat treat |
| Chemical | Composition, contamination |
| Fractography | Fracture origin, mechanism |
| SEM/EDS | Surface features, elemental analysis |

### Example

**Problem:** Shaft fracture in service

**Suspected cause:** Fatigue from stress concentration at fillet

**Physical evidence:**
1. Beach marks visible on fracture surface (fatigue indicator)
2. Fracture origin at fillet radius
3. Fillet radius measured 0.2mm vs spec 0.5mm minimum
4. Stress analysis confirms fillet is highest stress location

**Conclusion:** Physical evidence confirms fatigue failure initiated at undersized fillet

---

## Verification Documentation

### Required Elements

| Element | Description |
|---------|-------------|
| Root cause statement | Clear, specific cause |
| Verification method | Which method used |
| Test conditions | How test was conducted |
| Results | Data, measurements, observations |
| Conclusion | Does evidence support cause? |
| Approval | Sign-off that verification is adequate |

### Verification Record Template

```
ROOT CAUSE VERIFICATION RECORD

8D Number: ____________
Root Cause: ____________________________________________

Verification Method: [ ] Reproduction [ ] Elimination [ ] Correlation [ ] Physical

Test Description:
__________________________________________________________________
__________________________________________________________________

Test Conditions:
__________________________________________________________________

Results:
__________________________________________________________________
__________________________________________________________________

Conclusion: [ ] Verified [ ] Not Verified [ ] Partially Verified

If partially verified, additional investigation needed:
__________________________________________________________________

Verified by: _____________ Date: _____________
Approved by: _____________ Date: _____________
```

---

## Corrective Action Effectiveness Validation

### Verification vs Validation

| Verification | Validation |
|--------------|------------|
| Was action implemented correctly? | Did action solve the problem? |
| Check the process | Check the outcome |
| Immediate | Over time |
| Yes/No | Metric improvement |

---

## Implementation Verification

### What to Verify

| Change Type | Verification Evidence |
|-------------|----------------------|
| Procedure change | Document revision, training records |
| Equipment change | Maintenance record, photos, settings |
| Tooling change | First article, capability study |
| Process parameter | Settings verification, SPC chart |
| Inspection change | Control Plan, actual practice audit |
| Training | Training records, competency check |

### Verification Checklist

- [ ] Change documented in appropriate system
- [ ] Affected personnel trained
- [ ] Change implemented per plan
- [ ] Settings/configurations confirmed
- [ ] Visual confirmation (photos if applicable)
- [ ] First article/trial run acceptable

---

## Effectiveness Validation

### Validation Criteria

| Criterion | Target | Measurement |
|-----------|--------|-------------|
| **Defect recurrence** | Zero | Track specific defect |
| **PPM improvement** | Per target | Before/after comparison |
| **Capability** | ≥1.33 Cpk | Capability study |
| **Process stability** | In control | Control chart |
| **Customer feedback** | No complaints | Customer reports |

### Validation Timeline

| Phase | Duration | Check |
|-------|----------|-------|
| Immediate | 1-7 days | No defects on initial lots |
| Short-term | 2-4 weeks | Sustained performance |
| Medium-term | 1-3 months | Confirmed effectiveness |
| Long-term | 3-12 months | Systemic verification |

### Validation Methods

| Method | Application |
|--------|-------------|
| **Before/After comparison** | Compare metric pre and post change |
| **Control chart** | Process stability over time |
| **Capability study** | Cpk improvement |
| **Audit** | Verify continued compliance |
| **Customer acceptance** | Zero complaints post-change |

---

## Validation Data Collection

### Sample Size Guidelines

| Validation Type | Minimum Sample |
|-----------------|----------------|
| Defect rate comparison | 500-1000 units each period |
| Capability study | 30-50 consecutive |
| Before/After PPM | At least 30 days each |
| Customer validation | 3-6 months no complaints |

### Statistical Comparison

For before/after defect rate comparison:

1. **Collect baseline data** (before corrective action)
2. **Collect validation data** (after corrective action)
3. **Statistical test** - Chi-square or proportion test
4. **Confirm significance** - P-value <0.05

### Example Validation

**Problem:** Defect rate 2.5%

**Corrective action:** Process parameter change

**Validation:**
| Period | Sample | Defects | Rate |
|--------|--------|---------|------|
| Before | 5,000 | 125 | 2.5% |
| After | 5,000 | 3 | 0.06% |

**Statistical test:** Chi-square p-value < 0.001

**Conclusion:** Statistically significant improvement validates effectiveness

---

## Closure Criteria

### Standard Closure Criteria

- [ ] Root cause verified by reproduction or elimination
- [ ] All corrective actions implemented
- [ ] Implementation verified
- [ ] Effectiveness validated for minimum period
- [ ] No defect recurrence during validation period
- [ ] FMEA/Control Plan updated
- [ ] Customer accepts closure (if applicable)

### Validation Period by Severity

| Severity | Minimum Validation |
|----------|-------------------|
| Safety/Regulatory | 6 months zero defects |
| Customer complaint | 3 months zero defects |
| High-volume production | 30 days zero defects |
| Low-volume/intermittent | Minimum 3 production runs |

---

## Failed Validation

### If Validation Fails

1. **Don't close the 8D** - Return to analysis
2. **Review root cause** - Was it correct?
3. **Review corrective actions** - Were they adequate?
4. **Check implementation** - Properly executed?
5. **Investigate new factors** - What changed?

### Escalation

If repeated validation failures:
- Escalate to management
- Consider external expertise
- Review fundamental approach
- Increase team resources

---

## Documentation Requirements

### Validation Record

```
CORRECTIVE ACTION EFFECTIVENESS VALIDATION

8D Number: ____________
Corrective Action: ________________________________________

Validation Method: _________________________________________

Validation Period: From ____________ to ____________

Metrics:
| Metric | Before | After | Target | Result |
|--------|--------|-------|--------|--------|
|        |        |       |        |        |
|        |        |       |        |        |

Statistical Analysis (if applicable):
__________________________________________________________________

Conclusion: [ ] Effective [ ] Not Effective

If not effective, next steps:
__________________________________________________________________

Validated by: _____________ Date: _____________
Approved by: _____________ Date: _____________
```

### Retention

Keep verification and validation records:
- Attached to 8D report
- Minimum 3 years
- Per customer requirements
- Accessible for audits
