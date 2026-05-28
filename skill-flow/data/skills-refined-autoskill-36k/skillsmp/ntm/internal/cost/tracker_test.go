// Package cost provides API cost tracking for AI agent sessions.
package cost

import (
	"os"
	"path/filepath"
	"sync"
	"testing"
	"time"
)

func TestEstimateTokens(t *testing.T) {
	tests := []struct {
		text     string
		expected int
	}{
		{"", 0},
		{"a", 1},
		{"test", 1},
		{"hello world", 3},           // 11 chars -> 3 tokens
		{"This is a longer text", 6}, // 21 chars -> 6 tokens
		{"A very long sentence that should result in many tokens being counted", 19}, // 68 chars -> 19 tokens
	}

	for _, tt := range tests {
		t.Run(tt.text, func(t *testing.T) {
			got := EstimateTokens(tt.text)
			if got != tt.expected {
				t.Errorf("EstimateTokens(%q) = %d, want %d", tt.text, got, tt.expected)
			}
		})
	}
}

func TestGetModelPricing(t *testing.T) {
	tests := []struct {
		model      string
		wantInput  float64
		wantOutput float64
	}{
		{"claude-opus", 0.015, 0.075},
		{"claude-sonnet", 0.003, 0.015},
		{"claude-haiku", 0.00025, 0.00125},
		{"gpt-4o", 0.005, 0.015},
		{"gpt-4o-mini", 0.00015, 0.0006},
		{"gemini-flash", 0.000075, 0.0003},
		{"unknown-model", 0.003, 0.015}, // Falls back to default
	}

	for _, tt := range tests {
		t.Run(tt.model, func(t *testing.T) {
			pricing := GetModelPricing(tt.model)
			if pricing.InputPer1K != tt.wantInput {
				t.Errorf("GetModelPricing(%q).InputPer1K = %v, want %v", tt.model, pricing.InputPer1K, tt.wantInput)
			}
			if pricing.OutputPer1K != tt.wantOutput {
				t.Errorf("GetModelPricing(%q).OutputPer1K = %v, want %v", tt.model, pricing.OutputPer1K, tt.wantOutput)
			}
		})
	}
}

func TestAgentCost_Cost(t *testing.T) {
	tests := []struct {
		name         string
		inputTokens  int
		outputTokens int
		model        string
		wantMin      float64
		wantMax      float64
	}{
		{
			name:         "claude-opus 1k input 1k output",
			inputTokens:  1000,
			outputTokens: 1000,
			model:        "claude-opus",
			wantMin:      0.089, // 0.015 + 0.075 = 0.09
			wantMax:      0.091,
		},
		{
			name:         "claude-haiku cheap",
			inputTokens:  10000,
			outputTokens: 5000,
			model:        "claude-haiku",
			wantMin:      0.008, // 10*0.00025 + 5*0.00125 = 0.0025 + 0.00625 = 0.00875
			wantMax:      0.009,
		},
		{
			name:         "zero tokens",
			inputTokens:  0,
			outputTokens: 0,
			model:        "claude-opus",
			wantMin:      0,
			wantMax:      0.001,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			a := &AgentCost{
				InputTokens:  tt.inputTokens,
				OutputTokens: tt.outputTokens,
				Model:        tt.model,
			}
			got := a.Cost()
			if got < tt.wantMin || got > tt.wantMax {
				t.Errorf("AgentCost.Cost() = %v, want between %v and %v", got, tt.wantMin, tt.wantMax)
			}
		})
	}
}

func TestSessionCost_TotalCost(t *testing.T) {
	s := &SessionCost{
		Agents: map[string]*AgentCost{
			"agent1": {InputTokens: 1000, OutputTokens: 1000, Model: "claude-opus"},
			"agent2": {InputTokens: 1000, OutputTokens: 1000, Model: "claude-haiku"},
		},
	}

	total := s.TotalCost()
	// claude-opus: 0.015 + 0.075 = 0.09
	// claude-haiku: 0.00025 + 0.00125 = 0.00175
	// total: ~0.09175
	if total < 0.09 || total > 0.095 {
		t.Errorf("SessionCost.TotalCost() = %v, want ~0.09175", total)
	}
}

