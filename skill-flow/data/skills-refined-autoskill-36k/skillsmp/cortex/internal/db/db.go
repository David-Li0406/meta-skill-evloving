package db

import (
	"database/sql"
	_ "embed"
	"fmt"
	"path/filepath"

	_ "modernc.org/sqlite"

	"github.com/Napageneral/cortex/internal/config"
)

//go:embed schema.sql
var schemaSQL string

// Init initializes the database and creates tables if needed
func Init() error {
	dataDir, err := config.GetDataDir()
	if err != nil {
		return err
	}

	dbPath := filepath.Join(dataDir, "cortex.db")

	db, err := sql.Open("sqlite", dbPath)
	if err != nil {
		return fmt.Errorf("failed to open database: %w", err)
	}
	defer db.Close()

	// SQLite behaves best with a single connection per process.
	// Multiple connections can contend for the write lock and cause SQLITE_BUSY.
	db.SetMaxOpenConns(1)
	db.SetMaxIdleConns(1)

	// Pragmas for performance + concurrency.
	// WAL allows concurrent readers while a writer is active.
	// busy_timeout reduces SQLITE_BUSY errors under contention.
	_, _ = db.Exec("PRAGMA journal_mode = WAL")
	_, _ = db.Exec("PRAGMA synchronous = NORMAL")
	_, _ = db.Exec("PRAGMA busy_timeout = 30000")
	_, _ = db.Exec("PRAGMA foreign_keys = ON")

	// Ensure legacy columns exist before applying schema (prevents index errors).
	if err := ensureLegacyColumns(db); err != nil {
		return err
	}

	// Execute schema
	if _, err := db.Exec(schemaSQL); err != nil {
		return fmt.Errorf("failed to create schema: %w", err)
	}

	return nil
}

// Open opens a connection to the database
func Open() (*sql.DB, error) {
	dataDir, err := config.GetDataDir()
	if err != nil {
		return nil, err
	}

	dbPath := filepath.Join(dataDir, "cortex.db")

	db, err := sql.Open("sqlite", dbPath)
	if err != nil {
		return nil, fmt.Errorf("failed to open database: %w", err)
	}

	// SQLite behaves best with a single connection per process.
	// Multiple connections can contend for the write lock and cause SQLITE_BUSY.
	db.SetMaxOpenConns(1)
	db.SetMaxIdleConns(1)

	// Pragmas for performance + concurrency.
	// WAL allows concurrent readers while a writer is active.
	// busy_timeout reduces SQLITE_BUSY errors under contention.
	if _, err := db.Exec("PRAGMA journal_mode = WAL"); err != nil {
		db.Close()
		return nil, fmt.Errorf("failed to enable WAL: %w", err)
	}
	if _, err := db.Exec("PRAGMA synchronous = NORMAL"); err != nil {
		db.Close()
		return nil, fmt.Errorf("failed to set synchronous: %w", err)
	}
	if _, err := db.Exec("PRAGMA busy_timeout = 30000"); err != nil {
		db.Close()
		return nil, fmt.Errorf("failed to set busy_timeout: %w", err)
	}
	if _, err := db.Exec("PRAGMA foreign_keys = ON"); err != nil {
		db.Close()
		return nil, fmt.Errorf("failed to enable foreign keys: %w", err)
	}

	return db, nil
}

// GetPath returns the path to the database file
func GetPath() (string, error) {
	dataDir, err := config.GetDataDir()
	if err != nil {
		return "", err
	}
	return filepath.Join(dataDir, "cortex.db"), nil
}

func ensureLegacyColumns(db *sql.DB) error {
	// Columns added after earlier schema versions.
	if err := ensureColumn(db, "person_facts", "source_episode_id", "TEXT"); err != nil {
		return err
	}
	if err := ensureColumn(db, "unattributed_facts", "source_episode_id", "TEXT REFERENCES episodes(id)"); err != nil {
		return err
	}
	if err := ensureColumn(db, "candidate_mentions", "source_episode_id", "TEXT REFERENCES episodes(id)"); err != nil {
		return err
	}
	return nil
}

func ensureColumn(db *sql.DB, table, column, definition string) error {
	if !tableExists(db, table) {
		return nil
	}
	has, err := columnExists(db, table, column)
	if err != nil {
		return err
	}
	if has {
		return nil
	}
	_, err = db.Exec(fmt.Sprintf("ALTER TABLE %s ADD COLUMN %s %s", table, column, definition))
	if err != nil {
		return fmt.Errorf("add column %s.%s: %w", table, column, err)
	}
	return nil
}

func tableExists(db *sql.DB, table string) bool {
	var name string
	err := db.QueryRow(`SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?`, table).Scan(&name)
	return err == nil
}

func columnExists(db *sql.DB, table, column string) (bool, error) {
	rows, err := db.Query(fmt.Sprintf("PRAGMA table_info(%s)", table))
	if err != nil {
		return false, err
	}
	defer rows.Close()

	for rows.Next() {
		var cid int
		var name, ctype string
		var notnull int
		var dfltValue sql.NullString
		var pk int
		if err := rows.Scan(&cid, &name, &ctype, &notnull, &dfltValue, &pk); err != nil {
			return false, err
		}
		if name == column {
			return true, nil
		}
	}
	if err := rows.Err(); err != nil {
		return false, err
	}
	return false, nil
}
