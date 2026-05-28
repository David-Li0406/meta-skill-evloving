---
name: distributed-systems
description: Use when working with distributed systems, clustering, consensus algorithms, network partitions, CAP tradeoffs, or distributed Erlang/Elixir patterns
---

# Distributed Systems Patterns

## Overview

Building distributed systems in Elixir/Erlang provides powerful capabilities but introduces unique challenges: consensus, network partitions, clock synchronization, and split-brain scenarios. This skill covers production-tested patterns for distributed systems design, consensus algorithms, clustering strategies, and debugging distributed bugs.

## When to Use

Use this skill when:
- Designing distributed system architectures
- Evaluating consensus algorithms (Paxos, Raft, Multi-Raft)
- Planning clustering strategies (Distributed Erlang, Partisan)
- Debugging distributed system issues
- Analyzing CAP theorem tradeoffs
- Handling network partitions
- Implementing conflict resolution (CRDTs, vector clocks)
- Building globally distributed applications
- Working with distributed state or caching

## Core Concepts

### CAP Theorem Tradeoffs

**Consistency + Availability + Partition Tolerance** - Pick 2:

**CA (Consistency + Availability, no Partition Tolerance)**:
- Traditional RDBMS in single datacenter
- Example: PostgreSQL without replication
- Limitation: Network partition breaks system
- Use case: Single-datacenter applications

**CP (Consistency + Partition Tolerance)**:
- Prioritize correctness over availability
- Examples: Raft consensus (ra, raft libraries), etcd, ZooKeeper
- During partition: Minority partition becomes unavailable
- Use case: Financial systems, inventory management, leader election

**AP (Availability + Partition Tolerance)**:
- Prioritize availability over strong consistency
- Examples: CRDTs (lasp, delta_crdt), Cassandra, DynamoDB
- During partition: All nodes serve requests, reconcile later
- Use case: Social media, content delivery, collaborative editing

**Elixir-specific considerations**:
```elixir
# CP approach: Raft consensus via :ra
{:ok, _cluster} = :ra.start_cluster(
  :my_cluster,
  {:module, MyStateMachine, %{}},
  [node() | Node.list()]
)

# AP approach: CRDTs via delta_crdt
{:ok, crdt_pid} = DeltaCrdt.start_link(DeltaCrdt.AWLWWMap)
```

### Distributed Erlang Architecture

**Capabilities**:
- Transparent remote process communication
- Location transparency (`send/2` works across nodes)
- Distributed process registry
- Global name registration (`:global` module)
- Automatic network failure detection

**Limitations**:
- **Full-mesh topology**: Every node connects to every other node
- **O(n²) network overhead**: Breaks down at ~50-100 nodes
- **All-or-nothing security**: Either fully trusted or isolated
- **Global namespace conflicts**: Name collisions across nodes
- **Netsplits**: Network partitions create split-brain scenarios

**When Distributed Erlang is good enough**:
```elixir
# Small to medium clusters (< 50 nodes)
# Trusted network environment
# Simple clustering needs

# Setup with libcluster
config :libcluster,
  topologies: [
    k8s: [
      strategy: Cluster.Strategy.Kubernetes,
      config: [
        mode: :dns,
        kubernetes_node_basename: "myapp",
        kubernetes_selector: "app=myapp",
        polling_interval: 10_000
      ]
    ]
  ]
```

### Partisan: Large-Scale Clustering

**Why Partisan?**:
- Overlay network topology (not full-mesh)
- Support for 100s-1000s of nodes
- Configurable topologies (client-server, HyParView)
- Partial connectivity between nodes
- Better network efficiency

**Architecture**:
```elixir
# Partisan configuration
config :partisan,
  peer_service: Partisan.PeerService.HyParView,
  active_max_size: 6,
  passive_max_size: 30

# Partisan membership
Partisan.PeerService.join(:"node@other_host")

# Partisan messaging
Partisan.forward_message(node, pid, message)
```

**Use Partisan when**:
- Cluster size > 50 nodes
- Need custom network topology
- Building multi-datacenter systems
- Require gossip protocols
- Implementing peer-to-peer systems

