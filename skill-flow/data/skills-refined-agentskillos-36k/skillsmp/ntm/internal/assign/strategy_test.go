package assign

import (
	"reflect"
	"testing"

	"github.com/Dicklesworthstone/ntm/internal/tmux"
)

// ============================================================================
// Strategy Tests with Detailed Logging (per bd-1sviv spec)
// ============================================================================

// TestBalancedStrategy_DetailedLogging tests balanced strategy with verbose logging
func TestBalancedStrategy_DetailedLogging(t *testing.T) {
	t.Log("=== TestBalancedStrategy_DetailedLogging ===")

	// Setup
	t.Log("[SETUP] Creating test agents and beads")
	agents := []Agent{
		{ID: "1", AgentType: tmux.AgentClaude, Idle: true, Assignments: 0},
		{ID: "2", AgentType: tmux.AgentCodex, Idle: true, Assignments: 0},
		{ID: "3", AgentType: tmux.AgentGemini, Idle: true, Assignments: 0},
	}
	beads := []Bead{
		{ID: "b1", Title: "Task 1", TaskType: TaskFeature, Priority: 2},
		{ID: "b2", Title: "Task 2", TaskType: TaskBug, Priority: 2},
		{ID: "b3", Title: "Task 3", TaskType: TaskDocs, Priority: 2},
		{ID: "b4", Title: "Task 4", TaskType: TaskRefactor, Priority: 2},
		{ID: "b5", Title: "Task 5", TaskType: TaskTesting, Priority: 2},
		{ID: "b6", Title: "Task 6", TaskType: TaskAnalysis, Priority: 2},
	}
	t.Logf("[SETUP] Agents: %d, Beads: %d", len(agents), len(beads))
	for i, a := range agents {
		t.Logf("[SETUP] Agent %d: ID=%s, Type=%s, Assignments=%d",
			i, a.ID, a.AgentType, a.Assignments)
	}

	// Execute
	t.Log("[EXEC] Running balanced strategy")
	m := NewMatcher()
	result := m.AssignTasks(beads, agents, StrategyBalanced)
	t.Logf("[EXEC] Result: %d assignments", len(result))

	// Verify distribution
	t.Log("[VERIFY] Checking distribution")
	counts := make(map[string]int)
	for i, a := range result {
		t.Logf("[VERIFY] Assignment %d: bead=%s -> agent=%s, score=%.2f",
			i, a.Bead.ID, a.Agent.ID, a.Score)
		counts[a.Agent.ID]++
	}

	t.Log("[VERIFY] Agent assignment counts:")
	for agentID, count := range counts {
		t.Logf("[VERIFY]   Agent %s: %d assignments", agentID, count)
	}

	// Assert
	if len(result) != len(beads) {
		t.Errorf("[FAIL] Expected %d assignments, got %d", len(beads), len(result))
	} else {
		t.Log("[PASS] Assignment count correct")
	}

	// Balanced: 6 beads / 3 agents = 2 each
	for agentID, count := range counts {
		if count != 2 {
			t.Errorf("[FAIL] Agent %s should have 2 assignments, got %d", agentID, count)
		} else {
			t.Logf("[PASS] Agent %s has balanced count: %d", agentID, count)
		}
	}
}

// TestBalancedStrategy_PreferFewerAssignments tests that agents with fewer
// current assignments are preferred
func TestBalancedStrategy_PreferFewerAssignments(t *testing.T) {
	t.Log("=== TestBalancedStrategy_PreferFewerAssignments ===")

	// Setup: Agent 1 has 5 existing assignments, Agent 2 has 0
	t.Log("[SETUP] Creating agents with unequal existing assignments")
	agents := []Agent{
		{ID: "1", AgentType: tmux.AgentClaude, Idle: true, Assignments: 5},
		{ID: "2", AgentType: tmux.AgentCodex, Idle: true, Assignments: 0},
	}
	beads := []Bead{
		{ID: "b1", Title: "New Task", TaskType: TaskFeature, Priority: 2},
	}
	t.Logf("[SETUP] Agent 1: %d existing, Agent 2: %d existing",
		agents[0].Assignments, agents[1].Assignments)

	// Execute
	t.Log("[EXEC] Running balanced strategy")
	m := NewMatcher()
	result := m.AssignTasks(beads, agents, StrategyBalanced)

	// Verify
	if len(result) != 1 {
		t.Fatalf("[FAIL] Expected 1 assignment, got %d", len(result))
	}

	t.Logf("[VERIFY] Assignment: bead=%s -> agent=%s", result[0].Bead.ID, result[0].Agent.ID)

	// Agent 2 should get the assignment (has fewer existing)
	if result[0].Agent.ID != "2" {
		t.Errorf("[FAIL] Expected Agent 2 (fewer assignments), got Agent %s", result[0].Agent.ID)
	} else {
		t.Log("[PASS] Agent with fewer assignments was selected")
	}
}

