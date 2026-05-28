package notify

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"os"
	"path/filepath"
	"testing"
	"time"
)

func TestDefaultConfig(t *testing.T) {
	cfg := DefaultConfig()
	if !cfg.Enabled {
		t.Error("Default config should be enabled")
	}
	if !cfg.Desktop.Enabled {
		t.Error("Default desktop should be enabled")
	}
}

func TestNewNotifier(t *testing.T) {
	cfg := DefaultConfig()
	n := New(cfg)
	if n == nil {
		t.Fatal("New returned nil")
	}
	if !n.enabledSet[EventAgentError] {
		t.Error("EventAgentError should be enabled")
	}
}

func TestNotifyDisabled(t *testing.T) {
	cfg := Config{Enabled: false}
	n := New(cfg)
	err := n.Notify(Event{Type: EventAgentError})
	if err != nil {
		t.Errorf("Notify failed when disabled: %v", err)
	}
}

func TestWebhookNotification(t *testing.T) {
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Method != "POST" {
			t.Errorf("Expected POST, got %s", r.Method)
		}
		var payload map[string]string
		json.NewDecoder(r.Body).Decode(&payload)
		if payload["text"] != "NTM: agent.error - Test error" {
			t.Errorf("Unexpected payload: %v", payload)
		}
	}))
	defer ts.Close()

	cfg := Config{
		Enabled: true,
		Events:  []string{"agent.error"},
		Webhook: WebhookConfig{
			Enabled:  true,
			URL:      ts.URL,
			Template: `{"text": "NTM: {{.Type}} - {{.Message}}"}`,
		},
	}

	n := New(cfg)
	err := n.Notify(Event{
		Type:    EventAgentError,
		Message: "Test error",
	})
	if err != nil {
		t.Errorf("Notify failed: %v", err)
	}
}

func TestLogNotification(t *testing.T) {
	tmpDir := t.TempDir()
	logPath := filepath.Join(tmpDir, "test.log")

	cfg := Config{
		Enabled: true,
		Events:  []string{"agent.error"},
		Log: LogConfig{
			Enabled: true,
			Path:    logPath,
		},
	}

	n := New(cfg)
	err := n.Notify(Event{
		Type:      EventAgentError,
		Message:   "Test log",
		Timestamp: time.Now(),
	})
	if err != nil {
		t.Fatalf("Notify failed: %v", err)
	}

	content, _ := os.ReadFile(logPath)
	if len(content) == 0 {
		t.Error("Log file is empty")
	}
}

func TestHelperFunctions(t *testing.T) {
	evt := NewRateLimitEvent("sess", "p1", "cc", 30)
	if evt.Type != EventRateLimit {
		t.Errorf("NewRateLimitEvent type = %v", evt.Type)
	}
	if evt.Details["wait_seconds"] != "30" {
		t.Errorf("NewRateLimitEvent details = %v", evt.Details)
	}

	evt = NewAgentCrashedEvent("sess", "p1", "cc")
	if evt.Type != EventAgentCrashed {
		t.Errorf("NewAgentCrashedEvent type = %v", evt.Type)
	}

	evt = NewAgentErrorEvent("sess", "p1", "cc", "error")
	if evt.Type != EventAgentError {
		t.Errorf("NewAgentErrorEvent type = %v", evt.Type)
	}

	evt = NewHealthDegradedEvent("sess", 5, 1, 0)
	if evt.Type != EventHealthDegraded {
		t.Errorf("NewHealthDegradedEvent type = %v", evt.Type)
	}

	evt = NewRotationNeededEvent("sess", 1, "cc", "cmd")
	if evt.Type != EventRotationNeeded {
		t.Errorf("NewRotationNeededEvent type = %v", evt.Type)
	}
}

func TestFileBoxNotification(t *testing.T) {
	tmpDir := t.TempDir()

	cfg := Config{
		Enabled: true,
		Events:  []string{"agent.error"},
		FileBox: FileBoxConfig{
			Enabled: true,
			Path:    tmpDir,
		},
	}

	n := New(cfg)
	testTime := time.Date(2026, 1, 4, 10, 30, 0, 0, time.UTC)
	err := n.Notify(Event{
		Type:      EventAgentError,
		Message:   "Test file inbox",
		Session:   "test-session",
		Agent:     "cc",
		Timestamp: testTime,
		Details:   map[string]string{"key": "value"},
	})
	if err != nil {
		t.Fatalf("Notify failed: %v", err)
	}

	// Check that file was created
	expectedFile := filepath.Join(tmpDir, "2026-01-04_10-30-00_agent_error.md")
	content, err := os.ReadFile(expectedFile)
	if err != nil {
		t.Fatalf("Failed to read inbox file: %v", err)
	}

	contentStr := string(content)
	if !contains(contentStr, "# agent.error") {
		t.Error("File should contain event type header")
	}
	if !contains(contentStr, "Test file inbox") {
		t.Error("File should contain message")
	}
	if !contains(contentStr, "test-session") {
		t.Error("File should contain session")
	}
	if !contains(contentStr, "**key:** value") {
		t.Error("File should contain details")
	}
}