### Consensus Algorithms

#### Paxos

**Properties**:
- Classic consensus algorithm (Leslie Lamport, 1989)
- Provably correct
- Notoriously difficult to understand and implement
- Requires majority quorum (⌊n/2⌋ + 1)

**Phases**:
1. Prepare: Proposer sends proposal number
2. Promise: Acceptors promise not to accept lower proposals
3. Accept: Proposer sends value
4. Accepted: Acceptors record accepted value

**In Elixir**:
- Rarely implemented directly (complexity)
- Use Raft instead for most use cases

#### Raft

**Properties**:
- Designed for understandability (Diego Ongaro, 2014)
- Leader-based consensus
- Log replication
- Strong consistency guarantees
- Requires majority quorum

**Key components**:
```elixir
# Using :ra (RabbitMQ's Raft implementation)
defmodule MyStateMachine do
  @behaviour :ra_machine

  def init(_config), do: %{}

  def apply(_meta, {:set, key, value}, state) do
    {state, Map.put(state, key, value), :ok}
  end

  def apply(_meta, {:get, key}, state) do
    {state, Map.get(state, key), {:ok, Map.get(state, key)}}
  end
end

# Start Raft cluster
:ra.start_cluster(
  :my_cluster,
  {:module, MyStateMachine, %{}},
  [
    {:"node1@host", :ra_node_id},
    {:"node2@host", :ra_node_id},
    {:"node3@host", :ra_node_id}
  ]
)

# Submit command
:ra.process_command({:my_cluster, node()}, {:set, :key, :value})
```

**When to use Raft**:
- Need strong consistency (CP)
- Leader election
- Replicated state machines
- Configuration management
- Distributed locks

**Libraries**:
- `:ra` - Production-grade (RabbitMQ)
- `raft` - Pure Elixir implementation

#### Multi-Raft with Leader Leases

**Advanced pattern** used by CockroachDB, TiKV:

**Key optimizations**:
- Multiple Raft groups for sharding
- Leader leases reduce read latency
- Lease-based reads (no quorum check)
- Clock-bound wait (Google Spanner style)

**Concept**:
```elixir
# Multiple Raft groups (sharding)
# Group 1: Handles keys "a-m"
# Group 2: Handles keys "n-z"

# Leader lease optimization
defmodule RaftLeader do
  # Leader holds lease for 10 seconds
  @lease_duration 10_000

  def read_with_lease(state) do
    if lease_valid?(state.lease) do
      # Fast read: No quorum needed
      {:ok, state.data}
    else
      # Fallback: Quorum read
      quorum_read(state)
    end
  end

  defp lease_valid?(lease) do
    System.monotonic_time(:millisecond) < lease.expiry
  end
end
```

**Benefits**:
- 10x faster reads (no quorum)
- Better scalability (sharding)
- Maintains strong consistency

**Tradeoffs**:
- Clock drift sensitivity
- Increased complexity
- Lease management overhead

### Conflict-Free Replicated Data Types (CRDTs)

**For AP systems** - Automatic conflict resolution:

**Key CRDT types**:
```elixir
# G-Counter: Grow-only counter
{:ok, counter} = DeltaCrdt.start_link(DeltaCrdt.GCounter)
DeltaCrdt.mutate(counter, :increment)

# PN-Counter: Increment/decrement counter
{:ok, counter} = DeltaCrdt.start_link(DeltaCrdt.PNCounter)
DeltaCrdt.mutate(counter, :increment)
DeltaCrdt.mutate(counter, :decrement)

# AWLWWMap: Add-wins, Last-write-wins map
{:ok, map} = DeltaCrdt.start_link(DeltaCrdt.AWLWWMap)
DeltaCrdt.mutate(map, :add, ["key", "value"])
DeltaCrdt.mutate(map, :remove, ["key"])

# OR-Set: Observed-remove set
{:ok, set} = DeltaCrdt.start_link(DeltaCrdt.ORSet)
DeltaCrdt.mutate(set, :add, ["element"])
DeltaCrdt.mutate(set, :remove, ["element"])
```