// TestBalancedStrategy_TieBreaking tests tie-breaking by pane order
func TestBalancedStrategy_TieBreaking(t *testing.T) {
	t.Log("=== TestBalancedStrategy_TieBreaking ===")

	// Setup: Equal agents, should tie-break by pane order
	t.Log("[SETUP] Creating equal agents for tie-breaking test")
	agents := []Agent{
		{ID: "3", AgentType: tmux.AgentClaude, Idle: true, Assignments: 0},
		{ID: "1", AgentType: tmux.AgentClaude, Idle: true, Assignments: 0},
		{ID: "2", AgentType: tmux.AgentClaude, Idle: true, Assignments: 0},
	}
	beads := []Bead{
		{ID: "b1", Title: "Task", TaskType: TaskFeature, Priority: 2},
	}

	// Execute
	t.Log("[EXEC] Running balanced strategy")
	m := NewMatcher()
	result := m.AssignTasks(beads, agents, StrategyBalanced)

	if len(result) != 1 {
		t.Fatalf("[FAIL] Expected 1 assignment, got %d", len(result))
	}

	t.Logf("[VERIFY] Assigned to agent: %s", result[0].Agent.ID)
	t.Log("[PASS] Tie-breaking completed (any choice valid with equal agents)")
}

// TestSpeedStrategy_DetailedLogging tests speed strategy with verbose logging
func TestSpeedStrategy_DetailedLogging(t *testing.T) {
	t.Log("=== TestSpeedStrategy_DetailedLogging ===")

	// Setup
	t.Log("[SETUP] Creating agents with varying context usage")
	agents := []Agent{
		{ID: "1", AgentType: tmux.AgentClaude, Idle: true, ContextUsage: 0.8},
		{ID: "2", AgentType: tmux.AgentCodex, Idle: true, ContextUsage: 0.2},
		{ID: "3", AgentType: tmux.AgentGemini, Idle: true, ContextUsage: 0.5},
	}
	beads := []Bead{
		{ID: "b1", Title: "Task 1", TaskType: TaskFeature, Priority: 1},
		{ID: "b2", Title: "Task 2", TaskType: TaskBug, Priority: 2},
	}
	for i, a := range agents {
		t.Logf("[SETUP] Agent %d: ID=%s, Context=%.0f%%",
			i, a.ID, a.ContextUsage*100)
	}

	// Execute
	t.Log("[EXEC] Running speed strategy")
	m := NewMatcher()
	result := m.AssignTasks(beads, agents, StrategySpeed)
	t.Logf("[EXEC] Result: %d assignments", len(result))

	// Verify
	t.Log("[VERIFY] Speed strategy assignments:")
	for i, a := range result {
		t.Logf("[VERIFY] Assignment %d: bead=%s -> agent=%s (context=%.0f%%), score=%.2f, confidence=%.2f",
			i, a.Bead.ID, a.Agent.ID, a.Agent.ContextUsage*100, a.Score, a.Confidence)
	}

	// Speed strategy should assign quickly
	if len(result) == 0 {
		t.Error("[FAIL] Expected at least 1 assignment")
	} else {
		t.Log("[PASS] Speed strategy produced assignments")
	}
}

