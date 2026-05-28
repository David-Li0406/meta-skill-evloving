---
name: clinical-decision-support
description: Generate professional clinical decision support (CDS) documents for pharmaceutical and clinical research settings, including patient cohort analyses (biomarker-stratified with outcomes) and treatment recommendation reports (evidence-based guidelines with decision algorithms). Supports GRADE evidence grading, statistical analysis (hazard ratios, survival curves, waterfall plots), biomarker integration, and regulatory compliance. Outputs publication-ready LaTeX/PDF format optimized for drug development, clinical research, and evidence synthesis.
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
- Molecular subtype classification (e.g., GBM mesenchymal-immune-active vs proneural, breast cancer subtypes).
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
- Line-of-therapy sequencing based on biomarkers.
- Decision pathways with clinical and molecular criteria.
- Pharmaceutical strategy documents.
- Clinical guideline development for medical societies.

### Clinical Features

- **Biomarker Integration**: Genomic alterations (mutations, CNV, fusions), gene expression signatures, IHC markers, PD-L1 scoring.
- **Statistical Analysis**: Hazard ratios, p-values, confidence intervals, survival curves, Cox regression, log-rank tests.
- **Evidence Grading**: GRADE system (1A/1B/2A/2B/2C), Oxford CEBM levels, quality of evidence assessment.
- **Clinical Terminology**: SNOMED-CT, LOINC, proper medical nomenclature, trial nomenclature.
- **Regulatory Compliance**: HIPAA de-identification, confidentiality headers, ICH-GCP alignment.
- **Professional Formatting**: Compact 0.5in margins, color-coded recommendations, publication-ready, suitable for regulatory submissions.

## Pharmaceutical and Research Use Cases

This skill is specifically designed for pharmaceutical and clinical research applications:

**Drug Development**
- **Phase 2/3 Trial Analyses**: Biomarker-stratified efficacy and safety analyses.
- **Subgroup Analyses**: Forest plots showing treatment effects across patient subgroups.
- **Companion Diagnostic Development**: Linking biomarkers to drug response.
- **Regulatory Submissions**: IND/NDA documentation with evidence summaries.

**Medical Affairs**
- **KOL Education Materials**: Evidence-based treatment algorithms for thought leaders.
- **Medical Strategy Documents**: Competitive landscape and positioning strategies.
- **Advisory Board Materials**: Cohort analyses and treatment recommendation frameworks.
- **Publication Planning**: Manuscript-ready analyses for peer-reviewed journals.

**Clinical Guidelines**
- **Guideline Development**: Evidence synthesis with GRADE methodology for specialty societies.
- **Consensus Recommendations**: Multi-stakeholder treatment algorithm development.
- **Practice Standards**: Biomarker-based treatment selection criteria.
- **Quality Measures**: Evidence-based performance metrics.

**Real-World Evidence**
- **RWE Cohort Studies**: Retrospective analyses of patient cohorts from EMR data.
- **Comparative Effectiveness**: Head-to-head treatment comparisons in real-world settings.
- **Outcomes Research**: Long-term survival and safety in clinical practice.
- **Health Economics**: Cost-effectiveness analyses by biomarker subgroup.

## When to Use

Use this skill when you need to:

- **Analyze patient cohorts** stratified by biomarkers, molecular subtypes, or clinical characteristics.
- **Generate treatment recommendation reports** with evidence grading for clinical guidelines or pharmaceutical strategies.
- **Compare outcomes** between patient subgroups with statistical analysis (survival, response rates, hazard ratios).
- **Produce pharmaceutical research documents** for drug development, clinical trials, or regulatory submissions.
- **Develop clinical practice guidelines** with GRADE evidence grading and decision algorithms.
- **Document biomarker-guided therapy selection** at the population level (not individual patients).
- **Synthesize evidence** from multiple trials or real-world data sources.
- **Create clinical decision algorithms** with flowcharts for treatment sequencing.

**Do NOT use this skill for:**
- Individual patient treatment plans (use `treatment-plans` skill).
- Bedside clinical care documentation (use `treatment-plans` skill).
- Simple patient-specific treatment protocols (use `treatment-plans` skill).

## Visual Enhancement with Scientific Schematics

**⚠️ MANDATORY: Every clinical decision support document MUST include at least 1-2 AI-generated figures using the scientific-schematics skill.**

This is not optional. Clinical decision documents require clear visual algorithms. Before finalizing any document:
1. Generate at minimum ONE schematic or diagram (e.g., clinical decision algorithm, treatment pathway, or biomarker stratification tree).
2. For cohort analyses: include patient flow diagram.
3. For treatment recommendations: include decision flowchart.

