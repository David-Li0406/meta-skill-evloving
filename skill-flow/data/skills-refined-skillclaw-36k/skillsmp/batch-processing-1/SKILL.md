---
name: batch-processing
description: Patterns for processing multiple samples efficiently. Trigger when analyzing cohorts, processing sample batches, or parallelizing analyses. Provides patterns for sample sheets, parallel processing, and result aggregation while maintaining streaming memory efficiency.
---

# Batch Processing

Patterns for efficiently processing multiple samples while maintaining biometal's streaming architecture.

## Core Principles

1. **Sequential file processing**: Constant memory per sample
2. **Parallel computation**: Where beneficial (CPU-bound)
3. **Structured sample sheets**: Consistent input format
4. **Result aggregation**: Combine without loading all data
5. **Progress tracking**: Monitor long-running batches

## Sample Sheet Handling

### Standard Format

```
sample_id	fastq_path	group	metadata_1	metadata_2
S001	data/S001.fq.gz	control	value1	value2
S002	data/S002.fq.gz	treatment	value3	value4
```

### Loading Sample Sheets

```python
import csv
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class Sample:
    """Sample information from sample sheet."""
    sample_id: str
    fastq_path: str
    group: str
    metadata: Dict[str, str]

    def validate(self) -> List[str]:
        """Validate sample information."""
        errors = []
        if not self.sample_id:
            errors.append("Missing sample_id")
        if not Path(self.fastq_path).exists():
            errors.append(f"File not found: {self.fastq_path}")
        return errors


def load_sample_sheet(path: str) -> List[Sample]:
    """
    Load samples from TSV sample sheet.

    Args:
        path: Path to sample sheet TSV

    Returns:
        List of Sample objects
    """
    samples = []
    required_columns = {"sample_id", "fastq_path"}

    with open(path) as f:
        reader = csv.DictReader(f, delimiter="\t")
        columns = set(reader.fieldnames or [])

        if not required_columns.issubset(columns):
            missing = required_columns - columns
            raise ValueError(f"Missing required columns: {missing}")

        metadata_columns = columns - {"sample_id", "fastq_path", "group"}

        for row in reader:
            sample = Sample(
                sample_id=row["sample_id"],
                fastq_path=row["fastq_path"],
                group=row.get("group", "unknown"),
                metadata={col: row.get(col, "") for col in metadata_columns},
            )
            samples.append(sample)

    return samples


def validate_sample_sheet(samples: List[Sample]) -> Dict:
    """
    Validate all samples in sample sheet.

    Returns:
        Dict with validation results
    """
    results = {
        "valid": True,
        "total_samples": len(samples),
        "errors": [],
    }

    for sample in samples:
        errors = sample.validate()
        if errors:
            results["valid"] = False
            results["errors"].append({
                "sample_id": sample.sample_id,
                "errors": errors,
            })

    return results
```

## Sequential Processing

### Basic Pattern

```python
import biometal
from typing import Callable, Dict, Any

def process_samples_sequential(
    samples: List[Sample],
    process_fn: Callable[[Sample], Dict[str, Any]],
    output_dir: str,
    progress_callback: Callable[[int, int, str], None] = None,
) -> Dict[str, Dict]:
    """
    Process samples sequentially with constant memory.

    Args:
        samples: List of samples to process
        process_fn: Function to process each sample
        output_dir: Directory for outputs
        progress_callback: Optional callback for progress updates

    Returns:
        Dict of {sample_id: results}
    """
    results = {}
    total = len(samples)

    for i, sample in enumerate(samples):
        if progress_callback:
            progress_callback(i + 1, total, sample.sample_id)

        try:
            sample_results = process_fn(sample)
            results[sample.sample_id] = {
                "status": "success",
                "results": sample_results,
            }
        except Exception as e:
            results[sample.sample_id] = {
                "status": "failed",
                "error": str(e),
            }

    return results


# Example usage
def analyze_sample(sample: Sample) -> Dict:
    """Process single sample."""
    stats = {"reads": 0, "bases": 0, "gc_sum": 0.0}

    for record in biometal.FastqStream.from_path(sample.fastq_path):
        stats["reads"] += 1
        stats["bases"] += len(record.sequence)
        stats["gc_sum"] += biometal.gc_content(record.sequence)

    return {
        "total_reads": stats["reads"],
        "total_bases": stats["bases"],
        "mean_gc": stats["gc_sum"] / stats["reads"] if stats["reads"] > 0 else 0,
        "group": sample.group,
    }


# Run batch
samples = load_sample_sheet("samples.tsv")
results = process_samples_sequential(
    samples,
    analyze_sample,
    output_dir="results",
    progress_callback=lambda i, n, s: print(f"[{i}/{n}] Processing {s}..."),
)
```

