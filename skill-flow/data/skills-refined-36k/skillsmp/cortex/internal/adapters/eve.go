package adapters

// DEPRECATED: This adapter reads from eve.db which is no longer used.
// Use IMessageAdapter (imessage.go) instead, which reads directly from chat.db
// via the eve/imessage library package.
//
// This file is kept for reference during the migration period and will be
// removed in a future version.

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"

	"github.com/google/uuid"
	_ "modernc.org/sqlite"
)

// EveAdapter syncs iMessage events from Eve's database
//
// Deprecated: Use IMessageAdapter instead, which reads directly from chat.db
type EveAdapter struct {
	eveDBPath string
}

// NewEveAdapter creates a new Eve adapter
//
// Deprecated: Use NewIMessageAdapter instead
func NewEveAdapter() (*EveAdapter, error) {
	home, err := os.UserHomeDir()
	if err != nil {
		return nil, fmt.Errorf("failed to get home directory: %w", err)
	}

	eveDBPath := filepath.Join(home, "Library", "Application Support", "Eve", "eve.db")
	if _, err := os.Stat(eveDBPath); os.IsNotExist(err) {
		return nil, fmt.Errorf("Eve database not found at %s", eveDBPath)
	}

	return &EveAdapter{
		eveDBPath: eveDBPath,
	}, nil
}

func (e *EveAdapter) Name() string {
	return "imessage"
}

// normalizePhoneEve normalizes phone numbers to match Eve's normalizePhoneNumber format:
// - Remove all non-digit chars
// - If 11 digits starting with 1, drop the leading 1 (US numbers)
// This matches Eve's internal normalization for consistent matching
func normalizePhoneEve(s string) string {
	s = strings.TrimSpace(s)
	if s == "" {
		return ""
	}
	// Remove all non-digit characters
	var b strings.Builder
	for _, r := range s {
		if r >= '0' && r <= '9' {
			b.WriteRune(r)
		}
	}
	digits := b.String()

	// If it's a US number (11 digits starting with 1), remove the leading 1
	if len(digits) == 11 && strings.HasPrefix(digits, "1") {
		return digits[1:]
	}
	return digits
}

func (e *EveAdapter) Sync(ctx context.Context, cortexDB *sql.DB, full bool) (SyncResult, error) {
	startTime := time.Now()
	result := SyncResult{}

	// Open Eve database (read-only)
	eveDB, err := sql.Open("sqlite", "file:"+e.eveDBPath+"?mode=ro&_busy_timeout=5000")
	if err != nil {
		return result, fmt.Errorf("failed to open Eve database: %w", err)
	}
	defer eveDB.Close()

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
		_, _ = cortexDB.Exec("PRAGMA cache_size = -200000")        // ~200MB
		_, _ = cortexDB.Exec("PRAGMA mmap_size = 268435456")       // 256MB
		_, _ = cortexDB.Exec("PRAGMA wal_autocheckpoint = 1000000") // reduce checkpoints
	}
	// Keep correctness while reducing per-statement overhead.
	_, _ = cortexDB.Exec("PRAGMA defer_foreign_keys = ON")

	// Get sync watermark (last synced timestamp)
	var lastSyncTimestamp int64
	if !full {
		row := cortexDB.QueryRow("SELECT last_sync_at FROM sync_watermarks WHERE adapter = ?", e.Name())
		if err := row.Scan(&lastSyncTimestamp); err != nil && err != sql.ErrNoRows {
			return result, fmt.Errorf("failed to get sync watermark: %w", err)
		}
	}

	// Sync contacts first (to establish person/identity mappings)
	contactsStart := time.Now()
	personsCreated, contactMap, mePersonID, perfContacts, err := e.syncContacts(ctx, eveDB, cortexDB)
	if err != nil {
		return result, fmt.Errorf("failed to sync contacts: %w", err)
	}
	result.PersonsCreated = personsCreated
	if result.Perf == nil {
		result.Perf = map[string]string{}
	}
	for k, v := range perfContacts {
		result.Perf["contacts."+k] = v
	}
	result.Perf["contacts.total"] = time.Since(contactsStart).String()

	// Sync chats/threads (to establish thread metadata)
	chatsStart := time.Now()
	threadsCreated, threadsUpdated, perfChats, err := e.syncChats(ctx, eveDB, cortexDB)
	if err != nil {
		return result, fmt.Errorf("failed to sync chats: %w", err)
	}
	result.ThreadsCreated = threadsCreated
	result.ThreadsUpdated = threadsUpdated
	for k, v := range perfChats {
		result.Perf["chats."+k] = v
	}
	result.Perf["chats.total"] = time.Since(chatsStart).String()

	// Sync messages
	messagesStart := time.Now()
	eventsCreated, eventsUpdated, maxImportedTimestamp, perfMessages, err := e.syncMessages(ctx, eveDB, cortexDB, lastSyncTimestamp, contactMap, mePersonID)
	if err != nil {
		return result, fmt.Errorf("failed to sync messages: %w", err)
	}
	result.EventsCreated = eventsCreated
	result.EventsUpdated = eventsUpdated
	for k, v := range perfMessages {
		result.Perf["messages."+k] = v
	}
	result.Perf["messages.total"] = time.Since(messagesStart).String()

	// Sync attachments
	attachmentsStart := time.Now()
	attachmentsCreated, attachmentsUpdated, perfAttachments, err := e.syncAttachments(ctx, eveDB, cortexDB, lastSyncTimestamp)
	if err != nil {
		return result, fmt.Errorf("failed to sync attachments: %w", err)
	}
	result.AttachmentsCreated = attachmentsCreated
	result.AttachmentsUpdated = attachmentsUpdated
	for k, v := range perfAttachments {
		result.Perf["attachments."+k] = v
	}
	result.Perf["attachments.total"] = time.Since(attachmentsStart).String()

	// Sync reactions
	reactionsStart := time.Now()
	reactionsCreated, reactionsUpdated, perfReactions, err := e.syncReactions(ctx, eveDB, cortexDB, lastSyncTimestamp, contactMap, mePersonID)
	if err != nil {
		return result, fmt.Errorf("failed to sync reactions: %w", err)
	}
	result.ReactionsCreated = reactionsCreated
	result.ReactionsUpdated = reactionsUpdated
	for k, v := range perfReactions {
		result.Perf["reactions."+k] = v
	}
	result.Perf["reactions.total"] = time.Since(reactionsStart).String()

	// Update sync watermark
	// IMPORTANT: use the max imported event timestamp, NOT wall-clock time.
	// This avoids skipping late-arriving/backfilled messages whose timestamp is older than "now".
	watermark := lastSyncTimestamp
	if maxImportedTimestamp > watermark {
		watermark = maxImportedTimestamp
	}
	_, err = cortexDB.Exec(`
		INSERT INTO sync_watermarks (adapter, last_sync_at)
		VALUES (?, ?)
		ON CONFLICT(adapter) DO UPDATE SET last_sync_at = excluded.last_sync_at
	`, e.Name(), watermark)
	if err != nil {
		return result, fmt.Errorf("failed to update sync watermark: %w", err)
	}

	result.Duration = time.Since(startTime)
	if result.Perf == nil {
		result.Perf = map[string]string{}
	}
	result.Perf["total"] = result.Duration.String()
	return result, nil
}

