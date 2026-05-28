# Nebu Processor Patterns

This guide explains the architecture and patterns for building Nebu processors.

## Overview

Nebu processors are modular components that process Stellar blockchain data. They follow Unix philosophy: do one thing well and compose via pipes.

### Three Types

```
Origin → Transform → Sink
   ↓         ↓         ↓
Extract   Modify    Store
```

**Origin:** Extract data from Stellar ledgers
**Transform:** Filter or modify event streams
**Sink:** Write events to external systems

## Architecture

### Data Flow

```
Stellar RPC
    ↓
Origin Processor (extract events)
    ↓ JSON stream
Transform Processor (filter/modify)
    ↓ JSON stream
Sink Processor (store/publish)
```

### Module Structure

Every processor is a standalone Go module:

```
examples/processors/{name}/
├── cmd/{name}/
│   └── main.go           # CLI entry point
├── go.mod                # Standalone module
├── processor.go          # Business logic (optional)
├── README.md             # Documentation
└── *_test.go             # Tests (optional)
```

**Key requirement:** `go.mod` must NOT have replace directives (breaks `go install`).

## CLI Helpers

Nebu provides CLI helpers in `pkg/processor/cli` to handle:
- Argument parsing (flags, env vars)
- Stdin/stdout handling
- Error reporting
- Signal handling
- Schema versioning

### Available Helpers

**For Origins:**
```go
cli.RunProtoOriginCLI()      // For protobuf-based output
cli.RunGenericOriginCLI()    // For JSON output
```

**For Transforms:**
```go
cli.RunTransformCLI()        // JSON in → JSON out
```

**For Sinks:**
```go
cli.RunSinkCLI()             // JSON in → external system
```

## Code Patterns

### Origin Pattern

```go
func main() {
    config := cli.OriginConfig{
        Name:        "my-origin",
        Description: "Extract events from ledgers",
        Version:     version,
    }

    cli.RunProtoOriginCLI(config, func(networkPass string) cli.ProtoOriginProcessor[*MyEvent] {
        return NewOrigin(networkPass)
    })
}

type Origin struct {
    emitter *processor.Emitter[*MyEvent]
}

func (o *Origin) ProcessLedger(ctx context.Context, ledger xdr.LedgerCloseMeta) error {
    // Extract events from ledger
    events := extractEvents(ledger)

    for _, event := range events {
        o.emitter.Emit(event)
    }

    return nil
}
```

### Transform Pattern

```go
func main() {
    config := cli.TransformConfig{
        Name:        "my-filter",
        Description: "Filter events by criteria",
        Version:     version,
    }

    cli.RunTransformCLI(config, transformEvent, addFlags)
}

func transformEvent(event map[string]interface{}) (map[string]interface{}, error) {
    // Return nil, nil to filter out
    if !shouldInclude(event) {
        return nil, nil
    }

    // Return modified event
    event["enriched"] = "data"
    return event, nil
}

func addFlags(cmd *cobra.Command) {
    cmd.Flags().IntVar(&threshold, "min", 0, "minimum threshold")
}
```

### Sink Pattern

```go
func main() {
    config := cli.SinkConfig{
        Name:        "my-sink",
        Description: "Write events to destination",
        Version:     version,
    }

    cli.RunSinkCLI(config, processEvent, addFlags)
}

func processEvent(event map[string]interface{}) error {
    // Write to external system
    return writeToDestination(event)
}

func addFlags(cmd *cobra.Command) {
    cmd.Flags().StringVar(&dsn, "dsn", "", "connection string")
}
```

## Module Setup

### go.mod Template

```go
module github.com/withObsrvr/nebu/examples/processors/{name}

go 1.25.4

require (
    github.com/withObsrvr/nebu v0.0.0-20251220140929-61e9fa85d21a
    // Add processor-specific dependencies
)

// CRITICAL: NO replace directives!
// Use go.work for local development instead
```

### go.work for Development

When working locally, add processor to workspace:

```go
// /home/tillman/Documents/nebu/go.work
use (
    .
    ./examples/processors/my-processor
)
```

This allows local development without replace directives.

## Common Dependencies

### All Processors
- `github.com/spf13/cobra` - CLI framework (via nebu)
- `github.com/withObsrvr/nebu/pkg/processor/cli` - CLI helpers

### Origin Processors
- `github.com/stellar/go-stellar-sdk` - Stellar types and utilities
- `google.golang.org/protobuf` - For proto-based processors

### Sink Processors
- `github.com/lib/pq` - PostgreSQL driver
- `github.com/nats-io/nats.go` - NATS messaging

