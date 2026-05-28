package dashboard

import (
	"errors"
	"testing"
	"time"

	tea "github.com/charmbracelet/bubbletea"

	"github.com/Dicklesworthstone/ntm/internal/alerts"
	"github.com/Dicklesworthstone/ntm/internal/bv"
	"github.com/Dicklesworthstone/ntm/internal/cass"
	"github.com/Dicklesworthstone/ntm/internal/config"
	"github.com/Dicklesworthstone/ntm/internal/history"
	"github.com/Dicklesworthstone/ntm/internal/tmux"
	"github.com/Dicklesworthstone/ntm/internal/tracker"
	"github.com/Dicklesworthstone/ntm/internal/tui/dashboard/panels"
)

func TestFetchBeadsCmd_NoBv(t *testing.T) {
	t.Parallel()

	m := newTestModel(120)
	cmd := m.fetchBeadsCmd()

	msg := cmd()
	beadsMsg, ok := msg.(BeadsUpdateMsg)
	if !ok {
		t.Fatalf("expected BeadsUpdateMsg, got %T", msg)
	}

	// When bv is not installed or not available, we expect an error
	// This is the expected behavior for environments without bv
	if beadsMsg.Err == nil {
		// bv might be installed in test environment - verify Summary is valid
		if !beadsMsg.Summary.Available && beadsMsg.Summary.Reason == "" {
			t.Error("expected either error or available summary")
		}
	}
}

func TestFetchAlertsCmd(t *testing.T) {
	t.Parallel()

	m := newTestModel(120)
	cmd := m.fetchAlertsCmd()

	msg := cmd()
	alertsMsg, ok := msg.(AlertsUpdateMsg)
	if !ok {
		t.Fatalf("expected AlertsUpdateMsg, got %T", msg)
	}

	// Should return without panic; Alerts may be nil or empty in test env
	// We just verify the command completes and returns correct message type
	_ = alertsMsg.Alerts
}

func TestFetchAlertsCmd_WithConfig(t *testing.T) {
	t.Parallel()

	m := newTestModel(120)
	// Set a minimal config
	m.cfg = &config.Config{
		Alerts: config.AlertsConfig{
			Enabled:              true,
			AgentStuckMinutes:    15,
			DiskLowThresholdGB:   5.0,
			MailBacklogThreshold: 50,
			BeadStaleHours:       48,
			ResolvedPruneMinutes: 60,
		},
		ProjectsBase: "/tmp",
	}

	cmd := m.fetchAlertsCmd()
	msg := cmd()
	alertsMsg, ok := msg.(AlertsUpdateMsg)
	if !ok {
		t.Fatalf("expected AlertsUpdateMsg, got %T", msg)
	}

	// Should return without panic; Alerts may be nil or empty in test env
	// Config should influence alert checking, but we just verify completion
	_ = alertsMsg.Alerts
}

func TestFetchMetricsCmd_NoPanes(t *testing.T) {
	t.Parallel()

	m := newTestModel(120)
	m.panes = nil // No panes

	cmd := m.fetchMetricsCmd()
	msg := cmd()
	metricsMsg, ok := msg.(MetricsUpdateMsg)
	if !ok {
		t.Fatalf("expected MetricsUpdateMsg, got %T", msg)
	}

	// With no panes, should have zero metrics
	if metricsMsg.Data.TotalTokens != 0 {
		t.Errorf("expected 0 tokens with no panes, got %d", metricsMsg.Data.TotalTokens)
	}
	if metricsMsg.Data.TotalCost != 0 {
		t.Errorf("expected 0 cost with no panes, got %f", metricsMsg.Data.TotalCost)
	}
	if len(metricsMsg.Data.Agents) != 0 {
		t.Errorf("expected 0 agent metrics, got %d", len(metricsMsg.Data.Agents))
	}
}

func TestFetchMetricsCmd_SkipsUserPanes(t *testing.T) {
	t.Parallel()

	m := newTestModel(120)
	m.panes = []tmux.Pane{
		{ID: "user-pane", Type: tmux.AgentUser, Title: "user"},
	}

	cmd := m.fetchMetricsCmd()
	msg := cmd()
	metricsMsg, ok := msg.(MetricsUpdateMsg)
	if !ok {
		t.Fatalf("expected MetricsUpdateMsg, got %T", msg)
	}

	// User panes should be skipped
	if len(metricsMsg.Data.Agents) != 0 {
		t.Errorf("expected user panes to be skipped, got %d agents", len(metricsMsg.Data.Agents))
	}
}

func TestFetchHistoryCmd(t *testing.T) {
	t.Parallel()

	m := newTestModel(120)
	cmd := m.fetchHistoryCmd()

	msg := cmd()
	historyMsg, ok := msg.(HistoryUpdateMsg)
	if !ok {
		t.Fatalf("expected HistoryUpdateMsg, got %T", msg)
	}

	// Should return entries or an error (if history file doesn't exist)
	// We don't expect a panic either way
	_ = historyMsg
}

func TestFetchFileChangesCmd(t *testing.T) {
	t.Parallel()

	m := newTestModel(120)
	cmd := m.fetchFileChangesCmd()

	msg := cmd()
	fileChangeMsg, ok := msg.(FileChangeMsg)
	if !ok {
		t.Fatalf("expected FileChangeMsg, got %T", msg)
	}

	// Should return a slice (possibly empty) of changes
	// We don't expect a panic
	_ = fileChangeMsg
}