// syncContacts syncs Eve contacts to cortex persons and identities
func (e *EveAdapter) syncContacts(ctx context.Context, eveDB, cortexDB *sql.DB) (personsCreated int, contactMap map[int64]string, mePersonID string, perf map[string]string, err error) {
	perf = map[string]string{}

	// Seed "me" from Eve's rich whoami info (authoritative identity set: phones/emails/handles).
	// This is the key link that allows other adapters (aix/gmail/...) to attach to a cohesive user.
	wStart := time.Now()
	meCreated, meID, err := e.syncWhoami(ctx, eveDB, cortexDB)
	if err != nil {
		return 0, nil, "", perf, err
	}
	mePersonID = meID
	perf["whoami"] = time.Since(wStart).String()

	// Query contacts and their identifiers from Eve
	qStart := time.Now()
	rows, err := eveDB.Query(`
		SELECT
			c.id,
			c.name,
			c.nickname,
			ci.identifier,
			ci.type
		FROM contacts c
		LEFT JOIN contact_identifiers ci ON c.id = ci.contact_id
		WHERE c.is_me = 0
		ORDER BY c.id
	`)
	if err != nil {
		return meCreated, nil, mePersonID, perf, fmt.Errorf("failed to query Eve contacts: %w", err)
	}
	defer rows.Close()
	perf["query"] = time.Since(qStart).String()

	personsCreated = meCreated
	contactMap = make(map[int64]string) // Eve contact_id -> cortex person_id

	// Bulk write in a single transaction for SQLite performance.
	txStart := time.Now()
	tx, err := cortexDB.Begin()
	if err != nil {
		return personsCreated, contactMap, mePersonID, perf, fmt.Errorf("begin cortex tx: %w", err)
	}
	defer tx.Rollback()

	stmtInsertPerson, err := tx.Prepare(`
		INSERT INTO persons (id, canonical_name, is_me, created_at, updated_at)
		VALUES (?, ?, 0, ?, ?)
	`)
	if err != nil {
		return personsCreated, contactMap, mePersonID, perf, fmt.Errorf("prepare insert person: %w", err)
	}
	defer stmtInsertPerson.Close()

	stmtInsertIdentity, err := tx.Prepare(`
		INSERT INTO identities (id, person_id, channel, identifier, created_at)
		VALUES (?, ?, ?, ?, ?)
		ON CONFLICT(channel, identifier) DO NOTHING
	`)
	if err != nil {
		return personsCreated, contactMap, mePersonID, perf, fmt.Errorf("prepare insert identity: %w", err)
	}
	defer stmtInsertIdentity.Close()

		for rows.Next() {
		var eveContactID int64
		var name, nickname sql.NullString
		var identifier, identifierType sql.NullString

		if err := rows.Scan(&eveContactID, &name, &nickname, &identifier, &identifierType); err != nil {
			return personsCreated, contactMap, mePersonID, perf, fmt.Errorf("failed to scan contact row: %w", err)
		}

		// Determine canonical name - never fall back to phone identifiers
		canonicalName := "Unknown Contact"
		if name.Valid && name.String != "" {
			canonicalName = name.String
		} else if nickname.Valid && nickname.String != "" {
			canonicalName = nickname.String
		}
		// Explicitly do NOT fall back to identifier - use "Unknown Contact" instead

		// FIXED: First check if we already have a person for this Eve contact_id
		// This handles contacts with multiple identifiers (phone + email)
		var personID string
		if existingPersonID, ok := contactMap[eveContactID]; ok {
			personID = existingPersonID
		} else if identifier.Valid && identifierType.Valid {
			// Try to find person by identifier (normalize phone numbers to Eve format)
			lookupIdent := identifier.String
			if identifierType.String == "phone" {
				lookupIdent = normalizePhoneEve(lookupIdent)
			}
			// Note: Use tx.QueryRow to avoid deadlock - SQLite doesn't allow concurrent access
			row := tx.QueryRow(`
				SELECT person_id FROM identities
				WHERE channel = ? AND identifier = ?
			`, identifierType.String, lookupIdent)
			if err := row.Scan(&personID); err != nil && err != sql.ErrNoRows {
				return personsCreated, contactMap, mePersonID, perf, fmt.Errorf("failed to query identity: %w", err)
			}
		}

		// If not found, create new person
		if personID == "" {
			personID = uuid.New().String()
			now := time.Now().Unix()

			// Best-effort: if insert fails due to uniqueness collisions on identities, we still map this contact_id.
			if _, err := stmtInsertPerson.Exec(personID, canonicalName, now, now); err == nil {
				personsCreated++
			}
		}

		contactMap[eveContactID] = personID

		// Add identity if we have an identifier
		if identifier.Valid && identifierType.Valid {
			identityID := uuid.New().String()
			now := time.Now().Unix()

			// Normalize phone numbers to Eve format for consistent matching
			ident := identifier.String
			if identifierType.String == "phone" {
				ident = normalizePhoneEve(ident)
			}
			_, _ = stmtInsertIdentity.Exec(identityID, personID, identifierType.String, ident, now)
		}
	}

	if err := rows.Err(); err != nil {
		return personsCreated, contactMap, mePersonID, perf, err
	}
	if err := tx.Commit(); err != nil {
		return personsCreated, contactMap, mePersonID, perf, fmt.Errorf("commit cortex tx: %w", err)
	}
	perf["tx_commit"] = time.Since(txStart).String()
	return personsCreated, contactMap, mePersonID, perf, nil
}

