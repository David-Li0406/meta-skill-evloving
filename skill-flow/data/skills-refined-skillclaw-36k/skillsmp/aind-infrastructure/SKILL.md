---
name: aind-infrastructure
description: Knowledge about AIND data infrastructure including MongoDB/DocumentDB access patterns, S3 asset storage, collection schemas, and query patterns. Use when working with AIND analysis results, querying metadata, or accessing stored assets.
---

# AIND Analysis Infrastructure

This skill captures knowledge about the Allen Institute for Neural Dynamics (AIND) data infrastructure for analysis results.

## Overview

AIND stores analysis results in a two-tier system:
1. **MongoDB (DocumentDB)**: Metadata and pointers to S3 assets
2. **S3**: Actual result files (figures, tables, videos)

## MongoDB Access

### Connection Pattern

Use `aind-data-access-api` for DocumentDB access:

```python
from aind_data_access_api.document_db import MetadataDbClient

client = MetadataDbClient(
    host="api.allenneuraldynamics.org",  # Public API endpoint
    database="analysis",                  # Analysis database
    collection="<collection-name>",       # Project-specific collection
)
```

### One Collection Per Project

Each analysis project has its own collection. Examples:
- `dynamic-foraging-model-fitting` - Foraging behavior MLE fitting
- Other projects follow same pattern

### Query Patterns

```python
# Basic query - old format only
records = client.retrieve_docdb_records(
    filter_query={"status": "success"},
    projection={"_id": 1, "subject_id": 1, "s3_location": 1},
    paginate=False,  # Set True for large queries
)

# Query for new format
records = client.retrieve_docdb_records(
    filter_query={"processing.data_processes.output_parameters.additional_info": "success"},
    projection={"_id": 1, "location": 1},
    paginate=False,
)
```

**Note:** Due to the two different formats, it's recommended to use `aind-analysis-arch-result-access` which handles both formats automatically.

### Two Pipeline Formats

AIND has two analysis pipeline formats with different document structures:

#### 1. Prototype Pipeline (older format)

Flat structure with fields at root level:

```json
{
  "_id": "fe96ff6c9e7b...",  // SHA256 hash
  "subject_id": "744040",
  "session_date": "2024-12-09",
  "status": "success",
  "s3_location": "s3://aind-dynamic-foraging-analysis-prod-o5171v/fe96ff6c...",
  "analysis_datetime": "2025-01-18T05:14:46.722265",
  "nwb_name": "744040_2024-12-09_13-30-23.nwb",
  "analysis_spec": {
    "analysis_name": "MLE fitting",
    "analysis_args": { ... }
  },
  "analysis_results": {
    "fit_settings": { "agent_alias": "QLearning_L1F1_CK1_softmax", ... },
    "params": { ... },
    "log_likelihood": -144.83,
    "AIC": 299.67,
    "BIC": 319.50,
    "n_trials": 390,
    "prediction_accuracy": 0.807,
    "cross_validation": { ... }
  }
}
```

**Key paths:**
- `subject_id` → root level
- `session_date` → root level
- `status` → root level
- S3 location → `s3_location`
- Fitting results → `analysis_results.*`
- Agent alias → `analysis_results.fit_settings.agent_alias`

#### 2. AIND Analysis Framework (new format)

Nested structure following `aind-data-schema`:

```json
{
  "_id": "d2a652c73ee8420a...",  // Shorter UUID
  "object_type": "Metadata",
  "name": "7d9b907880012b65...",
  "location": "s3://aind-analysis-prod-o5171v/dynamic-foraging-model-fitting/7d9b...",
  "processing": {
    "data_processes": [
      {
        "name": "han_df_mle_aind-analysis-wrapper",
        "start_date_time": "2026-01-10T04:07:11",
        "output_parameters": {
          "additional_info": "success",
          "subject_id": "781575",
          "session_date": "2025-07-14",
          "nwb_name": "behavior_781575_2025-07-14_21-41-11.nwb",
          "fitting_results": {
            "fit_settings": { "agent_alias": "ForagingCompareThreshold", ... },
            "params": { ... },
            "log_likelihood": -272.10,
            "AIC": 552.20,
            "BIC": 569.34,
            "n_trials": 536,
            "prediction_accuracy": 0.783,
            "cross_validation": { ... }
          }
        }
      }
    ]
  }
}
```

**Key paths:**
- `subject_id` → `processing.data_processes[0].output_parameters.subject_id`
- `session_date` → `processing.data_processes[0].output_parameters.session_date`
- `status` → `processing.data_processes[0].output_parameters.additional_info`
- S3 location → `location`
- Fitting results → `processing.data_processes[0].output_parameters.fitting_results.*`
- Agent alias → `processing.data_processes[0].output_parameters.fitting_results.fit_settings.agent_alias`

#### Field Mapping Summary

