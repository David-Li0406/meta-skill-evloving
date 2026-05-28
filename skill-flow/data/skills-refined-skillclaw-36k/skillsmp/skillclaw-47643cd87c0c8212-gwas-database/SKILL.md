---
name: gwas-database
description: Use this skill when you need to query the NHGRI-EBI GWAS Catalog for SNP-trait associations, including searching by rs ID, disease/trait, or gene, and retrieving p-values and summary statistics for genetic epidemiology and polygenic risk scores.
---

# GWAS Catalog Database

## Overview

The GWAS Catalog is a comprehensive repository of published genome-wide association studies maintained by the National Human Genome Research Institute (NHGRI) and the European Bioinformatics Institute (EBI). It contains curated SNP-trait associations from thousands of GWAS publications, including genetic variants, associated traits and diseases, p-values, effect sizes, and full summary statistics.

## When to Use This Skill

This skill should be used when queries involve:

- **Genetic variant associations**: Finding SNPs associated with diseases or traits.
- **SNP lookups**: Retrieving information about specific genetic variants (rs IDs).
- **Trait/disease searches**: Discovering genetic associations for phenotypes.
- **Gene associations**: Finding variants in or near specific genes.
- **GWAS summary statistics**: Accessing complete genome-wide association data.
- **Study metadata**: Retrieving publication and cohort information.
- **Population genetics**: Exploring ancestry-specific associations.
- **Polygenic risk scores**: Identifying variants for risk prediction models.
- **Functional genomics**: Understanding variant effects and genomic context.
- **Systematic reviews**: Comprehensive literature synthesis of genetic associations.

## Core Capabilities

### 1. Understanding GWAS Catalog Data Structure

The GWAS Catalog is organized around four core entities:

- **Studies**: GWAS publications with metadata (PMID, author, cohort details).
- **Associations**: SNP-trait associations with statistical evidence (p ≤ 5×10⁻⁸).
- **Variants**: Genetic markers (SNPs) with genomic coordinates and alleles.
- **Traits**: Phenotypes and diseases (mapped to EFO ontology terms).

**Key Identifiers:**
- Study accessions: `GCST` IDs (e.g., GCST001234).
- Variant IDs: `rs` numbers (e.g., rs7903146) or `variant_id` format.
- Trait IDs: EFO terms (e.g., EFO_0001360 for type 2 diabetes).
- Gene symbols: HGNC approved names (e.g., TCF7L2).

### 2. Web Interface Searches

The web interface at [EBI GWAS Catalog](https://www.ebi.ac.uk/gwas/) supports multiple search modes:

**By Variant (rs ID):**
```
rs7903146
```
Returns all trait associations for this SNP.

**By Disease/Trait:**
```
type 2 diabetes
```
Returns all SNPs associated with this trait.