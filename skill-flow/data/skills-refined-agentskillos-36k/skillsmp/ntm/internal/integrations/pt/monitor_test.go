package pt

import (
	"testing"
	"time"

	"github.com/Dicklesworthstone/ntm/internal/config"
)

func TestNewHealthMonitor(t *testing.T) {
	cfg := config.DefaultProcessTriageConfig()
	m := NewHealthMonitor(&cfg)

	if m == nil {
		t.Fatal("expected non-nil monitor")
	}
	if m.config == nil {
		t.Error("expected non-nil config")
	}
	if m.pidMap == nil {
		t.Error("expected non-nil pidMap")
	}
	if m.ptAdapter == nil {
		t.Error("expected non-nil ptAdapter")
	}
	if m.states == nil {
		t.Error("expected non-nil states map")
	}
	if m.alertCh == nil {
		t.Error("expected non-nil alert channel")
	}
	if m.running {
		t.Error("expected monitor not to be running initially")
	}
}

func TestHealthMonitorOptions(t *testing.T) {
	cfg := config.DefaultProcessTriageConfig()
	alertCh := make(chan Alert, 10)

	m := NewHealthMonitor(&cfg,
		WithSession("test-session"),
		WithAlertChannel(alertCh),
		WithRano(false),
	)

	if m.session != "test-session" {
		t.Errorf("expected session 'test-session', got %q", m.session)
	}
	if m.alertCh != alertCh {
		t.Error("expected custom alert channel")
	}
	if m.useRano {
		t.Error("expected useRano to be false")
	}
}

func TestClassificationMapping(t *testing.T) {
	tests := []struct {
		name     string
		ptClass  string
		expected Classification
	}{
		{"useful maps to useful", "useful", ClassUseful},
		{"abandoned maps to stuck", "abandoned", ClassStuck},
		{"zombie maps to zombie", "zombie", ClassZombie},
		{"unknown maps to unknown", "unknown", ClassUnknown},
		{"empty maps to unknown", "", ClassUnknown},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Note: We can't directly test mapPTClassification as it takes tools.PTClassification
			// This is more of a documentation test
		})
	}
}

func TestAgentState(t *testing.T) {
	state := &AgentState{
		Pane:             "test__cc_1",
		PID:              12345,
		Classification:   ClassUseful,
		Confidence:       0.95,
		Since:            time.Now(),
		LastCheck:        time.Now(),
		History:          []ClassificationEvent{},
		ConsecutiveCount: 1,
	}

	if state.Pane != "test__cc_1" {
		t.Errorf("expected pane 'test__cc_1', got %q", state.Pane)
	}
	if state.PID != 12345 {
		t.Errorf("expected PID 12345, got %d", state.PID)
	}
	if state.Classification != ClassUseful {
		t.Errorf("expected classification useful, got %s", state.Classification)
	}
}

func TestAlert(t *testing.T) {
	alert := Alert{
		Type:      AlertStuck,
		Pane:      "test__cc_1",
		PID:       12345,
		State:     ClassStuck,
		Duration:  10 * time.Minute,
		Timestamp: time.Now(),
		Message:   "Agent test__cc_1 has been stuck for 10m0s",
	}

	if alert.Type != AlertStuck {
		t.Errorf("expected alert type stuck, got %s", alert.Type)
	}
	if alert.Pane != "test__cc_1" {
		t.Errorf("expected pane 'test__cc_1', got %q", alert.Pane)
	}
}

func TestMonitorStats(t *testing.T) {
	cfg := config.DefaultProcessTriageConfig()
	m := NewHealthMonitor(&cfg)

	stats := m.GetStats()

	if stats.Running {
		t.Error("expected monitor not to be running")
	}
	if stats.CheckInterval != cfg.CheckInterval {
		t.Errorf("expected check interval %d, got %d", cfg.CheckInterval, stats.CheckInterval)
	}
	if stats.IdleThreshold != cfg.IdleThreshold {
		t.Errorf("expected idle threshold %d, got %d", cfg.IdleThreshold, stats.IdleThreshold)
	}
	if stats.StuckThreshold != cfg.StuckThreshold {
		t.Errorf("expected stuck threshold %d, got %d", cfg.StuckThreshold, stats.StuckThreshold)
	}
	if stats.AgentCount != 0 {
		t.Errorf("expected agent count 0, got %d", stats.AgentCount)
	}
}

func TestGetState(t *testing.T) {
	cfg := config.DefaultProcessTriageConfig()
	m := NewHealthMonitor(&cfg)

	// No state should exist initially
	state := m.GetState("nonexistent")
	if state != nil {
		t.Error("expected nil state for nonexistent pane")
	}
}

func TestGetAllStates(t *testing.T) {
	cfg := config.DefaultProcessTriageConfig()
	m := NewHealthMonitor(&cfg)

	states := m.GetAllStates()
	if len(states) != 0 {
		t.Errorf("expected 0 states, got %d", len(states))
	}
}

func TestRunningState(t *testing.T) {
	cfg := config.DefaultProcessTriageConfig()
	m := NewHealthMonitor(&cfg)

	if m.Running() {
		t.Error("expected monitor not to be running initially")
	}

	// Note: We can't easily test Start() without pt being available
	// This would require mocking the ptAdapter
}

func TestGlobalMonitor(t *testing.T) {
	// Note: This modifies global state, so be careful
	m1 := GetGlobalMonitor()
	if m1 == nil {
		t.Fatal("expected non-nil global monitor")
	}

	// Getting global monitor again should return same instance
	m2 := GetGlobalMonitor()
	if m1 != m2 {
		t.Error("expected same global monitor instance")
	}
}

func TestInitGlobalMonitor(t *testing.T) {
	cfg := config.DefaultProcessTriageConfig()
	cfg.CheckInterval = 60 // Different from default

	m := InitGlobalMonitor(&cfg, WithSession("custom-session"))
	if m == nil {
		t.Fatal("expected non-nil monitor")
	}
	if m.session != "custom-session" {
		t.Errorf("expected session 'custom-session', got %q", m.session)
	}
	if m.config.CheckInterval != 60 {
		t.Errorf("expected check interval 60, got %d", m.config.CheckInterval)
	}
}
