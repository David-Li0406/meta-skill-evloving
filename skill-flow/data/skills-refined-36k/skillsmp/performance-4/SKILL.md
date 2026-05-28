---
name: performance
description: This skill should be used when the user asks about "Ruby performance", "optimization", "profiling", "benchmarking", "memory", "garbage collection", "GC", "benchmark-ips", "stackprof", "memory_profiler", "slow code", "speed up Ruby", or needs guidance on making Ruby code faster.
version: 1.0.0
---

# Ruby Performance Optimization

Guide to profiling, benchmarking, and optimizing Ruby code.

## Profiling First

Always measure before optimizing. Identify bottlenecks with profiling tools.

### benchmark-ips

Compare implementations with statistical significance:

```ruby
require "benchmark/ips"

Benchmark.ips do |x|
  x.report("map + flatten") do
    [[1, 2], [3, 4]].map { |a| a * 2 }.flatten
  end

  x.report("flat_map") do
    [[1, 2], [3, 4]].flat_map { |a| a * 2 }
  end

  x.compare!
end

# Output:
# flat_map:  1234567.8 i/s
# map + flatten: 987654.3 i/s - 1.25x slower
```

### stackprof (CPU Profiling)

```ruby
require "stackprof"

StackProf.run(mode: :cpu, out: "tmp/stackprof.dump") do
  # Code to profile
  1000.times { expensive_operation }
end

# View results
# $ stackprof tmp/stackprof.dump --text
# $ stackprof tmp/stackprof.dump --method 'YourClass#method'
```

### memory_profiler

```ruby
require "memory_profiler"

report = MemoryProfiler.report do
  # Code to analyze
  data = process_large_dataset
end

report.pretty_print
# Shows allocated objects, retained objects, memory by gem/file/location
```

## Memory Optimization

### Reduce Object Allocations

```ruby
# Bad: Creates many intermediate objects
def bad_join(items)
  result = ""
  items.each do |item|
    result = result + item.to_s + ", "  # Creates new strings each time
  end
  result
end

# Good: Modify in place
def good_join(items)
  result = +""  # Unfrozen empty string
  items.each do |item|
    result << item.to_s << ", "
  end
  result
end

# Best: Use built-in
items.join(", ")
```

### Frozen String Literals

```ruby
# frozen_string_literal: true

# All string literals are now frozen (immutable)
# Reduces memory by reusing string objects
name = "Alice"  # Frozen, shared across uses
```

### Symbol vs String

```ruby
# Symbols are interned (shared in memory)
# Good for hash keys, identifiers
hash = { name: "Alice", age: 30 }  # Symbol keys

# Strings are mutable, not shared
# Good for user data, content
hash = { "user_input" => value }
```

### Lazy Enumerables

```ruby
# Bad: Loads entire file into memory
File.readlines("large.txt").select { |l| l.include?("ERROR") }.first(10)

# Good: Processes line by line, stops early
File.foreach("large.txt")
    .lazy
    .select { |l| l.include?("ERROR") }
    .first(10)
```

### Object Pooling

```ruby
class ConnectionPool
  def initialize(size:)
    @available = Array.new(size) { create_connection }
    @mutex = Mutex.new
  end

  def with_connection
    conn = checkout
    yield conn
  ensure
    checkin(conn)
  end

  private

  def checkout
    @mutex.synchronize { @available.pop }
  end

  def checkin(conn)
    @mutex.synchronize { @available.push(conn) }
  end

  def create_connection
    # Expensive connection creation
  end
end
```

## Algorithm Optimization

### Choose Right Data Structures

```ruby
require "set"

# O(n) lookup
array = [1, 2, 3, 4, 5]
array.include?(3)  # Slow for large arrays

# O(1) lookup
set = Set[1, 2, 3, 4, 5]
set.include?(3)  # Fast

# O(1) lookup with value
hash = { 1 => true, 2 => true, 3 => true }
hash.key?(3)  # Fast
```

### Avoid N+1 in Ruby Code

