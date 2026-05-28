# Quality Assessment Report Template

This template provides the structure for comprehensive extraction quality reports.

## Report Header

```markdown
# [Pipeline Name] Quality Assessment Report

**Generated:** YYYY-MM-DD HH:MM
**Investigator:** [Name or "Claude Sonnet 4.5"]
**Total Documents:** [N]
**Sample Size:** [M] ([M/N]% of corpus)
**Documents Verified:** [K]
**Quality Grade:** [A/B/C/D/F]

---
```

## Section 1: Executive Summary

### Template

```markdown
## Executive Summary

This comprehensive quality investigation assessed the [domain] extraction pipeline across **[N] processed documents** spanning [time period]. Through stratified sampling and detailed verification of **[M] documents**, the investigation reveals the following:

### Overall Quality Grade: **[A/B/C/D/F] ([Excellent/Good/Fair/Poor/Failing])**

**Average Quality Score:** [X.X]/10

### Key Findings

[3-5 bullet points with high-level findings]

✅ **[Category]: [RATING]**
- [Key point 1]
- [Key point 2]

✅/**⚠️** **[Another Category]:**
- [Key point 1]

**Confidence Scoring:**
- Low confidence documents: [N]/[Total] ([%])
- [Assessment of confidence scoring]

**Critical Issues:** [None/N identified]
- [List if any]

### Recommendations

**Immediate Actions:** [None Required / List actions]

**Optional Enhancements:**
1. [Enhancement 1]
2. [Enhancement 2]
```

### Content Guidelines

**Keep it concise:** 1-2 pages maximum

**Focus on:**
- Overall quality grade (A-F)
- Most critical findings
- Actionable recommendations
- Statistical highlights

**Avoid:**
- Technical jargon without explanation
- Exhaustive details (save for later sections)
- Hedging language (be direct)

---

## Section 2: Data Landscape

### Template

```markdown
## Data Landscape

### Corpus Statistics

**Total Documents:** [N]

[If multiple profiles:]
| Profile | Documents | Percentage |
|---------|-----------|------------|
| [Name1] | [N1]      | [%]        |
| [Name2] | [N2]      | [%]        |

### Temporal Distribution

| Era/Period | Count | Percentage | Notes |
|------------|-------|------------|-------|
| [1990s]    | [N]   | [%]        | [Oldest documents] |
| [2000s]    | [N]   | [%]        |  |
| [2010s]    | [N]   | [%]        |  |
| [2020s]    | [N]   | [%]        | [Recent documents] |

**Key Finding:** [Observation about temporal distribution]

### Document Category Distribution

| Category | Count | Percentage | Examples |
|----------|-------|------------|----------|
| [Cat1]   | [N]   | [%]        | [Examples] |
| [Cat2]   | [N]   | [%]        | [Examples] |

### Confidence Score Distribution

| Level | Count | Percentage | Confidence Range |
|-------|-------|------------|------------------|
| High (≥0.9) | [N] | [%] | 0.90 - 1.00 |
| Medium (0.7-0.9) | [N] | [%] | 0.70 - 0.89 |
| Low (<0.7) | [N] | [%] | 0.50 - 0.69 |

**Critical Insight:** [Observation about confidence distribution]

### Complexity Distribution

| Complexity Level | Count | Percentage | Page Range |
|------------------|-------|------------|------------|
| Simple (1-2 pages) | [N] | [%] | 1-2 |
| Multi-page (3-9) | [N] | [%] | 3-9 |
| Complex (10+) | [N] | [%] | 10-[MAX] |
```

### Content Guidelines

**Purpose:** Paint picture of corpus composition

**Include:**
- Distribution tables with percentages
- Temporal span
- Category breakdown
- Complexity/confidence distributions

**Key insight for each distribution:**
- What does this tell us about the corpus?
- Any concerning patterns?

---

## Section 3: Sampling Methodology

### Template

