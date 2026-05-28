# Sections

This file defines all sections, their ordering, impact levels, and descriptions.
The section ID (in parentheses) is the filename prefix used to group rules.

---

## 1. I/O Patterns (io)

**Impact:** CRITICAL  
**Description:** I/O is the #1 bottleneck for Python services. Blocking I/O serializes otherwise parallelizable work, wasting CPU cycles waiting for network and disk.

## 2. Async Concurrency (async)

**Impact:** CRITICAL  
**Description:** Sequential awaits create waterfalls that multiply latency. Proper async patterns with gather/TaskGroup yield 2-10× improvement for I/O-bound code.

## 3. Memory Management (mem)

**Impact:** HIGH  
**Description:** Memory allocation and object creation overhead compounds in hot paths. Using __slots__, generators, and efficient data structures reduces memory footprint by 30-50%.

## 4. Data Structures (ds)

**Impact:** HIGH  
**Description:** Wrong data structure choice leads to O(n) instead of O(1) operations. Sets and dicts provide constant-time lookups; deque beats list for queue operations.

## 5. Algorithm Efficiency (algo)

**Impact:** MEDIUM-HIGH  
**Description:** Algorithm complexity dominates at scale. List comprehensions, generator expressions, and built-in functions outperform manual loops by 2-5×.

## 6. Concurrency Model (conc)

**Impact:** MEDIUM  
**Description:** GIL limits threading for CPU-bound work. Choosing the right concurrency model—asyncio, threading, or multiprocessing—determines scalability.

## 7. Serialization (serial)

**Impact:** MEDIUM  
**Description:** JSON/pickle overhead adds up in hot paths. Efficient serialization with orjson, msgpack, or Protocol Buffers reduces CPU and memory pressure.

## 8. Caching and Memoization (cache)

**Impact:** LOW-MEDIUM  
**Description:** functools.lru_cache and manual caching prevent redundant computation but add memory overhead. Use strategically on expensive, frequently-called functions.

## 9. Runtime Tuning (runtime)

**Impact:** LOW  
**Description:** Python 3.11+ optimizations, interpreter settings, and micro-optimizations for hot paths provide incremental but measurable gains.