**When to use CRDTs**:
- Eventually consistent systems (AP)
- Offline-first applications
- Collaborative editing
- Shopping carts
- Presence tracking
- Like/favorite counts

**Libraries**:
- `delta_crdt` - Production-ready
- `lasp` - Research-grade, advanced

### Vector Clocks

**For causal consistency** - Track causality between events:

```elixir
defmodule VectorClock do
  def new, do: %{}

  def increment(clock, node) do
    Map.update(clock, node, 1, &(&1 + 1))
  end

  def merge(clock1, clock2) do
    Map.merge(clock1, clock2, fn _k, v1, v2 -> max(v1, v2) end)
  end

  # Returns :concurrent, :before, or :after
  def compare(clock1, clock2) do
    cond do
      descends?(clock1, clock2) -> :after
      descends?(clock2, clock1) -> :before
      true -> :concurrent
    end
  end

  defp descends?(clock1, clock2) do
    Enum.all?(clock2, fn {node, count} ->
      Map.get(clock1, node, 0) >= count
    end) and clock1 != clock2
  end
end

# Usage in distributed system
defmodule DistributedCache do
  def put(key, value, clock) do
    new_clock = VectorClock.increment(clock, node())
    # Store {value, new_clock}
    {:ok, new_clock}
  end

  def resolve_conflict(values_with_clocks) do
    # Keep all concurrent values, discard causally dominated
    Enum.reject(values_with_clocks, fn {_v1, c1} ->
      Enum.any?(values_with_clocks, fn {_v2, c2} ->
        VectorClock.compare(c1, c2) == :before
      end)
    end)
  end
end
```

## Common Distributed Bugs

### Split-Brain Scenario

**Problem**: Network partition creates multiple leaders

**Example**:
```elixir
# Before partition: Single leader
# [Node1 (Leader)] <-> [Node2] <-> [Node3]

# After partition: TWO leaders!
# [Node1 (Leader)] <-> [Node2]  |  [Node3 (Leader)]
```

**Prevention strategies**:

**1. Quorum-based consensus (CP approach)**:
```elixir
# Raft: Requires majority
# 5 nodes: Need 3 for quorum
# After split: 3-node partition has leader, 2-node cannot elect

defmodule QuorumCheck do
  def has_quorum?(cluster_size, reachable_nodes) do
    reachable_nodes >= div(cluster_size, 2) + 1
  end
end
```

**2. Fencing tokens**:
```elixir
defmodule LeaderFence do
  # Each leader gets monotonically increasing token
  def write_with_fence(resource, data, fence_token) do
    case Storage.conditional_write(resource, data, fence_token) do
      :ok -> :ok
      {:error, :stale_token} -> {:error, :not_leader}
    end
  end
end

# Storage layer rejects writes with old tokens
```

**3. External coordinator** (etcd, ZooKeeper, Consul):
```elixir
# Leader lease in etcd
defmodule LeaderElection do
  def acquire_leadership(node_id) do
    case Etcd.acquire_lease(node_id, ttl: 10) do
      {:ok, lease_id} ->
        # Periodically renew lease
        Process.send_after(self(), :renew_lease, 5_000)
        {:ok, lease_id}
      {:error, :already_held} ->
        {:error, :not_leader}
    end
  end
end
```

**Detection**:
```elixir
# Monitor for split-brain
defmodule SplitBrainDetector do
  def check_cluster_health do
    visible_nodes = [node() | Node.list()]
    expected_nodes = Application.get_env(:app, :cluster_nodes)

    if length(visible_nodes) < length(expected_nodes) / 2 do
      Logger.error("Possible split-brain: #{inspect(visible_nodes)}")
      trigger_alarm(:split_brain)
    end
  end
end
```

### Clock Drift Issues

**Problem**: Distributed clocks drift apart

**Impact**:
- Incorrect event ordering
- Lease expiry bugs
- Timestamp-based logic fails
- Data inconsistency

**Mitigation**:

