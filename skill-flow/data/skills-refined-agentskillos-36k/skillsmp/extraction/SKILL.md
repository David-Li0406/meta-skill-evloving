---
name: extraction
description: Document parsing pipeline for financial statements (PDFs, images, CSVs) using OpenRouter vision models. Use this skill when working with statement uploads, parsing, confidence scoring, or supported institutions.
---

# Document Extraction Domain Model

> **Core Definition**: Parsing financial statements using vision models with confidence scoring.

## Data Flow

```mermaid
flowchart TB
    A[Upload PDF/Image/CSV] --> S[Store to Object Storage]
    S --> P[Create PARSING Statement]
    P --> B{File Type}
    B -->|PDF/Image| C["OpenRouter Vision Model"]
    B -->|CSV| D[Structured Parser]
    C --> E[Extract JSON]
    D --> E
    E --> F{Confidence Score}
    F -->|≥85| G[Auto-Accept]
    F -->|60-84| H[Review Queue]
    F -->|<60| I[Manual Entry]
    G --> J[(PostgreSQL)]
    H --> J
```

## Confidence Scoring

| Factor | Weight | Criteria |
|--------|--------|----------|
| Balance Check | 40% | opening + Σtxn ≈ closing (±0.1) |
| Field Completeness | 30% | Required fields present |
| Format Consistency | 20% | Valid date/amount formats |
| Transaction Count | 10% | Reasonable (1-500) |

**Thresholds**:
- ≥85: Auto-accept
- 60-84: Review queue
- <60: Manual entry required

## Supported Institutions

| Institution | Format | Tier |
|-------------|--------|------|
| DBS/POSB | PDF | v1 |
| CMB (China Merchants Bank) | PDF | v1 |
| Maybank | PDF | v1 |
| Wise | PDF/CSV | v1 |
| Brokerage (generic) | PDF/CSV | v1 |
| Insurance (generic) | PDF | v1 |
| OCBC | PDF | Extended |
| MariBank | PDF | Extended |
| GXS | PDF | Extended |

## Data Integrity

To prevent floating-point errors:

1. **AI Output**: LLM prompt requests monetary values as numbers or strings
2. **Pydantic Validation**: **NEVER** use `float` for `amount` fields. **MUST** use `Decimal`
3. **Database Storage**: Stored as `DECIMAL(18,2)`

## Parsing Resilience

- **Bucket auto-create**: storage ensures the bucket exists before upload
- **Orphan cleanup**: if DB persistence fails after upload, the uploaded object is deleted
- **Stuck job supervisor**: statements stuck in `parsing` longer than 30 minutes are marked `rejected`

## Source Files

- **Models**: `apps/backend/src/models/statement.py`
- **Schemas**: `apps/backend/src/schemas/extraction.py`
- **Logic**: `apps/backend/src/services/extraction.py`
- **Validation**: `apps/backend/src/services/validation.py`
- **Storage**: `apps/backend/src/services/storage.py`
