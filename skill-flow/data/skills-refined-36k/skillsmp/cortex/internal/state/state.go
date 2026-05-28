package state

import (
	"database/sql"
	"fmt"
	"time"
)

func ensureTable(db *sql.DB) error {
	_, err := db.Exec(`
		CREATE TABLE IF NOT EXISTS adapter_state (
			adapter TEXT NOT NULL,
			key TEXT NOT NULL,
			value TEXT NOT NULL,
			updated_at INTEGER NOT NULL,
			PRIMARY KEY (adapter, key)
		)
	`)
	if err != nil {
		return fmt.Errorf("failed to ensure adapter_state table: %w", err)
	}
	return nil
}

func Get(db *sql.DB, adapter string, key string) (string, bool, error) {
	if err := ensureTable(db); err != nil {
		return "", false, err
	}
	var v string
	err := db.QueryRow(`SELECT value FROM adapter_state WHERE adapter = ? AND key = ?`, adapter, key).Scan(&v)
	if err == sql.ErrNoRows {
		return "", false, nil
	}
	if err != nil {
		return "", false, fmt.Errorf("failed to get adapter state: %w", err)
	}
	return v, true, nil
}

func Set(db *sql.DB, adapter string, key string, value string) error {
	if err := ensureTable(db); err != nil {
		return err
	}
	now := time.Now().Unix()
	_, err := db.Exec(`
		INSERT INTO adapter_state (adapter, key, value, updated_at)
		VALUES (?, ?, ?, ?)
		ON CONFLICT(adapter, key) DO UPDATE SET
			value = excluded.value,
			updated_at = excluded.updated_at
	`, adapter, key, value, now)
	if err != nil {
		return fmt.Errorf("failed to set adapter state: %w", err)
	}
	return nil
}