func (e *EveAdapter) syncWhoami(ctx context.Context, eveDB, cortexDB *sql.DB) (personsCreated int, mePersonID string, err error) {
	type whoamiJSON struct {
		OK     bool     `json:"ok"`
		Name   string   `json:"name"`
		Emails []string `json:"emails"`
		Phones []string `json:"phones"`
	}

	findEveBin := func() (string, bool) {
		// Explicit override (best for testing + portability).
		if p := os.Getenv("CORTEX_EVE_BIN"); p != "" {
			return p, true
		}
		if p := os.Getenv("COMMS_EVE_BIN"); p != "" {
			return p, true
		}
		if p := os.Getenv("EVE_BIN"); p != "" {
			return p, true
		}

		// Normal PATH lookup.
		if p, err := exec.LookPath("eve"); err == nil {
			return p, true
		}

		// Common dev locations in this Nexus workspace.
		home, err := os.UserHomeDir()
		if err == nil {
			candidates := []string{
				filepath.Join(home, "nexus", "home", "projects", "eve", "bin", "eve"),
				filepath.Join(home, "Desktop", "projects", "eve", "bin", "eve"),
			}
			for _, p := range candidates {
				if st, err := os.Stat(p); err == nil && !st.IsDir() {
					return p, true
				}
			}
		}

		return "", false
	}

	// Prefer the Eve CLI `whoami` output (this is what the user sees and is the richest signal).
	// If the `eve` binary is not available, fall back to any warehouse representation (if present).
	if evePath, ok := findEveBin(); ok {
		cmd := exec.CommandContext(ctx, evePath, "whoami")
		out, runErr := cmd.Output()
		if runErr != nil {
			return 0, "", fmt.Errorf("failed to run `eve whoami` for seeding me: %w", runErr)
		}
		var w whoamiJSON
		if err := json.Unmarshal(out, &w); err != nil {
			return 0, "", fmt.Errorf("failed to parse `eve whoami` output: %w", err)
		}
		if w.OK {
			now := time.Now().Unix()

			// Find or create the cortex "me" person.
			_ = cortexDB.QueryRow("SELECT id FROM persons WHERE is_me = 1 LIMIT 1").Scan(&mePersonID)

			bestName := w.Name
			if bestName == "" {
				bestName = "Me"
			}

			if mePersonID == "" {
				mePersonID = uuid.New().String()
				if _, err := cortexDB.Exec(`
					INSERT INTO persons (id, canonical_name, is_me, created_at, updated_at)
					VALUES (?, ?, 1, ?, ?)
				`, mePersonID, bestName, now, now); err != nil {
					return 0, "", fmt.Errorf("failed to create me person: %w", err)
				}
				personsCreated++
			} else {
				// Best-effort: keep canonical_name fresh if it was a placeholder.
				_, _ = cortexDB.Exec(
					`UPDATE persons SET canonical_name = ?, updated_at = ? WHERE id = ? AND (canonical_name = '' OR canonical_name = 'Me' OR canonical_name = 'Unknown')`,
					bestName, now, mePersonID,
				)
			}

			// Upsert phone/email identities onto the cortex me person.
			for _, p := range w.Phones {
				if p == "" {
					continue
				}
				identityID := uuid.New().String()
				if _, err := cortexDB.Exec(`
					INSERT INTO identities (id, person_id, channel, identifier, created_at)
					VALUES (?, ?, ?, ?, ?)
					ON CONFLICT(channel, identifier) DO UPDATE SET person_id = excluded.person_id
				`, identityID, mePersonID, "phone", p, now); err != nil {
					return personsCreated, mePersonID, fmt.Errorf("failed to upsert whoami phone identity: %w", err)
				}
			}
			for _, em := range w.Emails {
				if em == "" {
					continue
				}
				identityID := uuid.New().String()
				if _, err := cortexDB.Exec(`
					INSERT INTO identities (id, person_id, channel, identifier, created_at)
					VALUES (?, ?, ?, ?, ?)
					ON CONFLICT(channel, identifier) DO UPDATE SET person_id = excluded.person_id
				`, identityID, mePersonID, "email", em, now); err != nil {
					return personsCreated, mePersonID, fmt.Errorf("failed to upsert whoami email identity: %w", err)
				}
			}

			return personsCreated, mePersonID, nil
		}
	}

	// Find or create the cortex "me" person.
	_ = cortexDB.QueryRow("SELECT id FROM persons WHERE is_me = 1 LIMIT 1").Scan(&mePersonID)

	rows, err := eveDB.Query(`
		SELECT
			c.name,
			c.nickname,
			ci.identifier,
			ci.type
		FROM contacts c
		LEFT JOIN contact_identifiers ci ON c.id = ci.contact_id
		WHERE c.is_me = 1
		ORDER BY c.id
	`)
	if err != nil {
		return 0, "", fmt.Errorf("failed to query Eve whoami: %w", err)
	}
	defer rows.Close()

	var (
		bestName        string
		identifiersSeen bool
	)

	type ident struct {
		channel    string
		identifier string
	}
	var idents []ident

	for rows.Next() {
		var name, nickname, identifier, identifierType sql.NullString
		if err := rows.Scan(&name, &nickname, &identifier, &identifierType); err != nil {
			return 0, "", fmt.Errorf("failed to scan Eve whoami row: %w", err)
		}

		// Determine best canonical name candidate.
		if bestName == "" {
			if name.Valid && name.String != "" {
				bestName = name.String
			} else if nickname.Valid && nickname.String != "" {
				bestName = nickname.String
			}
		}

		if identifier.Valid && identifierType.Valid && identifier.String != "" && identifierType.String != "" {
			identifiersSeen = true
			idents = append(idents, ident{
				channel:    identifierType.String,
				identifier: identifier.String,
			})
		}
	}
	if err := rows.Err(); err != nil {
		return 0, "", fmt.Errorf("error iterating Eve whoami: %w", err)
	}

	// If Eve has no whoami rows, do nothing.
	if bestName == "" && !identifiersSeen {
		return 0, "", nil
	}
	if bestName == "" {
		bestName = "Me"
	}

	now := time.Now().Unix()
	if mePersonID == "" {
		mePersonID = uuid.New().String()
		if _, err := cortexDB.Exec(`
			INSERT INTO persons (id, canonical_name, is_me, created_at, updated_at)
			VALUES (?, ?, 1, ?, ?)
		`, mePersonID, bestName, now, now); err != nil {
			return 0, "", fmt.Errorf("failed to create me person: %w", err)
		}
		personsCreated++
	} else {
		// Best-effort: keep canonical_name fresh if it was a placeholder.
		_, _ = cortexDB.Exec(`UPDATE persons SET canonical_name = ?, updated_at = ? WHERE id = ? AND (canonical_name = '' OR canonical_name = 'Me' OR canonical_name = 'Unknown')`,
			bestName, now, mePersonID,
		)
	}

	// Upsert all whoami identifiers onto the cortex me person.
	for _, it := range idents {
		identityID := uuid.New().String()
		_, err := cortexDB.Exec(`
			INSERT INTO identities (id, person_id, channel, identifier, created_at)
			VALUES (?, ?, ?, ?, ?)
			ON CONFLICT(channel, identifier) DO UPDATE SET person_id = excluded.person_id
		`, identityID, mePersonID, it.channel, it.identifier, now)
		if err != nil {
			return personsCreated, mePersonID, fmt.Errorf("failed to upsert whoami identity (%s:%s): %w", it.channel, it.identifier, err)
		}
	}

	return personsCreated, mePersonID, nil
}