func TestSessionCost_TotalTokens(t *testing.T) {
	s := &SessionCost{
		Agents: map[string]*AgentCost{
			"agent1": {InputTokens: 1000, OutputTokens: 500},
			"agent2": {InputTokens: 2000, OutputTokens: 1500},
		},
	}

	input, output := s.TotalTokens()
	if input != 3000 {
		t.Errorf("TotalTokens() input = %d, want 3000", input)
	}
	if output != 2000 {
		t.Errorf("TotalTokens() output = %d, want 2000", output)
	}
}

func TestNewCostTracker(t *testing.T) {
	tracker := NewCostTracker("/tmp/test")
	if tracker == nil {
		t.Fatal("NewCostTracker returned nil")
	}
	if tracker.dataDir != "/tmp/test" {
		t.Errorf("dataDir = %q, want %q", tracker.dataDir, "/tmp/test")
	}
	if tracker.sessions == nil {
		t.Error("sessions map should not be nil")
	}
}

func TestCostTracker_RecordPrompt(t *testing.T) {
	tracker := NewCostTracker("")
	tracker.RecordPrompt("session1", "pane1", "claude-opus", "Hello world")

	s := tracker.GetSession("session1")
	if s == nil {
		t.Fatal("session not created")
	}
	agent, ok := s.Agents["pane1"]
	if !ok {
		t.Fatal("agent not created")
	}
	if agent.InputTokens == 0 {
		t.Error("InputTokens should be > 0")
	}
	if agent.Model != "claude-opus" {
		t.Errorf("Model = %q, want %q", agent.Model, "claude-opus")
	}
}

func TestCostTracker_RecordResponse(t *testing.T) {
	tracker := NewCostTracker("")
	tracker.RecordResponse("session1", "pane1", "claude-sonnet", "This is a response")

	s := tracker.GetSession("session1")
	if s == nil {
		t.Fatal("session not created")
	}
	agent := s.Agents["pane1"]
	if agent == nil {
		t.Fatal("agent not created")
	}
	if agent.OutputTokens == 0 {
		t.Error("OutputTokens should be > 0")
	}
}

func TestCostTracker_RecordTokens(t *testing.T) {
	tracker := NewCostTracker("")
	tracker.RecordTokens("session1", "pane1", "gpt-4o", 500, 200)

	s := tracker.GetSession("session1")
	if s == nil {
		t.Fatal("session not created")
	}
	agent := s.Agents["pane1"]
	if agent.InputTokens != 500 {
		t.Errorf("InputTokens = %d, want 500", agent.InputTokens)
	}
	if agent.OutputTokens != 200 {
		t.Errorf("OutputTokens = %d, want 200", agent.OutputTokens)
	}
}

func TestCostTracker_GetSessionCost(t *testing.T) {
	tracker := NewCostTracker("")
	tracker.RecordTokens("session1", "pane1", "claude-opus", 1000, 1000)

	cost := tracker.GetSessionCost("session1")
	// 0.015 + 0.075 = 0.09
	if cost < 0.089 || cost > 0.091 {
		t.Errorf("GetSessionCost() = %v, want ~0.09", cost)
	}

	// Non-existent session
	cost = tracker.GetSessionCost("nonexistent")
	if cost != 0 {
		t.Errorf("GetSessionCost(nonexistent) = %v, want 0", cost)
	}
}

func TestCostTracker_GetAllSessions(t *testing.T) {
	tracker := NewCostTracker("")
	tracker.RecordPrompt("session1", "pane1", "claude-opus", "test")
	tracker.RecordPrompt("session2", "pane1", "claude-opus", "test")

	sessions := tracker.GetAllSessions()
	if len(sessions) != 2 {
		t.Errorf("GetAllSessions() returned %d sessions, want 2", len(sessions))
	}
}

func TestCostTracker_GetTotalCost(t *testing.T) {
	tracker := NewCostTracker("")
	tracker.RecordTokens("session1", "pane1", "claude-opus", 1000, 1000)
	tracker.RecordTokens("session2", "pane1", "claude-opus", 1000, 1000)

	total := tracker.GetTotalCost()
	// 2 sessions * 0.09 = 0.18
	if total < 0.17 || total > 0.19 {
		t.Errorf("GetTotalCost() = %v, want ~0.18", total)
	}
}

