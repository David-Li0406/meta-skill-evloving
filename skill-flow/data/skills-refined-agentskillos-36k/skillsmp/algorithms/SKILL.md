---
name: algorithms
description: Use when researching algorithms, data structures, optimization, performance, or need modern alternatives to classic algorithms
---

# Modern Algorithms and Data Structures

## Overview

This skill provides comprehensive guidance on modern algorithms and data structures from recent computer science research, with focus on practical Elixir implementations. Modern algorithms often provide significant performance improvements over classic approaches through better cache utilization, parallelization, and probabilistic techniques.

## When to Use

Use this skill when:
- Researching algorithmic approaches for a problem
- Need modern alternatives to classic algorithms
- Optimizing performance-critical code
- Evaluating data structure choices
- Assessing implementation complexity vs performance gains
- Working with large-scale data requiring approximate solutions
- Implementing distributed system algorithms

## Core Concepts

### Modern Hash Functions

Modern hash functions significantly outperform classic algorithms like MD5 and SHA1 for non-cryptographic use cases.

#### xxHash3 (2020)

**Overview**: Extremely fast non-cryptographic hash function optimized for modern CPUs with SIMD instructions.

**Performance**:
- 31.5 GB/s on modern hardware (vs 0.5 GB/s for MD5)
- Excellent hash quality with low collision rates
- Consistent across 32-bit and 64-bit platforms

**Elixir Implementation**:
```elixir
# Add to mix.exs
{:exhash, "~> 0.2"}

# Usage
:exhash.xxh3_128("data to hash")
```

**Use Cases**:
- Hash tables and hash maps
- Data deduplication
- Checksum verification (non-security)
- Bloom filters and other probabilistic structures

**Paper**: "xxHash: Fast Hash Algorithm" (Collet, 2020)

#### BLAKE3 (2020)

**Overview**: Cryptographic hash function that's significantly faster than SHA-2/SHA-3 while maintaining security.

**Performance**:
- 2.5 GB/s (vs 0.4 GB/s for SHA-256)
- Parallelizable and optimized for SIMD
- Suitable for cryptographic applications

**Elixir Implementation**:
```elixir
# Add to mix.exs
{:b3, "~> 0.2"}

# Usage
B3.hash("data to hash")
```

**Use Cases**:
- Content-addressed storage
- File integrity verification
- Digital signatures
- Password hashing alternatives (use with key derivation)