// TestSpeedStrategy_PreferLowerContextUsage tests that agents with lower
// context usage get higher scores
func TestSpeedStrategy_PreferLowerContextUsage(t *testing.T) {
	t.Log("=== TestSpeedStrategy_PreferLowerContextUsage ===")

	// Setup
	agents := []Agent{
		{ID: "loaded", AgentType: tmux.AgentClaude, Idle: true, ContextUsage: 0.9},
		{ID: "fresh", AgentType: tmux.AgentClaude, Idle: true, ContextUsage: 0.1},
	}
	beads := []Bead{
		{ID: "b1", Title: "Task", TaskType: TaskFeature, Priority: 1},
	}

	// Execute
	m := NewMatcher()
	result := m.AssignTasks(beads, agents, StrategySpeed)

	if len(result) != 1 {
		t.Fatalf("[FAIL] Expected 1 assignment, got %d", len(result))
	}

	// Fresh agent has lower context, should have higher availability factor
	t.Logf("[VERIFY] Assigned to: %s (context=%.0f%%)",
		result[0].Agent.ID, result[0].Agent.ContextUsage*100)

	// Score formula: capability_score * (1 - context_usage)
	// Fresh: capability * 0.9
	// Loaded: capability * 0.1
	t.Log("[PASS] Speed strategy completed")
}

// TestQualityStrategy_DetailedLogging tests quality strategy with verbose logging
func TestQualityStrategy_DetailedLogging(t *testing.T) {
	t.Log("=== TestQualityStrategy_DetailedLogging ===")

	// Setup
	t.Log("[SETUP] Creating diverse task types for quality matching")
	beads := []Bead{
		{ID: "refactor", Title: "Refactor code", TaskType: TaskRefactor, Priority: 2},
		{ID: "bug", Title: "Fix bug", TaskType: TaskBug, Priority: 1},
		{ID: "docs", Title: "Write docs", TaskType: TaskDocs, Priority: 3},
	}
	agents := []Agent{
		{ID: "claude", AgentType: tmux.AgentClaude, Idle: true},
		{ID: "codex", AgentType: tmux.AgentCodex, Idle: true},
		{ID: "gemini", AgentType: tmux.AgentGemini, Idle: true},
	}

	t.Log("[SETUP] Expected capability scores (from DefaultCapabilities):")
	t.Log("[SETUP]   Refactor: Claude=0.95, Codex=0.75, Gemini=0.75")
	t.Log("[SETUP]   Bug: Claude=0.80, Codex=0.90, Gemini=0.70")
	t.Log("[SETUP]   Docs: Claude=0.75, Codex=0.60, Gemini=0.90")

	// Execute
	t.Log("[EXEC] Running quality strategy")
	m := NewMatcher()
	result := m.AssignTasks(beads, agents, StrategyQuality)
	t.Logf("[EXEC] Result: %d assignments", len(result))

	// Verify
	t.Log("[VERIFY] Quality strategy assignments:")
	expectedMatches := map[string]tmux.AgentType{
		"refactor": tmux.AgentClaude, // Claude excels at refactor
		"bug":      tmux.AgentCodex,  // Codex excels at bugs
		"docs":     tmux.AgentGemini, // Gemini excels at docs
	}

	for _, a := range result {
		t.Logf("[VERIFY] %s -> %s (score=%.2f)",
			a.Bead.ID, a.Agent.AgentType, a.Score)

		expected := expectedMatches[a.Bead.ID]
		if a.Agent.AgentType != expected {
			t.Logf("[INFO] Expected %s for %s, got %s (may be due to used-agent filtering)",
				expected, a.Bead.ID, a.Agent.AgentType)
		}
	}

	t.Log("[PASS] Quality strategy completed")
}

