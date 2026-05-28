package db

import (
	"crypto/sha256"
	"database/sql"
	"embed"
	"encoding/binary"
	"encoding/json"
	"fmt"
	"math"
	"os"
	"path/filepath"
	"runtime"
	"strings"
	"sync"
	"time"

	_ "github.com/mattn/go-sqlite3"

	"github.com/Napageneral/aix/internal/models"
)

//go:embed schema.sql
var schemaFS embed.FS

// DB wraps the SQLite database connection
type DB struct {
	conn *sql.DB
	path string
}

// Conn exposes the underlying sql.DB for advanced use (e.g. taskengine).
func (db *DB) Conn() *sql.DB {
	return db.conn
}

// Open opens or creates the database at the default location
func Open() (*DB, error) {
	path := DefaultDBPath()
	return OpenPath(path)
}

// OpenPath opens or creates the database at the specified path
func OpenPath(path string) (*DB, error) {
	// Ensure directory exists
	if err := os.MkdirAll(filepath.Dir(path), 0755); err != nil {
		return nil, fmt.Errorf("failed to create data directory: %w", err)
	}

	conn, err := sql.Open("sqlite3", path+"?_journal_mode=WAL&_foreign_keys=on")
	if err != nil {
		return nil, fmt.Errorf("failed to open database: %w", err)
	}

	db := &DB{conn: conn, path: path}

	// Initialize schema
	if err := db.initSchema(); err != nil {
		conn.Close()
		return nil, fmt.Errorf("failed to initialize schema: %w", err)
	}

	return db, nil
}

// DefaultDBPath returns the default database path based on OS
func DefaultDBPath() string {
	if xdg := os.Getenv("XDG_DATA_HOME"); xdg != "" {
		return filepath.Join(xdg, "aix", "aix.db")
	}
	home, _ := os.UserHomeDir()
	if runtime.GOOS == "darwin" {
		return filepath.Join(home, "Library", "Application Support", "aix", "aix.db")
	}
	return filepath.Join(home, ".local", "share", "aix", "aix.db")
}

// Close closes the database connection
func (db *DB) Close() error {
	return db.conn.Close()
}

// Begin starts a new transaction
func (db *DB) Begin() (*sql.Tx, error) {
	return db.conn.Begin()
}

// TxBatch provides transaction-aware batch operations for high-performance bulk imports
type TxBatch struct {
	conn                 *sql.DB
	pragmaState          *bulkPragmaState
	restoreOnce          sync.Once
	tx                   *sql.Tx
	stmtUpsertSession    *sql.Stmt
	stmtInsertMessage    *sql.Stmt
	stmtInsertMetadata   *sql.Stmt
	stmtInsertCapability *sql.Stmt
	stmtInsertLint       *sql.Stmt
	stmtInsertMsgFile    *sql.Stmt
	stmtInsertCodeblock  *sql.Stmt
	stmtInsertFileRef    *sql.Stmt
	stmtDeleteMessages   *sql.Stmt
	stmtDeleteMetadata   *sql.Stmt
	stmtDeleteCaps       *sql.Stmt
	stmtDeleteLints      *sql.Stmt
	stmtDeleteMsgFiles   *sql.Stmt
	stmtDeleteCodeblocks *sql.Stmt
	stmtDeleteFiles      *sql.Stmt
}

type bulkPragmaState struct {
	synchronous    int64
	foreignKeys    int64
	tempStore      int64
	cacheSize      int64
	mmapSize       int64
	walCheckpoint  int64
	busyTimeout    int64
	journalMode    string
}

func readPragmaInt(db *sql.DB, name string) (int64, error) {
	var v sql.NullInt64
	if err := db.QueryRow("PRAGMA "+name).Scan(&v); err != nil {
		return 0, err
	}
	return v.Int64, nil
}

func readPragmaText(db *sql.DB, name string) (string, error) {
	var v sql.NullString
	if err := db.QueryRow("PRAGMA "+name).Scan(&v); err != nil {
		return "", err
	}
	return v.String, nil
}

func captureBulkPragmaState(db *sql.DB) *bulkPragmaState {
	st := &bulkPragmaState{}
	if v, err := readPragmaInt(db, "synchronous"); err == nil {
		st.synchronous = v
	}
	if v, err := readPragmaInt(db, "foreign_keys"); err == nil {
		st.foreignKeys = v
	}
	if v, err := readPragmaInt(db, "temp_store"); err == nil {
		st.tempStore = v
	}
	if v, err := readPragmaInt(db, "cache_size"); err == nil {
		st.cacheSize = v
	}
	if v, err := readPragmaInt(db, "mmap_size"); err == nil {
		st.mmapSize = v
	}
	if v, err := readPragmaInt(db, "wal_autocheckpoint"); err == nil {
		st.walCheckpoint = v
	}
	if v, err := readPragmaInt(db, "busy_timeout"); err == nil {
		st.busyTimeout = v
	}
	if v, err := readPragmaText(db, "journal_mode"); err == nil {
		st.journalMode = v
	}
	return st
}

func applyBulkImportPragmas(db *sql.DB) {
	// We prefer speed over durability during import; WAL still gives good safety.
	// We restore previous values after commit/rollback.
	_, _ = db.Exec("PRAGMA foreign_keys = OFF")
	_, _ = db.Exec("PRAGMA synchronous = OFF")
	_, _ = db.Exec("PRAGMA temp_store = MEMORY")
	_, _ = db.Exec("PRAGMA cache_size = -200000")        // ~200MB page cache
	_, _ = db.Exec("PRAGMA mmap_size = 268435456")       // 256MB mmap
	_, _ = db.Exec("PRAGMA wal_autocheckpoint = 0")      // avoid checkpoint work during import
	_, _ = db.Exec("PRAGMA busy_timeout = 5000")         // reduce transient lock errors
	_, _ = db.Exec("PRAGMA journal_mode = WAL")          // ensure WAL
}

