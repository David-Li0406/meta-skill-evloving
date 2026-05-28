---
name: resilience-patterns
description: Resilience and error recovery patterns including circuit breaker, retry strategies, and graceful degradation
---

# Resilience Patterns Skill

Use this skill when:
- Building fault-tolerant distributed systems
- Implementing retry strategies with exponential backoff
- Creating circuit breaker patterns for failure isolation
- Designing graceful degradation strategies
- Building systems that continue working despite partial failures
- Implementing timeout handling and bulkhead patterns

## When to Use

### Use this skill when:
- Your application calls external services (APIs, databases, message queues)
- You need high availability despite component failures
- You're building distributed systems with unreliable networks
- You need to prevent cascading failures
- You're implementing retry logic for transient failures

### Key Scenarios

1. **External Service Calls**: APIs, databases, message queues may fail
2. **Network Issues**: Packet loss, latency spikes, partitions
3. **Service Degradation**: Third-party services may be slow or unavailable
4. **Resource Exhaustion**: Database connections, memory limits
5. **Partial System Failure**: Some components fail while others work

---

## Circuit Breaker Pattern

### 1. State Machine

```elixir
defmodule MyApp.CircuitBreaker do
  use GenServer
  require Logger

  @states [:closed, :open, :half_open]
  @default_threshold 5
  @default_timeout 60_000
  @default_retry_timeout 10_000

  # Client API
  def start_link(opts), do: GenServer.start_link(__MODULE__, opts, name: Keyword.get(opts, :name, __MODULE__})
  def call(service_name, fun, opts \\ []) do
    GenServer.call(__MODULE__, {:call, service_name, fun, opts})
  end

  # Server Callbacks
  @impl true
  def init(opts) do
    Logger.info("Starting circuit breaker")
    {:ok, %{
      state: :closed,
      failures: 0,
      threshold: Keyword.get(opts, :threshold, @default_threshold),
      timeout: Keyword.get(opts, :timeout, @default_timeout),
      retry_timeout: Keyword.get(opts, :retry_timeout, @default_retry_timeout),
      last_failure_time: nil,
      services: %{}
    }}
  end

  @impl true
  def handle_call({:call, service_name, fun, opts}, from, state) do
    case get_circuit_state(state, service_name) do
      :closed ->
        result = execute_and_track(service_name, fun, state)
        {:reply, result, state}
      :open ->
        Logger.warning("Circuit breaker OPEN for #{service_name}")
        {:reply, {:error, :circuit_open}, state}
      :half_open ->
        result = test_service(service_name, fun, state)
        {:reply, result, update_after_test(service_name, result, state)}
    end
  end

  @impl true
  def handle_info({:reset_circuit, service_name}, state) do
    Logger.info("Resetting circuit breaker for #{service_name}")
    {:noreply, reset_circuit(service_name, state)}
  end

  # Implementation
  defp get_circuit_state(state, service_name) do
    case get_in(state, [:services, service_name, :state]) do
      nil -> :closed
      circuit_state -> circuit_state
    end
  end

  defp execute_and_track(service_name, fun, state) do
    try do
      result = fun.()
      # Success: reset failures
      new_state = put_in(state, [:services, service_name], %{
        state: :closed,
        failures: 0,
        last_failure_time: nil
      })
      {:ok, result}
    rescue
      error ->
        Logger.error("Service #{service_name} failed: #{inspect(error)}")
        # Increment failures and check threshold
        failures = get_in(state, [:services, service_name, :failures, 0) + 1
        threshold = get_in(state, [:services, service_name, :threshold, state[:threshold])
        
        new_state = if failures >= threshold do
          Logger.warning("Circuit breaker opening for #{service_name} after #{failures} failures")
          timeout = get_in(state, [:services, service_name, :timeout, state[:timeout])
          # Schedule reset
          Process.send_after(self(), {:reset_circuit, service_name}, timeout)
          
          put_in(state, [:services, service_name], %{
            state: :open,
            failures: failures,
            last_failure_time: DateTime.utc_now()
          })
        else
          put_in(state, [:services, service_name, :failures, failures)
        end
        
        {:error, error}
    end
  end

  defp test_service(service_name, fun, state) do
    retry_timeout = get_in(state, [:services, service_name, :retry_timeout, state[:retry_timeout])
    
    try do
      result = fun.()
      # Success: close circuit
      new_state = put_in(state, [:services, service_name], %{
        state: :closed,
        failures: 0,
        last_failure_time: nil
      })
      {:ok, result}
    rescue
      error ->
        Logger.error("Service #{service_name} failed in half-open state")
        # Failure: open circuit
        timeout = get_in(state, [:services, service_name, :timeout, state[:timeout])
        Process.send_after(self(), {:reset_circuit, service_name}, timeout)
        
        new_state = put_in(state, [:services, service_name], %{
          state: :open,
          failures: get_in(state, [:services, service_name, :failures, 0) + 1,
          last_failure_time: DateTime.utc_now()
        })
        {:error, error}
    end
  end

  defp update_after_test(service_name, {:ok, _result}, state) do
    # Success in half-open: close circuit
    put_in(state, [:services, service_name, :state, :closed)
  end

  defp update_after_test(service_name, {:error, _reason}, state) do
    # Failure in half-open: open circuit
    timeout = get_in(state, [:services, service_name, :timeout, state[:timeout])
    Process.send_after(self(), {:reset_circuit, service_name}, timeout)
    
    put_in(state, [:services, service_name, %{
      state: :open,
      failures: get_in(state, [:services, service_name, :failures, 0) + 1,
      last_failure_time: DateTime.utc_now()
    })
  end

  defp reset_circuit(service_name, state) do
    put_in(state, [:services, service_name], %{
      state: :half_open,
      failures: 0,
      last_failure_time: nil
    })
  end
end
```

