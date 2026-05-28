---
name: biorxiv-database
description: Use this skill when searching for life sciences preprints by keywords, authors, date ranges, or categories, retrieving paper metadata, downloading PDFs, or conducting literature reviews.
---

# bioRxiv Database

## Overview

This skill provides efficient Python-based tools for searching and retrieving preprints from the bioRxiv database. It enables comprehensive searches by keywords, authors, date ranges, and categories, returning structured JSON metadata that includes titles, abstracts, DOIs, and citation information. The skill also supports PDF downloads for full-text analysis.

## When to Use This Skill

Use this skill when:
- Searching for recent preprints in specific research areas
- Tracking publications by particular authors
- Conducting systematic literature reviews
- Analyzing research trends over time periods
- Retrieving metadata for citation management
- Downloading preprint PDFs for analysis
- Filtering papers by bioRxiv subject categories

## Core Search Capabilities

### 1. Keyword Search

Search for preprints containing specific keywords in titles, abstracts, or author lists.

**Basic Usage:**
```python
python scripts/biorxiv_search.py \
  --keywords "CRISPR" "gene editing" \
  --start-date 2024-01-01 \
  --end-date 2024-12-31 \
  --output results.json
```

**With Category Filter:**
```python
python scripts/biorxiv_search.py \
  --keywords "neural networks" "deep learning" \
  --days-back 180 \
  --category neuroscience \
  --output recent_neuroscience.json
```

**Search Fields:**
By default, keywords are searched in both title and abstract. Customize with `--search-fields`:
```python
python scripts/biorxiv_search.py \
  --keywords "AlphaFold" \
  --search-fields title \
  --days-back 365
```

### 2. Author Search

Find all papers by a specific author within a date range.

**Basic Usage:**
```python
python scripts/biorxiv_search.py \
  --author "Smith" \
  --start-date 2023-01-01 \
  --end-date 2024-12-31 \
  --output smith_papers.json
```

**Recent Publications:**
```python
# Last year by default if no dates specified
python scripts/biorxiv_search.py \
  --author "Johnson" \
  --output johnson_recent.json
```

### 3. Date Range Search

Retrieve all preprints posted within a specific date range.

**Basic Usage:**
```python
python scripts/biorxiv_search.py \
  --start-date 2024-01-01 \
  --end-date 2024-01-31 \
  --output january_2024.json
```