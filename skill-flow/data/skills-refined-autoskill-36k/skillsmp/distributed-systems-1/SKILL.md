---
name: distributed-systems
description: Distributed systems patterns for BEAM/OTP including clustering, supervision, and multi-region deployment
---

# Distributed Systems Skill

Use this skill when:
- Creating distributed Elixir applications
- Designing node clustering strategies
- Implementing cross-node supervision
- Building multi-region deployments
- Handling network partitions
- Designing fault-tolerant systems

## When to Use

### Use this skill when:
- Your application needs to run on multiple nodes
- You need global process coordination
- You're building real-time collaborative features
- You need high availability and fault tolerance
- You're implementing distributed data storage (Mnesia, Redis)

### Key Scenarios

1. **Clustering**: Multiple Elixir nodes working together
2. **Global State**: Coordinating state across nodes
3. **Fault Tolerance**: System continues despite node failures
4. **Multi-Region**: Deployment across geographic regions
5. **Real-time**: Real-time collaborative features (Presence, PubSub)

---

## Node Clustering

### Erlang Distribution

```elixir
# Start node with name
iex --name app1@127.0.0.1 -S mix

# Start node with cookie
iex --name app1@127.0.0.1 --cookie secret_cookie -S mix

# Connect to another node
Node.connect(:app2@127.0.0.1)

# List connected nodes
Node.list()
```

### Libcluster Strategy

```elixir
# config/config.exs
config :libcluster,
  topologies: [
    production: [
      strategy: Cluster.Strategy.Kubernetes.DNS,
      config: [
        service: "my-app",
        application_name: :my_app,
        polling_interval: 10_000
      ]
    ]
  ]

# mix.exs
defp deps do
  [
    {:libcluster, "~> 3.3"}
  ]
end

# application.ex
defmodule MyApp.Application do
  use Application

  def start(_type, _args) do
    children = [
      # Start clustering
      {Cluster.Supervisor, [topologies: Application.get_env(:my_app, :topologies)]}
    ]
    
    opts = [strategy: :one_for_one, name: MyApp.Supervisor]
    Supervisor.start_link(children, opts)
  end
end
```

### DNS Cluster Strategy

```elixir
config :my_app, :topologies,
  production: [
    strategy: Cluster.Strategy.DNSPoll,
    config: [
      query: "my-app-headless.default.svc.cluster.local",
      node_basename: "my_app",
      polling_interval: 5_000,
      ip_lookup_mode: :dns
    ]
  ]
```

---

## Distributed Supervision

### DynamicSupervisor with Global Registry

```elixir
defmodule MyApp.WorkersSupervisor do
  use DynamicSupervisor

  def start_link(opts) do
    opts = Keyword.put_new(opts, :name, __MODULE__)
    DynamicSupervisor.start_link(__MODULE__, opts, opts)
  end

  @impl true
  def init(_opts) do
    DynamicSupervisor.init(strategy: :one_for_one)
  end

  def start_worker(worker_module, worker_id, opts \\ []) do
    spec = {worker_module, Keyword.put(opts, :id, worker_id)}
    DynamicSupervisor.start_child(__MODULE__, spec)
  end

  def stop_worker(worker_id) do
    case Registry.lookup(MyApp.Registry, worker_id) do
      [{pid, _}] ->
        DynamicSupervisor.terminate_child(__MODULE__, pid)
      [] ->
        {:error, :not_found}
    end
  end
end
```

### Global Process Registration

```elixir
# Using :global
:global.register_name(:unique_name, pid)
case :global.whereis_name(:unique_name) do
  pid when is_pid(pid) -> {:ok, pid}
  :undefined -> {:error, :not_registered}
end

# Using Registry (distributed)
defmodule MyApp.Registry do
  use Registry

  def start_link(opts) do
    opts = Keyword.put_new(opts, :keys, :unique)
    opts = Keyword.put_new(opts, :name, __MODULE__)
    Registry.start_link(opts, opts)
  end

  def register_name(name, pid) do
    case Registry.register(__MODULE__, name, pid) do
      {:ok, _pid} -> :ok
      {:error, _reason} -> {:error, :already_registered}
    end
  end

  def lookup_name(name) do
    case Registry.lookup(__MODULE__, name) do
      [{pid, _}] -> {:ok, pid}
      [] -> {:error, :not_found}
    end
  end
end
```

