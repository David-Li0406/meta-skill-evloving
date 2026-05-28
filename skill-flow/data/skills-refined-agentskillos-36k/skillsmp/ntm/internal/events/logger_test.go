package events

import (
	"bytes"
	"encoding/json"
	"os"
	"path/filepath"
	"testing"
	"time"
)

func TestNewLogger(t *testing.T) {
	// Create temp directory
	tmpDir := t.TempDir()
	logPath := filepath.Join(tmpDir, "events.jsonl")

	logger, err := NewLogger(LoggerOptions{
		Path:          logPath,
		RetentionDays: 30,
		Enabled:       true,
	})
	if err != nil {
		t.Fatalf("NewLogger failed: %v", err)
	}
	defer logger.Close()

	if logger.file == nil {
		t.Error("Expected file to be opened")
	}
}

func TestNewLogger_Disabled(t *testing.T) {
	logger, err := NewLogger(LoggerOptions{
		Enabled: false,
	})
	if err != nil {
		t.Fatalf("NewLogger failed: %v", err)
	}

	if logger.file != nil {
		t.Error("Expected file to be nil when disabled")
	}

	// Logging should be a no-op
	err = logger.Log(NewEvent(EventSessionCreate, "test", nil))
	if err != nil {
		t.Errorf("Log on disabled logger should not error: %v", err)
	}
}

func TestLogger_Log(t *testing.T) {
	tmpDir := t.TempDir()
	logPath := filepath.Join(tmpDir, "events.jsonl")

	logger, err := NewLogger(LoggerOptions{
		Path:    logPath,
		Enabled: true,
	})
	if err != nil {
		t.Fatalf("NewLogger failed: %v", err)
	}
	defer logger.Close()

	// Log an event
	event := NewEvent(EventSessionCreate, "myproject", map[string]interface{}{
		"claude_count": 2,
		"codex_count":  1,
	})
	if err := logger.Log(event); err != nil {
		t.Fatalf("Log failed: %v", err)
	}

	// Close and read the file
	logger.Close()

	data, err := os.ReadFile(logPath)
	if err != nil {
		t.Fatalf("ReadFile failed: %v", err)
	}

	// Parse the logged event
	var logged Event
	if err := json.Unmarshal(data, &logged); err != nil {
		t.Fatalf("Unmarshal failed: %v", err)
	}

	if logged.Type != EventSessionCreate {
		t.Errorf("Type = %q, want %q", logged.Type, EventSessionCreate)
	}

	if logged.Session != "myproject" {
		t.Errorf("Session = %q, want %q", logged.Session, "myproject")
	}
}

func TestLogger_LogEvent(t *testing.T) {
	tmpDir := t.TempDir()
	logPath := filepath.Join(tmpDir, "events.jsonl")

	logger, err := NewLogger(LoggerOptions{
		Path:    logPath,
		Enabled: true,
	})
	if err != nil {
		t.Fatalf("NewLogger failed: %v", err)
	}
	defer logger.Close()

	// Log using convenience method
	err = logger.LogEvent(EventPromptSend, "test-session", PromptSendData{
		TargetCount:  3,
		PromptLength: 100,
		Template:     "code_review",
	})
	if err != nil {
		t.Fatalf("LogEvent failed: %v", err)
	}

	logger.Close()

	data, err := os.ReadFile(logPath)
	if err != nil {
		t.Fatalf("ReadFile failed: %v", err)
	}

	var logged Event
	if err := json.Unmarshal(data, &logged); err != nil {
		t.Fatalf("Unmarshal failed: %v", err)
	}

	if logged.Type != EventPromptSend {
		t.Errorf("Type = %q, want %q", logged.Type, EventPromptSend)
	}

	if tc, ok := logged.Data["target_count"].(float64); !ok || int(tc) != 3 {
		t.Errorf("target_count = %v, want 3", logged.Data["target_count"])
	}
}

