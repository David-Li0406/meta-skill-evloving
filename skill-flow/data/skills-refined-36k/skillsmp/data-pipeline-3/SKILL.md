---
name: data-pipeline
description: GenStage, Broadway, and Flow for Elixir data pipelines
---

# Data Pipeline Patterns Skill

Use this skill when implementing:
- Data processing pipelines
- Streaming data transformations
- Backpressure handling
- ETL operations
- Real-time event processing
- High-throughput data ingestion

## When to Use

- Processing streams of data with backpressure
- Building ETL pipelines
- Real-time event streaming
- Multi-stage data transformations
- Rate-limiting external API calls

## GenStage

### Basic Producer

```elixir
defmodule MyApp.Producer do
  use GenStage

  def start_link(_opts) do
    GenStage.start_link(__MODULE__, :normal)
  end

  @impl true
  def init(:normal) do
    {:producer, state}
  end

  @impl true
  def handle_demand(:start, _from, state) do
    # Emit data events
    {:noreply, [], state}
  end
end
```

### ProducerConsumer

```elixir
defmodule MyApp.ProducerConsumer do
  use GenStage

  def start_link(_opts) do
    GenStage.start_link(__MODULE__, :normal)
  end

  @impl true
  def init(:normal) do
    {:producer_consumer, state}
  end

  @impl true
  def handle_events(events, _from, state) do
    # Process each event
    {:noreply, state}
  end

  @impl true
  def handle_demand(:start, _from, state) do
    # Request more events from producer
    {:noreply, 100, state}
  end
end
```

### Broadway

### Data Processing Pipeline

```elixir
defmodule MyApp.Pipeline do
  use Broadway

  def start_link(opts) do
    Broadway.start_link(__MODULE__, opts)
  end

  @impl true
  def init(opts) do
    Broadway.Topic.producer_name(opts)
  end

  @impl true
  def handle_message(message, metadata) do
    # Process each message
    message
    |> Broadway.Message.update_data(&transform/1)
    |> ack()
  end

  defp transform_1(data) do
    # Transformation logic
    data
  end
end
```

## Backpressure Handling

```elixir
# GenStage automatic backpressure
@max_demand 10  # Consumer asks for at most 10 events

# Broadway automatic backpressure with :concurrency
@concurrency 4  # Process up to 4 messages concurrently
```

## Patterns

### 1. Fan-Out

```elixir
# One producer, multiple consumers
defmodule MyApp.FanOut do
  use GenStage

  def start_link do
    {:producer, [consumer1: :consumer1, consumer2: :consumer2]}
  end
end
```

### 2. Fan-In

```elixir
# Multiple producers, one consumer
defmodule MyApp.FanIn do
  use GenStage

  def start_link do
    {:consumer, [producer1: :producer1, producer2: :producer2]}
  end
end
```

### 3. ETL Pipeline

```elixir
defmodule MyApp.ETL do
  use GenStage

  # Extract
  defmodule Extractor do
    use GenStage
    # Extract data from source
  end

  # Transform
  defmodule Transformer do
    use GenStage
    # Transform data
  end

  # Load
  defmodule Loader do
    use GenStage
    # Load data to destination
  end
end
```

## Best Practices

- **Always handle backpressure** - Never ignore demand
- **Use supervisors** - Ensure proper supervision trees
- **Handle failures** - Implement proper error handling
- **Test with real data** - Test with production-like data volumes
- **Monitor metrics** - Use Telemetry to monitor pipeline performance

## Token Efficiency

Use for:
- Streaming data processing
- ETL operations
- Real-time event handling
- Backpressure-controlled pipelines

Savings: ~40% vs manual pipeline implementation

## Tools to Use

- **GenStage**: Built-in Elixir/OTP
- **Broadway**: Elixir/Erlang data processing
- **Flow**: Parallel data transformation
- **Telemetry**: Metrics and monitoring
