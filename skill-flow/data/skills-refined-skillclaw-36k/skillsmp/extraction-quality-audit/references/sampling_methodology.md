# Stratified Sampling Methodology

This document explains the sampling methodology used in extraction quality audits.

## Overview

**Stratified random sampling** is a probability sampling technique where the population is divided into distinct subgroups (strata) and random samples are taken from each stratum. This ensures representative coverage of important subpopulations.

For extraction quality audits, we stratify by:
- **Confidence scores** (low, medium, high)
- **Document complexity** (simple, multi-page, complex)
- **Time period/era** (1990s, 2000s, 2010s, 2020s)
- **Document category** (type-specific)
- **Custom characteristics** (handwritten, image-heavy, etc.)

## Why Stratified Sampling?

**Benefits:**
1. **Ensures coverage** of rare but critical cases (e.g., low confidence documents)
2. **More efficient** than simple random sampling for heterogeneous populations
3. **Reduces sampling error** for important subgroups
4. **Enables subgroup analysis** (compare quality across document types)
5. **Statistical rigor** while maintaining practical sample sizes

**Comparison to alternatives:**
- **Simple random sampling:** Might miss rare cases (e.g., only 5 LOW_CONF docs in 199)
- **Convenience sampling:** Introduces bias, not statistically valid
- **Systematic sampling:** Doesn't guarantee representation of small subgroups

## Priority Tag System

Priority tags identify documents with higher risk or importance for quality assessment.

### Default Priority Tags

| Tag | Definition | Priority Weight | Default Coverage |
|-----|------------|-----------------|------------------|
| `LOW_CONF` | min_confidence < 0.7 | 1000 | 100% |
| `COMPLEX` | page_count >= 10 | 100 | 100% |
| `OLD_DOC` | era in [1990s, 2000s] | 10 | 60-80% |
| `MULTI_PAGE` | 3 <= page_count < 10 | 1 | 40-60% |

**Priority weights** determine sampling order (higher = sampled first).

**Coverage** specifies what percentage of documents with this tag should be included in the sample.

### Custom Priority Tags

Create custom tags for your domain:

**Medical Documents:**
```python
'HANDWRITTEN': lambda doc: 'prescription' in doc.get('category', '').lower(),
'IMAGE_HEAVY': lambda doc: 'endoscopy' in doc.get('category', '').lower(),
'COMPLEX_ANATOMY': lambda doc: doc.get('word_count', 0) > 5000,
```

**Legal Documents:**
```python
'MULTI_PARTY': lambda doc: doc.get('party_count', 0) > 2,
'LONG_FORM': lambda doc: doc.get('page_count', 0) > 50,
'HISTORICAL': lambda doc: doc.get('year', 9999) < 1950,
```

**Financial Documents:**
```python
'HIGH_VALUE': lambda doc: doc.get('transaction_amount', 0) > 1000000,
'MULTI_CURRENCY': lambda doc: doc.get('currency_count', 0) > 1,
'COMPLEX_TABLES': lambda doc: doc.get('table_count', 0) > 10,
```

### Tag Design Guidelines

**Good tags:**
- ✓ Objective criteria (confidence score, page count, date)
- ✓ Actionable (identifies specific quality concerns)
- ✓ Mutually inclusive (documents can have multiple tags)
- ✓ Stable across audit runs

**Avoid:**
- ✗ Subjective criteria requiring manual judgment
- ✗ Redundant with existing tags
- ✗ Too granular (creates tiny strata)

## Sample Size Calculation

### Recommended Sizes by Corpus Size

| Corpus Size | Minimum Sample | Recommended Sample | Coverage |
|-------------|----------------|-------------------|----------|
| < 100 docs | 25-30 | 30-40 | 25-40% |
| 100-500 docs | 30-40 | 40-60 | 10-20% |
| 500-1000 docs | 40-60 | 60-100 | 6-12% |
| 1000-5000 docs | 60-100 | 100-200 | 2-5% |
| > 5000 docs | 100-200 | 200-500 | 1-4% |