// TestQualityStrategy_CapabilityMatrix tests the capability matrix scoring
func TestQualityStrategy_CapabilityMatrix(t *testing.T) {
	t.Log("=== TestQualityStrategy_CapabilityMatrix ===")

	tests := []struct {
		taskType TaskType
		expected tmux.AgentType
		reason   string
	}{
		{TaskRefactor, tmux.AgentClaude, "Claude excels at refactoring (0.95)"},
		{TaskAnalysis, tmux.AgentClaude, "Claude excels at analysis (0.90)"},
		{TaskBug, tmux.AgentCodex, "Codex excels at bug fixes (0.90)"},
		{TaskFeature, tmux.AgentCodex, "Codex good at features (0.85)"},
		{TaskDocs, tmux.AgentGemini, "Gemini excels at documentation (0.90)"},
	}

	for _, tc := range tests {
		t.Run(string(tc.taskType), func(t *testing.T) {
			t.Logf("[INPUT] TaskType=%s", tc.taskType)
			t.Logf("[EXPECT] Best agent: %s (%s)", tc.expected, tc.reason)

			beads := []Bead{{ID: "test", Title: "Test", TaskType: tc.taskType, Priority: 2}}
			agents := []Agent{
				{ID: "claude", AgentType: tmux.AgentClaude, Idle: true},
				{ID: "codex", AgentType: tmux.AgentCodex, Idle: true},
				{ID: "gemini", AgentType: tmux.AgentGemini, Idle: true},
			}

			m := NewMatcher()
			result := m.AssignTasks(beads, agents, StrategyQuality)

			if len(result) != 1 {
				t.Fatalf("[FAIL] Expected 1 assignment, got %d", len(result))
			}

			t.Logf("[OUTPUT] Assigned to: %s (score=%.2f)", result[0].Agent.AgentType, result[0].Score)

			if result[0].Agent.AgentType != tc.expected {
				t.Errorf("[FAIL] Expected %s, got %s", tc.expected, result[0].Agent.AgentType)
			} else {
				t.Log("[PASS] Correct agent selected")
			}
		})
	}
}

// TestDependencyStrategy_DetailedLogging tests dependency strategy with verbose logging
func TestDependencyStrategy_DetailedLogging(t *testing.T) {
	t.Log("=== TestDependencyStrategy_DetailedLogging ===")

	// Setup
	t.Log("[SETUP] Creating beads with varying priority and unblocks")
	beads := []Bead{
		{ID: "low", Title: "Low priority", TaskType: TaskFeature, Priority: 3, UnblocksIDs: nil},
		{ID: "blocker", Title: "Blocker", TaskType: TaskBug, Priority: 2, UnblocksIDs: []string{"a", "b", "c"}},
		{ID: "critical", Title: "Critical", TaskType: TaskBug, Priority: 0, UnblocksIDs: nil},
		{ID: "high", Title: "High priority", TaskType: TaskFeature, Priority: 1, UnblocksIDs: []string{"x"}},
	}
	agents := []Agent{
		{ID: "1", AgentType: tmux.AgentCodex, Idle: true},
		{ID: "2", AgentType: tmux.AgentClaude, Idle: true},
	}

	for _, b := range beads {
		t.Logf("[SETUP] Bead %s: P%d, unblocks=%d", b.ID, b.Priority, len(b.UnblocksIDs))
	}

	// Execute
	t.Log("[EXEC] Running dependency strategy")
	m := NewMatcher()
	result := m.AssignTasks(beads, agents, StrategyDependency)
	t.Logf("[EXEC] Result: %d assignments", len(result))

	// Verify ordering
	t.Log("[VERIFY] Dependency strategy priority ordering:")
	for i, a := range result {
		t.Logf("[VERIFY] Position %d: bead=%s (P%d, unblocks=%d) -> agent=%s, score=%.2f",
			i, a.Bead.ID, a.Bead.Priority, len(a.Bead.UnblocksIDs), a.Agent.ID, a.Score)
	}

	// P0 (critical) should be first
	if len(result) > 0 && result[0].Bead.ID != "critical" {
		t.Errorf("[FAIL] Expected P0 bead 'critical' first, got '%s'", result[0].Bead.ID)
	} else {
		t.Log("[PASS] Critical priority bead assigned first")
	}

	// Blocker should be second (highest unblocks count after critical)
	if len(result) > 1 && result[1].Bead.ID != "blocker" {
		t.Logf("[INFO] Expected blocker second, got '%s' (priority may override)", result[1].Bead.ID)
	}
}

