---
name: performance-profiling
description: Performance profiling and optimization for Elixir/BEAM applications
---

# Performance Profiling Skill

Use this skill when:
- Investigating performance issues in Elixir applications
- Optimizing database queries and N+1 problems
- Identifying bottlenecks in BEAM schedulers
- Optimizing GenServer and OTP processes
- Analyzing memory usage and leaks
- Implementing hot code reloading strategies

## When to Use

### Use this skill when:
- Your application is slow or has latency issues
- You're experiencing high CPU or memory usage
- You're seeing scheduler warnings in BEAM
- You're optimizing database queries
- You're implementing performance-critical features
- You're investigating memory leaks or garbage collection issues

### Key Scenarios

1. **Database Performance**: Slow queries, N+1 problems
2. **Process Performance**: Bottlenecks in GenServer/Supervisor
3. **Memory Issues**: High memory usage, GC pressure
4. **Scheduler Issues**: Process starvation, scheduler warnings
5. **CPU Intensive**: CPU-bound operations
6. **Latency Optimization**: Reducing response times

---

## Benchmarking

### Benchee

```elixir
# Add to deps
defp deps do
  [
    {:benchee, "~> 1.0"}
  ]
end

# Benchmark function
Benchee.run(%{
  "map" => fn ->
    Enum.map(1..1000, &(&1 * &1))
  end,
  "reduce" => fn ->
    Enum.reduce(1..1000, 0, &(&1 + &1))
  end
  "comprehension" => fn ->
    for n <- 1..1000, do: n * n
    end
  end)
)
```

### StreamData Benchmarking

```elixir
defmodule MyApp.Benchmarks do
  use ExUnit.Case
  use Benchee

  test "map vs comprehension performance" do
    data = Enum.to_list(1..10_000)
    
    benchees = %{
      "map" => fn ->
        Enum.map(data, &(&1 * &1))
      end,
      "comprehension" => fn ->
        for n <- data, do: n * n
      end
    end
    
    Benchee.run(benchees, time: 10, print: [configuration: false])
  end
end
end
```

---

## BEAM Profiling Tools

### 1. :eprof (Function Profiling)

```elixir
# Start eprof
:eprof.start()

# Run code to profile
result = MyApp.Computation.intensive_function()

# Stop eprof
:eprof.stop()

# Analyze results
:eprof.analyze(:eprof.results())

# Generate report
:eprof.display(:eprof.results())
```

### 2. :fprof (System Profiling)

```elixir
# Start fprof
:fprof.start()
:fprof.trace(:start)

# Run code to profile
result = MyApp.Computation.intensive_function()

# Stop fprof
:fprof.stop()

# Generate report
:fprof.report(:fprof.results())
```

### 3. :eper (Advanced Profiling)

```elixir
# Add to deps
defp deps do
  [
    {:eper, "~> 0.5"}
  ]
end

# Profile GenServer
defmodule MyApp.Worker do
  use GenServer
  use Eper

  def start_link(opts), do: GenServer.start_link(__MODULE__, opts, name: __MODULE__)

  @eper.label "worker computation"
  defp computation(data) do
    # Long-running computation
    :timer.sleep(100)
    {:processed, data}
  end

  @impl true
  def handle_call({:compute, data}, from, state) do
    result = computation(data)
    {:reply, {:ok, result}, state}
  end
end

# Run profile
Mix.Task.run(fn ->
  :eper.start()
  GenServer.call(MyApp.Worker, {:compute, :data})
  :eper.stop()
end)
```

---

## Memory Profiling

### 1. :erlang.memory()

```elixir
defmodule MyApp.MemoryProfiler do
  require Logger

  def profile_function(fun, label) do
    Logger.info("Profiling: #{label}")
    
    # Memory before
    memory_before = :erlang.memory(:total)
    
    # Run function
    result = fun.()
    
    # Memory after
    memory_after = :erlang.memory(:total)
    
    memory_diff = memory_after - memory_before
    Logger.info("Memory change for #{label}: #{format_bytes(memory_diff)}")
    
    {result, memory_diff}
  end

  def format_bytes(bytes) do
    cond do
      bytes < 1_000 ->
        "#{bytes} B"
      bytes < 1_000_000 ->
        "#{div(bytes, 1_000)} KB"
      bytes < 1_000_000_000 ->
        "#{div(bytes, 1_000_000)} MB"
      true ->
        "#{div(bytes, 1_000_000_000)} GB"
    end
  end
end
```

### 2. Memory Leak Detection

