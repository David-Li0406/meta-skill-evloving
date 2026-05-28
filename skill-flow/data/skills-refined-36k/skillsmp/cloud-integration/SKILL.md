---
name: cloud-integration
description: Patterns for streaming data from cloud sources (S3, GCS, HTTP, SRA). Trigger when accessing remote data, working with public databases, or needing to analyze data without downloading. biometal supports network streaming with constant memory.
---

# Cloud Integration

Patterns for streaming data from cloud and network sources with constant memory.

## Core Capability

biometal supports **network streaming** - analyze remote data without downloading:

```python
import biometal

# Stream directly from HTTP (no download!)
url = "https://example.com/dataset.fq.gz"
for record in biometal.FastqStream.from_path(url):
    # Memory: constant ~5 MB
    gc = biometal.gc_content(record.sequence)
```

## HTTP/HTTPS Streaming

### Public Data Sources

```python
import biometal

# ENA (European Nucleotide Archive)
ena_url = "ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR000/SRR000001/SRR000001.fastq.gz"

# Direct HTTP streaming
for record in biometal.FastqStream.from_path(ena_url):
    process(record)
```

### Streaming with Progress

```python
def stream_with_progress(url: str, report_every: int = 100000) -> dict:
    """
    Stream from URL with progress reporting.

    Args:
        url: Remote URL to stream from
        report_every: Report progress every N records

    Returns:
        Analysis results
    """
    stats = {"records": 0, "bases": 0}

    for record in biometal.FastqStream.from_path(url):
        stats["records"] += 1
        stats["bases"] += len(record.sequence)

        if stats["records"] % report_every == 0:
            print(f"Processed {stats['records']:,} records, {stats['bases']:,} bases")

    return stats
```

## AWS S3 Integration

### Using Pre-Signed URLs

```python
import boto3
from botocore.config import Config

def stream_from_s3(bucket: str, key: str) -> biometal.FastqStream:
    """
    Stream FASTQ from S3 using pre-signed URL.

    Args:
        bucket: S3 bucket name
        key: Object key (path within bucket)

    Returns:
        biometal FastqStream
    """
    # Create S3 client
    s3 = boto3.client("s3", config=Config(signature_version="s3v4"))

    # Generate pre-signed URL (valid for 1 hour)
    url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=3600,
    )

    # Stream using biometal
    return biometal.FastqStream.from_path(url)


# Example usage
stream = stream_from_s3("my-bucket", "data/sample.fq.gz")
for record in stream:
    process(record)
```

### Processing S3 Manifests

```python
import boto3

def process_s3_manifest(
    bucket: str,
    manifest_key: str,
    process_fn,
) -> dict:
    """
    Process multiple files from S3 based on manifest.

    Args:
        bucket: S3 bucket
        manifest_key: Path to manifest file in bucket
        process_fn: Function to process each file

    Returns:
        Results for all files
    """
    s3 = boto3.client("s3")

    # Download manifest
    response = s3.get_object(Bucket=bucket, Key=manifest_key)
    manifest_content = response["Body"].read().decode("utf-8")

    # Parse manifest (assume one file path per line)
    file_keys = [line.strip() for line in manifest_content.split("\n") if line.strip()]

    results = {}

    for key in file_keys:
        print(f"Processing s3://{bucket}/{key}...")

        # Generate pre-signed URL
        url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=3600,
        )

        # Process with biometal streaming
        try:
            result = process_fn(url)
            results[key] = {"status": "success", "result": result}
        except Exception as e:
            results[key] = {"status": "failed", "error": str(e)}

    return results
```

## Google Cloud Storage

### Using Signed URLs

```python
from google.cloud import storage
from datetime import timedelta

def stream_from_gcs(bucket_name: str, blob_name: str) -> biometal.FastqStream:
    """
    Stream FASTQ from Google Cloud Storage.

    Args:
        bucket_name: GCS bucket name
        blob_name: Blob path within bucket

    Returns:
        biometal FastqStream
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Generate signed URL (valid for 1 hour)
    url = blob.generate_signed_url(
        version="v4",
        expiration=timedelta(hours=1),
        method="GET",
    )

    return biometal.FastqStream.from_path(url)
```

## SRA (Sequence Read Archive)

### Direct SRA Access

```python
def stream_from_sra(accession: str) -> dict:
    """
    Stream directly from SRA accession.

    Note: Requires SRA toolkit or ENA mirror.

    Args:
        accession: SRA accession (e.g., SRR000001)

    Returns:
        Analysis results
    """
    # Use ENA mirror for direct HTTP access
    # Format: ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR000/SRR000001/SRR000001.fastq.gz

    # Parse accession to construct URL
    prefix = accession[:6]
    url = f"ftp://ftp.sra.ebi.ac.uk/vol1/fastq/{prefix}/{accession}/{accession}.fastq.gz"

    # Alternative: NCBI direct (may require SRA toolkit)
    # url = f"https://sra-pub-run-odp.s3.amazonaws.com/sra/{accession}/{accession}"

    stats = {"reads": 0, "bases": 0, "gc_sum": 0.0}

    print(f"Streaming from {accession}...")

    for record in biometal.FastqStream.from_path(url):
        stats["reads"] += 1
        stats["bases"] += len(record.sequence)
        stats["gc_sum"] += biometal.gc_content(record.sequence)

    return {
        "accession": accession,
        "total_reads": stats["reads"],
        "total_bases": stats["bases"],
        "mean_gc": stats["gc_sum"] / stats["reads"] if stats["reads"] > 0 else 0,
    }


def batch_stream_sra(accessions: list) -> dict:
    """
    Stream multiple SRA accessions.

    Memory: Constant ~5 MB per accession (sequential processing).
    """
    results = {}

    for accession in accessions:
        try:
            result = stream_from_sra(accession)
            results[accession] = {"status": "success", "result": result}
        except Exception as e:
            results[accession] = {"status": "failed", "error": str(e)}

    return results
```