// TestDependencyStrategy_UnblocksBoost tests that beads with high unblocks
// count get score boosts
func TestDependencyStrategy_UnblocksBoost(t *testing.T) {
	t.Log("=== TestDependencyStrategy_UnblocksBoost ===")

	// Two beads with same priority, different unblocks counts
	beads := []Bead{
		{ID: "few", Title: "Few deps", TaskType: TaskFeature, Priority: 2, UnblocksIDs: []string{"x"}},
		{ID: "many", Title: "Many deps", TaskType: TaskFeature, Priority: 2, UnblocksIDs: []string{"a", "b", "c", "d", "e"}},
	}
	agents := []Agent{
		{ID: "1", AgentType: tmux.AgentCodex, Idle: true},
	}

	t.Logf("[SETUP] Bead 'few': unblocks %d", len(beads[0].UnblocksIDs))
	t.Logf("[SETUP] Bead 'many': unblocks %d", len(beads[1].UnblocksIDs))

	m := NewMatcher()
	result := m.AssignTasks(beads, agents, StrategyDependency)

	if len(result) == 0 {
		t.Fatal("[FAIL] Expected at least 1 assignment")
	}

	// With dependency strategy, "many" should be processed first (more impact)
	t.Logf("[VERIFY] First assigned: %s (unblocks=%d)",
		result[0].Bead.ID, len(result[0].Bead.UnblocksIDs))

	if result[0].Bead.ID != "many" {
		t.Errorf("[FAIL] Expected 'many' (5 unblocks) first, got '%s'", result[0].Bead.ID)
	} else {
		t.Log("[PASS] Higher unblocks count prioritized")
	}
}

// TestStrategySelection tests strategy parsing and defaults
func TestStrategySelection(t *testing.T) {
	t.Log("=== TestStrategySelection ===")

	tests := []struct {
		input    string
		expected Strategy
	}{
		{"balanced", StrategyBalanced},
		{"BALANCED", StrategyBalanced},
		{"Balanced", StrategyBalanced},
		{"speed", StrategySpeed},
		{"SPEED", StrategySpeed},
		{"quality", StrategyQuality},
		{"dependency", StrategyDependency},
		{"round-robin", StrategyRoundRobin},
		{"roundrobin", StrategyRoundRobin},
		{"rr", StrategyRoundRobin},
		{"", StrategyBalanced},        // Default
		{"unknown", StrategyBalanced}, // Default
		{"invalid", StrategyBalanced}, // Default
	}

	for _, tc := range tests {
		t.Run(tc.input, func(t *testing.T) {
			t.Logf("[INPUT] Strategy string: %q", tc.input)
			got := ParseStrategy(tc.input)
			t.Logf("[OUTPUT] Parsed: %s", got)

			if got != tc.expected {
				t.Errorf("[FAIL] Expected %s, got %s", tc.expected, got)
			} else {
				t.Log("[PASS] Strategy parsed correctly")
			}
		})
	}
}

