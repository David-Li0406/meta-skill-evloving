---
name: lab-pipeline-templates
description: Standard analysis pipeline templates for the lab. Trigger when setting up new analyses, creating workflows, or asking about standard procedures. Provides pre-approved, validated pipeline structures. CUSTOMIZE THIS SKILL with your lab's standard workflows.
---

# Lab Pipeline Templates

**TEMPLATE SKILL**: Customize with your lab's validated standard workflows.

This skill provides pre-approved pipeline templates for common analyses.

## Pipeline Philosophy

1. **Streaming first**: Use biometal primitives for constant memory
2. **Checkpoint early**: Save intermediate results
3. **Log everything**: Record all parameters and versions
4. **Validate inputs**: Check data before processing
5. **Document outputs**: Generate reports automatically

## Template 1: FASTQ Quality Control Pipeline

```python
"""
Standard FASTQ QC Pipeline
Inputs: Raw FASTQ files
Outputs: Filtered FASTQ + QC reports
"""

import biometal
import json
from pathlib import Path
from datetime import datetime

def run_fastq_qc_pipeline(
    input_path: str,
    output_dir: str,
    sample_id: str,
) -> dict:
    """
    Standard FASTQ QC pipeline.

    Steps:
    1. Validate input
    2. Calculate raw statistics
    3. Filter reads
    4. Calculate filtered statistics
    5. Generate report
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    results = {
        "sample_id": sample_id,
        "input_path": input_path,
        "pipeline": "fastq_qc_v1",
        "started": datetime.now().isoformat(),
    }

    # Step 1: Validate input
    if not Path(input_path).exists():
        raise FileNotFoundError(f"Input not found: {input_path}")

    # Step 2: Raw statistics
    print(f"[{sample_id}] Calculating raw statistics...")
    raw_stats = calculate_fastq_stats(input_path)
    results["raw_stats"] = raw_stats

    # Step 3: Filter reads
    print(f"[{sample_id}] Filtering reads...")
    filtered_path = output_dir / f"{sample_id}.filtered.fq.gz"
    filter_stats = filter_reads_with_qc(input_path, str(filtered_path))
    results["filter_stats"] = filter_stats

    # Step 4: Filtered statistics
    print(f"[{sample_id}] Calculating filtered statistics...")
    filtered_stats = calculate_fastq_stats(str(filtered_path))
    results["filtered_stats"] = filtered_stats

    # Step 5: Generate report
    results["completed"] = datetime.now().isoformat()
    results["qc_decision"] = sample_qc_decision(filter_stats)

    report_path = output_dir / f"{sample_id}_qc_report.json"
    with open(report_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"[{sample_id}] Complete: {results['qc_decision']['decision']}")
    return results


def calculate_fastq_stats(path: str) -> dict:
    """Calculate comprehensive FASTQ statistics."""
    stats = {"reads": 0, "bases": 0, "gc_sum": 0.0, "quality_sum": 0.0}

    for record in biometal.FastqStream.from_path(path):
        stats["reads"] += 1
        stats["bases"] += len(record.sequence)
        stats["gc_sum"] += biometal.gc_content(record.sequence)
        stats["quality_sum"] += biometal.mean_quality(record.quality)

    n = stats["reads"]
    return {
        "total_reads": n,
        "total_bases": stats["bases"],
        "mean_length": stats["bases"] / n if n > 0 else 0,
        "mean_gc": stats["gc_sum"] / n if n > 0 else 0,
        "mean_quality": stats["quality_sum"] / n if n > 0 else 0,
    }
```

## Template 2: Alignment QC Pipeline

```python
"""
Standard Alignment QC Pipeline
Inputs: BAM file
Outputs: QC metrics + coverage report
"""

def run_alignment_qc_pipeline(
    bam_path: str,
    output_dir: str,
    sample_id: str,
    targets_bed: str = None,
) -> dict:
    """
    Standard alignment QC pipeline.

    Steps:
    1. Validate input
    2. Calculate alignment statistics
    3. Calculate coverage (if targets provided)
    4. Assess quality
    5. Generate report
    """
    import biometal
    from pathlib import Path

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    results = {
        "sample_id": sample_id,
        "bam_path": bam_path,
        "pipeline": "alignment_qc_v1",
        "started": datetime.now().isoformat(),
    }

    # Step 1: Validate
    if not Path(bam_path).exists():
        raise FileNotFoundError(f"BAM not found: {bam_path}")

    # Step 2: Alignment statistics
    print(f"[{sample_id}] Calculating alignment statistics...")
    results["alignment_stats"] = calculate_bam_stats(bam_path)

    # Step 3: Coverage (if targets provided)
    if targets_bed:
        print(f"[{sample_id}] Calculating target coverage...")
        results["coverage_stats"] = calculate_target_coverage(bam_path, targets_bed)

    # Step 4: QC assessment
    passed, reasons = passes_alignment_qc(results["alignment_stats"])
    results["qc_passed"] = passed
    results["qc_reasons"] = reasons

    # Step 5: Report
    results["completed"] = datetime.now().isoformat()

    report_path = output_dir / f"{sample_id}_alignment_qc.json"
    with open(report_path, "w") as f:
        json.dump(results, f, indent=2)

    return results


def calculate_bam_stats(bam_path: str) -> dict:
    """Calculate BAM statistics using biometal."""
    stats = {
        "total": 0, "mapped": 0, "paired": 0,
        "proper_pair": 0, "duplicates": 0, "mapq_sum": 0
    }

    for record in biometal.BamReader.from_path(bam_path):
        stats["total"] += 1
        if record.is_mapped:
            stats["mapped"] += 1
            stats["mapq_sum"] += record.mapq
        if record.is_paired:
            stats["paired"] += 1
        if record.is_proper_pair:
            stats["proper_pair"] += 1
        if record.is_duplicate:
            stats["duplicates"] += 1

    n = stats["total"]
    m = stats["mapped"]

    return {
        "total_reads": n,
        "mapped_reads": m,
        "mapping_rate": m / n if n > 0 else 0,
        "duplicate_rate": stats["duplicates"] / n if n > 0 else 0,
        "proper_pair_rate": stats["proper_pair"] / stats["paired"] if stats["paired"] > 0 else 0,
        "mean_mapq": stats["mapq_sum"] / m if m > 0 else 0,
    }
```