**1. Use monotonic time for intervals**:
```elixir
# ❌ Wrong: System time changes (NTP adjustments)
start_time = System.system_time(:millisecond)
# ... work ...
elapsed = System.system_time(:millisecond) - start_time

# ✅ Correct: Monotonic time never goes backwards
start_time = System.monotonic_time(:millisecond)
# ... work ...
elapsed = System.monotonic_time(:millisecond) - start_time
```

**2. Hybrid Logical Clocks (HLC)**:
```elixir
defmodule HLC do
  # Combines physical time + logical counter
  defstruct [:physical_time, :logical_counter, :node_id]

  def new(node_id) do
    %HLC{
      physical_time: System.system_time(:millisecond),
      logical_counter: 0,
      node_id: node_id
    }
  end

  def send_event(clock) do
    physical = System.system_time(:millisecond)

    if physical > clock.physical_time do
      %{clock | physical_time: physical, logical_counter: 0}
    else
      %{clock | logical_counter: clock.logical_counter + 1}
    end
  end

  def receive_event(clock, remote_clock) do
    physical = System.system_time(:millisecond)
    max_physical = max(physical, max(clock.physical_time, remote_clock.physical_time))

    logical =
      if max_physical == clock.physical_time and max_physical == remote_clock.physical_time do
        max(clock.logical_counter, remote_clock.logical_counter) + 1
      else
        0
      end

    %{clock | physical_time: max_physical, logical_counter: logical}
  end
end
```

**3. NTP monitoring**:
```elixir
# Check clock skew
defmodule ClockMonitor do
  def check_ntp_offset do
    case System.cmd("ntpq", ["-c", "rv"]) do
      {output, 0} ->
        offset = parse_offset(output)
        if abs(offset) > 100 do # 100ms threshold
          Logger.error("Clock offset too high: #{offset}ms")
          trigger_alarm(:clock_skew)
        end
      _ ->
        Logger.error("Cannot check NTP")
    end
  end
end
```

### Quorum Calculation Errors

**Problem**: Incorrect quorum math

**Examples**:
```elixir
# ❌ Wrong: Even split isn't majority
quorum = div(cluster_size, 2)  # 5 nodes -> 2 (not majority!)

# ✅ Correct: Need more than half
quorum = div(cluster_size, 2) + 1  # 5 nodes -> 3

# Handle edge cases
defmodule Quorum do
  def required_nodes(cluster_size) when cluster_size > 0 do
    div(cluster_size, 2) + 1
  end

  def has_quorum?(cluster_size, available_nodes) do
    available_nodes >= required_nodes(cluster_size)
  end

  # Account for node failures
  def max_failures(cluster_size) do
    div(cluster_size - 1, 2)
  end
end

# Examples:
# 1 node: quorum=1, max_failures=0
# 3 nodes: quorum=2, max_failures=1
# 5 nodes: quorum=3, max_failures=2
# 7 nodes: quorum=4, max_failures=3
```

**Dynamic membership** adds complexity:
```elixir
# Reconfiguration must go through consensus
defmodule RaftReconfiguration do
  def add_node(cluster, new_node) do
    # Use joint consensus (C_old + C_new)
    :ra.add_member(cluster, new_node)
  end

  def remove_node(cluster, old_node) do
    :ra.remove_member(cluster, old_node)
  end
end
```

### Network Partition Handling

**Strategies**:

**1. Last-Write-Wins (LWW)**:
```elixir
# Simple but loses data
defmodule LWW do
  def resolve({value1, timestamp1}, {value2, timestamp2}) do
    if timestamp1 > timestamp2, do: value1, else: value2
  end
end
```

**2. Application-specific merge**:
```elixir
defmodule ShoppingCart do
  # Merge carts from both sides of partition
  def merge(cart1, cart2) do
    items1 = MapSet.new(cart1.items, fn item -> {item.product_id, item} end)
    items2 = MapSet.new(cart2.items, fn item -> {item.product_id, item} end)

    merged_items =
      MapSet.union(items1, items2)
      |> Enum.map(fn {_id, item} -> item end)

    %{cart1 | items: merged_items}
  end
end
```