### Distributed GenServer

```elixir
defmodule MyApp.Worker do
  use GenServer
  require Logger

  # Client API
  def start_link(opts), do: GenServer.start_link(__MODULE__, opts, name: {:global, __MODULE__})
  def do_work(data), do: GenServer.call({:global, __MODULE__}, {:do_work, data})

  # Server Callbacks
  @impl true
  def init(opts) do
    Logger.info("Starting distributed worker on node: #{Node.self()}")
    {:ok, opts}
  end

  @impl true
  def handle_call({:do_work, data}, _from, state) do
    Logger.info("Processing work on node: #{Node.self()}")
    # Process work
    result = process_data(data, state)
    {:reply, {:ok, result}, state}
  end

  @impl true
  def handle_info({:EXIT, _pid, reason}, state) do
    Logger.error("Worker exited: #{inspect(reason)}")
    {:noreply, state}
  end

  defp process_data(data, opts) do
    # Business logic
    {:processed, data}
  end
end
```

---

## Cross-Node Communication

### RPC with Node.spawn

```elixir
# Spawn on remote node
result = Node.spawn(:worker@host, fn ->
  MyApp.Worker.do_work(data)
end)

# Call with timeout
result = :rpc.call(:worker@host, MyApp.Worker, :do_work, [data], 5_000)

# Cast (fire and forget)
:rpc.cast(:worker@host, MyApp.Worker, :do_work, [data])
```

### Phoenix.PubSub Distribution

```elixir
# config/config.exs
config :my_app, MyApp.PubSub,
  adapter: Phoenix.PubSub.PG2,
  pool_size: 10

# application.ex
defmodule MyApp.Application do
  use Application

  def start(_type, _args) do
    children = [
      # Start PubSub with distribution
      {Phoenix.PubSub, [name: MyApp.PubSub]},
      # Start distributed processes
      MyApp.WorkersSupervisor
    ]

    opts = [strategy: :one_for_one, name: MyApp.Supervisor]
    Supervisor.start_link(children, opts)
  end
end

# Subscribe to topic
Phoenix.PubSub.subscribe(MyApp.PubSub, "events:topic")

# Publish to topic
Phoenix.PubSub.broadcast(MyApp.PubSub, "events:topic", {:new_event, data})
```

### Distributed GenServer with PubSub

```elixir
defmodule MyApp.DistributedCache do
  use GenServer
  require Logger

  def start_link(opts), do: GenServer.start_link(__MODULE__, opts, name: __MODULE__)

  # Client API
  def get(key), do: GenServer.call(__MODULE__, {:get, key})
  def put(key, value), do: GenServer.cast(__MODULE__, {:put, key, value})
  def subscribe(cache_events), do: Phoenix.PubSub.subscribe(MyApp.PubSub, cache_events)

  # Server Callbacks
  @impl true
  def init(opts) do
    Logger.info("Starting distributed cache on node: #{Node.self()}")
    {:ok, %{cache: %{}, opts: opts}}
  end

  @impl true
  def handle_call({:get, key}, _from, state) do
    result = Map.get(state.cache, key)
    {:reply, result, state}
  end

  @impl true
  def handle_cast({:put, key, value}, state) do
    new_cache = Map.put(state.cache, key, value)
    new_state = %{state | cache: new_cache}
    
    # Notify other nodes
    Phoenix.PubSub.broadcast(MyApp.PubSub, "cache:updates", {:put, key, value})
    
    {:noreply, new_state}
  end

  @impl true
  def handle_info({:put, key, value}, state) do
    # Handle updates from other nodes
    new_cache = Map.put(state.cache, key, value)
    new_state = %{state | cache: new_cache}
    {:noreply, new_state}
  end
end
```

