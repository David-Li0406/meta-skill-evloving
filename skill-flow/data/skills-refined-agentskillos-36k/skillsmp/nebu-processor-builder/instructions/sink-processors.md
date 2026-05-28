# Sink Processors

Sink processors write events to external systems: databases, message queues, files, APIs.

## What is a Sink Processor?

Sinks are the **output layer** in a Nebu pipeline. They:
- Read JSON events from stdin (line-by-line)
- Write to external systems (databases, queues, files)
- Handle connection management
- Implement batching for performance
- Manage errors and retries

```
stdin (JSON) → Sink Logic → External System
```

## When to Use

Create a sink processor when you need to:
- Store events in a database
- Publish to message queues
- Write to files
- Send to external APIs
- Archive data
- Trigger webhooks

**Don't use for:** Extracting from ledgers (use origins), filtering (use transforms)

## Architecture

```
    ┌─────────────┐
    │ stdin       │
    │ (JSON lines)│
    └──────┬──────┘
           │ event
           ↓
    ┌─────────────────────┐
    │ processEvent()      │
    │ - Parse JSON        │
    │ - Validate          │
    │ - Batch (optional)  │
    └──────┬──────────────┘
           │
           ↓
    ┌─────────────────────┐
    │ External System     │
    │ - Database          │
    │ - Message Queue     │
    │ - File              │
    │ - API               │
    └─────────────────────┘
```

## Code Pattern

### Basic Structure

```go
package main

import (
	"database/sql"
	"encoding/json"

	"github.com/spf13/cobra"
	"github.com/withObsrvr/nebu/pkg/processor/cli"
)

var version = "0.1.0"

var (
	dsn string
	// other config
)

func main() {
	config := cli.SinkConfig{
		Name:        "my-sink",
		Description: "Write events to destination",
		Version:     version,
	}

	cli.RunSinkCLI(config, processEvent, addFlags)
}

// processEvent handles a single event
func processEvent(event map[string]interface{}) error {
	// TODO: Implement your sink logic here

	// Example: Write to database
	return writeToDatabase(event)
}

// addFlags adds custom flags
func addFlags(cmd *cobra.Command) {
	cmd.Flags().StringVar(&dsn, "dsn", "", "Database connection string (required)")
	cobra.MarkFlagRequired(cmd.Flags(), "dsn")
}
```

## CLI Helper Usage

```go
cli.RunSinkCLI(config, processEvent, addFlags)
```

**What it does:**
- Reads JSON events from stdin (line-by-line)
- Calls `processEvent()` for each
- Handles errors (prints to stderr)
- Supports `-q` quiet flag
- Signal handling (graceful shutdown)

## Connection Management

### Lazy Initialization

Initialize connections on first event, not in main():

```go
var (
	db     *sql.DB
	dbOnce sync.Once
)

func processEvent(event map[string]interface{}) error {
	// Initialize connection on first use
	dbOnce.Do(func() {
		var err error
		db, err = sql.Open("postgres", dsn)
		if err != nil {
			log.Fatal("failed to connect:", err)
		}
	})

	// Use connection
	return insertEvent(db, event)
}
```

**Why:** Avoid errors during flag parsing. Connect only when actually processing events.

### Connection Pooling

```go
func init() {
	// Will be called when needed
}

func connectDB() *sql.DB {
	db, err := sql.Open("postgres", dsn)
	if err != nil {
		log.Fatal(err)
	}

	// Configure pool
	db.SetMaxOpenConns(25)
	db.SetMaxIdleConns(5)
	db.SetConnMaxLifetime(5 * time.Minute)

	return db
}
```

### Graceful Shutdown

```go
func main() {
	// Setup cleanup
	defer func() {
		if db != nil {
			db.Close()
		}
	}()

	config := cli.SinkConfig{...}
	cli.RunSinkCLI(config, processEvent, addFlags)
}
```

## Batching Patterns

### Simple Batching

Batch events for better performance:

```go
var (
	batch     []map[string]interface{}
	batchSize = 100
	batchLock sync.Mutex
)

func processEvent(event map[string]interface{}) error {
	batchLock.Lock()
	defer batchLock.Unlock()

	batch = append(batch, event)

	if len(batch) >= batchSize {
		return flushBatch()
	}

	return nil
}

func flushBatch() error {
	if len(batch) == 0 {
		return nil
	}

	// Write batch
	err := writeBatch(batch)
	if err != nil {
		return err
	}

	// Clear batch
	batch = nil
	return nil
}
```

