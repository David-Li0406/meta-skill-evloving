package agent

import (
	"testing"
)

// TestParser_StuckInWorkingBug verifies that an agent is correctly identified as Idle
// even if "working" keywords appear in the recent history, provided a prompt is present at the end.
func TestParser_StuckInWorkingBug(t *testing.T) {
	p := NewParser()

	// Scenario: Agent ran tests (producing "testing" keyword) but has finished and is waiting.
	// Before the fix, "testing" would trigger IsWorking=true, which would skip IsIdle detection.
	output := `Claude Opus 4.5
Running tests...
testing package internal/agent...
ok  	github.com/Dicklesworthstone/ntm/internal/agent	0.123s
Tests completed.
> `

	state, err := p.Parse(output)
	if err != nil {
		t.Fatalf("Parse error: %v", err)
	}

	// 1. Verify Agent Type
	if state.Type != AgentTypeClaudeCode {
		t.Errorf("Type = %v, want %v", state.Type, AgentTypeClaudeCode)
	}

	// 2. Verify Idle State (Should be TRUE because of the prompt "> ")
	if !state.IsIdle {
		t.Error("Expected IsIdle to be true because a prompt is present at the end")
	}

	// 3. Verify Working State (Should be FALSE because Idle overrides Working)
	if state.IsWorking {
		t.Error("Expected IsWorking to be false because the agent is idle, despite 'testing' keyword")
	}
}