---

## Network Partition Handling

### Detecting Network Partitions

```elixir
defmodule MyApp.NodeMonitor do
  use GenServer
  require Logger

  def start_link(opts), do: GenServer.start_link(__MODULE__, opts, name: __MODULE__)

  @impl true
  def init(opts) do
    # Monitor node connections
    :net_kernel.monitor_nodes(true)
    {:ok, %{connected_nodes: Node.list()}}
  end

  @impl true
  def handle_info({:nodeup, node}, state) do
    Logger.info("Node joined: #{node}")
    new_state = %{state | connected_nodes: [node | state.connected_nodes]}
    {:noreply, new_state}
  end

  @impl true
  def handle_info({:nodedown, node}, state) do
    Logger.warning("Node left: #{node}")
    new_state = %{state | connected_nodes: List.delete(state.connected_nodes, node)}
    {:noreply, handle_node_down(node, state)}
  end

  defp handle_node_down(node, state) do
    # Handle graceful degradation
    MyApp.DistributedCache.rebalance(state.connected_nodes)
    MyApp.WorkerSupervisor.restart_workers_on_new_node()
    state
  end
end
```

### Quorum-Based Decisions

```elixir
defmodule MyApp.Quorum do
  require Logger

  def quorum_count(total_nodes \\ nil) do
    total_nodes = total_nodes || length(Node.list()) + 1
    div(total_nodes, 2) + 1
  end

  def achieve_quorum?(votes) when length(votes) >= quorum_count(), do: true
  def achieve_quorum?(_votes), do: false

  def make_decision(nodes, decision_fn) do
    votes = Enum.map(nodes, fn node ->
      :rpc.call(node, decision_fn, [], 5_000)
    end)
    
    if achieve_quorum?(votes) do
      {:ok, majority_vote(votes)}
    else
      {:error, :quorum_not_achieved}
    end
  end

  defp majority_vote(votes) do
    Enum.frequencies(votes)
    |> Enum.max_by(fn {_result, count} -> count end)
    |> elem(0)
  end
end
```

### Conflict Resolution (Last Write Wins)

```elixir
defmodule MyApp.ConflictResolver do
  def resolve_conflict(old_value, new_value, timestamp) do
    cond do
      is_nil(old_value) -> new_value
      is_nil(new_value) -> old_value
      true ->
        # Use timestamps for last-write-wins
        if old_value.updated_at > new_value.updated_at do
          old_value
        else
          new_value
        end
    end
  end

  def resolve_conflict_vector_clock(old_vc, new_vc, old_data, new_data) do
    # Implement vector clocks for conflict resolution
    case compare_vector_clocks(old_vc, new_vc) do
      :lt -> new_data  # Old is less than new
      :gt -> old_data  # Old is greater than new
      :concurrent -> merge_data(old_data, new_data)
    end
  end

  defp compare_vector_clocks(vc1, vc2) do
    # Simplified vector clock comparison
    cond do
      all_clocks_greater?(vc1, vc2) -> :gt
      all_clocks_greater?(vc2, vc1) -> :lt
      true -> :concurrent
    end
  end

  defp all_clocks_greater?(vc1, vc2) do
    Enum.all?(vc1, fn {node, clock} ->
      Map.get(vc2, node, 0) < clock
    end)
  end

  defp merge_data(data1, data2) do
    # Implement data merging logic
    Map.merge(data1, data2, fn _k, v1, v2 -> merge_values(v1, v2) end)
  end

  defp merge_values(v1, v2) when is_map(v1) and is_map(v2) do
    Map.merge(v1, v2, fn _k, v1_val, v2_val -> merge_values(v1_val, v2_val) end)
  end

  defp merge_values(_v1, v2), do: v2
end
```

---

## Multi-Region Deployment

### Regional Clusters

