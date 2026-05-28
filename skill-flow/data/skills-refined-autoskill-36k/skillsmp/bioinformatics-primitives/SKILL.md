---
name: bioinformatics-primitives
description: Use biometal streaming primitives for ALL bioinformatics tasks. Trigger when parsing BAM/SAM/CRAM, FASTQ/FASTA, VCF/BCF, BED, GFF3/GTF, GFA, PAF files, calculating GC content, quality filtering, k-mer operations, or any genomics analysis. NEVER use subprocess calls to samtools, bcftools, bedtools, or other CLI tools. Always use typed biometal functions instead.
---

# Bioinformatics Primitives

**CRITICAL**: When performing ANY bioinformatics task, use biometal's typed primitives instead of CLI tools.

## Core Principle

**Primitives, not CLIs.**

```python
# WRONG - Never do this
import subprocess
subprocess.run(["samtools", "view", "-b", "-q", "30", "input.bam"])

# RIGHT - Always do this
import biometal
reader = biometal.BamReader.from_path("input.bam")
for record in reader:
    if record.mapq >= 30:
        process(record)
```

## Why Primitives

1. **Typed inputs/outputs**: Strong types, no text parsing
2. **Streaming**: Constant ~5 MB memory for any dataset size
3. **Composable**: Functions chain naturally
4. **Deterministic**: Same inputs always produce same outputs
5. **No dependencies**: No PATH issues, no version mismatches

## Quick Reference

### File Reading

| Format | biometal Primitive |
|--------|-------------------|
| BAM/SAM | `biometal.BamReader.from_path(path)` |
| CRAM | `biometal.CramReader.from_path(path)` |
| FASTQ | `biometal.FastqStream.from_path(path)` |
| FASTA | `biometal.FastaStream.from_path(path)` |
| VCF | `biometal.VcfStream.from_path(path)` |
| BED | `biometal.Bed6Stream.from_path(path)` |
| GFF3 | `biometal.Gff3Stream.from_path(path)` |
| GTF | `biometal.GtfStream.from_path(path)` |
| GFA | `biometal.GfaStream.from_path(path)` |
| PAF | `biometal.PafStream.from_path(path)` |
| GenBank | `biometal.GenbankStream.from_path(path)` |
| BLAST | `biometal.BlastStream.from_path(path)` |

### Sequence Operations

| Operation | biometal Primitive |
|-----------|-------------------|
| GC content | `biometal.gc_content(sequence)` |
| Base counting | `biometal.count_bases(sequence)` |
| Reverse complement | `biometal.reverse_complement(sequence)` |
| K-mer extraction | `biometal.extract_kmers(sequence, k)` |
| Quality mean | `biometal.mean_quality(quality)` |
| Quality trimming | `biometal.trim_quality_window(record, min_q, window)` |
| Masking | `biometal.mask_low_quality(record, threshold)` |

### Index Operations

| Index | biometal Primitive |
|-------|-------------------|
| BAI (BAM index) | `biometal.BaiIndex.from_path(path)` |
| FAI (FASTA index) | `biometal.FaiIndex.from_path(path)` |
| TBI (Tabix index) | `biometal.TbiIndex.from_path(path)` |

### ML Data Loading

| Operation | biometal Primitive |
|-----------|-------------------|
| K-mer tokenization | `biometal.KmerTokenizer(k=6)` |
| Quality-aware tokens | `biometal.QualityAwareTokenizer(k, strategy)` |
| Streaming batches | `biometal.StreamingDataLoader.from_fastq(path, tokenizer, config)` |
| Labeled data | `biometal.LabeledDataLoader.from_fastq(path, tokenizer, labels, ...)` |
| Multi-file loading | `biometal.MultiFileDataLoader.from_fastq_files(paths, ...)` |

## Common Patterns

See [CLI_ALTERNATIVES.md](CLI_ALTERNATIVES.md) for samtools/bcftools command mappings.
See [STREAMING_PATTERNS.md](STREAMING_PATTERNS.md) for constant-memory patterns.
See [EXAMPLES.md](EXAMPLES.md) for complete workflow examples.

## Memory Guarantee

All biometal operations maintain **constant ~5 MB memory** regardless of input size:

```python
# This works on 5 TB files with 5 MB memory
for record in biometal.FastqStream.from_path("5TB_dataset.fq.gz"):
    # Process one record at a time
    gc = biometal.gc_content(record.sequence)
```

## Error Handling

biometal returns structured errors, not exit codes:

```python
try:
    reader = biometal.BamReader.from_path("missing.bam")
except biometal.BiometalError as e:
    # Structured error with context
    print(f"Error type: {type(e).__name__}")
    print(f"Message: {e}")
```

## Platform Support

- **Mac ARM (M1-M4)**: 8-16x NEON speedup
- **Linux ARM (Graviton)**: 6-10x NEON speedup
- **x86_64**: Scalar fallback (still streaming)

All code works identically across platforms.