```elixir
defmodule MyApp.MemoryLeakDetector do
  use GenServer
  require Logger

  @check_interval 30_000  # 30 seconds

  def start_link(opts), do: GenServer.start_link(__MODULE__, opts, name: __MODULE__)

  @impl true
  def init(opts) do
    Logger.info("Starting memory leak detector")
    schedule_check()
    {:ok, %{snapshots: %{}, opts: opts}}
  end

  @impl true
  def handle_info(:check_memory, state) do
    take_memory_snapshot()
    analyze_memory_growth(state)
    schedule_check()
    {:noreply, state}
  end

  defp schedule_check do
    Process.send_after(self(), :check_memory, @check_interval)
  end

  defp take_memory_snapshot() do
    memory = :erlang.memory(:total)
    Logger.info("Memory snapshot: total=#{format_bytes(memory.total)}")
    GenServer.cast(__MODULE__, {:record_snapshot, memory})
  end

  defp analyze_memory_growth(state) do
    # Analyze memory growth patterns
    detect_memory_leaks(state)
    warn_on_high_memory(state)
  end

  defp detect_memory_leaks(state) do
    # Compare snapshots and detect leaks
    Enum.each(state.snapshots, fn {process, memory} ->
      memory_diff = memory.total - process.memory.total
      
      if memory_diff > 100_000_000 do  # 100 MB growth
        Logger.warning("Possible memory leak detected in #{process}")
      end
    end)
  end

  defp warn_on_high_memory(state) do
    memory = :erlang.memory(:total)
    threshold = Application.get_env(:my_app, :memory_warning_threshold, 1_000_000_000) # 1 GB

    if memory.total > threshold do
      Logger.error("High memory usage: #{format_bytes(memory.total)}")
    end
  end

  defp format_bytes(bytes) do
    cond do
      bytes < 1_000 -> "#{bytes} B"
      bytes < 1_000_000 -> "#{div(bytes, 1_000)} KB"
      bytes < 1_000_000_000 -> "#{div(bytes, 1_000_000)} MB"
      true -> "#{div(bytes, 1_000_000_000)} GB"
    end
  end
end
```

---

## GenServer Optimization

### 1. Non-blocking Callbacks

```elixir
defmodule MyApp.Worker do
  use GenServer
  require Logger

  # Client API
  def start_link(opts), do: GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  def process_data(data), do: GenServer.cast(__MODULE__, {:process, data})

  # Server Callbacks
  @impl true
  def init(opts), do: {:ok, opts}

  @impl true
  def handle_cast({:process, data}, state) do
    # Non-blocking: spawn task in separate process
    Task.start(fn ->
      result = do_heavy_work(data)
      GenServer.cast(__MODULE__, {:result, result})
    end)
    
    {:noreply, state}
  end

  @impl true
  def handle_cast({:result, result}, state) do
    # Store result or notify
    handle_result(result)
    {:noreply, state}
  end

  defp do_heavy_work(data) do
    :timer.sleep(1000) # Simulate heavy work
    {:processed, data}
  end
end
```

### 2. Process Message Handling

```elixir
defmodule MyApp.Worker do
  use GenServer
  require Logger

  @message_queue_size 1000

  def start_link(opts), do: GenServer.start_link(__MODULE__, opts, name: __MODULE__)

  @impl true
  def init(opts), do
    Logger.info("Starting optimized worker")
    {:ok, %{opts: opts, queue: :queue.new()}}
  end

  @impl true
  def handle_cast(msg, state) do
    new_queue = :queue.in(msg, state.queue)
    
    # If queue is empty after enqueuing, process messages
    if :queue.is_empty(new_queue) and :queue.len(state.queue) < @message_queue_size do
      Process.send_after(self(), :process_queue, 0)
    end
    
    {:noreply, %{state | queue: new_queue}}
  end

  @impl true
  def handle_info(:process_queue, state) do
    case :queue.out(state.queue) do
      {:empty, _queue} ->
        # No messages to process
        {:noreply, state}
      
      {:value, msg, new_queue} ->
        # Process message
        handle_message(msg)
        
        # Continue processing
        if :queue.is_empty(new_queue) do
          {:noreply, %{state | queue: new_queue}}
        else
          Process.send_after(self(), :process_queue, 0)
        end
    end
  end
end
```

---

## Database Query Optimization

### 1. N+1 Prevention

