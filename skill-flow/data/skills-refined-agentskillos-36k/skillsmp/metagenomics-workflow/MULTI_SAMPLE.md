# Multi-Sample Analysis Patterns

Patterns for analyzing multiple metagenome samples efficiently.

## Sample Manifest

Always use a structured sample manifest:

```python
import csv

def load_sample_manifest(manifest_path: str) -> dict:
    """
    Load sample manifest from TSV file.

    Expected columns: sample_id, fastq_path, group, [metadata...]

    Returns:
        Dict of {sample_id: {"path": ..., "group": ..., ...}}
    """
    samples = {}

    with open(manifest_path) as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            sample_id = row["sample_id"]
            samples[sample_id] = {
                "path": row["fastq_path"],
                "group": row.get("group", "unknown"),
                "metadata": {k: v for k, v in row.items()
                            if k not in ("sample_id", "fastq_path", "group")},
            }

    return samples
```

Example manifest (`samples.tsv`):
```
sample_id	fastq_path	group	timepoint	subject
S001	data/S001.fq.gz	control	baseline	P01
S002	data/S002.fq.gz	control	baseline	P02
S003	data/S003.fq.gz	treatment	week4	P01
S004	data/S004.fq.gz	treatment	week4	P02
```

## Sequential Processing

Process samples one at a time for constant memory:

```python
import biometal
from collections import Counter

def process_cohort_sequentially(samples: dict, k: int = 21) -> dict:
    """
    Process entire cohort with constant memory per sample.
    """
    all_results = {}

    for sample_id, sample_info in samples.items():
        print(f"Processing {sample_id}...")

        # Process single sample
        kmer_counts = Counter()
        stats = {"reads": 0, "bases": 0}

        for record in biometal.FastqStream.from_path(sample_info["path"]):
            stats["reads"] += 1
            stats["bases"] += len(record.sequence)

            if biometal.mean_quality(record.quality) >= 20:
                for kmer in biometal.extract_kmers(record.sequence, k):
                    kmer_counts[kmer] += 1

        # Store results (k-mer counts may be large)
        all_results[sample_id] = {
            "stats": stats,
            "kmer_counts": kmer_counts,
            "group": sample_info["group"],
        }

    return all_results
```

## Two-Pass Analysis

For memory-constrained environments, use two passes:

```python
def two_pass_analysis(samples: dict, k: int = 21) -> dict:
    """
    Pass 1: Collect statistics and build global k-mer set
    Pass 2: Count k-mers using fixed vocabulary
    """
    # Pass 1: Collect stats and sample k-mers
    print("Pass 1: Collecting statistics...")
    global_kmers = set()
    sample_stats = {}

    for sample_id, sample_info in samples.items():
        stats = {"reads": 0, "bases": 0}
        sample_kmers = set()

        for record in biometal.FastqStream.from_path(sample_info["path"]):
            stats["reads"] += 1
            stats["bases"] += len(record.sequence)

            if biometal.mean_quality(record.quality) >= 20:
                for kmer in biometal.extract_kmers(record.sequence, k):
                    sample_kmers.add(kmer)

        sample_stats[sample_id] = stats
        global_kmers.update(sample_kmers)

    print(f"Global k-mer vocabulary: {len(global_kmers):,} k-mers")

    # Pass 2: Count with fixed vocabulary
    print("Pass 2: Counting k-mers...")
    kmer_list = list(global_kmers)
    kmer_to_idx = {kmer: i for i, kmer in enumerate(kmer_list)}

    # Count matrix: samples x k-mers
    count_matrix = {}

    for sample_id, sample_info in samples.items():
        counts = [0] * len(kmer_list)

        for record in biometal.FastqStream.from_path(sample_info["path"]):
            if biometal.mean_quality(record.quality) >= 20:
                for kmer in biometal.extract_kmers(record.sequence, k):
                    if kmer in kmer_to_idx:
                        counts[kmer_to_idx[kmer]] += 1

        count_matrix[sample_id] = counts

    return {
        "kmer_vocabulary": kmer_list,
        "count_matrix": count_matrix,
        "sample_stats": sample_stats,
    }
```

## Group Comparisons

Compare samples between groups:

```python
from collections import Counter
import math

def compare_groups(
    sample_results: dict,
    group_a: str,
    group_b: str,
) -> dict:
    """
    Compare k-mer profiles between two groups.
    """
    # Separate samples by group
    profiles_a = [r["kmer_counts"] for r in sample_results.values()
                  if r["group"] == group_a]
    profiles_b = [r["kmer_counts"] for r in sample_results.values()
                  if r["group"] == group_b]

    # Aggregate group profiles
    aggregate_a = Counter()
    for profile in profiles_a:
        aggregate_a.update(profile)

    aggregate_b = Counter()
    for profile in profiles_b:
        aggregate_b.update(profile)

    # Find differential k-mers
    all_kmers = set(aggregate_a.keys()) | set(aggregate_b.keys())

    differential = []
    for kmer in all_kmers:
        count_a = aggregate_a.get(kmer, 0)
        count_b = aggregate_b.get(kmer, 0)

        # Simple fold change
        if count_a > 0 and count_b > 0:
            fold_change = count_a / count_b
            log2_fc = math.log2(fold_change)
        elif count_a > 0:
            log2_fc = float("inf")
        elif count_b > 0:
            log2_fc = float("-inf")
        else:
            continue

        if abs(log2_fc) > 1:  # 2-fold change threshold
            differential.append({
                "kmer": kmer,
                "count_a": count_a,
                "count_b": count_b,
                "log2_fc": log2_fc,
            })

    # Sort by absolute fold change
    differential.sort(key=lambda x: abs(x["log2_fc"]) if x["log2_fc"] != float("inf") else 999,
                     reverse=True)

    return {
        "group_a": group_a,
        "group_b": group_b,
        "samples_a": len(profiles_a),
        "samples_b": len(profiles_b),
        "differential_kmers": differential[:100],  # Top 100
        "unique_to_a": sum(1 for k in aggregate_a if k not in aggregate_b),
        "unique_to_b": sum(1 for k in aggregate_b if k not in aggregate_a),
        "shared": len(set(aggregate_a.keys()) & set(aggregate_b.keys())),
    }
```

## Output Formats

### Abundance Table

```python
def write_abundance_table(
    sample_results: dict,
    output_path: str,
    min_count: int = 10,
) -> None:
    """
    Write k-mer abundance table (samples x k-mers).
    """
    # Collect all k-mers above threshold
    all_kmers = set()
    for result in sample_results.values():
        for kmer, count in result["kmer_counts"].items():
            if count >= min_count:
                all_kmers.add(kmer)

    kmer_list = sorted(all_kmers)
    sample_ids = sorted(sample_results.keys())

    with open(output_path, "w") as f:
        # Header
        f.write("kmer\t" + "\t".join(sample_ids) + "\n")

        # Rows
        for kmer in kmer_list:
            counts = [str(sample_results[s]["kmer_counts"].get(kmer, 0))
                     for s in sample_ids]
            f.write(f"{kmer}\t" + "\t".join(counts) + "\n")
```

### Distance Matrix

```python
def write_distance_matrix(
    beta_diversity: dict,
    output_path: str,
    metric: str = "bray_curtis",
) -> None:
    """
    Write distance matrix for downstream analysis (e.g., PCoA).
    """
    samples = beta_diversity["samples"]
    matrix = beta_diversity[metric]

    with open(output_path, "w") as f:
        # Header
        f.write("\t" + "\t".join(samples) + "\n")

        # Rows
        for i, sample in enumerate(samples):
            row = [f"{matrix[i][j]:.4f}" for j in range(len(samples))]
            f.write(f"{sample}\t" + "\t".join(row) + "\n")
```

## Complete Multi-Sample Pipeline

```python
def metagenome_cohort_analysis(manifest_path: str, output_dir: str) -> None:
    """
    Complete multi-sample metagenomics analysis.
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    # Load samples
    samples = load_sample_manifest(manifest_path)
    print(f"Loaded {len(samples)} samples")

    # Process cohort
    results = process_cohort_sequentially(samples, k=21)

    # Calculate beta diversity
    profiles = {s: r["kmer_counts"] for s, r in results.items()}
    beta = calculate_beta_diversity_matrix(profiles)

    # Group comparison (if groups defined)
    groups = set(r["group"] for r in results.values())
    if len(groups) == 2:
        g1, g2 = sorted(groups)
        comparison = compare_groups(results, g1, g2)
        print(f"Differential k-mers: {len(comparison['differential_kmers'])}")

    # Write outputs
    write_abundance_table(results, f"{output_dir}/abundance.tsv")
    write_distance_matrix(beta, f"{output_dir}/bray_curtis.tsv", "bray_curtis")
    write_distance_matrix(beta, f"{output_dir}/jaccard.tsv", "jaccard")

    # Summary statistics
    with open(f"{output_dir}/summary.tsv", "w") as f:
        f.write("sample_id\tgroup\treads\tbases\tshannon\n")
        for sample_id, result in results.items():
            alpha = calculate_alpha_diversity(result["kmer_counts"])
            f.write(f"{sample_id}\t{result['group']}\t"
                   f"{result['stats']['reads']}\t{result['stats']['bases']}\t"
                   f"{alpha['shannon']:.4f}\n")

    print(f"Results written to {output_dir}/")
```