func restoreBulkImportPragmas(db *sql.DB, st *bulkPragmaState) {
	if st == nil {
		return
	}
	if st.journalMode != "" {
		_, _ = db.Exec("PRAGMA journal_mode = " + st.journalMode)
	}
	_, _ = db.Exec(fmt.Sprintf("PRAGMA busy_timeout = %d", st.busyTimeout))
	_, _ = db.Exec(fmt.Sprintf("PRAGMA wal_autocheckpoint = %d", st.walCheckpoint))
	_, _ = db.Exec(fmt.Sprintf("PRAGMA mmap_size = %d", st.mmapSize))
	_, _ = db.Exec(fmt.Sprintf("PRAGMA cache_size = %d", st.cacheSize))
	_, _ = db.Exec(fmt.Sprintf("PRAGMA temp_store = %d", st.tempStore))
	_, _ = db.Exec(fmt.Sprintf("PRAGMA synchronous = %d", st.synchronous))
	_, _ = db.Exec(fmt.Sprintf("PRAGMA foreign_keys = %d", st.foreignKeys))
}

// GetSessionHashes returns a map of session ID -> SHA256 hash of raw_json for a given source
// Used for incremental sync to detect unchanged sessions
func (db *DB) GetSessionHashes(source string) (map[string]string, error) {
	rows, err := db.conn.Query(`
		SELECT id, raw_json FROM sessions WHERE source = ?
	`, source)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	hashes := make(map[string]string)
	for rows.Next() {
		var id string
		var rawJSON sql.NullString
		if err := rows.Scan(&id, &rawJSON); err != nil {
			continue
		}
		if rawJSON.Valid && rawJSON.String != "" {
			// Use first 16 chars of SHA256 as quick hash
			h := sha256.Sum256([]byte(rawJSON.String))
			hashes[id] = fmt.Sprintf("%x", h[:8])
		}
	}
	return hashes, rows.Err()
}

// DeleteSessionData deletes all data for specific session IDs
func (db *DB) DeleteSessionDataByIDs(sessionIDs []string) error {
	if len(sessionIDs) == 0 {
		return nil
	}

	// Build placeholder string
	placeholders := make([]string, len(sessionIDs))
	args := make([]interface{}, len(sessionIDs))
	for i, id := range sessionIDs {
		placeholders[i] = "?"
		args[i] = id
	}
	inClause := strings.Join(placeholders, ",")

	// Delete in FK order
	queries := []string{
		"DELETE FROM message_metadata WHERE session_id IN (" + inClause + ")",
		"DELETE FROM message_capabilities WHERE session_id IN (" + inClause + ")",
		"DELETE FROM message_lints WHERE session_id IN (" + inClause + ")",
		"DELETE FROM message_files WHERE session_id IN (" + inClause + ")",
		"DELETE FROM message_codeblocks WHERE session_id IN (" + inClause + ")",
		"DELETE FROM messages WHERE session_id IN (" + inClause + ")",
		"DELETE FROM files_referenced WHERE session_id IN (" + inClause + ")",
	}

	for _, q := range queries {
		if _, err := db.conn.Exec(q, args...); err != nil {
			return err
		}
	}
	return nil
}

// DeleteAllSourceData deletes all messages and related data for sessions from a given source
func (db *DB) DeleteAllSourceData(source string) error {
	// Delete in FK order
	_, err := db.conn.Exec(`DELETE FROM message_metadata WHERE session_id IN (SELECT id FROM sessions WHERE source = ?)`, source)
	if err != nil {
		return err
	}
	_, err = db.conn.Exec(`DELETE FROM message_capabilities WHERE session_id IN (SELECT id FROM sessions WHERE source = ?)`, source)
	if err != nil {
		return err
	}
	_, err = db.conn.Exec(`DELETE FROM message_lints WHERE session_id IN (SELECT id FROM sessions WHERE source = ?)`, source)
	if err != nil {
		return err
	}
	_, err = db.conn.Exec(`DELETE FROM message_files WHERE session_id IN (SELECT id FROM sessions WHERE source = ?)`, source)
	if err != nil {
		return err
	}
	_, err = db.conn.Exec(`DELETE FROM message_codeblocks WHERE session_id IN (SELECT id FROM sessions WHERE source = ?)`, source)
	if err != nil {
		return err
	}
	_, err = db.conn.Exec(`DELETE FROM messages WHERE session_id IN (SELECT id FROM sessions WHERE source = ?)`, source)
	if err != nil {
		return err
	}
	_, err = db.conn.Exec(`DELETE FROM files_referenced WHERE session_id IN (SELECT id FROM sessions WHERE source = ?)`, source)
	if err != nil {
		return err
	}
	return nil
}

