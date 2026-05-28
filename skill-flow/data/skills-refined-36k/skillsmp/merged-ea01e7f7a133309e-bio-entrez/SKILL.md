---
name: bio-entrez
description: Use this skill to search, retrieve, and link records across NCBI databases using Biopython's Bio.Entrez module. Ideal for fetching sequences, summaries, and navigating relationships between genes, proteins, and publications.
---

# Entrez Workflow

This skill encompasses searching, fetching, and linking records from NCBI databases using Biopython's Entrez module.

## Required Setup

```python
from Bio import Entrez

Entrez.email = 'your.email@example.com'  # Required by NCBI
Entrez.api_key = 'your_api_key'          # Optional, raises rate limit
```

## Core Functions

### Search NCBI Databases

#### Entrez.esearch() - Search a Database

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

### Retrieve Records

#### Entrez.efetch() - Retrieve Full Records

Fetch complete records in various formats from any NCBI database.

```python
handle = Entrez.efetch(db='nucleotide', id='NM_007294', rettype='gb', retmode='text')
genbank_text = handle.read()
handle.close()
```

### Get Document Summaries

#### Entrez.esummary() - Document Summaries

Get brief summaries without downloading full records.

```python
handle = Entrez.esummary(db='nucleotide', id='NM_007294')
record = Entrez.read(handle)
handle.close()

summary = record[0]  # First (only) record
print(f"Title: {summary['Title']}")
```

### Cross-Database Links

#### Entrez.elink() - Cross-Database Links

Find related records in the same or different databases.

```python
handle = Entrez.elink(dbfrom='gene', db='protein', id='672')
record = Entrez.read(handle)
handle.close()

if record[0]['LinkSetDb']:
    links = record[0]['LinkSetDb'][0]['Link']
    protein_ids = [link['Id'] for link in links]
    print(f"Found {len(protein_ids)} linked proteins")
```

## Common Use Cases

### Fetch Sequence by Accession

```python
def fetch_sequence(accession, db='nucleotide'):
    handle = Entrez.efetch(db=db, id=accession, rettype='fasta', retmode='text')
    record = SeqIO.read(handle, 'fasta')
    handle.close()
    return record
```

### Search and Fetch

```python
def search_and_fetch(db, term):
    handle = Entrez.esearch(db=db, term=term, usehistory='y')
    record = Entrez.read(handle)
    handle.close()
    webenv = record['WebEnv']
    query_key = record['QueryKey']
    
    # Fetch records using webenv and query_key
    handle = Entrez.efetch(db=db, webenv=webenv, query_key=query_key, rettype='fasta', retmode='text')
    records = handle.read()
    handle.close()
    return records
```

### Get Related Publications

```python
def get_related_articles(pmid):
    handle = Entrez.elink(dbfrom='pubmed', db='pubmed', id=pmid, linkname='pubmed_pubmed')
    record = Entrez.read(handle)
    handle.close()
    return [link['Id'] for link in record[0]['LinkSetDb'][0]['Link']]
```

## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `HTTPError 429` | Rate limit exceeded | Add delays or use API key |
| `HTTPError 400` | Invalid query syntax | Check field names and operators |
| Empty IdList | No matches or typo | Check QueryTranslation field |

## Decision Tree

```
Need to search NCBI?
├── Finding records in one database?
│   └── Use Entrez.esearch()
├── Need to fetch actual records?
│   └── Use Entrez.efetch() after searching
├── Need to find related records?
│   └── Use Entrez.elink()
└── Need summaries without full records?
    └── Use Entrez.esummary()
```

## Related Skills

- **entrez-fetch** - Retrieve full records after searching
- **entrez-link** - Find related records in other databases
- **batch-downloads** - Download large result sets efficiently