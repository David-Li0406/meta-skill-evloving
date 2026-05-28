package sync

import (
	"encoding/json"
	"os"
	"path/filepath"
	"testing"
)

func TestPiAgentParser_ClawdbotDefaults(t *testing.T) {
	parser := NewClawdbotParser("")
	if parser.source != "clawdbot" {
		t.Errorf("expected source 'clawdbot', got '%s'", parser.source)
	}
	if parser.basePath == "" {
		t.Error("expected non-empty basePath")
	}
}

func TestPiAgentParser_NexusDefaults(t *testing.T) {
	parser := NewNexusParser("")
	if parser.source != "nexus" {
		t.Errorf("expected source 'nexus', got '%s'", parser.source)
	}
	if parser.basePath == "" {
		t.Error("expected non-empty basePath")
	}
}

func TestPiAgentParser_ParsesSessionHeader(t *testing.T) {
	// Create temp directory
	dir := t.TempDir()

	// Write a session JSONL file with session header
	sessionContent := `{"type":"session","version":"1.0","id":"test-session-123","timestamp":"2026-01-21T12:00:00Z","cwd":"/Users/test/project"}
{"type":"user","timestamp":"2026-01-21T12:00:01Z","sessionId":"test-session-123","uuid":"msg-1","message":{"role":"user","content":"Hello"}}
{"type":"assistant","timestamp":"2026-01-21T12:00:02Z","sessionId":"test-session-123","uuid":"msg-2","message":{"role":"assistant","content":"Hi there!","model":"claude-4-sonnet"}}
`
	err := os.WriteFile(filepath.Join(dir, "test-session-123.jsonl"), []byte(sessionContent), 0644)
	if err != nil {
		t.Fatal(err)
	}

	parser := NewClawdbotParser(dir)
	sessions, errors := parser.ParseAll()

	if len(errors) > 0 {
		t.Errorf("unexpected errors: %v", errors)
	}
	if len(sessions) != 1 {
		t.Fatalf("expected 1 session, got %d", len(sessions))
	}

	sess := sessions[0]
	if sess.Session.ID != "test-session-123" {
		t.Errorf("expected session ID 'test-session-123', got '%s'", sess.Session.ID)
	}
	if sess.Session.Source != "clawdbot" {
		t.Errorf("expected source 'clawdbot', got '%s'", sess.Session.Source)
	}
	if sess.Session.Model != "claude-4-sonnet" {
		t.Errorf("expected model 'claude-4-sonnet', got '%s'", sess.Session.Model)
	}
	if len(sess.Messages) != 2 {
		t.Errorf("expected 2 messages, got %d", len(sess.Messages))
	}
}

func TestPiAgentParser_ParsesContentBlocks(t *testing.T) {
	dir := t.TempDir()

	// Write session with content blocks (array format)
	sessionContent := `{"type":"session","version":"1.0","id":"content-blocks-test","timestamp":"2026-01-21T12:00:00Z","cwd":"/test"}
{"type":"user","timestamp":"2026-01-21T12:00:01Z","sessionId":"content-blocks-test","uuid":"msg-1","message":{"role":"user","content":[{"type":"text","text":"Hello world"}]}}
{"type":"assistant","timestamp":"2026-01-21T12:00:02Z","sessionId":"content-blocks-test","uuid":"msg-2","message":{"role":"assistant","content":[{"type":"text","text":"First part"},{"type":"text","text":"Second part"}],"model":"claude-4"}}
`
	err := os.WriteFile(filepath.Join(dir, "content-blocks-test.jsonl"), []byte(sessionContent), 0644)
	if err != nil {
		t.Fatal(err)
	}

	parser := NewNexusParser(dir)
	sessions, errors := parser.ParseAll()

	if len(errors) > 0 {
		t.Errorf("unexpected errors: %v", errors)
	}
	if len(sessions) != 1 {
		t.Fatalf("expected 1 session, got %d", len(sessions))
	}

	sess := sessions[0]
	if sess.Session.Source != "nexus" {
		t.Errorf("expected source 'nexus', got '%s'", sess.Session.Source)
	}
	if len(sess.Messages) != 2 {
		t.Fatalf("expected 2 messages, got %d", len(sess.Messages))
	}

	// Check content extraction from array
	if sess.Messages[0].Content != "Hello world" {
		t.Errorf("expected 'Hello world', got '%s'", sess.Messages[0].Content)
	}
	if sess.Messages[1].Content != "First part\nSecond part" {
		t.Errorf("expected 'First part\\nSecond part', got '%s'", sess.Messages[1].Content)
	}
}

