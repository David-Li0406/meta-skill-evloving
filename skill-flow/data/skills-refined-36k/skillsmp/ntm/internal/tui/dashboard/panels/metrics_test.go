package panels

import (
	"errors"
	"strings"
	"testing"
	"time"
)

func TestNewMetricsPanel(t *testing.T) {
	panel := NewMetricsPanel()
	if panel == nil {
		t.Fatal("NewMetricsPanel returned nil")
	}
}

func TestMetricsPanelConfig(t *testing.T) {
	panel := NewMetricsPanel()
	cfg := panel.Config()

	if cfg.ID != "metrics" {
		t.Errorf("expected ID 'metrics', got %q", cfg.ID)
	}
	if cfg.Title != "Metrics & Usage" {
		t.Errorf("expected Title 'Metrics & Usage', got %q", cfg.Title)
	}
	if cfg.Priority != PriorityNormal {
		t.Errorf("expected PriorityNormal, got %v", cfg.Priority)
	}
	if cfg.RefreshInterval != 10*time.Second {
		t.Errorf("expected 10s refresh, got %v", cfg.RefreshInterval)
	}
	if !cfg.Collapsible {
		t.Error("expected Collapsible to be true")
	}
}

func TestMetricsPanelSetSize(t *testing.T) {
	panel := NewMetricsPanel()
	panel.SetSize(100, 30)

	if panel.Width() != 100 {
		t.Errorf("expected width 100, got %d", panel.Width())
	}
	if panel.Height() != 30 {
		t.Errorf("expected height 30, got %d", panel.Height())
	}
}

func TestMetricsPanelFocusBlur(t *testing.T) {
	panel := NewMetricsPanel()

	panel.Focus()
	if !panel.IsFocused() {
		t.Error("expected IsFocused to be true after Focus()")
	}

	panel.Blur()
	if panel.IsFocused() {
		t.Error("expected IsFocused to be false after Blur()")
	}
}

func TestMetricsPanelSetData(t *testing.T) {
	panel := NewMetricsPanel()

	data := MetricsData{
		TotalTokens: 150000,
		TotalCost:   12.50,
		Agents: []AgentMetric{
			{Name: "cc_1", Type: "cc", Tokens: 50000, Cost: 4.00, ContextPct: 25.0},
			{Name: "cod_1", Type: "cod", Tokens: 100000, Cost: 8.50, ContextPct: 50.0},
		},
	}

	panel.SetData(data, nil)

	if panel.data.TotalTokens != 150000 {
		t.Errorf("expected TotalTokens 150000, got %d", panel.data.TotalTokens)
	}
	if panel.data.TotalCost != 12.50 {
		t.Errorf("expected TotalCost 12.50, got %f", panel.data.TotalCost)
	}
	if len(panel.data.Agents) != 2 {
		t.Errorf("expected 2 agents, got %d", len(panel.data.Agents))
	}
}

func TestMetricsPanelKeybindings(t *testing.T) {
	panel := NewMetricsPanel()
	bindings := panel.Keybindings()

	if len(bindings) == 0 {
		t.Error("expected non-empty keybindings")
	}

	// Check for expected actions
	actions := make(map[string]bool)
	for _, b := range bindings {
		actions[b.Action] = true
	}

	if !actions["refresh"] {
		t.Error("expected 'refresh' action in keybindings")
	}
	if !actions["copy"] {
		t.Error("expected 'copy' action in keybindings")
	}
}

func TestMetricsPanelInit(t *testing.T) {
	panel := NewMetricsPanel()
	cmd := panel.Init()
	if cmd != nil {
		t.Error("expected Init() to return nil")
	}
}

func TestMetricsPanelUpdate(t *testing.T) {
	panel := NewMetricsPanel()

	newModel, cmd := panel.Update(nil)

	if newModel != panel {
		t.Error("expected Update to return same model")
	}
	if cmd != nil {
		t.Error("expected Update to return nil cmd")
	}
}

func TestMetricsPanelViewContainsTitle(t *testing.T) {
	panel := NewMetricsPanel()
	panel.SetSize(80, 20)

	view := panel.View()

	if !strings.Contains(view, "Metrics & Usage") {
		t.Error("expected view to contain title")
	}
}

func TestMetricsPanelViewShowsStats(t *testing.T) {
	panel := NewMetricsPanel()
	panel.SetSize(80, 20)

	data := MetricsData{
		TotalTokens: 100000,
		TotalCost:   10.00,
		Agents:      []AgentMetric{},
	}
	panel.SetData(data, nil)

	view := panel.View()

	if !strings.Contains(view, "100000 tokens") {
		t.Error("expected view to contain token count")
	}
	if !strings.Contains(view, "$10.00") {
		t.Error("expected view to contain cost")
	}
}

func TestMetricsPanelViewShowsAgents(t *testing.T) {
	panel := NewMetricsPanel()
	panel.SetSize(80, 30)

	data := MetricsData{
		TotalTokens: 75000,
		TotalCost:   7.50,
		Agents: []AgentMetric{
			{Name: "cc_1", Type: "cc", Tokens: 50000, Cost: 5.00, ContextPct: 33.0},
			{Name: "cod_1", Type: "cod", Tokens: 25000, Cost: 2.50, ContextPct: 17.0},
		},
	}
	panel.SetData(data, nil)

	view := panel.View()

	// Should contain agent names
	if !strings.Contains(view, "cc_1") {
		t.Error("expected view to contain agent name 'cc_1'")
	}
	if !strings.Contains(view, "cod_1") {
		t.Error("expected view to contain agent name 'cod_1'")
	}
}