```elixir
# config/config.exs
config :my_app, :clusters,
  us_east: [
    strategy: Cluster.Strategy.Kubernetes.DNS,
    config: [
      service: "my-app-us-east",
      polling_interval: 10_000
    ]
  ],
  us_west: [
    strategy: Cluster.Strategy.Kubernetes.DNS,
    config: [
      service: "my-app-us-west",
      polling_interval: 10_000
    ]
  ]
```

### Data Replication

```elixir
defmodule MyApp.Replication do
  use GenServer
  require Logger

  def start_link(opts), do: GenServer.start_link(__MODULE__, opts, name: __MODULE__)

  @impl true
  def init(opts) do
    # Subscribe to local data changes
    Phoenix.PubSub.subscribe(MyApp.PubSub, "data:changes")
    {:ok, opts}
  end

  @impl true
  def handle_info({:data_change, key, value}, state) do
    # Replicate to remote regions
    replicate_to_regions(key, value, state.regions)
    {:noreply, state}
  end

  defp replicate_to_regions(key, value, regions) do
    Enum.each(regions, fn region ->
      replicate_to_region(key, value, region)
    end)
  end

  defp replicate_to_region(key, value, region) do
    # Send to regional leader
    region_node = :"my_app-#{region}@#{region}.internal"
    
    case Node.connect(region_node) do
      true ->
        GenServer.call({:global, region_node}, {:replicate, key, value}, 5_000)
      false ->
        Logger.warning("Failed to connect to region: #{region}")
    end
  end
end
```

---

## Best Practices

### DO

✅ **Start with single node**: Test locally before clustering
✅ **Use libcluster**: Let libcluster manage node discovery
✅ **Monitor nodes**: Track node up/down events
✅ **Handle network partitions**: Design for partial connectivity
✅ **Use global names**: :global or Registry with unique keys
✅ **Implement graceful degradation**: System continues with reduced functionality
✅ **Use quorum**: Require majority for critical operations
✅ **Implement conflict resolution**: Use timestamps, vector clocks, or CRDTs
✅ **Test partition scenarios**: Chaos testing with failure injection
✅ **Monitor performance**: Track latency and throughput across regions

### DON'T

❌ **Assume all nodes are equal**: Some nodes may be slower or unreliable
❌ **Ignore network partitions**: System must continue despite partial connectivity
❌ **Make blocking RPC calls**: Use timeouts and handle failures
❌ **Create single points of failure**: Distribute critical processes
❌ **Ignore latency**: Multi-region deployment has network overhead
❌ **Forget about clock skew**: Different clocks need synchronization
❌ **Overuse :global**: It's a bottleneck for global processes
❌ **Skip testing**: Test distributed scenarios (network partitions, node failures)
❌ **Hardcode node names**: Use service discovery (DNS, Kubernetes)

---

## Integration with ai-rules

### Roles to Reference

- **Architect**: Use for distributed system design
- **DevOps Engineer**: Use for deployment and configuration
- **QA**: Test distributed scenarios (network partitions, node failures)
- **Security Architect**: Implement secure inter-node communication

### Skills to Reference

- **otp-patterns**: GenServer and Supervisor patterns
- **observability**: Monitor node health and performance
- **test-generation**: Write tests for distributed scenarios

### Documentation Links

- **Clustering**: `patterns/clustering_strategies.md` (to create)
- **Distributed Supervision**: `patterns/distributed_supervision.md` (to create)
- **Mnesia Patterns**: `patterns/mnesia_patterns.md` (to create)

---

## Summary

Distributed systems on BEAM/OTP provide:
- ✅ Built-in distribution via Erlang VM
- ✅ Fault tolerance through supervision trees
- ✅ Global process coordination
- ✅ Multi-region deployment support
- ✅ Real-time collaborative features
- ✅ Network partition handling
- ✅ Conflict resolution strategies

**Key**: Design for partial connectivity, use quorum for consensus, and test distributed scenarios.