### Statistical Confidence

**Confidence intervals** depend on sample size and population characteristics:

For **proportions** (e.g., error rate):
- **n=30:** ±18% margin of error at 95% confidence
- **n=50:** ±14% margin of error at 95% confidence
- **n=100:** ±10% margin of error at 95% confidence
- **n=200:** ±7% margin of error at 95% confidence

**Note:** These assume simple random sampling. Stratified sampling typically achieves better precision.

### Critical Cases Always Included

**100% coverage** of critical cases is non-negotiable:
- **All LOW_CONF documents** (often <5% of corpus)
- **All COMPLEX documents** (often <5% of corpus)
- **All ERROR_FLAGGED documents** (if available)

Even if this exceeds target sample size, include them all.

## Sampling Phases

### Phase 1: Priority Tags (High Coverage)

Sample documents based on priority tags, starting with highest priority.

**Example (target n=30):**
```
1. LOW_CONF (5 docs) → 100% coverage = 5 sampled
2. COMPLEX (4 docs) → 100% coverage = 4 sampled
3. OLD_DOC (18 docs) → 70% coverage = 13 sampled
4. MULTI_PAGE (44 docs) → 40% coverage = 18 sampled
   Total: 40 documents (10 over target, but acceptable)
```

**Overlap handling:** Documents can satisfy multiple tags. Track `used_stems` to avoid duplicates.

### Phase 2: Category Balancing

Ensure representation across document categories.

**Target distribution:** Proportional to corpus or minimum per category.

**Example:**
```python
category_balance = {
    'imaging': 3,      # At least 3 imaging documents
    'ultrasound': 3,
    'endoscopy': 3,
    'other': 2,
}
```

If category already well-represented in Phase 1, skip.

### Phase 3: Era Diversity

Ensure temporal diversity across document eras.

**Minimum representation:**
- 1990s: At least 1-2 documents (if available)
- 2000s: At least 2-3 documents
- 2010s: At least 3-5 documents
- 2020s: At least 3-5 documents

### Phase 4: Confidence Baseline

Include high-confidence documents as **baseline/control group**.

**Purpose:**
- Verify that high confidence correlates with high quality
- Establish quality ceiling
- Detect false negatives (high confidence but poor quality)

**Target:** 3-5 high confidence documents (confidence ≥ 0.9)

### Phase 5: Random Fill

Fill remaining slots with simple random sampling.

**Purpose:**
- Reach target sample size
- Add serendipity (discover unexpected patterns)
- Ensure truly representative sample

## Sampling Configuration

### Configuration File Format

```json
{
  "priority_tags": {
    "LOW_CONF": {
      "coverage": 1.0,
      "priority": 1000
    },
    "COMPLEX": {
      "coverage": 1.0,
      "priority": 100
    },
    "OLD_DOC": {
      "coverage": 0.7,
      "priority": 10
    },
    "MULTI_PAGE": {
      "coverage": 0.4,
      "priority": 1
    }
  },
  "category_balance": {
    "imaging": 3,
    "ultrasound": 3,
    "endoscopy": 3,
    "other": 2
  },
  "era_minimum": {
    "1990s": 1,
    "2000s": 2,
    "2010s": 3,
    "2020s": 3
  },
  "high_conf_baseline": 5,
  "random_seed": 42
}
```

### Adjusting Coverage Rates

**When to increase coverage:**
- High error rates discovered in initial verification
- Critical document type requires thorough assessment
- Compliance/audit requirements
- Small absolute numbers (e.g., only 3 OLD_DOC total)

**When to decrease coverage:**
- Very large corpus (>5000 documents)
- Time/budget constraints
- Preliminary/exploratory audit
- Consistent high quality observed

## Common Sampling Scenarios

### Scenario 1: Small Corpus (<100 docs)

