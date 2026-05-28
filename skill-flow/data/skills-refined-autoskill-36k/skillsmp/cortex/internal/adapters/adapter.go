package adapters

import (
	"context"
	"database/sql"
	"time"
)

// Adapter is the interface that all channel adapters must implement
type Adapter interface {
	// Name returns the adapter name (e.g., "imessage", "gmail")
	Name() string

	// Sync synchronizes events from this adapter into the event store
	// full=true forces a complete re-sync, full=false does incremental sync
	Sync(ctx context.Context, db *sql.DB, full bool) (SyncResult, error)
}

// SyncResult contains statistics about a sync operation
type SyncResult struct {
	EventsCreated      int
	EventsUpdated      int
	PersonsCreated     int
	ThreadsCreated     int
	ThreadsUpdated     int
	AttachmentsCreated int
	AttachmentsUpdated int
	ReactionsCreated   int
	ReactionsUpdated   int
	Duration           time.Duration
	// Perf is an optional breakdown of phase timings (human-readable durations).
	Perf map[string]string `json:"perf,omitempty"`
}