func TestRoutingRules(t *testing.T) {
	tmpDir := t.TempDir()
	logPath := filepath.Join(tmpDir, "test.log")
	inboxPath := filepath.Join(tmpDir, "inbox")

	cfg := Config{
		Enabled: true,
		Events:  []string{"agent.error", "agent.crashed"},
		Routing: map[string][]string{
			"agent.error":   {"log"},     // Only log for errors
			"agent.crashed": {"filebox"}, // Only filebox for crashes
		},
		Log: LogConfig{
			Enabled: true,
			Path:    logPath,
		},
		FileBox: FileBoxConfig{
			Enabled: true,
			Path:    inboxPath,
		},
	}

	n := New(cfg)

	// Send error - should go to log only
	err := n.Notify(Event{
		Type:      EventAgentError,
		Message:   "Error event",
		Timestamp: time.Now(),
	})
	if err != nil {
		t.Fatalf("Notify failed: %v", err)
	}

	// Check log was written
	logContent, _ := os.ReadFile(logPath)
	if !contains(string(logContent), "Error event") {
		t.Error("Log should contain error event")
	}

	// Check inbox was NOT written for error
	files, _ := os.ReadDir(inboxPath)
	if len(files) > 0 {
		t.Error("Inbox should be empty for error event (routed to log only)")
	}
}

func TestPrimaryFallback(t *testing.T) {
	tmpDir := t.TempDir()
	inboxPath := filepath.Join(tmpDir, "inbox")

	// Create config with primary=webhook (disabled) and fallback=filebox (enabled)
	cfg := Config{
		Enabled:  true,
		Events:   []string{"agent.error"},
		Primary:  "webhook", // Webhook is not enabled, so should fallback
		Fallback: "filebox",
		Webhook: WebhookConfig{
			Enabled: false, // Disabled - will fail
		},
		FileBox: FileBoxConfig{
			Enabled: true,
			Path:    inboxPath,
		},
	}

	n := New(cfg)
	err := n.Notify(Event{
		Type:      EventAgentError,
		Message:   "Fallback test",
		Timestamp: time.Now(),
	})
	if err != nil {
		t.Fatalf("Notify failed: %v", err)
	}

	// Fallback to filebox should have worked
	files, _ := os.ReadDir(inboxPath)
	if len(files) == 0 {
		t.Error("Fallback to filebox should have created a file")
	}
}

func TestEnvVarExpansion(t *testing.T) {
	// Set test env var
	os.Setenv("TEST_WEBHOOK_URL", "https://example.com/hook")
	defer os.Unsetenv("TEST_WEBHOOK_URL")

	cfg := Config{
		Enabled: true,
		Events:  []string{"agent.error"},
		Webhook: WebhookConfig{
			Enabled: true,
			URL:     "${TEST_WEBHOOK_URL}",
		},
	}

	n := New(cfg)
	if n.config.Webhook.URL != "https://example.com/hook" {
		t.Errorf("Env var not expanded: got %s", n.config.Webhook.URL)
	}
}

func TestChannelConstants(t *testing.T) {
	// Verify channel constants are defined
	channels := []ChannelName{
		ChannelDesktop,
		ChannelWebhook,
		ChannelShell,
		ChannelLog,
		ChannelFileBox,
	}

	expected := []string{"desktop", "webhook", "shell", "log", "filebox"}
	for i, ch := range channels {
		if string(ch) != expected[i] {
			t.Errorf("Channel %d: got %s, want %s", i, ch, expected[i])
		}
	}
}

func contains(s, substr string) bool {
	return len(s) >= len(substr) && (s == substr || len(s) > 0 && containsAt(s, substr, 0))
}

func containsAt(s, substr string, start int) bool {
	for i := start; i <= len(s)-len(substr); i++ {
		if s[i:i+len(substr)] == substr {
			return true
		}
	}
	return false
}
