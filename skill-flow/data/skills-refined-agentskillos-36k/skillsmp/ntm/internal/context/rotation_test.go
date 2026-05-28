package context

import (
	"strings"
	"testing"
	"time"

	"github.com/Dicklesworthstone/ntm/internal/config"
	"github.com/Dicklesworthstone/ntm/internal/tmux"
)

// MockPaneSpawner is a test double for PaneSpawner.
type MockPaneSpawner struct {
	spawnedPanes []string
	killedPanes  []string
	sentKeys     map[string][]string
	panes        []tmux.Pane
	spawnError   error
	killError    error
	sendError    error
	panesError   error
}

func NewMockPaneSpawner() *MockPaneSpawner {
	return &MockPaneSpawner{
		sentKeys: make(map[string][]string),
		panes:    []tmux.Pane{},
	}
}

func (m *MockPaneSpawner) SpawnAgent(session, agentType string, index int, variant string, workDir string) (string, error) {
	if m.spawnError != nil {
		return "", m.spawnError
	}
	paneID := "%new-pane"
	m.spawnedPanes = append(m.spawnedPanes, paneID)
	return paneID, nil
}

func (m *MockPaneSpawner) KillPane(paneID string) error {
	if m.killError != nil {
		return m.killError
	}
	m.killedPanes = append(m.killedPanes, paneID)
	return nil
}

func (m *MockPaneSpawner) SendKeys(paneID, text string, enter bool) error {
	if m.sendError != nil {
		return m.sendError
	}
	m.sentKeys[paneID] = append(m.sentKeys[paneID], text)
	return nil
}

func (m *MockPaneSpawner) GetPanes(session string) ([]tmux.Pane, error) {
	if m.panesError != nil {
		return nil, m.panesError
	}
	return m.panes, nil
}

func TestNewRotator(t *testing.T) {
	t.Parallel()

	monitor := NewContextMonitor(DefaultMonitorConfig())
	spawner := NewMockPaneSpawner()

	cfg := RotatorConfig{
		Monitor: monitor,
		Spawner: spawner,
		Config:  config.DefaultContextRotationConfig(),
	}

	r := NewRotator(cfg)

	if r.monitor != monitor {
		t.Error("monitor not set correctly")
	}
	if r.spawner != spawner {
		t.Error("spawner not set correctly")
	}
	if r.compactor == nil {
		t.Error("compactor should be created automatically when monitor is provided")
	}
	if r.summary == nil {
		t.Error("summary generator should be created automatically")
	}
}

func TestCheckAndRotate_NoMonitor(t *testing.T) {
	t.Parallel()

	r := NewRotator(RotatorConfig{
		Config: config.DefaultContextRotationConfig(),
	})

	_, err := r.CheckAndRotate("test-session", "/tmp")
	if err == nil || !strings.Contains(err.Error(), "no monitor") {
		t.Errorf("expected 'no monitor' error, got: %v", err)
	}
}

func TestCheckAndRotate_NoSpawner(t *testing.T) {
	t.Parallel()

	monitor := NewContextMonitor(DefaultMonitorConfig())
	r := NewRotator(RotatorConfig{
		Monitor: monitor,
		Config:  config.DefaultContextRotationConfig(),
	})

	_, err := r.CheckAndRotate("test-session", "/tmp")
	if err == nil || !strings.Contains(err.Error(), "no spawner") {
		t.Errorf("expected 'no spawner' error, got: %v", err)
	}
}

func TestCheckAndRotate_Disabled(t *testing.T) {
	t.Parallel()

	monitor := NewContextMonitor(DefaultMonitorConfig())
	spawner := NewMockPaneSpawner()

	cfg := config.DefaultContextRotationConfig()
	cfg.Enabled = false

	r := NewRotator(RotatorConfig{
		Monitor: monitor,
		Spawner: spawner,
		Config:  cfg,
	})

	results, err := r.CheckAndRotate("test-session", "/tmp")
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}
	if results != nil {
		t.Error("expected nil results when disabled")
	}
}

func TestCheckAndRotate_NoAgentsAboveThreshold(t *testing.T) {
	t.Parallel()

	monitor := NewContextMonitor(DefaultMonitorConfig())
	spawner := NewMockPaneSpawner()

	// Register an agent but don't add enough messages to exceed threshold
	monitor.RegisterAgent("test__cc_1", "%0", "claude-opus-4")
	monitor.RecordMessage("test__cc_1", 100, 100)

	r := NewRotator(RotatorConfig{
		Monitor: monitor,
		Spawner: spawner,
		Config:  config.DefaultContextRotationConfig(),
	})

	results, err := r.CheckAndRotate("test", "/tmp")
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}
	if len(results) != 0 {
		t.Errorf("expected 0 results, got %d", len(results))
	}
}