**How to generate figures:**
- Use the **scientific-schematics** skill to generate AI-powered publication-quality diagrams.
- Simply describe your desired diagram in natural language.
- Nano Banana Pro will automatically generate, review, and refine the schematic.

**How to generate schematics:**
```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```

The AI will automatically:
- Create publication-quality images with proper formatting.
- Review and refine through multiple iterations.
- Ensure accessibility (colorblind-friendly, high contrast).
- Save outputs in the figures/ directory.

**When to add schematics:**
- Clinical decision algorithm flowcharts.
- Treatment pathway diagrams.
- Biomarker stratification trees.
- Patient cohort flow diagrams (CONSORT-style).
- Survival curve visualizations.
- Molecular mechanism diagrams.
- Any complex concept that benefits from visualization.

For detailed guidance on creating schematics, refer to the scientific-schematics skill documentation.

---

## Document Structure

**CRITICAL REQUIREMENT: All clinical decision support documents MUST begin with a complete executive summary on page 1 that spans the entire first page before any table of contents or detailed sections.**

### Page 1 Executive Summary Structure

The first page of every CDS document should contain ONLY the executive summary with the following components:

**Required Elements (all on page 1):**
1. **Document Title and Type**
   - Main title (e.g., "Biomarker-Stratified Cohort Analysis" or "Evidence-Based Treatment Recommendations").
   - Subtitle with disease state and focus.
   
2. **Report Information Box** (using colored tcolorbox)
   - Document type and purpose.
   - Date of analysis/report.
   - Disease state and patient population.
   - Author/institution (if applicable).
   - Analysis framework or methodology.
   
3. **Key Findings Boxes** (3-5 colored boxes using tcolorbox)
   - **Primary Results** (blue box): Main efficacy/outcome findings.
   - **Biomarker Insights** (green box): Key molecular subtype findings.
   - **Clinical Implications** (yellow/orange box): Actionable treatment implications.
   - **Statistical Summary** (gray box): Hazard ratios, p-values, key statistics.
   - **Safety Highlights** (red box, if applicable): Critical adverse events or warnings.

**Visual Requirements:**
- Use `\thispagestyle{empty}` to remove page numbers from page 1.
- All content must fit on page 1 (before `\newpage`).
- Use colored tcolorbox environments with different colors for visual hierarchy.
- Boxes should be scannable and highlight most critical information.
- Use bullet points, not narrative paragraphs.
- End page 1 with `\newpage` before table of contents or detailed sections.

**Example First Page LaTeX Structure:**
```latex
\maketitle
\thispagestyle{empty}

% Report Information Box
\begin{tcolorbox}[colback=blue!5!white, colframe=blue!75!black, title=Report Information]
\textbf{Document Type:} Patient Cohort Analysis\\
\textbf{Disease State:} HER2-Positive Metastatic Breast Cancer\\
\textbf{Analysis Date:} \today\\
\textbf{Population:} 60 patients, biomarker-stratified by HR status
\end{tcolorbox}

\vspace{0.3cm}

% Key Finding #1: Primary Results
\begin{tcolorbox}[colback=blue!5!white, colframe=blue!75!black, title=Primary Efficacy Results]
\begin{itemize}
    \item Overall ORR: 72\% (95\% CI: 59-83\%).
    \item Median PFS: 18.5 months (95\% CI: 14.2-22.8).
    \item Median OS: 35.2 months (95\% CI: 28.1-NR).
\end{itemize}
\end{tcolorbox}

\vspace{0.3cm}

% Key Finding #2: Biomarker Insights
\begin{tcolorbox}[colback=green!5!white, colframe=green!75!black, title=Biomarker Stratification Findings]
\begin{itemize}
    \item HR+/HER2+: ORR 68\%, median PFS 16.2 months.
    \item HR-/HER2+: ORR 78\%, median PFS 22.1 months.
    \item HR status significantly associated with outcomes (p=0.041).
\end{itemize}
\end{tcolorbox}

\vspace{0.3cm}

% Key Finding #3: Clinical Implications
\begin{tcolorbox}[colback=orange!5!white, colframe=orange!75!black, title=Clinical Recommendations]
\begin{itemize}
    \item Strong efficacy observed regardless of HR status (Grade 1A).
    \item HR-/HER2+ patients showed numerically superior outcomes.
    \item Treatment recommended for all HER2+ MBC patients.
\end{itemize}
\end{tcolorbox}

\newpage
\tableofcontents  % TOC on page 2
\newpage  % Detailed content starts page 3
```

