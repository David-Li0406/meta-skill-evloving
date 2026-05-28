---
name: gget
description: Use this skill when you need to perform rapid bioinformatics queries across multiple genomic databases for tasks like gene information retrieval, sequence analysis, and enrichment analysis.
---

# gget

## Overview

gget is a command-line bioinformatics tool and Python package providing unified access to 20+ genomic databases and analysis methods. It allows users to query gene information, sequence analysis, protein structures, expression data, and disease associations through a consistent interface. All gget modules work both as command-line tools and as Python functions.

**Important**: The databases queried by gget are continuously updated, which sometimes changes their structure. gget modules are tested automatically on a biweekly basis and updated to match new database structures when necessary.

## Installation

Install gget in a clean virtual environment to avoid conflicts:

```bash
# Using uv (recommended)
uv uv pip install gget

# Or using pip
uv pip install --upgrade gget

# In Python/Jupyter
import gget
```

## Quick Start

Basic usage pattern for all modules:

```bash
# Command-line
gget <module> [arguments] [options]

# Python
gget.module(arguments, options)
```

Most modules return:
- **Command-line**: JSON (default) or CSV with `-csv` flag
- **Python**: DataFrame or dictionary

Common flags across modules:
- `-o/--out`: Save results to file
- `-q/--quiet`: Suppress progress information
- `-csv`: Return CSV format (command-line only)

## Module Categories

### 1. Reference & Gene Information

#### gget ref - Reference Genome Downloads

Retrieve download links and metadata for Ensembl reference genomes.

**Parameters**:
- `species`: Genus_species format (e.g., 'homo_sapiens', 'mus_musculus'). Shortcuts: 'human', 'mouse'
- `-w/--which`: Specify return types (gtf, cdna, dna, cds, cdrna, pep). Default: all
- `-r/--release`: Ensembl release number (default: latest)
- `-l/--list_species`: List available vertebrate species
- `-liv/--list_iv_species`: List available invertebrate species
- `-ftp`: Return only FTP links
- `-d/--download`: Download files (requires curl)

**Examples**:
```bash
# List available species
gget ref --list_species

# Get all reference files for human
gget ref homo_sapiens

# Download only GTF annotation for mouse
gget ref -w gtf -d mouse
```