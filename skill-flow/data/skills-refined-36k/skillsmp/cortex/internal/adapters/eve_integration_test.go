//go:build integration

package adapters

import (
	"context"
	"database/sql"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"testing"

	"github.com/Napageneral/cortex/internal/db"
	"github.com/Napageneral/cortex/internal/me"
)

func eveDBPath(t *testing.T) string {
	t.Helper()
	if p := os.Getenv("EVE_DB_PATH"); p != "" {
		return p
	}
	home, err := os.UserHomeDir()
	if err != nil {
		t.Fatalf("os.UserHomeDir: %v", err)
	}
	return filepath.Join(home, "Library", "Application Support", "Eve", "eve.db")
}

func openEveDB(t *testing.T) *sql.DB {
	t.Helper()
	p := eveDBPath(t)
	if _, err := os.Stat(p); err != nil {
		t.Fatalf("eve db not accessible at %s: %v", p, err)
	}
	dbc, err := sql.Open("sqlite", "file:"+p+"?mode=ro")
	if err != nil {
		t.Fatalf("open eve db: %v", err)
	}
	t.Cleanup(func() { _ = dbc.Close() })
	return dbc
}

func setupTempCommsDB(t *testing.T) *sql.DB {
	t.Helper()
	tmp := t.TempDir()
	dataDir := filepath.Join(tmp, "data")
	configDir := filepath.Join(tmp, "config")
	if err := os.MkdirAll(dataDir, 0o755); err != nil {
		t.Fatalf("mkdir data dir: %v", err)
	}
	if err := os.MkdirAll(configDir, 0o755); err != nil {
		t.Fatalf("mkdir config dir: %v", err)
	}

	// Force cortex to use temp locations (macOS otherwise uses ~/Library/...).
	t.Setenv("COMMS_DATA_DIR", dataDir)
	t.Setenv("COMMS_CONFIG_DIR", configDir)

	if err := db.Init(); err != nil {
		t.Fatalf("db.Init: %v", err)
	}

	cortexDB, err := db.Open()
	if err != nil {
		t.Fatalf("db.Open: %v", err)
	}
	t.Cleanup(func() { _ = cortexDB.Close() })

	// Ensure "me" exists so sent messages can attach a sender participant.
	if err := me.SetMeName(cortexDB, "Test User"); err != nil {
		t.Fatalf("me.SetMeName: %v", err)
	}

	return cortexDB
}

