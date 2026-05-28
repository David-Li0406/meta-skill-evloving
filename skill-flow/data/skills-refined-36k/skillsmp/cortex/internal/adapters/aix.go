package adapters

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"runtime"
	"strings"
	"time"

	"github.com/google/uuid"
	_ "modernc.org/sqlite"
)

// AixAdapter syncs AI session events from aix's SQLite database (Cursor sessions, etc.)
type AixAdapter struct {
	source string // cursor, codex, opencode, ...
	dbPath string
}

// NewAixAdapter creates a new Aix adapter for a given source.
// Currently supported: source="cursor" (others can be added later).
func NewAixAdapter(source string) (*AixAdapter, error) {
	source = strings.TrimSpace(source)
	if source == "" {
		return nil, fmt.Errorf("aix adapter requires source (e.g. cursor)")
	}

	dbPath, err := DefaultAixDBPath()
	if err != nil {
		return nil, err
	}
	if _, err := os.Stat(dbPath); err != nil {
		return nil, fmt.Errorf("aix database not found at %s (run aix sync --all first): %w", dbPath, err)
	}

	return &AixAdapter{
		source: source,
		dbPath: dbPath,
	}, nil
}

func (a *AixAdapter) Name() string {
	// Keep this stable + human friendly; also used as source_adapter and watermark key.
	// If we add more AI sources later, they'll get their own adapter names (codex, opencode, etc.).
	return a.source
}