---

## Retry Strategies

### 1. Exponential Backoff

```elixir
defmodule MyApp.Retry do
  require Logger

  @default_max_attempts 3
  @default_base_delay 100
  @default_max_delay 10_000
  @default_jitter 0.1

  # Client API
  def with_retry(fun, opts \\ []) do
    max_attempts = Keyword.get(opts, :max_attempts, @default_max_attempts)
    base_delay = Keyword.get(opts, :base_delay, @default_base_delay)
    max_delay = Keyword.get(opts, :max_delay, @default_max_delay)
    jitter = Keyword.get(opts, :jitter, @default_jitter)
    
    do_retry(fun, max_attempts, base_delay, max_delay, jitter, 1)
  end

  # Implementation
  defp do_retry(fun, max_attempts, base_delay, max_delay, jitter, attempt) do
    Logger.info("Attempt #{attempt}/#{max_attempts}")

    try do
      result = fun.()
      {:ok, result}
    rescue
      error ->
        Logger.error("Attempt #{attempt} failed: #{inspect(error)}")

        if attempt < max_attempts do
          # Calculate delay with exponential backoff and jitter
          delay = calculate_delay(base_delay, max_delay, attempt, jitter)
          
          Logger.info("Retrying in #{delay}ms...")
          :timer.sleep(delay)
          
          # Retry
          do_retry(fun, max_attempts, base_delay, max_delay, jitter, attempt + 1)
        else
          # Max attempts reached
          Logger.error("Max attempts (#{max_attempts}) reached")
          {:error, error}
        end
    end
  end

  defp calculate_delay(base_delay, max_delay, attempt, jitter) do
    # Exponential backoff: base * 2^(attempt - 1)
    exponential_delay = base_delay * :math.pow(2, attempt - 1) |> trunc()
    
    # Cap at max delay
    capped_delay = min(exponential_delay, max_delay)
    
    # Add jitter to avoid thundering herd
    jitter_amount = trunc(capped_delay * jitter)
    random_jitter = :rand.uniform(jitter_amount)
    
    capped_delay + random_jitter
  end
end
```

### 2. Retry with Backoff Library

