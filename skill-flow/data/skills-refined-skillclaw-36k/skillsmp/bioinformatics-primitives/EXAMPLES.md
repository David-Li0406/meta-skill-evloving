# Complete Workflow Examples

Real-world examples showing biometal primitives in action.

---

## Example 1: FASTQ Quality Control Pipeline

```python
import biometal
from collections import Counter

def fastq_qc_report(fastq_path: str) -> dict:
    """
    Generate comprehensive QC report for FASTQ file.
    Memory: Constant ~5 MB regardless of file size.
    """
    stats = {
        "total_reads": 0,
        "total_bases": 0,
        "gc_sum": 0.0,
        "quality_sum": 0.0,
        "length_histogram": Counter(),
        "quality_histogram": Counter(),
        "passed_qc": 0,
    }

    for record in biometal.FastqStream.from_path(fastq_path):
        stats["total_reads"] += 1
        stats["total_bases"] += len(record.sequence)

        # GC content
        gc = biometal.gc_content(record.sequence)
        stats["gc_sum"] += gc

        # Quality
        mean_q = biometal.mean_quality(record.quality)
        stats["quality_sum"] += mean_q

        # Histograms (binned for constant memory)
        length_bin = min(len(record.sequence) // 50, 10)  # 0-500+ bp
        stats["length_histogram"][length_bin] += 1

        quality_bin = min(int(mean_q), 40)  # 0-40
        stats["quality_histogram"][quality_bin] += 1

        # QC pass criteria
        if mean_q >= 20 and len(record.sequence) >= 50:
            stats["passed_qc"] += 1

    # Calculate means
    n = stats["total_reads"]
    return {
        "total_reads": n,
        "total_bases": stats["total_bases"],
        "mean_length": stats["total_bases"] / n if n > 0 else 0,
        "mean_gc": stats["gc_sum"] / n if n > 0 else 0,
        "mean_quality": stats["quality_sum"] / n if n > 0 else 0,
        "qc_pass_rate": stats["passed_qc"] / n if n > 0 else 0,
        "length_histogram": dict(stats["length_histogram"]),
        "quality_histogram": dict(stats["quality_histogram"]),
    }

# Usage
report = fastq_qc_report("sample.fq.gz")
print(f"Total reads: {report['total_reads']:,}")
print(f"Mean GC: {report['mean_gc']:.1%}")
print(f"Mean quality: {report['mean_quality']:.1f}")
print(f"QC pass rate: {report['qc_pass_rate']:.1%}")
```

---

## Example 2: BAM Alignment Statistics

```python
import biometal
from collections import defaultdict

def bam_alignment_stats(bam_path: str) -> dict:
    """
    Calculate comprehensive alignment statistics.
    Memory: Constant ~5 MB.
    """
    stats = {
        "total": 0,
        "mapped": 0,
        "unmapped": 0,
        "paired": 0,
        "proper_pair": 0,
        "duplicates": 0,
        "secondary": 0,
        "mapq_sum": 0,
        "mapq_histogram": defaultdict(int),
        "edit_distance_sum": 0,
        "edit_distance_count": 0,
    }

    for record in biometal.BamReader.from_path(bam_path):
        stats["total"] += 1

        if record.is_mapped:
            stats["mapped"] += 1
            stats["mapq_sum"] += record.mapq
            stats["mapq_histogram"][record.mapq] += 1

            # Edit distance from NM tag
            ed = record.edit_distance()
            if ed is not None:
                stats["edit_distance_sum"] += ed
                stats["edit_distance_count"] += 1
        else:
            stats["unmapped"] += 1

        if record.is_paired:
            stats["paired"] += 1
        if record.is_proper_pair:
            stats["proper_pair"] += 1
        if record.is_duplicate:
            stats["duplicates"] += 1
        if record.is_secondary:
            stats["secondary"] += 1

    # Calculate derived statistics
    n = stats["total"]
    m = stats["mapped"]

    return {
        "total_reads": n,
        "mapped_reads": m,
        "mapping_rate": m / n if n > 0 else 0,
        "unmapped_reads": stats["unmapped"],
        "paired_reads": stats["paired"],
        "proper_pair_reads": stats["proper_pair"],
        "proper_pair_rate": stats["proper_pair"] / stats["paired"] if stats["paired"] > 0 else 0,
        "duplicate_reads": stats["duplicates"],
        "duplicate_rate": stats["duplicates"] / n if n > 0 else 0,
        "secondary_alignments": stats["secondary"],
        "mean_mapq": stats["mapq_sum"] / m if m > 0 else 0,
        "mean_edit_distance": stats["edit_distance_sum"] / stats["edit_distance_count"] if stats["edit_distance_count"] > 0 else 0,
    }

# Usage
stats = bam_alignment_stats("alignments.bam")
print(f"Mapping rate: {stats['mapping_rate']:.1%}")
print(f"Mean MAPQ: {stats['mean_mapq']:.1f}")
print(f"Duplicate rate: {stats['duplicate_rate']:.1%}")
```

