---
name: ena-database
description: Use this skill when you need to access the European Nucleotide Archive (ENA) to retrieve DNA/RNA sequences, raw reads, genome assemblies, and associated metadata for genomics and bioinformatics applications.
---

# ENA Database

## Overview

The European Nucleotide Archive (ENA) is a comprehensive public repository for nucleotide sequence data and associated metadata. Access and query DNA/RNA sequences, raw reads, genome assemblies, and functional annotations through REST APIs and FTP for genomics and bioinformatics pipelines.

## When to Use This Skill

This skill should be used when:

- Retrieving nucleotide sequences or raw sequencing reads by accession
- Searching for samples, studies, or assemblies by metadata criteria
- Downloading FASTQ files or genome assemblies for analysis
- Querying taxonomic information for organisms
- Accessing sequence annotations and functional data
- Integrating ENA data into bioinformatics pipelines
- Performing cross-reference searches to related databases
- Bulk downloading datasets via FTP or Aspera

## Core Capabilities

### 1. Data Types and Structure

ENA organizes data into hierarchical object types:

- **Studies/Projects**: Group related data and control release dates. Studies are the primary unit for citing archived data.
- **Samples**: Represent units of biomaterial from which sequencing libraries were produced. Samples must be registered before submitting most data types.
- **Raw Reads**: Consist of:
  - **Experiments**: Metadata about sequencing methods, library preparation, and instrument details
  - **Runs**: References to data files containing raw sequencing reads from a single sequencing run
- **Assemblies**: Genome, transcriptome, metagenome, or metatranscriptome assemblies at various completion levels.
- **Sequences**: Assembled and annotated sequences stored in the EMBL Nucleotide Sequence Database, including coding/non-coding regions and functional annotations.
- **Analyses**: Results from computational analyses of sequence data.
- **Taxonomy Records**: Taxonomic information including lineage and rank.

### 2. Programmatic Access

ENA provides multiple REST APIs for data access. Consult the API documentation for detailed endpoint information.

**Key APIs:**

- **ENA Portal API**: Advanced search functionality across all ENA data types
  - Documentation: [ENA Portal API Documentation](https://www.ebi.ac.uk/ena/portal/api/doc)
  - Use for complex queries and metadata searches

- **ENA Browser API**: Direct retrieval of data based on specific criteria.