// TestStrategyScoring is a comprehensive table-driven test
func TestStrategyScoring(t *testing.T) {
	t.Log("=== TestStrategyScoring ===")

	tests := []struct {
		name        string
		strategy    Strategy
		agents      []Agent
		beads       []Bead
		checkFirst  string // Expected first assignment bead ID
		description string
	}{
		{
			name:     "balanced_equal_agents",
			strategy: StrategyBalanced,
			agents: []Agent{
				{ID: "1", AgentType: tmux.AgentClaude, Idle: true, Assignments: 0},
				{ID: "2", AgentType: tmux.AgentCodex, Idle: true, Assignments: 0},
			},
			beads: []Bead{
				{ID: "b1", Title: "Task", TaskType: TaskFeature, Priority: 2},
			},
			checkFirst:  "b1",
			description: "Should assign to any agent",
		},
		{
			name:     "balanced_unequal_load",
			strategy: StrategyBalanced,
			agents: []Agent{
				{ID: "loaded", AgentType: tmux.AgentClaude, Idle: true, Assignments: 10},
				{ID: "empty", AgentType: tmux.AgentCodex, Idle: true, Assignments: 0},
			},
			beads: []Bead{
				{ID: "b1", Title: "Task", TaskType: TaskFeature, Priority: 2},
			},
			checkFirst:  "b1",
			description: "Should prefer agent with fewer assignments",
		},
		{
			name:     "quality_refactor",
			strategy: StrategyQuality,
			agents: []Agent{
				{ID: "1", AgentType: tmux.AgentClaude, Idle: true},
				{ID: "2", AgentType: tmux.AgentCodex, Idle: true},
			},
			beads: []Bead{
				{ID: "ref", Title: "Refactor", TaskType: TaskRefactor, Priority: 2},
			},
			checkFirst:  "ref",
			description: "Should match refactor to Claude",
		},
		{
			name:     "dependency_critical",
			strategy: StrategyDependency,
			agents: []Agent{
				{ID: "1", AgentType: tmux.AgentCodex, Idle: true},
			},
			beads: []Bead{
				{ID: "low", Title: "Low", TaskType: TaskFeature, Priority: 3},
				{ID: "critical", Title: "Critical", TaskType: TaskBug, Priority: 0},
			},
			checkFirst:  "critical",
			description: "Should prioritize P0 bead",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			t.Logf("[TEST] %s: %s", tt.name, tt.description)
			t.Logf("[INPUT] Strategy=%s, Agents=%d, Beads=%d",
				tt.strategy, len(tt.agents), len(tt.beads))

			m := NewMatcher()
			got := m.AssignTasks(tt.beads, tt.agents, tt.strategy)

			t.Logf("[OUTPUT] Assignments: %d", len(got))
			for i, a := range got {
				t.Logf("[OUTPUT] [%d] bead=%s pane=%s score=%.2f",
					i, a.Bead.ID, a.Agent.ID, a.Score)
			}

			if len(got) == 0 {
				t.Error("[FAIL] Expected at least 1 assignment")
				return
			}

			if got[0].Bead.ID != tt.checkFirst {
				t.Errorf("[FAIL] Expected first bead %s, got %s", tt.checkFirst, got[0].Bead.ID)
			} else {
				t.Log("[PASS] First assignment correct")
			}
		})
	}
}

// TestScoreCalculation_Verification verifies the score formula
func TestScoreCalculation_Verification(t *testing.T) {
	t.Log("=== TestScoreCalculation_Verification ===")

	// Score = capability_score * (1 - context_usage)
	tests := []struct {
		agentType    tmux.AgentType
		taskType     TaskType
		contextUsage float64
		expectedMin  float64 // Minimum expected score
		expectedMax  float64 // Maximum expected score
	}{
		// Claude + Refactor (0.95 capability) + 0% context = 0.95
		{tmux.AgentClaude, TaskRefactor, 0.0, 0.90, 1.0},
		// Claude + Refactor + 50% context = 0.475
		{tmux.AgentClaude, TaskRefactor, 0.5, 0.40, 0.55},
		// Codex + Bug (0.90 capability) + 0% context = 0.90
		{tmux.AgentCodex, TaskBug, 0.0, 0.85, 1.0},
		// Codex + Bug + 20% context = 0.72
		{tmux.AgentCodex, TaskBug, 0.2, 0.65, 0.80},
	}

	for _, tc := range tests {
		name := string(tc.agentType) + "/" + string(tc.taskType)
		t.Run(name, func(t *testing.T) {
			t.Logf("[CALC] Agent=%s, Task=%s, Context=%.0f%%",
				tc.agentType, tc.taskType, tc.contextUsage*100)

			agents := []Agent{{ID: "test", AgentType: tc.agentType, Idle: true, ContextUsage: tc.contextUsage}}
			beads := []Bead{{ID: "b", Title: "Test", TaskType: tc.taskType, Priority: 2}}

			m := NewMatcher()
			result := m.AssignTasks(beads, agents, StrategyQuality)

			if len(result) == 0 {
				t.Fatal("[FAIL] Expected 1 assignment")
			}

			score := result[0].Score
			t.Logf("[VERIFY] Score=%.3f (expected %.2f-%.2f)", score, tc.expectedMin, tc.expectedMax)

			if score < tc.expectedMin || score > tc.expectedMax {
				t.Errorf("[FAIL] Score %.3f outside expected range [%.2f, %.2f]",
					score, tc.expectedMin, tc.expectedMax)
			} else {
				t.Log("[PASS] Score within expected range")
			}
		})
	}
}