// BeginBatch starts a new transaction batch for high-performance bulk imports
func (db *DB) BeginBatch() (*TxBatch, error) {
	// Bulk import mode pragmas (restored after commit/rollback)
	st := captureBulkPragmaState(db.conn)
	applyBulkImportPragmas(db.conn)

	tx, err := db.conn.Begin()
	if err != nil {
		return nil, err
	}

	batch := &TxBatch{conn: db.conn, pragmaState: st, tx: tx}

	// Prepare all statements for reuse
	batch.stmtUpsertSession, err = tx.Prepare(`
		INSERT INTO sessions (id, source, project, model, created_at, message_count, summary, raw_json)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?)
		ON CONFLICT(id) DO UPDATE SET
			source = excluded.source,
			project = excluded.project,
			model = excluded.model,
			created_at = excluded.created_at,
			message_count = excluded.message_count,
			summary = excluded.summary,
			raw_json = excluded.raw_json`)
	if err != nil {
		tx.Rollback()
		return nil, fmt.Errorf("prepare upsert session: %w", err)
	}

	batch.stmtInsertMessage, err = tx.Prepare(`
		INSERT OR REPLACE INTO messages (id, session_id, role, content, sequence, timestamp)
		VALUES (?, ?, ?, ?, ?, ?)`)
	if err != nil {
		tx.Rollback()
		return nil, fmt.Errorf("prepare insert message: %w", err)
	}

	batch.stmtInsertMetadata, err = tx.Prepare(`
		INSERT OR REPLACE INTO message_metadata (message_id, session_id, metadata_json)
		VALUES (?, ?, ?)`)
	if err != nil {
		tx.Rollback()
		return nil, fmt.Errorf("prepare insert metadata: %w", err)
	}

	batch.stmtInsertCapability, err = tx.Prepare(`
		INSERT OR IGNORE INTO message_capabilities (message_id, session_id, phase, capability)
		VALUES (?, ?, ?, ?)`)
	if err != nil {
		tx.Rollback()
		return nil, fmt.Errorf("prepare insert capability: %w", err)
	}

	batch.stmtInsertLint, err = tx.Prepare(`
		INSERT OR IGNORE INTO message_lints (message_id, session_id, file_path, message, source, start_line, start_col, end_line, end_col)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`)
	if err != nil {
		tx.Rollback()
		return nil, fmt.Errorf("prepare insert lint: %w", err)
	}

	batch.stmtInsertMsgFile, err = tx.Prepare(`
		INSERT OR IGNORE INTO message_files (message_id, session_id, kind, file_path, line_number)
		VALUES (?, ?, ?, ?, ?)`)
	if err != nil {
		tx.Rollback()
		return nil, fmt.Errorf("prepare insert msg file: %w", err)
	}

	batch.stmtInsertCodeblock, err = tx.Prepare(`
		INSERT OR IGNORE INTO message_codeblocks (message_id, session_id, idx, raw_json)
		VALUES (?, ?, ?, ?)`)
	if err != nil {
		tx.Rollback()
		return nil, fmt.Errorf("prepare insert codeblock: %w", err)
	}

	batch.stmtInsertFileRef, err = tx.Prepare(`
		INSERT OR IGNORE INTO files_referenced (session_id, file_path)
		VALUES (?, ?)`)
	if err != nil {
		tx.Rollback()
		return nil, fmt.Errorf("prepare insert file ref: %w", err)
	}

	// Delete statements
	batch.stmtDeleteMessages, err = tx.Prepare(`DELETE FROM messages WHERE session_id = ?`)
	if err != nil {
		tx.Rollback()
		return nil, fmt.Errorf("prepare delete messages: %w", err)
	}

	batch.stmtDeleteMetadata, err = tx.Prepare(`DELETE FROM message_metadata WHERE session_id = ?`)
	if err != nil {
		tx.Rollback()
		return nil, fmt.Errorf("prepare delete metadata: %w", err)
	}

	batch.stmtDeleteCaps, err = tx.Prepare(`DELETE FROM message_capabilities WHERE session_id = ?`)
	if err != nil {
		tx.Rollback()
		return nil, fmt.Errorf("prepare delete caps: %w", err)
	}

	batch.stmtDeleteLints, err = tx.Prepare(`DELETE FROM message_lints WHERE session_id = ?`)
	if err != nil {
		tx.Rollback()
		return nil, fmt.Errorf("prepare delete lints: %w", err)
	}

	batch.stmtDeleteMsgFiles, err = tx.Prepare(`DELETE FROM message_files WHERE session_id = ?`)
	if err != nil {
		tx.Rollback()
		return nil, fmt.Errorf("prepare delete msg files: %w", err)
	}

	batch.stmtDeleteCodeblocks, err = tx.Prepare(`DELETE FROM message_codeblocks WHERE session_id = ?`)
	if err != nil {
		tx.Rollback()
		return nil, fmt.Errorf("prepare delete codeblocks: %w", err)
	}

	batch.stmtDeleteFiles, err = tx.Prepare(`DELETE FROM files_referenced WHERE session_id = ?`)
	if err != nil {
		tx.Rollback()
		return nil, fmt.Errorf("prepare delete files: %w", err)
	}

	return batch, nil
}

// UpsertSession upserts a session within the batch transaction
func (b *TxBatch) UpsertSession(s *models.Session, rawJSON string) error {
	_, err := b.stmtUpsertSession.Exec(s.ID, s.Source, s.Project, s.Model, s.CreatedAt, s.MessageCount, s.Summary, rawJSON)
	return err
}

// DeleteSessionData deletes all data for a session within the batch transaction
func (b *TxBatch) DeleteSessionData(sessionID string) error {
	// Delete in order to respect FK constraints (metadata tables first)
	if _, err := b.stmtDeleteMetadata.Exec(sessionID); err != nil {
		return err
	}
	if _, err := b.stmtDeleteCaps.Exec(sessionID); err != nil {
		return err
	}
	if _, err := b.stmtDeleteLints.Exec(sessionID); err != nil {
		return err
	}
	if _, err := b.stmtDeleteMsgFiles.Exec(sessionID); err != nil {
		return err
	}
	if _, err := b.stmtDeleteCodeblocks.Exec(sessionID); err != nil {
		return err
	}
	if _, err := b.stmtDeleteMessages.Exec(sessionID); err != nil {
		return err
	}
	if _, err := b.stmtDeleteFiles.Exec(sessionID); err != nil {
		return err
	}
	return nil
}

