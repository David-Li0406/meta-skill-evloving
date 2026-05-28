---
name: lab-qc-thresholds
description: Lab-specific quality control thresholds and pass/fail criteria. Trigger when filtering reads, assessing alignment quality, or making QC decisions. Enforces consistent quality standards across all analyses. CUSTOMIZE THIS SKILL with your lab's validated thresholds.
---

# Lab QC Thresholds

**TEMPLATE SKILL**: Customize thresholds based on your lab's validated standards.

This skill defines consistent quality thresholds for all analyses.

## Read-Level QC

### FASTQ Quality Thresholds

```python
# Customize these for your lab
READ_QC_THRESHOLDS = {
    "min_mean_quality": 20,      # Phred score
    "min_length": 50,            # Base pairs
    "max_length": 500,           # Base pairs (0 = no limit)
    "min_gc": 0.20,              # Fraction
    "max_gc": 0.80,              # Fraction
    "max_n_fraction": 0.10,      # Max fraction of N bases
    "max_homopolymer": 10,       # Max consecutive same base
    "min_complexity": 0.5,       # Dust score threshold
}

def passes_read_qc(record, thresholds: dict = READ_QC_THRESHOLDS) -> tuple:
    """
    Check if read passes all QC criteria.

    Returns:
        (passed: bool, reasons: list of failure reasons)
    """
    import biometal

    reasons = []

    # Quality check
    mean_q = biometal.mean_quality(record.quality)
    if mean_q < thresholds["min_mean_quality"]:
        reasons.append(f"low_quality:{mean_q:.1f}")

    # Length check
    seq_len = len(record.sequence)
    if seq_len < thresholds["min_length"]:
        reasons.append(f"too_short:{seq_len}")
    if thresholds["max_length"] > 0 and seq_len > thresholds["max_length"]:
        reasons.append(f"too_long:{seq_len}")

    # GC content
    gc = biometal.gc_content(record.sequence)
    if gc < thresholds["min_gc"]:
        reasons.append(f"low_gc:{gc:.2f}")
    if gc > thresholds["max_gc"]:
        reasons.append(f"high_gc:{gc:.2f}")

    # N content
    counts = biometal.count_bases(record.sequence)
    n_fraction = counts.get(ord('N'), 0) / seq_len if seq_len > 0 else 0
    if n_fraction > thresholds["max_n_fraction"]:
        reasons.append(f"high_n:{n_fraction:.2f}")

    return (len(reasons) == 0, reasons)
```

### Application

```python
import biometal

def filter_reads_with_qc(input_path: str, output_path: str) -> dict:
    """Filter reads using lab QC thresholds."""
    stats = {"total": 0, "passed": 0, "failed_reasons": {}}

    writer = biometal.FastqWriter.create(output_path)

    for record in biometal.FastqStream.from_path(input_path):
        stats["total"] += 1
        passed, reasons = passes_read_qc(record)

        if passed:
            stats["passed"] += 1
            writer.write_record(record)
        else:
            for reason in reasons:
                key = reason.split(":")[0]
                stats["failed_reasons"][key] = stats["failed_reasons"].get(key, 0) + 1

    writer.finish()

    stats["pass_rate"] = stats["passed"] / stats["total"] if stats["total"] > 0 else 0
    return stats
```

## Alignment QC

### BAM Quality Thresholds

```python
ALIGNMENT_QC_THRESHOLDS = {
    "min_mapq": 30,                  # Mapping quality
    "min_mapping_rate": 0.80,        # Fraction mapped
    "max_duplicate_rate": 0.30,      # Fraction duplicates
    "min_proper_pair_rate": 0.85,    # For paired-end
    "max_mismatch_rate": 0.05,       # Mismatches per aligned base
    "min_coverage": 10,              # Mean coverage (target regions)
    "max_coverage_cv": 0.50,         # Coefficient of variation
}

def passes_alignment_qc(bam_stats: dict, thresholds: dict = ALIGNMENT_QC_THRESHOLDS) -> tuple:
    """
    Check if alignment passes QC criteria.

    Args:
        bam_stats: Dict from bam_alignment_stats()

    Returns:
        (passed: bool, reasons: list of failure reasons)
    """
    reasons = []

    if bam_stats["mapping_rate"] < thresholds["min_mapping_rate"]:
        reasons.append(f"low_mapping_rate:{bam_stats['mapping_rate']:.2f}")

    if bam_stats["duplicate_rate"] > thresholds["max_duplicate_rate"]:
        reasons.append(f"high_duplicates:{bam_stats['duplicate_rate']:.2f}")

    if bam_stats.get("proper_pair_rate", 1.0) < thresholds["min_proper_pair_rate"]:
        reasons.append(f"low_proper_pairs:{bam_stats['proper_pair_rate']:.2f}")

    if bam_stats["mean_mapq"] < thresholds["min_mapq"]:
        reasons.append(f"low_mean_mapq:{bam_stats['mean_mapq']:.1f}")

    return (len(reasons) == 0, reasons)
```

