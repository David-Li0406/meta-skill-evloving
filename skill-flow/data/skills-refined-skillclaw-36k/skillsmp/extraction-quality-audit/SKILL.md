---
name: extraction-quality-audit
description: Comprehensive quality assessment for document extraction pipelines. Use when (1) After implementing extraction pipeline, (2) Before production deployment, (3) Periodic quality audits, (4) Investigating suspected quality issues, (5) Validating pipeline changes, (6) Benchmarking extraction accuracy across document types/eras. Performs stratified sampling, systematic verification, pattern analysis, and generates detailed quality reports.
---

# Extraction Quality Audit

## Overview

This skill performs comprehensive quality assessment of document extraction pipelines through stratified sampling, systematic verification, pattern analysis, and detailed quality reporting.

**Use this skill when:**
- After implementing or modifying an extraction pipeline
- Before production deployment of document processing systems
- Conducting periodic quality audits (quarterly/annual)
- Investigating suspected quality issues or accuracy concerns
- Validating prompt modifications or model changes
- Benchmarking extraction accuracy across document types or time periods
- Evaluating LLM-based document processing systems

**Prerequisites:**
- Extraction pipeline outputs exist (structured files with metadata)
- Source documents available for comparison
- Claude has vision access for document comparison
- Output files contain metadata (YAML frontmatter, JSON, or similar)

**Expected Time:**
- Phase 1 (Inventory): 5-10 minutes
- Phase 2 (Sampling): 2-5 minutes
- Phase 3 (Verification): 2-4 hours for 25-30 documents
- Phase 4 (Analysis): 15-30 minutes
- Phase 5 (Report): 5-10 minutes

## Quick Start

```bash
# 1. Configure paths in generate_inventory.py
python ~/.claude/skills/extraction-quality-audit/scripts/generate_inventory.py \
  --input-dir /path/to/source/documents \
  --output-dir /path/to/extraction/outputs \
  --profile-name your_profile

# 2. Run stratified sampling
python ~/.claude/skills/extraction-quality-audit/scripts/stratified_sampling.py \
  --inventory inventory.json \
  --target-size 30

# 3. Perform systematic verification (interactive with Claude)
python ~/.claude/skills/extraction-quality-audit/scripts/verification_framework.py \
  --sample sample.json

# 4. Generate comprehensive report
python ~/.claude/skills/extraction-quality-audit/scripts/report_generator.py \
  --inventory inventory.json \
  --sample sample.json \
  --results verification_results.json \
  --output QUALITY_REPORT.md
```

## Phase 1: Document Inventory

**Purpose:** Create a comprehensive catalog of all processed documents with metadata for sampling.

**What it does:**
- Scans output directory for all extraction results
- Extracts metadata from each document (dates, categories, confidence scores, page counts)
- Classifies documents by complexity, era, and characteristics
- Tags documents with priority markers for sampling
- Outputs structured JSON inventory

**Script:** `scripts/generate_inventory.py`

**Usage:**
```bash
python scripts/generate_inventory.py \
  --input-dir /path/to/source/docs \
  --output-dir /path/to/extraction/outputs \
  --profile-name profile_name \
  --output inventory.json
```

**Configuration Options:**
- `--input-dir`: Directory containing source documents (PDFs, images, etc.)
- `--output-dir`: Directory containing extraction outputs (markdown, JSON, etc.)
- `--profile-name`: Profile or category name for this document set
- `--output`: Output filename (default: inventory.json)
- `--metadata-format`: Format of metadata (yaml, json, frontmatter)

**Output Structure:**
```json
[
  {
    "profile": "profile_name",
    "doc_stem": "document_name",
    "doc_dir": "/path/to/output/dir",
    "page_count": 3,
    "has_summary": true,
    "confidence_scores": [0.95, 0.89, 0.92],
    "min_confidence": 0.89,
    "max_confidence": 0.95,
    "avg_confidence": 0.92,
    "date": "2024-01-15",
    "category": "imaging",
    "era": "2020s",
    "tags": ["CAT_IMAGING", "MULTI_PAGE"]
  }
]
```