```markdown
## Sampling Methodology

### Sampling Strategy

**Target Sample Size:** [N] documents ([%] of corpus)
**Actual Sample Size:** [M] documents
**Sampling Method:** Stratified random sampling

**Priority Criteria Applied:**

1. **ALL [N] LOW_CONF documents** (100% coverage of high-risk cases)
2. **ALL [N] COMPLEX documents** (100% coverage of 10+ page docs)
3. **[N] of [M] OLD_DOC** ([%] coverage of [time period] documents)
4. **[N] MULTI_PAGE documents** ([%] coverage of 3-9 page docs)
5. **Balanced representation** across categories and eras

**Sample Coverage:**

| Priority Tag | Population | Sampled | Coverage |
|--------------|------------|---------|----------|
| LOW_CONF     | [N]        | [M]     | [%]      |
| COMPLEX      | [N]        | [M]     | [%]      |
| OLD_DOC      | [N]        | [M]     | [%]      |
| MULTI_PAGE   | [N]        | [M]     | [%]      |

**Profile Distribution in Sample:**

| Profile | Corpus % | Sample % | Match? |
|---------|----------|----------|--------|
| [Name1] | [%]      | [%]      | [✓/✗]  |
| [Name2] | [%]      | [%]      | [✓/✗]  |

### Statistical Confidence

Sample size of [N] documents from a population of [M] provides:
- **Confidence Level:** [95/90]%
- **Margin of Error:** ±[X]% for proportions
- **Coverage of Critical Cases:** [100%/N%] (HIGH/LOW_CONF, COMPLEX documents)

**Assessment:** Sample is [representative/biased] with [high/medium/low] statistical confidence.
```

### Content Guidelines

**Purpose:** Justify sample composition and establish statistical rigor

**Key elements:**
- Sampling method explanation
- Priority criteria with coverage rates
- Comparison of sample vs. corpus distributions
- Statistical confidence calculations

---

## Section 4: Detailed Verification Results

### Template

```markdown
## Detailed Verification Results

### Overview

**Total Documents Verified:** [N]
**Verification Method:** Systematic side-by-side comparison using Claude vision analysis
**Verification Period:** [Date range]

### Example Verified Documents

#### Document 1: [Document Name]

**Document Profile:**
- **Pages:** [N]
- **Confidence:** [0.XX]
- **Category:** [Category]
- **Era:** [Era]
- **Priority Tags:** [Tag1, Tag2]
- **Sample Reason:** [Reason]

**Verification Results:**

| Quality Dimension          | Score | Details                                      |
|----------------------------|-------|----------------------------------------------|
| Metadata Accuracy          | [N]/10 | [Brief assessment]                          |
| Transcription Completeness | [N]/10 | [Brief assessment]                          |
| Transcription Accuracy     | [N]/10 | [Brief assessment]                          |
| Layout Preservation        | [N]/10 | [Brief assessment]                          |
| Domain Terminology         | [★★★★★] | [Excellent/Good/Fair/Poor]                |
| Summary Quality            | [N]/10 | [Brief assessment]                          |
| **Overall Score**          | **[N]/10** | **[Excellent/Good/Fair/Poor]**      |

**Key Findings:**

[Detailed paragraph describing what was verified and findings]

**Issues Identified:**
1. [Issue 1 with severity]
2. [Issue 2 with severity]

**Notable Strengths:**
- [Strength 1]
- [Strength 2]

[If LOW_CONF:]
**Low Confidence Investigation:**
- **Root Cause:** [What triggered low confidence]
- **Justified?:** [YES/NO - explanation]
- **Extraction Quality Despite Low Conf:** [Assessment]

---

[Repeat for 2-4 more representative examples]

### Verification Summary Table

| Document | Pages | Conf | Category | Overall Score | Issues |
|----------|-------|------|----------|---------------|--------|
| [Doc1]   | [N]   | [X]  | [Cat]    | [N]/10 ★★★★★ | [None/List] |
| [Doc2]   | [N]   | [X]  | [Cat]    | [N]/10 ★★★★  | [List] |
[...]
```

### Content Guidelines

**Show 3-5 detailed examples:**
- Include at least one LOW_CONF document
- Include at least one COMPLEX document
- Include at least one high-quality baseline
- Include at least one with issues (if any)

**For each example:**
- Full verification scores table
- Narrative description of findings
- Specific issues with examples
- Notable strengths

**Summary table:**
- All verified documents in compact table
- Sortable by score, category, complexity

---

## Section 5: Pattern Analysis

### Template