**Approach:** Near-exhaustive sampling
- Target: 30-50% of corpus
- Include ALL critical cases
- High coverage of all tags (80-100%)
- Minimal random fill needed

### Scenario 2: Large Corpus (>1000 docs)

**Approach:** Targeted sampling
- Target: 1-5% of corpus (100-200 docs)
- 100% of critical cases (may be substantial)
- Medium coverage of high-priority tags (50-70%)
- Lower coverage of low-priority tags (20-30%)
- Significant random fill

### Scenario 3: Suspected Quality Issues

**Approach:** Problem-focused sampling
- Over-sample problem areas (e.g., 100% OLD_DOC if suspected issue)
- Include all LOW_CONF documents
- Add custom tags for suspected issues
- Reduce random fill, increase targeted sampling

### Scenario 4: Periodic Monitoring

**Approach:** Trend tracking
- Consistent sample size across audit runs
- Same random seed for reproducibility
- Track quality changes over time
- Include new document types as they appear

## Sample Validation

### Checking Sample Quality

Before verification, validate that sample is representative:

**1. Profile/User Distribution:**
```
Is profile distribution in sample similar to corpus?
Example: 32% Tiago, 68% Cristina in both
```

**2. Category Coverage:**
```
Are all major categories represented?
Any category < 5% of corpus but 0% of sample?
```

**3. Era Distribution:**
```
Does sample span full time range?
Any era completely missing?
```

**4. Complexity Distribution:**
```
Mix of simple, multi-page, and complex documents?
```

**5. Confidence Distribution:**
```
Sample includes low, medium, and high confidence?
```

### Red Flags

**Warning signs of poor sampling:**
- ⚠️ All sampled docs from single profile (if multi-profile corpus)
- ⚠️ Zero representation of major category (>10% of corpus)
- ⚠️ No high-confidence documents (can't establish baseline)
- ⚠️ All documents from single era (temporal bias)
- ⚠️ Sample entirely from problem cases (can't assess typical quality)

**Action:** Regenerate sample with adjusted parameters.

## Reporting Sample Composition

Always report sampling methodology in final report:

**Include:**
1. Target sample size and actual size
2. Priority tags used and coverage rates
3. Sampling phases applied
4. Profile/category/era distribution comparison (corpus vs. sample)
5. Statistical confidence level
6. Random seed (for reproducibility)

**Example:**
```
Sample Size: 44 documents (22% of 199 corpus)

Priority Coverage:
- LOW_CONF: 5/5 (100%)
- COMPLEX: 4/4 (100%)
- OLD_DOC: 15/18 (83%)
- MULTI_PAGE: 17/44 (39%)

Statistical Confidence: 95% confidence level with ±12% margin of error
Random Seed: 42
```

## Advanced Topics

### Adaptive Sampling

Adjust sampling during verification if unexpected patterns emerge:

**Example:**
- Initial sample reveals 50% error rate in category X
- Add more category X documents mid-audit
- Report: "Adaptive sampling applied: added 10 category X documents after initial findings"

### Multi-Stage Sampling

For very large corpora (>10,000 docs):

1. **Stage 1:** Sample documents (e.g., 200 docs)
2. **Stage 2:** For multi-page documents, sample pages (e.g., 2-3 pages per doc)

### Cluster Sampling

If documents organized in natural clusters (e.g., by patient, case, project):

1. Sample clusters (e.g., 20 patients)
2. Verify all documents within selected clusters

**Trade-off:** Easier to verify (fewer context switches) but potentially less representative.

## References

- Cochran, W. G. (1977). *Sampling Techniques*. Wiley.
- Lohr, S. L. (2019). *Sampling: Design and Analysis*. Chapman and Hall/CRC.
- Thompson, S. K. (2012). *Sampling*. Wiley.

## Version History

- **v1.0** (2026-01-21): Initial methodology based on medical-exams-parser quality investigation