func (a *AixAdapter) Sync(ctx context.Context, cortexDB *sql.DB, full bool) (SyncResult, error) {
	start := time.Now()
	var result SyncResult

	// Open aix database (read-only)
	aixDB, err := sql.Open("sqlite", "file:"+a.dbPath+"?mode=ro")
	if err != nil {
		return result, fmt.Errorf("failed to open aix database: %w", err)
	}
	defer aixDB.Close()
	// Reduce transient SQLITE_BUSY errors while aix is writing.
	_, _ = aixDB.Exec("PRAGMA busy_timeout = 5000")

	// Enable foreign keys on cortex DB
	if _, err := cortexDB.Exec("PRAGMA foreign_keys = ON"); err != nil {
		return result, fmt.Errorf("failed to enable foreign keys: %w", err)
	}
	// Avoid transient SQLITE_BUSY errors during large writes.
	_, _ = cortexDB.Exec("PRAGMA busy_timeout = 5000")
	// Prefer WAL for ingestion performance (safe default for SQLite).
	_, _ = cortexDB.Exec("PRAGMA journal_mode = WAL")
	_, _ = cortexDB.Exec("PRAGMA synchronous = NORMAL")
	// Aggressive full-sync pragmas (speed > durability during import).
	// NOTE: If the machine crashes mid-import, the cortex DB could be left in a bad state.
	// For full rebuilds, this is an acceptable tradeoff for performance.
	if full {
		_, _ = cortexDB.Exec("PRAGMA synchronous = OFF")
		_, _ = cortexDB.Exec("PRAGMA temp_store = MEMORY")
		_, _ = cortexDB.Exec("PRAGMA cache_size = -200000")         // ~200MB
		_, _ = cortexDB.Exec("PRAGMA mmap_size = 268435456")        // 256MB
		_, _ = cortexDB.Exec("PRAGMA wal_autocheckpoint = 1000000") // reduce checkpoints
	}
	// Keep correctness while reducing per-statement overhead.
	_, _ = cortexDB.Exec("PRAGMA defer_foreign_keys = ON")

	// Get sync watermark (seconds)
	var lastSync int64
	var lastEventID sql.NullString
	if !full {
		row := cortexDB.QueryRow("SELECT last_sync_at, last_event_id FROM sync_watermarks WHERE adapter = ?", a.Name())
		if err := row.Scan(&lastSync, &lastEventID); err != nil && err != sql.ErrNoRows {
			return result, fmt.Errorf("failed to get sync watermark: %w", err)
		}
	}

	// Look up me person if present (optional).
	var mePersonID string
	_ = cortexDB.QueryRow("SELECT id FROM persons WHERE is_me = 1 LIMIT 1").Scan(&mePersonID)

	// Ensure "me" has an identity that indicates presence on this source (helps cross-platform views).
	if mePersonID != "" {
		if err := a.ensureMeIdentity(cortexDB, mePersonID); err != nil {
			return result, err
		}
	}

	// Cache AI persons per model to avoid repeated DB round-trips.
	aiByModel := make(map[string]string) // modelKey -> personID

	lastEvent := ""
	if lastEventID.Valid {
		lastEvent = lastEventID.String
	}

	threadCreated, threadUpdated, threadPerf, err := a.syncSessions(aixDB, cortexDB, lastSync, full)
	if err != nil {
		return result, err
	}
	result.ThreadsCreated = threadCreated
	result.ThreadsUpdated = threadUpdated
	if result.Perf == nil {
		result.Perf = map[string]string{}
	}
	for k, v := range threadPerf {
		result.Perf["threads_"+k] = v
	}

	// Create AI persons *before* the big write transaction to avoid SQLITE_BUSY from nested transactions.
	modelKeys, err := a.listModelsInWindow(aixDB, lastSync, lastEvent)
	if err != nil {
		return result, err
	}
	for _, mk := range modelKeys {
		if _, ok := aiByModel[mk]; ok {
			continue
		}
		pid, createdPerson, err := a.getOrCreateAIPerson(cortexDB, mk)
		if err != nil {
			return result, err
		}
		aiByModel[mk] = pid
		if createdPerson {
			result.PersonsCreated++
		}
	}

	phaseStart := time.Now()
	eventsCreated, eventsUpdated, maxTS, maxEventID, personsCreated, perf, err := a.syncMessages(ctx, aixDB, cortexDB, lastSync, lastEvent, mePersonID, aiByModel)
	if err != nil {
		return result, err
	}
	result.EventsCreated = eventsCreated
	result.EventsUpdated = eventsUpdated
	result.PersonsCreated += personsCreated
	if result.Perf == nil {
		result.Perf = map[string]string{}
	}
	for k, v := range perf {
		result.Perf[k] = v
	}
	result.Perf["total"] = time.Since(phaseStart).String()

	// Update watermark to max imported event timestamp (seconds)
	watermark := lastSync
	if maxTS > watermark {
		watermark = maxTS
	}
	newLastEventID := lastEvent
	if maxTS > lastSync {
		newLastEventID = maxEventID
	} else if maxTS == lastSync && maxEventID != "" && maxEventID > lastEvent {
		newLastEventID = maxEventID
	}
	_, err = cortexDB.Exec(`
		INSERT INTO sync_watermarks (adapter, last_sync_at, last_event_id)
		VALUES (?, ?, ?)
		ON CONFLICT(adapter) DO UPDATE SET
			last_sync_at = excluded.last_sync_at,
			last_event_id = excluded.last_event_id
	`, a.Name(), watermark, nullIfEmpty(newLastEventID))
	if err != nil {
		return result, fmt.Errorf("failed to update sync watermark: %w", err)
	}

	result.Duration = time.Since(start)
	return result, nil
}

func (a *AixAdapter) listModelsInWindow(aixDB *sql.DB, lastSyncSeconds int64, lastEventID string) ([]string, error) {
	query := `
		SELECT DISTINCT COALESCE(NULLIF(TRIM(s.model), ''), 'unknown') as model_key
		FROM messages m
		JOIN sessions s ON m.session_id = s.id
		WHERE s.source = ?
		  AND (
		    CAST(COALESCE(m.timestamp, s.created_at) / 1000 AS INTEGER) > ?
		    OR (CAST(COALESCE(m.timestamp, s.created_at) / 1000 AS INTEGER) = ? AND m.id > ?)
		  )
	`
	rows, err := aixDB.Query(query, a.source, lastSyncSeconds, lastSyncSeconds, lastEventID)
	if err != nil {
		return nil, fmt.Errorf("failed to list models: %w", err)
	}
	defer rows.Close()

	var out []string
	for rows.Next() {
		var mk string
		if err := rows.Scan(&mk); err != nil {
			return nil, fmt.Errorf("scan model: %w", err)
		}
		out = append(out, mk)
	}
	if err := rows.Err(); err != nil {
		return nil, err
	}
	if len(out) == 0 {
		return []string{"unknown"}, nil
	}
	// Ensure fallback exists.
	foundUnknown := false
	for _, mk := range out {
		if mk == "unknown" {
			foundUnknown = true
			break
		}
	}
	if !foundUnknown {
		out = append(out, "unknown")
	}
	return out, nil
}

