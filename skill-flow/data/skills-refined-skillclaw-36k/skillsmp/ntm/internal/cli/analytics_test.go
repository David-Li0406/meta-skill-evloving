package cli

import (
	"encoding/json"
	"os"
	"path/filepath"
	"testing"
	"time"

	"github.com/Dicklesworthstone/ntm/internal/events"
)

func TestReadEvents(t *testing.T) {
	// Create temp directory
	tmpDir := t.TempDir()
	logPath := filepath.Join(tmpDir, "events.jsonl")

	// Write test events
	now := time.Now().UTC()
	testEvents := []events.Event{
		{Timestamp: now.AddDate(0, 0, -5), Type: events.EventSessionCreate, Session: "test1", Data: map[string]interface{}{"claude_count": float64(2), "codex_count": float64(1)}},
		{Timestamp: now.AddDate(0, 0, -3), Type: events.EventPromptSend, Session: "test1", Data: map[string]interface{}{"prompt_length": float64(100), "target_types": "cc"}},
		{Timestamp: now.AddDate(0, 0, -40), Type: events.EventSessionCreate, Session: "old", Data: map[string]interface{}{"claude_count": float64(1)}},
	}

	var data []byte
	for _, e := range testEvents {
		line, _ := json.Marshal(e)
		data = append(data, line...)
		data = append(data, '\n')
	}

	if err := os.WriteFile(logPath, data, 0644); err != nil {
		t.Fatalf("WriteFile failed: %v", err)
	}

	// Test reading with 30-day cutoff
	cutoff := now.AddDate(0, 0, -30)
	eventList, err := readEvents(logPath, cutoff)
	if err != nil {
		t.Fatalf("readEvents failed: %v", err)
	}

	// Should have 2 events (not the old one)
	if len(eventList) != 2 {
		t.Errorf("Got %d events, want 2", len(eventList))
	}
}

func TestAggregateStats(t *testing.T) {
	now := time.Now().UTC()
	cutoff := now.AddDate(0, 0, -30)

	testEvents := []events.Event{
		{Timestamp: now.AddDate(0, 0, -5), Type: events.EventSessionCreate, Session: "test1", Data: map[string]interface{}{"claude_count": float64(2), "codex_count": float64(1)}},
		{Timestamp: now.AddDate(0, 0, -3), Type: events.EventPromptSend, Session: "test1", Data: map[string]interface{}{"prompt_length": float64(100), "target_types": "cc"}},
		{Timestamp: now.AddDate(0, 0, -2), Type: events.EventPromptSend, Session: "test1", Data: map[string]interface{}{"prompt_length": float64(200), "target_types": "all"}},
		{Timestamp: now.AddDate(0, 0, -1), Type: events.EventError, Session: "test1", Data: map[string]interface{}{"error_type": "spawn_failed"}},
	}

	stats := aggregateStats(testEvents, 30, "", cutoff)

	if stats.TotalSessions != 1 {
		t.Errorf("TotalSessions = %d, want 1", stats.TotalSessions)
	}

	if stats.TotalAgents != 3 {
		t.Errorf("TotalAgents = %d, want 3", stats.TotalAgents)
	}

	if stats.TotalPrompts != 2 {
		t.Errorf("TotalPrompts = %d, want 2", stats.TotalPrompts)
	}

	if stats.TotalCharsSent != 300 {
		t.Errorf("TotalCharsSent = %d, want 300", stats.TotalCharsSent)
	}

	if stats.ErrorCount != 1 {
		t.Errorf("ErrorCount = %d, want 1", stats.ErrorCount)
	}

	// Check agent breakdown
	if claude, ok := stats.AgentBreakdown["claude"]; ok {
		if claude.Count != 2 {
			t.Errorf("claude.Count = %d, want 2", claude.Count)
		}
	} else {
		t.Error("Missing claude in agent breakdown")
	}
}

func TestParseTargetTypes(t *testing.T) {
	tests := []struct {
		input    string
		expected []string
	}{
		{"cc", []string{"claude"}},
		{"cod", []string{"codex"}},
		{"gmi", []string{"gemini"}},
		{"cc,cod", []string{"claude", "codex"}},
		{"all", []string{"claude", "codex", "gemini"}},
		{"agents", []string{"claude", "codex", "gemini"}},
		{"", []string{}},
	}

	for _, tt := range tests {
		result := parseTargetTypes(tt.input)
		if len(result) != len(tt.expected) {
			t.Errorf("parseTargetTypes(%q) = %v, want %v", tt.input, result, tt.expected)
		}
	}
}

func TestBuildSessionDetails(t *testing.T) {
	now := time.Now().UTC()
	testEvents := []events.Event{
		{Timestamp: now.AddDate(0, 0, -5), Type: events.EventSessionCreate, Session: "test1", Data: map[string]interface{}{"claude_count": float64(2)}},
		{Timestamp: now.AddDate(0, 0, -3), Type: events.EventPromptSend, Session: "test1", Data: map[string]interface{}{}},
		{Timestamp: now.AddDate(0, 0, -2), Type: events.EventPromptSend, Session: "test1", Data: map[string]interface{}{}},
		{Timestamp: now.AddDate(0, 0, -1), Type: events.EventSessionCreate, Session: "test2", Data: map[string]interface{}{"codex_count": float64(1)}},
	}

	details := buildSessionDetails(testEvents)

	if len(details) != 2 {
		t.Errorf("Got %d sessions, want 2", len(details))
	}

	// Test2 should be first (more recent)
	if len(details) > 0 && details[0].Name != "test2" {
		t.Errorf("First session = %q, want 'test2'", details[0].Name)
	}

	// Test1 should have 2 prompts
	for _, d := range details {
		if d.Name == "test1" && d.PromptCount != 2 {
			t.Errorf("test1 prompts = %d, want 2", d.PromptCount)
		}
	}
}
