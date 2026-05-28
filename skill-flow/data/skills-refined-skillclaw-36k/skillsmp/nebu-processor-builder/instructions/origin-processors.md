# Origin Processors

Origin processors extract data from Stellar ledgers and emit structured events.

## What is an Origin Processor?

Origins are the **data source** in a Nebu pipeline. They:
- Connect to Stellar RPC endpoints
- Read ledger data (XDR format)
- Extract specific events or transactions
- Emit structured JSON or protobuf events
- Handle bounded ledger ranges

```
Stellar RPC → Origin → JSON/Protobuf Events
```

## When to Use

Create an origin processor when you need to:
- Extract specific event types from ledgers
- Process transaction data
- Track contract invocations
- Monitor token transfers
- Index blockchain state changes

**Don't use for:** Filtering existing events (use transforms), storing data (use sinks)

## Architecture

```
    ┌─────────────┐
    │ Stellar RPC │
    └──────┬──────┘
           │ LedgerCloseMeta (XDR)
           ↓
    ┌─────────────────────┐
    │ ProcessLedger()     │
    │ - Parse XDR         │
    │ - Extract events    │
    │ - Enrich data       │
    └──────┬──────────────┘
           │ Events
           ↓
    ┌─────────────┐
    │ Emitter[T]  │
    └──────┬──────┘
           │ JSON/Proto
           ↓
    to stdout
```

## Code Pattern

### Basic Structure

```go
package main

import (
	"github.com/withObsrvr/nebu/pkg/processor/cli"
	"github.com/stellar/go-stellar-sdk/xdr"
)

var version = "0.1.0"

func main() {
	config := cli.OriginConfig{
		Name:        "my-origin",
		Description: "Extract events from ledgers",
		Version:     version,
	}

	// For JSON output
	cli.RunGenericOriginCLI(config, func(networkPass string) cli.GenericOriginProcessor {
		return NewOrigin(networkPass)
	})

	// OR for protobuf output
	// cli.RunProtoOriginCLI(config, func(networkPass string) cli.ProtoOriginProcessor[*MyEvent] {
	//     return NewOrigin(networkPass)
	// })
}
```

### Processor Implementation

```go
type Origin struct {
	passphrase string
	emitter    *processor.Emitter[map[string]interface{}] // or *MyProtoEvent
}

func NewOrigin(passphrase string) *Origin {
	return &Origin{
		passphrase: passphrase,
		emitter:    processor.NewEmitter[map[string]interface{}](1024),
	}
}

// Name implements processor.Processor
func (o *Origin) Name() string {
	return "my-origin"
}

// Type implements processor.Processor
func (o *Origin) Type() processor.Type {
	return processor.TypeOrigin
}

// Out returns output channel
func (o *Origin) Out() <-chan map[string]interface{} {
	return o.emitter.Out()
}

// Close closes the emitter
func (o *Origin) Close() {
	o.emitter.Close()
}

// ProcessLedger implements processor.Origin
func (o *Origin) ProcessLedger(ctx context.Context, ledger xdr.LedgerCloseMeta) error {
	// TODO: Extract events from ledger

	// Example: Process transactions
	reader, err := ingest.NewLedgerTransactionReaderFromLedgerCloseMeta(o.passphrase, ledger)
	if err != nil {
		return err
	}
	defer reader.Close()

	for {
		tx, err := reader.Read()
		if err != nil {
			break // End of transactions
		}

		// Extract your events
		events := extractEventsFromTx(tx)

		for _, event := range events {
			select {
			case <-ctx.Done():
				return ctx.Err()
			default:
				o.emitter.Emit(event)
			}
		}
	}

	return nil
}
```

## CLI Helper Usage

### RunGenericOriginCLI (JSON output)

**When to use:** Simple processors, flexible schema, don't need type safety

```go
cli.RunGenericOriginCLI(config, func(networkPass string) cli.GenericOriginProcessor {
	return NewOrigin(networkPass)
})
```

**Emits:** `map[string]interface{}` as JSON to stdout

### RunProtoOriginCLI (Protobuf output)

**When to use:** Type-safe events, performance critical, complex schemas

```go
cli.RunProtoOriginCLI(config, func(networkPass string) cli.ProtoOriginProcessor[*MyEvent] {
	return NewOrigin(networkPass)
})
```

**Emits:** Protobuf messages as JSON to stdout (automatically serialized)

## Dependencies

Add to go.mod:

```go
require (
	github.com/stellar/go-stellar-sdk v0.1.0
	github.com/withObsrvr/nebu v0.0.0-20251220140929-61e9fa85d21a
)

// If using protobuf:
require google.golang.org/protobuf v1.36.11
```

## Common Patterns

### Tracking Transaction Success

```go
// Build success map
txSuccessMap := make(map[string]bool)
reader, _ := ingest.NewLedgerTransactionReaderFromLedgerCloseMeta(passphrase, ledger)
for {
	tx, err := reader.Read()
	if err != nil {
		break
	}
	txSuccessMap[tx.Result.TransactionHash.HexString()] = tx.Result.Successful()
}

// Use when processing events
event.InSuccessfulTx = txSuccessMap[event.TxHash]
```