```ruby
# Bad: O(n*m) - nested iteration
users.each do |user|
  user.orders.each do |order|
    # O(n*m) iterations
  end
end

# Better: Pre-group data
orders_by_user = orders.group_by(&:user_id)
users.each do |user|
  user_orders = orders_by_user[user.id] || []
  # O(n) + O(m) iterations
end
```

### Memoization

```ruby
class ExpensiveCalculator
  def result
    @result ||= compute_expensive_result
  end

  # For methods with arguments
  def calculate(n)
    @cache ||= {}
    @cache[n] ||= expensive_computation(n)
  end

  # Clear cache when needed
  def clear_cache!
    @result = nil
    @cache = nil
  end
end
```

## Garbage Collection

### Understanding GC

```ruby
# Check GC stats
GC.stat
# => { count: 42, heap_allocated_pages: 100, ... }

# Manual GC (usually not needed)
GC.start

# Disable during benchmarks (not in production)
GC.disable
# ... run benchmark ...
GC.enable
```

### Reduce GC Pressure

```ruby
# Bad: Many short-lived objects
def bad_process(items)
  items.map { |i| i.to_s }
       .map { |s| s.upcase }
       .map { |s| s.strip }
end

# Good: Chain operations, fewer intermediates
def good_process(items)
  items.map { |i| i.to_s.upcase.strip }
end

# Best: Modify in place when possible
def best_process(items)
  items.each do |i|
    # Modify i in place if possible
  end
end
```

### GC Tuning Environment Variables

```bash
# Increase heap slots (reduce GC frequency)
# Note: These values are examples. Profile your application first
# and adjust based on actual memory usage patterns.
RUBY_GC_HEAP_INIT_SLOTS=600000

# Increase malloc limit before GC
RUBY_GC_MALLOC_LIMIT=64000000

# Growth factor for heap
RUBY_GC_HEAP_GROWTH_FACTOR=1.25
```

**Warning:** GC tuning values should be determined through profiling your specific application. Avoid cargo-cult optimization by copying values without understanding your application's memory patterns. Always measure before and after tuning.

## Concurrency

### Threads for I/O

```ruby
require "concurrent"

# Thread pool for I/O-bound work
pool = Concurrent::ThreadPoolExecutor.new(
  min_threads: 5,
  max_threads: 10,
  max_queue: 100
)

urls.each do |url|
  pool.post do
    fetch_url(url)
  end
end

pool.shutdown
pool.wait_for_termination
```

### Ractors for CPU

```ruby
# True parallelism for CPU-bound work
ractors = data.each_slice(data.size / 4).map do |chunk|
  Ractor.new(chunk) do |items|
    items.map { |item| expensive_computation(item) }
  end
end

results = ractors.flat_map(&:take)
```

### Async for I/O

```ruby
require "async"

Async do
  results = urls.map do |url|
    Async do
      fetch_url(url)
    end
  end.map(&:wait)
end
```

## Common Optimizations

### String Building

```ruby
# Bad
result = ""
items.each { |i| result += i.to_s }

# Good
result = items.map(&:to_s).join

# Also good for large strings
io = StringIO.new
items.each { |i| io << i.to_s }
result = io.string
```

### Array Operations

```ruby
# Use appropriate methods
array.any? { |x| x > 5 }  # Stops at first match
array.all? { |x| x > 5 }  # Stops at first failure
array.find { |x| x > 5 }  # Returns first match

# Avoid repeated operations
# Bad
array.count > 0   # Counts all elements
# Good
array.any?        # Stops immediately

# Bad
array.select { ... }.first
# Good
array.find { ... }
```

### Hash Operations

```ruby
# Use fetch with default
hash.fetch(:key, default_value)
hash.fetch(:key) { compute_default }

# Transform keys/values efficiently
hash.transform_keys(&:to_sym)
hash.transform_values(&:to_s)

# Merge in place
hash.merge!(other_hash)  # Modifies hash
```

## Additional Resources

### Reference Files

- **`references/profiling-guide.md`** - Detailed profiling workflows and tool usage
