---
name: bio-entrez
description: Use this skill to interact with NCBI databases via Biopython's Entrez module for searching, fetching records, and navigating cross-database links.
---

# Bio Entrez

This skill allows you to search, fetch, and link records across various NCBI databases using Biopython's Entrez module.

## Required Setup

```python
from Bio import Entrez

Entrez.email = 'your.email@example.com'  # Required by NCBI
Entrez.api_key = 'your_api_key'          # Optional, raises rate limit 3->10 req/sec
```

## Core Functions

### 1. Search NCBI Databases

#### `Entrez.esearch()`

Search any NCBI database and get matching record IDs.

```python
handle = Entrez.esearch(db='nucleotide', term='human[orgn] AND BRCA1[gene]')
record = Entrez.read(handle)
handle.close()

print(f"Found {record['Count']} records")
print(f"IDs: {record['IdList']}")  # First 20 IDs by default
```

**Key Parameters:**
| Parameter | Description | Default |
|-----------|-------------|---------|
| `db` | Database to search | Required |
| `term` | Search query | Required |
| `retmax` | Max IDs to return | 20 |
| `retstart` | Starting index (pagination) | 0 |
| `usehistory` | Store results on server | 'n' |

### 2. Fetch Records

#### `Entrez.efetch()`

Fetch complete records in various formats from any NCBI database.

```python
# Fetch GenBank record by ID
handle = Entrez.efetch(db='nucleotide', id='NM_007294', rettype='gb', retmode='text')
genbank_text = handle.read()
handle.close()
```

**Key Parameters:**
| Parameter | Description | Example |
|-----------|-------------|---------|
| `db` | Database name | `'nucleotide'`, `'protein'` |
| `id` | Record ID(s) | `'NM_007294'` or `'123,456,789'` |
| `rettype` | Return type | `'fasta'`, `'gb'` |
| `retmode` | Return mode | `'text'`, `'xml'` |

### 3. Cross-Database Links

#### `Entrez.elink()`

Find related records in the same or different databases.

```python
# Find proteins linked to a gene
handle = Entrez.elink(dbfrom='gene', db='protein', id='672')
record = Entrez.read(handle)
handle.close()

# Extract linked IDs
linkset = record[0]
if linkset['LinkSetDb']:
    links = linkset['LinkSetDb'][0]['Link']
    protein_ids = [link['Id'] for link in links]
    print(f"Found {len(protein_ids)} linked proteins")
```

**Key Parameters:**
| Parameter | Description | Example |
|-----------|-------------|---------|
| `dbfrom` | Source database | `'gene'` |
| `db` | Target database | `'protein'` |
| `id` | Source record ID(s) | `'672'` |

## Common Use Cases

- **Searching**: Use `esearch` to find records by keywords.
- **Fetching**: Use `efetch` to download sequences or records.
- **Linking**: Use `elink` to navigate between related records across databases.