## Template 3: Variant Calling Pipeline

```python
"""
Standard Variant Analysis Pipeline
Inputs: VCF file
Outputs: Filtered VCF + variant summary
"""

def run_variant_qc_pipeline(
    vcf_path: str,
    output_dir: str,
    sample_id: str,
) -> dict:
    """
    Standard variant QC pipeline.

    Steps:
    1. Validate input
    2. Calculate variant statistics
    3. Filter variants
    4. Generate summary
    """
    import biometal

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    results = {
        "sample_id": sample_id,
        "vcf_path": vcf_path,
        "pipeline": "variant_qc_v1",
        "started": datetime.now().isoformat(),
    }

    # Step 1: Raw statistics
    print(f"[{sample_id}] Analyzing variants...")
    raw_stats = {"total": 0, "snps": 0, "indels": 0, "passed_qc": 0}

    filtered_path = output_dir / f"{sample_id}.filtered.vcf"
    writer = biometal.VcfWriter.create(str(filtered_path))

    for variant in biometal.VcfStream.from_path(vcf_path):
        raw_stats["total"] += 1

        if variant.is_snp():
            raw_stats["snps"] += 1
        elif variant.is_indel():
            raw_stats["indels"] += 1

        # Apply QC filter
        passed, reasons = passes_variant_qc(variant)
        if passed:
            raw_stats["passed_qc"] += 1
            writer.write_record(variant)

    writer.finish()

    results["variant_stats"] = raw_stats
    results["pass_rate"] = raw_stats["passed_qc"] / raw_stats["total"] if raw_stats["total"] > 0 else 0
    results["completed"] = datetime.now().isoformat()

    # Write report
    report_path = output_dir / f"{sample_id}_variant_qc.json"
    with open(report_path, "w") as f:
        json.dump(results, f, indent=2)

    return results
```

## Template 4: Multi-Sample Comparison

```python
"""
Multi-Sample Comparison Pipeline
Inputs: Sample manifest
Outputs: Comparison statistics + distance matrix
"""

def run_comparison_pipeline(
    manifest_path: str,
    output_dir: str,
    analysis_type: str = "kmer",
) -> dict:
    """
    Standard multi-sample comparison pipeline.

    Steps:
    1. Load manifest
    2. Process each sample
    3. Calculate pairwise distances
    4. Generate comparison report
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load samples
    samples = load_sample_manifest(manifest_path)

    results = {
        "manifest": manifest_path,
        "n_samples": len(samples),
        "analysis_type": analysis_type,
        "started": datetime.now().isoformat(),
    }

    # Process samples
    sample_profiles = {}
    sample_stats = {}

    for sample_id, info in samples.items():
        print(f"Processing {sample_id}...")
        profile, stats = process_sample_for_comparison(info["path"])
        sample_profiles[sample_id] = profile
        sample_stats[sample_id] = stats

    # Calculate distances
    print("Calculating distances...")
    beta_diversity = calculate_beta_diversity_matrix(sample_profiles)

    # Save outputs
    results["sample_stats"] = sample_stats
    results["beta_diversity"] = beta_diversity
    results["completed"] = datetime.now().isoformat()

    # Write distance matrix
    write_distance_matrix(
        beta_diversity,
        str(output_dir / "distance_matrix.tsv"),
        "bray_curtis"
    )

    # Write report
    with open(output_dir / "comparison_report.json", "w") as f:
        json.dump(results, f, indent=2, default=str)

    return results
```

## Pipeline Execution

### Running a Pipeline

```python
# Single sample
results = run_fastq_qc_pipeline(
    input_path="data/sample.fq.gz",
    output_dir="results/qc",
    sample_id="PROJ_S001_L001_20260126",
)

# Multiple samples from manifest
import csv

with open("samples.tsv") as f:
    reader = csv.DictReader(f, delimiter="\t")
    for row in reader:
        run_fastq_qc_pipeline(
            input_path=row["fastq_path"],
            output_dir="results/qc",
            sample_id=row["sample_id"],
        )
```

### Pipeline Logging

```python
import logging

def setup_pipeline_logging(output_dir: str, pipeline_name: str) -> logging.Logger:
    """Setup logging for pipeline."""
    log_path = Path(output_dir) / f"{pipeline_name}.log"

    logger = logging.getLogger(pipeline_name)
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler(log_path)
    handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    ))
    logger.addHandler(handler)

    return logger
```

## Customization Guide

1. **Add new templates**: Create functions following the same structure
2. **Modify thresholds**: Import from `lab-qc-thresholds` skill
3. **Adjust outputs**: Modify report format as needed
4. **Add steps**: Insert additional processing as required

All templates use biometal primitives for streaming, constant-memory processing.
