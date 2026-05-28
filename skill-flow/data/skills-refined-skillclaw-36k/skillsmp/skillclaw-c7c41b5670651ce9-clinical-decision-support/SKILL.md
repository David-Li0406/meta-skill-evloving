---
name: clinical-decision-support
description: Use this skill to generate professional clinical decision support (CDS) documents for pharmaceutical and clinical research settings, including patient cohort analyses and treatment recommendation reports.
---

# Clinical Decision Support Documents

## Description

Generate professional clinical decision support (CDS) documents for pharmaceutical companies, clinical researchers, and medical decision-makers. This skill specializes in analytical, evidence-based documents that inform treatment strategies and drug development:

1. **Patient Cohort Analysis** - Biomarker-stratified group analyses with statistical outcome comparisons.
2. **Treatment Recommendation Reports** - Evidence-based clinical guidelines with GRADE grading and decision algorithms.

All documents are generated as publication-ready LaTeX/PDF files optimized for pharmaceutical research, regulatory submissions, and clinical guideline development.

**Note:** For individual patient treatment plans at the bedside, use the `treatment-plans` skill instead. This skill focuses on group-level analyses and evidence synthesis for pharmaceutical/research settings.

**Writing Style:** For publication-ready documents targeting medical journals, consult the **venue-templates** skill's `medical_journal_styles.md` for guidance on structured abstracts, evidence language, and CONSORT/STROBE compliance.

## Capabilities

### Document Types

**Patient Cohort Analysis**
- Biomarker-based patient stratification (molecular subtypes, gene expression, IHC).
- Outcome metrics with statistical analysis (OS, PFS, ORR, DOR, DCR).
- Statistical comparisons between subgroups (hazard ratios, p-values, 95% CI).
- Survival analysis with Kaplan-Meier curves and log-rank tests.
- Efficacy tables and waterfall plots.
- Comparative effectiveness analyses.
- Pharmaceutical cohort reporting (trial subgroups, real-world evidence).

**Treatment Recommendation Reports**
- Evidence-based treatment guidelines for specific disease states.
- Strength of recommendation grading (GRADE system: 1A, 1B, 2A, 2B, 2C).
- Quality of evidence assessment (high, moderate, low, very low).
- Treatment algorithm flowcharts with TikZ diagrams.