```markdown
## Pattern Analysis

### By Document Type/Category

**[Category 1] Documents:**
- Sample size: [N] documents
- Average quality: [X.X]/10
- Common issues: [List or "None identified"]
- Strengths: [List]

**[Category 2] Documents:**
- Sample size: [N] documents
- Average quality: [X.X]/10
- Common issues: [List or "None identified"]
- Strengths: [List]

**Assessment:** [Summary of category-based patterns]

### By Time Period/Era

**[Era 1] ([Years]):**
- Sample size: [N] documents
- Average quality: [X.X]/10
- Issues: [List or "None"]
- **Finding:** [Key observation]

**[Era 2] ([Years]):**
- Sample size: [N] documents
- Average quality: [X.X]/10
- Issues: [List or "None"]
- **Finding:** [Key observation]

**Assessment:** [Is there era-based quality variation?]

### By Complexity

**Simple (1-2 pages):**
- Average quality: [X.X]/10
- Issues: [List]

**Multi-page (3-9 pages):**
- Average quality: [X.X]/10
- Coherence issues: [List or "None"]

**Complex (10+ pages):**
- Average quality: [X.X]/10
- Coherence issues: [List or "None"]

**Assessment:** [Does complexity affect quality?]

### By Confidence Score

**High Confidence (≥0.9):**
- Verified: [N] documents
- Actual quality: [Average score]
- **Correlation:** [Strong/Weak - high confidence = high quality?]

**Low Confidence (<0.7):**
- Verified: [N] documents
- Root causes: [List with frequencies]
- Actual quality: [Average score]
- **Assessment:** [Is low confidence justified?]

**False Positives:** [N] documents (low conf but high quality)
**False Negatives:** [N] documents (high conf but low quality)

### Error Type Analysis

| Error Type | Count | Percentage | Examples |
|------------|-------|------------|----------|
| Critical (hallucinations, missing findings) | [N] | [%] | [Examples] |
| Major (wrong terms, wrong measurements) | [N] | [%] | [Examples] |
| Minor (spacing, case) | [N] | [%] | [Examples] |

**Error Rate:**
- Critical: [%]
- Major: [%]
- Minor: [%]

### Systematic Issues Identified

[If any systematic issues found:]

**Issue 1: [Issue Name]**
- **Frequency:** [N] documents ([%])
- **Affected categories:** [List]
- **Severity:** [Critical/Major/Minor]
- **Example:** [Specific example]
- **Recommended action:** [Action]

[Or if none:]

**No systematic issues identified.** Issues that occurred were isolated and non-repeating.
```

### Content Guidelines

**Purpose:** Identify patterns and correlations

**Key analyses:**
- Quality by category (which types problematic?)
- Quality by era (older docs worse?)
- Quality by complexity (coherence issues?)
- Confidence scoring reliability
- Error type frequencies

**For each dimension:**
- State sample size
- Provide average scores
- Identify patterns
- Assess significance

**Systematic issues:**
- Only flag issues appearing in 3+ documents
- Distinguish systematic from random errors

---

## Section 6: Quantitative Metrics

### Template

```markdown
## Quantitative Metrics

### Aggregate Scores from Verified Documents

| Quality Dimension            | Average Score | Range   | Grade    |
|------------------------------|---------------|---------|----------|
| Metadata Accuracy            | [X.X]/10      | [N-M]   | [A/B/C/D/F] |
| Transcription Completeness   | [X.X]/10      | [N-M]   | [A/B/C/D/F] |
| Transcription Accuracy       | [X.X]/10      | [N-M]   | [A/B/C/D/F] |
| Layout Preservation          | [X.X]/10      | [N-M]   | [A/B/C/D/F] |
| Domain Terminology           | [Rating]      | [Range] | [A/B/C/D/F] |
| Summary Quality              | [X.X]/10      | [N-M]   | [A/B/C/D/F] |
| **Overall Quality**          | **[X.X]/10**  | **[N-M]** | **[Grade]** |

### Error Rate Analysis

**Total Issues Found Across [N] Verified Documents:**

| Error Severity | Count | Rate | Examples |
|----------------|-------|------|----------|
| Critical       | [N]   | [%]  | [Examples] |
| Major          | [N]   | [%]  | [Examples] |
| Minor          | [N]   | [%]  | [Examples] |

**Acceptable Rates:**
- Critical: 0% (zero tolerance) → **[PASS/FAIL]**
- Major: <0.1% → **[PASS/FAIL]**
- Minor: <1% → **[PASS/FAIL]**

### Coverage Statistics

**Metadata Fields Extraction:**
- [Field1]: [%] accuracy
- [Field2]: [%] accuracy
- [Field3]: [%] accuracy

**Text Completeness:**
- Headers/titles: [%] captured
- Body text: [%] captured
- Measurements: [%] captured with units
- Signatures: [%] appropriately marked

### Distribution Statistics

[Charts or tables showing score distributions]

**Quality Score Distribution:**
- Excellent (9-10): [N] docs ([%])
- Good (7-8.9): [N] docs ([%])
- Fair (5-6.9): [N] docs ([%])
- Poor (<5): [N] docs ([%])
```