**3. Read-repair**:
```elixir
defmodule ReadRepair do
  def get(key) do
    # Read from multiple nodes
    results = Enum.map(nodes(), fn node ->
      :rpc.call(node, Storage, :get, [key])
    end)

    # Find latest version
    {latest_value, latest_version} = find_latest(results)

    # Repair stale replicas
    Enum.each(results, fn {node, value, version} ->
      if version < latest_version do
        :rpc.cast(node, Storage, :put, [key, latest_value, latest_version])
      end
    end)

    latest_value
  end
end
```

### Race Conditions in Distributed State

**Problem**: Concurrent updates from different nodes

**Example**:
```elixir
# Two nodes decrement counter simultaneously
# Node1: read=10, write=9
# Node2: read=10, write=9
# Expected: 8, Actual: 9 (lost update!)
```

**Solution 1: Optimistic locking**:
```elixir
defmodule OptimisticLock do
  def update(key, update_fn) do
    case Storage.get_with_version(key) do
      {:ok, value, version} ->
        new_value = update_fn.(value)
        case Storage.put_if_version(key, new_value, version) do
          :ok -> {:ok, new_value}
          {:error, :version_mismatch} ->
            # Retry
            update(key, update_fn)
        end
      {:error, :not_found} ->
        {:error, :not_found}
    end
  end
end
```

**Solution 2: CRDTs**:
```elixir
# PN-Counter handles concurrent decrements correctly
{:ok, counter} = DeltaCrdt.start_link(DeltaCrdt.PNCounter)

# Node1 and Node2 can both decrement
DeltaCrdt.mutate(counter, :decrement)

# CRDTs merge automatically
```

**Solution 3: Serialization via consensus**:
```elixir
# All updates go through Raft leader
:ra.process_command({:my_cluster, node()}, {:decrement, :counter})
```

## Clustering Strategies

### libcluster Integration

**Kubernetes DNS**:
```elixir
config :libcluster,
  topologies: [
    k8s: [
      strategy: Cluster.Strategy.Kubernetes,
      config: [
        mode: :dns,
        kubernetes_node_basename: "myapp",
        kubernetes_selector: "app=myapp",
        polling_interval: 10_000
      ]
    ]
  ]
```

**Consul**:
```elixir
config :libcluster,
  topologies: [
    consul: [
      strategy: Cluster.Strategy.Consul,
      config: [
        host: "consul.service.consul",
        port: 8500,
        service_name: "myapp",
        polling_interval: 10_000
      ]
    ]
  ]
```

**Gossip (UDP multicast)**:
```elixir
config :libcluster,
  topologies: [
    gossip: [
      strategy: Cluster.Strategy.Gossip,
      config: [
        port: 45892,
        multicast_addr: "230.1.1.251",
        multicast_ttl: 1
      ]
    ]
  ]
```

### Phoenix.PubSub for Distributed State

**Cluster-wide broadcasts**:
```elixir
# Broadcast to all nodes
Phoenix.PubSub.broadcast(
  MyApp.PubSub,
  "cache:invalidate",
  {:invalidate, key}
)

# Subscribe on all nodes
Phoenix.PubSub.subscribe(MyApp.PubSub, "cache:invalidate")

# Handle invalidation
def handle_info({:invalidate, key}, state) do
  LocalCache.delete(key)
  {:noreply, state}
end
```

**Distributed process registry**:
```elixir
# Use Phoenix.Tracker for distributed presence
defmodule MyApp.Presence do
  use Phoenix.Presence,
    otp_app: :my_app,
    pubsub_server: MyApp.PubSub
end

# Track user across cluster
MyApp.Presence.track(
  self(),
  "users:lobby",
  user.id,
  %{name: user.name, joined_at: System.system_time(:second)}
)

# List all users (all nodes)
MyApp.Presence.list("users:lobby")
```

## Distributed Debugging Patterns

### Distributed Tracing