### Processing Contract Events

```go
func extractContractEvents(ledger xdr.LedgerCloseMeta) ([]*ContractEvent, error) {
	var events []*ContractEvent

	// Iterate through transactions
	// Extract contract events
	// Decode topics and data

	return events, nil
}
```

### Adding Metadata

```go
event := &Event{
	LedgerSequence: ledger.LedgerSequence(),
	ClosedAt:       ledger.LedgerCloseTime(),
	// ... event-specific data

	// Schema versioning
	Schema:      "nebu.my_origin.v1",
	NebuVersion: version,
}
```

## Testing

### Unit Tests

```go
func TestProcessLedger(t *testing.T) {
	origin := NewOrigin(network.TestNetworkPassphrase)

	// Load test ledger
	ledger := loadTestLedger(t, "testdata/ledger.xdr")

	err := origin.ProcessLedger(context.Background(), ledger)
	assert.NoError(t, err)

	// Verify events emitted
	select {
	case event := <-origin.Out():
		assert.NotNil(t, event)
	case <-time.After(time.Second):
		t.Fatal("no event emitted")
	}
}
```

### Integration Tests

```bash
# Test against real RPC
my-origin --start-ledger 60200000 --end-ledger 60200001 | jq -c . | head -3

# Verify event structure
my-origin --start-ledger 60200000 --end-ledger 60200001 | jq '.eventType' | sort | uniq -c

# Check for errors
my-origin --start-ledger 60200000 --end-ledger 60200001 2>&1 | grep -i error
```

## Reference Processors

Study these examples:

### token-transfer
**What it does:** Extracts token transfer events (transfers, mints, burns)
**Key features:**
- Uses Stellar's official `token_transfer.EventsProcessor`
- Protobuf-based events
- Tracks transaction success
- Handles multiple event types

**Study:** `examples/processors/token-transfer/processor.go`

### contract-events
**What it does:** Extracts all Soroban contract events
**Key features:**
- JSON-based events
- Decodes XDR topics and data
- Simpler than token-transfer
- Good starting point

**Study:** `examples/processors/contract-events/contract_events.go`

### contract-invocation
**What it does:** Extracts contract invocation details
**Key features:**
- Tracks function calls
- Captures arguments and results
- Diagnostic events
- State changes

**Study:** `examples/processors/contract-invocation/processor.go`

## Common Pitfalls

### ❌ DON'T: Buffer all ledgers

```go
// BAD - memory leak for large ranges
var allLedgers []xdr.LedgerCloseMeta
func ProcessLedger(ctx context.Context, ledger xdr.LedgerCloseMeta) error {
	allLedgers = append(allLedgers, ledger) // Grows unbounded!
	return nil
}
```

### ✓ DO: Process incrementally

```go
// GOOD - constant memory
func ProcessLedger(ctx context.Context, ledger xdr.LedgerCloseMeta) error {
	events := extractEvents(ledger)
	for _, event := range events {
		o.emitter.Emit(event) // Stream immediately
	}
	return nil
}
```

### ❌ DON'T: Ignore context cancellation

```go
// BAD - doesn't respect cancellation
func ProcessLedger(ctx context.Context, ledger xdr.LedgerCloseMeta) error {
	for _, event := range manyEvents {
		o.emitter.Emit(event) // Blocks forever if downstream cancelled
	}
	return nil
}
```

### ✓ DO: Check context

```go
// GOOD - respects cancellation
func ProcessLedger(ctx context.Context, ledger xdr.LedgerCloseMeta) error {
	for _, event := range manyEvents {
		select {
		case <-ctx.Done():
			return ctx.Err()
		default:
			o.emitter.Emit(event)
		}
	}
	return nil
}
```

## Performance Tips

1. **Use buffered emitter:** `processor.NewEmitter[T](1024)` - prevents blocking
2. **Parse XDR efficiently:** Reuse readers, avoid repeated parsing
3. **Emit as you go:** Don't collect all events then emit
4. **Handle large ledgers:** Some ledgers have 1000+ events
5. **Connection pooling:** For RPC-heavy processors

## Troubleshooting

### No events emitted
- Check emitter buffer size (increase if needed)
- Verify events are actually being extracted
- Check for early returns or errors
- Test with known ledger containing events

### Wrong event data
- Verify XDR parsing logic
- Check transaction success status
- Ensure metadata fields populated
- Compare with Stellar explorer

### Performance issues
- Profile with `go tool pprof`
- Check for repeated RPC calls
- Verify emitter not blocking
- Test with smaller ledger range first

## Next Steps

1. Implement `ProcessLedger()` logic
2. Add event extraction code
3. Test with small ledger range
4. Verify event structure
5. Add error handling
6. Write tests
7. Document in README
8. Create registry entry (if public)

## Additional Resources

- [Stellar Ingest Package](https://github.com/stellar/go/tree/master/ingest)
- [XDR Types](https://github.com/stellar/go/tree/master/xdr)
- [Token Transfer Processor](https://github.com/stellar/go/tree/master/processors/token_transfer)
- [Nebu Processor Interface](https://github.com/withObsrvr/nebu/tree/main/pkg/processor)
