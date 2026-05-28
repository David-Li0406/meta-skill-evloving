package adapters

import (
	"bufio"
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"sort"
	"strings"
	"time"
)

type NexusAdapterOptions struct {
	EventsDir string
	StateDir  string
	Source    string
}

// NexusAdapter syncs Nexus event logs into cortex events.
type NexusAdapter struct {
	eventsDir string
	source    string
}

// NewNexusAdapter creates a new adapter for Nexus event logs.
func NewNexusAdapter(opts NexusAdapterOptions) (*NexusAdapter, error) {
	eventsDir := strings.TrimSpace(opts.EventsDir)
	if eventsDir == "" {
		stateDir := strings.TrimSpace(opts.StateDir)
		if stateDir == "" {
			home, err := os.UserHomeDir()
			if err != nil {
				return nil, fmt.Errorf("failed to get home directory: %w", err)
			}
			stateDir = filepath.Join(home, "nexus", "state")
		}
		eventsDir = filepath.Join(stateDir, "events")
	}

	if _, err := os.Stat(eventsDir); err != nil {
		return nil, fmt.Errorf("nexus events directory not found at %s: %w", eventsDir, err)
	}

	return &NexusAdapter{
		eventsDir: eventsDir,
		source:    strings.TrimSpace(opts.Source),
	}, nil
}

func (a *NexusAdapter) Name() string {
	return "nexus"
}

type nexusEventLogEntry struct {
	ID             string                 `json:"id"`
	Ts             int64                  `json:"ts"`
	Seq            int                    `json:"seq"`
	SessionID      string                 `json:"session_id"`
	Source         string                 `json:"source"`
	EventType      string                 `json:"event_type"`
	CommandPath    string                 `json:"command_path,omitempty"`
	InvocationKind string                 `json:"invocation_kind,omitempty"`
	Stream         string                 `json:"stream,omitempty"`
	Status         string                 `json:"status,omitempty"`
	Error          string                 `json:"error,omitempty"`
	Argv           []string               `json:"argv,omitempty"`
	Cwd            string                 `json:"cwd,omitempty"`
	Data           map[string]interface{} `json:"data,omitempty"`
}

