---
name: gene-database
description: Use this skill when you need to query the NCBI Gene database to search for gene information by symbol or ID, retrieve gene metadata, or perform batch lookups for gene annotation and functional analysis.
---

# Gene Database

## Overview

NCBI Gene is a comprehensive database that integrates gene information from diverse species, providing nomenclature, reference sequences (RefSeqs), chromosomal maps, biological pathways, genetic variations, phenotypes, and cross-references to global genomic resources.

## When to Use This Skill

This skill should be used when working with gene data, including searching by gene symbol or ID, retrieving gene sequences and metadata, analyzing gene functions and pathways, or performing batch gene lookups.

## Quick Start

NCBI provides two main APIs for gene data access:

1. **E-utilities** (Traditional): Full-featured API for all Entrez databases with flexible querying.
2. **NCBI Datasets API** (Newer): Optimized for gene data retrieval with simplified workflows.

Choose E-utilities for complex queries and cross-database searches. Choose the Datasets API for straightforward gene data retrieval with metadata and sequences in a single request.

## Common Workflows

### Search Genes by Symbol or Name

To search for genes by symbol or name across organisms:

1. Use the `scripts/query_gene.py` script with E-utilities ESearch.
2. Specify the gene symbol and organism (e.g., "BRCA1 in human").
3. The script returns matching Gene IDs.

Example query patterns:
- Gene symbol: `insulin[gene name] AND human[organism]`
- Gene with disease: `dystrophin[gene name] AND muscular dystrophy[disease]`
- Chromosome location: `human[organism] AND 17q21[chromosome]`

### Retrieve Gene Information by ID

To fetch detailed information for known Gene IDs:

1. Use `scripts/fetch_gene_data.py` with the Datasets API for comprehensive data.
2. Alternatively, use `scripts/query_gene.py` with E-utilities EFetch for specific formats.
3. Specify the desired output format (JSON, XML, or text).

The Datasets API returns:
- Gene nomenclature and aliases
- Reference sequences (RefSeqs) for transcripts and proteins
- Chromosomal location and mapping
- Gene Ontology (GO) annotations
- Associated publications

### Batch Gene Lookups

For multiple genes simultaneously:

1. Use `scripts/batch_gene_lookup.py` for efficient batch processing.
2. Provide a list of gene symbols or IDs.
3. Specify the organism for symbol-based queries.
4. The script handles rate limiting automatically.