---

## Example 3: VCF Variant Summary

```python
import biometal
from collections import Counter

def vcf_variant_summary(vcf_path: str) -> dict:
    """
    Summarize variants in VCF file.
    Memory: Constant ~5 MB.
    """
    stats = {
        "total": 0,
        "snps": 0,
        "indels": 0,
        "insertions": 0,
        "deletions": 0,
        "multi_allelic": 0,
        "pass_filter": 0,
        "quality_sum": 0.0,
        "quality_count": 0,
        "chromosome_counts": Counter(),
        "ts_count": 0,  # Transitions
        "tv_count": 0,  # Transversions
    }

    transitions = {("A", "G"), ("G", "A"), ("C", "T"), ("T", "C")}

    stream = biometal.VcfStream.from_path(vcf_path)

    for variant in stream:
        stats["total"] += 1
        stats["chromosome_counts"][variant.chrom] += 1

        # Variant type
        if variant.is_snp():
            stats["snps"] += 1
            # Ts/Tv ratio
            ref, alt = variant.reference, variant.alternate[0]
            if (ref, alt) in transitions:
                stats["ts_count"] += 1
            else:
                stats["tv_count"] += 1

        elif variant.is_indel():
            stats["indels"] += 1
            if len(variant.alternate[0]) > len(variant.reference):
                stats["insertions"] += 1
            else:
                stats["deletions"] += 1

        # Multi-allelic
        if len(variant.alternate) > 1:
            stats["multi_allelic"] += 1

        # Filter
        if not variant.filter or "PASS" in variant.filter:
            stats["pass_filter"] += 1

        # Quality
        if variant.quality is not None:
            stats["quality_sum"] += variant.quality
            stats["quality_count"] += 1

    return {
        "total_variants": stats["total"],
        "snps": stats["snps"],
        "indels": stats["indels"],
        "insertions": stats["insertions"],
        "deletions": stats["deletions"],
        "multi_allelic": stats["multi_allelic"],
        "pass_rate": stats["pass_filter"] / stats["total"] if stats["total"] > 0 else 0,
        "mean_quality": stats["quality_sum"] / stats["quality_count"] if stats["quality_count"] > 0 else 0,
        "ts_tv_ratio": stats["ts_count"] / stats["tv_count"] if stats["tv_count"] > 0 else 0,
        "variants_per_chromosome": dict(stats["chromosome_counts"]),
    }

# Usage
summary = vcf_variant_summary("variants.vcf.gz")
print(f"Total variants: {summary['total_variants']:,}")
print(f"SNPs: {summary['snps']:,}")
print(f"Indels: {summary['indels']:,}")
print(f"Ts/Tv ratio: {summary['ts_tv_ratio']:.2f}")
```

---

## Example 4: ML Data Preparation

```python
import biometal

def prepare_ml_dataset(
    fastq_paths: list,
    labels_path: str,
    output_batches: int = 1000,
) -> dict:
    """
    Prepare genomic data for ML training.
    Memory: Constant ~5 MB regardless of dataset size.
    """
    # Quality-aware tokenizer (novel biometal feature)
    tokenizer = biometal.QualityAwareTokenizer(
        k=6,
        strategy="mask",  # Mask low-quality k-mers
        threshold=20,
    )

    # Load labels
    labels = biometal.LabelMap.from_tsv(labels_path)

    # Configure data loader
    config = biometal.DataLoaderConfig() \
        .with_batch_size(32) \
        .with_max_length(512) \
        .with_shuffle_buffer(10000) \
        .with_reverse_complement(True)  # Data augmentation

    # Create labeled loader
    loader = biometal.LabeledDataLoader.from_fastq(
        fastq_paths[0],
        tokenizer,
        labels,
        batch_size=32,
        max_length=512,
    )

    # Process batches
    stats = {"batches": 0, "sequences": 0, "masked_tokens": 0}

    for batch in loader:
        stats["batches"] += 1
        stats["sequences"] += len(batch.input_ids)

        # Count masked tokens
        for seq in batch.input_ids:
            stats["masked_tokens"] += sum(1 for t in seq if t == tokenizer.mask_token_id())

        if stats["batches"] >= output_batches:
            break

    return {
        "batches_processed": stats["batches"],
        "sequences_processed": stats["sequences"],
        "masked_token_rate": stats["masked_tokens"] / (stats["sequences"] * 512),
        "num_classes": loader.num_classes(),
        "class_names": loader.class_names(),
    }

# Usage
stats = prepare_ml_dataset(
    fastq_paths=["sample1.fq.gz", "sample2.fq.gz"],
    labels_path="labels.tsv",
)
print(f"Processed {stats['sequences_processed']:,} sequences")
print(f"Classes: {stats['class_names']}")
print(f"Masked token rate: {stats['masked_token_rate']:.1%}")
```