## Parallel Processing

### Thread Pool Pattern

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable

def process_samples_parallel(
    samples: List[Sample],
    process_fn: Callable[[Sample], Dict[str, Any]],
    max_workers: int = 4,
    progress_callback: Callable[[int, int], None] = None,
) -> Dict[str, Dict]:
    """
    Process samples in parallel using thread pool.

    Note: biometal's streaming is thread-safe for independent files.
    Each worker maintains its own ~5 MB memory footprint.

    Args:
        samples: List of samples to process
        process_fn: Function to process each sample
        max_workers: Maximum parallel workers
        progress_callback: Optional progress callback

    Returns:
        Dict of {sample_id: results}
    """
    results = {}
    completed = 0
    total = len(samples)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        futures = {
            executor.submit(process_fn, sample): sample.sample_id
            for sample in samples
        }

        # Collect results as they complete
        for future in as_completed(futures):
            sample_id = futures[future]
            completed += 1

            if progress_callback:
                progress_callback(completed, total)

            try:
                result = future.result()
                results[sample_id] = {
                    "status": "success",
                    "results": result,
                }
            except Exception as e:
                results[sample_id] = {
                    "status": "failed",
                    "error": str(e),
                }

    return results
```

### Process Pool Pattern (CPU-Bound)

```python
from multiprocessing import Pool

def process_sample_standalone(args: tuple) -> tuple:
    """
    Standalone function for multiprocessing.

    Args must be picklable - can't use Sample object directly.
    """
    sample_id, fastq_path, group = args

    import biometal  # Import inside function for multiprocessing

    stats = {"reads": 0, "bases": 0, "gc_sum": 0.0}

    for record in biometal.FastqStream.from_path(fastq_path):
        stats["reads"] += 1
        stats["bases"] += len(record.sequence)
        stats["gc_sum"] += biometal.gc_content(record.sequence)

    return (sample_id, {
        "total_reads": stats["reads"],
        "mean_gc": stats["gc_sum"] / stats["reads"] if stats["reads"] > 0 else 0,
        "group": group,
    })


def process_samples_multiprocess(
    samples: List[Sample],
    num_processes: int = 4,
) -> Dict[str, Dict]:
    """
    Process samples using multiple processes.

    Better for CPU-bound work. Each process has independent memory.
    """
    # Convert to picklable format
    args_list = [
        (s.sample_id, s.fastq_path, s.group)
        for s in samples
    ]

    results = {}

    with Pool(num_processes) as pool:
        for sample_id, result in pool.map(process_sample_standalone, args_list):
            results[sample_id] = {
                "status": "success",
                "results": result,
            }

    return results
```

## Result Aggregation

### Combining Results

```python
def aggregate_batch_results(
    results: Dict[str, Dict],
    group_by: str = "group",
) -> Dict:
    """
    Aggregate results across samples.

    Args:
        results: Results from batch processing
        group_by: Metadata field to group by

    Returns:
        Aggregated statistics by group
    """
    # Group results
    groups = {}
    for sample_id, result in results.items():
        if result["status"] != "success":
            continue

        group = result["results"].get(group_by, "unknown")
        if group not in groups:
            groups[group] = []
        groups[group].append(result["results"])

    # Calculate per-group statistics
    aggregated = {}
    for group, samples in groups.items():
        n = len(samples)
        aggregated[group] = {
            "n_samples": n,
            "mean_reads": sum(s["total_reads"] for s in samples) / n,
            "mean_gc": sum(s["mean_gc"] for s in samples) / n,
            "total_reads": sum(s["total_reads"] for s in samples),
        }

    return aggregated
```

### Writing Batch Results

```python
def write_batch_results(
    results: Dict[str, Dict],
    output_path: str,
    columns: List[str] = None,
) -> None:
    """
    Write batch results to TSV.

    Args:
        results: Results from batch processing
        output_path: Output TSV path
        columns: Columns to include (default: all)
    """
    if columns is None:
        # Infer columns from first successful result
        for result in results.values():
            if result["status"] == "success":
                columns = ["sample_id", "status"] + list(result["results"].keys())
                break

    with open(output_path, "w") as f:
        f.write("\t".join(columns) + "\n")

        for sample_id, result in sorted(results.items()):
            row = [sample_id, result["status"]]

            if result["status"] == "success":
                for col in columns[2:]:
                    value = result["results"].get(col, "N/A")
                    if isinstance(value, float):
                        row.append(f"{value:.4f}")
                    else:
                        row.append(str(value))
            else:
                row.extend(["N/A"] * (len(columns) - 2))

            f.write("\t".join(row) + "\n")
