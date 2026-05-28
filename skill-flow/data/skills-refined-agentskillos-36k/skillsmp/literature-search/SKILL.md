---
name: literature-search
description: Search and retrieve scientific literature. Use when asked to find papers, research a topic, find citations, get paper abstracts, or conduct literature reviews. Accesses Semantic Scholar, arXiv, and other academic databases.
allowed-tools:
  - Read
  - Write
  - Bash
  - WebSearch
  - WebFetch
---

# Scientific Literature Search

You are conducting scientific literature searches and reviews.

## Available Resources

### Semantic Scholar (Primary)
- 225M+ papers indexed
- Rich citation network
- AI-powered relevance ranking
- API access via MCP server

### arXiv
- Preprints in physics, materials science, chemistry
- Open access
- Latest research before peer review

### PubMed
- Biomedical and life sciences
- Peer-reviewed publications

### CrossRef
- DOI resolution
- Publication metadata

## Search Strategies

### Topic Search
When researching a topic:
1. Start with broad search terms
2. Refine based on initial results
3. Follow citation networks (cited by, references)
4. Look for review articles first

### Specific Paper Search
When looking for a specific paper:
1. Search by title (exact or partial)
2. Search by author + keywords
3. Search by DOI if known

### Citation Analysis
1. Find highly cited papers in the field
2. Look at recent papers citing foundational work
3. Identify key authors and groups

## Using Semantic Scholar MCP

The Semantic Scholar MCP server provides:
- Paper search
- Author search
- Citation information
- Paper recommendations

Example queries:
```
Search for papers on "CO2 adsorption in MOFs"
Find recent papers by Author Name about topic
Get citations for paper with ID xxx
```

## Using Web Search

For broader searches:
```
Search for "metal-organic framework CO2 capture" site:nature.com
Search for "LAMMPS force field" filetype:pdf
```

## Manual API Access (Fallback)

### Semantic Scholar API
```bash
curl "https://api.semanticscholar.org/graph/v1/paper/search?query=machine+learning+materials&limit=10"
```

### arXiv API
```bash
curl "http://export.arxiv.org/api/query?search_query=all:materials+science&max_results=10"
```

## Literature Review Workflow

1. **Define Scope**
   - What specific question are you answering?
   - What time period? (last 5 years typical)
   - What subfields?

2. **Initial Search**
   - Use 3-5 different keyword combinations
   - Note total results to gauge field size

3. **Screen Results**
   - Read titles and abstracts
   - Flag relevant papers
   - Note key authors and journals

4. **Deep Dive**
   - Read full text of key papers
   - Extract methods, parameters, findings
   - Build citation network

5. **Synthesize**
   - Identify consensus and controversies
   - Note gaps in literature
   - Summarize for user

## Extracting Information

From papers, extract:
- **Methods**: Simulation software, parameters, conditions
- **Force fields**: Which potentials used, parameters
- **Results**: Key numerical values, trends
- **Limitations**: What authors acknowledge

## Citation Format

Use consistent format:
```
Author1, Author2, et al. "Title." Journal Volume, Pages (Year). DOI: xxx
```

## Saving Results

Save literature search results to:
```
workspaces/project-name/literature/
├── search-results.md       # Summary of search
├── key-papers.md           # Annotated bibliography
├── extracted-parameters.md # Force field params, etc.
└── pdfs/                   # Downloaded papers (if permitted)
```

## Web Download (via Playwright)

For downloading papers or supplementary info:
```
Use playwright to navigate to [URL] and download the PDF
```

Note: Respect copyright and access restrictions.

## Best Practices

1. **Document Everything**: Record search terms, dates, result counts
2. **Check Recency**: Prefer recent papers unless seeking foundational work
3. **Verify Citations**: Cross-check important claims
4. **Look for Reviews**: Start with review articles for new topics
5. **Follow Authors**: Key researchers often have related work
6. **Check Preprints**: arXiv may have newer versions

## Common Queries

### Materials Science
- Force field parameters for [material]
- DFT study of [property] in [material]
- Molecular dynamics of [process]

### Computational Methods
- Best practices for [simulation type]
- Convergence testing for [property]
- Comparison of [method A] vs [method B]

### Specific Materials
- [Material] synthesis and characterization
- [Material] applications in [field]
- [Material] properties: [specific property]