// InsertMessage inserts a message within the batch transaction
func (b *TxBatch) InsertMessage(m *models.Message) error {
	_, err := b.stmtInsertMessage.Exec(m.ID, m.SessionID, m.Role, m.Content, m.Sequence, m.Timestamp)
	return err
}

// InsertMessagesBulk inserts multiple messages in a single SQL statement (much faster)
func (b *TxBatch) InsertMessagesBulk(messages []models.Message) error {
	if len(messages) == 0 {
		return nil
	}

	// SQLite has a limit of ~999 bound parameters, so batch in chunks
	const batchSize = 100 // 6 params per row = 600 params per batch

	for i := 0; i < len(messages); i += batchSize {
		end := i + batchSize
		if end > len(messages) {
			end = len(messages)
		}
		batch := messages[i:end]

		// Build multi-value INSERT
		query := "INSERT OR REPLACE INTO messages (id, session_id, role, content, sequence, timestamp) VALUES "
		args := make([]interface{}, 0, len(batch)*6)

		for j, m := range batch {
			if j > 0 {
				query += ", "
			}
			query += "(?, ?, ?, ?, ?, ?)"
			args = append(args, m.ID, m.SessionID, m.Role, m.Content, m.Sequence, m.Timestamp)
		}

		if _, err := b.tx.Exec(query, args...); err != nil {
			return err
		}
	}
	return nil
}

// InsertMessageMetadata inserts message metadata within the batch transaction
func (b *TxBatch) InsertMessageMetadata(messageID, sessionID, metadataJSON string) error {
	_, err := b.stmtInsertMetadata.Exec(messageID, sessionID, metadataJSON)
	return err
}

// MetadataEntry is a tuple for bulk metadata insert
type MetadataEntry struct {
	MessageID, SessionID, MetadataJSON string
}

// InsertMessageMetadataBulk inserts multiple metadata entries in a single SQL statement
func (b *TxBatch) InsertMessageMetadataBulk(entries []MetadataEntry) error {
	if len(entries) == 0 {
		return nil
	}

	const batchSize = 200 // 3 params per row

	for i := 0; i < len(entries); i += batchSize {
		end := i + batchSize
		if end > len(entries) {
			end = len(entries)
		}
		batch := entries[i:end]

		query := `INSERT INTO message_metadata (message_id, session_id, metadata_json)
		          VALUES `
		args := make([]interface{}, 0, len(batch)*3)

		for j, e := range batch {
			if j > 0 {
				query += ", "
			}
			query += "(?, ?, ?)"
			args = append(args, e.MessageID, e.SessionID, e.MetadataJSON)
		}
		query += ` ON CONFLICT(message_id) DO UPDATE SET
			session_id = excluded.session_id,
			metadata_json = excluded.metadata_json`

		if _, err := b.tx.Exec(query, args...); err != nil {
			return err
		}
	}
	return nil
}

// InsertMessageCapability inserts a message capability within the batch transaction
func (b *TxBatch) InsertMessageCapability(messageID, sessionID, phase string, capability int) error {
	_, err := b.stmtInsertCapability.Exec(messageID, sessionID, phase, capability)
	return err
}

// InsertMessageLint inserts a message lint within the batch transaction
func (b *TxBatch) InsertMessageLint(messageID, sessionID, filePath, msg, source string, startLine, startCol, endLine, endCol int) error {
	_, err := b.stmtInsertLint.Exec(messageID, sessionID, filePath, msg, source, startLine, startCol, endLine, endCol)
	return err
}

// InsertMessageFile inserts a message file reference within the batch transaction
func (b *TxBatch) InsertMessageFile(messageID, sessionID, kind, filePath string, lineNumber int) error {
	_, err := b.stmtInsertMsgFile.Exec(messageID, sessionID, kind, filePath, lineNumber)
	return err
}

// InsertMessageCodeblock inserts a message codeblock within the batch transaction
func (b *TxBatch) InsertMessageCodeblock(messageID, sessionID string, idx int, rawJSON string) error {
	_, err := b.stmtInsertCodeblock.Exec(messageID, sessionID, idx, rawJSON)
	return err
}

// InsertFileReference inserts a file reference within the batch transaction
func (b *TxBatch) InsertFileReference(sessionID, filePath string) error {
	_, err := b.stmtInsertFileRef.Exec(sessionID, filePath)
	return err
}

// FileRefEntry is a tuple for bulk file reference insert
type FileRefEntry struct {
	SessionID, FilePath string
}

// InsertFileReferencesBulk inserts multiple file references in a single SQL statement
func (b *TxBatch) InsertFileReferencesBulk(entries []FileRefEntry) error {
	if len(entries) == 0 {
		return nil
	}

	const batchSize = 300 // 2 params per row

	for i := 0; i < len(entries); i += batchSize {
		end := i + batchSize
		if end > len(entries) {
			end = len(entries)
		}
		batch := entries[i:end]

		query := `INSERT OR IGNORE INTO files_referenced (session_id, file_path) VALUES `
		args := make([]interface{}, 0, len(batch)*2)

		for j, e := range batch {
			if j > 0 {
				query += ", "
			}
			query += "(?, ?)"
			args = append(args, e.SessionID, e.FilePath)
		}

		if _, err := b.tx.Exec(query, args...); err != nil {
			return err
		}
	}
	return nil
}