func TestNeedsRotation(t *testing.T) {
	t.Parallel()

	monitor := NewContextMonitor(DefaultMonitorConfig())
	spawner := NewMockPaneSpawner()

	// Register an agent and add enough messages to exceed threshold
	monitor.RegisterAgent("test__cc_1", "%0", "claude-opus-4")
	for i := 0; i < 200; i++ {
		monitor.RecordMessage("test__cc_1", 1000, 1000)
	}

	cfg := config.DefaultContextRotationConfig()
	cfg.RotateThreshold = 0.50 // 50%

	r := NewRotator(RotatorConfig{
		Monitor: monitor,
		Spawner: spawner,
		Config:  cfg,
	})

	agents, reason := r.NeedsRotation()
	if len(agents) == 0 {
		t.Errorf("expected agents needing rotation, got none. Reason: %s", reason)
	}
	if !strings.Contains(reason, "above") && !strings.Contains(reason, "threshold") {
		t.Errorf("expected threshold reason, got: %s", reason)
	}
}

func TestNeedsWarning(t *testing.T) {
	t.Parallel()

	monitor := NewContextMonitor(DefaultMonitorConfig())
	spawner := NewMockPaneSpawner()

	// Register an agent and add enough messages to exceed warning threshold
	monitor.RegisterAgent("test__cc_1", "%0", "claude-opus-4")
	for i := 0; i < 100; i++ {
		monitor.RecordMessage("test__cc_1", 1000, 1000)
	}

	cfg := config.DefaultContextRotationConfig()
	cfg.WarningThreshold = 0.30 // 30%

	r := NewRotator(RotatorConfig{
		Monitor: monitor,
		Spawner: spawner,
		Config:  cfg,
	})

	agents, reason := r.NeedsWarning()
	if len(agents) == 0 {
		t.Errorf("expected agents needing warning, got none. Reason: %s", reason)
	}
}

func TestNeedsRotation_Disabled(t *testing.T) {
	t.Parallel()

	monitor := NewContextMonitor(DefaultMonitorConfig())

	cfg := config.DefaultContextRotationConfig()
	cfg.Enabled = false

	r := NewRotator(RotatorConfig{
		Monitor: monitor,
		Config:  cfg,
	})

	agents, reason := r.NeedsRotation()
	if len(agents) != 0 {
		t.Error("expected no agents when rotation disabled")
	}
	if !strings.Contains(reason, "disabled") {
		t.Errorf("expected disabled reason, got: %s", reason)
	}
}

func TestNeedsRotation_NoMonitor(t *testing.T) {
	t.Parallel()

	r := NewRotator(RotatorConfig{
		Config: config.DefaultContextRotationConfig(),
	})

	agents, reason := r.NeedsRotation()
	if len(agents) != 0 {
		t.Error("expected no agents when no monitor")
	}
	if !strings.Contains(reason, "no monitor") {
		t.Errorf("expected 'no monitor' reason, got: %s", reason)
	}
}

func TestGetHistory(t *testing.T) {
	t.Parallel()

	r := NewRotator(RotatorConfig{
		Config: config.DefaultContextRotationConfig(),
	})

	history := r.GetHistory()
	if len(history) != 0 {
		t.Error("expected empty history initially")
	}
}

func TestClearHistory(t *testing.T) {
	t.Parallel()

	r := NewRotator(RotatorConfig{
		Config: config.DefaultContextRotationConfig(),
	})

	// Manually add an event to history
	r.history = append(r.history, RotationEvent{
		SessionName: "test",
		OldAgentID:  "cc_1",
		NewAgentID:  "cc_1",
		Timestamp:   time.Now(),
	})

	if len(r.GetHistory()) != 1 {
		t.Error("expected 1 event in history")
	}

	r.ClearHistory()

	if len(r.GetHistory()) != 0 {
		t.Error("expected empty history after clear")
	}
}

func TestExtractAgentIndex(t *testing.T) {
	t.Parallel()

	tests := []struct {
		agentID string
		want    int
	}{
		{"myproject__cc_1", 1},
		{"myproject__cc_2", 2},
		{"myproject__cod_10", 10},
		{"myproject__gmi_3_variant", 3},
		{"invalid", 1},
		{"", 1},
	}

	for _, tt := range tests {
		t.Run(tt.agentID, func(t *testing.T) {
			t.Parallel()
			got := extractAgentIndex(tt.agentID)
			if got != tt.want {
				t.Errorf("extractAgentIndex(%q) = %d, want %d", tt.agentID, got, tt.want)
			}
		})
	}
}

func TestDeriveAgentTypeFromID(t *testing.T) {
	t.Parallel()

	tests := []struct {
		agentID string
		want    string
	}{
		{"myproject__cc_1", "claude"},
		{"myproject__cod_2", "codex"},
		{"myproject__gmi_3", "gemini"},
		{"myproject__cc_1_opus", "claude"},
		{"invalid", "unknown"},
		{"", "unknown"},
	}

	for _, tt := range tests {
		t.Run(tt.agentID, func(t *testing.T) {
			t.Parallel()
			got := deriveAgentTypeFromID(tt.agentID)
			if got != tt.want {
				t.Errorf("deriveAgentTypeFromID(%q) = %q, want %q", tt.agentID, got, tt.want)
			}
		})
	}
}