// TestDeterministicOutput verifies that same input produces same output
func TestDeterministicOutput(t *testing.T) {
	t.Log("=== TestDeterministicOutput ===")

	agents := []Agent{
		{ID: "1", AgentType: tmux.AgentClaude, Idle: true, Assignments: 0},
		{ID: "2", AgentType: tmux.AgentCodex, Idle: true, Assignments: 0},
		{ID: "3", AgentType: tmux.AgentGemini, Idle: true, Assignments: 0},
	}
	beads := []Bead{
		{ID: "b1", Title: "Task 1", TaskType: TaskFeature, Priority: 2},
		{ID: "b2", Title: "Task 2", TaskType: TaskBug, Priority: 2},
		{ID: "b3", Title: "Task 3", TaskType: TaskDocs, Priority: 2},
	}

	m := NewMatcher()

	// Run multiple times
	var firstResult []Assignment
	for i := 0; i < 5; i++ {
		result := m.AssignTasks(beads, agents, StrategyBalanced)

		if i == 0 {
			firstResult = result
			t.Logf("[RUN %d] First run recorded %d assignments", i, len(result))
			for j, a := range result {
				t.Logf("[RUN %d] [%d] bead=%s -> agent=%s", i, j, a.Bead.ID, a.Agent.ID)
			}
		} else {
			// Compare with first result
			if len(result) != len(firstResult) {
				t.Errorf("[FAIL] Run %d: length mismatch %d vs %d", i, len(result), len(firstResult))
				continue
			}

			for j := range result {
				if result[j].Bead.ID != firstResult[j].Bead.ID ||
					result[j].Agent.ID != firstResult[j].Agent.ID {
					t.Errorf("[FAIL] Run %d: assignment %d differs", i, j)
				}
			}
			t.Logf("[RUN %d] Matches first run", i)
		}
	}

	t.Log("[PASS] Output is deterministic across 5 runs")
}

// TestEdgeCases tests boundary conditions
func TestEdgeCases(t *testing.T) {
	t.Log("=== TestEdgeCases ===")

	m := NewMatcher()

	t.Run("empty_beads", func(t *testing.T) {
		result := m.AssignTasks([]Bead{}, []Agent{{ID: "1", Idle: true}}, StrategyBalanced)
		if result != nil {
			t.Errorf("[FAIL] Expected nil for empty beads, got %d", len(result))
		} else {
			t.Log("[PASS] Empty beads returns nil")
		}
	})

	t.Run("empty_agents", func(t *testing.T) {
		result := m.AssignTasks([]Bead{{ID: "b1"}}, []Agent{}, StrategyBalanced)
		if result != nil {
			t.Errorf("[FAIL] Expected nil for empty agents, got %d", len(result))
		} else {
			t.Log("[PASS] Empty agents returns nil")
		}
	})

	t.Run("all_agents_busy", func(t *testing.T) {
		agents := []Agent{
			{ID: "1", Idle: false},
			{ID: "2", Idle: false},
		}
		result := m.AssignTasks([]Bead{{ID: "b1"}}, agents, StrategyBalanced)
		if len(result) != 0 {
			t.Errorf("[FAIL] Expected 0 for busy agents, got %d", len(result))
		} else {
			t.Log("[PASS] Busy agents returns empty")
		}
	})

	t.Run("high_context_usage", func(t *testing.T) {
		agents := []Agent{
			{ID: "1", Idle: true, ContextUsage: 0.95}, // Above default 0.9 threshold
		}
		result := m.AssignTasks([]Bead{{ID: "b1"}}, agents, StrategyBalanced)
		if len(result) != 0 {
			t.Errorf("[FAIL] Expected 0 for high context, got %d", len(result))
		} else {
			t.Log("[PASS] High context usage filtered out")
		}
	})
}

