---
name: reactome-database
description: Use this skill when you need to query the Reactome REST API for pathway analysis, enrichment, gene-pathway mapping, and molecular interactions in systems biology studies.
---

# Skill Body

## Overview

Reactome is a free, open-source, curated pathway database with over 2,825 human pathways. It allows users to query biological pathways, perform overrepresentation and expression analysis, map genes to pathways, and explore molecular interactions via a REST API and a Python client.

## When to Use This Skill

This skill should be used when:
- Performing pathway enrichment analysis on gene or protein lists.
- Analyzing gene expression data to identify relevant biological pathways.
- Querying specific pathway information, reactions, or molecular interactions.
- Mapping genes or proteins to biological pathways and processes.
- Exploring disease-related pathways and mechanisms.
- Visualizing analysis results in the Reactome Pathway Browser.
- Conducting comparative pathway analysis across species.

## Core Capabilities

Reactome provides two main API services and a Python client library:

### 1. Content Service - Data Retrieval

Query and retrieve biological pathway data, molecular interactions, and entity information.

**Common operations:**
- Retrieve pathway information and hierarchies.
- Query specific entities (proteins, reactions, complexes).
- Get participating molecules in pathways.
- Access database version and metadata.
- Explore pathway compartments and locations.

**API Base URL:** `https://reactome.org/ContentService`

### 2. Analysis Service - Pathway Analysis

Perform computational analysis on gene lists and expression data.

**Analysis types:**
- **Overrepresentation Analysis**: Identify statistically significant pathways from gene/protein lists.
- **Expression Data Analysis**: Analyze gene expression datasets to find relevant pathways.
- **Species Comparison**: Compare pathway data across different organisms.

**API Base URL:** `https://reactome.org/AnalysisService`

### 3. reactome2py Python Package

A Python client library that wraps Reactome API calls for easier programmatic access.

**Installation:**
```bash
pip install reactome2py
```

**Note:** The reactome2py package (version 3.0.0, released January 2021) is functional but not actively maintained. For the most up-to-date functionality, consider using direct REST API calls.