## Testing Patterns

### Unit Tests

```go
func TestTransformEvent(t *testing.T) {
    event := map[string]interface{}{
        "amount": 1000000,
    }

    result, err := transformEvent(event)

    assert.NoError(t, err)
    assert.NotNil(t, result)
}
```

### Integration Tests

```bash
# Generate test data
token-transfer --start-ledger 60200000 --end-ledger 60200001 > /tmp/test.jsonl

# Test processor
cat /tmp/test.jsonl | ./my-processor

# Verify output
cat /tmp/test.jsonl | ./my-processor | jq -c . | wc -l
```

## Best Practices

### DO ✓

- Use CLI helpers (don't reinvent)
- Follow reference processor structure
- Add helpful TODOs for implementation
- Write clear package comments
- Include usage examples in README
- Test build immediately after generation
- Keep processors focused (single responsibility)

### DON'T ✗

- Add replace directives to go.mod
- Implement custom cobra setup
- Buffer unbounded event streams
- Hardcode paths or assumptions
- Skip error handling
- Modify events in place
- Create complex logic in initial scaffold

## Error Handling

### Transform Processors

```go
// Filter out (silent)
return nil, nil

// Pass through
return event, nil

// Error (stops pipeline)
return nil, fmt.Errorf("validation failed: %w", err)
```

### Sink Processors

```go
// Success
return nil

// Retriable error
return fmt.Errorf("temporary failure: %w", err)

// Fatal error
log.Fatal("configuration invalid")
```

## Performance Considerations

### Origins
- Process ledgers sequentially (don't buffer all)
- Use efficient XDR parsing
- Emit events as discovered (don't batch unnecessarily)

### Transforms
- Stateless when possible (easier to scale)
- If stateful, use bounded cache
- Don't buffer entire stream

### Sinks
- Batch writes for performance
- Handle backpressure
- Flush on shutdown
- Connection pooling for databases

## Schema Versioning

Add schema version to events:

```go
event := map[string]interface{}{
    "_schema":        "nebu.my_processor.v1",
    "_nebu_version":  version,
    // ... event data
}
```

This helps:
- Track event format changes
- Debug issues
- Version compatibility

## Deployment

### Local Development

```bash
# Build
go build ./cmd/my-processor

# Test
./my-processor --help

# Use in pipeline
token-transfer | ./my-processor | json-file-sink
```

### Installation

```bash
# Via nebu CLI (requires registry entry)
nebu install my-processor

# Direct go install
go install github.com/withObsrvr/nebu/examples/processors/my-processor/cmd/my-processor@latest
```

### Production

- Use `nebu install` for users
- Deploy binaries via go install or releases
- Configure via environment variables
- Monitor with structured logging

## Registry Entry

For public processors, create registry entry:

```yaml
# nebu-processor-registry/processors/my-processor/description.yml
processor:
  name: my-processor
  type: origin|transform|sink
  description: One-line description
  version: 1.0.0
  language: Go
  license: MIT

docs:
  quick_start: |
    nebu install my-processor
    my-processor --help

  examples: |
    # Usage examples
```

## Reference Processors

Study these for patterns:

**Origins:**
- `token-transfer` - Complex proto-based origin
- `contract-events` - Simpler JSON origin
- `contract-invocation` - Invocation processing

**Transforms:**
- `amount-filter` - Numeric filtering
- `usdc-filter` - String matching
- `dedup` - Stateful deduplication
- `time-window` - Time-based filtering

**Sinks:**
- `json-file-sink` - Simple file output
- `nats-sink` - Message queue publishing
- `postgres-sink` - Database storage with batching

## Troubleshooting

### Build fails with "ambiguous import"
- You're in go.work mode (this is OK)
- Build still works: `go build ./cmd/{name}`
- For production, use go install (no go.work)

### "go install" fails with replace directive
- Remove replace from go.mod
- Use go.work for local development
- Ensure module version is published

### Events not flowing through
- Check stdin/stdout handling
- Verify JSON format
- Test with small dataset first
- Use `-q` flag to suppress banners

### Performance issues
- Profile with `go tool pprof`
- Check for buffering unbounded streams
- Verify database connection pooling
- Consider batching for sinks

## Additional Resources

- [Nebu Documentation](https://github.com/withObsrvr/nebu)
- [Stellar Go SDK](https://github.com/stellar/go)
- [CLI Helpers Source](https://github.com/withObsrvr/nebu/tree/main/pkg/processor/cli)
- [Processor Registry](https://github.com/withObsrvr/nebu-processor-registry)
