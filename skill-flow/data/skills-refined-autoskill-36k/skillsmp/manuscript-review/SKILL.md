---
name: manuscript-review
description: Systematically evaluate scientific manuscripts for methodology, statistics, reproducibility, and scholarly rigor. Provides structured feedback following peer review best practices.
allowed-tools: [Read, Write, Edit, Bash, WebSearch, WebFetch]
---

# Manuscript Review Assistant

## Purpose

Guide thorough, constructive evaluation of scientific manuscripts across disciplines. This skill provides a structured framework for assessing methodology, statistics, reproducibility, ethics, and presentation quality.

## Review Process

### Phase 1: Initial Assessment
- Evaluate scope alignment with venue
- Assess novelty and contribution
- Gauge overall quality and completeness

### Phase 2: Section-by-Section Analysis

#### Abstract
- Accurate summary of findings?
- Appropriate length and structure?
- Key results clearly stated?

#### Introduction
- Context established appropriately?
- Gap in knowledge identified?
- Objectives clearly stated?

#### Methods
- Sufficient detail for replication?
- Appropriate study design?
- Statistical approach justified?

#### Results
- Findings presented objectively?
- Figures and tables clear?
- Statistics reported correctly?

#### Discussion
- Results interpreted appropriately?
- Limitations acknowledged?
- Conclusions supported by data?

### Phase 3: Technical Rigor

#### Methodological Assessment
- Sample size justification
- Control conditions
- Randomization and blinding
- Measurement validity

#### Statistical Evaluation
- Appropriate tests selected
- Assumptions verified
- Effect sizes reported
- Multiple comparisons addressed

### Phase 4: Reproducibility Check
- Data availability statement present?
- Code/materials accessible?
- Protocol detail sufficient?
- Reporting standards followed?

### Phase 5: Presentation Quality
- Figures clear and informative?
- Tables appropriately formatted?
- Writing clear and accessible?
- Organization logical?

### Phase 6: Ethical Review
- Human subjects approval documented?
- Animal welfare addressed?
- Conflicts disclosed?
- Prior work properly cited?

## Feedback Structure

Organize comments hierarchically:

### Summary Statement
Overall assessment (2-3 sentences)

### Major Comments
Fundamental issues affecting validity or conclusions
- Number these clearly
- Explain the concern
- Suggest remediation

### Minor Comments
Improvements that would strengthen the work
- Clarity suggestions
- Additional analyses
- Presentation tweaks

### Questions for Authors
Clarifications needed to complete review

## Constructive Review Principles

- Acknowledge strengths alongside weaknesses
- Be specific rather than vague
- Explain reasoning behind concerns
- Suggest solutions where possible
- Maintain respectful, professional tone
- Focus on the work, not the authors

## Discipline-Specific Considerations

Adjust focus based on field:
- **Clinical research**: Patient safety, CONSORT/STROBE adherence
- **Laboratory science**: Technical replication, controls
- **Computational work**: Code availability, validation
- **Qualitative research**: Rigor criteria differ (credibility, transferability)

## Common Issues Checklist

- [ ] Overstated conclusions
- [ ] Missing control conditions
- [ ] Inappropriate statistical tests
- [ ] p-hacking indicators
- [ ] Inadequate sample size
- [ ] Cherry-picked results
- [ ] Missing limitations discussion
- [ ] Inadequate prior work citation

## Integration

Coordinates with:
- `academic-writing` for understanding manuscript standards
- `reference-management` for citation verification
- `lit-review` for assessing literature coverage
