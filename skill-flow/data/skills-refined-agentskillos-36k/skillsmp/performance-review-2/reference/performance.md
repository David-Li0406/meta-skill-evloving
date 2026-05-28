# Performance Optimization

## Profile Before Optimizing

**Never optimize without profiling first.** Premature optimization wastes time and often makes code harder to maintain.

### The Optimization Workflow

1. **Write correct code first** - Get it working
2. **Measure performance** - Identify actual bottlenecks
3. **Optimize hot paths** - Focus on measured problems
4. **Verify improvement** - Measure again to confirm
5. **Ensure correctness** - Run tests to verify no regressions

### Profiling Tools

**C++ Profiling**:
```bash
# CPU profiling with perf (Linux)
perf record -g ./program
perf report

# CPU profiling with Instruments (macOS)
instruments -t "Time Profiler" ./program

# Valgrind callgrind
valgrind --tool=callgrind ./program
kcachegrind callgrind.out.*
```

**Python Profiling**:
```python
import cProfile
import pstats

# Profile a function
cProfile.run('expensive_function()', 'profile_stats')

# Analyze results
stats = pstats.Stats('profile_stats')
stats.sort_stats('cumulative')
stats.print_stats(10)  # Top 10 functions
```

```bash
# Line-by-line profiling
pip install line_profiler
kernprof -l -v script.py
```

**Kotlin/Java Profiling**:
```bash
# JProfiler, YourKit, VisualVM
# Or use built-in JFR (Java Flight Recorder)
java -XX:StartFlightRecording=duration=60s,filename=recording.jfr MyApp
```

## Identify Bottlenecks

### Common Performance Issues

1. **Algorithmic complexity** - O(n²) where O(n log n) possible
2. **Excessive allocations** - Creating temporary objects in loops
3. **Cache misses** - Poor data locality
4. **I/O bottlenecks** - Unbuffered or synchronous I/O
5. **Lock contention** - Over-synchronization in concurrent code
6. **Database queries** - N+1 query problem, missing indexes

### Performance Hotspots

Focus on code that:
- Appears high in profiler output
- Runs frequently (inner loops)
- Processes large amounts of data
- Performs I/O operations

## Reduce Overhead

### Minimize Allocations

❌ **Excessive allocations**:
```cpp
std::vector<int> processData(const std::vector<int>& input) {
    std::vector<int> result;
    for (int value : input) {
        result.push_back(value * 2);  // May reallocate multiple times
    }
    return result;
}
```

✅ **Pre-allocate**:
```cpp
std::vector<int> processData(const std::vector<int>& input) {
    std::vector<int> result;
    result.reserve(input.size());  // Allocate once
    for (int value : input) {
        result.push_back(value * 2);
    }
    return result;
}
```

✅ **In-place transformation** (when possible):
```cpp
void processDataInPlace(std::vector<int>& data) {
    for (int& value : data) {
        value *= 2;  // No allocation
    }
}
```

### Avoid Unnecessary Copies

❌ **Unnecessary copying**:
```cpp
void processUser(User user) {  // Copies entire User object
    // ...
}

std::string getName() {
    return userName;  // May copy string
}
```

✅ **Pass by const reference**:
```cpp
void processUser(const User& user) {  // No copy, read-only
    // ...
}

void modifyUser(User& user) {  // No copy, modifiable
    // ...
}

const std::string& getName() const {  // No copy
    return userName;
}
```

✅ **Move semantics** (C++):
```cpp
std::vector<int> createLargeVector() {
    std::vector<int> result(1000000);
    // ... populate vector
    return result;  // Moved, not copied (NRVO or move)
}

void takeOwnership(std::unique_ptr<Resource> resource) {
    // resource moved in, no copy
}
```

### Efficient Data Structures

Choose the right data structure for the access pattern:

| Operation | Vector/Array | List | Hash Map | Tree Map |
|-----------|--------------|------|----------|----------|
| Random access | O(1) | O(n) | O(1) avg | O(log n) |
| Insert at end | O(1) amortized | O(1) | O(1) avg | O(log n) |
| Insert at beginning | O(n) | O(1) | N/A | N/A |
| Search | O(n) | O(n) | O(1) avg | O(log n) |
| Ordered iteration | ✓ | ✓ | ✗ | ✓ |

**Example**:
```cpp
// Need fast lookup by key? Use hash map
std::unordered_map<UserId, User> userCache;

// Need ordered iteration? Use tree map
std::map<Timestamp, Event> eventLog;

// Need fast random access? Use vector
std::vector<Item> inventory;

// Need fast insertion/removal at both ends? Use deque
std::deque<Task> taskQueue;
```

