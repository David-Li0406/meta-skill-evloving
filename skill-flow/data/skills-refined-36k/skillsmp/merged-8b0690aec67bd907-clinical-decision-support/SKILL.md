---
name: clinical-decision-support
description: Generate professional clinical decision support (CDS) documents for pharmaceutical and clinical research settings, including patient cohort analyses and treatment recommendation reports. This skill supports GRADE evidence grading, statistical analysis, biomarker integration, and regulatory compliance, producing publication-ready LaTeX/PDF documents optimized for drug development and clinical research.
---

# Clinical Decision Support Documents

## Description

Generate professional clinical decision support (CDS) documents for pharmaceutical companies, clinical researchers, and medical decision-makers. This skill specializes in analytical, evidence-based documents that inform treatment strategies and drug development:

1. **Patient Cohort Analysis** - Biomarker-stratified group analyses with statistical outcome comparisons.
2. **Treatment Recommendation Reports** - Evidence-based clinical guidelines with GRADE grading and decision algorithms.

All documents are generated as publication-ready LaTeX/PDF files optimized for pharmaceutical research, regulatory submissions, and clinical guideline development.

**Note:** For individual patient treatment plans at the bedside, use the `treatment-plans` skill instead. This skill focuses on group-level analyses and evidence synthesis for pharmaceutical/research settings.

## Capabilities

### Document Types

**Patient Cohort Analysis**
- Biomarker-based patient stratification (molecular subtypes, gene expression, IHC).
- Outcome metrics with statistical analysis (OS, PFS, ORR, DOR, DCR).
- Statistical comparisons between subgroups (hazard ratios, p-values, 95% CI).
- Survival analysis with Kaplan-Meier curves and log-rank tests.
- Efficacy tables and waterfall plots.
- Comparative effectiveness analyses.

**Treatment Recommendation Reports**
- Evidence-based treatment guidelines for specific disease states.
- Strength of recommendation grading (GRADE system: 1A, 1B, 2A, 2B, 2C).
- Quality of evidence assessment (high, moderate, low, very low).
- Treatment algorithm flowcharts with TikZ diagrams.
- Decision pathways with clinical and molecular criteria.

### Clinical Features

- **Biomarker Integration**: Genomic alterations (mutations, CNV, fusions), gene expression signatures, IHC markers.
- **Statistical Analysis**: Hazard ratios, p-values, confidence intervals, survival curves.
- **Evidence Grading**: GRADE system (1A/1B/2A/2B/2C), quality of evidence assessment.
- **Regulatory Compliance**: HIPAA de-identification, confidentiality headers, ICH-GCP alignment.
- **Professional Formatting**: Compact 0.5in margins, color-coded recommendations, publication-ready.

## Pharmaceutical and Research Use Cases

This skill is specifically designed for pharmaceutical and clinical research applications:

**Drug Development**
- Phase 2/3 Trial Analyses: Biomarker-stratified efficacy and safety analyses.
- Regulatory Submissions: IND/NDA documentation with evidence summaries.

**Medical Affairs**
- KOL Education Materials: Evidence-based treatment algorithms for thought leaders.
- Publication Planning: Manuscript-ready analyses for peer-reviewed journals.

**Clinical Guidelines**
- Guideline Development: Evidence synthesis with GRADE methodology for specialty societies.

**Real-World Evidence**
- RWE Cohort Studies: Retrospective analyses of patient cohorts from EMR data.

## When to Use

Use this skill when you need to:

- Analyze patient cohorts stratified by biomarkers or clinical characteristics.
- Generate treatment recommendation reports with evidence grading.
- Compare outcomes between patient subgroups with statistical analysis.
- Produce pharmaceutical research documents for drug development or regulatory submissions.
- Develop clinical practice guidelines with GRADE evidence grading.

**Do NOT use this skill for:**
- Individual patient treatment plans (use `treatment-plans` skill).
- Bedside clinical care documentation (use `treatment-plans` skill).

## Visual Enhancement with Scientific Schematics

**⚠️ MANDATORY: Every clinical decision support document MUST include at least 1-2 AI-generated figures.**

Before finalizing any document:
1. Generate at minimum ONE schematic or diagram (e.g., clinical decision algorithm, treatment pathway).
2. For cohort analyses: include patient flow diagram.
3. For treatment recommendations: include decision flowchart.

**How to generate figures:**
- Use the **scientific-schematics** skill to generate AI-powered publication-quality diagrams.

## Document Structure

**CRITICAL REQUIREMENT: All clinical decision support documents MUST begin with a complete executive summary on page 1.**

### Page 1 Executive Summary Structure

The first page of every CDS document should contain ONLY the executive summary with the following components:

1. **Document Title and Type**
2. **Report Information Box** (using colored tcolorbox)
3. **Key Findings Boxes** (3-5 colored boxes using tcolorbox)

**Visual Requirements:**
- Use `\thispagestyle{empty}` to remove page numbers from page 1.
- All content must fit on page 1 (before `\newpage`).

### Detailed Sections (Page 3+)
- **Cohort Characteristics**: Demographics, baseline features.
- **Biomarker Stratification**: Molecular subtypes, genomic alterations.
- **Outcome Analysis**: Response rates, survival data.
- **Statistical Methods**: Kaplan-Meier survival curves, hazard ratios.
- **Clinical Recommendations**: Treatment implications based on biomarker profiles.

## Output Format

**MANDATORY FIRST PAGE REQUIREMENT:**
- **Page 1**: Full-page executive summary with 3-5 colored tcolorbox elements.
- **Page 2**: Table of contents (optional).
- **Page 3+**: Detailed sections with methods, results, figures, tables.

## Integration

This skill integrates with:
- **scientific-writing**: Citation management, statistical reporting.
- **clinical-reports**: Medical terminology, regulatory documentation.
- **scientific-schematics**: TikZ flowcharts for decision algorithms.

## Key Differentiators from Treatment-Plans Skill

**Clinical Decision Support (this skill):**
- Audience: Pharmaceutical companies, clinical researchers.
- Scope: Population-level analyses, evidence synthesis.
- Output: Multi-page analytical documents (5-15 pages typical).

**Treatment-Plans Skill:**
- Audience: Clinicians, patients.
- Scope: Individual patient care planning.
- Output: Concise 1-4 page actionable care plans.

## Example Usage

### Patient Cohort Analysis
**Example 1: NSCLC Biomarker Stratification**
```
> Analyze a cohort of 45 NSCLC patients stratified by PD-L1 expression.
```

### Treatment Recommendation Report
**Example 1: HER2+ Metastatic Breast Cancer Guidelines**
```
> Create evidence-based treatment recommendations for HER2-positive metastatic breast cancer.
```

## Best Practices

1. **Patient Selection Transparency**: Clearly document inclusion/exclusion criteria.
2. **Biomarker Clarity**: Specify assay methods and validation status.
3. **Statistical Rigor**: Report hazard ratios with 95% confidence intervals.
4. **De-identification**: Remove all 18 HIPAA identifiers before document generation.

## References

See the `references/` directory for detailed guidance on:
- Patient cohort analysis and stratification methods.
- Treatment recommendation development.
- Clinical decision algorithms.

## Templates

See the `assets/` directory for LaTeX templates:
- `cohort_analysis_template.tex`
- `treatment_recommendation_template.tex`

## Scripts

See the `scripts/` directory for analysis and visualization tools:
- `generate_survival_analysis.py`
- `create_waterfall_plot.py`