func TestCostTracker_ClearSession(t *testing.T) {
	tracker := NewCostTracker("")
	tracker.RecordPrompt("session1", "pane1", "claude-opus", "test")
	tracker.ClearSession("session1")

	s := tracker.GetSession("session1")
	if s != nil {
		t.Error("session should be nil after ClearSession")
	}
}

func TestCostTracker_Persistence(t *testing.T) {
	tmpDir := t.TempDir()

	// Create tracker and record data
	tracker1 := NewCostTracker(tmpDir)
	tracker1.RecordTokens("session1", "pane1", "claude-opus", 1000, 500)
	tracker1.RecordTokens("session1", "pane2", "claude-sonnet", 2000, 1000)

	// Save
	if err := tracker1.SaveToDir(tmpDir); err != nil {
		t.Fatalf("SaveToDir failed: %v", err)
	}

	// Verify file exists
	costPath := filepath.Join(tmpDir, ".ntm", "costs.json")
	if _, err := os.Stat(costPath); os.IsNotExist(err) {
		t.Fatal("costs.json not created")
	}

	// Create new tracker and load
	tracker2 := NewCostTracker(tmpDir)
	if err := tracker2.LoadFromDir(tmpDir); err != nil {
		t.Fatalf("LoadFromDir failed: %v", err)
	}

	// Verify data was loaded correctly
	s := tracker2.GetSession("session1")
	if s == nil {
		t.Fatal("session not loaded")
	}
	if len(s.Agents) != 2 {
		t.Errorf("expected 2 agents, got %d", len(s.Agents))
	}

	agent1 := s.Agents["pane1"]
	if agent1.InputTokens != 1000 || agent1.OutputTokens != 500 {
		t.Errorf("pane1 tokens not loaded correctly: input=%d output=%d", agent1.InputTokens, agent1.OutputTokens)
	}
}

func TestCostTracker_LoadFromDir_NoFile(t *testing.T) {
	tmpDir := t.TempDir()
	tracker := NewCostTracker(tmpDir)

	// Should not error when file doesn't exist
	if err := tracker.LoadFromDir(tmpDir); err != nil {
		t.Errorf("LoadFromDir should not error for missing file: %v", err)
	}
}

func TestCostTracker_Concurrent(t *testing.T) {
	tracker := NewCostTracker("")
	var wg sync.WaitGroup

	// Simulate concurrent access from multiple agents
	for i := 0; i < 10; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			pane := "pane" + string(rune('A'+id))
			for j := 0; j < 100; j++ {
				tracker.RecordPrompt("session1", pane, "claude-opus", "test prompt")
				tracker.RecordResponse("session1", pane, "claude-opus", "test response")
			}
		}(i)
	}

	wg.Wait()

	s := tracker.GetSession("session1")
	if s == nil {
		t.Fatal("session not created")
	}
	if len(s.Agents) != 10 {
		t.Errorf("expected 10 agents, got %d", len(s.Agents))
	}
}

func TestFormatCost(t *testing.T) {
	tests := []struct {
		usd  float64
		want string
	}{
		{0.0001, "$0.0001"},
		{0.001, "$0.0010"},
		{0.01, "$0.010"},
		{0.1, "$0.100"},
		{1.0, "$1.00"},
		{10.5, "$10.50"},
		{100.99, "$100.99"},
	}

	for _, tt := range tests {
		t.Run(tt.want, func(t *testing.T) {
			got := FormatCost(tt.usd)
			if got != tt.want {
				t.Errorf("FormatCost(%v) = %q, want %q", tt.usd, got, tt.want)
			}
		})
	}
}

func TestAgentCost_LastUpdated(t *testing.T) {
	tracker := NewCostTracker("")
	before := time.Now()
	tracker.RecordPrompt("session1", "pane1", "claude-opus", "test")
	after := time.Now()

	s := tracker.GetSession("session1")
	agent := s.Agents["pane1"]

	if agent.LastUpdated.Before(before) || agent.LastUpdated.After(after) {
		t.Errorf("LastUpdated = %v, want between %v and %v", agent.LastUpdated, before, after)
	}
}

