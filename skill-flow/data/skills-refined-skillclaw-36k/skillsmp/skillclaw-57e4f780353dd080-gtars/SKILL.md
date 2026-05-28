---
name: gtars
description: Use this skill when working with genomic interval data, such as BED files, for tasks like overlap detection, coverage track generation, and machine learning preprocessing in computational genomics.
---

# Gtars: Genomic Tools and Algorithms in Rust

## Overview

Gtars is a high-performance Rust toolkit for manipulating, analyzing, and processing genomic interval data. It provides specialized tools for overlap detection, coverage analysis, tokenization for machine learning, and reference sequence management.

Use this skill when working with:
- Genomic interval files (BED format)
- Overlap detection between genomic regions
- Coverage track generation (WIG, BigWig)
- Genomic ML preprocessing and tokenization
- Fragment analysis in single-cell genomics
- Reference sequence retrieval and validation

## Installation

### Python Installation

Install gtars Python bindings:

```bash
pip install gtars
```

### CLI Installation

Install command-line tools (requires Rust/Cargo):

```bash
# Install with all features
cargo install gtars-cli --features "uniwig overlaprs igd bbcache scoring fragsplit"

# Or install specific features only
cargo install gtars-cli --features "uniwig overlaprs"
```

### Rust Library

Add to Cargo.toml for Rust projects:

```toml
[dependencies]
gtars = { version = "0.1", features = ["tokenizers", "overlaprs"] }
```

## Core Capabilities

Gtars is organized into specialized modules, each focused on specific genomic analysis tasks:

### 1. Overlap Detection and IGD Indexing

Efficiently detect overlaps between genomic intervals using the Integrated Genome Database (IGD) data structure.

**When to use:**
- Finding overlapping regulatory elements
- Variant annotation
- Comparing ChIP-seq peaks
- Identifying shared genomic features

**Quick example:**
```python
import gtars

# Build IGD index and query overlaps
igd = gtars.igd.build_index("regions.bed")
overlaps = igd.query("chr1", 1000, 2000)
```

### 2. Coverage Track Generation

Generate coverage tracks from sequencing data with the uniwig module.

**When to use:**
- ATAC-seq accessibility profiles
- ChIP-seq coverage visualization
- RNA-seq read coverage
- Differential coverage analysis

**Quick example:**
```bash
# Generate BigWig coverage track
gtars uniwig generate --input fragments.bed --output coverage.bw
```