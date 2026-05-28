---
name: arxiv-search
description: Use this skill when you need to search the arXiv preprint repository for scholarly articles in various scientific fields.
---

# arXiv Search Skill

This skill provides access to arXiv, a free distribution service and open-access archive for scholarly articles in physics, mathematics, computer science, quantitative biology, quantitative finance, statistics, electrical engineering, systems science, and economics.

## When to Use This Skill

Use this skill when you need to:
- Find preprints and recent research papers before journal publication.
- Search for papers in computational biology, bioinformatics, or systems biology.
- Access mathematical or statistical methods papers relevant to biology.
- Find machine learning papers applied to biological problems.
- Get the latest research that may not yet be in PubMed.

## How to Use

The skill provides a script that searches arXiv and returns formatted results.

### Basic Usage

**Note:** Always use the absolute path from your skills directory.

For Python:
```bash
python3 [YOUR_SKILLS_DIR]/arxiv-search/arxiv_search.py "your search query" [--max-papers N]
```

For TypeScript:
```bash
npx tsx [YOUR_SKILLS_DIR]/arxiv-search/arxiv_search.ts "your search query" [--max-papers N]
```

Replace `[YOUR_SKILLS_DIR]` with the absolute skills directory path from your system prompt.

**Arguments:**
- `query` (required): The search query string (e.g., "neural networks protein structure", "single cell RNA-seq").
- `--max-papers` (optional): Maximum number of papers to retrieve (default: 10).

### Examples

Search for machine learning papers:
```bash
python3 [YOUR_SKILLS_DIR]/arxiv-search/arxiv_search.py "deep learning drug discovery" --max-papers 5
```

Search for computational biology papers:
```bash
python3 [YOUR_SKILLS_DIR]/arxiv-search/arxiv_search.py "protein folding prediction"
```

Search for bioinformatics methods:
```bash
python3 [YOUR_SKILLS_DIR]/arxiv-search/arxiv_search.py "genome assembly algorithms"
```

## Output Format

The script returns formatted results with:
- **Title**: Paper title.
- **Summary**: Abstract/summary text.

Each paper is separated by blank lines for readability.

## Features

- **Relevance sorting**: Results ordered by relevance to query.
- **Fast retrieval**: Direct API access with no authentication required.
- **Simple interface**: Clean, easy-to-parse output.
- **No API key required**: Free access to arXiv database.