func TestCostTracker_ModelUpdate(t *testing.T) {
	tracker := NewCostTracker("")

	// First record without model
	tracker.RecordPrompt("session1", "pane1", "", "test")

	s := tracker.GetSession("session1")
	if s.Agents["pane1"].Model != "" {
		t.Error("Model should be empty initially")
	}

	// Second record with model - should update
	tracker.RecordPrompt("session1", "pane1", "claude-opus", "test")

	s = tracker.GetSession("session1")
	if s.Agents["pane1"].Model != "claude-opus" {
		t.Errorf("Model should be updated to claude-opus, got %q", s.Agents["pane1"].Model)
	}
}

func TestCostTracker_GetSession_ReturnsCopy(t *testing.T) {
	tracker := NewCostTracker("")
	tracker.RecordTokens("session1", "pane1", "claude-opus", 1000, 500)

	// Get a copy
	s1 := tracker.GetSession("session1")

	// Modify the copy
	s1.Agents["pane1"].InputTokens = 9999

	// Get another copy - should not reflect the modification
	s2 := tracker.GetSession("session1")
	if s2.Agents["pane1"].InputTokens != 1000 {
		t.Error("GetSession should return a copy, not the original")
	}
}

// =============================================================================
// bd-25o0: Additional Cost Estimation Tests
// =============================================================================

func TestPerModelPricingComprehensive(t *testing.T) {
	t.Parallel()

	tests := []struct {
		model       string
		inputPer1K  float64
		outputPer1K float64
	}{
		// Claude models
		{"claude-opus", 0.015, 0.075},
		{"claude-opus-4", 0.015, 0.075},
		{"claude-opus-4-5", 0.015, 0.075},
		{"claude-sonnet", 0.003, 0.015},
		{"claude-sonnet-4", 0.003, 0.015},
		{"claude-haiku", 0.00025, 0.00125},
		{"claude-haiku-3-5", 0.00025, 0.00125},
		{"claude-3-opus", 0.015, 0.075},
		{"claude-3-sonnet", 0.003, 0.015},
		{"claude-3-haiku", 0.00025, 0.00125},
		{"claude-3-5-sonnet", 0.003, 0.015},
		{"claude-3-5-haiku", 0.00025, 0.00125},

		// OpenAI models
		{"gpt-4o", 0.005, 0.015},
		{"gpt-4o-mini", 0.00015, 0.0006},
		{"gpt-4-turbo", 0.01, 0.03},
		{"gpt-4", 0.03, 0.06},
		{"o1", 0.015, 0.06},
		{"o1-mini", 0.003, 0.012},
		{"o1-preview", 0.015, 0.06},

		// Google models
		{"gemini-pro", 0.00025, 0.0005},
		{"gemini-pro-1.5", 0.00025, 0.0005},
		{"gemini-ultra", 0.00125, 0.00375},
		{"gemini-flash", 0.000075, 0.0003},
		{"gemini-flash-1.5", 0.000075, 0.0003},
		{"gemini-2.0-flash", 0.000075, 0.0003},

		// Unknown model defaults
		{"unknown-model", 0.003, 0.015},
	}

	for _, tt := range tests {
		t.Run(tt.model, func(t *testing.T) {
			t.Parallel()

			pricing := GetModelPricing(tt.model)

			t.Logf("COST_TEST: Pricing | Model=%s | InputPer1K=$%.5f | OutputPer1K=$%.5f",
				tt.model, pricing.InputPer1K, pricing.OutputPer1K)

			if pricing.InputPer1K != tt.inputPer1K {
				t.Errorf("InputPer1K = %v, want %v", pricing.InputPer1K, tt.inputPer1K)
			}
			if pricing.OutputPer1K != tt.outputPer1K {
				t.Errorf("OutputPer1K = %v, want %v", pricing.OutputPer1K, tt.outputPer1K)
			}
		})
	}
}