---

## Example 5: Region-Based Coverage Analysis

```python
import biometal
from collections import defaultdict

def calculate_region_coverage(
    bam_path: str,
    bed_path: str,
) -> list:
    """
    Calculate coverage for each region in BED file.
    Uses indexed queries for efficiency.
    Memory: Constant ~5 MB + index.
    """
    # Load BAM index
    bam_index = biometal.BaiIndex.from_path(f"{bam_path}.bai")

    results = []

    for region in biometal.Bed6Stream.from_path(bed_path):
        # Per-position coverage
        coverage = defaultdict(int)

        # Query only reads overlapping this region
        for record in biometal.BamReader.query_region(
            bam_path, bam_index, region.chrom, region.start, region.end
        ):
            if not record.is_mapped or record.position is None:
                continue

            # Walk through CIGAR to calculate coverage
            pos = record.position
            for op in record.cigar:
                if op.consumes_reference():
                    for i in range(op.length):
                        if region.start <= pos + i < region.end:
                            coverage[pos + i] += 1
                    pos += op.length
                elif op.is_insertion():
                    pass  # Insertions don't advance reference position

        # Calculate statistics
        region_length = region.end - region.start
        if coverage:
            depths = list(coverage.values())
            mean_depth = sum(depths) / len(depths)
            covered_bases = len(depths)
        else:
            mean_depth = 0
            covered_bases = 0

        results.append({
            "chrom": region.chrom,
            "start": region.start,
            "end": region.end,
            "name": region.name,
            "length": region_length,
            "mean_coverage": mean_depth,
            "covered_bases": covered_bases,
            "breadth": covered_bases / region_length if region_length > 0 else 0,
        })

    return results

# Usage
coverage = calculate_region_coverage("alignments.bam", "targets.bed")
for region in coverage[:10]:
    print(f"{region['name']}: {region['mean_coverage']:.1f}x coverage, {region['breadth']:.1%} breadth")
```

---

## Example 6: Multi-Sample Comparison

```python
import biometal

def compare_samples(sample_paths: dict) -> dict:
    """
    Compare statistics across multiple samples.
    Memory: Constant ~5 MB per sample (processed sequentially).
    """
    results = {}

    for sample_name, fastq_path in sample_paths.items():
        stats = {"reads": 0, "bases": 0, "gc_sum": 0.0, "q20_reads": 0}

        for record in biometal.FastqStream.from_path(fastq_path):
            stats["reads"] += 1
            stats["bases"] += len(record.sequence)
            stats["gc_sum"] += biometal.gc_content(record.sequence)

            if biometal.mean_quality(record.quality) >= 20:
                stats["q20_reads"] += 1

        results[sample_name] = {
            "total_reads": stats["reads"],
            "total_bases": stats["bases"],
            "mean_gc": stats["gc_sum"] / stats["reads"] if stats["reads"] > 0 else 0,
            "q20_rate": stats["q20_reads"] / stats["reads"] if stats["reads"] > 0 else 0,
        }

    return results

# Usage
samples = {
    "control": "control.fq.gz",
    "treatment_1": "treatment1.fq.gz",
    "treatment_2": "treatment2.fq.gz",
}

comparison = compare_samples(samples)

print("Sample Comparison:")
print("-" * 60)
for name, stats in comparison.items():
    print(f"{name}:")
    print(f"  Reads: {stats['total_reads']:,}")
    print(f"  Mean GC: {stats['mean_gc']:.1%}")
    print(f"  Q20 rate: {stats['q20_rate']:.1%}")
```

---

## Key Takeaways

1. **Always stream** - Use `for record in stream` pattern
2. **Accumulate statistics** - Don't store records
3. **Use indices** - For region queries, load index once
4. **Bin histograms** - Fixed bins for constant memory
5. **Write immediately** - Don't buffer output records

All examples maintain **constant ~5 MB memory** regardless of input size.
