---
name: metagenomics-workflow
description: Domain expertise for metagenomics and microbiome analysis. Trigger when analyzing microbial communities, calculating diversity metrics (alpha/beta diversity), taxonomic profiling, comparing multiple samples, or processing 16S/shotgun metagenome data. Provides patterns for streaming analysis of large metagenome datasets.
---

# Metagenomics Workflow

Domain-specific patterns for microbiome and metagenome analysis using biometal primitives.

## Prerequisites

This skill builds on `bioinformatics-primitives`. Always use streaming patterns.

## Core Concepts

### Sample Organization

Metagenomics typically involves:
- Multiple samples (10s to 1000s)
- Large files per sample (1-100 GB)
- Comparative analysis across samples

**Key principle**: Process samples sequentially to maintain constant memory.

```python
samples = {
    "gut_1": "gut_sample_1.fq.gz",
    "gut_2": "gut_sample_2.fq.gz",
    "oral_1": "oral_sample_1.fq.gz",
}

# Process sequentially - constant memory
for sample_name, path in samples.items():
    stats = analyze_sample(path)
    results[sample_name] = stats
```

## Diversity Metrics

### Alpha Diversity (Within-Sample)

```python
import biometal
from collections import Counter
import math

def calculate_alpha_diversity(kmer_counts: Counter) -> dict:
    """
    Calculate alpha diversity metrics from k-mer spectrum.

    Args:
        kmer_counts: Counter of k-mer frequencies

    Returns:
        Dict with Shannon, Simpson, and richness metrics
    """
    total = sum(kmer_counts.values())
    if total == 0:
        return {"shannon": 0, "simpson": 0, "richness": 0}

    # Richness (number of unique k-mers)
    richness = len(kmer_counts)

    # Shannon entropy: H = -sum(p * log(p))
    shannon = 0.0
    for count in kmer_counts.values():
        if count > 0:
            p = count / total
            shannon -= p * math.log(p)

    # Simpson index: D = sum(p^2)
    simpson = sum((count / total) ** 2 for count in kmer_counts.values())

    # Inverse Simpson (more intuitive - higher = more diverse)
    inv_simpson = 1 / simpson if simpson > 0 else 0

    return {
        "shannon": shannon,
        "simpson": simpson,
        "inverse_simpson": inv_simpson,
        "richness": richness,
        "evenness": shannon / math.log(richness) if richness > 1 else 0,
    }


def sample_kmer_diversity(fastq_path: str, k: int = 21) -> dict:
    """
    Calculate k-mer-based diversity for a metagenome sample.
    Memory: Constant ~5 MB + k-mer counter.
    """
    kmer_counts = Counter()

    for record in biometal.FastqStream.from_path(fastq_path):
        # Only high-quality reads
        if biometal.mean_quality(record.quality) < 20:
            continue

        # Extract k-mers
        for kmer in biometal.extract_kmers(record.sequence, k):
            kmer_counts[kmer] += 1

    return calculate_alpha_diversity(kmer_counts)
```

### Beta Diversity (Between-Sample)