### Time-Based Flushing

Flush periodically even if batch not full:

```go
var (
	batch       []map[string]interface{}
	lastFlush   time.Time
	flushPeriod = 5 * time.Second
)

func processEvent(event map[string]interface{}) error {
	batchLock.Lock()
	defer batchLock.Unlock()

	batch = append(batch, event)

	// Flush if size threshold OR time threshold reached
	if len(batch) >= batchSize || time.Since(lastFlush) > flushPeriod {
		return flushBatch()
	}

	return nil
}
```

## Common Patterns

### Database Sink (SQL)

```go
func processEvent(event map[string]interface{}) error {
	// Lazy connect
	if db == nil {
		db = connectDB()
	}

	// Serialize event to JSONB
	eventJSON, err := json.Marshal(event)
	if err != nil {
		return err
	}

	// Insert
	_, err = db.Exec(`
		INSERT INTO events (data, created_at)
		VALUES ($1, NOW())
	`, eventJSON)

	return err
}
```

### Message Queue Sink (NATS)

```go
var (
	nc     *nats.Conn
	ncOnce sync.Once
)

func processEvent(event map[string]interface{}) error {
	// Lazy connect
	ncOnce.Do(func() {
		var err error
		nc, err = nats.Connect(natsURL)
		if err != nil {
			log.Fatal(err)
		}
	})

	// Serialize
	data, err := json.Marshal(event)
	if err != nil {
		return err
	}

	// Publish
	return nc.Publish(subject, data)
}
```

### File Sink

```go
var (
	file     *os.File
	fileOnce sync.Once
	fileLock sync.Mutex
)

func processEvent(event map[string]interface{}) error {
	// Open file on first use
	fileOnce.Do(func() {
		var err error
		file, err = os.OpenFile(outputPath, os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0644)
		if err != nil {
			log.Fatal(err)
		}
	})

	// Serialize
	data, err := json.Marshal(event)
	if err != nil {
		return err
	}

	// Write with lock
	fileLock.Lock()
	defer fileLock.Unlock()

	_, err = file.Write(append(data, '\n'))
	return err
}
```

### API Sink

```go
var httpClient = &http.Client{
	Timeout: 10 * time.Second,
}

func processEvent(event map[string]interface{}) error {
	// Serialize
	data, err := json.Marshal(event)
	if err != nil {
		return err
	}

	// POST to API
	resp, err := httpClient.Post(apiURL, "application/json", bytes.NewReader(data))
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		return fmt.Errorf("API returned %d", resp.StatusCode)
	}

	return nil
}
```

## Error Handling

### Retriable Errors

```go
func processEvent(event map[string]interface{}) error {
	err := writeToDestination(event)

	// Classify error
	if isRetriable(err) {
		// Retry with backoff
		for i := 0; i < maxRetries; i++ {
			time.Sleep(backoff(i))
			err = writeToDestination(event)
			if err == nil {
				return nil
			}
		}
	}

	return err // Fatal or exhausted retries
}

func isRetriable(err error) bool {
	// Network errors, timeouts, rate limits
	return errors.Is(err, syscall.ECONNREFUSED) ||
		errors.Is(err, context.DeadlineExceeded)
}
```

### Logging Errors

```go
func processEvent(event map[string]interface{}) error {
	err := writeToDestination(event)
	if err != nil {
		// Log but don't stop pipeline
		log.Printf("Error processing event %v: %v", event["id"], err)

		// Or stop pipeline
		return err
	}
	return nil
}
```

## Testing

### Unit Tests

```go
func TestProcessEvent(t *testing.T) {
	// Setup test database/file/etc
	db := setupTestDB(t)
	defer db.Close()

	event := map[string]interface{}{
		"id":     "test-123",
		"amount": float64(1000000),
	}

	err := processEvent(event)
	assert.NoError(t, err)

	// Verify written
	var count int
	db.QueryRow("SELECT COUNT(*) FROM events WHERE data->>'id' = $1", "test-123").Scan(&count)
	assert.Equal(t, 1, count)
}
```