func TestFetchCASSContextCmd_NoCass(t *testing.T) {
	t.Parallel()

	m := newTestModel(120)
	m.session = "test-session"
	cmd := m.fetchCASSContextCmd()

	msg := cmd()
	cassMsg, ok := msg.(CASSContextMsg)
	if !ok {
		t.Fatalf("expected CASSContextMsg, got %T", msg)
	}

	// If CASS is not installed, we expect an error
	// If CASS is installed, we may get hits or empty hits
	_ = cassMsg
}

// Test that commands return tea.Cmd (not nil)
func TestCommandsReturnTeaCmd(t *testing.T) {
	t.Parallel()

	m := newTestModel(120)

	tests := []struct {
		name string
		cmd  func() tea.Cmd
	}{
		{"fetchBeadsCmd", func() tea.Cmd { return m.fetchBeadsCmd() }},
		{"fetchAlertsCmd", func() tea.Cmd { return m.fetchAlertsCmd() }},
		{"fetchMetricsCmd", func() tea.Cmd { return m.fetchMetricsCmd() }},
		{"fetchHistoryCmd", func() tea.Cmd { return m.fetchHistoryCmd() }},
		{"fetchFileChangesCmd", func() tea.Cmd { return m.fetchFileChangesCmd() }},
		{"fetchCASSContextCmd", func() tea.Cmd { return m.fetchCASSContextCmd() }},
	}

	for _, tc := range tests {
		tc := tc
		t.Run(tc.name, func(t *testing.T) {
			t.Parallel()
			cmd := tc.cmd()
			if cmd == nil {
				t.Errorf("%s returned nil tea.Cmd", tc.name)
			}
		})
	}
}

// Test message types are correct
func TestMessageTypes(t *testing.T) {
	t.Parallel()

	// Verify message types can be created and have expected fields
	t.Run("BeadsUpdateMsg", func(t *testing.T) {
		msg := BeadsUpdateMsg{
			Ready: []bv.BeadPreview{{ID: "task-1", Title: "Task 1"}, {ID: "task-2", Title: "Task 2"}},
		}
		if len(msg.Ready) != 2 {
			t.Errorf("expected 2 ready items, got %d", len(msg.Ready))
		}
	})

	t.Run("AlertsUpdateMsg", func(t *testing.T) {
		msg := AlertsUpdateMsg{
			Alerts: []alerts.Alert{
				{Type: alerts.AlertAgentStuck, Message: "test"},
			},
		}
		if len(msg.Alerts) != 1 {
			t.Errorf("expected 1 alert, got %d", len(msg.Alerts))
		}
	})

	t.Run("MetricsUpdateMsg", func(t *testing.T) {
		msg := MetricsUpdateMsg{
			Data: panels.MetricsData{
				TotalTokens: 1000,
				TotalCost:   0.01,
				Agents: []panels.AgentMetric{
					{Name: "cc_1", Tokens: 500},
				},
			},
		}
		if msg.Data.TotalTokens != 1000 {
			t.Errorf("expected 1000 tokens, got %d", msg.Data.TotalTokens)
		}
	})

	t.Run("HistoryUpdateMsg", func(t *testing.T) {
		msg := HistoryUpdateMsg{
			Entries: []history.HistoryEntry{
				{ID: "abc123", Prompt: "test prompt"},
			},
		}
		if len(msg.Entries) != 1 {
			t.Errorf("expected 1 entry, got %d", len(msg.Entries))
		}
	})

	t.Run("FileChangeMsg", func(t *testing.T) {
		msg := FileChangeMsg{
			Changes: []tracker.RecordedFileChange{
				{
					Timestamp: time.Now(),
					Session:   "test",
					Change:    tracker.FileChange{Path: "/tmp/file.go"},
				},
			},
		}
		if len(msg.Changes) != 1 {
			t.Errorf("expected 1 change, got %d", len(msg.Changes))
		}
	})

	t.Run("CASSContextMsg", func(t *testing.T) {
		msg := CASSContextMsg{
			Hits: []cass.SearchHit{
				{Title: "test hit", Score: 0.9},
			},
		}
		if len(msg.Hits) != 1 {
			t.Errorf("expected 1 hit, got %d", len(msg.Hits))
		}
	})
}

// Test error handling in messages
func TestMessageErrorHandling(t *testing.T) {
	t.Parallel()

	t.Run("BeadsUpdateMsg_WithError", func(t *testing.T) {
		msg := BeadsUpdateMsg{
			Err: errors.New("test error"),
		}
		// Error type check
		if msg.Err == nil {
			t.Error("expected error to be set")
		}
	})

	t.Run("HistoryUpdateMsg_WithError", func(t *testing.T) {
		msg := HistoryUpdateMsg{
			Err: errors.New("test error"),
		}
		if msg.Err == nil {
			t.Error("expected error to be set")
		}
	})

	t.Run("CASSContextMsg_WithError", func(t *testing.T) {
		msg := CASSContextMsg{
			Err: errors.New("test error"),
		}
		if msg.Err == nil {
			t.Error("expected error to be set")
		}
	})
}