```python
import biometal
from collections import Counter
import math

def jaccard_distance(counts_a: Counter, counts_b: Counter) -> float:
    """
    Jaccard distance between two k-mer profiles.
    J = 1 - |A ∩ B| / |A ∪ B|
    """
    set_a = set(counts_a.keys())
    set_b = set(counts_b.keys())

    intersection = len(set_a & set_b)
    union = len(set_a | set_b)

    return 1 - (intersection / union) if union > 0 else 1.0


def bray_curtis_distance(counts_a: Counter, counts_b: Counter) -> float:
    """
    Bray-Curtis dissimilarity between two abundance profiles.
    BC = sum(|a_i - b_i|) / sum(a_i + b_i)
    """
    all_kmers = set(counts_a.keys()) | set(counts_b.keys())

    numerator = sum(abs(counts_a.get(k, 0) - counts_b.get(k, 0)) for k in all_kmers)
    denominator = sum(counts_a.get(k, 0) + counts_b.get(k, 0) for k in all_kmers)

    return numerator / denominator if denominator > 0 else 0.0


def calculate_beta_diversity_matrix(sample_profiles: dict) -> dict:
    """
    Calculate pairwise beta diversity matrix.

    Args:
        sample_profiles: Dict of {sample_name: Counter of k-mer counts}

    Returns:
        Dict with distance matrices
    """
    samples = list(sample_profiles.keys())
    n = len(samples)

    jaccard_matrix = [[0.0] * n for _ in range(n)]
    bray_curtis_matrix = [[0.0] * n for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            jd = jaccard_distance(sample_profiles[samples[i]], sample_profiles[samples[j]])
            bc = bray_curtis_distance(sample_profiles[samples[i]], sample_profiles[samples[j]])

            jaccard_matrix[i][j] = jaccard_matrix[j][i] = jd
            bray_curtis_matrix[i][j] = bray_curtis_matrix[j][i] = bc

    return {
        "samples": samples,
        "jaccard": jaccard_matrix,
        "bray_curtis": bray_curtis_matrix,
    }
```

## Multi-Sample Analysis

See [MULTI_SAMPLE.md](MULTI_SAMPLE.md) for detailed patterns.

### Basic Pattern

```python
import biometal
from collections import Counter

def analyze_metagenome_cohort(sample_paths: dict, k: int = 21) -> dict:
    """
    Analyze multiple metagenome samples.
    Memory: Constant ~5 MB per sample + accumulated profiles.
    """
    sample_profiles = {}
    sample_stats = {}

    for sample_name, path in sample_paths.items():
        print(f"Processing {sample_name}...")

        kmer_counts = Counter()
        stats = {"reads": 0, "bases": 0, "gc_sum": 0.0, "q20_reads": 0}

        for record in biometal.FastqStream.from_path(path):
            stats["reads"] += 1
            stats["bases"] += len(record.sequence)
            stats["gc_sum"] += biometal.gc_content(record.sequence)

            if biometal.mean_quality(record.quality) >= 20:
                stats["q20_reads"] += 1
                for kmer in biometal.extract_kmers(record.sequence, k):
                    kmer_counts[kmer] += 1

        # Store profile
        sample_profiles[sample_name] = kmer_counts

        # Calculate sample-level stats
        sample_stats[sample_name] = {
            "total_reads": stats["reads"],
            "total_bases": stats["bases"],
            "mean_gc": stats["gc_sum"] / stats["reads"] if stats["reads"] > 0 else 0,
            "q20_rate": stats["q20_reads"] / stats["reads"] if stats["reads"] > 0 else 0,
            "alpha_diversity": calculate_alpha_diversity(kmer_counts),
        }

    # Calculate beta diversity
    beta_diversity = calculate_beta_diversity_matrix(sample_profiles)

    return {
        "sample_stats": sample_stats,
        "beta_diversity": beta_diversity,
    }
```

## Taxonomic Profiling

For k-mer based taxonomic classification:

```python
import biometal
from collections import Counter, defaultdict

def kmer_taxonomic_profile(
    fastq_path: str,
    reference_kmers: dict,  # {kmer: taxon_id}
    k: int = 21,
) -> dict:
    """
    Classify reads by k-mer matching to reference database.

    Args:
        fastq_path: Path to metagenome FASTQ
        reference_kmers: Pre-built k-mer to taxon mapping
        k: K-mer size (must match reference)

    Returns:
        Taxonomic abundance profile
    """
    taxon_counts = Counter()
    unclassified = 0

    for record in biometal.FastqStream.from_path(fastq_path):
        if biometal.mean_quality(record.quality) < 20:
            continue

        # Classify by majority vote of k-mer hits
        read_taxon_hits = Counter()
        kmers = list(biometal.extract_kmers(record.sequence, k))

        for kmer in kmers:
            if kmer in reference_kmers:
                read_taxon_hits[reference_kmers[kmer]] += 1

        if read_taxon_hits:
            # Assign to taxon with most k-mer hits
            best_taxon = read_taxon_hits.most_common(1)[0][0]
            taxon_counts[best_taxon] += 1
        else:
            unclassified += 1

    total = sum(taxon_counts.values()) + unclassified

    return {
        "taxon_counts": dict(taxon_counts),
        "unclassified": unclassified,
        "classification_rate": 1 - (unclassified / total) if total > 0 else 0,
        "total_reads": total,
    }
```

