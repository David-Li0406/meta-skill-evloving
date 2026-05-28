# CLI Alternatives

This document maps common CLI tool commands to biometal primitives.

**Rule**: NEVER use `subprocess.run()` for these operations. Use biometal.

---

## samtools Alternatives

### samtools view

```bash
# CLI (DON'T USE)
samtools view -b -q 30 -F 4 input.bam > filtered.bam
```

```python
# biometal (USE THIS)
import biometal

reader = biometal.BamReader.from_path("input.bam")
writer = biometal.BamWriter.create("filtered.bam")

for record in reader:
    if record.mapq >= 30 and record.is_mapped:
        writer.write_record(record)

writer.finish()
```

### samtools flagstat

```bash
# CLI (DON'T USE)
samtools flagstat input.bam
```

```python
# biometal (USE THIS)
import biometal

stats = {"total": 0, "mapped": 0, "paired": 0, "proper_pair": 0}

for record in biometal.BamReader.from_path("input.bam"):
    stats["total"] += 1
    if record.is_mapped:
        stats["mapped"] += 1
    if record.is_paired:
        stats["paired"] += 1
    if record.is_proper_pair:
        stats["proper_pair"] += 1

print(f"Total: {stats['total']}")
print(f"Mapped: {stats['mapped']} ({100*stats['mapped']/stats['total']:.1f}%)")
```

### samtools index

```bash
# CLI (DON'T USE)
samtools index input.bam
```

```python
# biometal (USE THIS)
# Note: biometal reads existing indices, index creation not yet supported
# For now, use samtools for index creation, then biometal for queries

index = biometal.BaiIndex.from_path("input.bam.bai")
```

### samtools faidx (region query)

```bash
# CLI (DON'T USE)
samtools faidx reference.fa chr1:1000-2000
```

```python
# biometal (USE THIS)
import biometal

index = biometal.FaiIndex.from_path("reference.fa.fai")
sequence = index.fetch_region("reference.fa", "chr1", 1000, 2000)
```

### samtools depth

```bash
# CLI (DON'T USE)
samtools depth -r chr1:1000-2000 input.bam
```

```python
# biometal (USE THIS)
from collections import defaultdict
import biometal

index = biometal.BaiIndex.from_path("input.bam.bai")
coverage = defaultdict(int)

for record in biometal.BamReader.query_region("input.bam", index, "chr1", 1000, 2000):
    if record.is_mapped and record.position is not None:
        pos = record.position
        for op in record.cigar:
            if op.consumes_reference():
                for i in range(op.length):
                    coverage[pos + i] += 1

for pos in sorted(coverage.keys()):
    print(f"chr1\t{pos}\t{coverage[pos]}")
```

---

## bcftools Alternatives

### bcftools view (filter variants)

```bash
# CLI (DON'T USE)
bcftools view -i 'QUAL>30' variants.vcf.gz > filtered.vcf
```

```python
# biometal (USE THIS)
import biometal

stream = biometal.VcfStream.from_path("variants.vcf.gz")
writer = biometal.VcfWriter.create("filtered.vcf")

for variant in stream:
    if variant.quality and variant.quality > 30:
        writer.write_record(variant)

writer.finish()
```

### bcftools stats

```bash
# CLI (DON'T USE)
bcftools stats variants.vcf.gz
```

```python
# biometal (USE THIS)
import biometal

stats = {"snps": 0, "indels": 0, "multi_allelic": 0, "pass": 0}

for variant in biometal.VcfStream.from_path("variants.vcf.gz"):
    if variant.is_snp():
        stats["snps"] += 1
    elif variant.is_indel():
        stats["indels"] += 1
    if len(variant.alternate) > 1:
        stats["multi_allelic"] += 1
    if "PASS" in variant.filter or not variant.filter:
        stats["pass"] += 1

print(f"SNPs: {stats['snps']}")
print(f"Indels: {stats['indels']}")
print(f"Multi-allelic: {stats['multi_allelic']}")
print(f"PASS: {stats['pass']}")
```

---

## bedtools Alternatives

### bedtools intersect

```bash
# CLI (DON'T USE)
bedtools intersect -a regions.bed -b peaks.bed > overlap.bed
```

```python
# biometal (USE THIS)
import biometal

# Load regions into memory (for small files)
regions_a = list(biometal.Bed6Stream.from_path("regions.bed"))

# Stream through second file
writer = biometal.BedWriter.create("overlap.bed")

for region_b in biometal.Bed6Stream.from_path("peaks.bed"):
    for region_a in regions_a:
        if (region_a.chrom == region_b.chrom and
            region_a.start < region_b.end and
            region_a.end > region_b.start):
            # Overlapping - write intersection
            writer.write_bed6(region_b)
            break

writer.finish()
```

### bedtools coverage

```bash
# CLI (DON'T USE)
bedtools coverage -a regions.bed -b alignments.bam
```

```python
# biometal (USE THIS)
import biometal

bam_index = biometal.BaiIndex.from_path("alignments.bam.bai")

for region in biometal.Bed6Stream.from_path("regions.bed"):
    count = sum(1 for _ in biometal.BamReader.query_region(
        "alignments.bam", bam_index, region.chrom, region.start, region.end
    ))
    print(f"{region.chrom}\t{region.start}\t{region.end}\t{count}")
```

---

## seqtk Alternatives

### seqtk seq (FASTA/FASTQ conversion)

```bash
# CLI (DON'T USE)
seqtk seq -a input.fq > output.fa
```

```python
# biometal (USE THIS)
import biometal

writer = biometal.FastaWriter.create("output.fa")

for record in biometal.FastqStream.from_path("input.fq"):
    fasta_record = biometal.FastaRecord(record.name, record.sequence)
    writer.write_record(fasta_record)

writer.finish()
```

### seqtk subseq (extract sequences)

```bash
# CLI (DON'T USE)
seqtk subseq sequences.fa names.txt > subset.fa
```

```python
# biometal (USE THIS)
import biometal

# Load names to extract
with open("names.txt") as f:
    names_to_extract = set(line.strip() for line in f)

writer = biometal.FastaWriter.create("subset.fa")

for record in biometal.FastaStream.from_path("sequences.fa"):
    if record.name in names_to_extract:
        writer.write_record(record)

writer.finish()
```

---

## General Pattern

For ANY CLI tool, follow this pattern:

1. **Identify the operation** (filter, transform, aggregate)
2. **Use biometal stream** for input
3. **Apply logic in Python** (typed, debuggable)
4. **Use biometal writer** for output (if needed)

```python
# Universal pattern
import biometal

# 1. Stream input
for record in biometal.SomeStream.from_path("input"):
    # 2. Apply logic (filter, transform, etc.)
    if meets_criteria(record):
        # 3. Process or accumulate
        process(record)

# 4. Write output (if needed)
writer.finish()
```

This pattern works for ANY bioinformatics operation with constant memory.