func TestEveAdapter_MapsCoreFields(t *testing.T) {
	ctx := context.Background()
	eve := openEveDB(t)

	// Pick 3 target messages near the end of the dataset to keep the sync fast:
	// 1) Latest message with attachment
	// 2) Latest message whose chat row is missing
	// 3) Latest message whose chat row exists (thread_id should equal chat_identifier)
	type target struct {
		name         string
		guid         string
		ts           int64
		expectThread string
		expectPrefix string
		expectAttach bool
	}

	var (
		attach target
		miss   target
		okchat target
	)

	// Latest attachment message
	{
		row := eve.QueryRow(`
			SELECT m.guid, CAST(strftime('%s', m.timestamp) AS INTEGER) as ts
			FROM messages m
			WHERE EXISTS (SELECT 1 FROM attachments a WHERE a.message_id = m.id)
			ORDER BY m.timestamp DESC
			LIMIT 1
		`)
		if err := row.Scan(&attach.guid, &attach.ts); err != nil {
			t.Fatalf("query latest attachment message: %v", err)
		}
		attach.name = "attachment"
		attach.expectAttach = true
	}

	// Latest missing-chat message
	{
		var chatID int64
		row := eve.QueryRow(`
			SELECT m.guid, CAST(strftime('%s', m.timestamp) AS INTEGER) as ts, m.chat_id
			FROM messages m
			LEFT JOIN chats c ON m.chat_id = c.id
			WHERE c.id IS NULL
			ORDER BY m.timestamp DESC
			LIMIT 1
		`)
		if err := row.Scan(&miss.guid, &miss.ts, &chatID); err != nil {
			t.Fatalf("query latest missing-chat message: %v", err)
		}
		miss.name = "missing_chat"
		miss.expectPrefix = "chat_id:"
	}

	// Latest ok-chat message
	{
		row := eve.QueryRow(`
			SELECT m.guid, CAST(strftime('%s', m.timestamp) AS INTEGER) as ts, c.chat_identifier
			FROM messages m
			JOIN chats c ON m.chat_id = c.id
			ORDER BY m.timestamp DESC
			LIMIT 1
		`)
		if err := row.Scan(&okchat.guid, &okchat.ts, &okchat.expectThread); err != nil {
			t.Fatalf("query latest ok-chat message: %v", err)
		}
		okchat.name = "ok_chat"
	}

	minTS := attach.ts
	for _, ts := range []int64{miss.ts, okchat.ts} {
		if ts < minTS {
			minTS = ts
		}
	}

	cortexDB := setupTempCommsDB(t)

	// Seed watermark so sync only imports a small tail window.
	watermark := minTS - 5
	if watermark < 0 {
		watermark = 0
	}
	_, err := cortexDB.Exec(`
		INSERT INTO sync_watermarks (adapter, last_sync_at, last_event_id)
		VALUES (?, ?, NULL)
		ON CONFLICT(adapter) DO UPDATE SET last_sync_at = excluded.last_sync_at
	`, "imessage", watermark)
	if err != nil {
		t.Fatalf("seed watermark: %v", err)
	}

	adapter, err := NewEveAdapter()
	if err != nil {
		t.Fatalf("NewEveAdapter: %v", err)
	}

	sr, err := adapter.Sync(ctx, cortexDB, false)
	if err != nil {
		t.Fatalf("Sync: %v", err)
	}
	if sr.EventsCreated <= 0 {
		t.Fatalf("expected some events created, got %d", sr.EventsCreated)
	}

	// Validate mapping for each target GUID
	check := func(tgt target) {
		t.Helper()

		var (
			threadID     sql.NullString
			contentTypes string
		)
		row := cortexDB.QueryRow(`
			SELECT thread_id, content_types
			FROM events
			WHERE source_adapter = 'imessage' AND source_id = ?
			LIMIT 1
		`, tgt.guid)
		if err := row.Scan(&threadID, &contentTypes); err != nil {
			t.Fatalf("event not found for %s guid=%s: %v", tgt.name, tgt.guid, err)
		}

		if tgt.expectThread != "" && (!threadID.Valid || threadID.String != tgt.expectThread) {
			t.Fatalf("%s: expected thread_id=%q, got %q", tgt.name, tgt.expectThread, threadID.String)
		}
		if tgt.expectPrefix != "" && (!threadID.Valid || !strings.HasPrefix(threadID.String, tgt.expectPrefix)) {
			t.Fatalf("%s: expected thread_id to have prefix %q, got %q", tgt.name, tgt.expectPrefix, threadID.String)
		}
		if tgt.expectAttach && !strings.Contains(contentTypes, "attachment") {
			t.Fatalf("%s: expected content_types to contain attachment, got %q", tgt.name, contentTypes)
		}
	}

	check(attach)
	check(miss)
	check(okchat)
}

func TestEveAdapter_CountMatchesEveTailWindow(t *testing.T) {
	ctx := context.Background()
	eve := openEveDB(t)
	cortexDB := setupTempCommsDB(t)

	// Get Eve max timestamp and sync only the last 120 seconds.
	var maxTSStr string
	if err := eve.QueryRow(`SELECT MAX(strftime('%s', timestamp)) FROM messages`).Scan(&maxTSStr); err != nil {
		t.Fatalf("query max ts: %v", err)
	}
	maxTS, err := strconv.ParseInt(maxTSStr, 10, 64)
	if err != nil {
		t.Fatalf("parse max ts: %v", err)
	}
	watermark := maxTS - 120
	if watermark < 0 {
		watermark = 0
	}

	var expected int
	if err := eve.QueryRow(`SELECT COUNT(*) FROM messages WHERE CAST(strftime('%s', timestamp) AS INTEGER) > ?`, watermark).Scan(&expected); err != nil {
		t.Fatalf("expected count query: %v", err)
	}

	_, err = cortexDB.Exec(`
		INSERT INTO sync_watermarks (adapter, last_sync_at, last_event_id)
		VALUES (?, ?, NULL)
		ON CONFLICT(adapter) DO UPDATE SET last_sync_at = excluded.last_sync_at
	`, "imessage", watermark)
	if err != nil {
		t.Fatalf("seed watermark: %v", err)
	}

	adapter, err := NewEveAdapter()
	if err != nil {
		t.Fatalf("NewEveAdapter: %v", err)
	}

	sr, err := adapter.Sync(ctx, cortexDB, false)
	if err != nil {
		t.Fatalf("Sync: %v", err)
	}

	// On a fresh cortex DB, everything imported should be new.
	if sr.EventsCreated != expected {
		t.Fatalf("expected EventsCreated=%d, got %d (EventsUpdated=%d)", expected, sr.EventsCreated, sr.EventsUpdated)
	}
	if sr.EventsUpdated != 0 {
		t.Fatalf("expected EventsUpdated=0 on fresh db, got %d", sr.EventsUpdated)
	}
}