### Content Guidelines

**Purpose:** Provide quantitative evidence for quality assessment

**Include:**
- Aggregate score table (all dimensions)
- Error rate analysis with pass/fail
- Coverage statistics
- Score distributions

**Be precise:**
- Use exact numbers
- Show ranges
- Calculate percentages
- Compare to thresholds

---

## Section 7: Recommendations

### Template

```markdown
## Recommendations

### Production Readiness Assessment

| Criterion                        | Threshold | Actual  | Pass? |
|----------------------------------|-----------|---------|-------|
| Critical Error Rate              | <0.1%     | [%]     | [✓/✗] |
| Domain Term Accuracy             | >99%      | [%]     | [✓/✗] |
| Metadata Accuracy                | >95%      | [%]     | [✓/✗] |
| Summary Completeness             | >95%      | [%]     | [✓/✗] |
| Multi-page Coherence             | 100%      | [%]     | [✓/✗] |
| Overall Quality Score            | ≥7.0      | [X.X]   | [✓/✗] |

**Overall Assessment:** [✓ PRODUCTION READY / ⚠️ IMPROVEMENTS NEEDED / ✗ NOT READY]

### Immediate Actions

[If grade A or high B:]
**None Required** - The extraction pipeline demonstrates [excellent/good] quality.

[If grade C or below:]
**REQUIRED BEFORE PRODUCTION:**
1. [Critical action 1]
2. [Critical action 2]
3. [Critical action 3]

### Recommended Improvements

**Priority: HIGH**
1. **[Issue]:** [Description]
   - **Impact:** [Severity and scope]
   - **Recommendation:** [Specific action]
   - **Effort:** [Low/Medium/High]

**Priority: MEDIUM**
1. **[Issue]:** [Description]
   - **Impact:** [Severity and scope]
   - **Recommendation:** [Specific action]
   - **Effort:** [Low/Medium/High]

**Priority: LOW** (Optional Enhancements)
1. **[Enhancement]:** [Description]
   - **Benefit:** [What this improves]
   - **Effort:** [Low/Medium/High]

### Documents Requiring Reprocessing

[If any:]
**[N] documents recommended for reprocessing:**

| Document | Reason | Priority |
|----------|--------|----------|
| [Doc1]   | [Reason] | [High/Med/Low] |
| [Doc2]   | [Reason] | [High/Med/Low] |

**Reprocessing Actions:**
1. [Specific steps]

[If none:]
**None Identified** - All verified documents have acceptable quality.

### Configuration Tuning

**Current Configuration:**
- Extraction attempts (N): [N]
- Confidence threshold: [X]
- Model: [Model name]

**Recommendations:**
- [Keep as-is / Adjust X to Y because Z]

### Future Quality Monitoring

**Recommended Schedule:**
- **Quarterly:** Verify [N] random documents
- **On Prompt Changes:** Verify [N] documents before deployment
- **On Model Changes:** Comprehensive re-verification

**Monitoring Metrics:**
- Track confidence score distribution over time
- Monitor error rates by category
- Track processing time/cost

### Risk Assessment

| Risk                              | Probability | Impact   | Mitigation                    |
|-----------------------------------|-------------|----------|-------------------------------|
| [Risk 1]                          | [Low/Med/High] | [Low/Med/High] | [Mitigation strategy] |
| [Risk 2]                          | [Low/Med/High] | [Low/Med/High] | [Mitigation strategy] |

**Overall Risk Level:** [LOW/MEDIUM/HIGH]
```

### Content Guidelines

**Structure recommendations by:**
1. Production readiness (pass/fail)
2. Immediate actions (required)
3. Prioritized improvements (high/medium/low)
4. Reprocessing needs
5. Configuration tuning
6. Future monitoring

**Be specific:**
- What exactly needs to change?
- Why is it important?
- What's the effort level?
- What's the expected impact?

---

## Section 8: Appendices

### Template