func TestAgentTypeShort(t *testing.T) {
	t.Parallel()

	tests := []struct {
		agentType string
		want      string
	}{
		{"claude", "cc"},
		{"Claude", "cc"},
		{"cc", "cc"},
		{"codex", "cod"},
		{"cod", "cod"},
		{"gemini", "gmi"},
		{"gmi", "gmi"},
		{"unknown", "unknown"},
	}

	for _, tt := range tests {
		t.Run(tt.agentType, func(t *testing.T) {
			t.Parallel()
			got := agentTypeShort(tt.agentType)
			if got != tt.want {
				t.Errorf("agentTypeShort(%q) = %q, want %q", tt.agentType, got, tt.want)
			}
		})
	}
}

func TestAgentTypeLong(t *testing.T) {
	t.Parallel()

	tests := []struct {
		shortType string
		want      string
	}{
		{"cc", "claude"},
		{"cod", "codex"},
		{"gmi", "gemini"},
		{"unknown", "unknown"},
	}

	for _, tt := range tests {
		t.Run(tt.shortType, func(t *testing.T) {
			t.Parallel()
			got := agentTypeLong(tt.shortType)
			if got != tt.want {
				t.Errorf("agentTypeLong(%q) = %q, want %q", tt.shortType, got, tt.want)
			}
		})
	}
}

func TestRotationResultFormatForDisplay(t *testing.T) {
	t.Parallel()

	successResult := &RotationResult{
		Success:       true,
		OldAgentID:    "test__cc_1",
		NewAgentID:    "test__cc_1",
		Method:        RotationThresholdExceeded,
		State:         RotationStateCompleted,
		SummaryTokens: 500,
		Duration:      5 * time.Second,
	}

	output := successResult.FormatForDisplay()
	if !strings.Contains(output, "✓") {
		t.Error("success output should contain checkmark")
	}
	if !strings.Contains(output, "test__cc_1") {
		t.Error("output should contain agent ID")
	}
	if !strings.Contains(output, "completed") {
		t.Error("output should contain state")
	}

	failResult := &RotationResult{
		Success:    false,
		OldAgentID: "test__cc_1",
		State:      RotationStateFailed,
		Error:      "test error",
	}

	output = failResult.FormatForDisplay()
	if !strings.Contains(output, "✗") {
		t.Error("failure output should contain X mark")
	}
	if !strings.Contains(output, "test error") {
		t.Error("output should contain error message")
	}
}

func TestManualRotate_NoMonitor(t *testing.T) {
	t.Parallel()

	r := NewRotator(RotatorConfig{
		Config: config.DefaultContextRotationConfig(),
	})

	result := r.ManualRotate("test-session", "test__cc_1", "/tmp")
	if result.Success {
		t.Error("expected failure when no monitor")
	}
	if !strings.Contains(result.Error, "no monitor") {
		t.Errorf("expected 'no monitor' error, got: %s", result.Error)
	}
	if result.Method != RotationManual {
		t.Errorf("expected RotationManual method, got: %s", result.Method)
	}
}

func TestManualRotate_NoSpawner(t *testing.T) {
	t.Parallel()

	monitor := NewContextMonitor(DefaultMonitorConfig())
	r := NewRotator(RotatorConfig{
		Monitor: monitor,
		Config:  config.DefaultContextRotationConfig(),
	})

	result := r.ManualRotate("test-session", "test__cc_1", "/tmp")
	if result.Success {
		t.Error("expected failure when no spawner")
	}
	if !strings.Contains(result.Error, "no spawner") {
		t.Errorf("expected 'no spawner' error, got: %s", result.Error)
	}
	if result.Method != RotationManual {
		t.Errorf("expected RotationManual method, got: %s", result.Method)
	}
}

func TestDefaultPaneSpawnerGetAgentCommand(t *testing.T) {
	t.Parallel()

	// Without config
	spawner := NewDefaultPaneSpawner(nil)

	tests := []struct {
		agentType string
		want      string
	}{
		{"claude", "claude"},
		{"codex", "codex"},
		{"gemini", "gemini"},
	}

	for _, tt := range tests {
		t.Run(tt.agentType, func(t *testing.T) {
			got := spawner.getAgentCommand(tt.agentType)
			if got != tt.want {
				t.Errorf("getAgentCommand(%q) = %q, want %q", tt.agentType, got, tt.want)
			}
		})
	}

	// With custom config
	cfg := &config.Config{}
	cfg.Agents.Claude = "custom-claude"
	cfg.Agents.Codex = "custom-codex"
	cfg.Agents.Gemini = "custom-gemini"

	spawner2 := NewDefaultPaneSpawner(cfg)

	if got := spawner2.getAgentCommand("claude"); got != "custom-claude" {
		t.Errorf("expected custom-claude, got %q", got)
	}
	if got := spawner2.getAgentCommand("codex"); got != "custom-codex" {
		t.Errorf("expected custom-codex, got %q", got)
	}
	if got := spawner2.getAgentCommand("gemini"); got != "custom-gemini" {
		t.Errorf("expected custom-gemini, got %q", got)
	}
}
