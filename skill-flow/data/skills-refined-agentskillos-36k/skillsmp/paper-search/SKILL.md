---
name: paper-search
description: Find relevant academic literature across scholarly databases. Intelligent search across PubMed, Google Scholar, Semantic Scholar, arXiv, and other repositories with quality filtering and citation tracking.
allowed-tools: [Read, Write, Edit, Bash, WebSearch, WebFetch]
---

# Paper Search Assistant

## Purpose

Locate relevant academic literature efficiently across multiple scholarly databases. This skill provides intelligent search strategies with quality filtering to surface the most important papers on a topic.

## Supported Sources

### Primary Databases
- **PubMed**: Biomedical and life sciences
- **Google Scholar**: Broad coverage across fields
- **Semantic Scholar**: AI-powered semantic search
- **arXiv**: Preprints in physics, math, CS, biology

### Specialized Resources
- **bioRxiv/medRxiv**: Biology and medicine preprints
- **SSRN**: Social sciences working papers
- **IEEE Xplore**: Engineering and computing
- **Web of Science**: Citation-indexed journals

## Search Strategies

### Query Construction
- Use Boolean operators: AND, OR, NOT
- Employ quotes for exact phrases
- Apply field-specific syntax where available

### PubMed Syntax Examples
```
diabetes AND ("machine learning" OR "deep learning")
author:Smith[au] AND 2020:2024[dp]
randomized controlled trial[pt]
```

### Google Scholar Tips
- Use `author:` for specific researchers
- Use `site:` to limit domains
- Filter by date range

### Semantic Scholar Advantages
- Understands conceptual meaning
- Citation and reference graphs
- Author disambiguation

## Quality Filtering

### Citation Thresholds by Paper Age
- **Published within 2 years**: 10+ citations noteworthy
- **2-4 years old**: 50+ citations indicates influence
- **4-7 years old**: 150+ citations expected for important work
- **7+ years old**: 300+ citations for foundational papers

### Venue Quality Tiers

**Tier 1 - Premier**
Nature, Science, Cell, NEJM, Lancet, JAMA, field-specific top journals

**Tier 2 - High Impact**
Major field journals, high-impact specialty publications

**Tier 3 - Solid Peer-Reviewed**
Reputable journals with established review processes

**Tier 4 - Supporting**
Lower-impact but peer-reviewed (use selectively)

## Search Workflow

### Phase 1: Scoping Search
- Broad initial queries to map the landscape
- Identify key terms and author names
- Find review articles for orientation

### Phase 2: Targeted Search
- Refined queries based on scoping results
- Systematic database coverage
- Citation tracking (forward and backward)

### Phase 3: Quality Assessment
- Filter by citation count and venue
- Check author credibility and affiliations
- Assess recency and relevance

### Phase 4: Organization
- Group papers by theme or subtopic
- Note key findings from abstracts
- Flag must-read versus supporting papers

## Output Format

For each relevant paper, capture:
- Title and authors
- Publication venue and year
- DOI or stable link
- Citation count
- Brief relevance note

## Integration

Coordinates with:
- `reference-management` for BibTeX generation
- `lit-review` for systematic review searches
- `hypothesis-dev` for evidence gathering
