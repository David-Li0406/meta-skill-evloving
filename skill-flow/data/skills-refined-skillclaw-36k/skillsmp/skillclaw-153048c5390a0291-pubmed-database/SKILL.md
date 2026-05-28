---
name: pubmed-database
description: Use this skill when you need to access and query the PubMed database for biomedical literature, utilizing advanced search techniques and the E-utilities API.
---

# PubMed Database

## Overview

PubMed is the U.S. National Library of Medicine's comprehensive database providing free access to MEDLINE and life sciences literature. This skill allows you to construct advanced queries using Boolean operators, MeSH terms, and field tags, and access data programmatically via the E-utilities API for systematic reviews and literature analysis.

## When to Use This Skill

Use this skill when:
- Searching for biomedical or life sciences research articles
- Constructing complex search queries with Boolean operators, field tags, or MeSH terms
- Conducting systematic literature reviews or meta-analyses
- Accessing PubMed data programmatically via the E-utilities API
- Finding articles by specific criteria (author, journal, publication date, article type)
- Retrieving citation information, abstracts, or full-text articles
- Working with PMIDs (PubMed IDs) or DOIs
- Creating automated workflows for literature monitoring or data extraction

## Core Capabilities

### 1. Advanced Search Query Construction

Construct sophisticated PubMed queries using Boolean operators, field tags, and specialized syntax.

**Basic Search Strategies**:
- Combine concepts with Boolean operators (AND, OR, NOT)
- Use field tags to limit searches to specific record parts
- Employ phrase searching with double quotes for exact matches
- Apply wildcards for term variations
- Use proximity searching for terms within specified distances

**Example Queries**:
```
# Recent systematic reviews on diabetes treatment
diabetes mellitus[mh] AND treatment[tiab] AND systematic review[pt] AND 2023:2024[dp]

# Clinical trials comparing two drugs
(metformin[nm] OR insulin[nm]) AND diabetes mellitus, type 2[mh] AND randomized controlled trial[pt]

# Author-specific research
smith ja[au] AND cancer[tiab] AND 2023[dp] AND english[la]
```

**When to consult search_syntax.md**:
- Need a comprehensive list of available field tags
- Require detailed explanation of search operators
- Constructing complex proximity searches
- Understanding automatic term mapping behavior
- Need specific syntax for date ranges, wildcards, or special characters

Grep pattern for field tags: `\[au\]|\[ti\]|\[ab\]|\[mh\]|\[pt\]|\[dp\]`