**Default Priority Tags:**
- `LOW_CONF`: Minimum confidence < 0.7
- `OLD_DOC`: Documents from 1990s-2000s (configurable)
- `COMPLEX`: 10+ pages
- `MULTI_PAGE`: 3-9 pages
- `CAT_[CATEGORY]`: Document category tags

**Customization:** Edit tag definitions in `generate_inventory.py` configuration section.

**Reference:** See `references/sampling_methodology.md` for detailed tag design rationale.

## Phase 2: Stratified Sampling

**Purpose:** Select a representative sample of documents for deep verification using stratified random sampling.

**What it does:**
- Applies priority-based stratified sampling across multiple dimensions
- Ensures coverage of high-risk categories (low confidence, complex, old)
- Balances representation across document types, eras, and categories
- Provides sampling justification for each selected document
- Outputs sample with selection reasons

**Script:** `scripts/stratified_sampling.py`

**Usage:**
```bash
python scripts/stratified_sampling.py \
  --inventory inventory.json \
  --target-size 30 \
  --config sampling_config.json \
  --output sample.json
```

**Sampling Strategy:**

1. **100% coverage of critical cases:**
   - All LOW_CONF documents (highest priority)
   - All COMPLEX documents (10+ pages)

2. **High coverage of challenging cases:**
   - 60-80% of OLD_DOC (older documents)
   - 40-60% of MULTI_PAGE (3-9 pages)

3. **Balanced representation:**
   - Proportional sampling across categories
   - Era diversity (cover all time periods)
   - Profile/user distribution matching corpus

4. **Random fill:**
   - Remaining slots filled randomly to reach target size

**Target Sample Size:**
- **Minimum:** 25-30 documents for statistical significance
- **Large corpora (>500):** 50-75 documents
- **Very large (>1000):** 100+ documents

**Customizing Sampling:**

Edit `sampling_config.json`:
```json
{
  "priority_tags": {
    "LOW_CONF": {"coverage": 1.0, "priority": 1000},
    "COMPLEX": {"coverage": 1.0, "priority": 100},
    "OLD_DOC": {"coverage": 0.7, "priority": 10},
    "MULTI_PAGE": {"coverage": 0.4, "priority": 1}
  },
  "random_seed": 42
}
```

**Reference:** See `references/sampling_methodology.md` for stratified sampling theory and best practices.

## Phase 3: Systematic Verification

**Purpose:** Deep quality assessment of sampled documents through side-by-side comparison of source and extraction.

**What it does:**
- Presents verification checklist for each sampled document
- Loads source documents and extraction outputs
- Guides systematic comparison across quality dimensions
- Tracks verification progress
- Saves detailed scoring and findings incrementally

**Script:** `scripts/verification_framework.py`

**Usage:**
```bash
python scripts/verification_framework.py \
  --sample sample.json \
  --results verification_results.json
```

**Verification Workflow:**

For each document in sample:

1. **Load Files:**
   - Read source document (PDF, image, etc.) using Claude's vision
   - Read all extraction output files (pages, summaries)

2. **Verify Metadata Accuracy (Score 0-10):**
   - Date correctness
   - Document title/name accuracy
   - Category classification
   - Facility, doctor, department names
   - Other structured fields

3. **Verify Transcription Quality (Score 0-10):**
   - **Completeness:** All text captured? (Score 0-10)
   - **Accuracy:** Text matches source? (Score 0-10)
   - **Layout:** Structure preserved? (Score 0-10)
   - Document specific issues

4. **Verify Domain-Specific Terminology:**
   - Medical: Anatomical terms, diagnostic phrases, measurements
   - Legal: Contract clauses, case citations, legal entities
   - Financial: Accounting terms, currency handling
   - Technical: Code snippets, API references, formulas
   - **Rating:** Excellent/Good/Fair/Poor

5. **Verify Summary Quality (Score 0-10):**
   - Completeness of key information
   - Accuracy of summary content
   - Appropriate level of detail
   - No hallucinations