## Error Handling

### Retry Pattern

```python
import time
from typing import Callable, TypeVar

T = TypeVar("T")

def retry_with_backoff(
    fn: Callable[[], T],
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
) -> T:
    """
    Retry function with exponential backoff.

    Args:
        fn: Function to retry
        max_retries: Maximum retry attempts
        initial_delay: Initial delay between retries (seconds)
        backoff_factor: Multiplier for delay after each retry

    Returns:
        Function result

    Raises:
        Last exception if all retries fail
    """
    delay = initial_delay
    last_exception = None

    for attempt in range(max_retries + 1):
        try:
            return fn()
        except Exception as e:
            last_exception = e
            if attempt < max_retries:
                print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay:.1f}s...")
                time.sleep(delay)
                delay *= backoff_factor

    raise last_exception


# Usage
def fetch_sra_stats(accession):
    return retry_with_backoff(
        lambda: stream_from_sra(accession),
        max_retries=3,
    )
```

### Connection Handling

```python
def stream_with_timeout(url: str, timeout_seconds: int = 300) -> dict:
    """
    Stream with timeout handling.

    Args:
        url: Remote URL
        timeout_seconds: Maximum time for operation

    Returns:
        Results or timeout error
    """
    import signal

    class TimeoutError(Exception):
        pass

    def timeout_handler(signum, frame):
        raise TimeoutError(f"Operation timed out after {timeout_seconds}s")

    # Set timeout (Unix only)
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout_seconds)

    try:
        stats = {"reads": 0}
        for record in biometal.FastqStream.from_path(url):
            stats["reads"] += 1
        return {"status": "success", "stats": stats}
    except TimeoutError as e:
        return {"status": "timeout", "error": str(e)}
    finally:
        signal.alarm(0)  # Cancel alarm
```

## Best Practices

### 1. Use Streaming, Not Downloading

```python
# BAD - Downloads entire file first
import subprocess
subprocess.run(["wget", url, "-O", "temp.fq.gz"])
for record in biometal.FastqStream.from_path("temp.fq.gz"):
    process(record)

# GOOD - Streams directly
for record in biometal.FastqStream.from_path(url):
    process(record)
```

### 2. Handle Network Errors Gracefully

```python
def robust_stream_analysis(url: str) -> dict:
    """Analyze with robust error handling."""
    try:
        stats = {"reads": 0, "bases": 0}
        for record in biometal.FastqStream.from_path(url):
            stats["reads"] += 1
            stats["bases"] += len(record.sequence)
        return {"status": "success", "stats": stats}

    except ConnectionError as e:
        return {"status": "connection_error", "error": str(e)}
    except TimeoutError as e:
        return {"status": "timeout", "error": str(e)}
    except Exception as e:
        return {"status": "error", "error": str(e)}
```

### 3. Log Data Sources

```python
from datetime import datetime

def log_data_source(url: str, log_path: str):
    """Log data source for provenance."""
    with open(log_path, "a") as f:
        f.write(f"{datetime.now().isoformat()}\t{url}\n")
```

## Memory Characteristics

| Source | Memory Usage | Notes |
|--------|--------------|-------|
| Local file | ~5 MB | Standard streaming |
| HTTP/HTTPS | ~5 MB + buffer | 1-2 MB network buffer |
| S3 (pre-signed) | ~5 MB + buffer | Same as HTTP |
| GCS (signed URL) | ~5 MB + buffer | Same as HTTP |
| SRA (ENA mirror) | ~5 MB + buffer | Same as HTTP |

**Key insight**: Network streaming uses same memory as local streaming, plus a small network buffer. You can analyze 5 TB of cloud data with 5 MB of memory.

## Complete Cloud Pipeline

```python
def analyze_cloud_cohort(
    source_type: str,  # "s3", "gcs", "sra"
    locations: list,   # bucket/key pairs or accessions
    output_dir: str,
) -> dict:
    """
    Analyze multiple samples from cloud sources.

    Memory: Constant ~5 MB per sample (sequential processing).
    """
    results = {}

    for i, location in enumerate(locations):
        print(f"[{i+1}/{len(locations)}] Processing {location}...")

        # Construct URL based on source type
        if source_type == "s3":
            bucket, key = location
            url = get_s3_url(bucket, key)
        elif source_type == "gcs":
            bucket, blob = location
            url = get_gcs_url(bucket, blob)
        elif source_type == "sra":
            url = get_sra_url(location)  # accession
        else:
            raise ValueError(f"Unknown source type: {source_type}")

        # Process with retry
        result = retry_with_backoff(
            lambda: analyze_url(url),
            max_retries=3,
        )
        results[str(location)] = result

    # Save results
    import json
    with open(f"{output_dir}/cloud_analysis_results.json", "w") as f:
        json.dump(results, f, indent=2)

    return results
```