```elixir
# Use retry library
defp deps do
  [
    {:retry, "~> 0.18"}
  ]
end

defmodule MyApp.ExternalService do
  require Logger

  def call_api(data) do
    Retry.retry_while with_retry(data, &attempt_api_call/1, 3_000)
  end

  defp with_retry(data, fun, timeout) do
    Retry.retry(
      data,
      fn
        {:ok, result} = fun.(data)
        {:stop, {:ok, result}}
      end,
      # Retry only on transient errors
      should_retry?(&1),
      # Wait exponentially between retries
      retry_exp_backoff(100, 1_000),
      # Maximum timeout
      timeout
    )
  end

  defp attempt_api_call(data) do
    # Make API call
    case HTTPoison.post("https://api.example.com/endpoint", Jason.encode!(data)) do
      {:ok, %{status_code: 200, body: body}} -> {:ok, Jason.decode!(body)}
      {:ok, %{status_code: 503}} -> {:retry, :service_unavailable}
      {:ok, %{status_code: 504}} -> {:stop, {:error, :not_found}}
      {:error, _reason} -> {:retry, :network_error}
    end
  end

  defp should_retry?({:retry, _reason}), do: true
  defp should_retry?(_), do: false
end
```

---

## Bulkhead Patterns

### 1. Task Pool Limitation

```elixir
defmodule MyApp.Bulkhead do
  use GenServer
  require Logger

  @default_pool_size 10
  @default_queue_size 100

  # Client API
  def start_link(opts), do: GenServer.start_link(__MODULE__, opts, name: Keyword.get(opts, :name, __MODULE__))
  def submit_task(task_name, fun), do: GenServer.cast(__MODULE__, {:submit_task, task_name, fun})

  # Server Callbacks
  @impl true
  def init(opts) do
    pool_size = Keyword.get(opts, :pool_size, @default_pool_size)
    queue_size = Keyword.get(opts, :queue_size, @default_queue_size)
    Logger.info("Starting bulkhead with pool_size: #{pool_size}, queue_size: #{queue_size}")
    
    # Start task pool
    {:ok, task_supervisor} = Task.Supervisor.start_link(__MODULE__, [], name: :task_supervisor)
    
    {:ok, %{
      task_supervisor: task_supervisor,
      pool_size: pool_size,
      queue_size: queue_size,
      active_tasks: 0,
      queue: :queue.new()
    }}
  end

  @impl true
  def handle_cast({:submit_task, task_name, fun}, state) do
    if :queue.len(state.queue) >= state.queue_size do
      Logger.warning("Queue full, rejecting task #{task_name}")
      {:noreply, state}
    else
      # Queue task
      new_queue = :queue.in({task_name, fun}, state.queue)
      new_state = %{state | queue: new_queue}
      
      # Try to process
      {:noreply, process_queue(new_state)}
    end
  end

  @impl true
  def handle_info({:DOWN, _ref, :process, _pid, reason}, state) do
    Logger.info("Task completed, reason: #{inspect(reason)}")
    new_state = %{state | active_tasks: state.active_tasks - 1}
    
    # Process next task from queue
    {:noreply, process_queue(new_state)}
  end

  defp process_queue(state) do
    cond do
      # Queue empty or at pool limit: do nothing
      :queue.is_empty(state.queue) or state.active_tasks >= state.pool_size ->
        state
      
      # Process next task
      true ->
        case :queue.out(state.queue) do
          {{:value, {task_name, fun}}, new_queue} ->
            # Start task
            Task.Supervisor.start_child(state.task_supervisor, Task, fn ->
              Logger.info("Starting task: #{task_name}")
              fun.()
            end)
            
            new_state = %{state |
              queue: new_queue,
              active_tasks: state.active_tasks + 1
            }
            
          {:empty, _} ->
            state
        end
    end
  end
end
```

---

## Timeout Handling

### 1. GenServer with Timeout

```elixir
defmodule MyApp.TimeoutHandler do
  use GenServer
  require Logger

  @default_timeout 5_000

  # Client API
  def start_link(opts), do: GenServer.start_link(__MODULE__, opts, name: Keyword.get(opts, :name, __MODULE__))
  def process_data(data, timeout \\ @default_timeout), do
    GenServer.call(__MODULE__, {:process, data}, timeout)
  end

  # Server Callbacks
  @impl true
  def init(opts), do: {:ok, opts}

  @impl true
  def handle_call({:process, data}, from, state) do
    Logger.info("Processing data")
    
    # Process data with timeout
    Task.start(fn ->
      result = do_long_operation(data)
      GenServer.reply(from, {:ok, result})
    end)
    
    # Don't reply here - task will reply
    {:noreply, state}
  end

  @impl true
  def handle_info({:DOWN, _ref, :process, _pid, reason}, state) do
    Logger.error("Task crashed: #{inspect(reason)}")
    {:noreply, state}
  end

  defp do_long_operation(data) do
    # Simulate long operation
    :timer.sleep(2_000)
    {:processed, data}
  end
end
```