func TestLogger_MultipleEvents(t *testing.T) {
	tmpDir := t.TempDir()
	logPath := filepath.Join(tmpDir, "events.jsonl")

	logger, err := NewLogger(LoggerOptions{
		Path:    logPath,
		Enabled: true,
	})
	if err != nil {
		t.Fatalf("NewLogger failed: %v", err)
	}

	// Log multiple events
	for i := 0; i < 5; i++ {
		logger.LogEvent(EventSessionCreate, "session-"+string(rune('a'+i)), nil)
	}
	logger.Close()

	// Read and count lines
	data, err := os.ReadFile(logPath)
	if err != nil {
		t.Fatalf("ReadFile failed: %v", err)
	}

	lines := bytes.Split(data, []byte("\n"))
	nonEmpty := 0
	for _, line := range lines {
		if len(line) > 0 {
			nonEmpty++
		}
	}

	if nonEmpty != 5 {
		t.Errorf("Got %d events, want 5", nonEmpty)
	}
}

func TestRotateOldEntries(t *testing.T) {
	tmpDir := t.TempDir()
	logPath := filepath.Join(tmpDir, "events.jsonl")

	// Create file with old and new entries
	now := time.Now().UTC()
	old := now.AddDate(0, 0, -35)   // 35 days ago
	recent := now.AddDate(0, 0, -5) // 5 days ago

	entries := []Event{
		{Timestamp: old, Type: EventSessionCreate, Session: "old"},
		{Timestamp: recent, Type: EventSessionCreate, Session: "recent"},
		{Timestamp: now, Type: EventSessionCreate, Session: "now"},
	}

	var data []byte
	for _, e := range entries {
		line, _ := json.Marshal(e)
		data = append(data, line...)
		data = append(data, '\n')
	}

	if err := os.WriteFile(logPath, data, 0644); err != nil {
		t.Fatalf("WriteFile failed: %v", err)
	}

	// Create logger and trigger rotation
	logger, err := NewLogger(LoggerOptions{
		Path:          logPath,
		RetentionDays: 30,
		Enabled:       true,
	})
	if err != nil {
		t.Fatalf("NewLogger failed: %v", err)
	}

	// Force rotation
	logger.lastRotation = time.Time{} // Reset to trigger rotation
	if err := logger.rotateOldEntries(); err != nil {
		t.Fatalf("rotateOldEntries failed: %v", err)
	}
	logger.Close()

	// Read and verify
	data, err = os.ReadFile(logPath)
	if err != nil {
		t.Fatalf("ReadFile failed: %v", err)
	}

	lines := bytes.Split(data, []byte("\n"))
	nonEmpty := 0
	for _, line := range lines {
		if len(line) > 0 {
			nonEmpty++
			var e Event
			json.Unmarshal(line, &e)
			if e.Session == "old" {
				t.Error("Old entry should have been rotated out")
			}
		}
	}

	if nonEmpty != 2 {
		t.Errorf("Got %d entries after rotation, want 2", nonEmpty)
	}
}

func TestExpandPath(t *testing.T) {
	tests := []struct {
		input string
		want  string
	}{
		{"/absolute/path", "/absolute/path"},
		{"relative/path", "relative/path"},
	}

	for _, tt := range tests {
		got := expandPath(tt.input)
		if got != tt.want {
			t.Errorf("expandPath(%q) = %q, want %q", tt.input, got, tt.want)
		}
	}

	// Test ~ expansion (can't test exact value since it depends on user)
	expanded := expandPath("~/test")
	if expanded == "~/test" {
		t.Error("expandPath should have expanded ~")
	}
}

func TestToMap(t *testing.T) {
	data := SessionCreateData{
		ClaudeCount: 2,
		CodexCount:  1,
		WorkDir:     "/path",
	}

	m := ToMap(data)

	if m["claude_count"] != 2 {
		t.Errorf("claude_count = %v, want 2", m["claude_count"])
	}

	if m["codex_count"] != 1 {
		t.Errorf("codex_count = %v, want 1", m["codex_count"])
	}
}

func TestNewEvent(t *testing.T) {
	before := time.Now()
	event := NewEvent(EventSessionCreate, "test", map[string]interface{}{"key": "value"})
	after := time.Now()

	if event.Type != EventSessionCreate {
		t.Errorf("Type = %q, want %q", event.Type, EventSessionCreate)
	}

	if event.Session != "test" {
		t.Errorf("Session = %q, want %q", event.Session, "test")
	}

	if event.Timestamp.Before(before) || event.Timestamp.After(after) {
		t.Error("Timestamp should be between before and after")
	}
}
