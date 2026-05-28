---
name: data-pipeline
description: This skill should be used when the user asks to "generate a pipeline", "create ETL", "build ELT", "ingest data", or "load data into warehouse".
---

# /data-pipeline

Generate ETL/ELT pipeline code from profiled data or specifications.

## Instructions

### 1. Gather Requirements

If not already provided, ask for:

- **Source**: File format (CSV, Excel, PDF, DOCX) or data profile output
- **Destination**: Database, warehouse, or file format
- **Pattern**: ETL (transform before load) or ELT (load then transform)
- **Orchestration**: Airflow, Prefect, Dagster, or standalone Python
- **Schedule**: One-time, daily, hourly, or event-driven

### 2. Choose Pipeline Pattern

Based on requirements, select the appropriate pattern:

| Pattern          | When to Use                                 |
| ---------------- | ------------------------------------------- |
| **Batch ETL**    | File-based sources, daily/hourly loads      |
| **Batch ELT**    | Raw load to staging, transform in warehouse |
| **Incremental**  | Large datasets with timestamp/ID columns    |
| **Full Refresh** | Small datasets, dimension tables            |
| **CDC**          | Real-time changes from databases            |

### 3. Generate Pipeline Code

#### For Standalone Python

```python
# pipeline.py
import pandas as pd
from pathlib import Path

def extract(source_path: str) -> pd.DataFrame:
    """Extract data from source file."""
    # Implementation based on file type
    pass

def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Apply business transformations."""
    # Type conversions, cleaning, derivations
    pass

def load(df: pd.DataFrame, target: str) -> int:
    """Load data to destination."""
    # Database insert, file write, etc.
    pass

def run_pipeline(source: str, target: str) -> dict:
    """Execute full pipeline with metrics."""
    df = extract(source)
    df = transform(df)
    rows = load(df, target)
    return {"rows_processed": rows}
```

#### For Airflow DAG

```python
# dags/ingest_{source_name}.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "data-team",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="ingest_{source_name}",
    default_args=default_args,
    schedule_interval="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["ingest", "{source_type}"],
) as dag:

    extract_task = PythonOperator(
        task_id="extract",
        python_callable=extract_fn,
    )

    transform_task = PythonOperator(
        task_id="transform",
        python_callable=transform_fn,
    )

    load_task = PythonOperator(
        task_id="load",
        python_callable=load_fn,
    )

    extract_task >> transform_task >> load_task
```

#### For SQL Transformations (ELT)

```sql
-- models/staging/stg_{source_name}.sql
WITH source AS (
    SELECT * FROM {{ source('{schema}', '{table}_raw') }}
),

cleaned AS (
    SELECT
        -- Type casting
        CAST(id AS INTEGER) AS id,
        TRIM(name) AS name,
        -- Date parsing
        TO_DATE(date_col, 'YYYY-MM-DD') AS date_col,
        -- Null handling
        COALESCE(amount, 0) AS amount,
        -- Timestamps
        CURRENT_TIMESTAMP AS _loaded_at
    FROM source
    WHERE id IS NOT NULL  -- Filter invalid records
)

SELECT * FROM cleaned
```

### 4. Include Data Quality Checks

Always generate corresponding tests:

```python
def test_no_nulls_in_pk(df: pd.DataFrame, pk_col: str) -> bool:
    """Primary key should never be null."""
    return df[pk_col].notna().all()

def test_row_count_reasonable(df: pd.DataFrame, min_rows: int = 1) -> bool:
    """Should have at least minimum expected rows."""
    return len(df) >= min_rows

def test_no_duplicates(df: pd.DataFrame, pk_col: str) -> bool:
    """No duplicate primary keys."""
    return df[pk_col].is_unique
```

### 5. Output Structure

Provide the user with:

```
## Generated Pipeline

### Files Created
- `{path}/extract.py` - Source extraction logic
- `{path}/transform.py` - Transformation functions
- `{path}/load.py` - Destination loading
- `{path}/pipeline.py` - Orchestration entry point
- `{path}/tests/` - Data quality tests

### Configuration
- Source: {source_description}
- Target: {target_description}
- Schedule: {schedule}
- Incremental Key: {column or "N/A"}

### Data Flow
{source} -> extract -> transform -> load -> {target}

### Next Steps
1. Review generated code
2. Configure credentials (env vars)
3. Run tests locally
4. Deploy to orchestrator
```

## File Format Handlers

### CSV/TSV

```python
def extract_csv(path: str, **kwargs) -> pd.DataFrame:
    return pd.read_csv(
        path,
        encoding=kwargs.get("encoding", "utf-8"),
        sep=kwargs.get("delimiter", ","),
        dtype=str,  # Read all as string, cast later
    )
```

### Excel

```python
def extract_excel(path: str, sheet: str = None) -> pd.DataFrame:
    return pd.read_excel(
        path,
        sheet_name=sheet or 0,
        dtype=str,
    )
```

### PDF

```python
def extract_pdf_tables(path: str) -> list[pd.DataFrame]:
    import pdfplumber
    tables = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables():
                if table:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    tables.append(df)
    return tables
```

### DOCX

```python
def extract_docx_tables(path: str) -> list[pd.DataFrame]:
    from docx import Document
    doc = Document(path)
    tables = []
    for table in doc.tables:
        data = [[cell.text for cell in row.cells] for row in table.rows]
        if data:
            df = pd.DataFrame(data[1:], columns=data[0])
            tables.append(df)
    return tables
```

## Best Practices

- **Idempotent**: Pipeline should be safe to re-run
- **Atomic**: All-or-nothing loading (use transactions)
- **Observable**: Log row counts, timing, errors
- **Testable**: Include data quality assertions
- **Configurable**: Use env vars for paths, credentials