### Integration Tests

```bash
# Generate test data
token-transfer --start-ledger 60200000 --end-ledger 60200001 > /tmp/test.jsonl

# Write to sink
cat /tmp/test.jsonl | ./my-sink --dsn "postgres://..."

# Verify written
psql $DSN -c "SELECT COUNT(*) FROM events"

# Check for errors
cat /tmp/test.jsonl | ./my-sink --dsn "postgres://..." 2>&1 | grep -i error
```

## Reference Processors

Study these examples:

### json-file-sink
**What it does:** Writes events to JSONL files
**Key features:**
- Simple file I/O
- Append mode
- Error handling
- Good starting point

**Study:** `examples/processors/json-file-sink/cmd/json-file-sink/main.go`

### postgres-sink
**What it does:** Stores events in PostgreSQL
**Key features:**
- JSONB storage
- TOID generation for idempotency
- Batched COPY for performance
- Connection pooling

**Study:** `examples/processors/postgres-sink/cmd/postgres-sink/main.go`

### nats-sink
**What it does:** Publishes to NATS message bus
**Key features:**
- Lazy connection
- Dynamic subject routing
- JetStream support
- Reconnection handling

**Study:** `examples/processors/nats-sink/cmd/nats-sink/main.go`

## Common Pitfalls

### ❌ DON'T: Connect in main()

```go
// BAD - fails before flags parsed
func main() {
	db = connectDB() // dsn not set yet!
	cli.RunSinkCLI(config, processEvent, addFlags)
}
```

### ✓ DO: Lazy initialization

```go
// GOOD - connect on first event
func processEvent(event map[string]interface{}) error {
	if db == nil {
		db = connectDB() // dsn is set by now
	}
	// ...
}
```

### ❌ DON'T: Ignore flush on shutdown

```go
// BAD - loses last batch
func main() {
	cli.RunSinkCLI(config, processEvent, addFlags)
	// Batch never flushed!
}
```

### ✓ DO: Flush before exit

```go
// GOOD - flush on shutdown
func main() {
	defer func() {
		if len(batch) > 0 {
			flushBatch()
		}
	}()

	cli.RunSinkCLI(config, processEvent, addFlags)
}
```

### ❌ DON'T: Forget connection limits

```go
// BAD - creates unlimited connections
for each event {
	db := connectDB()
	db.Exec(...)
}
```

### ✓ DO: Reuse connections

```go
// GOOD - connection pooling
var db *sql.DB // Reuse

func processEvent(event map[string]interface{}) error {
	if db == nil {
		db = connectDB() // Once
	}
	// Reuse db
}
```

## Performance Tips

1. **Batch writes:** Combine multiple events
2. **Connection pooling:** Reuse connections
3. **Async publishing:** For message queues
4. **Prepared statements:** For SQL
5. **Buffer I/O:** For file writes
6. **Compression:** For large payloads

## Troubleshooting

### Events not being written
- Check connection string/credentials
- Verify destination is accessible
- Check for errors in stderr
- Test connection manually first

### Slow performance
- Implement batching
- Check network latency
- Profile with `go tool pprof`
- Monitor destination system load

### Data corruption
- Verify JSON serialization
- Check character encoding
- Validate before writing
- Test with small dataset first

## Dependencies

Add to go.mod based on destination:

**PostgreSQL:**
```go
require github.com/lib/pq v1.10.9
```

**NATS:**
```go
require github.com/nats-io/nats.go v1.47.0
```

**Redis:**
```go
require github.com/go-redis/redis/v8 v8.11.5
```

## Next Steps

1. Implement `processEvent()` logic
2. Add connection management
3. Implement batching (if appropriate)
4. Add error handling and retries
5. Test with sample data
6. Verify data written correctly
7. Add graceful shutdown
8. Write tests
9. Document in README
10. Create registry entry (if public)

## Additional Resources

- [database/sql Package](https://golang.org/pkg/database/sql/)
- [NATS.go Client](https://github.com/nats-io/nats.go)
- [PostgreSQL in Go](https://github.com/lib/pq)
- [CLI Helpers Source](https://github.com/withObsrvr/nebu/tree/main/pkg/processor/cli)