6. **Multi-Page Coherence (for multi-page docs):**
   - Metadata consistency across pages
   - Page numbering accuracy
   - No duplicate content
   - Cross-page references preserved

7. **Low Confidence Investigation (for LOW_CONF docs):**
   - Identify root cause of low confidence
   - Assess if confidence is justified
   - Determine if extraction quality is still acceptable

**Verification Template:**
```json
{
  "doc_stem": "document_name",
  "metadata_accuracy": {
    "score": 10,
    "issues": []
  },
  "transcription_quality": {
    "completeness_score": 10,
    "accuracy_score": 10,
    "layout_preservation_score": 9,
    "overall_score": 9.7,
    "issues": ["Minor spacing variation"]
  },
  "domain_terminology": {
    "rating": "Excellent",
    "issues": []
  },
  "summary_quality": {
    "score": 10,
    "issues": []
  },
  "overall_assessment": "Excellent",
  "notable_issues": [],
  "recommendations": [],
  "verified_date": "2026-01-21"
}
```

**Progress Tracking:**

The framework saves results incrementally, allowing you to:
- Pause and resume verification
- Track how many documents remain
- Review completed verifications

**Reference:** See `references/verification_checklist.md` for detailed verification steps and scoring rubrics.

## Phase 4: Pattern Analysis

**Purpose:** Aggregate findings across all verified documents to identify systematic issues and quality patterns.

**What it does:**
- Analyzes verification results to find patterns
- Identifies issues by document type, era, complexity, confidence level
- Calculates aggregate quality metrics
- Correlates confidence scores with actual quality
- Detects systematic vs. random errors

**Analysis Dimensions:**

1. **By Document Type/Category:**
   - Which categories have lower quality?
   - Are specific document types problematic?

2. **By Time Period/Era:**
   - Do older documents have quality issues?
   - Are recent documents better?

3. **By Complexity:**
   - Do multi-page documents have coherence issues?
   - Are simple documents more accurate?

4. **By Confidence Score:**
   - Do low confidence docs have poor quality?
   - Are there false positives/negatives in confidence?

5. **Error Type Analysis:**
   - What types of errors occur most frequently?
   - Are errors systematic (same issue across docs) or random?

**Interactive Analysis with Claude:**

This phase is typically performed interactively with Claude:

```
User: "Analyze the verification results and identify any patterns"

Claude will:
- Load inventory.json, sample.json, verification_results.json
- Compute aggregate statistics
- Identify correlations
- Report systematic issues
- Provide visualizations (ASCII tables, markdown)
```

**Key Metrics to Calculate:**

- Overall average quality scores by dimension
- Error rates (critical, major, minor)
- Confidence score reliability (true positive rate)
- Quality distribution by category/era/complexity
- Metadata extraction accuracy rate
- Summary quality consistency

## Phase 5: Report Generation

**Purpose:** Generate comprehensive markdown report with findings, recommendations, and supporting data.

**Script:** `scripts/report_generator.py`

**Usage:**
```bash
python scripts/report_generator.py \
  --inventory inventory.json \
  --sample sample.json \
  --results verification_results.json \
  --output QUALITY_REPORT.md
```

**Report Structure:**

1. **Executive Summary:**
   - Key findings (3-5 bullet points)
   - Overall quality grade (A/B/C/D/F)
   - Critical issues requiring immediate action
   - Confidence score assessment

2. **Data Landscape:**
   - Corpus statistics (total docs, profiles, categories)
   - Temporal distribution (eras)
   - Confidence score distribution
   - Complexity distribution

3. **Sampling Methodology:**
   - Sample size justification
   - Priority criteria applied
   - Coverage statistics

4. **Detailed Verification Results:**
   - Per-document findings for key examples
   - Quality scores by dimension
   - Notable issues and patterns

5. **Systematic Pattern Analysis:**
   - Issues by category, era, complexity
   - Confidence scoring reliability
   - Error rate analysis

6. **Quantitative Metrics:**
   - Aggregate scores table
   - Error rates by severity
   - Coverage statistics

