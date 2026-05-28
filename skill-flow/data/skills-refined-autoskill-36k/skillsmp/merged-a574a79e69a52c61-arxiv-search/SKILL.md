---
name: arxiv-search
description: Use this skill to search the arXiv preprint repository for research papers in physics, mathematics, computer science, quantitative biology, and related fields.
---

# arXiv Search Skill

This skill provides access to arXiv, a free distribution service and open-access archive for scholarly articles across various fields including physics, mathematics, computer science, quantitative biology, quantitative finance, statistics, and economics.

## When to Use This Skill

Use this skill when you need to:

- Find preprints and recent research papers before journal publication
- Search for papers in computational biology, bioinformatics, or systems biology
- Access mathematical or statistical methods papers relevant to biology
- Find machine learning papers applied to biological problems
- Get the latest research that may not yet be in PubMed

## How to Use

The skill provides a script that searches arXiv and returns formatted results.

### Basic Usage

**Note:** Always use the absolute path from your skills directory.

For Python implementation:
```bash
python3 [YOUR_SKILLS_DIR]/arxiv-search/arxiv_search.py "your search query" [--max-papers N]
```

For TypeScript implementation:
```bash
npx tsx [YOUR_SKILLS_DIR]/arxiv-search/arxiv_search.ts "your search query" [--max-papers N]
```

Replace `[YOUR_SKILLS_DIR]` with the absolute path to your skills directory.

### Arguments

- `query` (required): The search query string (e.g., "neural networks protein structure", "single cell RNA-seq")
- `--max-papers` (optional): Maximum number of papers to retrieve (default: 10)

### Examples

**Search for machine learning papers:**
```bash
python3 [YOUR_SKILLS_DIR]/arxiv-search/arxiv_search.py "deep learning drug discovery" --max-papers 5
```

**Search for computational biology papers:**
```bash
npx tsx [YOUR_SKILLS_DIR]/arxiv-search/arxiv_search.ts "protein folding prediction"
```

**Search for bioinformatics methods:**
```bash
python3 [YOUR_SKILLS_DIR]/arxiv-search/arxiv_search.py "genome assembly algorithms"
```

## Output Format

The script returns formatted results with:

- **Title**: Paper title
- **Summary**: Abstract/summary text

Each paper is separated by blank lines for readability.

## Features

- **Relevance sorting**: Results ordered by relevance to query
- **Fast retrieval**: Direct API access with no authentication required
- **Simple interface**: Clean, easy-to-parse output
- **No API key required**: Free access to arXiv database

## Dependencies

This skill requires the `arxiv` Python package. If it's not installed, you can install it using:
```bash
pip install arxiv
```

## Notes

- Papers are preprints and may not be peer-reviewed.
- Results include both recent uploads and older papers.
- Best for computational/theoretical work in biology and related fields.