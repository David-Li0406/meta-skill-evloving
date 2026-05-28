---
name: lit-review
description: Conduct thorough, methodical literature reviews adhering to scholarly standards. This skill guides systematic research synthesis across academic databases including PubMed, arXiv, bioRxiv, and Semantic Scholar.
allowed-tools: [Read, Write, Edit, Bash, WebSearch, WebFetch, Task]
---

# Literature Review Assistant

## Purpose

This skill facilitates rigorous, systematic literature reviews that follow established academic methodology for synthesizing research across multiple scholarly databases.

## Workflow Stages

The review process consists of seven sequential phases:

### 1. Planning Phase
- Define research questions using established frameworks (PICO for clinical, SPIDER for qualitative)
- Establish clear scope boundaries
- Document inclusion and exclusion criteria upfront

### 2. Search Execution
- Query multiple databases with documented Boolean search strings
- Record search dates, databases used, and result counts
- Save raw search results for reproducibility

### 3. Screening Process
- Apply criteria at title level first
- Progress to abstract screening
- Conduct full-text review for remaining candidates

### 4. Data Extraction
- Collect relevant data systematically
- Assess study quality using appropriate tools (GRADE, Newcastle-Ottawa, etc.)
- Document extraction in structured format

### 5. Synthesis
- Organize findings thematically rather than study-by-study
- Identify patterns, gaps, and contradictions
- Draw connections across the body of literature

### 6. Citation Verification
- Validate all citations before submission
- Cross-check DOIs through CrossRef
- Ensure bibliographic accuracy

### 7. Document Generation
- Produce formatted output (markdown, LaTeX, or PDF)
- Include PRISMA flow diagram showing selection process
- Add thematic synthesis visualizations where appropriate

## Source Prioritization

### Citation Thresholds by Age
- Recent papers (1-3 years): 20+ citations indicates influence
- Established papers (3-7 years): 100+ citations expected
- Foundational work (7+ years): 500+ citations for seminal papers

### Venue Quality Hierarchy
- **Premier venues**: Nature, Science, Cell, NEJM, Lancet, JAMA
- **High-impact journals**: Field-specific top journals (IF > 10)
- **Solid peer-reviewed**: Reputable journals with rigorous review
- **Supporting sources**: Lower-impact but peer-reviewed (use sparingly)

## Quality Assurance

- Document every step for reproducibility
- Include PRISMA diagram showing paper flow
- Specify exclusion reasons with counts
- Verify all DOIs and citations programmatically when possible

## Integration

This skill works alongside:
- `reference-management` for citation handling
- `paper-search` for literature discovery
- `academic-writing` for manuscript preparation
