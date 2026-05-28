# Transform Processors

Transform processors modify event streams: filtering, enriching, or transforming data.

## What is a Transform Processor?

Transforms are the **middle layer** in a Nebu pipeline. They:
- Read JSON events from stdin (line-by-line)
- Apply business logic (filter, modify, enrich)
- Write modified events to stdout
- Can be stateless OR stateful
- Compose via Unix pipes

```
stdin (JSON) → Transform Logic → stdout (JSON)
```

## When to Use

Create a transform processor when you need to:
- Filter events by criteria (amount, asset, address)
- Enrich events with additional data
- Transform event schema or format
- Deduplicate event streams
- Window or aggregate events
- Validate event data

**Don't use for:** Extracting from ledgers (use origins), storing data (use sinks)

## Architecture

```
    ┌─────────────┐
    │ stdin       │
    │ (JSON lines)│
    └──────┬──────┘
           │ event
           ↓
    ┌─────────────────────┐
    │ transformEvent()    │
    │ - Parse JSON        │
    │ - Apply logic       │
    │ - Return result     │
    └──────┬──────────────┘
           │
           ├─→ nil, nil (filter out)
           ├─→ modified event (pass through)
           └─→ error (stop pipeline)
           ↓
    ┌─────────────┐
    │ stdout      │
    │ (JSON lines)│
    └─────────────┘
```

## Code Pattern

### Basic Structure

```go
package main

import (
	"time"

	"github.com/spf13/cobra"
	"github.com/withObsrvr/nebu/pkg/processor/cli"
)

var version = "0.1.0"

// Custom flags
var (
	minAmount int64
	assetCode string
)

func main() {
	config := cli.TransformConfig{
		Name:        "my-filter",
		Description: "Filters events by criteria",
		Version:     version,
	}

	cli.RunTransformCLI(config, transformEvent, addFlags)
}

// transformEvent processes a single event
func transformEvent(event map[string]interface{}) (map[string]interface{}, error) {
	// TODO: Implement your transform logic here

	// Example: Filter by amount
	if amount, ok := event["amount"].(float64); ok {
		if int64(amount) < minAmount {
			return nil, nil // Filter out
		}
	}

	// Example: Enrich event
	event["enriched_at"] = time.Now().Unix()

	return event, nil // Pass through
}

// addFlags adds custom flags to the command
func addFlags(cmd *cobra.Command) {
	cmd.Flags().Int64Var(&minAmount, "min", 0, "Minimum amount")
	cmd.Flags().StringVar(&assetCode, "asset", "", "Filter by asset code")
}
```

## Return Values

The `transformEvent` function has three possible outcomes:

### 1. Filter Out (nil, nil)

```go
if !shouldInclude(event) {
	return nil, nil // Event is silently filtered
}
```

**When to use:** Event doesn't match criteria, should be skipped

### 2. Pass Through (event, nil)

```go
// Unmodified
return event, nil

// Modified
event["new_field"] = "value"
return event, nil
```

**When to use:** Event passes filter or has been modified

### 3. Error (nil, error)

```go
if invalid(event) {
	return nil, fmt.Errorf("invalid event: %w", err)
}
```

**When to use:** Fatal error, should stop entire pipeline

## CLI Helper Usage

```go
cli.RunTransformCLI(config, transformEvent, addFlags)
```

**What it does:**
- Reads JSON events from stdin (line-by-line)
- Calls `transformEvent()` for each
- Writes non-nil results to stdout
- Handles errors (prints to stderr, exits)
- Supports `-q` quiet flag (suppresses banner)
- Signal handling (SIGINT, SIGTERM)

## Stateless vs Stateful

### Stateless (Recommended)

Each event processed independently. No shared state.

```go
func transformEvent(event map[string]interface{}) (map[string]interface{}, error) {
	// Decision based only on current event
	if event["amount"].(float64) > 1000000 {
		return event, nil
	}
	return nil, nil
}
```

**Pros:** Simple, scalable, no memory issues
**Cons:** Can't deduplicate, aggregate, or window

### Stateful (Advanced)

Maintains state across events. Use for deduplication, aggregation, windowing.

