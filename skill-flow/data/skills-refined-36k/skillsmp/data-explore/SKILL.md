---
name: data-explore
description: Explore Hive tables and datasets in the Wellcome Collection data warehouse. Use this skill to query tables, understand schemas, or analyze data distributions. Invoke with /data-explore.
---

# Data Exploration

This skill helps explore the Wellcome Collection data warehouse stored in Hive tables.

## Available Tables

### Core Tables
| Table | Records | Description |
|-------|---------|-------------|
| `works` | 738,073 | Wellcome Collection works catalog |
| `images` | 128,755 | Image metadata from IIIF manifests |
| `iiif_manifests` | ~340,000 | IIIF manifest metadata |
| `iiif_canvases` | ~42M | Page-level canvas data |

### Text Tables
| Table | Records | Description |
|-------|---------|-------------|
| `alto_text` | ~226,000 | OCR text from works (9.8B words total) |
| `alto_sentence` | ~550M | Sentence-level text |
| `alto_text_chunks` | ~74M | Text chunks for embedding |

### Embedding Tables
| Table | Description |
|-------|-------------|
| `vlm_embeddings` | VLM image embeddings (1536-dim) |
| `text_embeddings` | Qwen3 text embeddings |

### Label Tables
| Table | Records | Description |
|-------|---------|-------------|
| `dn_labels` | 646,786 | Combined genres/subjects/contributors |

## Quick Start

### Connect to Spark
```python
from wc_simd.utility import get_spark_session
spark = get_spark_session()
```

### List Tables
```python
spark.sql("SHOW TABLES").show()
```

### Explore Schema
```python
spark.table("works").printSchema()
```

### Sample Data
```python
spark.table("works").show(10, truncate=False)
```

### Count Records
```python
spark.table("works").count()
```

## Common Queries

### Works with OCR Text
```sql
SELECT COUNT(*) FROM works w
JOIN alto_text t ON w.id = t.id
```

### Genre Distribution
```sql
SELECT genre.label, COUNT(*) as cnt
FROM works
LATERAL VIEW explode(genres) AS genre
GROUP BY genre.label
ORDER BY cnt DESC
LIMIT 20
```

### Subject Distribution
```sql
SELECT subject.label, COUNT(*) as cnt
FROM works
LATERAL VIEW explode(subjects) AS subject
GROUP BY subject.label
ORDER BY cnt DESC
LIMIT 20
```

### Concept Types
```sql
SELECT concept.type, COUNT(*) as cnt
FROM works
LATERAL VIEW explode(subjects) AS subject
LATERAL VIEW explode(subject.concepts) AS concept
GROUP BY concept.type
```

## Key Statistics

- **Total words**: 9.8 billion (~12,500 King James Bibles)
- **Text chunks**: 74.3 million (1000 chars, 200 overlap)
- **Languages**: 78.9% English
- **Genre labels**: 1,523 unique
- **Subject labels**: 204,322 unique
- **Concept labels**: 126,714 unique
