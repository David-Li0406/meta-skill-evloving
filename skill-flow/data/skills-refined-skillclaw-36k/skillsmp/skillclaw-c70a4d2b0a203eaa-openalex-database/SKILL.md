---
name: openalex-database
description: Use this skill when you need to query and analyze scholarly literature using the OpenAlex database, whether for searching academic papers, analyzing research trends, or tracking citations.
---

# OpenAlex Database

## Overview

OpenAlex is a comprehensive open catalog of over 240 million scholarly works, authors, institutions, topics, sources, publishers, and funders. This skill provides tools and workflows for querying the OpenAlex API to search literature, analyze research output, track citations, and conduct bibliometric studies.

## Quick Start

### Basic Setup

Always initialize the client with an email address to access the polite pool (10x rate limit boost):

```python
from scripts.openalex_client import OpenAlexClient

client = OpenAlexClient(email="your-email@example.edu")
```

### Installation Requirements

Install the required package using:

```bash
uv pip install requests
```

No API key is required - OpenAlex is completely open.

## Core Capabilities

### 1. Search for Papers

**Use for**: Finding papers by title, abstract, or topic.

```python
# Simple search
results = client.search_works(
    search="machine learning",
    per_page=100
)

# Search with filters
results = client.search_works(
    search="CRISPR gene editing",
    filter_params={
        "publication_year": ">2020",
        "is_oa": "true"
    },
    sort="cited_by_count:desc"
)
```

### 2. Find Works by Author

**Use for**: Getting all publications by a specific researcher.

Use the two-step pattern (entity name → ID → works):

```python
from scripts.query_helpers import find_author_works

works = find_author_works(
    author_name="Jennifer Doudna",
    client=client,
    limit=100
)
```

**Manual two-step approach**:
```python
# Step 1: Get author ID
author_response = client._make_request(
    '/authors',
    params={'search': 'Jennifer Doudna', 'per-page': 1}
)
author_id = author_response['results'][0]['id'].split('/')[-1]

# Step 2: Get works
works = client.search_works(
    filter_params={"authorships.author.id": author_id}
)
```

### 3. Find Works from Institution

**Use for**: Analyzing research output from universities or organizations.

```python
from scripts.query_helpers import find_institution_works

works = find_institution_works(
    institution_name="Harvard University",
    client=client,
    limit=100
)
```