```go
var (
	seen     = make(map[string]bool)
	seenLock sync.Mutex
)

func transformEvent(event map[string]interface{}) (map[string]interface{}, error) {
	key := event["txHash"].(string)

	seenLock.Lock()
	defer seenLock.Unlock()

	if seen[key] {
		return nil, nil // Duplicate, filter out
	}

	seen[key] = true
	return event, nil // First occurrence
}
```

**Pros:** Enables deduplication, aggregation
**Cons:** Memory usage grows, need cache eviction strategy

## Common Patterns

### Numeric Filtering

```go
func transformEvent(event map[string]interface{}) (map[string]interface{}, error) {
	amount, ok := event["amount"].(float64)
	if !ok {
		return nil, fmt.Errorf("invalid amount field")
	}

	if amount < float64(minAmount) {
		return nil, nil // Below threshold
	}

	if amount > float64(maxAmount) {
		return nil, nil // Above threshold
	}

	return event, nil
}
```

### String Matching

```go
func transformEvent(event map[string]interface{}) (map[string]interface{}, error) {
	assetCode, ok := event["assetCode"].(string)
	if !ok {
		return nil, nil // No asset code
	}

	if assetCode != targetAsset {
		return nil, nil // Wrong asset
	}

	return event, nil
}
```

### Nested Field Access

```go
func transformEvent(event map[string]interface{}) (map[string]interface{}, error) {
	// Access nested field safely
	transfer, ok := event["transfer"].(map[string]interface{})
	if !ok {
		return nil, nil // No transfer field
	}

	amount, ok := transfer["amount"].(float64)
	if !ok {
		return nil, nil // No amount in transfer
	}

	if amount > 1000000 {
		return event, nil
	}

	return nil, nil
}
```

### Event Enrichment

```go
// Note: import "time" required
func transformEvent(event map[string]interface{}) (map[string]interface{}, error) {
	// Add calculated fields
	if amount, ok := event["amount"].(float64); ok {
		event["amount_usd"] = amount / 10000000 // Convert stroops to dollars
	}

	// Add metadata
	event["processed_at"] = time.Now().Unix()
	event["processor_version"] = version

	return event, nil
}
```

### Deduplication

```go
// Note: import "time" and "sync" required
var (
	cache    = make(map[string]time.Time)
	cacheMux sync.Mutex
	ttl      = 1 * time.Hour
)

func transformEvent(event map[string]interface{}) (map[string]interface{}, error) {
	key := event["txHash"].(string)

	cacheMux.Lock()
	defer cacheMux.Unlock()

	// Check if seen recently
	if lastSeen, exists := cache[key]; exists {
		if time.Since(lastSeen) < ttl {
			return nil, nil // Duplicate
		}
	}

	// Record as seen
	cache[key] = time.Now()

	// Evict old entries (simple strategy)
	if len(cache) > 10000 {
		for k, v := range cache {
			if time.Since(v) > ttl {
				delete(cache, k)
			}
		}
	}

	return event, nil
}
```

## Testing

### Unit Tests

```go
func TestTransformEvent(t *testing.T) {
	tests := []struct {
		name    string
		input   map[string]interface{}
		want    map[string]interface{}
		wantErr bool
	}{
		{
			name: "passes filter",
			input: map[string]interface{}{
				"amount": float64(2000000),
			},
			want: map[string]interface{}{
				"amount": float64(2000000),
			},
		},
		{
			name: "filtered out",
			input: map[string]interface{}{
				"amount": float64(100),
			},
			want: nil, // Filtered
		},
	}

	minAmount = 1000000 // Set threshold

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := transformEvent(tt.input)

			if tt.wantErr {
				assert.Error(t, err)
				return
			}

			assert.NoError(t, err)
			assert.Equal(t, tt.want, got)
		})
	}
}
```

### Integration Tests

```bash
# Generate test data
token-transfer --start-ledger 60200000 --end-ledger 60200001 > /tmp/test.jsonl

# Test transform
cat /tmp/test.jsonl | ./my-filter --min 1000000 > /tmp/filtered.jsonl

# Verify output
echo "Input events: $(wc -l < /tmp/test.jsonl)"
echo "Output events: $(wc -l < /tmp/filtered.jsonl)"

# Check filtered events meet criteria
cat /tmp/filtered.jsonl | jq -r '.amount' | awk '$1 >= 1000000' | wc -l
```