func nullIfEmpty(s string) interface{} {
	if strings.TrimSpace(s) == "" {
		return nil
	}
	return s
}

func (a *AixAdapter) ensureMeIdentity(cortexDB *sql.DB, mePersonID string) error {
	// This is intentionally coarse; Eve whoami is the canonical rich identity seed.
	identityChannel := "aix"
	identityIdentifier := fmt.Sprintf("aix:%s:user", a.source)
	now := time.Now().Unix()
	identityID := uuid.New().String()
	_, err := cortexDB.Exec(`
		INSERT INTO identities (id, person_id, channel, identifier, created_at)
		VALUES (?, ?, ?, ?, ?)
		ON CONFLICT(channel, identifier) DO UPDATE SET person_id = excluded.person_id
	`, identityID, mePersonID, identityChannel, identityIdentifier, now)
	if err != nil {
		return fmt.Errorf("upsert me aix identity: %w", err)
	}
	return nil
}

func (a *AixAdapter) getOrCreateAIPerson(cortexDB *sql.DB, modelKey string) (personID string, created bool, err error) {
	// Map each (source, model) to a stable identity key.
	identityChannel := "ai"
	identityIdentifier := fmt.Sprintf("aix:%s:model:%s", a.source, modelKey)

	// Try lookup first
	row := cortexDB.QueryRow(`SELECT person_id FROM identities WHERE channel = ? AND identifier = ?`, identityChannel, identityIdentifier)
	if err := row.Scan(&personID); err == nil {
		return personID, false, nil
	} else if err != sql.ErrNoRows {
		return "", false, fmt.Errorf("failed to query ai identity: %w", err)
	}

	// Create person + identity
	personID = uuid.New().String()
	now := time.Now().Unix()
	canonicalName := "AI Assistant"
	sourceTitle := strings.ToUpper(a.source[:1]) + a.source[1:]
	displayName := fmt.Sprintf("%s AI (%s)", sourceTitle, modelKey)

	tx, err := cortexDB.Begin()
	if err != nil {
		return "", false, fmt.Errorf("begin tx: %w", err)
	}
	defer tx.Rollback()

	_, err = tx.Exec(`
		INSERT INTO persons (id, canonical_name, display_name, is_me, created_at, updated_at)
		VALUES (?, ?, ?, 0, ?, ?)
	`, personID, canonicalName, displayName, now, now)
	if err != nil {
		return "", false, fmt.Errorf("insert ai person: %w", err)
	}

	identityID := uuid.New().String()
	_, err = tx.Exec(`
		INSERT INTO identities (id, person_id, channel, identifier, created_at)
		VALUES (?, ?, ?, ?, ?)
		ON CONFLICT(channel, identifier) DO NOTHING
	`, identityID, personID, identityChannel, identityIdentifier, now)
	if err != nil {
		return "", false, fmt.Errorf("insert ai identity: %w", err)
	}

	if err := tx.Commit(); err != nil {
		return "", false, fmt.Errorf("commit tx: %w", err)
	}
	return personID, true, nil
}