func TestCostCalculationAccuracy(t *testing.T) {
	t.Parallel()

	tests := []struct {
		name         string
		inputTokens  int
		outputTokens int
		model        string
		expectedCost float64
	}{
		{
			name:         "claude-opus 10k/5k tokens",
			inputTokens:  10000,
			outputTokens: 5000,
			model:        "claude-opus",
			// 10k * 0.015/1000 + 5k * 0.075/1000 = 0.15 + 0.375 = 0.525
			expectedCost: 0.525,
		},
		{
			name:         "claude-haiku 100k/50k tokens",
			inputTokens:  100000,
			outputTokens: 50000,
			model:        "claude-haiku",
			// 100k * 0.00025/1000 + 50k * 0.00125/1000 = 0.025 + 0.0625 = 0.0875
			expectedCost: 0.0875,
		},
		{
			name:         "gpt-4o 10k/10k tokens",
			inputTokens:  10000,
			outputTokens: 10000,
			model:        "gpt-4o",
			// 10k * 0.005/1000 + 10k * 0.015/1000 = 0.05 + 0.15 = 0.20
			expectedCost: 0.20,
		},
		{
			name:         "gemini-flash 100k/100k tokens",
			inputTokens:  100000,
			outputTokens: 100000,
			model:        "gemini-flash",
			// 100k * 0.000075/1000 + 100k * 0.0003/1000 = 0.0075 + 0.03 = 0.0375
			expectedCost: 0.0375,
		},
		{
			name:         "zero tokens",
			inputTokens:  0,
			outputTokens: 0,
			model:        "claude-opus",
			expectedCost: 0.0,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			t.Parallel()

			agent := &AgentCost{
				InputTokens:  tt.inputTokens,
				OutputTokens: tt.outputTokens,
				Model:        tt.model,
			}

			cost := agent.Cost()

			t.Logf("COST_TEST: %s | Tokens=%d/%d | Model=%s | Cost=$%.4f",
				tt.name, tt.inputTokens, tt.outputTokens, tt.model, cost)

			// Allow small floating point tolerance
			diff := cost - tt.expectedCost
			if diff < -0.0001 || diff > 0.0001 {
				t.Errorf("Cost() = %.6f, want %.6f", cost, tt.expectedCost)
			}
		})
	}
}

func TestCostAggregationMultiAgent(t *testing.T) {
	t.Parallel()

	tracker := NewCostTracker("")

	// Record tokens for multiple agents with different models
	agents := []struct {
		pane   string
		model  string
		input  int
		output int
	}{
		{"pane1", "claude-opus", 10000, 5000},    // $0.525
		{"pane2", "claude-sonnet", 20000, 10000}, // $0.21
		{"pane3", "claude-haiku", 100000, 50000}, // $0.0875
		{"pane4", "gpt-4o", 10000, 5000},         // $0.125
	}

	for _, a := range agents {
		tracker.RecordTokens("test-session", a.pane, a.model, a.input, a.output)
	}

	totalCost := tracker.GetSessionCost("test-session")

	// Expected: 0.525 + 0.21 + 0.0875 + 0.125 = 0.9475
	expectedTotal := 0.9475

	t.Logf("COST_TEST: CostAggregation | AgentCount=%d | TotalCost=$%.4f | Expected=$%.4f",
		len(agents), totalCost, expectedTotal)

	diff := totalCost - expectedTotal
	if diff < -0.001 || diff > 0.001 {
		t.Errorf("TotalCost = %.6f, want ~%.6f", totalCost, expectedTotal)
	}
}

func TestCostFormatting(t *testing.T) {
	t.Parallel()

	tests := []struct {
		cost     float64
		expected string
	}{
		{0.00001, "$0.0000"},
		{0.0001, "$0.0001"},
		{0.001, "$0.0010"},
		{0.005, "$0.0050"},
		{0.01, "$0.010"},
		{0.05, "$0.050"},
		{0.10, "$0.100"},
		{0.50, "$0.500"},
		{1.00, "$1.00"},
		{5.00, "$5.00"},
		{10.00, "$10.00"},
		{99.99, "$99.99"},
		{100.00, "$100.00"},
		{1000.50, "$1000.50"},
	}

	for _, tt := range tests {
		t.Run(tt.expected, func(t *testing.T) {
			t.Parallel()

			formatted := FormatCost(tt.cost)

			t.Logf("COST_TEST: Format | Cost=%.6f | Formatted=%s", tt.cost, formatted)

			if formatted != tt.expected {
				t.Errorf("FormatCost(%.6f) = %q, want %q", tt.cost, formatted, tt.expected)
			}
		})
	}
}