```markdown
## Appendices

### A. Detailed Document Results

[Complete table of all verified documents]

| # | Document | Profile | Pages | Conf | Category | Metadata | Trans | Term | Summary | Overall | Issues |
|---|----------|---------|-------|------|----------|----------|-------|------|---------|---------|--------|
| 1 | [Doc1] | [Prof] | [N] | [X] | [Cat] | [10] | [9.3] | [★★★★★] | [10] | [9.4] | [None] |
| 2 | [Doc2] | [Prof] | [N] | [X] | [Cat] | [10] | [8.7] | [★★★★] | [9] | [9.0] | [Minor] |
[...]

### B. Statistical Confidence

**Sample Size Justification:**
- Population: [N] documents
- Sample: [M] documents ([%] of population)
- Deeply Verified: [K] documents

**Coverage of Priority Cases:**
- LOW_CONF: [%] coverage
- COMPLEX: [%] coverage
- OLD_DOC: [%] coverage

**Statistical Significance:**

Given:
- [Low/Medium/High] error rate in verified samples
- [%] HIGH_CONF rate in population
- [%] coverage of problematic cases

**Confidence Level:** >[95/90]% that overall extraction quality is [GRADE] across entire corpus.

### C. Methodology Reference

This quality assessment used:

1. **Stratified Random Sampling** for representative document selection
   - See: `references/sampling_methodology.md`

2. **Systematic Verification** with standardized checklist
   - See: `references/verification_checklist.md`

3. **Multi-dimensional Quality Scoring** (0-10 scale)
   - Metadata accuracy
   - Transcription quality (completeness, accuracy, layout)
   - Domain-specific terminology
   - Summary quality
   - Multi-page coherence

4. **Pattern Analysis** across:
   - Document types/categories
   - Time periods/eras
   - Complexity levels
   - Confidence score ranges

### D. Verification Timeline

| Phase | Date | Duration | Outcome |
|-------|------|----------|---------|
| Inventory Generation | [Date] | [Time] | [N] documents cataloged |
| Stratified Sampling | [Date] | [Time] | [M] documents sampled |
| Systematic Verification | [Date range] | [Time] | [K] documents verified |
| Pattern Analysis | [Date] | [Time] | [Findings] |
| Report Generation | [Date] | [Time] | This report |

### E. Glossary

**Key Terms:**
- **Confidence Score:** Self-consistency voting agreement (0-1 scale)
- **Stratified Sampling:** Sampling method ensuring representation of subgroups
- **Priority Tags:** Flags identifying high-risk documents for sampling
- **Critical Error:** Error affecting clinical/legal/financial outcomes
- **Major Error:** Significant error not affecting outcomes
- **Minor Error:** Negligible error (spacing, case)

### F. Contact and Follow-up

**For questions about this report:**
- Review methodology: `references/verification_checklist.md`
- Review sampling: `references/sampling_methodology.md`
- Domain guide: `references/[domain]_terminology_guide.md`

**For follow-up investigations:**
- Access verification results: `verification_results.json`
- Access sample data: `sample.json`
- Access inventory: `inventory.json`

---

**Report End**

*Generated by extraction-quality-audit skill*
*Report Version: 1.0*
*Date: [YYYY-MM-DD]*
```

---

## Report Quality Checklist

Before finalizing report, verify:

- [ ] Executive summary is concise (1-2 pages max)
- [ ] Quality grade clearly stated multiple times
- [ ] All tables have clear headers
- [ ] Percentages calculated correctly
- [ ] Examples are concrete and specific
- [ ] Recommendations are actionable
- [ ] Statistical confidence is justified
- [ ] No jargon without explanation
- [ ] Consistent terminology throughout
- [ ] Grammar and spelling checked
- [ ] All sections linked logically
- [ ] Appendices referenced where appropriate

---

## Customization for Domains

**Medical reports:**
- Emphasize patient safety and clinical accuracy
- Include accent preservation statistics
- Detail anatomical terminology verification

**Legal reports:**
- Emphasize accuracy of case citations and dates
- Detail contract clause preservation
- Include jurisdiction-specific requirements

**Financial reports:**
- Emphasize numerical accuracy
- Detail currency handling
- Include audit trail requirements

**Technical reports:**
- Emphasize code syntax preservation
- Detail API reference accuracy
- Include version control considerations

---

## Version History

- **v1.0** (2026-01-21): Initial template based on medical-exams-parser quality report
