# Streaming Patterns

biometal guarantees **constant ~5 MB memory** for any dataset size. This document explains the patterns that make this possible.

---

## Core Principle: Never Accumulate

```python
# BAD - Accumulates in memory (OOM on large files)
all_records = list(biometal.FastqStream.from_path("huge.fq.gz"))

# GOOD - Streams with constant memory
for record in biometal.FastqStream.from_path("huge.fq.gz"):
    process_one(record)  # Memory stays at ~5 MB
```

---

## Pattern 1: Single-Pass Statistics

Calculate statistics without storing records:

```python
import biometal

# Accumulators (constant memory)
total = 0
gc_sum = 0.0
quality_sum = 0.0

for record in biometal.FastqStream.from_path("reads.fq.gz"):
    total += 1
    gc_sum += biometal.gc_content(record.sequence)
    quality_sum += biometal.mean_quality(record.quality)

# Results
mean_gc = gc_sum / total
mean_quality = quality_sum / total
```

**Memory**: ~5 MB regardless of file size.

---

## Pattern 2: Streaming Filter + Write

Filter records and write to new file:

```python
import biometal

reader = biometal.FastqStream.from_path("input.fq.gz")
writer = biometal.FastqWriter.create("filtered.fq.gz")

for record in reader:
    # Quality filter
    if biometal.mean_quality(record.quality) >= 20:
        # Length filter
        if 50 <= len(record.sequence) <= 300:
            writer.write_record(record)

writer.finish()
```

**Memory**: ~5 MB (input stream + output buffer).

---

## Pattern 3: Histogram / Distribution

Build distributions with fixed-size bins:

```python
import biometal
from collections import Counter

# Fixed-size histogram (constant memory)
gc_histogram = Counter()  # GC bins: 0-10%, 10-20%, ..., 90-100%

for record in biometal.FastqStream.from_path("reads.fq.gz"):
    gc = biometal.gc_content(record.sequence)
    bin_index = min(int(gc * 10), 9)  # 0-9
    gc_histogram[bin_index] += 1

# Print distribution
for bin_idx in range(10):
    pct = gc_histogram[bin_idx]
    print(f"{bin_idx*10}-{(bin_idx+1)*10}%: {pct}")
```

**Memory**: ~5 MB + histogram size (10 integers = negligible).

---

## Pattern 4: Top-K / Reservoir Sampling

Keep only the top K items (bounded memory):

```python
import biometal
import heapq

# Keep top 100 longest reads (bounded memory)
top_k = []
K = 100

for record in biometal.FastqStream.from_path("reads.fq.gz"):
    length = len(record.sequence)

    if len(top_k) < K:
        heapq.heappush(top_k, (length, record.name))
    elif length > top_k[0][0]:
        heapq.heapreplace(top_k, (length, record.name))

# Results
for length, name in sorted(top_k, reverse=True):
    print(f"{name}: {length} bp")
```

**Memory**: ~5 MB + K records.

---

## Pattern 5: Multi-File Streaming

Process multiple files with consistent memory:

```python
import biometal

files = ["sample1.fq.gz", "sample2.fq.gz", "sample3.fq.gz"]

# Option 1: Manual iteration
for filepath in files:
    for record in biometal.FastqStream.from_path(filepath):
        process(record)

# Option 2: MultiFileDataLoader (for ML)
tokenizer = biometal.KmerTokenizer(k=6)
config = biometal.DataLoaderConfig().with_batch_size(32)
loader = biometal.MultiFileDataLoader.from_fastq_files(files, tokenizer, config)

for batch in loader:
    train_step(batch)
```

**Memory**: ~5 MB (processes one file at a time).

---

## Pattern 6: Indexed Region Queries

Query specific regions without scanning entire file:

```python
import biometal

# Load index once (< 1 MB)
index = biometal.BaiIndex.from_path("alignments.bam.bai")

# Query multiple regions (streaming within each region)
regions = [
    ("chr1", 1000000, 2000000),
    ("chr2", 5000000, 6000000),
    ("chrX", 100000, 200000),
]

for chrom, start, end in regions:
    region_stats = {"count": 0, "mapq_sum": 0}

    for record in biometal.BamReader.query_region(
        "alignments.bam", index, chrom, start, end
    ):
        region_stats["count"] += 1
        region_stats["mapq_sum"] += record.mapq

    mean_mapq = region_stats["mapq_sum"] / region_stats["count"] if region_stats["count"] > 0 else 0
    print(f"{chrom}:{start}-{end}: {region_stats['count']} reads, mean MAPQ {mean_mapq:.1f}")
```

**Memory**: ~5 MB (index + streaming records).

---

## Pattern 7: Parallel-Safe Streaming

For multi-worker scenarios (PyTorch DataLoader):

```python
import biometal
from torch.utils.data import DataLoader

# biometal handles batching internally
dataset = biometal.GenomicIterableDataset.from_fastq(
    "huge_dataset.fq.gz",
    k=6,
    batch_size=32,
    max_length=512,
)

# Use batch_size=None since biometal already batched
loader = DataLoader(dataset, batch_size=None, num_workers=0)

for batch in loader:
    # batch["input_ids"]: [32, 512]
    # batch["attention_mask"]: [32, 512]
    train_step(batch)
```

**Memory**: ~5 MB per worker.

---

## Anti-Patterns to Avoid

### 1. Loading All Records

```python
# BAD - Will OOM on large files
records = list(stream)
```

### 2. Storing Sequences in Dict

```python
# BAD - Unbounded memory growth
sequences = {}
for record in stream:
    sequences[record.name] = record.sequence  # Grows forever
```

### 3. Nested Full Scans

```python
# BAD - O(n*m) complexity and memory
for record_a in stream_a:
    for record_b in stream_b:  # Re-reads entire file!
        compare(record_a, record_b)
```

### 4. Accumulating Results in List

```python
# BAD - Unbounded growth
results = []
for record in stream:
    results.append(analyze(record))  # Grows forever
```

---

## Memory Budget Guidelines

| Component | Memory |
|-----------|--------|
| FASTQ stream buffer | ~1 MB |
| BAM stream buffer | ~2 MB |
| BGZF decompression | ~1 MB |
| Output writer buffer | ~1 MB |
| **Total baseline** | **~5 MB** |

Additional memory for:
- Indices (BAI/FAI/TBI): 1-10 MB depending on file size
- Histograms/counters: Negligible (fixed bins)
- Top-K structures: K * record_size

---

## Summary

**Always stream. Never accumulate. Memory stays constant.**

```python
# Template for any analysis
import biometal

# Accumulators (bounded)
stats = initialize_accumulators()

# Stream (constant memory)
for record in biometal.SomeStream.from_path("input"):
    update_accumulators(stats, record)

# Report
report(stats)
```
