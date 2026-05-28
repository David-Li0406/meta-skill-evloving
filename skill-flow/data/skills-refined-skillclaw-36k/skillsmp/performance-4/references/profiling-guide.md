# Profiling Guide

Detailed workflows for profiling Ruby applications.

## Complete Profiling Workflow

### 1. Identify the Problem

```ruby
# Start with simple timing
require "benchmark"

time = Benchmark.measure do
  # Code to measure
  result = process_data(input)
end

puts time  # =>   0.234567   0.012345   0.246912 (  0.250000)
#               user        system      total       real
```

### 2. CPU Profiling with StackProf

```ruby
# Add to Gemfile
# gem 'stackprof'

require "stackprof"

# Profile a block
StackProf.run(mode: :cpu, out: "tmp/cpu_profile.dump", raw: true) do
  # Code to profile
  1000.times { process_request }
end

# Profile for wall time (includes I/O wait)
StackProf.run(mode: :wall, out: "tmp/wall_profile.dump") do
  make_api_calls
end

# Profile object allocations
StackProf.run(mode: :object, out: "tmp/object_profile.dump") do
  generate_report
end
```

Analyze results:

```bash
# Summary
stackprof tmp/cpu_profile.dump --text

# Detailed method breakdown
stackprof tmp/cpu_profile.dump --method 'User#calculate_score'

# Flamegraph (visual)
stackprof tmp/cpu_profile.dump --flamegraph > flamegraph.html

# Call tree
stackprof tmp/cpu_profile.dump --text --limit 20
```

### 3. Memory Profiling

```ruby
require "memory_profiler"

# Basic memory report
report = MemoryProfiler.report do
  data = load_and_process_file("large.csv")
end

report.pretty_print

# Detailed options
report = MemoryProfiler.report(
  top: 50,                    # Top N allocations
  trace: [String, Array],     # Only trace specific classes
  ignore_files: /gems/        # Ignore gem internals
) do
  process_data
end

# Save to file
report.pretty_print(to_file: "memory_report.txt")
```

### 4. Allocation Tracing

```ruby
require "allocation_tracer"

# Trace allocations
AllocationTracer.trace do
  result = process_data
end

# Get results
AllocationTracer.results.each do |k, v|
  path, line, type = k
  count, old_count, total_age, min_age, max_age, memsize = v
  puts "#{type} at #{path}:#{line} - #{count} allocations"
end
```

## Benchmarking Best Practices

### Warming Up

```ruby
require "benchmark/ips"

Benchmark.ips do |x|
  x.config(warmup: 2, time: 5)  # 2s warmup, 5s measurement

  x.report("implementation A") { method_a }
  x.report("implementation B") { method_b }

  x.compare!
end
```

### Isolating Variables

```ruby
# Bad: Results affected by GC
Benchmark.ips do |x|
  x.report("test") { allocate_many_objects }
end

# Good: Disable GC during benchmark
GC.disable
Benchmark.ips do |x|
  x.report("test") { allocate_many_objects }
end
GC.enable
GC.start
```

### Statistical Significance

```ruby
# benchmark-ips handles this, but verify with multiple runs
3.times do
  Benchmark.ips do |x|
    x.report("A") { method_a }
    x.report("B") { method_b }
    x.compare!
  end
  puts "---"
end
```

## Production Profiling

### rack-mini-profiler

```ruby
# Gemfile
gem 'rack-mini-profiler', require: false

# config/initializers/mini_profiler.rb
require 'rack-mini-profiler'
Rack::MiniProfiler.config.position = 'bottom-right'
Rack::MiniProfiler.config.start_hidden = true
```

### Skylight / Scout / NewRelic

For production APM:

```ruby
# Gemfile
gem 'skylight'  # or 'scout_apm' or 'newrelic_rpm'

# Custom instrumentation
class OrderProcessor
  include Skylight::Helpers

  instrument_method
  def process
    # Automatically traced
  end
end
```

### Custom Metrics

```ruby
class PerformanceTracker
  def self.track(name)
    start = Process.clock_gettime(Process::CLOCK_MONOTONIC)
    result = yield
    duration = Process.clock_gettime(Process::CLOCK_MONOTONIC) - start

    Rails.logger.info("Performance: #{name} took #{duration.round(3)}s")
    StatsD.timing(name, duration * 1000)

    result
  end
end

PerformanceTracker.track("order.process") do
  order.process!
end
```

## Optimization Checklist

### Before Optimizing

- [ ] Have you profiled to find the actual bottleneck?
- [ ] Is the bottleneck in your code or a dependency?
- [ ] Have you established a baseline measurement?
- [ ] Do you have tests to ensure correctness after changes?

### During Optimization

- [ ] Are you optimizing the right thing (Pareto principle)?
- [ ] Have you tried algorithmic improvements first?
- [ ] Are you measuring after each change?
- [ ] Is the optimization worth the code complexity?

### After Optimizing

- [ ] Have you verified the improvement with benchmarks?
- [ ] Have you tested for correctness?
- [ ] Have you documented why the optimization was needed?
- [ ] Have you considered edge cases?

## Common Bottlenecks

### 1. Database (most common in web apps)

```ruby
# Use explain to understand queries
User.where(active: true).explain

# Check for N+1 queries with bullet gem
# gem 'bullet'
```

### 2. External API Calls

```ruby
# Profile with timing
require "net/http"

def timed_request(url)
  start = Time.now
  response = Net::HTTP.get_response(URI(url))
  duration = Time.now - start
  puts "Request to #{url} took #{duration}s"
  response
end

# Consider async/parallel requests
```

### 3. Serialization

```ruby
# Compare JSON libraries
Benchmark.ips do |x|
  x.report("JSON") { JSON.generate(data) }
  x.report("Oj") { Oj.dump(data) }
  x.compare!
end
```

### 4. Template Rendering

```ruby
# Profile view rendering
ActiveSupport::Notifications.subscribe("render_template.action_view") do |event|
  puts "Rendered #{event.payload[:identifier]} in #{event.duration}ms"
end
```