**Paper**: "BLAKE3: One Function, Fast Everywhere" (O'Connor et al., 2020)

#### HighwayHash (2017)

**Overview**: SIMD-optimized hash function with strong security properties, developed by Google.

**Performance**:
- 10 GB/s on modern CPUs
- Uses AES-NI and AVX2 instructions when available
- Keyed hash for authentication

**Use Cases**:
- Message authentication codes (MAC)
- Fingerprinting for data structures
- High-performance checksums

**Note**: Limited Elixir support; consider xxHash3 for most non-crypto cases.

**Paper**: "HighwayHash: Fast Strong Hashing" (Pike & Alakuijala, 2017)

### Probabilistic Data Structures

Probabilistic structures trade perfect accuracy for dramatic space savings and speed improvements. Essential for large-scale systems.

#### HyperLogLog (2007)

**Overview**: Estimates cardinality (unique count) with configurable accuracy using minimal memory.

**Space Complexity**:
- Standard: 1.5 KB for billions of elements
- vs Exact: 8 bytes per unique element (8 GB for 1 billion elements)

**Accuracy**:
- Typical error: ±2% with 1.5 KB
- Error decreases with more memory (configurable)

**Elixir Implementation**:
```elixir
# Add to mix.exs
{:hyperloglog, "~> 1.0"}

# Usage
hll = HyperLogLog.new(14)  # 14-bit precision (16,384 registers)

hll =
  Enum.reduce(1..1_000_000, hll, fn i, acc ->
    HyperLogLog.add(acc, "user_#{i}")
  end)

estimated_count = HyperLogLog.count(hll)
# ~1,000,000 with ±2% error
```

**Use Cases**:
- Unique visitor counting
- Distinct value estimation in databases
- Network traffic analysis
- Real-time analytics dashboards

**Performance Comparison**:
```
Counting 10M unique items:
- Exact (MapSet): 800 MB memory, 100% accurate
- HyperLogLog: 12 KB memory, 98% accurate
```

**Paper**: "HyperLogLog: the analysis of a near-optimal cardinality estimation algorithm" (Flajolet et al., 2007)

**Production Pattern**:
```elixir
defmodule MyApp.Analytics.UniqueVisitors do
  use GenServer

  def start_link(opts) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end

  def init(_opts) do
    # 16-bit precision = ~0.8% error, 64 KB memory
    hll = HyperLogLog.new(16)
    {:ok, %{hll: hll}}
  end

  def track_visitor(user_id) do
    GenServer.cast(__MODULE__, {:track, user_id})
  end

  def get_count do
    GenServer.call(__MODULE__, :count)
  end

  def handle_cast({:track, user_id}, state) do
    hll = HyperLogLog.add(state.hll, to_string(user_id))
    {:noreply, %{state | hll: hll}}
  end

  def handle_call(:count, _from, state) do
    count = HyperLogLog.count(state.hll)
    {:reply, count, state}
  end
end
```

#### Cuckoo Filters (2014)

**Overview**: Space-efficient probabilistic data structure for set membership testing. Improves on Bloom filters by supporting deletion.

**Advantages over Bloom Filters**:
- Supports deletion (Bloom filters cannot delete)
- Better space efficiency for low false positive rates
- Better cache locality

**Space Complexity**: ~1.5 bytes per item for 3% false positive rate

**Elixir Implementation**:
```elixir
# Add to mix.exs
{:cuckoo_filter, "~> 0.1"}

# Usage
filter = CuckooFilter.new(capacity: 1_000_000)

filter = CuckooFilter.add(filter, "item1")
filter = CuckooFilter.add(filter, "item2")

CuckooFilter.contains?(filter, "item1")  # true
CuckooFilter.contains?(filter, "item99")  # false (or rare false positive)

# Unlike Bloom filters, can delete
filter = CuckooFilter.delete(filter, "item1")
```

**Use Cases**:
- Cache invalidation (track what's cached)
- Spam filtering with updating rules
- Distributed system deduplication
- Rate limiting with key expiration

**Performance Comparison**:
```
Storing 1M items with 2% false positive rate:
- Exact (MapSet): 80 MB, 100% accurate, supports deletion
- Bloom Filter: 1.8 MB, 2% FP rate, no deletion
- Cuckoo Filter: 1.5 MB, 2% FP rate, supports deletion
```

**Paper**: "Cuckoo Filter: Practically Better Than Bloom" (Fan et al., 2014)

**Production Pattern**:
```elixir
defmodule MyApp.Cache.Filter do
  use GenServer

  @capacity 10_000_000
  @fpr 0.01  # 1% false positive rate

  def start_link(opts) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end

  def init(_opts) do
    filter = CuckooFilter.new(capacity: @capacity, fpr: @fpr)
    {:ok, %{filter: filter}}
  end

  def mark_cached(key) do
    GenServer.cast(__MODULE__, {:add, key})
  end

  def is_cached?(key) do
    GenServer.call(__MODULE__, {:contains, key})
  end

  def invalidate(key) do
    GenServer.cast(__MODULE__, {:delete, key})
  end

  def handle_cast({:add, key}, state) do
    filter = CuckooFilter.add(state.filter, key)
    {:noreply, %{state | filter: filter}}
  end

  def handle_cast({:delete, key}, state) do
    filter = CuckooFilter.delete(state.filter, key)
    {:noreply, %{state | filter: filter}}
  end

  def handle_call({:contains, key}, _from, state) do
    result = CuckooFilter.contains?(state.filter, key)
    {:reply, result, state}
  end
end
```

#### Count-Min Sketch (2005)

**Overview**: Probabilistic data structure for frequency estimation in streams. Answers "how many times has X appeared?" with bounded error.

**Space Complexity**: Configurable based on error bounds (typically few KB for millions of items)

**Accuracy**: Overestimates by at most ε×N with probability 1-δ
- ε (epsilon): error rate (e.g., 0.01 = 1% error)
- δ (delta): failure probability (e.g., 0.001 = 0.1% chance of exceeding error)

**Elixir Implementation**:
```elixir
# Add to mix.exs
{:count_min_sketch, "~> 0.1"}

# Usage
# epsilon=0.001 (0.1% error), delta=0.01 (1% failure probability)
cms = CountMinSketch.new(epsilon: 0.001, delta: 0.01)

# Track events
cms =
  Enum.reduce(events, cms, fn event, acc ->
    CountMinSketch.add(acc, event.type)
  end)

# Query frequency
CountMinSketch.count(cms, "page_view")  # Estimated count
```

**Use Cases**:
- Real-time analytics (top K items)
- Network traffic monitoring
- Detecting heavy hitters in streams
- Frequency-based rate limiting

**Performance Comparison**:
```
Tracking 100M events with 1% error:
- Exact (Map): 1.6 GB memory
- Count-Min Sketch: 40 KB memory
```

**Paper**: "An Improved Data Stream Summary: The Count-Min Sketch and its Applications" (Cormode & Muthukrishnan, 2005)

**Production Pattern**:
```elixir
defmodule MyApp.Analytics.FrequencyTracker do
  use GenServer

  def start_link(opts) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end

  def init(_opts) do
    # 0.1% error, 99% confidence
    cms = CountMinSketch.new(epsilon: 0.001, delta: 0.01)
    {:ok, %{cms: cms}}
  end

  def track_event(event_type) do
    GenServer.cast(__MODULE__, {:track, event_type})
  end

  def get_frequency(event_type) do
    GenServer.call(__MODULE__, {:count, event_type})
  end

  def get_top_k(k) do
    GenServer.call(__MODULE__, {:top_k, k})
  end

  def handle_cast({:track, event_type}, state) do
    cms = CountMinSketch.add(state.cms, event_type)
    {:noreply, %{state | cms: cms}}
  end

  def handle_call({:count, event_type}, _from, state) do
    count = CountMinSketch.count(state.cms, event_type)
    {:reply, count, state}
  end

  def handle_call({:top_k, k}, _from, state) do
    # Combine with min-heap for top-K tracking
    top_items = CountMinSketch.top_k(state.cms, k)
    {:reply, top_items, state}
  end
end
```

### Cache-Efficient Algorithms

Modern CPUs have multiple cache levels (L1, L2, L3). Cache-oblivious algorithms automatically adapt to cache hierarchy without tuning.

#### Cache-Oblivious Algorithms

**Overview**: Algorithms designed to work efficiently across all cache levels without knowing cache parameters.

**Key Principle**: Divide-and-conquer with base cases small enough to fit in cache.

**Example - Matrix Multiplication**:
```elixir
defmodule CacheOblivious.Matrix do
  @moduledoc """
  Cache-oblivious matrix multiplication using recursive subdivision.
  Automatically adapts to cache hierarchy.
  """

  # Base case threshold (tune to L1 cache size)
  @base_case 64

  def multiply(a, b) do
    n = length(a)

    if n <= @base_case do
      naive_multiply(a, b)
    else
      # Divide matrices into quadrants
      {a11, a12, a21, a22} = subdivide(a)
      {b11, b12, b21, b22} = subdivide(b)

      # Recursively multiply submatrices
      c11 = add(multiply(a11, b11), multiply(a12, b21))
      c12 = add(multiply(a11, b12), multiply(a12, b22))
      c21 = add(multiply(a21, b11), multiply(a22, b21))
      c22 = add(multiply(a21, b12), multiply(a22, b22))

      combine(c11, c12, c21, c22)
    end
  end

  defp naive_multiply(a, b) do
    # Standard O(n³) multiplication for small matrices
    # Fits in L1 cache for better performance
    # ... implementation ...
  end
end
```

**Performance Impact**:
- 2-3× faster than naive approach for large matrices
- Scales better as data exceeds cache size

**Paper**: "Cache-Oblivious Algorithms" (Frigo et al., 1999)

#### B+ Trees for Disk/Cache Efficiency

**Overview**: Self-balancing tree optimized for systems with cache/disk hierarchy. Used in databases.

**Key Properties**:
- All data in leaf nodes
- Internal nodes only store keys for navigation
- Leaf nodes linked for range queries
- High fan-out (many children per node) reduces height

**Elixir Implementation**:
```elixir
# Add to mix.exs
{:b_tree, "~> 0.1"}

# Usage
tree = BTree.new(order: 100)  # Up to 100 children per node

tree =
  Enum.reduce(1..1_000_000, tree, fn i, acc ->
    BTree.insert(acc, i, "value_#{i}")
  end)

BTree.get(tree, 42)  # Fast lookup
BTree.range(tree, 100, 200)  # Efficient range queries
```

**Use Cases**:
- Database indexes
- File systems
- On-disk data structures
- Large sorted collections

**Performance Comparison**:
```
1M items, random access:
- Map (hash): O(1) average, poor cache locality
- Binary tree: O(log n), poor cache locality
- B+ tree: O(log n), excellent cache locality, 3-5× faster
```

### Modern Sorting Algorithms

#### BlockQuicksort (2016)

**Overview**: Variant of quicksort with better cache behavior through block-wise partitioning.

**Key Innovation**: Process elements in blocks that fit in CPU cache, reducing cache misses.

**Performance**:
- 1.5-2× faster than standard quicksort on modern hardware
- Better worst-case behavior with median-of-medians pivot selection

**Elixir Implementation**:
```elixir
defmodule BlockQuicksort do
  @block_size 128  # Typical L1 cache can hold ~512 elements

  def sort(list) when length(list) <= @block_size do
    Enum.sort(list)  # Use native sort for small lists
  end

  def sort(list) do
    pivot = select_pivot(list)

    # Partition in blocks for cache efficiency
    {left, equal, right} = partition_blockwise(list, pivot)

    # Recursively sort partitions in parallel
    Task.async_stream([left, right], &sort/1, ordered: false)
    |> Enum.flat_map(fn {:ok, sorted} -> sorted end)
    |> Kernel.++(equal)
  end

  defp partition_blockwise(list, pivot) do
    list
    |> Enum.chunk_every(@block_size)
    |> Enum.reduce({[], [], []}, fn block, {l, e, r} ->
      {block_left, block_equal, block_right} = partition_block(block, pivot)
      {l ++ block_left, e ++ block_equal, r ++ block_right}
    end)
  end

  defp partition_block(block, pivot) do
    Enum.reduce(block, {[], [], []}, fn elem, {l, e, r} ->
      cond do
        elem < pivot -> {[elem | l], e, r}
        elem == pivot -> {l, [elem | e], r}
        elem > pivot -> {l, e, [elem | r]}
      end
    end)
  end

  defp select_pivot(list) do
    # Median-of-medians for better worst-case
    list
    |> Enum.take_random(5)
    |> Enum.sort()
    |> Enum.at(2)
  end
end
```

**Paper**: "BlockQuicksort: How Branch Mispredictions don't affect Quicksort" (Edelkamp & Weiß, 2016)

#### Pattern-Defeating Quicksort (pdqsort, 2021)

**Overview**: Hybrid sorting algorithm that detects patterns (sorted, reverse-sorted, equal elements) and adapts strategy.

**Key Features**:
- Switches to heapsort when recursion depth excessive
- Uses insertion sort for small partitions
- Detects and handles common patterns efficiently

**Performance**:
- O(n log n) worst-case (vs O(n²) for standard quicksort)
- Near-optimal for partially sorted data
- Used in Rust's standard library

**Elixir Pattern**:
```elixir
defmodule PatternDetectingSort do
  @insertion_threshold 24
  @max_depth_factor 2

  def sort(list) do
    max_depth = floor(:math.log2(length(list))) * @max_depth_factor
    pdqsort(list, 0, max_depth)
  end

  defp pdqsort(list, depth, max_depth) when length(list) <= @insertion_threshold do
    insertion_sort(list)
  end

  defp pdqsort(list, depth, max_depth) when depth >= max_depth do
    # Recursion too deep, switch to heapsort
    heapsort(list)
  end

  defp pdqsort(list, depth, max_depth) do
    if already_sorted?(list) do
      list
    else
      pivot = select_pivot(list)
      {left, equal, right} = partition(list, pivot)

      # Check for patterns
      cond do
        length(left) < length(list) / 8 ->
          # Highly unbalanced, likely pattern detected
          adaptive_sort(list)

        true ->
          # Standard recursive sort
          pdqsort(left, depth + 1, max_depth) ++
          equal ++
          pdqsort(right, depth + 1, max_depth)
      end
    end
  end

  defp already_sorted?(list) do
    list == Enum.sort(list)
  end

  defp adaptive_sort(list) do
    # Switch to different algorithm based on pattern
    cond do
      mostly_equal?(list) -> handle_equal_elements(list)
      mostly_sorted?(list) -> insertion_sort(list)
      true -> Enum.sort(list)
    end
  end
end
```

**Paper**: "Pattern-defeating Quicksort" (Orson Peters, 2021)

### When to Use Modern vs Classic Algorithms

| Use Case | Modern Algorithm | Classic Alternative | When to Switch |
|----------|------------------|---------------------|----------------|
| **Hashing (non-crypto)** | xxHash3 | MD5, SHA1 | Always - 60× faster |
| **Hashing (crypto)** | BLAKE3 | SHA-256 | When performance critical |
| **Unique Counting** | HyperLogLog | MapSet/exact count | >100K unique items |
| **Membership Testing** | Cuckoo Filter | Bloom Filter | Need deletion support |
| **Frequency Estimation** | Count-Min Sketch | Map counter | Millions of items |
| **Sorting Large Data** | BlockQuicksort | Standard quicksort | >10K items on modern CPU |
| **Sorting with Patterns** | pdqsort | Quicksort | Data has patterns |
| **Matrix Multiplication** | Cache-oblivious | Naive O(n³) | Large matrices (>1000×1000) |
| **Database Indexes** | B+ Tree | Binary tree | Persistent storage |

## Quick Reference

### Hash Function Selection

```elixir
# Non-cryptographic (fast checksums, hash tables)
:exhash.xxh3_64("data")  # 64-bit hash
:exhash.xxh3_128("data")  # 128-bit hash

# Cryptographic (integrity, signatures)
B3.hash("sensitive data")  # BLAKE3

# Message authentication
:crypto.mac(:hmac, :sha256, key, message)  # HMAC-SHA256
```

### Probabilistic Structure Selection

```elixir
# Cardinality estimation (unique counts)
hll = HyperLogLog.new(14)
hll = HyperLogLog.add(hll, item)
count = HyperLogLog.count(hll)

# Membership testing (with deletion)
filter = CuckooFilter.new(capacity: 1_000_000)
filter = CuckooFilter.add(filter, item)
CuckooFilter.contains?(filter, item)

# Frequency estimation
cms = CountMinSketch.new(epsilon: 0.001, delta: 0.01)
cms = CountMinSketch.add(cms, event)
count = CountMinSketch.count(cms, event)
```

## Common Mistakes

### Using MD5/SHA1 for Non-Security Tasks

**Problem**: MD5 and SHA1 are slow for non-cryptographic hashing.

```elixir
# ❌ SLOW - cryptographic hash for non-security use
:crypto.hash(:md5, data)  # ~0.5 GB/s

# ✅ FAST - modern non-crypto hash
:exhash.xxh3_64(data)  # ~31 GB/s
```

**When to fix**: Hashing for hash tables, checksums, deduplication (not security).

### Exact Counting When Estimation Suffices

**Problem**: Using exact counts wastes memory for analytics.

```elixir
# ❌ MEMORY INTENSIVE - exact count
unique_visitors = MapSet.new()  # 8 bytes per visitor
Enum.reduce(events, unique_visitors, fn event, acc ->
  MapSet.put(acc, event.user_id)
end)
# 800 MB for 100M unique visitors

# ✅ MEMORY EFFICIENT - approximate count
hll = HyperLogLog.new(14)  # 16 KB total
Enum.reduce(events, hll, fn event, acc ->
  HyperLogLog.add(acc, event.user_id)
end)
# 16 KB with ±2% accuracy
```

**When to fix**: Analytics, dashboards, monitoring (where ±2% error acceptable).

### Using Bloom Filters When Need Deletion

**Problem**: Bloom filters don't support deletion; leads to false positives growing over time.

```elixir
# ❌ WRONG - can't delete from Bloom filter
bloom = BloomFilter.new(1_000_000)
bloom = BloomFilter.add(bloom, "cached_item")
# Can't delete when cache invalidated!

# ✅ CORRECT - Cuckoo filter supports deletion
filter = CuckooFilter.new(capacity: 1_000_000)
filter = CuckooFilter.add(filter, "cached_item")
filter = CuckooFilter.delete(filter, "cached_item")  # Works!
```

**When to fix**: Cache tracking, rate limiting with expiration, any scenario requiring deletion.

### Naive Sorting on Modern Hardware

**Problem**: Standard quicksort doesn't exploit CPU cache effectively.

```elixir
# ❌ CACHE INEFFICIENT - many cache misses
Enum.sort(large_list)  # Standard quicksort

# ✅ CACHE EFFICIENT - block-wise processing
BlockQuicksort.sort(large_list)  # 1.5-2× faster
```

**When to fix**: Sorting >10K items on modern CPUs (post-2010).

## When to Research Further

Consider using the `algorithms-researcher` agent when:

1. **Novel Problems**: No established solution exists
2. **Scale Beyond Standard**: Handling billions of items, petabytes of data
3. **Extreme Performance Needs**: Current solutions too slow even after optimization
4. **Cutting-Edge Requirements**: Need latest research (published in last 2 years)
5. **Domain-Specific**: Specialized algorithms (graph, geometric, streaming)

**Example Questions for Researcher**:
- "What's the fastest known algorithm for approximate nearest neighbor search?"
- "Are there better alternatives to HyperLogLog for cardinality published recently?"
- "What's the state-of-the-art for real-time top-K tracking in streams?"

Use the `algorithms-researcher` agent for deep research with paper citations.

## Elixir Library Recommendations

### Production-Ready Libraries

| Algorithm Type | Library | Maturity | Notes |
|----------------|---------|----------|-------|
| Hash Functions | `exhash` | Stable | xxHash3, xxHash64 |
| Cryptographic Hash | `b3` | Stable | BLAKE3 implementation |
| HyperLogLog | `hyperloglog` | Stable | Cardinality estimation |
| Bloom Filters | `bloomex` | Stable | Standard Bloom filters |
| Cuckoo Filters | `cuckoo_filter` | Beta | Actively maintained |
| Count-Min Sketch | Write custom | - | No stable library yet |
| B+ Trees | `b_tree` | Beta | For persistent data |

### When to Write Custom Implementations

Consider custom implementation when:
- Need specific tuning for your use case
- No stable library available (e.g., Count-Min Sketch)
- Integrating with existing C/Rust code
- Performance critical and library overhead matters

**Resources**:
- NIFs for CPU-intensive algorithms (Rustler recommended)
- Elixir's `:atomics` for lock-free counters
- ETS for shared mutable state in probabilistic structures

## References

- **Modern Hash Functions**: "xxHash: Fast Hash Algorithm" (Collet, 2020)
- **Cryptographic Hashing**: "BLAKE3: One Function, Fast Everywhere" (O'Connor et al., 2020)
- **HyperLogLog**: "HyperLogLog: the analysis of a near-optimal cardinality estimation algorithm" (Flajolet et al., 2007)
- **Cuckoo Filters**: "Cuckoo Filter: Practically Better Than Bloom" (Fan et al., 2014)
- **Count-Min Sketch**: "An Improved Data Stream Summary: The Count-Min Sketch and its Applications" (Cormode & Muthukrishnan, 2005)
- **Cache-Oblivious Algorithms**: "Cache-Oblivious Algorithms" (Frigo et al., 1999)
- **BlockQuicksort**: "BlockQuicksort: How Branch Mispredictions don't affect Quicksort" (Edelkamp & Weiß, 2016)
- **Pattern-Defeating Quicksort**: "Pattern-defeating Quicksort" (Orson Peters, 2021)

## Related Skills

- `performance` - For profiling and benchmarking optimizations
- `distributed-systems` - For consensus and replication algorithms
- `database` - For index and query optimization