func TestPerAgentTracking(t *testing.T) {
	t.Parallel()

	tracker := NewCostTracker("")

	// Record multiple interactions for the same agent
	tracker.RecordTokens("session1", "pane1", "claude-opus", 1000, 500)
	tracker.RecordTokens("session1", "pane1", "claude-opus", 2000, 1000)
	tracker.RecordTokens("session1", "pane1", "claude-opus", 3000, 1500)

	// Record for different agent
	tracker.RecordTokens("session1", "pane2", "claude-sonnet", 5000, 2500)

	session := tracker.GetSession("session1")

	// Verify pane1 accumulated correctly
	pane1 := session.Agents["pane1"]
	expectedInput := 1000 + 2000 + 3000
	expectedOutput := 500 + 1000 + 1500

	t.Logf("COST_TEST: PerAgent | Pane1 Input=%d (want %d) | Output=%d (want %d)",
		pane1.InputTokens, expectedInput, pane1.OutputTokens, expectedOutput)

	if pane1.InputTokens != expectedInput {
		t.Errorf("pane1 InputTokens = %d, want %d", pane1.InputTokens, expectedInput)
	}
	if pane1.OutputTokens != expectedOutput {
		t.Errorf("pane1 OutputTokens = %d, want %d", pane1.OutputTokens, expectedOutput)
	}

	// Verify pane2 is separate
	pane2 := session.Agents["pane2"]
	t.Logf("COST_TEST: PerAgent | Pane2 Input=%d | Output=%d",
		pane2.InputTokens, pane2.OutputTokens)

	if pane2.InputTokens != 5000 {
		t.Errorf("pane2 InputTokens = %d, want 5000", pane2.InputTokens)
	}
	if pane2.OutputTokens != 2500 {
		t.Errorf("pane2 OutputTokens = %d, want 2500", pane2.OutputTokens)
	}
}

func TestSessionTotals(t *testing.T) {
	t.Parallel()

	session := &SessionCost{
		Agents: map[string]*AgentCost{
			"pane1": {InputTokens: 10000, OutputTokens: 5000, Model: "claude-opus"},
			"pane2": {InputTokens: 20000, OutputTokens: 10000, Model: "claude-sonnet"},
			"pane3": {InputTokens: 50000, OutputTokens: 25000, Model: "claude-haiku"},
		},
	}

	// Test TotalTokens
	inputTotal, outputTotal := session.TotalTokens()
	expectedInput := 10000 + 20000 + 50000
	expectedOutput := 5000 + 10000 + 25000

	t.Logf("COST_TEST: SessionTotals | InputTokens=%d (want %d) | OutputTokens=%d (want %d)",
		inputTotal, expectedInput, outputTotal, expectedOutput)

	if inputTotal != expectedInput {
		t.Errorf("TotalTokens input = %d, want %d", inputTotal, expectedInput)
	}
	if outputTotal != expectedOutput {
		t.Errorf("TotalTokens output = %d, want %d", outputTotal, expectedOutput)
	}

	// Test TotalCost
	totalCost := session.TotalCost()
	// pane1: 10k*0.015/1k + 5k*0.075/1k = 0.15 + 0.375 = 0.525
	// pane2: 20k*0.003/1k + 10k*0.015/1k = 0.06 + 0.15 = 0.21
	// pane3: 50k*0.00025/1k + 25k*0.00125/1k = 0.0125 + 0.03125 = 0.04375
	expectedCost := 0.525 + 0.21 + 0.04375

	t.Logf("COST_TEST: SessionTotals | TotalCost=$%.4f (want $%.4f)", totalCost, expectedCost)

	diff := totalCost - expectedCost
	if diff < -0.001 || diff > 0.001 {
		t.Errorf("TotalCost = %.6f, want %.6f", totalCost, expectedCost)
	}
}