```elixir
defmodule MyApp.QueryOptimizer do
  require Logger

  def optimize_query(query) do
    Logger.info("Optimizing query")

    # Check for N+1 problems
    {optimized?, details} = check_n_plus_one(query)
    
    if optimized? do
      Logger.info("Query is optimized: #{details}")
      query
    else
      Logger.warning("N+1 problem detected: #{details}")
      fix_n_plus_one(query)
    end
  end

  defp check_n_plus_one(query) do
    # Check for missing preloads
    case detect_missing_preloads(query) do
      [] -> {true, "No N+1 problems"}
      missing_preloads ->
        {false, "Missing preloads: #{inspect(missing_preloads)}"}
    end
  end

  defp detect_missing_preloads(query) do
    # Use AST to analyze query
    # Simplified: check for association access in loop
    []
  end

  defp fix_n_plus_one(query) do
    # Add preload associations
    # Simplified: add common preloads
    MyApp.Repo.preload([:user, :comments], query)
  end
end
```

### 2. Query Profiling

```elixir
defmodule MyApp.QueryProfiler do
  require Logger

  def profile_query(query, iterations \\ 100) do
    Logger.info("Profiling query over #{iterations} iterations")

    start_time = System.monotonic_time(:millisecond)

    Enum.each(1..iterations, fn _i ->
      MyApp.Repo.all(query)
    end)

    end_time = System.monotonic_time(:millisecond)
    duration = end_time - start_time

    avg_duration = div(duration, iterations)
    Logger.info("Query profile: iterations=#{iterations}, total=#{duration}ms, avg=#{avg_duration}ms")

    %{iterations: iterations, total: duration, avg: avg_duration}
  end
end
```

---

## Hot Code Reloading

### 1. Code Reloader

```elixir
defmodule MyApp.CodeReloader do
  use GenServer
  require Logger

  def start_link(opts), do: GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  def reload_module(module), do: GenServer.call(__MODULE__, {:reload, module})

  @impl true
  def init(opts), do
    {:ok, opts}

  @impl true
  def handle_call({:reload, module}, _from, state) do
    Logger.info("Reloading module: #{inspect(module)}")

    # Reload module
    case Code.load_file(module.module_info(:file)) do
      {:module, _binary} ->
        Logger.info("Successfully reloaded: #{inspect(module)}")
        {:reply, {:ok, :reloaded}, state}
      
      {:error, reason} ->
        Logger.error("Failed to reload: #{inspect(module)}, reason: #{inspect(reason)}")
        {:reply, {:error, reason}, state}
    end
  end
end
```

### 2. Hot Code Swapping in Development

```elixir
# config/dev.exs
config :my_app,
  code_reloader: true

# application.ex
defmodule MyApp.Application do
  use Application

  def start(_type, _args) do
    children = []

    # Add code reloader in development
    if Application.get_env(:my_app, :code_reloader) do
      children = [
        {MyApp.CodeReloader, []} | children
      ]
    end

    opts = [strategy: :one_for_one, name: MyApp.Supervisor]
    Supervisor.start_link(children, opts)
  end
end
```

---

## Best Practices

### DO

✅ Benchmark before optimizing
✅ Use :eprof for function profiling
✅ Use :fprof for system profiling
✅ Profile memory usage and detect leaks
✅ Optimize GenServer callbacks (non-blocking)
✅ Process GenServer messages in batches
✅ Fix N+1 query problems
✅ Use hot code reloading in development
✅ Monitor scheduler and memory usage
✅ Optimize database queries with proper indexes
✅ Test optimizations with benchmarks

### DON'T

❌ Optimize without profiling
❌ Assume where bottlenecks are
❌ Ignore memory warnings
❌ Use blocking operations in GenServer callbacks
❌ Process one message at a time (batch when appropriate)
❌ Forget to commit optimization results
❌ Ignore scheduler warnings
❌ Optimize prematurely (measure first)
❌ Skip testing after optimization
❌ Ignore code quality for performance

---

## Integration with ai-rules

### Roles to Reference

- **Architect**: Use for performance design decisions
- **Orchestrator**: Implement optimizations and profiling
- **Reviewer**: Verify optimizations don't introduce bugs
- **QA**: Benchmark and test performance improvements

### Skills to Reference

- **distributed-systems**: Cluster performance monitoring
- **resilience-patterns**: Monitor for degradation patterns
- **observability**: Integrate performance metrics
- **test-generation**: Benchmark and test performance

---

## Summary

Performance profiling provides:
- ✅ Benchmarking tools (Benchee, StreamData)
- ✅ BEAM profiling (:eprof, :fprof, :eper)
- ✅ Memory leak detection
- ✅ GenServer optimization
- ✅ Database query optimization
- ✅ Hot code reloading strategies
- ✅ System performance monitoring

**Key**: Profile before optimizing, use benchmarks to verify improvements, and test all optimizations.
