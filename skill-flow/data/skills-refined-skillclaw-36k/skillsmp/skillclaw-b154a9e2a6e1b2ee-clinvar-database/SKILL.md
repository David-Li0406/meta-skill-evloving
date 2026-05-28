---
name: clinvar-database
description: Use this skill when you need to query NCBI ClinVar for variant clinical significance, interpret pathogenicity classifications, or access data programmatically via the E-utilities API or FTP.
---

# ClinVar Database

## Overview

ClinVar is NCBI's freely accessible archive of reports on relationships between human genetic variants and phenotypes, with supporting evidence. The database aggregates information about genomic variation and its relationship to human health, providing standardized variant classifications used in clinical genetics and research.

## When to Use This Skill

This skill should be used when:

- Searching for variants by gene, condition, or clinical significance
- Interpreting clinical significance classifications (pathogenic, benign, VUS)
- Accessing ClinVar data programmatically via E-utilities API
- Downloading and processing bulk data from FTP
- Understanding review status and star ratings
- Resolving conflicting variant interpretations
- Annotating variant call sets with clinical significance

## Core Capabilities

### 1. Search and Query ClinVar

#### Web Interface Queries

Search ClinVar using the web interface at [NCBI ClinVar](https://www.ncbi.nlm.nih.gov/clinvar/).

**Common search patterns:**
- By gene: `BRCA1[gene]`
- By clinical significance: `pathogenic[CLNSIG]`
- By condition: `breast cancer[disorder]`
- By variant: `NM_000059.3:c.1310_1313del[variant name]`
- By chromosome: `13[chr]`
- Combined: `BRCA1[gene] AND pathogenic[CLNSIG]`

#### Programmatic Access via E-utilities

Access ClinVar programmatically using NCBI's E-utilities API. Refer to the API documentation for comprehensive details including:
- **esearch** - Search for variants matching criteria
- **esummary** - Retrieve variant summaries
- **efetch** - Download full XML records
- **elink** - Find related records in other NCBI databases

**Quick example using curl:**
```bash
# Search for pathogenic BRCA1 variants
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term=BRCA1[gene]+AND+pathogenic[CLNSIG]&retmode=json"
```

**Best practices:**
- Test queries on the web interface before automating
- Use API keys to increase rate limits from 3 to 10 requests/second
- Implement exponential backoff for rate limit errors
- Set `Entrez.email` when using Biopython

### 2. Interpret Clinical Significance

#### Understanding Classifications

ClinVar uses standardized terminology for variant classifications, which include:
- **Pathogenic**: Variants that are known to cause disease.
- **Benign**: Variants that are not associated with disease.
- **Variant of Uncertain Significance (VUS)**: Variants for which the clinical significance is not yet established.

### 3. Downloading and Processing Bulk Data

You can download bulk data from ClinVar via FTP for local analysis. For example:
```bash
# Download ClinVar VCF for GRCh38
wget https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz
```

### 4. Annotating Variant Call Sets

Use the information from ClinVar to annotate your variant call format (VCF) files with clinical significance, aiding in genomic medicine applications.