func (a *AixAdapter) syncMessages(
	ctx context.Context,
	aixDB *sql.DB,
	cortexDB *sql.DB,
	lastSyncSeconds int64,
	lastEventID string,
	mePersonID string,
	aiByModel map[string]string,
) (created int, updated int, maxImportedTS int64, maxImportedEventID string, personsCreated int, perf map[string]string, err error) {
	_ = ctx
	perf = map[string]string{}

	adapterPrefix := a.Name() + ":"
	toolAdapter := a.Name() + "_tool"
	toolAdapterPrefix := toolAdapter + ":"
	threadPrefix := "aix_session:"
	const contentTypesText = "[\"text\"]"

	query := `
		SELECT
			m.id as message_id,
			m.session_id,
			m.role,
			m.content,
			CAST(COALESCE(m.timestamp, s.created_at) / 1000 AS INTEGER) as ts_sec,
			s.model,
			mm.metadata_json
		FROM messages m
		JOIN sessions s ON m.session_id = s.id
		LEFT JOIN message_metadata mm ON mm.message_id = m.id
		WHERE s.source = ?
		  AND (
		    CAST(COALESCE(m.timestamp, s.created_at) / 1000 AS INTEGER) > ?
		    OR (CAST(COALESCE(m.timestamp, s.created_at) / 1000 AS INTEGER) = ? AND m.id > ?)
		  )
		ORDER BY ts_sec ASC, m.id ASC
	`

	qStart := time.Now()
	rows, err := aixDB.Query(query, a.source, lastSyncSeconds, lastSyncSeconds, lastEventID)
	if err != nil {
		return 0, 0, 0, "", 0, perf, fmt.Errorf("failed to query aix messages: %w", err)
	}
	defer rows.Close()
	perf["query"] = time.Since(qStart).String()

	// Bulk write in a single transaction for SQLite performance.
	txStart := time.Now()
	tx, err := cortexDB.Begin()
	if err != nil {
		return 0, 0, 0, "", 0, perf, fmt.Errorf("begin cortex tx: %w", err)
	}
	defer tx.Rollback()

	stmtInsertEvent, err := tx.Prepare(`
		INSERT OR IGNORE INTO events (
			id, timestamp, channel, content_types, content,
			direction, thread_id, reply_to, source_adapter, source_id, metadata_json
		) VALUES (?, ?, ?, ?, ?, ?, ?, NULL, ?, ?, ?)
	`)
	if err != nil {
		return 0, 0, 0, "", 0, perf, fmt.Errorf("prepare insert event: %w", err)
	}
	defer stmtInsertEvent.Close()

	stmtUpdateEvent, err := tx.Prepare(`
		UPDATE events
		SET
			content = ?,
			content_types = ?,
			thread_id = ?,
			metadata_json = ?
		WHERE source_adapter = ?
		  AND source_id = ?
		  AND (
		    content IS NOT ?
		    OR content_types IS NOT ?
		    OR thread_id IS NOT ?
		    OR metadata_json IS NOT ?
		  )
	`)
	if err != nil {
		return 0, 0, 0, "", 0, perf, fmt.Errorf("prepare update event: %w", err)
	}
	defer stmtUpdateEvent.Close()

	stmtInsertToolEvent, err := tx.Prepare(`
		INSERT OR IGNORE INTO events (
			id, timestamp, channel, content_types, content,
			direction, thread_id, reply_to, source_adapter, source_id, metadata_json
		) VALUES (?, ?, ?, ?, ?, ?, ?, NULL, ?, ?, ?)
	`)
	if err != nil {
		return 0, 0, 0, "", 0, perf, fmt.Errorf("prepare insert tool event: %w", err)
	}
	defer stmtInsertToolEvent.Close()

	stmtUpdateToolEvent, err := tx.Prepare(`
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
		return 0, 0, 0, "", 0, perf, fmt.Errorf("prepare update tool event: %w", err)
	}
	defer stmtUpdateToolEvent.Close()

	stmtInsertParticipant, err := tx.Prepare(`
		INSERT OR IGNORE INTO event_participants (event_id, person_id, role)
		VALUES (?, ?, ?)
	`)
	if err != nil {
		return 0, 0, 0, "", 0, perf, fmt.Errorf("prepare insert participant: %w", err)
	}
	defer stmtInsertParticipant.Close()

	for rows.Next() {
		var (
			messageID    string
			sessionID    string
			role         string
			content      sql.NullString
			tsSec        int64
			model        sql.NullString
			metadataJSON sql.NullString
		)
		if err := rows.Scan(&messageID, &sessionID, &role, &content, &tsSec, &model, &metadataJSON); err != nil {
			return created, updated, maxImportedTS, maxImportedEventID, personsCreated, perf, fmt.Errorf("scan aix message: %w", err)
		}
		if tsSec > maxImportedTS {
			maxImportedTS = tsSec
			maxImportedEventID = messageID
		} else if tsSec == maxImportedTS && messageID > maxImportedEventID {
			maxImportedEventID = messageID
		}

		modelKey := "unknown"
		if model.Valid && strings.TrimSpace(model.String) != "" {
			modelKey = strings.TrimSpace(model.String)
		}

		aiPersonID, ok := aiByModel[modelKey]
		if !ok {
			// Should have been prefetched; fall back to "unknown" if needed.
			aiPersonID = aiByModel["unknown"]
		}

		// Map to cortex event semantics
		direction := "observed"
		switch role {
		case "user":
			direction = "sent"
		case "assistant":
			direction = "received"
		case "tool":
			direction = "observed"
		}

		threadID := threadPrefix + sessionID

		// Deterministic event ID to avoid UUID cost and extra lookups.
		eventID := adapterPrefix + messageID

		// Store metadata if present
		var metadataArg interface{}
		if metadataJSON.Valid && metadataJSON.String != "" {
			metadataArg = metadataJSON.String
		}

		// Insert if new.
		res, err := stmtInsertEvent.Exec(eventID, tsSec, a.source, contentTypesText, content.String, direction, threadID, a.Name(), messageID, metadataArg)
		if err != nil {
			return created, updated, maxImportedTS, maxImportedEventID, personsCreated, perf, fmt.Errorf("insert event: %w", err)
		}
		if n, _ := res.RowsAffected(); n == 1 {
			created++
		} else {
			// Update only if content/thread/metadata changed (prevents massive write churn on incremental runs).
			res2, err := stmtUpdateEvent.Exec(
				content.String, contentTypesText, threadID, metadataArg,
				a.Name(), messageID,
				content.String, contentTypesText, threadID, metadataArg,
			)
			if err != nil {
				return created, updated, maxImportedTS, maxImportedEventID, personsCreated, perf, fmt.Errorf("update event: %w", err)
			}
			if n2, _ := res2.RowsAffected(); n2 == 1 {
				updated++
			}
		}

		// Participants
		if mePersonID != "" && aiPersonID != "" {
			switch role {
			case "user":
				_, _ = stmtInsertParticipant.Exec(eventID, mePersonID, "sender")
				_, _ = stmtInsertParticipant.Exec(eventID, aiPersonID, "recipient")
			case "assistant":
				_, _ = stmtInsertParticipant.Exec(eventID, aiPersonID, "sender")
				_, _ = stmtInsertParticipant.Exec(eventID, mePersonID, "recipient")
			default:
				_, _ = stmtInsertParticipant.Exec(eventID, mePersonID, "observer")
				_, _ = stmtInsertParticipant.Exec(eventID, aiPersonID, "observer")
			}
		}
	}

	if err := rows.Err(); err != nil {
		return created, updated, maxImportedTS, maxImportedEventID, personsCreated, perf, err
	}

	// Sync tool invocations (terminal commands) from message metadata.
	toolQuery := `
		SELECT
			m.id as message_id,
			m.session_id,
			CAST(COALESCE(m.timestamp, s.created_at) / 1000 AS INTEGER) as ts_sec,
			mm.metadata_json
		FROM messages m
		JOIN sessions s ON m.session_id = s.id
		JOIN message_metadata mm ON mm.message_id = m.id
		WHERE s.source = ?
		  AND (
		    mm.metadata_json LIKE '%run_terminal_cmd%'
		    OR mm.metadata_json LIKE '%run_terminal_command_v2%'
		  )
		  AND (
		    CAST(COALESCE(m.timestamp, s.created_at) / 1000 AS INTEGER) > ?
		    OR (CAST(COALESCE(m.timestamp, s.created_at) / 1000 AS INTEGER) = ? AND m.id > ?)
		  )
		ORDER BY ts_sec ASC, m.id ASC
	`
	toolQStart := time.Now()
	toolRows, err := aixDB.Query(toolQuery, a.source, lastSyncSeconds, lastSyncSeconds, lastEventID)
	if err != nil {
		return created, updated, maxImportedTS, maxImportedEventID, personsCreated, perf, fmt.Errorf("failed to query aix tool metadata: %w", err)
	}
	defer toolRows.Close()
	perf["tool_query"] = time.Since(toolQStart).String()

	for toolRows.Next() {
		var (
			messageID string
			sessionID string
			tsSec     int64
			metaJSON  string
		)
		if err := toolRows.Scan(&messageID, &sessionID, &tsSec, &metaJSON); err != nil {
			return created, updated, maxImportedTS, maxImportedEventID, personsCreated, perf, fmt.Errorf("scan aix tool metadata: %w", err)
		}

		toolName, toolCallID, command, ok := parseToolFormerCommand(metaJSON)
		if !ok || !isTerminalToolName(toolName) {
			continue
		}

		sourceID := messageID
		if toolCallID != "" {
			sourceID = messageID + ":" + toolCallID
		}
		eventID := toolAdapterPrefix + sourceID
		threadID := threadPrefix + sessionID

		res, err := stmtInsertToolEvent.Exec(eventID, tsSec, a.source, contentTypesText, command, "observed", threadID, toolAdapter, sourceID, metaJSON)
		if err != nil {
			return created, updated, maxImportedTS, maxImportedEventID, personsCreated, perf, fmt.Errorf("insert tool event: %w", err)
		}
		if n, _ := res.RowsAffected(); n == 1 {
			created++
		} else {
			res2, err := stmtUpdateToolEvent.Exec(
				command, contentTypesText, threadID,
				toolAdapter, sourceID,
				command, contentTypesText, threadID,
			)
			if err != nil {
				return created, updated, maxImportedTS, maxImportedEventID, personsCreated, perf, fmt.Errorf("update tool event: %w", err)
			}
			if n2, _ := res2.RowsAffected(); n2 == 1 {
				updated++
			}
		}
	}

	if err := toolRows.Err(); err != nil {
		return created, updated, maxImportedTS, maxImportedEventID, personsCreated, perf, err
	}
	if err := tx.Commit(); err != nil {
		return created, updated, maxImportedTS, maxImportedEventID, personsCreated, perf, fmt.Errorf("commit cortex tx: %w", err)
	}
	perf["tx_commit"] = time.Since(txStart).String()
	return created, updated, maxImportedTS, maxImportedEventID, personsCreated, perf, nil
}

func insertParticipant(db *sql.DB, eventID, personID, role string) error {
	_, err := db.Exec(`
		INSERT INTO event_participants (event_id, person_id, role)
		VALUES (?, ?, ?)
		ON CONFLICT(event_id, person_id, role) DO NOTHING
	`, eventID, personID, role)
	return err
}

func (a *AixAdapter) syncSessions(aixDB, cortexDB *sql.DB, lastSyncSeconds int64, full bool) (threadsCreated int, threadsUpdated int, perf map[string]string, err error) {
	perf = map[string]string{}

	query := `
		SELECT
			id,
			created_at,
			model
		FROM sessions
		WHERE source = ?
		ORDER BY created_at ASC, id ASC
	`
	args := []interface{}{a.source}
	if !full {
		query = `
			SELECT
				id,
				created_at,
				model
			FROM sessions
			WHERE source = ?
			  AND CAST(COALESCE(created_at, 0) / 1000 AS INTEGER) > ?
			ORDER BY created_at ASC, id ASC
		`
		args = append(args, lastSyncSeconds)
	}

	qStart := time.Now()
	rows, err := aixDB.Query(query, args...)
	if err != nil {
		return 0, 0, perf, fmt.Errorf("failed to query aix sessions: %w", err)
	}
	defer rows.Close()
	perf["query"] = time.Since(qStart).String()

	txStart := time.Now()
	tx, err := cortexDB.Begin()
	if err != nil {
		return 0, 0, perf, fmt.Errorf("begin cortex tx: %w", err)
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
		return 0, 0, perf, fmt.Errorf("prepare insert thread: %w", err)
	}
	defer stmtInsertThread.Close()

	threadPrefix := "aix_session:"

	for rows.Next() {
		var (
			sessionID string
			createdAt sql.NullInt64
			model     sql.NullString
		)
		if err := rows.Scan(&sessionID, &createdAt, &model); err != nil {
			return threadsCreated, threadsUpdated, perf, fmt.Errorf("scan aix session: %w", err)
		}

		threadID := threadPrefix + sessionID
		threadName := "Cursor Session"
		if model.Valid && strings.TrimSpace(model.String) != "" {
			threadName = strings.TrimSpace(model.String)
		}

		now := time.Now().Unix()
		if createdAt.Valid && createdAt.Int64 > 0 {
			now = createdAt.Int64 / 1000
		}

		res, err := stmtInsertThread.Exec(
			threadID,
			a.source,
			threadName,
			a.Name(),
			sessionID,
			now,
			now,
		)
		if err != nil {
			return threadsCreated, threadsUpdated, perf, fmt.Errorf("upsert thread: %w", err)
		}

		var exists int
		err = tx.QueryRow("SELECT 1 FROM threads WHERE source_adapter = ? AND source_id = ? AND updated_at < ?",
			a.Name(), sessionID, now).Scan(&exists)
		if err == sql.ErrNoRows {
			threadsCreated++
		} else if err == nil {
			threadsUpdated++
		} else {
			if n, _ := res.RowsAffected(); n > 0 {
				threadsCreated++
			}
		}
	}

	if err := rows.Err(); err != nil {
		return threadsCreated, threadsUpdated, perf, err
	}
	if err := tx.Commit(); err != nil {
		return threadsCreated, threadsUpdated, perf, fmt.Errorf("commit cortex tx: %w", err)
	}
	perf["tx_commit"] = time.Since(txStart).String()
	return threadsCreated, threadsUpdated, perf, nil
}

type aixToolFormerData struct {
	Name           string         `json:"name"`
	Status         string         `json:"status"`
	RawArgs        any            `json:"rawArgs"`
	Params         any            `json:"params"`
	AdditionalData map[string]any `json:"additionalData"`
	ToolCallID     string         `json:"toolCallId"`
}

type aixMessageMeta struct {
	ToolFormerData *aixToolFormerData `json:"toolFormerData"`
}

func parseToolFormerCommand(metaJSON string) (toolName, toolCallID, command string, ok bool) {
	var meta aixMessageMeta
	if err := json.Unmarshal([]byte(metaJSON), &meta); err != nil {
		return "", "", "", false
	}
	if meta.ToolFormerData == nil {
		return "", "", "", false
	}
	toolName = strings.TrimSpace(meta.ToolFormerData.Name)
	if toolName == "" {
		return "", "", "", false
	}
	if !shouldRecordToolCommand(meta.ToolFormerData) {
		return "", "", "", false
	}
	toolCallID = strings.TrimSpace(meta.ToolFormerData.ToolCallID)
	command = extractToolCommand(meta.ToolFormerData.Params)
	if command == "" {
		command = extractToolCommand(meta.ToolFormerData.RawArgs)
	}
	command = strings.TrimSpace(command)
	if command == "" {
		return "", "", "", false
	}
	return toolName, toolCallID, command, true
}

func shouldRecordToolCommand(tfd *aixToolFormerData) bool {
	status := strings.ToLower(strings.TrimSpace(tfd.Status))
	if status != "" && status != "completed" && status != "error" {
		return false
	}
	adStatus := strings.ToLower(strings.TrimSpace(asString(tfd.AdditionalData["status"])))
	switch adStatus {
	case "cancelled", "pending", "running":
		return false
	}
	return true
}

func extractToolCommand(val any) string {
	switch v := val.(type) {
	case string:
		var payload map[string]any
		if err := json.Unmarshal([]byte(v), &payload); err != nil {
			return ""
		}
		return asString(payload["command"])
	case map[string]any:
		return asString(v["command"])
	default:
		return ""
	}
}

func asString(val any) string {
	if s, ok := val.(string); ok {
		return s
	}
	return ""
}

func isTerminalToolName(name string) bool {
	switch strings.TrimSpace(name) {
	case "run_terminal_cmd", "run_terminal_command_v2":
		return true
	default:
		return false
	}
}

// DefaultAixDBPath returns the default path for aix.db.
func DefaultAixDBPath() (string, error) {
	return defaultAixDBPath()
}

func defaultAixDBPath() (string, error) {
	if override := os.Getenv("AIX_DB_PATH"); strings.TrimSpace(override) != "" {
		return filepath.Clean(os.ExpandEnv(override)), nil
	}
	home, err := os.UserHomeDir()
	if err != nil {
		return "", fmt.Errorf("failed to get home directory: %w", err)
	}
	if runtime.GOOS == "darwin" {
		return filepath.Join(home, "Library", "Application Support", "aix", "aix.db"), nil
	}
	if xdg := os.Getenv("XDG_DATA_HOME"); xdg != "" {
		return filepath.Join(xdg, "aix", "aix.db"), nil
	}
	return filepath.Join(home, ".local", "share", "aix", "aix.db"), nil
}