```elixir
# Using :telemetry for distributed traces
:telemetry.span(
  [:myapp, :distributed_call],
  %{node: target_node, operation: :fetch_data},
  fn ->
    result = :rpc.call(target_node, Module, :function, [args])
    {result, %{status: :ok}}
  end
)

# Correlate across nodes with trace_id
def distributed_operation(trace_id) do
  Logger.metadata(trace_id: trace_id)

  :rpc.call(other_node, RemoteModule, :operation, [trace_id])
end
```

### Distributed Observer

```elixir
# Connect to production cluster
Node.connect(:"prod@node1.example.com")

# Start observer on remote node
:observer.start()

# Or use :rpc for information
:rpc.call(remote_node, :erlang, :memory, [])
:rpc.call(remote_node, :erlang, :system_info, [:process_count])
```

### Investigating Netsplits

```elixir
defmodule NetsplitDebug do
  # Detect and log partition events
  def monitor_cluster do
    :net_kernel.monitor_nodes(true, [:nodedown_reason])
  end

  def handle_info({:nodedown, node, reason}, state) do
    Logger.error("Node down: #{node}, reason: #{inspect(reason)}")
    log_cluster_state()
    {:noreply, state}
  end

  def log_cluster_state do
    Logger.info("""
    Cluster state:
    - Current node: #{node()}
    - Visible nodes: #{inspect(Node.list())}
    - Hidden nodes: #{inspect(Node.list(:hidden))}
    - Connected: #{inspect(Node.list(:connected))}
    """)
  end
end
```

## Quick Reference

| Problem | Pattern | Tool/Library |
|---------|---------|--------------|
| Large clusters (>50 nodes) | Partisan overlay network | partisan |
| Strong consistency | Raft consensus | :ra, raft |
| Eventual consistency | CRDTs | delta_crdt, lasp |
| Leader election | Consensus or external coordinator | :ra, etcd |
| Service discovery | DNS, Consul, K8s | libcluster |
| Distributed state sync | PubSub | Phoenix.PubSub |
| Presence tracking | CRDT-based tracker | Phoenix.Tracker |
| Clock synchronization | Hybrid Logical Clocks | manual implementation |
| Split-brain prevention | Quorum + fencing | :ra, external coordinator |
| Causal ordering | Vector clocks | manual implementation |

## Production Checklist

Before deploying distributed system:

- [ ] **Consensus**: Choose CP (Raft) or AP (CRDT) based on requirements
- [ ] **Quorum**: Verify correct quorum calculation (`div(n, 2) + 1`)
- [ ] **Split-brain**: Implement detection and prevention
- [ ] **Clock drift**: Use monotonic time for intervals, NTP monitoring
- [ ] **Network partitions**: Define merge/resolution strategy
- [ ] **Cluster size**: Use Partisan if >50 nodes
- [ ] **Service discovery**: Configure libcluster for environment
- [ ] **Monitoring**: Set up distributed tracing (telemetry, OpenTelemetry)
- [ ] **Failure modes**: Test with Chaos Monkey, network partition simulation
- [ ] **Observability**: Distributed metrics, logging with trace_id

## When to Use Which Approach

### Use Raft (CP) when:
- Financial transactions
- Inventory management
- Configuration management
- Leader election
- Strong consistency required
- Can tolerate reduced availability during partitions

### Use CRDTs (AP) when:
- Social features (likes, follows)
- Collaborative editing
- Shopping carts
- Presence/status
- Offline-first apps
- Availability more important than consistency

### Use Distributed Erlang when:
- Small to medium cluster (<50 nodes)
- Trusted network
- Simple clustering needs
- Process distribution
- Transparent remote messaging

### Use Partisan when:
- Large clusters (>50 nodes)
- Need custom topology
- Multi-datacenter deployment
- Gossip protocols
- Peer-to-peer systems

## Related Skills

- **elixir-patterns**: GenServer, Supervisor, OTP patterns
- **production-quality**: Monitoring, observability, error handling
- **phoenix-liveview**: Phoenix.PubSub, Phoenix.Tracker

Use the **distributed-systems-expert** agent for deep analysis of distributed architectures, consensus algorithm selection, and distributed bug investigation.
