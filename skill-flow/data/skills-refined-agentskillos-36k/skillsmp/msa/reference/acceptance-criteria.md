# MSA Acceptance Criteria Reference

## Variable MSA (Gage R&R)

### %GR&R Criteria

| %GR&R | Classification | Decision | Application |
|-------|----------------|----------|-------------|
| <10% | Excellent | Acceptable | All applications |
| 10-20% | Acceptable | Acceptable | Most applications, may need improvement for critical |
| 20-30% | Marginal | Conditionally acceptable | Requires customer approval for critical |
| >30% | Unacceptable | Not acceptable | Improvement required before use |

### Customer-Specific Criteria

Some customers may have different requirements. Always check customer-specific requirements (CSRs).

| Customer Type | Typical Requirement |
|---------------|---------------------|
| Tier 1 Automotive | <10% for CC, <30% for SC |
| General Industrial | <30% acceptable |
| Aerospace | Often <10% required |
| Medical | Often <10% required |

### %GR&R Basis

Two calculation bases are used:

| Basis | Formula | When to Use |
|-------|---------|-------------|
| % of Study Variation | GRR/TV × 100 | Standard - measures gage capability relative to process |
| % of Tolerance | GRR/(Tolerance/6) × 100 | Alternative - measures gage relative to spec |

**MNMUK Standard:** Use % of Study Variation (TV) as primary metric.

---

## Number of Distinct Categories (ndc)

| ndc | Classification | Interpretation |
|-----|----------------|----------------|
| ≥5 | Acceptable | Gage can adequately distinguish between parts |
| 4 | Marginal | Limited discrimination ability |
| 3 | Marginal | Very limited, acts like rough attribute |
| 2 | Unacceptable | Can only tell "good" from "bad" |
| 1 | Unacceptable | Cannot distinguish parts at all |

### ndc Requirements by Application

| Application | Minimum ndc |
|-------------|-------------|
| SPC control charts | ≥5 |
| Process capability studies | ≥5 |
| General inspection | ≥3 |
| Go/No-go replacement | ≥2 |

---

## Attribute MSA Criteria

### Agreement Percentages

| Metric | Acceptable | Marginal | Unacceptable |
|--------|------------|----------|--------------|
| Within Appraiser | ≥90% | 80-90% | <80% |
| Between Appraiser | ≥90% | 80-90% | <80% |
| Appraiser vs Standard | ≥90% | 80-90% | <80% |

### Kappa Criteria

| Kappa | Classification | Interpretation |
|-------|----------------|----------------|
| ≥0.90 | Excellent | Almost perfect agreement |
| 0.75-0.89 | Good | Substantial agreement |
| 0.60-0.74 | Acceptable | Moderate to substantial |
| 0.40-0.59 | Marginal | Moderate agreement |
| <0.40 | Unacceptable | Fair to poor agreement |

### Error Rate Criteria

| Error Type | Definition | Maximum Acceptable |
|------------|------------|-------------------|
| False Accept (Miss Rate) | Bad parts called Good | <5% |
| False Reject | Good parts called Bad | <10% |

**Note:** False Accept is more critical - defects escape to customer.

---

## Bias and Linearity Criteria

### Bias

| Criterion | Formula | Acceptable |
|-----------|---------|------------|
| Bias | Measured avg - Reference | ≈0 or within calibration tolerance |
| % Bias | (Bias / Process Variation) × 100 | <5% |
| Statistical Significance | t-test on bias | p-value >0.05 (not significant) |

### Linearity

| Criterion | Formula | Acceptable |
|-----------|---------|------------|
| Linearity | Range of bias across measurement range | <5% of Process Variation |
| Slope | Regression slope | ≈0 |
| Statistical Significance | Slope confidence interval includes 0 | Yes |

---

## Stability Criteria

| Criterion | Method | Acceptable |
|-----------|--------|------------|
| Control Chart | Plot master measurements over time | In control (no OOC signals) |
| Variation | Range of measurements | Within historical limits |
| Trend | Visual or statistical analysis | No significant trend |

---

## Criteria by Characteristic Classification

### Critical Characteristics (CC)

| Metric | Requirement |
|--------|-------------|
| %GR&R | <10% |
| ndc | ≥5 |
| Attribute agreement | ≥95% |
| Kappa | ≥0.90 |
| False Accept | <2% |

### Significant Characteristics (SC)

| Metric | Requirement |
|--------|-------------|
| %GR&R | <30% (prefer <20%) |
| ndc | ≥4 |
| Attribute agreement | ≥90% |
| Kappa | ≥0.75 |
| False Accept | <5% |

### Standard Characteristics

| Metric | Requirement |
|--------|-------------|
| %GR&R | <30% |
| ndc | ≥3 |
| Attribute agreement | ≥85% |
| Kappa | ≥0.60 |
| False Accept | <10% |

---

## Decision Guidelines

### When %GR&R is Marginal (10-30%)

Consider:
1. Characteristic classification (CC/SC/Standard)
2. Process capability (if Cpk >2, marginal GRR may be acceptable)
3. Customer requirements
4. Cost of improvement vs. risk
5. Historical quality performance

Actions:
- Document rationale for acceptance
- Obtain customer approval if required
- Develop improvement plan
- Monitor more frequently

### When ndc is Low (<5)

Consider:
1. Is SPC really needed for this characteristic?
2. Can a more sensitive gage be used?
3. Is process variation adequate for the study?
4. Would attribute inspection be acceptable?

Actions:
- Improve gage resolution/capability
- Verify study parts represent actual process variation
- Consider alternative measurement method
- Document if attribute capability accepted

### When Attribute Agreement is Low

Consider:
1. Are standards/criteria clear?
2. Are samples adequately representing borderline cases?
3. Is training adequate?
4. Is the characteristic truly measurable?

Actions:
- Clarify acceptance criteria
- Develop boundary samples
- Retrain appraisers
- Consider variable measurement if possible

---

## Special Considerations

### New Gage/New Process

May have limited data for %GR&R vs. process variation:
- Use % of tolerance as alternative
- Establish provisional acceptance
- Re-study after process data available

### High Precision Requirements

Some applications require tighter criteria:
- Precision measurement (e.g., optical)
- High-value parts
- Safety-critical applications

Consider %GR&R <5% for these applications.

### Automated Measurement

For automated gaging:
- Repeatability should be very low
- Focus on stability over time
- Verify correlation to laboratory measurements
- Regular verification with masters
