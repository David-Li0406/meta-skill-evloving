package adapters

import (
	"context"
	"database/sql"
	"fmt"
	"os"
	"time"

	"github.com/Napageneral/eve/imessage"
	_ "modernc.org/sqlite"
)

// IMessageAdapter syncs iMessage events directly from chat.db via Eve library
type IMessageAdapter struct {
	chatDBPath string
}

// NewIMessageAdapter creates a new iMessage adapter
func NewIMessageAdapter() (*IMessageAdapter, error) {
	path := imessage.GetChatDBPath()
	if _, err := os.Stat(path); os.IsNotExist(err) {
		return nil, fmt.Errorf("chat.db not found at %s (Full Disk Access required for Terminal)", path)
	}

	return &IMessageAdapter{chatDBPath: path}, nil
}

func (a *IMessageAdapter) Name() string {
	return "imessage"
}

func (a *IMessageAdapter) Sync(ctx context.Context, cortexDB *sql.DB, full bool) (SyncResult, error) {
	startTime := time.Now()
	result := SyncResult{Perf: map[string]string{}}

	// Open chat.db via Eve library
	chatDB, err := imessage.OpenChatDB(a.chatDBPath)
	if err != nil {
		return result, fmt.Errorf("failed to open chat.db: %w", err)
	}
	defer chatDB.Close()

	// Get watermark for incremental sync
	var sinceRowID int64
	if !full {
		// Use max ROWID from messages we've already synced
		// The source_id for imessage events is the message GUID, but we need ROWID
		// For now, use sync_watermarks table
		row := cortexDB.QueryRow("SELECT last_sync_at FROM sync_watermarks WHERE adapter = ?", a.Name())
		if err := row.Scan(&sinceRowID); err != nil && err != sql.ErrNoRows {
			return result, fmt.Errorf("failed to get watermark: %w", err)
		}
	}

	// Get me person ID if exists
	var mePersonID string
	_ = cortexDB.QueryRow("SELECT id FROM persons WHERE is_me = 1 LIMIT 1").Scan(&mePersonID)

	// Call Eve library directly - no JSON, no CLI, no IPC
	opts := imessage.SyncOptions{
		SinceRowID:  sinceRowID,
		MePersonID:  mePersonID,
		AdapterName: a.Name(),
		Full:        full,
	}

	syncResult, err := imessage.Sync(ctx, chatDB, cortexDB, opts)
	if err != nil {
		return result, fmt.Errorf("sync failed: %w", err)
	}

	// Update watermark
	if syncResult.MaxMessageRowID > sinceRowID {
		_, err = cortexDB.Exec(`
			INSERT INTO sync_watermarks (adapter, last_sync_at)
			VALUES (?, ?)
			ON CONFLICT(adapter) DO UPDATE SET last_sync_at = excluded.last_sync_at
		`, a.Name(), syncResult.MaxMessageRowID)
		if err != nil {
			return result, fmt.Errorf("failed to update watermark: %w", err)
		}
	}

	// Map Eve result to Comms result
	result.PersonsCreated = syncResult.HandlesSynced
	result.ThreadsCreated = syncResult.ChatsSynced
	result.EventsCreated = syncResult.MessagesSynced
	result.ReactionsCreated = syncResult.ReactionsSynced
	result.AttachmentsCreated = syncResult.AttachmentsSynced
	result.Duration = time.Since(startTime)

	// Copy performance metrics
	for k, v := range syncResult.Perf {
		result.Perf[k] = v
	}
	result.Perf["total"] = result.Duration.String()

	return result, nil
}