### Efficient Algorithms

Replace inefficient algorithms:

❌ **Nested loops - O(n²)**:
```cpp
bool hasDuplicate(const std::vector<int>& data) {
    for (size_t i = 0; i < data.size(); ++i) {
        for (size_t j = i + 1; j < data.size(); ++j) {
            if (data[i] == data[j]) return true;
        }
    }
    return false;
}
```

✅ **Hash set - O(n)**:
```cpp
bool hasDuplicate(const std::vector<int>& data) {
    std::unordered_set<int> seen;
    for (int value : data) {
        if (!seen.insert(value).second) return true;
    }
    return false;
}
```

## Cache Optimization

### Data Locality

Access data sequentially when possible:

❌ **Poor cache locality**:
```cpp
// Array of pointers: data scattered in memory
std::vector<User*> users;
for (const auto* user : users) {
    process(user->name);  // Each access may be a cache miss
}
```

✅ **Good cache locality**:
```cpp
// Array of objects: data contiguous in memory
std::vector<User> users;
for (const auto& user : users) {
    process(user.name);  // Sequential access, cache-friendly
}
```

### Structure Packing

Order struct members to minimize padding:

❌ **Poor layout** (24 bytes on 64-bit):
```cpp
struct Data {
    char a;      // 1 byte + 7 padding
    double b;    // 8 bytes
    char c;      // 1 byte + 7 padding
};  // Total: 24 bytes
```

✅ **Optimized layout** (16 bytes):
```cpp
struct Data {
    double b;    // 8 bytes
    char a;      // 1 byte
    char c;      // 1 byte + 6 padding
};  // Total: 16 bytes
```

## I/O Optimization

### Buffered I/O

```cpp
// Unbuffered: many small writes
for (const auto& item : items) {
    file << item << '\n';  // Slow if not buffered
}

// Buffered: build string first, write once
std::ostringstream buffer;
for (const auto& item : items) {
    buffer << item << '\n';
}
file << buffer.str();  // Single write
```

### Asynchronous I/O

```cpp
// Synchronous: blocks until complete
auto data = readFile("data.txt");
processData(data);

// Asynchronous: continue while I/O in progress
auto future = std::async(std::launch::async, readFile, "data.txt");
// Do other work here
auto data = future.get();  // Wait for result when needed
processData(data);
```

## Compiler Optimizations

### Enable Optimization Flags

```bash
# C++ - Release build
g++ -O3 -DNDEBUG -march=native program.cpp

# C++ - Link-Time Optimization
g++ -O3 -flto program.cpp

# Disable debug assertions in release
g++ -O3 -DNDEBUG program.cpp  # NDEBUG disables assert()
```

### Help the Compiler

```cpp
// Inline small, frequently-called functions
inline int square(int x) {
    return x * x;
}

// Mark functions that don't throw
int calculate(int x) noexcept {
    return x * 2;
}

// Use const to enable optimizations
int sum(const std::vector<int>& data) {
    // Compiler knows data won't change
}

// Branch hints (C++20)
if (likely(normalCase)) {
    // Common path
} else {
    // Rare error path
}
```

## Performance Testing

### Benchmarking

**C++ with Google Benchmark**:
```cpp
#include <benchmark/benchmark.h>

static void BM_VectorPushBack(benchmark::State& state) {
    for (auto _ : state) {
        std::vector<int> vec;
        for (int i = 0; i < state.range(0); ++i) {
            vec.push_back(i);
        }
    }
}
BENCHMARK(BM_VectorPushBack)->Range(8, 8<<10);

BENCHMARK_MAIN();
```

**Python with timeit**:
```python
import timeit

# Quick benchmark
time = timeit.timeit('expensive_function()', number=1000)
print(f"Average time: {time/1000:.6f} seconds")

# Compare implementations
setup = "from mymodule import method1, method2"
time1 = timeit.timeit('method1()', setup=setup, number=10000)
time2 = timeit.timeit('method2()', setup=setup, number=10000)
print(f"method1: {time1:.4f}s, method2: {time2:.4f}s")
```

### Performance Regression Testing

```cpp
TEST(Performance, SearchPerformance) {
    auto start = std::chrono::high_resolution_clock::now();

    performSearch(largeDataset);

    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);

    // Ensure search completes within threshold
    EXPECT_LT(duration.count(), 100) << "Search took " << duration.count() << "ms";
}
```