// syncChats syncs Eve chats to cortex threads
func (e *EveAdapter) syncChats(ctx context.Context, eveDB, cortexDB *sql.DB) (threadsCreated int, threadsUpdated int, perf map[string]string, err error) {
	_ = ctx
	perf = map[string]string{}

	// Query chats from Eve
	qStart := time.Now()
	rows, err := eveDB.Query(`
		SELECT
			c.id,
			c.chat_identifier,
			c.chat_name,
			c.service_name
		FROM chats c
		ORDER BY c.id
	`)
	if err != nil {
		return 0, 0, perf, fmt.Errorf("failed to query Eve chats: %w", err)
	}
	defer rows.Close()
	perf["query"] = time.Since(qStart).String()

	// Bulk write in a single transaction for SQLite performance
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

	for rows.Next() {
		var chatID int64
		var chatIdentifier string
		var chatName, serviceName sql.NullString

		if err := rows.Scan(&chatID, &chatIdentifier, &chatName, &serviceName); err != nil {
			return threadsCreated, threadsUpdated, perf, fmt.Errorf("failed to scan chat row: %w", err)
		}

		// Determine thread name: prefer chat_name, fall back to chat_identifier
		threadName := chatIdentifier
		if chatName.Valid && chatName.String != "" {
			threadName = chatName.String
		}

		// Generate deterministic thread ID from chat_identifier
		threadID := e.Name() + ":" + chatIdentifier

		now := time.Now().Unix()

		// Try to insert, or update if exists
		res, err := stmtInsertThread.Exec(
			threadID,
			"imessage",
			threadName,
			e.Name(),
			chatIdentifier,
			now,
			now,
		)
		if err != nil {
			return threadsCreated, threadsUpdated, perf, fmt.Errorf("upsert thread: %w", err)
		}

		// Check if this was an insert or update
		// SQLite returns rows affected = 1 for both INSERT and UPDATE with ON CONFLICT
		// We need to check if the thread existed before to distinguish
		var exists int
		err = tx.QueryRow("SELECT 1 FROM threads WHERE source_adapter = ? AND source_id = ? AND updated_at < ?",
			e.Name(), chatIdentifier, now).Scan(&exists)
		if err == sql.ErrNoRows {
			// Thread was just created
			threadsCreated++
		} else if err == nil {
			// Thread existed and was updated
			threadsUpdated++
		}
		// Ignore other errors, just count based on RowsAffected
		if err != nil && err != sql.ErrNoRows {
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

// syncMessages syncs Eve messages to cortex events
func (e *EveAdapter) syncMessages(ctx context.Context, eveDB, cortexDB *sql.DB, lastSyncTimestamp int64, contactMap map[int64]string, mePersonID string) (created int, updated int, maxImportedTimestamp int64, perf map[string]string, err error) {
	_ = ctx
	perf = map[string]string{}

	adapterPrefix := e.Name() + ":"
	const contentTypesText = "[\"text\"]"
	const contentTypesAttachment = "[\"attachment\"]"
	const contentTypesTextAttachment = "[\"text\",\"attachment\"]"

	// Query messages from Eve
	// Note: thread_id is prefixed with adapter name to match threads.id format
	query := `
		SELECT
			m.id,
			m.guid,
			m.chat_id,
			m.sender_id,
			m.content,
			CAST(strftime('%s', m.timestamp) AS INTEGER) as timestamp_unix,
			m.is_from_me,
			m.service_name,
			m.reply_to_guid,
			'imessage:' || COALESCE(c.chat_identifier, printf('chat_id:%d', m.chat_id)) as thread_id,
			(SELECT COUNT(*) FROM attachments a WHERE a.message_id = m.id) as attachment_count
		FROM messages m
		LEFT JOIN chats c ON m.chat_id = c.id
		WHERE CAST(strftime('%s', m.timestamp) AS INTEGER) > ?
		ORDER BY timestamp_unix ASC
	`

	qStart := time.Now()
	rows, err := eveDB.Query(query, lastSyncTimestamp)
	if err != nil {
		return 0, 0, 0, perf, fmt.Errorf("failed to query Eve messages: %w", err)
	}
	defer rows.Close()
	perf["query"] = time.Since(qStart).String()

	// Bulk write in a single transaction for SQLite performance.
	txStart := time.Now()
	tx, err := cortexDB.Begin()
	if err != nil {
		return 0, 0, 0, perf, fmt.Errorf("begin cortex tx: %w", err)
	}
	defer tx.Rollback()

	stmtInsertEvent, err := tx.Prepare(`
		INSERT OR IGNORE INTO events (
			id, timestamp, channel, content_types, content,
			direction, thread_id, reply_to, source_adapter, source_id
		) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
	`)
	if err != nil {
		return 0, 0, 0, perf, fmt.Errorf("prepare insert event: %w", err)
	}
	defer stmtInsertEvent.Close()

	stmtUpdateEvent, err := tx.Prepare(`
		UPDATE events
		SET
			content = ?,
			content_types = ?,
			thread_id = ?,
			reply_to = ?
		WHERE source_adapter = ?
		  AND source_id = ?
		  AND (
		    content IS NOT ?
		    OR content_types IS NOT ?
		    OR thread_id IS NOT ?
		    OR reply_to IS NOT ?
		  )
	`)
	if err != nil {
		return 0, 0, 0, perf, fmt.Errorf("prepare update event: %w", err)
	}
	defer stmtUpdateEvent.Close()

	stmtInsertParticipant, err := tx.Prepare(`
		INSERT OR IGNORE INTO event_participants (event_id, person_id, role)
		VALUES (?, ?, ?)
	`)
	if err != nil {
		return 0, 0, 0, perf, fmt.Errorf("prepare insert participant: %w", err)
	}
	defer stmtInsertParticipant.Close()

	for rows.Next() {
		var messageID int64
		var guid, threadID string
		var chatID, senderID sql.NullInt64
		var content, serviceName, replyToGuid sql.NullString
		var timestamp int64
		var isFromMe bool
		var attachmentCount int

		if err := rows.Scan(&messageID, &guid, &chatID, &senderID, &content, &timestamp, &isFromMe, &serviceName, &replyToGuid, &threadID, &attachmentCount); err != nil {
			return created, updated, maxImportedTimestamp, perf, fmt.Errorf("failed to scan message row: %w", err)
		}

		if timestamp > maxImportedTimestamp {
			maxImportedTimestamp = timestamp
		}

		// Build content types JSON without per-row marshaling.
		contentTypesJSON := contentTypesText
		hasText := content.Valid && content.String != ""
		hasAttachment := attachmentCount > 0
		switch {
		case hasText && hasAttachment:
			contentTypesJSON = contentTypesTextAttachment
		case hasAttachment:
			contentTypesJSON = contentTypesAttachment
		default:
			contentTypesJSON = contentTypesText
		}

		// Determine direction
		direction := "received"
		if isFromMe {
			direction = "sent"
		}

		// Deterministic event ID to avoid UUID cost and extra lookups.
		eventID := adapterPrefix + guid

		res, err := stmtInsertEvent.Exec(
			eventID, timestamp, "imessage", contentTypesJSON, content.String,
			direction, threadID, replyToGuid.String, e.Name(), guid,
		)
		if err != nil {
			return created, updated, maxImportedTimestamp, perf, fmt.Errorf("insert event: %w", err)
		}
		if n, _ := res.RowsAffected(); n == 1 {
			created++
		} else {
			res2, err := stmtUpdateEvent.Exec(
				content.String, contentTypesJSON, threadID, replyToGuid.String,
				e.Name(), guid,
				content.String, contentTypesJSON, threadID, replyToGuid.String,
			)
			if err != nil {
				return created, updated, maxImportedTimestamp, perf, fmt.Errorf("update event: %w", err)
			}
			if n2, _ := res2.RowsAffected(); n2 == 1 {
				updated++
			}
		}

		// Participants: use in-memory contactMap from syncContacts to avoid per-message DB lookups.
		if senderID.Valid {
			if pid, ok := contactMap[senderID.Int64]; ok && pid != "" {
				role := "sender"
				if isFromMe {
					role = "recipient"
				}
				_, _ = stmtInsertParticipant.Exec(eventID, pid, role)
			}
		}
		if isFromMe && mePersonID != "" {
			_, _ = stmtInsertParticipant.Exec(eventID, mePersonID, "sender")
		}
	}

	if err := rows.Err(); err != nil {
		return created, updated, maxImportedTimestamp, perf, err
	}
	if err := tx.Commit(); err != nil {
		return created, updated, maxImportedTimestamp, perf, fmt.Errorf("commit cortex tx: %w", err)
	}
	perf["tx_commit"] = time.Since(txStart).String()
	return created, updated, maxImportedTimestamp, perf, nil
}

// syncAttachments syncs Eve attachments to cortex attachments table
func (e *EveAdapter) syncAttachments(ctx context.Context, eveDB, cortexDB *sql.DB, lastSyncTimestamp int64) (created int, updated int, perf map[string]string, err error) {
	_ = ctx
	perf = map[string]string{}

	adapterPrefix := e.Name() + ":"

	// Query attachments from Eve, joining with messages to get timestamp for incremental sync
	query := `
		SELECT
			a.id,
			a.guid,
			a.message_id,
			a.file_name,
			a.mime_type,
			a.size,
			a.is_sticker,
			a.uti,
			CAST(strftime('%s', a.created_date) AS INTEGER) as created_unix,
			m.guid as message_guid
		FROM attachments a
		JOIN messages m ON a.message_id = m.id
		WHERE CAST(strftime('%s', m.timestamp) AS INTEGER) > ?
		ORDER BY a.id ASC
	`

	qStart := time.Now()
	rows, err := eveDB.Query(query, lastSyncTimestamp)
	if err != nil {
		return 0, 0, perf, fmt.Errorf("failed to query Eve attachments: %w", err)
	}
	defer rows.Close()
	perf["query"] = time.Since(qStart).String()

	// Bulk write in a single transaction for SQLite performance
	txStart := time.Now()
	tx, err := cortexDB.Begin()
	if err != nil {
		return 0, 0, perf, fmt.Errorf("begin cortex tx: %w", err)
	}
	defer tx.Rollback()

	stmtInsertAttachment, err := tx.Prepare(`
		INSERT INTO attachments (
			id, event_id, filename, mime_type, size_bytes,
			media_type, storage_uri, storage_type, content_hash,
			source_id, metadata_json, created_at
		) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
		ON CONFLICT(id) DO UPDATE SET
			filename = excluded.filename,
			mime_type = excluded.mime_type,
			size_bytes = excluded.size_bytes,
			media_type = excluded.media_type,
			storage_uri = excluded.storage_uri
	`)
	if err != nil {
		return 0, 0, perf, fmt.Errorf("prepare insert attachment: %w", err)
	}
	defer stmtInsertAttachment.Close()

	for rows.Next() {
		var attachmentID int64
		var guid string
		var messageID int64
		var fileName, mimeType, uti, messageGuid sql.NullString
		var size sql.NullInt64
		var isSticker bool
		var createdUnix int64

		if err := rows.Scan(&attachmentID, &guid, &messageID, &fileName, &mimeType, &size, &isSticker, &uti, &createdUnix, &messageGuid); err != nil {
			return created, updated, perf, fmt.Errorf("failed to scan attachment row: %w", err)
		}

		// Build cortex event ID from message GUID
		eventID := adapterPrefix + messageGuid.String

		// Derive media_type from mime_type and is_sticker flag
		mediaType := deriveMediaType(mimeType.String, isSticker)

		// Build storage_uri - for now, we don't have the actual file path from Eve
		// Store the attachment GUID as reference
		storageURI := ""
		if fileName.Valid && fileName.String != "" {
			// If we had the actual path, we'd use file:// URI scheme
			// For now, store a placeholder that indicates the source
			storageURI = "eve://" + guid
		}

		// Build metadata_json with additional fields
		metadataJSON := ""
		if uti.Valid && uti.String != "" {
			metadataJSON = fmt.Sprintf(`{"uti":"%s","is_sticker":%v}`, uti.String, isSticker)
		} else {
			metadataJSON = fmt.Sprintf(`{"is_sticker":%v}`, isSticker)
		}

		// Deterministic attachment ID
		attachmentCommsID := adapterPrefix + guid

		// Check if attachment already exists to determine created vs updated
		var existingID string
		err := tx.QueryRow("SELECT id FROM attachments WHERE id = ?", attachmentCommsID).Scan(&existingID)
		wasCreated := (err == sql.ErrNoRows)

		// Insert or update attachment
		_, err = stmtInsertAttachment.Exec(
			attachmentCommsID,
			eventID,
			fileName.String,
			mimeType.String,
			size.Int64,
			mediaType,
			storageURI,
			"local", // storage_type
			"",      // content_hash (not available from Eve)
			guid,    // source_id
			metadataJSON,
			createdUnix,
		)
		if err != nil {
			return created, updated, perf, fmt.Errorf("upsert attachment: %w", err)
		}

		if wasCreated {
			created++
		} else {
			updated++
		}
	}

	if err := rows.Err(); err != nil {
		return created, updated, perf, err
	}
	if err := tx.Commit(); err != nil {
		return created, updated, perf, fmt.Errorf("commit cortex tx: %w", err)
	}
	perf["tx_commit"] = time.Since(txStart).String()
	return created, updated, perf, nil
}

// syncReactions syncs Eve reactions to cortex events
func (e *EveAdapter) syncReactions(ctx context.Context, eveDB, cortexDB *sql.DB, lastSyncTimestamp int64, contactMap map[int64]string, mePersonID string) (created int, updated int, perf map[string]string, err error) {
	_ = ctx
	perf = map[string]string{}

	adapterPrefix := e.Name() + ":"
	const contentTypesReaction = "[\"reaction\"]"

	// Query reactions from Eve, joining with messages to get timestamp for incremental sync
	query := `
		SELECT
			r.id,
			r.guid,
			r.original_message_guid,
			r.sender_id,
			r.chat_id,
			r.reaction_type,
			r.is_from_me,
			CAST(strftime('%s', r.timestamp) AS INTEGER) as timestamp_unix,
			'imessage:' || COALESCE(c.chat_identifier, printf('chat_id:%d', r.chat_id)) as thread_id
		FROM reactions r
		LEFT JOIN chats c ON r.chat_id = c.id
		WHERE CAST(strftime('%s', r.timestamp) AS INTEGER) > ?
		ORDER BY timestamp_unix ASC
	`

	qStart := time.Now()
	rows, err := eveDB.Query(query, lastSyncTimestamp)
	if err != nil {
		return 0, 0, perf, fmt.Errorf("failed to query Eve reactions: %w", err)
	}
	defer rows.Close()
	perf["query"] = time.Since(qStart).String()

	// Bulk write in a single transaction for SQLite performance
	txStart := time.Now()
	tx, err := cortexDB.Begin()
	if err != nil {
		return 0, 0, perf, fmt.Errorf("begin cortex tx: %w", err)
	}
	defer tx.Rollback()

	stmtInsertEvent, err := tx.Prepare(`
		INSERT OR IGNORE INTO events (
			id, timestamp, channel, content_types, content,
			direction, thread_id, reply_to, source_adapter, source_id
		) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
	`)
	if err != nil {
		return 0, 0, perf, fmt.Errorf("prepare insert event: %w", err)
	}
	defer stmtInsertEvent.Close()

	stmtUpdateEvent, err := tx.Prepare(`
		UPDATE events
		SET
			content = ?,
			content_types = ?,
			thread_id = ?,
			reply_to = ?
		WHERE source_adapter = ?
		  AND source_id = ?
		  AND (
		    content IS NOT ?
		    OR content_types IS NOT ?
		    OR thread_id IS NOT ?
		    OR reply_to IS NOT ?
		  )
	`)
	if err != nil {
		return 0, 0, perf, fmt.Errorf("prepare update event: %w", err)
	}
	defer stmtUpdateEvent.Close()

	stmtInsertParticipant, err := tx.Prepare(`
		INSERT OR IGNORE INTO event_participants (event_id, person_id, role)
		VALUES (?, ?, ?)
	`)
	if err != nil {
		return 0, 0, perf, fmt.Errorf("prepare insert participant: %w", err)
	}
	defer stmtInsertParticipant.Close()

	for rows.Next() {
		var reactionID int64
		var guid, originalMessageGuid, threadID string
		var chatID, senderID sql.NullInt64
		var reactionType sql.NullInt64
		var timestamp int64
		var isFromMe bool

		if err := rows.Scan(&reactionID, &guid, &originalMessageGuid, &senderID, &chatID, &reactionType, &isFromMe, &timestamp, &threadID); err != nil {
			return created, updated, perf, fmt.Errorf("failed to scan reaction row: %w", err)
		}

		// Map reaction_type integer to emoji
		// iMessage reaction types: 2000=love, 2001=like, 2002=dislike, 2003=laugh, 2004=emphasis, 2005=question
		reactionContent := mapReactionType(reactionType.Int64)

		// Determine direction
		direction := "received"
		if isFromMe {
			direction = "sent"
		}

		// Build reply_to: reference to the original message
		replyTo := adapterPrefix + originalMessageGuid

		// Deterministic event ID to avoid UUID cost and extra lookups
		eventID := adapterPrefix + guid

		res, err := stmtInsertEvent.Exec(
			eventID, timestamp, "imessage", contentTypesReaction, reactionContent,
			direction, threadID, replyTo, e.Name(), guid,
		)
		if err != nil {
			return created, updated, perf, fmt.Errorf("insert reaction event: %w", err)
		}
		if n, _ := res.RowsAffected(); n == 1 {
			created++
		} else {
			res2, err := stmtUpdateEvent.Exec(
				reactionContent, contentTypesReaction, threadID, replyTo,
				e.Name(), guid,
				reactionContent, contentTypesReaction, threadID, replyTo,
			)
			if err != nil {
				return created, updated, perf, fmt.Errorf("update reaction event: %w", err)
			}
			if n2, _ := res2.RowsAffected(); n2 == 1 {
				updated++
			}
		}

		// Participants: use in-memory contactMap from syncContacts to avoid per-reaction DB lookups
		if senderID.Valid {
			if pid, ok := contactMap[senderID.Int64]; ok && pid != "" {
				_, _ = stmtInsertParticipant.Exec(eventID, pid, "sender")
			}
		}
		if isFromMe && mePersonID != "" {
			_, _ = stmtInsertParticipant.Exec(eventID, mePersonID, "sender")
		}
	}

	if err := rows.Err(); err != nil {
		return created, updated, perf, err
	}
	if err := tx.Commit(); err != nil {
		return created, updated, perf, fmt.Errorf("commit cortex tx: %w", err)
	}
	perf["tx_commit"] = time.Since(txStart).String()
	return created, updated, perf, nil
}

// mapReactionType converts iMessage reaction_type integer to emoji
func mapReactionType(reactionType int64) string {
	switch reactionType {
	case 2000:
		return "❤️" // love
	case 2001:
		return "👍" // like
	case 2002:
		return "👎" // dislike
	case 2003:
		return "😂" // laugh
	case 2004:
		return "‼️" // emphasis
	case 2005:
		return "❓" // question
	default:
		return fmt.Sprintf("reaction:%d", reactionType) // fallback for unknown types
	}
}

// deriveMediaType determines the media_type category from mime_type
func deriveMediaType(mimeType string, isSticker bool) string {
	if isSticker {
		return "sticker"
	}

	mimeType = strings.ToLower(mimeType)

	// Image types
	if strings.HasPrefix(mimeType, "image/") {
		return "image"
	}

	// Video types
	if strings.HasPrefix(mimeType, "video/") {
		return "video"
	}

	// Audio types
	if strings.HasPrefix(mimeType, "audio/") {
		return "audio"
	}

	// Document types
	if strings.HasPrefix(mimeType, "application/pdf") ||
		strings.HasPrefix(mimeType, "application/msword") ||
		strings.HasPrefix(mimeType, "application/vnd.openxmlformats-officedocument") ||
		strings.HasPrefix(mimeType, "application/vnd.ms-") ||
		strings.HasPrefix(mimeType, "text/") {
		return "document"
	}

	// Default to document for unknown types
	return "document"
}
