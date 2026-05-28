# MSA - Extended Guidance

**Deep-dive content for comprehensive measurement system analysis.**

---

## Table of Contents

1. [MSA Planning and Preparation](#msa-planning-and-preparation)
2. [Detailed Study Procedures](#detailed-study-procedures)
3. [Statistical Foundations](#statistical-foundations)
4. [Troubleshooting Poor Results](#troubleshooting-poor-results)
5. [Special Situations](#special-situations)
6. [CMM and Automated Measurement](#cmm-and-automated-measurement)
7. [MSA Program Management](#msa-program-management)

---

## MSA Planning and Preparation

### Determining MSA Needs

**Questions to answer:**
1. What characteristics require MSA?
2. What type of study is appropriate?
3. Who will participate?
4. What parts/standards are needed?
5. How often should MSA be repeated?

### MSA Priority Matrix

| Characteristic | MSA Priority | Frequency |
|----------------|--------------|-----------|
| CC (Critical) | Mandatory | Annual + after change |
| SC (Significant) | Mandatory | Annual |
| SPC monitored | Mandatory | Annual |
| Standard | Recommended | Every 2-3 years |
| Incoming inspection | Recommended | Annual |

### Pre-Study Checklist

- [ ] Gage calibrated and in good condition
- [ ] Resolution adequate (≤1/10 of tolerance)
- [ ] Range adequate for characteristic
- [ ] Parts available representing process variation
- [ ] Operators available and trained
- [ ] Environment stable (temperature, vibration)
- [ ] Data collection method ready

---

## Detailed Study Procedures

### Variable Gage R&R - Step by Step

**Preparation:**
1. Select gage and verify calibration
2. Select 10 parts from process (representing variation)
3. Number parts (hidden from operator view)
4. Identify 3 operators
5. Prepare data collection form
6. Ensure stable environment

**Execution:**
1. Randomize measurement order
2. First operator measures all 10 parts (random order)
3. Record measurements
4. Operator measures all 10 parts again (different random order)
5. Repeat for third trial
6. Repeat steps 2-5 for remaining operators
7. Keep parts numbered but hidden from operators

**Data Collection Form:**

| Part | Op A T1 | Op A T2 | Op A T3 | Op B T1 | Op B T2 | Op B T3 | Op C T1 | Op C T2 | Op C T3 |
|------|---------|---------|---------|---------|---------|---------|---------|---------|---------|
| 1 | | | | | | | | | |
| 2 | | | | | | | | | |
| ... | | | | | | | | | |
| 10 | | | | | | | | | |

### Attribute Agreement - Step by Step

**Preparation:**
1. Select 30+ samples (include borderline cases)
2. Have expert classify each sample (reference)
3. Number samples
4. Identify 3 appraisers
5. Prepare data collection form

**Execution:**
1. Randomize sample order
2. First appraiser classifies all samples
3. Record decisions
4. Reshuffle samples
5. Appraiser classifies all samples again
6. Repeat for third trial
7. Repeat for remaining appraisers

**Data Collection Form:**

| Sample | Reference | Op A T1 | Op A T2 | Op A T3 | Op B T1 | ... |
|--------|-----------|---------|---------|---------|---------|-----|
| 1 | Good | | | | | |
| 2 | Bad | | | | | |
| ... | | | | | | |

---

## Statistical Foundations

### Variance Components

Total Observed Variance = Part Variance + Measurement Variance

Measurement Variance = Repeatability + Reproducibility

```
σ²_total = σ²_part + σ²_measurement
σ²_measurement = σ²_repeatability + σ²_reproducibility
```

### ANOVA Calculations

**Source of Variation:**

| Source | Degrees of Freedom | Sum of Squares | Mean Square | Variance |
|--------|-------------------|----------------|-------------|----------|
| Part | p-1 | SS_part | MS_part | σ²_part |
| Operator | o-1 | SS_operator | MS_operator | σ²_operator |
| Part×Operator | (p-1)(o-1) | SS_interaction | MS_interaction | σ²_interaction |
| Repeatability | po(r-1) | SS_repeat | MS_repeat | σ²_repeat |
| Total | por-1 | SS_total | | |

Where: p=parts, o=operators, r=trials

**Variance Estimates:**
```
σ²_repeat = MS_repeat
σ²_interaction = (MS_interaction - MS_repeat) / r
σ²_operator = (MS_operator - MS_interaction) / (p×r)
σ²_part = (MS_part - MS_interaction) / (o×r)

σ²_reproducibility = σ²_operator + σ²_interaction
σ²_GRR = σ²_repeat + σ²_reproducibility
```

### X-bar/R Method Calculations

**Constants:**

| Trials | K₁ |
|--------|-----|
| 2 | 4.56 |
| 3 | 3.05 |

| Operators | K₂ |
|-----------|-----|
| 2 | 3.65 |
| 3 | 2.70 |

**Formulas:**
```
R̄ = average of all ranges (within operator, per part)
EV = R̄ × K₁

X̄_diff = max(operator averages) - min(operator averages)
AV = √[(X̄_diff × K₂)² - (EV²/(n×r))]
Note: If negative under radical, AV = 0

GRR = √(EV² + AV²)

R_p = max(part averages) - min(part averages)
PV = R_p × K₃  (K₃ based on parts, usually 1.62 for 10 parts)

TV = √(GRR² + PV²)

%EV = (EV/TV) × 100
%AV = (AV/TV) × 100
%GRR = (GRR/TV) × 100
%PV = (PV/TV) × 100

ndc = 1.41 × (PV/GRR)
```

### Attribute Agreement Calculations

**Agreement Percentages:**
```
Within Appraiser = (# same decisions both trials) / total × 100
Between Appraiser = (# all appraisers agree) / total × 100
Appraiser vs Standard = (# matching reference) / total × 100
```

**Kappa Calculation:**
```
Kappa = (P_observed - P_chance) / (1 - P_chance)

Where:
P_observed = proportion of agreement
P_chance = expected agreement by chance
```

---

## Troubleshooting Poor Results

### High Repeatability (Equipment Variation)

**Symptoms:** Same operator, different readings on same part

**Causes:**
| Potential Cause | Investigation |
|-----------------|---------------|
| Poor gage resolution | Check ≤1/10 of tolerance |
| Gage wear/damage | Inspect gage condition |
| Calibration drift | Verify calibration |
| Environment | Check temperature, vibration |
| Part fixturing | Check part location consistency |
| Operator technique | Observe measurement method |

**Solutions:**
- Calibrate or repair gage
- Use higher resolution gage
- Improve fixturing
- Control environment
- Standardize technique

### High Reproducibility (Appraiser Variation)

**Symptoms:** Different operators get different readings

**Causes:**
| Potential Cause | Investigation |
|-----------------|---------------|
| Inconsistent technique | Observe each operator |
| Different interpretation | Review instructions |
| Training gap | Check training records |
| Physical differences | Observe operator ergonomics |
| Gage condition | Check for wear patterns |

**Solutions:**
- Standardize work instruction
- Retrain operators
- Improve measurement method
- Consider fixtures to reduce operator influence

### High Part × Operator Interaction

**Symptoms:** Some operators better on some parts than others

**Causes:**
| Potential Cause | Investigation |
|-----------------|---------------|
| Part-specific technique needed | Review method for different part features |
| Operator-specific blind spots | Observe specific difficulties |
| Part condition variation | Inspect parts for differences |

**Solutions:**
- Develop robust measurement method
- Additional training
- Fixture improvements

### Low ndc

**Symptoms:** ndc <5, gage can't distinguish parts

**Causes:**
| Potential Cause | Investigation |
|-----------------|---------------|
| Parts too similar | Verify parts represent process variation |
| GRR too high | Address repeatability/reproducibility |
| Gage not sensitive enough | Check resolution vs. variation |

**Solutions:**
- Use more sensitive gage
- Reduce GRR
- Verify parts span process variation
- Accept attribute-level capability (if appropriate)

---

## Special Situations

### Destructive Testing

When parts can only be measured once:
- Use nested design (different parts per operator)
- Assume parts from same batch are identical
- Larger sample size needed
- Use ANOVA analysis

### Non-Replicable Measurements

When measurement changes the part:
- Torque verification
- Hardness testing
- Some surface measurements

**Approach:**
- Use multiple similar specimens
- Estimate repeatability from batch variation
- Document assumptions

### Small Sample Situations

When <10 parts available:
- Use all available parts
- Increase trials per part
- Document limitations
- Consider reduced confidence

### Multiple Gages

When multiple gages measure same characteristic:
- Perform MSA on each gage
- Consider inter-gage variation
- May need gage correlation study

### CMM Measurements

See dedicated section below.

---

## CMM and Automated Measurement

### CMM-Specific Considerations

| Factor | Impact | Mitigation |
|--------|--------|------------|
| Program variation | Different programmers, different results | Use locked programs |
| Fixturing | Part location affects results | Standardize fixturing |
| Probe calibration | Affects accuracy | Regular calibration |
| Environment | Temperature affects CMM accuracy | Temperature control |
| Strategy | Touch points affect results | Standardize probing strategy |

### CMM MSA Study Modifications

**Repeatability:**
- Run same program multiple times
- Same operator, same part
- Evaluate equipment variation

**Reproducibility:**
- Different operators running same program
- Should be minimal (program-driven)
- Focus on setup/fixturing variation

**Program Validation:**
- Compare CMM to other methods
- Verify probing strategy appropriate
- Validate on reference parts

### Automated Gage MSA

For in-process automated gaging:

| Study Element | Method |
|---------------|--------|
| Repeatability | Multiple measurements same part |
| Gage stability | Control chart on masters |
| Accuracy | Compare to lab measurements |
| Correlation | Gage vs. CMM |

---

## MSA Program Management

### MSA Master List

Track all measurement systems requiring MSA:

| Gage ID | Description | Characteristic | Type | Last MSA | Next Due | Status |
|---------|-------------|----------------|------|----------|----------|--------|
| | | | | | | |

### MSA Frequency Guidelines

| Trigger | Required Action |
|---------|-----------------|
| New gage | Initial MSA before use |
| Gage repair | Re-study after repair |
| Gage calibration | May require re-study |
| Process change | Evaluate if MSA still valid |
| Annual | Confirm MSA current |
| Poor SPC results | Investigate MSA as cause |
| Customer complaint | Re-evaluate MSA |

### MSA Documentation Requirements

**For each study, maintain:**
- Study parameters (operators, parts, trials)
- Raw data
- Calculations or software output
- Conclusion and disposition
- Actions taken (if failed)
- Approval signatures

### Continuous MSA Monitoring

**SPC on Masters:**
- Regular measurement of reference part
- Plot on control chart
- Detects drift before it affects production

**Benefits:**
- Early warning of measurement problems
- Reduced frequency of full studies
- Better overall measurement confidence

---

## Software Tools

### MSA Software Options

| Software | Type | Features |
|----------|------|----------|
| Minitab | Commercial | Full MSA, ANOVA |
| JMP | Commercial | Full MSA, visualization |
| Excel templates | Custom | Basic calculations |
| SPC software | Varies | Often includes MSA module |

### Excel Template Tips

**For Gage R&R:**
- Use structured data entry
- Automate calculations with formulas
- Include charts (range chart, X-bar chart)
- Calculate all metrics (%GRR, ndc)

**For Attribute Agreement:**
- Matrix layout for easy data entry
- Automatic agreement calculations
- Kappa calculation
- Effectiveness summary

---

## Industry-Specific Guidance

### Automotive Requirements

- AIAG MSA Manual (4th Edition) as reference
- MSA for all Control Plan gages
- ndc ≥5 for SPC applications
- Customer approval for marginal systems

### Common Customer Requirements

| Customer | Key Requirements |
|----------|------------------|
| General | AIAG MSA Manual compliance |
| Some OEMs | %GR&R vs. tolerance preferred |
| Some OEMs | Specific acceptance criteria |

Always verify customer-specific requirements (CSRs).