7. **Recommendations:**
   - Immediate actions required
   - Optional enhancements (priority ranked)
   - Documents requiring reprocessing
   - Configuration tuning suggestions

8. **Appendices:**
   - Detailed document results table
   - Statistical confidence calculations
   - Reference to detailed verification data

**Template:** See `references/report_template.md` for complete report structure.

## Customization

### Domain-Specific Verification

The skill is designed to work with ANY document extraction pipeline. For domain-specific verification:

**Medical Documents:**
- Use `references/medical_terminology_guide.md`
- Verify accent preservation (Portuguese, Spanish, etc.)
- Check anatomical terms, measurements, diagnostic phrases

**Legal Documents:**
Create `references/legal_terminology_guide.md`:
- Contract clauses and provisions
- Case law citations (e.g., "Brown v. Board of Education, 347 U.S. 483")
- Legal entities and jurisdictions
- Dates and monetary amounts

**Financial Documents:**
Create `references/financial_terminology_guide.md`:
- Accounting terms (GAAP, EBITDA, etc.)
- Currency handling and precision
- Numerical accuracy (percentages, decimals)
- Financial formulas and calculations

**Scientific Documents:**
Create `references/scientific_terminology_guide.md`:
- Chemical formulas (H₂O, CO₂, etc.)
- Mathematical equations
- Scientific notation
- Citations and references

**Technical Documents:**
Create `references/technical_terminology_guide.md`:
- Code snippets and syntax
- API references and URLs
- Technical specifications
- Version numbers

### Custom Priority Tags

Edit `generate_inventory.py` to add custom tags:

```python
# Define custom priority tags
PRIORITY_TAGS = {
    'LOW_CONF': lambda doc: doc['min_confidence'] < 0.7,
    'OLD_DOC': lambda doc: doc.get('era') in ['1990s', '2000s'],
    'COMPLEX': lambda doc: doc['page_count'] >= 10,
    'MULTI_PAGE': lambda doc: 3 <= doc['page_count'] < 10,

    # Add custom tags
    'HAS_IMAGES': lambda doc: doc.get('has_images', False),
    'HANDWRITTEN': lambda doc: 'handwritten' in doc.get('tags', []),
    'LONG_TEXT': lambda doc: doc.get('word_count', 0) > 5000,
}
```

### Adjusting Sample Size

For different corpus sizes:

- **Small (<100 docs):** 25-30 documents (25-30% coverage)
- **Medium (100-500):** 30-50 documents (10-20% coverage)
- **Large (500-1000):** 50-75 documents (5-10% coverage)
- **Very large (>1000):** 100+ documents (5% coverage)

Always ensure 100% coverage of critical cases (LOW_CONF, COMPLEX).

## Expected Outputs

**Files Generated:**

1. **inventory.json:** Complete document catalog with metadata
2. **sample.json:** Selected documents with sampling justification
3. **verification_results.json:** Detailed verification scores and findings
4. **QUALITY_REPORT.md:** Comprehensive quality assessment report

**Report Deliverables:**

- Executive summary with actionable recommendations
- Quality grade (A through F)
- Quantitative metrics and aggregate scores
- Systematic issue identification
- Documents requiring reprocessing (if any)
- Configuration tuning recommendations

## Interpretation Guide

### Quality Grades

- **A (9-10):** Excellent, production-ready quality
- **B (7-8.9):** Good, minor improvements recommended
- **C (5-6.9):** Fair, significant improvements needed before production
- **D (3-4.9):** Poor, major issues require immediate attention
- **F (<3):** Failing, unsuitable for production use

### Confidence Score Interpretation

**Important:** Low confidence does NOT necessarily mean poor quality.

- **HIGH_CONF (≥0.9):** Standard content, consistent extraction
- **MED_CONF (0.7-0.9):** Some variation in extraction attempts
- **LOW_CONF (<0.7):** Challenging content (images, handwriting, complex layouts)

