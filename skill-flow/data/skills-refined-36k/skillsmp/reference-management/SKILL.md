---
name: reference-management
description: Handle citations systematically throughout research and writing. Search scholarly databases, extract metadata, validate references, and generate formatted BibTeX entries for academic work.
allowed-tools: [Read, Write, Edit, Bash, WebSearch, WebFetch]
---

# Reference Management Assistant

## Purpose

Maintain citation accuracy and consistency throughout the research and writing process. This skill provides tools for searching academic databases, extracting metadata, validating citation information, and generating properly formatted bibliographic entries.

## When to Apply This Skill

Use for:
- Searching for relevant papers on a topic
- Converting DOIs, PMIDs, or arXiv IDs to BibTeX
- Extracting complete metadata from papers
- Validating existing citations for accuracy
- Cleaning and deduplicating BibTeX files
- Finding highly-cited papers in a field
- Building comprehensive bibliographies

## Core Workflow

### Phase 1: Discovery
- Query Google Scholar, PubMed, or Semantic Scholar
- Filter by date range, venue, and citation count
- Identify highly-cited foundational works

### Phase 2: Metadata Extraction
- Retrieve full bibliographic data from CrossRef, PubMed, or arXiv
- Capture: authors, title, journal, volume, pages, DOI, year
- Handle special characters and formatting

### Phase 3: Validation
- Verify DOIs resolve correctly
- Check author name consistency
- Confirm publication details match source

### Phase 4: Formatting
- Generate BibTeX entries with consistent keys
- Apply appropriate entry types (article, inproceedings, book, etc.)
- Format according to target style guide

### Phase 5: Organization
- Detect and merge duplicate entries
- Maintain consistent naming conventions
- Group by topic or section as needed

## Search Strategies

### Google Scholar
- Use quotes for exact phrases
- `author:` operator for specific researchers
- `site:` to limit to specific domains

### PubMed
- MeSH terms for medical precision
- Boolean operators (AND, OR, NOT)
- Filters for article type, date, species

### Semantic Scholar
- Semantic search understands concepts
- Citation and reference graphs
- Author disambiguation

## BibTeX Best Practices

```bibtex
@article{AuthorYear,
  author    = {Last, First and Second, Author},
  title     = {Title in Sentence Case},
  journal   = {Full Journal Name},
  year      = {2024},
  volume    = {12},
  number    = {3},
  pages     = {100--115},
  doi       = {10.xxxx/xxxxx}
}
```

### Key Naming Convention
- Format: `FirstAuthorLastNameYear` (e.g., `Smith2024`)
- Add letter suffix for same author/year: `Smith2024a`, `Smith2024b`

## Common Issues to Avoid

- Missing DOIs (always include when available)
- Inconsistent author name formats
- Journal name abbreviation mismatches
- Broken special characters (UTF-8 vs LaTeX encoding)
- Duplicate entries with slightly different metadata

## Integration

Coordinates with:
- `lit-review` for systematic review citations
- `academic-writing` for manuscript references
- `paper-search` for literature discovery