## Variant QC

### VCF Quality Thresholds

```python
VARIANT_QC_THRESHOLDS = {
    "min_qual": 30,                  # QUAL field
    "min_depth": 10,                 # Total read depth
    "min_alt_depth": 3,              # Reads supporting alt allele
    "min_alt_fraction": 0.20,        # Alt allele fraction
    "max_strand_bias": 0.01,         # Fisher strand bias p-value
    "min_mapping_quality": 40,       # RMS mapping quality
    "expected_ts_tv": (1.8, 2.2),    # Expected Ts/Tv range (SNPs)
}

def passes_variant_qc(variant, thresholds: dict = VARIANT_QC_THRESHOLDS) -> tuple:
    """
    Check if variant passes QC criteria.

    Returns:
        (passed: bool, reasons: list of failure reasons)
    """
    reasons = []

    # Quality score
    if variant.quality is not None and variant.quality < thresholds["min_qual"]:
        reasons.append(f"low_qual:{variant.quality:.1f}")

    # Filter field
    if variant.filter and "PASS" not in variant.filter:
        reasons.append(f"filtered:{','.join(variant.filter)}")

    # Additional INFO field checks would go here
    # (depends on what INFO fields are present)

    return (len(reasons) == 0, reasons)
```

## Sample-Level QC

### Pass/Fail Decision

```python
SAMPLE_QC_THRESHOLDS = {
    # Read QC
    "min_total_reads": 1_000_000,
    "min_read_qc_pass_rate": 0.70,

    # Alignment QC
    "min_alignment_pass": True,

    # Coverage QC (for targeted sequencing)
    "min_target_coverage": 20,
    "min_target_breadth": 0.90,  # Fraction of target covered
}

def sample_qc_decision(sample_stats: dict) -> dict:
    """
    Make final QC pass/fail decision for sample.

    Returns:
        Dict with decision and reasons
    """
    passed = True
    reasons = []
    warnings = []

    # Check read count
    if sample_stats.get("total_reads", 0) < SAMPLE_QC_THRESHOLDS["min_total_reads"]:
        passed = False
        reasons.append("insufficient_reads")

    # Check read QC pass rate
    if sample_stats.get("read_qc_pass_rate", 0) < SAMPLE_QC_THRESHOLDS["min_read_qc_pass_rate"]:
        passed = False
        reasons.append("low_read_quality")

    # Check alignment
    if not sample_stats.get("alignment_qc_passed", True):
        passed = False
        reasons.append("alignment_qc_failed")

    # Warnings (don't fail, but flag)
    if sample_stats.get("duplicate_rate", 0) > 0.20:
        warnings.append("elevated_duplicates")

    return {
        "passed": passed,
        "decision": "PASS" if passed else "FAIL",
        "reasons": reasons,
        "warnings": warnings,
    }
```

## QC Report Generation

```python
def generate_qc_report(sample_id: str, all_stats: dict) -> dict:
    """Generate comprehensive QC report for sample."""
    decision = sample_qc_decision(all_stats)

    return {
        "sample_id": sample_id,
        "qc_decision": decision["decision"],
        "qc_reasons": decision["reasons"],
        "qc_warnings": decision["warnings"],
        "thresholds_used": {
            "read": READ_QC_THRESHOLDS,
            "alignment": ALIGNMENT_QC_THRESHOLDS,
            "sample": SAMPLE_QC_THRESHOLDS,
        },
        "metrics": all_stats,
        "timestamp": datetime.now().isoformat(),
    }
```

## Customization Guide

**TO CUSTOMIZE FOR YOUR LAB:**

1. **Read QC**: Adjust based on your sequencing platform
   - Illumina typically: Q20+, 50-300bp
   - Nanopore: Lower Q threshold, longer reads

2. **Alignment QC**: Adjust based on experiment type
   - WGS: 80%+ mapping expected
   - Capture: May have lower mapping rate
   - RNA-seq: Consider multi-mapping

3. **Variant QC**: Adjust based on analysis
   - Germline: Higher stringency
   - Somatic: May need lower thresholds

4. **Document rationale**: Keep notes on why thresholds were chosen

These thresholds should be validated on your lab's data before production use.