### Patient Cohort Analysis (Detailed Sections - Page 3+)
- **Cohort Characteristics**: Demographics, baseline features, patient selection criteria.
- **Biomarker Stratification**: Molecular subtypes, genomic alterations, IHC profiles.
- **Treatment Exposure**: Therapies received, dosing, treatment duration by subgroup.
- **Outcome Analysis**: Response rates (ORR, DCR), survival data (OS, PFS), DOR.
- **Statistical Methods**: Kaplan-Meier survival curves, hazard ratios, log-rank tests, Cox regression.
- **Subgroup Comparisons**: Biomarker-stratified efficacy, forest plots, statistical significance.
- **Safety Profile**: Adverse events by subgroup, dose modifications, discontinuations.
- **Clinical Recommendations**: Treatment implications based on biomarker profiles.
- **Figures**: Waterfall plots, swimmer plots, survival curves, forest plots.
- **Tables**: Demographics table, biomarker frequency, outcomes by subgroup.

### Treatment Recommendation Reports (Detailed Sections - Page 3+)

**Page 1 Executive Summary for Treatment Recommendations should include:**
1. **Report Information Box**: Disease state, guideline version/date, target population.
2. **Key Recommendations Box** (green): Top 3-5 GRADE-graded recommendations by line of therapy.
3. **Biomarker Decision Criteria Box** (blue): Key molecular markers influencing treatment selection.
4. **Evidence Summary Box** (gray): Major trials supporting recommendations (e.g., KEYNOTE-189, FLAURA).
5. **Critical Monitoring Box** (orange/red): Essential safety monitoring requirements.

**Detailed Sections (Page 3+):**
- **Clinical Context**: Disease state, epidemiology, current treatment landscape.
- **Target Population**: Patient characteristics, biomarker criteria, staging.
- **Evidence Review**: Systematic literature synthesis, guideline summary, trial data.
- **Treatment Options**: Available therapies with mechanism of action.
- **Evidence Grading**: GRADE assessment for each recommendation (1A, 1B, 2A, 2B, 2C).
- **Recommendations by Line**: First-line, second-line, subsequent therapies.
- **Biomarker-Guided Selection**: Decision criteria based on molecular profiles.
- **Treatment Algorithms**: TikZ flowcharts showing decision pathways.
- **Monitoring Protocol**: Safety assessments, efficacy monitoring, dose modifications.
- **Special Populations**: Elderly, renal/hepatic impairment, comorbidities.
- **References**: Full bibliography with trial names and citations.

## Output Format

**MANDATORY FIRST PAGE REQUIREMENT:**
- **Page 1**: Full-page executive summary with 3-5 colored tcolorbox elements.
- **Page 2**: Table of contents (optional).
- **Page 3+**: Detailed sections with methods, results, figures, tables.

**Document Specifications:**
- **Primary**: LaTeX/PDF with 0.5in margins for compact, data-dense presentation.
- **Length**: Typically 5-15 pages (1 page executive summary + 4-14 pages detailed content).
- **Style**: Publication-ready, pharmaceutical-grade, suitable for regulatory submissions.
- **First Page**: Always a complete executive summary spanning entire page 1 (see Document Structure section).

**Visual Elements:**
- **Colors**: 
  - Page 1 boxes: blue=data/information, green=biomarkers/recommendations, yellow/orange=clinical implications, red=warnings.
  - Recommendation boxes (green=strong recommendation, yellow=conditional, blue=research needed).
  - Biomarker stratification (color-coded molecular subtypes).
  - Statistical significance (color-coded p-values, hazard ratios).
- **Tables**: 
  - Demographics with baseline characteristics.
  - Biomarker frequency by subgroup.
  - Outcomes table (ORR, PFS, OS, DOR by molecular subtype).
  - Adverse events by cohort.
  - Evidence summary tables with GRADE ratings.
- **Figures**: 
  - Kaplan-Meier survival curves with log-rank p-values and number at risk tables.
  - Waterfall plots showing best response by patient.
  - Forest plots for subgroup analyses with confidence intervals.
  - TikZ decision algorithm flowcharts.
  - Swimmer plots for individual patient timelines.
- **Statistics**: Hazard ratios with 95% CI, p-values, median survival times, landmark survival rates.
- **Compliance**: De-identification per HIPAA Safe Harbor, confidentiality notices for proprietary data.

## Integration

This skill integrates with:
- **scientific-writing**: Citation management, statistical reporting, evidence synthesis.
- **clinical-reports**: Medical terminology, HIPAA compliance, regulatory documentation.
- **scientific-schematics**: TikZ flowcharts for decision algorithms and treatment pathways.
- **treatment-plans**: Individual patient applications of cohort-derived insights (bidirectional