func (a *NexusAdapter) Sync(ctx context.Context, cortexDB *sql.DB, full bool) (SyncResult, error) {
	start := time.Now()
	var result SyncResult

	if _, err := cortexDB.Exec("PRAGMA foreign_keys = ON"); err != nil {
		return result, fmt.Errorf("failed to enable foreign keys: %w", err)
	}
	_, _ = cortexDB.Exec("PRAGMA busy_timeout = 5000")
	_, _ = cortexDB.Exec("PRAGMA journal_mode = WAL")
	_, _ = cortexDB.Exec("PRAGMA synchronous = NORMAL")
	if full {
		_, _ = cortexDB.Exec("PRAGMA synchronous = OFF")
		_, _ = cortexDB.Exec("PRAGMA temp_store = MEMORY")
		_, _ = cortexDB.Exec("PRAGMA cache_size = -200000")         // ~200MB
		_, _ = cortexDB.Exec("PRAGMA mmap_size = 268435456")        // 256MB
		_, _ = cortexDB.Exec("PRAGMA wal_autocheckpoint = 1000000") // reduce checkpoints
	}
	_, _ = cortexDB.Exec("PRAGMA defer_foreign_keys = ON")

	var lastSync int64
	var lastEventID sql.NullString
	if !full {
		row := cortexDB.QueryRow("SELECT last_sync_at, last_event_id FROM sync_watermarks WHERE adapter = ?", a.Name())
		if err := row.Scan(&lastSync, &lastEventID); err != nil && err != sql.ErrNoRows {
			return result, fmt.Errorf("failed to get sync watermark: %w", err)
		}
	}

	files, err := a.listEventFiles()
	if err != nil {
		return result, err
	}

	adapterPrefix := a.Name() + ":"
	threadPrefix := "nexus_session:"
	const contentTypesText = "[\"text\"]"

	txStart := time.Now()
	tx, err := cortexDB.BeginTx(ctx, nil)
	if err != nil {
		return result, fmt.Errorf("begin cortex tx: %w", err)
	}
	defer tx.Rollback()

	stmtInsertThread, err := tx.Prepare(`
		INSERT INTO threads (id, channel, name, source_adapter, source_id, created_at, updated_at)
		VALUES (?, ?, ?, ?, ?, ?, ?)
		ON CONFLICT(source_adapter, source_id) DO UPDATE SET
			name = excluded.name,
			updated_at = excluded.updated_at
	`)
	if err != nil {
		return result, fmt.Errorf("prepare insert thread: %w", err)
	}
	defer stmtInsertThread.Close()

	stmtInsertEvent, err := tx.Prepare(`
		INSERT OR IGNORE INTO events (
			id, timestamp, channel, content_types, content,
			direction, thread_id, reply_to, source_adapter, source_id
		) VALUES (?, ?, ?, ?, ?, ?, ?, NULL, ?, ?)
	`)
	if err != nil {
		return result, fmt.Errorf("prepare insert event: %w", err)
	}
	defer stmtInsertEvent.Close()

	stmtUpdateEvent, err := tx.Prepare(`
		UPDATE events
		SET
			content = ?,
			content_types = ?,
			thread_id = ?
		WHERE source_adapter = ?
		  AND source_id = ?
		  AND (
		    content IS NOT ?
		    OR content_types IS NOT ?
		    OR thread_id IS NOT ?
		  )
	`)
	if err != nil {
		return result, fmt.Errorf("prepare update event: %w", err)
	}
	defer stmtUpdateEvent.Close()

	threadsSeen := make(map[string]struct{})
	maxTS := lastSync
	maxEventID := ""
	if lastEventID.Valid {
		maxEventID = lastEventID.String
	}

	for _, file := range files {
		if err := a.processFile(file, func(entry nexusEventLogEntry) error {
			if a.source != "" && entry.Source != a.source {
				return nil
			}
			if entry.ID == "" || entry.Ts == 0 || entry.SessionID == "" {
				return nil
			}
			tsSec := entry.Ts / 1000
			if !full {
				if tsSec < lastSync {
					return nil
				}
				if tsSec == lastSync && entry.ID <= maxEventID && maxEventID != "" {
					return nil
				}
			}

			if tsSec > maxTS {
				maxTS = tsSec
				maxEventID = entry.ID
			} else if tsSec == maxTS && entry.ID > maxEventID {
				maxEventID = entry.ID
			}

			channel := "nexus"
			if strings.Contains(entry.Source, "agent") {
				channel = "nexus_agent"
			}
			threadID := threadPrefix + entry.SessionID
			if _, ok := threadsSeen[threadID]; !ok {
				now := time.Now().Unix()
				threadName := entry.Source
				if threadName == "" {
					threadName = "nexus"
				}
				res, err := stmtInsertThread.Exec(
					threadID,
					channel,
					threadName,
					a.Name(),
					entry.SessionID,
					now,
					now,
				)
				if err != nil {
					return fmt.Errorf("insert thread: %w", err)
				}
				var exists int
				err = tx.QueryRow("SELECT 1 FROM threads WHERE source_adapter = ? AND source_id = ? AND updated_at < ?",
					a.Name(), entry.SessionID, now).Scan(&exists)
				if err == sql.ErrNoRows {
					result.ThreadsCreated++
				} else if err == nil {
					result.ThreadsUpdated++
				} else if n, _ := res.RowsAffected(); n > 0 {
					result.ThreadsCreated++
				}
				threadsSeen[threadID] = struct{}{}
			}

			contentBytes, err := json.Marshal(entry)
			if err != nil {
				return fmt.Errorf("marshal entry: %w", err)
			}
			content := string(contentBytes)
			eventID := adapterPrefix + entry.ID

			res, err := stmtInsertEvent.Exec(eventID, tsSec, channel, contentTypesText, content, "observed", threadID, a.Name(), entry.ID)
			if err != nil {
				return fmt.Errorf("insert event: %w", err)
			}
			if n, _ := res.RowsAffected(); n == 1 {
				result.EventsCreated++
			} else {
				res2, err := stmtUpdateEvent.Exec(
					content, contentTypesText, threadID,
					a.Name(), entry.ID,
					content, contentTypesText, threadID,
				)
				if err != nil {
					return fmt.Errorf("update event: %w", err)
				}
				if n2, _ := res2.RowsAffected(); n2 == 1 {
					result.EventsUpdated++
				}
			}

			return nil
		}); err != nil {
			return result, err
		}
	}

	if err := tx.Commit(); err != nil {
		return result, fmt.Errorf("commit cortex tx: %w", err)
	}

	_, err = cortexDB.Exec(`
		INSERT INTO sync_watermarks (adapter, last_sync_at, last_event_id)
		VALUES (?, ?, ?)
		ON CONFLICT(adapter) DO UPDATE SET
			last_sync_at = excluded.last_sync_at,
			last_event_id = excluded.last_event_id
	`, a.Name(), maxTS, nullIfEmpty(maxEventID))
	if err != nil {
		return result, fmt.Errorf("failed to update sync watermark: %w", err)
	}

	result.Duration = time.Since(start)
	if result.Perf == nil {
		result.Perf = map[string]string{}
	}
	result.Perf["tx_commit"] = time.Since(txStart).String()
	return result, nil
}

func (a *NexusAdapter) listEventFiles() ([]string, error) {
	entries, err := os.ReadDir(a.eventsDir)
	if err != nil {
		return nil, fmt.Errorf("read events dir: %w", err)
	}
	var files []string
	for _, entry := range entries {
		if entry.IsDir() {
			continue
		}
		name := entry.Name()
		if !strings.HasSuffix(name, ".jsonl") {
			continue
		}
		files = append(files, filepath.Join(a.eventsDir, name))
	}
	sort.Strings(files)
	return files, nil
}

func (a *NexusAdapter) processFile(path string, handle func(entry nexusEventLogEntry) error) error {
	f, err := os.Open(path)
	if err != nil {
		return fmt.Errorf("open events file: %w", err)
	}
	defer f.Close()

	scanner := bufio.NewScanner(f)
	buf := make([]byte, 0, 1024*1024)
	scanner.Buffer(buf, 2*1024*1024)

	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" {
			continue
		}
		var entry nexusEventLogEntry
		if err := json.Unmarshal([]byte(line), &entry); err != nil {
			continue
		}
		if err := handle(entry); err != nil {
			return err
		}
	}
	if err := scanner.Err(); err != nil {
		return fmt.Errorf("scan events file: %w", err)
	}
	return nil
}