func TestMetricsPanelViewShowsErrorState(t *testing.T) {
	panel := NewMetricsPanel()
	panel.SetSize(80, 20)

	panel.SetData(MetricsData{}, errors.New("metrics backend down"))

	view := panel.View()

	if !strings.Contains(view, "Error") {
		t.Error("expected view to include error badge")
	}
	if !strings.Contains(view, "metrics backend down") {
		t.Error("expected view to include error message")
	}
	if !strings.Contains(view, "Press r") {
		t.Error("expected view to include retry hint")
	}
}

func TestMetricsPanelViewSessionTotal(t *testing.T) {
	panel := NewMetricsPanel()
	panel.SetSize(80, 20)

	// Provide some data so it renders the stats
	data := MetricsData{
		TotalTokens: 100,
		TotalCost:   0.01,
		Agents:      []AgentMetric{{Name: "agent", Tokens: 100}},
	}
	panel.SetData(data, nil)

	view := panel.View()

	if !strings.Contains(view, "Session Total") {
		t.Error("expected view to contain 'Session Total'")
	}
}

func TestAgentMetricStruct(t *testing.T) {
	metric := AgentMetric{
		Name:       "test_agent",
		Type:       "cc",
		Tokens:     50000,
		Cost:       5.00,
		ContextPct: 25.5,
	}

	if metric.Name != "test_agent" {
		t.Errorf("expected Name 'test_agent', got %q", metric.Name)
	}
	if metric.Type != "cc" {
		t.Errorf("expected Type 'cc', got %q", metric.Type)
	}
	if metric.Tokens != 50000 {
		t.Errorf("expected Tokens 50000, got %d", metric.Tokens)
	}
	if metric.Cost != 5.00 {
		t.Errorf("expected Cost 5.00, got %f", metric.Cost)
	}
	if metric.ContextPct != 25.5 {
		t.Errorf("expected ContextPct 25.5, got %f", metric.ContextPct)
	}
}

func TestMetricsDataStruct(t *testing.T) {
	data := MetricsData{
		TotalTokens: 100000,
		TotalCost:   10.00,
		Agents: []AgentMetric{
			{Name: "agent1"},
		},
	}

	if data.TotalTokens != 100000 {
		t.Errorf("expected TotalTokens 100000, got %d", data.TotalTokens)
	}
	if data.TotalCost != 10.00 {
		t.Errorf("expected TotalCost 10.00, got %f", data.TotalCost)
	}
	if len(data.Agents) != 1 {
		t.Errorf("expected 1 agent, got %d", len(data.Agents))
	}
}

func TestMetricsPanelViewShowsRoutingScore(t *testing.T) {
	panel := NewMetricsPanel()
	panel.SetSize(80, 20)

	// Provide data with routing score
	data := MetricsData{
		TotalTokens: 100,
		TotalCost:   0.01,
		Agents: []AgentMetric{
			{
				Name:         "claude-1",
				Type:         "cc",
				Tokens:       100,
				ContextPct:   50.0,
				RoutingScore: 85.0,
				State:        "waiting",
			},
		},
	}
	panel.SetData(data, nil)

	view := panel.View()

	// Routing score should be visible
	if !strings.Contains(view, "85") {
		t.Error("expected view to contain routing score '85'")
	}
	// State should be visible
	if !strings.Contains(view, "waiting") {
		t.Error("expected view to contain state 'waiting'")
	}
}

func TestMetricsPanelViewShowsRecommendedIndicator(t *testing.T) {
	panel := NewMetricsPanel()
	panel.SetSize(80, 20)

	// Provide data with recommended agent
	data := MetricsData{
		TotalTokens: 200,
		TotalCost:   0.02,
		Agents: []AgentMetric{
			{
				Name:          "claude-1",
				Type:          "cc",
				Tokens:        100,
				ContextPct:    30.0,
				RoutingScore:  90.0,
				IsRecommended: true,
			},
			{
				Name:          "codex-1",
				Type:          "cod",
				Tokens:        100,
				ContextPct:    40.0,
				RoutingScore:  70.0,
				IsRecommended: false,
			},
		},
	}
	panel.SetData(data, nil)

	view := panel.View()

	// Recommended indicator (star) should be visible
	if !strings.Contains(view, "★") {
		t.Error("expected view to contain recommended indicator '★'")
	}
}

func TestAgentMetricRoutingFields(t *testing.T) {
	metric := AgentMetric{
		Name:          "test_agent",
		Type:          "cc",
		Tokens:        50000,
		Cost:          5.00,
		ContextPct:    25.5,
		RoutingScore:  75.0,
		IsRecommended: true,
		State:         "generating",
	}

	if metric.RoutingScore != 75.0 {
		t.Errorf("expected RoutingScore 75.0, got %f", metric.RoutingScore)
	}
	if !metric.IsRecommended {
		t.Error("expected IsRecommended true")
	}
	if metric.State != "generating" {
		t.Errorf("expected State 'generating', got %q", metric.State)
	}
}
