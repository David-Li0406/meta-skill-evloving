package robot

import (
	"os"
	"path/filepath"
	"testing"
)

func TestReadAuditLogStats_EmptyLog(t *testing.T) {
	tmpDir := t.TempDir()
	logPath := filepath.Join(tmpDir, "empty.jsonl")

	// Create empty file
	if err := os.WriteFile(logPath, []byte{}, 0644); err != nil {
		t.Fatalf("Failed to create empty log: %v", err)
	}

	count, lastBlocked := readAuditLogStats(logPath)

	if count != 0 {
		t.Errorf("Expected count 0, got %d", count)
	}
	if lastBlocked != nil {
		t.Errorf("Expected nil lastBlocked, got %+v", lastBlocked)
	}
}

func TestReadAuditLogStats_WithEntries(t *testing.T) {
	tmpDir := t.TempDir()
	logPath := filepath.Join(tmpDir, "test.jsonl")

	// Create log with entries
	content := `{"timestamp":"2024-01-15T10:30:00Z","event":"command_blocked","command":"rm -rf /","pane":"agent-1","session":"test","rule":"rm_rf_root","dcg_output":"Blocked"}
{"timestamp":"2024-01-15T10:31:00Z","event":"command_blocked","command":"git reset --hard","pane":"agent-2","session":"test","rule":"git_reset","dcg_output":"Blocked"}
`
	if err := os.WriteFile(logPath, []byte(content), 0644); err != nil {
		t.Fatalf("Failed to create log: %v", err)
	}

	count, lastBlocked := readAuditLogStats(logPath)

	if count != 2 {
		t.Errorf("Expected count 2, got %d", count)
	}
	if lastBlocked == nil {
		t.Fatal("Expected non-nil lastBlocked")
	}
	if lastBlocked.Command != "git reset --hard" {
		t.Errorf("Expected command 'git reset --hard', got '%s'", lastBlocked.Command)
	}
	if lastBlocked.Pane != "agent-2" {
		t.Errorf("Expected pane 'agent-2', got '%s'", lastBlocked.Pane)
	}
}

func TestReadAuditLogStats_NonExistent(t *testing.T) {
	count, lastBlocked := readAuditLogStats("/nonexistent/path/log.jsonl")

	if count != 0 {
		t.Errorf("Expected count 0 for non-existent file, got %d", count)
	}
	if lastBlocked != nil {
		t.Errorf("Expected nil lastBlocked for non-existent file")
	}
}

func TestGetDefaultAuditLogPath(t *testing.T) {
	path := getDefaultAuditLogPath()

	if path == "" {
		t.Error("Expected non-empty default audit log path")
	}

	// Should contain "ntm" and "dcg-audit.jsonl"
	if filepath.Base(path) != "dcg-audit.jsonl" {
		t.Errorf("Expected path to end with dcg-audit.jsonl, got %s", filepath.Base(path))
	}
}