// Commit commits the batch transaction
func (b *TxBatch) Commit() error {
	err := b.tx.Commit()
	b.restoreOnce.Do(func() {
		restoreBulkImportPragmas(b.conn, b.pragmaState)
	})
	return err
}

// Rollback rolls back the batch transaction
func (b *TxBatch) Rollback() error {
	err := b.tx.Rollback()
	b.restoreOnce.Do(func() {
		restoreBulkImportPragmas(b.conn, b.pragmaState)
	})
	return err
}

// Close closes all prepared statements (call after Commit or Rollback)
func (b *TxBatch) Close() {
	if b.stmtUpsertSession != nil {
		b.stmtUpsertSession.Close()
	}
	if b.stmtInsertMessage != nil {
		b.stmtInsertMessage.Close()
	}
	if b.stmtInsertMetadata != nil {
		b.stmtInsertMetadata.Close()
	}
	if b.stmtInsertCapability != nil {
		b.stmtInsertCapability.Close()
	}
	if b.stmtInsertLint != nil {
		b.stmtInsertLint.Close()
	}
	if b.stmtInsertMsgFile != nil {
		b.stmtInsertMsgFile.Close()
	}
	if b.stmtInsertCodeblock != nil {
		b.stmtInsertCodeblock.Close()
	}
	if b.stmtInsertFileRef != nil {
		b.stmtInsertFileRef.Close()
	}
	if b.stmtDeleteMessages != nil {
		b.stmtDeleteMessages.Close()
	}
	if b.stmtDeleteMetadata != nil {
		b.stmtDeleteMetadata.Close()
	}
	if b.stmtDeleteCaps != nil {
		b.stmtDeleteCaps.Close()
	}
	if b.stmtDeleteLints != nil {
		b.stmtDeleteLints.Close()
	}
	if b.stmtDeleteMsgFiles != nil {
		b.stmtDeleteMsgFiles.Close()
	}
	if b.stmtDeleteCodeblocks != nil {
		b.stmtDeleteCodeblocks.Close()
	}
	if b.stmtDeleteFiles != nil {
		b.stmtDeleteFiles.Close()
	}
}

// initSchema runs the embedded schema SQL
func (db *DB) initSchema() error {
	// Run migrations first to add any missing columns to existing tables
	// This must happen before schema.sql runs queries that expect new columns
	if err := db.migrate(); err != nil {
		return fmt.Errorf("failed to run migrations: %w", err)
	}

	schema, err := schemaFS.ReadFile("schema.sql")
	if err != nil {
		return fmt.Errorf("failed to read schema: %w", err)
	}

	_, err = db.conn.Exec(string(schema))
	if err != nil {
		return fmt.Errorf("failed to execute schema: %w", err)
	}

	return nil
}

// migrate runs any necessary schema migrations
func (db *DB) migrate() error {
	// Check if sessions table exists first
	var tableExists int
	err := db.conn.QueryRow(`
		SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='sessions'
	`).Scan(&tableExists)
	if err != nil {
		return err
	}

	// If table doesn't exist, schema.sql will create it with all columns
	if tableExists == 0 {
		return nil
	}

	// Add model column to sessions if missing
	var hasModelColumn int
	err = db.conn.QueryRow(`
		SELECT COUNT(*) FROM pragma_table_info('sessions') WHERE name = 'model'
	`).Scan(&hasModelColumn)
	if err != nil {
		return err
	}
	if hasModelColumn == 0 {
		_, err = db.conn.Exec(`ALTER TABLE sessions ADD COLUMN model TEXT`)
		if err != nil {
			return fmt.Errorf("failed to add model column: %w", err)
		}
	}
	return nil
}

