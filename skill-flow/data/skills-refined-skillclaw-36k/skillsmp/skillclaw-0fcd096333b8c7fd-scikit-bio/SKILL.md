---
name: scikit-bio
description: Use this skill when performing bioinformatics analyses involving biological sequences, alignments, phylogenetics, and microbial ecology.
---

# Skill body

## Overview

scikit-bio is a comprehensive Python library for working with biological data. It supports a variety of bioinformatics analyses, including sequence manipulation, alignment, phylogenetics, microbial ecology, and multivariate statistics.

## When to Use This Skill

This skill should be used when the user:
- Works with biological sequences (DNA, RNA, protein)
- Needs to read/write biological file formats (FASTA, FASTQ, GenBank, Newick, BIOM, etc.)
- Performs sequence alignments or searches for motifs
- Constructs or analyzes phylogenetic trees
- Calculates diversity metrics (alpha/beta diversity, UniFrac distances)
- Performs ordination analysis (PCoA, CCA, RDA)
- Runs statistical tests on biological/ecological data (PERMANOVA, ANOSIM, Mantel)
- Analyzes microbiome or community ecology data
- Works with protein embeddings from language models
- Needs to manipulate biological data tables

## Core Capabilities

### 1. Sequence Manipulation

Work with biological sequences using specialized classes for DNA, RNA, and protein data.

**Key operations:**
- Read/write sequences from FASTA, FASTQ, GenBank, EMBL formats
- Sequence slicing, concatenation, and searching
- Reverse complement, transcription (DNA→RNA), and translation (RNA→protein)
- Find motifs and patterns using regex
- Calculate distances (Hamming, k-mer based)
- Handle sequence quality scores and metadata

**Common patterns:**
```python
import skbio

# Read sequences from file
seq = skbio.DNA.read('input.fasta')

# Sequence operations
rc = seq.reverse_complement()
rna = seq.transcribe()
protein = rna.translate()

# Find motifs
motif_positions = seq.find_with_regex('ATG[ACGT]{3}')

# Check for properties
has_degens = seq.has_degenerates()
seq_no_gaps = seq.degap()
```

**Important notes:**
- Use `DNA`, `RNA`, `Protein` classes for grammared sequences with validation.
- Use `Sequence` class for generic sequences without alphabet restrictions.
- Quality scores are automatically loaded from FASTQ files into positional metadata.
- Metadata types include sequence-level (ID, description), positional (per-base), and interval (regions/features).

### 2. Sequence Alignment

Perform pairwise and multiple sequence alignments using dynamic programming algorithms.

**Key capabilities:**
- Implement various alignment algorithms (e.g., Needleman-Wunsch, Smith-Waterman).
- Analyze alignment scores and visualize results.

### 3. Phylogenetic Analysis

Construct and analyze phylogenetic trees.

**Key capabilities:**
- Build trees from sequence data using distance methods or maximum likelihood.
- Visualize trees and assess evolutionary relationships.

### 4. Diversity Metrics

Calculate and analyze diversity metrics for ecological data.

**Key capabilities:**
- Compute alpha and beta diversity metrics.
- Perform UniFrac analysis for microbial community comparisons.

### 5. Ordination Techniques

Conduct ordination analyses to visualize complex ecological data.

**Key capabilities:**
- Implement techniques like Principal Coordinates Analysis (PCoA), Canonical Correspondence Analysis (CCA), and Redundancy Analysis (RDA).
```