**Low confidence may indicate:**
- Image-heavy pages (legitimate uncertainty about visual content)
- Handwritten text (inherent ambiguity in interpretation)
- Complex layouts (inconsistent extraction across attempts)
- Very long documents (more opportunities for variation)

**Verify that:**
- LOW_CONF documents are appropriately flagged
- Extraction quality is acceptable despite low confidence
- No HIGH_CONF documents with poor quality (false negatives)

### Error Severity Classification

- **Critical:** Missing clinical/legal findings, hallucinations, wrong patient/party names
- **Major:** Incorrect technical terms, wrong measurements/amounts, incorrect dates
- **Minor:** Spacing variations, case inconsistencies, handwriting uncertainty

**Acceptable Error Rates:**
- Critical: 0% (zero tolerance)
- Major: <0.1% (near-zero tolerance)
- Minor: <1% (acceptable for production)

## Troubleshooting

**Issue:** Inventory generation fails with encoding errors

**Solution:** Specify encoding in script configuration:
```python
with open(file, 'r', encoding='utf-8') as f:
```

**Issue:** Can't find source documents for verification

**Solution:** Update path mapping in `verification_framework.py`:
```python
def get_document_paths(doc: Dict) -> Dict[str, Path]:
    # Update this function with your directory structure
```

**Issue:** Sample is too small or unrepresentative

**Solution:**
- Increase `--target-size` parameter
- Adjust priority tag coverage in sampling config
- Add custom tags for under-represented document types

**Issue:** Verification taking too long

**Solution:**
- Reduce sample size for initial audit
- Focus verification on highest priority documents only
- Use parallel verification (multiple Claude sessions)

**Issue:** Report generation fails

**Solution:**
- Ensure all input files exist (inventory, sample, results)
- Check JSON format validity
- Verify template file exists in references/

## Best Practices

1. **Run inventory immediately after extraction pipeline completes** to capture fresh metadata

2. **Always include 100% of LOW_CONF and COMPLEX documents** in sample for comprehensive risk assessment

3. **Verify documents interactively with Claude vision** for highest accuracy in quality assessment

4. **Save verification results incrementally** to avoid losing progress

5. **Focus on systematic patterns** rather than individual document issues

6. **Re-run audit after significant pipeline changes** (prompt modifications, model changes, configuration updates)

7. **Document domain-specific terminology guides** for consistent verification across audits

8. **Track quality trends over time** by comparing reports from multiple audit runs

## Limitations

- Requires Claude vision access for source document comparison
- Verification phase is time-intensive (manual review required)
- Statistical confidence depends on sample size
- Domain-specific terminology verification requires expertise
- Not suitable for real-time quality monitoring (batch assessment only)

## Integration with CI/CD

For automated quality audits in CI/CD pipelines:

```yaml
# .github/workflows/quality-audit.yml
name: Quality Audit
on:
  schedule:
    - cron: '0 0 1 * *'  # Monthly

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - name: Generate Inventory
        run: python scripts/generate_inventory.py ...

      - name: Run Sampling
        run: python scripts/stratified_sampling.py ...

      - name: Trigger Manual Verification
        uses: peter-evans/create-issue-from-file@v4
        with:
          title: Monthly Quality Audit Required
          content-filepath: verification_checklist.md
```

Note: Verification phase requires human review and cannot be fully automated.

## References

- **Sampling Methodology:** `references/sampling_methodology.md`
- **Verification Checklist:** `references/verification_checklist.md`
- **Medical Terminology Guide:** `references/medical_terminology_guide.md`
- **Report Template:** `references/report_template.md`

## Version History

- **v1.0:** Initial release (2026-01-21)
  - Full 5-phase quality audit workflow
  - Stratified sampling implementation
  - Domain-agnostic design with medical example
  - Comprehensive report generation

## Support

For issues or questions:
- Check `references/` directory for detailed guidance
- Review example outputs in skill directory
- Consult QUALITY_INVESTIGATION_REPORT.md for reference implementation

## License

This skill is part of the Claude Code skills ecosystem and is provided as-is for quality assessment of document extraction pipelines.