func TestHistoricalStorage(t *testing.T) {
	t.Parallel()

	tmpDir := t.TempDir()

	// Create tracker and record multiple sessions
	tracker1 := NewCostTracker(tmpDir)
	tracker1.RecordTokens("session1", "pane1", "claude-opus", 10000, 5000)
	tracker1.RecordTokens("session2", "pane1", "claude-sonnet", 20000, 10000)
	tracker1.RecordTokens("session3", "pane1", "gpt-4o", 15000, 7500)

	// Save to disk
	if err := tracker1.SaveToDir(tmpDir); err != nil {
		t.Fatalf("SaveToDir failed: %v", err)
	}

	// Create new tracker and load
	tracker2 := NewCostTracker(tmpDir)
	if err := tracker2.LoadFromDir(tmpDir); err != nil {
		t.Fatalf("LoadFromDir failed: %v", err)
	}

	// Verify all sessions were persisted
	sessions := tracker2.GetAllSessions()
	t.Logf("COST_TEST: HistoricalStorage | SessionCount=%d", len(sessions))

	if len(sessions) != 3 {
		t.Errorf("Expected 3 sessions, got %d", len(sessions))
	}

	// Verify cost data integrity
	for _, sessionName := range []string{"session1", "session2", "session3"} {
		s := tracker2.GetSession(sessionName)
		if s == nil {
			t.Errorf("Session %s not found after load", sessionName)
			continue
		}
		if len(s.Agents) != 1 {
			t.Errorf("Session %s has %d agents, want 1", sessionName, len(s.Agents))
		}
	}

	// Verify specific session data
	s1 := tracker2.GetSession("session1")
	if s1.Agents["pane1"].InputTokens != 10000 {
		t.Errorf("session1 input tokens not preserved: got %d, want 10000",
			s1.Agents["pane1"].InputTokens)
	}
}

func TestEdgeCases(t *testing.T) {
	t.Parallel()

	t.Run("very large token counts", func(t *testing.T) {
		t.Parallel()

		agent := &AgentCost{
			InputTokens:  10000000, // 10M tokens
			OutputTokens: 5000000,  // 5M tokens
			Model:        "claude-opus",
		}

		cost := agent.Cost()
		// 10M * 0.015/1k + 5M * 0.075/1k = 150 + 375 = 525
		expectedCost := 525.0

		t.Logf("COST_TEST: LargeTokens | Tokens=%d/%d | Cost=$%.2f",
			agent.InputTokens, agent.OutputTokens, cost)

		if cost != expectedCost {
			t.Errorf("Large token cost = %.2f, want %.2f", cost, expectedCost)
		}
	})

	t.Run("empty session", func(t *testing.T) {
		t.Parallel()

		session := &SessionCost{Agents: map[string]*AgentCost{}}
		cost := session.TotalCost()
		input, output := session.TotalTokens()

		t.Logf("COST_TEST: EmptySession | Cost=$%.4f | Input=%d | Output=%d",
			cost, input, output)

		if cost != 0 {
			t.Errorf("Empty session cost = %f, want 0", cost)
		}
		if input != 0 || output != 0 {
			t.Errorf("Empty session tokens = %d/%d, want 0/0", input, output)
		}
	})

	t.Run("mixed input only output only", func(t *testing.T) {
		t.Parallel()

		tracker := NewCostTracker("")
		// Input only
		tracker.RecordPrompt("session1", "pane1", "claude-opus", "Hello world test prompt")
		// Output only
		tracker.RecordResponse("session1", "pane2", "claude-opus", "Hello world test response")

		session := tracker.GetSession("session1")
		pane1 := session.Agents["pane1"]
		pane2 := session.Agents["pane2"]

		t.Logf("COST_TEST: MixedIO | Pane1(input-only) in=%d out=%d | Pane2(output-only) in=%d out=%d",
			pane1.InputTokens, pane1.OutputTokens, pane2.InputTokens, pane2.OutputTokens)

		if pane1.InputTokens == 0 {
			t.Error("pane1 should have input tokens")
		}
		if pane1.OutputTokens != 0 {
			t.Error("pane1 should have no output tokens")
		}
		if pane2.InputTokens != 0 {
			t.Error("pane2 should have no input tokens")
		}
		if pane2.OutputTokens == 0 {
			t.Error("pane2 should have output tokens")
		}
	})
}
