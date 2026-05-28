# Reporting Guidelines Reference

## Contents
1. [Guideline Selection](#guideline-selection)
2. [CONSORT](#consort-randomized-trials)
3. [STROBE](#strobe-observational-studies)
4. [PRISMA](#prisma-systematic-reviews)
5. [Other Guidelines](#other-guidelines)

---

## Guideline Selection

| Study Type | Guideline | Website |
|-----------|-----------|---------|
| Randomized controlled trial | CONSORT | consort-statement.org |
| Observational (cohort, case-control, cross-sectional) | STROBE | strobe-statement.org |
| Systematic review/meta-analysis | PRISMA | prisma-statement.org |
| Diagnostic accuracy | STARD | stard-statement.org |
| Prediction models | TRIPOD | tripod-statement.org |
| Animal research | ARRIVE | arriveguidelines.org |
| Case reports | CARE | care-statement.org |
| Quality improvement | SQUIRE | squire-statement.org |
| Economic evaluation | CHEERS | ispor.org/cheers |
| Clinical trial protocol | SPIRIT | spirit-statement.org |

**Rule**: Identify applicable guideline before writing. Use checklist during drafting.

---

## CONSORT (Randomized Trials)

### Essential Elements

**Title/Abstract**
- Identify as randomized trial in title
- Structured abstract with trial design, methods, results, conclusions

**Introduction**
- Scientific background and rationale
- Specific objectives or hypotheses

**Methods**
- Trial design (parallel, factorial, etc.) with allocation ratio
- Eligibility criteria for participants
- Settings and locations
- Interventions with sufficient detail for replication
- Pre-specified primary and secondary outcomes
- Sample size calculation
- Randomization: sequence generation, allocation concealment, implementation
- Blinding: who was blinded, how

**Results**
- Flow diagram (REQUIRED): enrollment, allocation, follow-up, analysis
- Baseline demographics table
- Numbers analyzed per group
- Primary outcome: effect estimate with precision (95% CI)
- All pre-specified secondary outcomes
- Harms/adverse events

**Discussion**
- Limitations (sources of bias, imprecision)
- Generalizability
- Interpretation consistent with results

**Other**
- Registration number and registry name
- Protocol access
- Funding source

### CONSORT Flow Diagram
```
Enrollment:     Assessed for eligibility (n=)
                    ↓
                Excluded (n=)
                • Not meeting criteria (n=)
                • Declined (n=)
                • Other (n=)
                    ↓
                Randomized (n=)
                    ↓
Allocation:     ←——————————————→
                Intervention (n=)    Control (n=)
                    ↓                    ↓
Follow-up:      Lost to FU (n=)     Lost to FU (n=)
                Discontinued (n=)    Discontinued (n=)
                    ↓                    ↓
Analysis:       Analyzed (n=)        Analyzed (n=)
                Excluded (n=)        Excluded (n=)
```

---

## STROBE (Observational Studies)

### Essential Elements

**Title/Abstract**
- Indicate study design (cohort, case-control, cross-sectional)

**Introduction**
- Background/rationale
- Objectives including pre-specified hypotheses

**Methods**
- Study design with key elements
- Setting: locations, dates of recruitment/exposure/follow-up
- Participants: eligibility, sources, selection methods
- Variables: outcomes, exposures, predictors, confounders
- Data sources/measurement for each variable
- Bias: efforts to address potential sources
- Study size: how determined
- Statistical methods including confounding control

**Results**
- Participant flow diagram
- Descriptive data: characteristics, exposures, follow-up time
- Outcome data: numbers in each category
- Main results: unadjusted and adjusted estimates with CI
- Other analyses (subgroups, interactions, sensitivity)

**Discussion**
- Key results summary
- Limitations including bias direction
- Interpretation with literature context
- Generalizability

### Study-Specific Requirements

**Cohort studies**: Report numbers at each follow-up stage, person-time at risk

**Case-control studies**: Report case/control selection rationale, matching criteria

**Cross-sectional studies**: Report analytical methods for sampling strategy

---

## PRISMA (Systematic Reviews)

### Essential Elements

**Title**
- Identify as systematic review, meta-analysis, or both

**Abstract**
- Structured summary: background, objectives, data sources, eligibility, synthesis methods, results, limitations, conclusions, registration

**Introduction**
- Rationale and objectives (PICO format recommended)

**Methods**
- Protocol registration (PROSPERO, OSF)
- Eligibility criteria
- Information sources with dates
- Search strategy (full for at least one database)
- Selection process
- Data collection process
- Data items
- Risk of bias assessment (tool used)
- Effect measures
- Synthesis methods (meta-analysis approach if used)
- Certainty assessment (e.g., GRADE)

**Results**
- PRISMA flow diagram (REQUIRED)
- Study characteristics
- Risk of bias within studies
- Results of individual studies
- Synthesis results with heterogeneity
- Risk of bias across studies
- Certainty of evidence

**Discussion**
- Summary of evidence
- Limitations
- Conclusions

### PRISMA Flow Diagram
```
Identification:  Records from databases (n=)
                 Records from other sources (n=)
                        ↓
                 Records after duplicates removed (n=)
                        ↓
Screening:       Records screened (n=)
                        ↓
                 Records excluded (n=)
                        ↓
                 Full-text assessed (n=)
                        ↓
                 Full-text excluded (n=)
                 • Reason 1 (n=)
                 • Reason 2 (n=)
                        ↓
Included:        Studies in qualitative synthesis (n=)
                        ↓
                 Studies in meta-analysis (n=)
```

---

## Other Guidelines

### STARD (Diagnostic Accuracy)
Key elements: Index test, reference standard, participant flow, 2×2 table, sensitivity/specificity with CI

### TRIPOD (Prediction Models)
Key elements: Model development vs. validation, predictor selection, model performance measures, calibration, discrimination

### ARRIVE (Animal Research)
Key elements: Species/strain, housing, sample size justification, randomization, blinding, humane endpoints

### CARE (Case Reports)
Key elements: Patient information, clinical findings, timeline, diagnostic assessment, therapeutic interventions, outcomes

---

## Pre-Submission Checklist

- [ ] Correct guideline identified for study type
- [ ] Checklist downloaded from official website
- [ ] All applicable items addressed
- [ ] Flow diagram included (CONSORT, STROBE, PRISMA)
- [ ] Registration number included (trials, systematic reviews)
- [ ] Checklist completed and ready for submission