// UpsertSession inserts or updates a session
func (db *DB) UpsertSession(s *models.Session, rawJSON string) (isNew bool, err error) {
	// Check if exists
	var existing string
	err = db.conn.QueryRow("SELECT id FROM sessions WHERE id = ?", s.ID).Scan(&existing)
	isNew = err == sql.ErrNoRows

	if isNew {
		_, err = db.conn.Exec(`
			INSERT INTO sessions (id, source, project, model, created_at, message_count, summary, raw_json)
			VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
			s.ID, s.Source, s.Project, s.Model, s.CreatedAt, s.MessageCount, s.Summary, rawJSON)
	} else {
		_, err = db.conn.Exec(`
			UPDATE sessions 
			SET source = ?, project = ?, model = ?, created_at = ?, message_count = ?, summary = ?, raw_json = ?
			WHERE id = ?`,
			s.Source, s.Project, s.Model, s.CreatedAt, s.MessageCount, s.Summary, rawJSON, s.ID)
	}

	return isNew, err
}

// InsertMessage inserts a message, replacing if exists
func (db *DB) InsertMessage(m *models.Message) error {
	_, err := db.conn.Exec(`
		INSERT OR REPLACE INTO messages (id, session_id, role, content, sequence, timestamp)
		VALUES (?, ?, ?, ?, ?, ?)`,
		m.ID, m.SessionID, m.Role, m.Content, m.Sequence, m.Timestamp)
	return err
}

// InsertFileReference inserts a file reference, ignoring duplicates
func (db *DB) InsertFileReference(sessionID, filePath string) error {
	_, err := db.conn.Exec(`
		INSERT OR IGNORE INTO files_referenced (session_id, file_path)
		VALUES (?, ?)`,
		sessionID, filePath)
	return err
}

// UpsertMessageMetadata inserts or updates message metadata JSON.
func (db *DB) UpsertMessageMetadata(messageID, sessionID, metadataJSON string) error {
	_, err := db.conn.Exec(`
		INSERT INTO message_metadata (message_id, session_id, metadata_json)
		VALUES (?, ?, ?)
		ON CONFLICT(message_id) DO UPDATE SET
			session_id = excluded.session_id,
			metadata_json = excluded.metadata_json
	`, messageID, sessionID, metadataJSON)
	return err
}

// InsertMessageCapability inserts a (phase, capability) usage record.
func (db *DB) InsertMessageCapability(messageID, sessionID, phase string, capability int) error {
	_, err := db.conn.Exec(`
		INSERT OR IGNORE INTO message_capabilities (message_id, session_id, phase, capability)
		VALUES (?, ?, ?, ?)
	`, messageID, sessionID, phase, capability)
	return err
}

// InsertMessageLint inserts a linter error captured for a message.
func (db *DB) InsertMessageLint(messageID, sessionID, filePath, msg, source string, startLine, startCol, endLine, endCol int) error {
	_, err := db.conn.Exec(`
		INSERT INTO message_lints (message_id, session_id, file_path, message, source, start_line, start_col, end_line, end_col)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
	`, messageID, sessionID, filePath, msg, source, startLine, startCol, endLine, endCol)
	return err
}

// InsertMessageFile inserts a per-message file reference.
func (db *DB) InsertMessageFile(messageID, sessionID, kind, filePath string, lineNumber int) error {
	_, err := db.conn.Exec(`
		INSERT OR IGNORE INTO message_files (message_id, session_id, kind, file_path, line_number)
		VALUES (?, ?, ?, ?, ?)
	`, messageID, sessionID, kind, filePath, lineNumber)
	return err
}

// InsertMessageCodeblock stores a suggested code block JSON for a message.
func (db *DB) InsertMessageCodeblock(messageID, sessionID string, idx int, rawJSON string) error {
	_, err := db.conn.Exec(`
		INSERT OR REPLACE INTO message_codeblocks (message_id, session_id, idx, raw_json)
		VALUES (?, ?, ?, ?)
	`, messageID, sessionID, idx, rawJSON)
	return err
}

// DeleteSessionMessages deletes all messages for a session
func (db *DB) DeleteSessionMessages(sessionID string) error {
	// Delete metadata first to avoid FK issues (message_id references messages)
	if _, err := db.conn.Exec("DELETE FROM message_metadata WHERE session_id = ?", sessionID); err != nil {
		return err
	}
	if _, err := db.conn.Exec("DELETE FROM message_capabilities WHERE session_id = ?", sessionID); err != nil {
		return err
	}
	if _, err := db.conn.Exec("DELETE FROM message_lints WHERE session_id = ?", sessionID); err != nil {
		return err
	}
	if _, err := db.conn.Exec("DELETE FROM message_files WHERE session_id = ?", sessionID); err != nil {
		return err
	}
	if _, err := db.conn.Exec("DELETE FROM message_codeblocks WHERE session_id = ?", sessionID); err != nil {
		return err
	}
	_, err := db.conn.Exec("DELETE FROM messages WHERE session_id = ?", sessionID)
	return err
}

// DeleteSessionFiles deletes all file references for a session
func (db *DB) DeleteSessionFiles(sessionID string) error {
	_, err := db.conn.Exec("DELETE FROM files_referenced WHERE session_id = ?", sessionID)
	return err
}

// ListSessions returns sessions with optional filters
func (db *DB) ListSessions(project string, since, until int64, limit int) ([]models.Session, error) {
	return db.ListSessionsFiltered(project, "", since, until, limit)
}

// ListSessionsFiltered returns sessions with optional project and source filters
func (db *DB) ListSessionsFiltered(project, source string, since, until int64, limit int) ([]models.Session, error) {
	query := "SELECT id, source, project, model, created_at, message_count, summary FROM sessions WHERE 1=1"
	args := []interface{}{}

	if project != "" {
		query += " AND project = ?"
		args = append(args, project)
	}
	if source != "" {
		query += " AND source = ?"
		args = append(args, source)
	}
	if since > 0 {
		query += " AND created_at >= ?"
		args = append(args, since)
	}
	if until > 0 {
		query += " AND created_at <= ?"
		args = append(args, until)
	}

	query += " ORDER BY created_at DESC"

	if limit > 0 {
		query += " LIMIT ?"
		args = append(args, limit)
	}

	rows, err := db.conn.Query(query, args...)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var sessions []models.Session
	for rows.Next() {
		var s models.Session
		var project, model, summary sql.NullString
		var createdAt sql.NullInt64

		if err := rows.Scan(&s.ID, &s.Source, &project, &model, &createdAt, &s.MessageCount, &summary); err != nil {
			return nil, err
		}
		s.Project = project.String
		s.Model = model.String
		s.Summary = summary.String
		s.CreatedAt = createdAt.Int64
		sessions = append(sessions, s)
	}

	return sessions, rows.Err()
}

// GetSession returns a single session by ID
func (db *DB) GetSession(id string) (*models.Session, error) {
	var s models.Session
	var project, model, summary sql.NullString
	var createdAt sql.NullInt64

	err := db.conn.QueryRow(`
		SELECT id, source, project, model, created_at, message_count, summary 
		FROM sessions WHERE id = ?`, id).
		Scan(&s.ID, &s.Source, &project, &model, &createdAt, &s.MessageCount, &summary)

	if err == sql.ErrNoRows {
		return nil, nil
	}
	if err != nil {
		return nil, err
	}

	s.Project = project.String
	s.Model = model.String
	s.Summary = summary.String
	s.CreatedAt = createdAt.Int64
	return &s, nil
}

// GetSessionMessages returns messages for a session
func (db *DB) GetSessionMessages(sessionID string) ([]models.Message, error) {
	rows, err := db.conn.Query(`
		SELECT id, session_id, role, content, sequence, timestamp 
		FROM messages WHERE session_id = ? ORDER BY sequence`, sessionID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var messages []models.Message
	for rows.Next() {
		var m models.Message
		var content sql.NullString
		var timestamp sql.NullInt64

		if err := rows.Scan(&m.ID, &m.SessionID, &m.Role, &content, &m.Sequence, &timestamp); err != nil {
			return nil, err
		}
		m.Content = content.String
		m.Timestamp = timestamp.Int64
		messages = append(messages, m)
	}

	return messages, rows.Err()
}

// GetSessionFiles returns file references for a session
func (db *DB) GetSessionFiles(sessionID string) ([]string, error) {
	rows, err := db.conn.Query(
		"SELECT file_path FROM files_referenced WHERE session_id = ?", sessionID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var files []string
	for rows.Next() {
		var path string
		if err := rows.Scan(&path); err != nil {
			return nil, err
		}
		files = append(files, path)
	}

	return files, rows.Err()
}

// QueryResult represents the result of a raw query
type QueryResult struct {
	OK       bool                     `json:"ok"`
	RowCount int                      `json:"row_count"`
	Rows     []map[string]interface{} `json:"rows,omitempty"`
	Error    string                   `json:"error,omitempty"`
}

// Query executes a raw SQL query and returns results as JSON-friendly maps
func (db *DB) Query(sql string) QueryResult {
	// Basic safety check - only allow SELECT and WITH
	trimmed := strings.TrimSpace(sql)
	upper := strings.ToUpper(trimmed)
	if !strings.HasPrefix(upper, "SELECT") && !strings.HasPrefix(upper, "WITH") {
		return QueryResult{
			OK:    false,
			Error: "only SELECT and WITH statements are allowed",
		}
	}

	rows, err := db.conn.Query(sql)
	if err != nil {
		return QueryResult{
			OK:    false,
			Error: fmt.Sprintf("query failed: %v", err),
		}
	}
	defer rows.Close()

	columns, err := rows.Columns()
	if err != nil {
		return QueryResult{
			OK:    false,
			Error: fmt.Sprintf("failed to get columns: %v", err),
		}
	}

	var results []map[string]interface{}
	for rows.Next() {
		values := make([]interface{}, len(columns))
		valuePtrs := make([]interface{}, len(columns))
		for i := range values {
			valuePtrs[i] = &values[i]
		}

		if err := rows.Scan(valuePtrs...); err != nil {
			return QueryResult{
				OK:    false,
				Error: fmt.Sprintf("failed to scan row: %v", err),
			}
		}

		rowMap := make(map[string]interface{})
		for i, col := range columns {
			val := values[i]
			if b, ok := val.([]byte); ok {
				rowMap[col] = string(b)
			} else {
				rowMap[col] = val
			}
		}
		results = append(results, rowMap)
	}

	if err := rows.Err(); err != nil {
		return QueryResult{
			OK:    false,
			Error: fmt.Sprintf("row iteration error: %v", err),
		}
	}

	return QueryResult{
		OK:       true,
		RowCount: len(results),
		Rows:     results,
	}
}

// GetDistinctProjects returns a list of distinct project names
func (db *DB) GetDistinctProjects() ([]string, error) {
	rows, err := db.conn.Query(
		"SELECT DISTINCT project FROM sessions WHERE project IS NOT NULL AND project != '' ORDER BY project")
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var projects []string
	for rows.Next() {
		var p string
		if err := rows.Scan(&p); err != nil {
			return nil, err
		}
		projects = append(projects, p)
	}

	return projects, rows.Err()
}

// Stats returns database statistics
func (db *DB) Stats() (map[string]interface{}, error) {
	stats := make(map[string]interface{})

	var sessionCount int
	err := db.conn.QueryRow("SELECT COUNT(*) FROM sessions").Scan(&sessionCount)
	if err != nil {
		return nil, err
	}
	stats["sessions"] = sessionCount

	var messageCount int
	err = db.conn.QueryRow("SELECT COUNT(*) FROM messages").Scan(&messageCount)
	if err != nil {
		return nil, err
	}
	stats["messages"] = messageCount

	var fileCount int
	err = db.conn.QueryRow("SELECT COUNT(*) FROM files_referenced").Scan(&fileCount)
	if err != nil {
		return nil, err
	}
	stats["files_referenced"] = fileCount

	// Get projects count
	var projectCount int
	err = db.conn.QueryRow("SELECT COUNT(DISTINCT project) FROM sessions WHERE project IS NOT NULL AND project != ''").Scan(&projectCount)
	if err != nil {
		return nil, err
	}
	stats["projects"] = projectCount

	stats["db_path"] = db.path

	return stats, nil
}

// GetSourceStats returns session counts by source
func (db *DB) GetSourceStats() (map[string]int, error) {
	rows, err := db.conn.Query(`
		SELECT source, COUNT(*) as count 
		FROM sessions 
		GROUP BY source 
		ORDER BY count DESC
	`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	stats := make(map[string]int)
	for rows.Next() {
		var source string
		var count int
		if err := rows.Scan(&source, &count); err != nil {
			return nil, err
		}
		stats[source] = count
	}
	return stats, rows.Err()
}

// GetSyncState gets a sync state value
func (db *DB) GetSyncState(key string) (string, error) {
	var value string
	err := db.conn.QueryRow("SELECT value FROM sync_state WHERE key = ?", key).Scan(&value)
	if err == sql.ErrNoRows {
		return "", nil
	}
	return value, err
}

// SetSyncState sets a sync state value
func (db *DB) SetSyncState(key, value string) error {
	_, err := db.conn.Exec(`
		INSERT OR REPLACE INTO sync_state (key, value, updated_at)
		VALUES (?, ?, ?)`,
		key, value, unixMillis())
	return err
}

func unixMillis() int64 {
	return time.Now().UnixMilli()
}

// Helper for JSON encoding in queries
func jsonEncode(v interface{}) string {
	b, _ := json.Marshal(v)
	return string(b)
}

// ResolveSessionIDPrefix resolves a session id prefix to a full session id.
// Returns "" if no match is found.
func (db *DB) ResolveSessionIDPrefix(prefix string) (string, error) {
	var id string
	err := db.conn.QueryRow(`SELECT id FROM sessions WHERE id LIKE ? LIMIT 1`, prefix+"%").Scan(&id)
	if err == sql.ErrNoRows {
		return "", nil
	}
	return id, err
}

// UpsertEmbedding stores an embedding for an entity (message/session/etc).
func (db *DB) UpsertEmbedding(entityType, entityID, model string, embedding []float64) error {
	if entityType == "" || entityID == "" || model == "" {
		return fmt.Errorf("entityType, entityID, and model are required")
	}
	if len(embedding) == 0 {
		return fmt.Errorf("empty embedding")
	}

	blob, err := float64SliceToBlob(embedding)
	if err != nil {
		return err
	}

	_, err = db.conn.Exec(`
		INSERT INTO embeddings (entity_type, entity_id, model, embedding_blob, dimension, created_at)
		VALUES (?, ?, ?, ?, ?, ?)
		ON CONFLICT(entity_type, entity_id, model) DO UPDATE SET
			embedding_blob = excluded.embedding_blob,
			dimension = excluded.dimension,
			created_at = excluded.created_at
	`, entityType, entityID, model, blob, len(embedding), unixMillis())

	return err
}

// MessageToEmbed is a message row used for embedding.
type MessageToEmbed struct {
	ID      string
	Content string
}

// GetMessagesMissingEmbeddings returns messages missing embeddings for a given model.
func (db *DB) GetMessagesMissingEmbeddings(model string, limit int) ([]MessageToEmbed, error) {
	if model == "" {
		return nil, fmt.Errorf("model is required")
	}
	if limit <= 0 {
		limit = 1000
	}

	rows, err := db.conn.Query(`
		SELECT m.id, m.content
		FROM messages m
		WHERE m.content IS NOT NULL AND m.content != ''
		  AND NOT EXISTS (
			SELECT 1 FROM embeddings e
			WHERE e.entity_type = 'message' AND e.entity_id = m.id AND e.model = ?
		  )
		ORDER BY m.session_id, m.sequence
		LIMIT ?
	`, model, limit)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var out []MessageToEmbed
	for rows.Next() {
		var m MessageToEmbed
		if err := rows.Scan(&m.ID, &m.Content); err != nil {
			return nil, err
		}
		out = append(out, m)
	}
	return out, rows.Err()
}

// EmbeddedMessage is a message joined with its embedding and some session metadata.
type EmbeddedMessage struct {
	MessageID string
	SessionID string
	Role      string
	Content   string
	Sequence  int
	Project   string
	CreatedAt int64
	Embedding []float64
}

// GetEmbeddedMessages loads message embeddings for similarity search.
func (db *DB) GetEmbeddedMessages(model string, project string) ([]EmbeddedMessage, error) {
	if model == "" {
		return nil, fmt.Errorf("model is required")
	}

	query := `
		SELECT e.entity_id, m.session_id, m.role, m.content, m.sequence, s.project, s.created_at, e.embedding_blob
		FROM embeddings e
		JOIN messages m ON e.entity_id = m.id
		JOIN sessions s ON m.session_id = s.id
		WHERE e.entity_type = 'message' AND e.model = ?
	`
	args := []interface{}{model}
	if project != "" {
		query += " AND s.project = ?"
		args = append(args, project)
	}

	rows, err := db.conn.Query(query, args...)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var out []EmbeddedMessage
	for rows.Next() {
		var em EmbeddedMessage
		var content sql.NullString
		var role sql.NullString
		var project sql.NullString
		var createdAt sql.NullInt64
		var blob []byte

		if err := rows.Scan(&em.MessageID, &em.SessionID, &role, &content, &em.Sequence, &project, &createdAt, &blob); err != nil {
			return nil, err
		}
		em.Role = role.String
		em.Content = content.String
		em.Project = project.String
		em.CreatedAt = createdAt.Int64
		vec, err := blobToFloat64Slice(blob)
		if err != nil {
			continue
		}
		em.Embedding = vec
		out = append(out, em)
	}
	return out, rows.Err()
}

func float64SliceToBlob(values []float64) ([]byte, error) {
	blob := make([]byte, len(values)*8)
	for i, v := range values {
		bits := math.Float64bits(v)
		binary.LittleEndian.PutUint64(blob[i*8:(i+1)*8], bits)
	}
	return blob, nil
}

func blobToFloat64Slice(blob []byte) ([]float64, error) {
	if len(blob)%8 != 0 {
		return nil, fmt.Errorf("invalid blob length: %d (must be multiple of 8)", len(blob))
	}
	values := make([]float64, len(blob)/8)
	for i := 0; i < len(values); i++ {
		bits := binary.LittleEndian.Uint64(blob[i*8 : (i+1)*8])
		values[i] = math.Float64frombits(bits)
	}
	return values, nil
}