| Field | Old Format | New Format |
|-------|-----------|------------|
| subject_id | `subject_id` | `processing.data_processes[0].output_parameters.subject_id` |
| session_date | `session_date` | `processing.data_processes[0].output_parameters.session_date` |
| status | `status` | `processing.data_processes[0].output_parameters.additional_info` |
| S3 location | `s3_location` | `location` |
| agent_alias | `analysis_results.fit_settings.agent_alias` | `processing.data_processes[0].output_parameters.fitting_results.fit_settings.agent_alias` |
| n_trials | `analysis_results.n_trials` | `processing.data_processes[0].output_parameters.fitting_results.n_trials` |
| AIC/BIC | `analysis_results.AIC/BIC` | `processing.data_processes[0].output_parameters.fitting_results.AIC/BIC` |

#### Querying Both Formats

Use MongoDB projection aliasing to normalize fields:

```python
# Query that works for both formats
projection = {
    "_id": 1,
    # Old format fields
    "subject_id": 1,
    "session_date": 1,
    "status": 1,
    "s3_location": 1,
    # New format fields (aliased)
    "subject_id_new": "$processing.data_processes.output_parameters.subject_id",
    "session_date_new": "$processing.data_processes.output_parameters.session_date",
    "location": 1,
}
```

The `aind-analysis-arch-result-access` package handles this automatically by querying both formats and merging results into a unified DataFrame.

## S3 Access

### Public Buckets

Analysis results are in public S3 buckets (no auth needed):

```python
import s3fs

# Anonymous access for public buckets
fs = s3fs.S3FileSystem(anon=True)
```

### Common Bucket Paths

```python
# Old pipeline bucket
S3_PATH_ANALYSIS_OLD = "s3://aind-dynamic-foraging-analysis-prod-o5171v"

# New pipeline bucket (AIND Analysis Framework)
S3_PATH_ANALYSIS_NEW = "s3://aind-analysis-prod-o5171v/dynamic-foraging-model-fitting"

# Bonsai processed data
S3_PATH_BONSAI_ROOT = "s3://aind-behavior-data/foraging_nwb_bonsai_processed"
```

### Asset URL Construction

Convert S3 path to HTTPS for web display:

```python
def s3_to_https(s3_path: str) -> str:
    """Convert s3://bucket/key to https://bucket.s3.amazonaws.com/key"""
    if s3_path.startswith("s3://"):
        s3_path = s3_path[5:]
    bucket = s3_path.split("/")[0]
    key = "/".join(s3_path.split("/")[1:])
    return f"https://{bucket}.s3.amazonaws.com/{key}"
```

### Reading Files from S3

```python
import json
import pickle

# JSON files
with fs.open("s3://bucket/path/file.json") as f:
    data = json.load(f)

# Pickle files
with fs.open("s3://bucket/path/file.pkl", "rb") as f:
    df = pickle.load(f)

# Check existence
if fs.exists("s3://bucket/path/file.png"):
    # File exists
```

### Batch Operations

For multiple S3 reads, use ThreadPoolExecutor:

```python
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

def fetch_file(s3_path):
    # ... fetch logic
    pass

with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(tqdm(
        executor.map(fetch_file, paths),
        total=len(paths),
        desc="Fetching files"
    ))
```

## Using aind-analysis-arch-result-access

This package provides ready-made functions for specific analyses:

```python
# Install: pip install aind-analysis-arch-result-access
from aind_analysis_arch_result_access import get_mle_model_fitting

# Get foraging model fitting results
# IMPORTANT: At least one filter parameter is required!
df = get_mle_model_fitting(
    subject_id="778869",           # Filter by subject (recommended for fast loading)
    # session_date="2024-10-24",   # Or filter by date
    # agent_alias="QLearning...",  # Or filter by model type
    # from_custom_query={...},     # Or use custom MongoDB query
    if_include_metrics=True,
    if_include_latent_variables=False,  # Set False for faster loading
    if_download_figures=False,
)

# For querying by date range:
from datetime import datetime, timedelta
three_months_ago = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
df_recent = get_mle_model_fitting(
    from_custom_query={"session_date": {"$gte": three_months_ago}},
    if_include_metrics=True,
    if_include_latent_variables=False,
)
```

**Important notes:**
- Function requires at least one of: `subject_id`, `session_date`, `agent_alias`, or `from_custom_query`
- The package queries both pipeline formats separately and merges results into a unified DataFrame
- `only_recent_version=True` (default) deduplicates by keeping most recent analysis
- Loading all records can be slow; filter by subject_id or date range for prototyping

Key columns in returned DataFrame:
- `_id`: Record identifier
- `subject_id`, `session_date`: Session info
- `agent_alias`: Model type used
- `n_trials`: Number of trials
- `S3_location`: Path to result files (use for constructing asset URLs)
- `status`: "success" or "failed"
- `pipeline_source`: "aind analysis framework" or "han's analysis pipeline"
- Metrics: `log_likelihood`, `AIC`, `BIC`, `prediction_accuracy`, etc.

## Common Asset Types

Assets stored in S3 per record:
- `fitted_session.png` - Main result figure
- `docDB_record.json` - Full analysis results
- `original_results_*.json` - Raw output files
- Latent variables (q-values, RPE, etc.)

## Best Practices

1. **Filter early**: Use MongoDB queries to reduce data before pandas operations
2. **Batch S3 operations**: Use threading for multiple file reads
3. **Cache results**: Consider caching DataFrames for repeated queries
4. **Handle both formats**: Account for old and new pipeline structures
5. **Check S3 existence**: Assets may not exist for all records