func TestPiAgentParser_LoadsSessionsStore(t *testing.T) {
	dir := t.TempDir()

	// Write sessions.json with rich metadata
	store := map[string]SessionEntry{
		"rich-session": {
			SessionID:     "rich-session",
			UpdatedAt:     1705838400000,
			InputTokens:   1000,
			OutputTokens:  500,
			TotalTokens:   1500,
			Model:         "claude-4-opus",
			ModelProvider: "anthropic",
			Origin: &SessionOrigin{
				Provider:  "telegram",
				Surface:   "dm",
				AccountID: "bot123",
			},
			QueueMode: "steer",
		},
	}
	storeData, _ := json.Marshal(store)
	err := os.WriteFile(filepath.Join(dir, "sessions.json"), storeData, 0644)
	if err != nil {
		t.Fatal(err)
	}

	// Write matching session file
	sessionContent := `{"type":"session","version":"1.0","id":"rich-session","timestamp":"2026-01-21T12:00:00Z","cwd":"/test"}
{"type":"user","timestamp":"2026-01-21T12:00:01Z","sessionId":"rich-session","uuid":"msg-1","message":{"role":"user","content":"Test"}}
`
	err = os.WriteFile(filepath.Join(dir, "rich-session.jsonl"), []byte(sessionContent), 0644)
	if err != nil {
		t.Fatal(err)
	}

	parser := NewClawdbotParser(dir)
	sessions, errors := parser.ParseAll()

	if len(errors) > 0 {
		t.Errorf("unexpected errors: %v", errors)
	}
	if len(sessions) != 1 {
		t.Fatalf("expected 1 session, got %d", len(sessions))
	}

	sess := sessions[0]
	// Model should come from sessions.json since not in transcript
	if sess.Session.Model != "claude-4-opus" {
		t.Errorf("expected model 'claude-4-opus' from store, got '%s'", sess.Session.Model)
	}

	// Check that session_entry metadata was captured
	if meta, ok := sess.MessageMetadata["session_entry"]; !ok || meta == "" {
		t.Error("expected session_entry metadata to be populated")
	} else {
		// Verify it contains origin data
		var entry SessionEntry
		if err := json.Unmarshal([]byte(meta), &entry); err != nil {
			t.Errorf("failed to parse session_entry: %v", err)
		} else {
			if entry.Origin == nil || entry.Origin.Provider != "telegram" {
				t.Errorf("expected origin.provider 'telegram', got %+v", entry.Origin)
			}
			if entry.TotalTokens != 1500 {
				t.Errorf("expected totalTokens 1500, got %d", entry.TotalTokens)
			}
		}
	}
}

