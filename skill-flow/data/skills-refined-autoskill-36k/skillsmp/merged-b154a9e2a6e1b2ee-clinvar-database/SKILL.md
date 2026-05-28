---
name: clinvar-database
description: Query NCBI ClinVar for variant clinical significance. Search by gene/position, interpret pathogenicity classifications, access via E-utilities API or FTP, annotate VCFs, for genomic medicine.
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

Search ClinVar using the web interface at https://www.ncbi.nlm.nih.gov/clinvar/

**Common search patterns:**
- By gene: `<gene>[gene]`
- By clinical significance: `pathogenic[CLNSIG]`
- By condition: `<condition>[disorder]`
- By variant: `<variant name>[variant name]`
- By chromosome: `<chromosome>[chr]`
- Combined: `<gene>[gene] AND pathogenic[CLNSIG]`

#### Programmatic Access via E-utilities

Access ClinVar programmatically using NCBI's E-utilities API. Refer to the API documentation for comprehensive details including:
- **esearch** - Search for variants matching criteria
- **esummary** - Retrieve variant summaries
- **efetch** - Download full XML records
- **elink** - Find related records in other NCBI databases

**Quick example using curl:**
```bash
# Search for pathogenic variants
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term=<gene>[gene]+AND+pathogenic[CLNSIG]&retmode=json"
```

**Best practices:**
- Test queries on the web interface before automating
- Use API keys to increase rate limits from 3 to 10 requests/second
- Implement exponential backoff for rate limit errors
- Set `Entrez.email` when using Biopython

### 2. Interpret Clinical Significance

#### Understanding Classifications

ClinVar uses standardized terminology for variant classifications. Key germline classification terms (ACMG/AMP) include:
- **Pathogenic (P)** - Variant causes disease (~99% probability)
- **Likely Pathogenic (LP)** - Variant likely causes disease (~90% probability)
- **Uncertain Significance (VUS)** - Insufficient evidence to classify
- **Likely Benign (LB)** - Variant likely does not cause disease
- **Benign (B)** - Variant does not cause disease

**Review status (star ratings):**
- ★★★★ Practice guideline - Highest confidence
- ★★★ Expert panel review (e.g., ClinGen) - High confidence
- ★★ Multiple submitters, no conflicts - Moderate confidence
- ★ Single submitter with criteria - Standard weight
- ☆ No assertion criteria - Low confidence

**Critical considerations:**
- Always check review status - prefer ★★★ or ★★★★ ratings
- Conflicting interpretations require manual evaluation
- Classifications may change as new evidence emerges
- VUS (uncertain significance) variants lack sufficient evidence for clinical use

### 3. Download Bulk Data from FTP

#### Access ClinVar FTP Site

Download complete datasets from `ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/`

**Update schedule:**
- Monthly releases: First Thursday of each month (complete dataset, archived)
- Weekly updates: Every Monday (incremental updates)

#### Available Formats

**XML files** (most comprehensive):
- VCV (Variation) files: `xml/clinvar_variation/` - Variant-centric aggregation
- RCV (Record) files: `xml/RCV/` - Variant-condition pairs

**VCF files** (for genomic pipelines):
- GRCh37: `vcf_GRCh37/clinvar.vcf.gz`
- GRCh38: `vcf_GRCh38/clinvar.vcf.gz`
- Limitations: Excludes variants >10kb and complex structural variants

**Tab-delimited files** (for quick analysis):
- `tab_delimited/variant_summary.txt.gz` - Summary of all variants

**Example download:**
```bash
# Download latest monthly XML release
wget ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/xml/clinvar_variation/ClinVarVariationRelease_00-latest.xml.gz

# Download VCF for GRCh38
wget ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz
```

### 4. Process and Analyze ClinVar Data

#### Working with XML Files

Process XML files to extract variant details, classifications, and evidence.

**Python example with xml.etree:**
```python
import gzip
import xml.etree.ElementTree as ET

with gzip.open('ClinVarVariationRelease.xml.gz', 'rt') as f:
    for event, elem in ET.iterparse(f, events=('end',)):
        if elem.tag == 'VariationArchive':
            variation_id = elem.attrib.get('VariationID')
            # Extract clinical significance, review status, etc.
            elem.clear()  # Free memory
```

#### Working with VCF Files

Annotate variant calls or filter by clinical significance using bcftools or Python.

**Using bcftools:**
```bash
# Filter pathogenic variants
bcftools view -i 'INFO/CLNSIG~"Pathogenic"' clinvar.vcf.gz

# Annotate your VCF with ClinVar
bcftools annotate -a clinvar.vcf.gz -c INFO your_variants.vcf
```

#### Working with Tab-Delimited Files

Use pandas or command-line tools for rapid filtering and analysis.

**Using pandas:**
```python
import pandas as pd

# Load variant summary
df = pd.read_csv('variant_summary.txt.gz', sep='\t', compression='gzip')

# Filter pathogenic variants in specific gene
pathogenic_brca = df[
    (df['GeneSymbol'] == 'BRCA1') &
    (df['ClinicalSignificance'].str.contains('Pathogenic', na=False))
]
```

### 5. Handle Conflicting Interpretations

When multiple submitters provide different classifications for the same variant, ClinVar reports "Conflicting interpretations of pathogenicity."

**Resolution strategy:**
1. Check review status (star rating) - higher ratings carry more weight
2. Examine evidence and assertion criteria from each submitter
3. Consider submission dates - newer submissions may reflect updated evidence
4. Review population frequency data (e.g., gnomAD) for context
5. Consult expert panel classifications (★★★) when available

### 6. Track Classification Updates

Variant classifications may change over time as new evidence emerges.

**Best practices:**
- Document ClinVar version and access date for reproducibility
- Re-check classifications periodically for critical variants
- Subscribe to ClinVar mailing list for major updates

### 7. Submit Data to ClinVar

Organizations can submit variant interpretations to ClinVar.

**Submission methods:**
- Web submission portal: https://submit.ncbi.nlm.nih.gov/subs/clinvar/
- API submission (requires service account)

**Requirements:**
- Organizational account with NCBI
- Assertion criteria (preferably ACMG/AMP guidelines)
- Supporting evidence for classification

## Important Limitations and Considerations

### Data Quality
- **Not all submissions have equal weight** - Check review status (star ratings)
- **Conflicting interpretations exist** - Require manual evaluation

### Scope Limitations
- **Not for direct clinical diagnosis** - Always involve genetics professional

### Technical Limitations
- **VCF files exclude large variants** - Variants >10kb not in VCF format
- **Rate limits on API** - 3 req/sec without key, 10 req/sec with API key

## Resources

### Reference Documentation
- **API documentation** - Complete E-utilities API documentation with examples for esearch, esummary, efetch, and elink.

### External Resources
- ClinVar home: https://www.ncbi.nlm.nih.gov/clinvar/
- ClinVar documentation: https://www.ncbi.nlm.nih.gov/clinvar/docs/

### Contact
For questions about ClinVar or data submission: clinvar@ncbi.nlm.nih.gov