## Quality Control

### Metagenome-Specific QC

```python
import biometal

def metagenome_qc(fastq_path: str) -> dict:
    """
    Metagenome-specific quality control.
    Checks for issues common in metagenome data.
    """
    stats = {
        "total_reads": 0,
        "low_complexity": 0,  # Repetitive sequences
        "adapter_suspect": 0,  # Potential adapter contamination
        "host_suspect": 0,  # Potential host contamination (high GC)
        "quality_passed": 0,
    }

    for record in biometal.FastqStream.from_path(fastq_path):
        stats["total_reads"] += 1

        seq = record.sequence
        gc = biometal.gc_content(seq)
        mean_q = biometal.mean_quality(record.quality)

        # Low complexity check (many repeated bases)
        counts = biometal.count_bases(seq)
        max_base_frac = max(counts.values()) / len(seq) if len(seq) > 0 else 0
        if max_base_frac > 0.5:
            stats["low_complexity"] += 1

        # Potential adapter (very high GC at ends)
        # Adapters often have GC ~60-70%
        if len(seq) >= 20:
            end_gc = biometal.gc_content(seq[-20:])
            if end_gc > 0.65:
                stats["adapter_suspect"] += 1

        # Potential host contamination (human/mouse have ~40% GC)
        if 0.38 <= gc <= 0.42:
            stats["host_suspect"] += 1

        # Overall QC pass
        if mean_q >= 20 and max_base_frac <= 0.5 and len(seq) >= 75:
            stats["quality_passed"] += 1

    n = stats["total_reads"]
    return {
        "total_reads": n,
        "low_complexity_rate": stats["low_complexity"] / n if n > 0 else 0,
        "adapter_suspect_rate": stats["adapter_suspect"] / n if n > 0 else 0,
        "host_suspect_rate": stats["host_suspect"] / n if n > 0 else 0,
        "qc_pass_rate": stats["quality_passed"] / n if n > 0 else 0,
    }
```

## Recommended Workflow

1. **QC** - Run metagenome-specific QC on each sample
2. **Filter** - Remove low-quality and low-complexity reads
3. **Profile** - Generate k-mer profiles for each sample
4. **Alpha diversity** - Calculate within-sample diversity
5. **Beta diversity** - Calculate between-sample distances
6. **Compare** - Statistical comparison between groups

```python
# Complete workflow
samples = load_sample_manifest("samples.tsv")

# Step 1-2: QC and filter
for name, path in samples.items():
    qc = metagenome_qc(path)
    if qc["qc_pass_rate"] < 0.7:
        print(f"WARNING: {name} has low QC pass rate")

# Step 3-5: Profile and diversity
results = analyze_metagenome_cohort(samples, k=21)

# Step 6: Report
for name, stats in results["sample_stats"].items():
    print(f"{name}: Shannon = {stats['alpha_diversity']['shannon']:.2f}")
```

## Memory Considerations

| Operation | Memory |
|-----------|--------|
| Per-sample streaming | ~5 MB |
| K-mer counter (k=21) | 50 MB - 2 GB depending on diversity |
| Distance matrix (n samples) | n² × 8 bytes |

For very large cohorts (>100 samples), consider:
- MinHash sketching for approximate diversity
- Streaming k-mer counting with pruning
- Disk-backed k-mer storage
