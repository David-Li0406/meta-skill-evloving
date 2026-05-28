package testutil

import (
	"database/sql"
	"os"
	"path/filepath"
	"runtime"
	"testing"

	_ "modernc.org/sqlite"
)

// OpenTestDB creates an in-memory SQLite DB and applies the cortex schema.
func OpenTestDB(t *testing.T) *sql.DB {
	t.Helper()

	db, err := sql.Open("sqlite", ":memory:")
	if err != nil {
		t.Fatalf("open db: %v", err)
	}

	_, _ = db.Exec("PRAGMA foreign_keys = ON")

	schema, err := readSchema()
	if err != nil {
		db.Close()
		t.Fatalf("read schema: %v", err)
	}
	if _, err := db.Exec(schema); err != nil {
		db.Close()
		t.Fatalf("apply schema: %v", err)
	}
	return db
}

func readSchema() (string, error) {
	_, filename, _, ok := runtime.Caller(0)
	if !ok {
		return "", os.ErrNotExist
	}
	schemaPath := filepath.Join(filepath.Dir(filename), "..", "db", "schema.sql")
	data, err := os.ReadFile(schemaPath)
	if err != nil {
		return "", err
	}
	return string(data), nil
}