## Reference Processors

Study these examples:

### amount-filter
**What it does:** Filters by amount ranges
**Key features:**
- Min/max amount flags
- Numeric comparison
- Simple stateless filter

**Study:** `examples/processors/amount-filter/cmd/amount-filter/main.go`

### usdc-filter
**What it does:** Filters for USDC transfers only
**Key features:**
- String matching
- Contract address filtering
- Very simple pattern

**Study:** `examples/processors/usdc-filter/cmd/usdc-filter/main.go`

### dedup
**What it does:** Removes duplicate events
**Key features:**
- Stateful (maintains cache)
- Configurable key fields
- Cache eviction strategy

**Study:** `examples/processors/dedup/cmd/dedup/main.go`

### time-window
**What it does:** Filters by time ranges
**Key features:**
- Time-based filtering
- Ledger timestamp parsing
- Duration flags

**Study:** `examples/processors/time-window/cmd/time-window/main.go`

## Common Pitfalls

### ❌ DON'T: Modify event in place without copying

```go
// BAD - mutates input
func transformEvent(event map[string]interface{}) (map[string]interface{}, error) {
	event["modified"] = true
	return nil, nil // Event still modified!
}
```

### ✓ DO: Return nil to filter, or return the event

```go
// GOOD - clear intent
func transformEvent(event map[string]interface{}) (map[string]interface{}, error) {
	if shouldFilter {
		return nil, nil // Explicitly filtered
	}
	event["modified"] = true
	return event, nil // Explicitly passed through
}
```

### ❌ DON'T: Buffer unbounded streams

```go
// BAD - memory leak
var allEvents []map[string]interface{}
func transformEvent(event map[string]interface{}) (map[string]interface{}, error) {
	allEvents = append(allEvents, event)
	// ... process batch later?
	return event, nil
}
```

### ✓ DO: Process incrementally

```go
// GOOD - constant memory
func transformEvent(event map[string]interface{}) (map[string]interface{}, error) {
	// Process immediately, don't accumulate
	result := processEvent(event)
	return result, nil
}
```

### ❌ DON'T: Use unbounded cache

```go
// BAD - grows forever
var cache = make(map[string]bool)
func transformEvent(event map[string]interface{}) (map[string]interface{}, error) {
	key := event["id"].(string)
	if cache[key] {
		return nil, nil
	}
	cache[key] = true // Never evicted!
	return event, nil
}
```

### ✓ DO: Implement cache eviction

```go
// GOOD - bounded memory
func transformEvent(event map[string]interface{}) (map[string]interface{}, error) {
	key := event["id"].(string)

	// LRU, TTL, or size-based eviction
	if len(cache) > maxSize {
		evictOldest()
	}

	// ... rest of logic
}
```

## Performance Tips

1. **Avoid repeated parsing:** Parse nested fields once
2. **Use type assertions:** Check types explicitly
3. **Bounded caches:** For stateful transforms
4. **Early returns:** Filter as soon as criteria not met
5. **No I/O in transform:** Keep pure, no network calls

## Troubleshooting

### Events not being filtered
- Check return values (nil,nil vs event,nil)
- Verify logic conditions
- Test with known inputs
- Add debug logging

### Wrong events passing through
- Verify field names match
- Check type assertions
- Test nested field access
- Validate assumptions about event structure

### Memory issues
- Check for unbounded caches
- Implement eviction strategy
- Profile with `go tool pprof`
- Consider stateless approach

## Next Steps

1. Implement `transformEvent()` logic
2. Add custom flags if needed
3. Test with sample data
4. Verify filtering works correctly
5. Add error handling
6. Write unit tests
7. Document in README
8. Create registry entry (if public)

## Additional Resources

- [CLI Helpers Source](https://github.com/withObsrvr/nebu/tree/main/pkg/processor/cli)
- [JSON in Go](https://golang.org/pkg/encoding/json/)
- [Transform Patterns](https://github.com/withObsrvr/nebu/tree/main/examples/processors)