---

## Graceful Degradation

### 1. Feature Flags

```elixir
defmodule MyApp.FeatureFlags do
  use GenServer
  require Logger

  # Client API
  def start_link(opts), do: GenServer.start_link(__MODULE__, opts, name: Keyword.get(opts, :name, __MODULE__))
  def is_enabled?(feature_name), do: GenServer.call(__MODULE__, {:is_enabled, feature_name})
  def enable(feature_name), do: GenServer.cast(__MODULE__, {:enable, feature_name})
  def disable(feature_name), do: GenServer.cast(__MODULE__, {:disable, feature_name})

  # Server Callbacks
  @impl true
  def init(opts) do
    Logger.info("Starting feature flags")
    features = Application.get_env(:my_app, :features, %{})
    {:ok, features}
  end

  @impl true
  def handle_call({:is_enabled, feature_name}, _from, state) do
    enabled = Map.get(state, feature_name, false)
    Logger.info("Feature #{feature_name} enabled: #{enabled}")
    {:reply, enabled, state}
  end

  @impl true
  def handle_cast({:enable, feature_name}, state) do
    Logger.info("Enabling feature: #{feature_name}")
    {:noreply, Map.put(state, feature_name, true)}
  end

  @impl true
  def handle_cast({:disable, feature_name}, state) do
    Logger.warning("Disabling feature: #{feature_name}")
    {:noreply, Map.put(state, feature_name, false)}
  end
end

# Use in application
defmodule MyApp.UserController do
  alias MyApp.FeatureFlags

  def index(conn, _params) do
    # Check if advanced search is enabled
    if FeatureFlags.is_enabled?(:advanced_search) do
      render_advanced_search(conn)
    else
      render_basic_search(conn)
    end
  end
end
```

---

## Best Practices

### DO

✅ **Start with circuit breaker**: Protect against cascading failures
✅ **Use exponential backoff**: Avoid overwhelming failing services
✅ **Add jitter to retries**: Prevent thundering herd
✅ **Implement timeouts**: Prevent hanging requests
✅ **Use bulkheads**: Limit concurrent operations
✅ **Graceful degradation**: Provide fallback behavior
✅ **Log failures**: Track failure patterns
✅ **Monitor circuit states**: Alert when circuits open
✅ **Test failure scenarios**: Chaos engineering
✅ **Configure thresholds**: Adjust based on service reliability

### DON'T

❌ **Infinite retries**: Always limit retry attempts
❌ **Ignore timeout errors**: Handle timeout explicitly
❌ **Retry on client errors**: Only retry transient failures
❌ **Hardcode delays**: Use configurable timeout/delay values
❌ **Ignore circuit state**: Don't call services when circuit is open
❌ **Forget about monitoring**: Alert on circuit state changes
❌ **Mix concerns**: Keep retry logic separate from business logic
❌ **Forget to back off**: Use exponential backoff with jitter
❌ **Silently swallow errors**: Always log or handle errors

---

## Integration with ai-rules

### Roles to Reference

- **Architect**: Use for fault-tolerant system design
- **Orchestrator**: Implement resilience patterns in features
- **Reviewer**: Verify resilience patterns are properly implemented
- **DevOps Engineer**: Configure timeouts and thresholds
- **QA**: Test failure scenarios (network partitions, service failures)

### Skills to Reference

- **distributed-systems**: Combine with clustering strategies
- **observability**: Monitor circuit states and failure patterns
- **test-generation**: Write tests for failure scenarios

---

## Summary

Resilience patterns provide:
- ✅ Circuit breaker for failure isolation
- ✅ Exponential backoff for retry strategies
- ✅ Timeout handling to prevent hanging
- ✅ Bulkheads to limit resource usage
- ✅ Graceful degradation for partial failures
- ✅ Feature flags for controlled rollout

**Key**: Design for failure, protect against cascading failures, and monitor resilience patterns.