func TestPiAgentParser_ParsesBackupFiles(t *testing.T) {
	dir := t.TempDir()

	// Write main session file
	mainContent := `{"type":"session","version":"1.0","id":"backup-test","timestamp":"2026-01-21T14:00:00Z","cwd":"/test"}
{"type":"user","timestamp":"2026-01-21T14:00:01Z","sessionId":"backup-test","uuid":"msg-3","message":{"role":"user","content":"After compaction"}}
`
	err := os.WriteFile(filepath.Join(dir, "backup-test.jsonl"), []byte(mainContent), 0644)
	if err != nil {
		t.Fatal(err)
	}

	// Write backup file (pre-compaction history)
	backupContent := `{"type":"session","version":"1.0","id":"backup-test","timestamp":"2026-01-21T12:00:00Z","cwd":"/test"}
{"type":"user","timestamp":"2026-01-21T12:00:01Z","sessionId":"backup-test","uuid":"msg-1","message":{"role":"user","content":"Before compaction"}}
{"type":"assistant","timestamp":"2026-01-21T12:00:02Z","sessionId":"backup-test","uuid":"msg-2","message":{"role":"assistant","content":"Old response"}}
`
	err = os.WriteFile(filepath.Join(dir, "backup-test.jsonl.bak.2026-01-21T13-00-00.000Z"), []byte(backupContent), 0644)
	if err != nil {
		t.Fatal(err)
	}

	// Without backups
	parser := NewNexusParser(dir)
	sessions, _ := parser.ParseAll()
	if len(sessions) != 1 {
		t.Errorf("without backups, expected 1 session, got %d", len(sessions))
	}

	// With backups
	parser = NewNexusParser(dir).WithBackups(true)
	sessions, errors := parser.ParseAll()

	if len(errors) > 0 {
		t.Errorf("unexpected errors: %v", errors)
	}
	if len(sessions) != 2 {
		t.Fatalf("with backups, expected 2 sessions, got %d", len(sessions))
	}

	// Find the backup session
	var backupSession *ParsedSession
	for _, s := range sessions {
		if s.MessageMetadata["archive_source"] != "" {
			backupSession = s
			break
		}
	}

	if backupSession == nil {
		t.Fatal("expected to find a backup session")
	}

	if len(backupSession.Messages) != 2 {
		t.Errorf("expected 2 messages in backup, got %d", len(backupSession.Messages))
	}
	if backupSession.Messages[0].Content != "Before compaction" {
		t.Errorf("expected 'Before compaction', got '%s'", backupSession.Messages[0].Content)
	}
}

func TestPiAgentParser_InfersProject(t *testing.T) {
	dir := t.TempDir()

	// Session with CWD that can infer project (matches /Users/xxx/Desktop/projects/xxx pattern)
	sessionContent := `{"type":"session","version":"1.0","id":"project-test","timestamp":"2026-01-21T12:00:00Z","cwd":"/Users/tyler/Desktop/projects/myapp"}
{"type":"user","timestamp":"2026-01-21T12:00:01Z","sessionId":"project-test","uuid":"msg-1","message":{"role":"user","content":"Test"}}
`
	err := os.WriteFile(filepath.Join(dir, "project-test.jsonl"), []byte(sessionContent), 0644)
	if err != nil {
		t.Fatal(err)
	}

	parser := NewClawdbotParser(dir)
	sessions, _ := parser.ParseAll()

	if len(sessions) != 1 {
		t.Fatalf("expected 1 session, got %d", len(sessions))
	}

	// Project should be inferred from CWD
	if sessions[0].Session.Project != "myapp" {
		t.Errorf("expected project 'myapp', got '%s'", sessions[0].Session.Project)
	}
}

func TestPiAgentParser_SkipsInvalidFiles(t *testing.T) {
	dir := t.TempDir()

	// Valid session
	validContent := `{"type":"session","version":"1.0","id":"valid","timestamp":"2026-01-21T12:00:00Z","cwd":"/test"}
{"type":"user","timestamp":"2026-01-21T12:00:01Z","sessionId":"valid","uuid":"msg-1","message":{"role":"user","content":"Valid"}}
`
	os.WriteFile(filepath.Join(dir, "valid.jsonl"), []byte(validContent), 0644)

	// Invalid JSON file
	os.WriteFile(filepath.Join(dir, "invalid.jsonl"), []byte("not json"), 0644)

	// Empty file (no session header)
	os.WriteFile(filepath.Join(dir, "empty.jsonl"), []byte(""), 0644)

	// Non-JSONL file (should be ignored)
	os.WriteFile(filepath.Join(dir, "readme.txt"), []byte("ignore me"), 0644)

	parser := NewNexusParser(dir)
	sessions, errors := parser.ParseAll()

	// Should get valid session
	if len(sessions) != 1 {
		t.Errorf("expected 1 valid session, got %d", len(sessions))
	}

	// Should not have fatal errors (invalid lines are skipped)
	// The empty file returns nil session (not an error)
	if len(errors) > 0 {
		t.Logf("got %d errors (may be expected for malformed files)", len(errors))
	}
}