```

## Progress Tracking

### Progress Reporter

```python
import sys
from datetime import datetime, timedelta

class BatchProgress:
    """Track progress of batch processing."""

    def __init__(self, total: int, description: str = "Processing"):
        self.total = total
        self.description = description
        self.completed = 0
        self.failed = 0
        self.start_time = datetime.now()
        self.last_update = self.start_time

    def update(self, sample_id: str, success: bool = True):
        """Update progress."""
        self.completed += 1
        if not success:
            self.failed += 1

        # Calculate ETA
        elapsed = (datetime.now() - self.start_time).total_seconds()
        rate = self.completed / elapsed if elapsed > 0 else 0
        remaining = (self.total - self.completed) / rate if rate > 0 else 0

        # Print progress
        pct = 100 * self.completed / self.total
        eta = str(timedelta(seconds=int(remaining)))

        sys.stdout.write(
            f"\r{self.description}: {self.completed}/{self.total} ({pct:.1f}%) "
            f"| Failed: {self.failed} | ETA: {eta}   "
        )
        sys.stdout.flush()

    def finish(self):
        """Print final summary."""
        elapsed = datetime.now() - self.start_time
        print(f"\n\nCompleted {self.completed} samples in {elapsed}")
        print(f"Success: {self.completed - self.failed}, Failed: {self.failed}")


# Usage
progress = BatchProgress(len(samples), "QC Analysis")

for sample in samples:
    try:
        result = analyze_sample(sample)
        progress.update(sample.sample_id, success=True)
    except Exception as e:
        progress.update(sample.sample_id, success=False)

progress.finish()
```

## Complete Batch Pipeline

```python
def run_batch_analysis(
    sample_sheet: str,
    output_dir: str,
    num_workers: int = 4,
    parallel: bool = True,
) -> Dict:
    """
    Complete batch analysis pipeline.

    Args:
        sample_sheet: Path to sample sheet TSV
        output_dir: Output directory
        num_workers: Number of parallel workers
        parallel: Use parallel processing

    Returns:
        Dict with results and summary
    """
    from pathlib import Path
    import json

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Load and validate samples
    print("Loading sample sheet...")
    samples = load_sample_sheet(sample_sheet)
    validation = validate_sample_sheet(samples)

    if not validation["valid"]:
        return {"status": "failed", "errors": validation["errors"]}

    print(f"Loaded {len(samples)} samples")

    # Process samples
    if parallel and num_workers > 1:
        print(f"Processing in parallel (workers={num_workers})...")
        results = process_samples_parallel(
            samples,
            analyze_sample,
            max_workers=num_workers,
        )
    else:
        print("Processing sequentially...")
        results = process_samples_sequential(
            samples,
            analyze_sample,
            output_dir=str(output_path),
        )

    # Aggregate results
    print("Aggregating results...")
    aggregated = aggregate_batch_results(results, group_by="group")

    # Write outputs
    write_batch_results(results, str(output_path / "sample_results.tsv"))

    with open(output_path / "aggregated_results.json", "w") as f:
        json.dump(aggregated, f, indent=2)

    # Summary
    n_success = sum(1 for r in results.values() if r["status"] == "success")
    n_failed = len(results) - n_success

    summary = {
        "status": "completed",
        "total_samples": len(samples),
        "successful": n_success,
        "failed": n_failed,
        "aggregated": aggregated,
    }

    with open(output_path / "batch_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\nBatch complete: {n_success} success, {n_failed} failed")
    return summary
```

## Memory Considerations

| Processing Mode | Memory per Sample | Total Memory |
|-----------------|-------------------|--------------|
| Sequential | ~5 MB | ~5 MB (constant) |
| Thread Pool (N workers) | ~5 MB each | ~5×N MB |
| Process Pool (N workers) | ~50 MB each | ~50×N MB |

**Recommendation**: For most cases, sequential or thread pool with 2-4 workers is sufficient. Process pool only for CPU-intensive operations where GIL is a bottleneck.