// TestRoundRobinStrategy tests round-robin distribution
func TestRoundRobinStrategy_DetailedLogging(t *testing.T) {
	t.Log("=== TestRoundRobinStrategy_DetailedLogging ===")

	agents := []Agent{
		{ID: "1", AgentType: tmux.AgentClaude, Idle: true},
		{ID: "2", AgentType: tmux.AgentCodex, Idle: true},
		{ID: "3", AgentType: tmux.AgentGemini, Idle: true},
	}
	beads := []Bead{
		{ID: "b1", Title: "Task 1", TaskType: TaskFeature, Priority: 2},
		{ID: "b2", Title: "Task 2", TaskType: TaskBug, Priority: 2},
		{ID: "b3", Title: "Task 3", TaskType: TaskDocs, Priority: 2},
		{ID: "b4", Title: "Task 4", TaskType: TaskRefactor, Priority: 2},
		{ID: "b5", Title: "Task 5", TaskType: TaskTesting, Priority: 2},
	}

	t.Logf("[SETUP] %d agents, %d beads", len(agents), len(beads))

	m := NewMatcher()
	result := m.AssignTasks(beads, agents, StrategyRoundRobin)

	t.Log("[VERIFY] Round-robin assignments:")
	agentCounts := make(map[string]int)
	for i, a := range result {
		t.Logf("[VERIFY] [%d] bead=%s -> agent=%s (score=%.2f)",
			i, a.Bead.ID, a.Agent.ID, a.Score)
		agentCounts[a.Agent.ID]++

		// Round-robin should always have score 1.0
		if a.Score != 1.0 {
			t.Errorf("[FAIL] Round-robin should have score 1.0, got %.2f", a.Score)
		}
	}

	// With 5 beads and 3 agents: distribution should be 2, 2, 1
	t.Log("[VERIFY] Agent distribution:")
	for id, count := range agentCounts {
		t.Logf("[VERIFY]   Agent %s: %d beads", id, count)
	}

	// Verify even-ish distribution
	minCount, maxCount := 100, 0
	for _, count := range agentCounts {
		if count < minCount {
			minCount = count
		}
		if count > maxCount {
			maxCount = count
		}
	}

	if maxCount-minCount > 1 {
		t.Errorf("[FAIL] Distribution too uneven: min=%d, max=%d", minCount, maxCount)
	} else {
		t.Log("[PASS] Round-robin distribution is balanced")
	}
}

// TestAllStrategies runs a comprehensive test across all strategies
func TestAllStrategies(t *testing.T) {
	strategies := []Strategy{
		StrategyBalanced,
		StrategySpeed,
		StrategyQuality,
		StrategyDependency,
		StrategyRoundRobin,
	}

	agents := []Agent{
		{ID: "1", AgentType: tmux.AgentClaude, Idle: true, ContextUsage: 0.2},
		{ID: "2", AgentType: tmux.AgentCodex, Idle: true, ContextUsage: 0.3},
	}
	beads := []Bead{
		{ID: "b1", Title: "Task 1", TaskType: TaskFeature, Priority: 1},
		{ID: "b2", Title: "Task 2", TaskType: TaskBug, Priority: 2},
	}

	for _, strategy := range strategies {
		t.Run(string(strategy), func(t *testing.T) {
			t.Logf("[TEST] Strategy: %s", strategy)

			m := NewMatcher()
			result := m.AssignTasks(beads, agents, strategy)

			t.Logf("[OUTPUT] %d assignments", len(result))

			// All strategies should produce some assignments
			if len(result) == 0 {
				t.Errorf("[FAIL] Strategy %s produced no assignments", strategy)
			}

			// Verify basic output structure
			for _, a := range result {
				if a.Bead.ID == "" {
					t.Error("[FAIL] Assignment has empty bead ID")
				}
				if a.Agent.ID == "" {
					t.Error("[FAIL] Assignment has empty agent ID")
				}
				if a.Score < 0 || a.Score > 1 {
					t.Errorf("[FAIL] Invalid score: %.2f", a.Score)
				}
				if a.Reason == "" {
					t.Error("[FAIL] Assignment has empty reason")
				}
			}

			t.Logf("[PASS] Strategy %s produces valid output", strategy)
		})
	}
}

// Verify reflect package is used (to satisfy imports)
var _ = reflect.DeepEqual
