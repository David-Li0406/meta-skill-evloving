---
name: clinpgx-database
description: Use this skill to access ClinPGx pharmacogenomics data for querying gene-drug interactions, CPIC guidelines, and allele functions to support precision medicine and genotype-guided dosing decisions.
---

# ClinPGx Database

## Overview

ClinPGx (Clinical Pharmacogenomics Database) is a comprehensive resource for clinical pharmacogenomics information, serving as a successor to PharmGKB. It consolidates data from PharmGKB, CPIC, and PharmCAT, providing curated information on how genetic variation affects medication response. Users can access gene-drug pairs, clinical guidelines, allele functions, and drug labels for precision medicine applications.

## When to Use This Skill

This skill should be used when:

- **Gene-drug interactions**: Querying how genetic variants affect drug metabolism, efficacy, or toxicity.
- **CPIC guidelines**: Accessing evidence-based clinical practice guidelines for pharmacogenetics.
- **Allele information**: Retrieving allele function, frequency, and phenotype data.
- **Drug labels**: Exploring FDA and other regulatory pharmacogenomic drug labeling.
- **Pharmacogenomic annotations**: Accessing curated literature on gene-drug-disease relationships.
- **Clinical decision support**: Using tools for phenoconversion and custom genotype interpretation.
- **Precision medicine**: Implementing pharmacogenomic testing in clinical practice.
- **Drug metabolism**: Understanding CYP450 and other pharmacogene functions.
- **Personalized dosing**: Finding genotype-guided dosing recommendations.
- **Adverse drug reactions**: Identifying genetic risk factors for drug toxicity.

## Installation and Setup

### Python API Access

The ClinPGx REST API provides programmatic access to all database resources. Basic setup:

```bash
pip install requests
```

### API Endpoint

```python
BASE_URL = "https://api.clinpgx.org/v1/"
```

**Rate Limits**:
- 2 requests per second maximum.
- Excessive requests will result in HTTP 429 (Too Many Requests) response.

**Authentication**: Not required for basic access.

**Data License**: Creative Commons Attribution-ShareAlike 4.0 International License.

For substantial API use, notify the ClinPGx team at api@clinpgx.org.

## Core Capabilities

### 1. Gene Queries

**Retrieve gene information** including function, clinical annotations, and pharmacogenomic significance:

```python
import requests

# Get gene details
response = requests.get("https://api.clinpgx.org/v1/gene/CYP2D6")
gene_data = response.json()
```