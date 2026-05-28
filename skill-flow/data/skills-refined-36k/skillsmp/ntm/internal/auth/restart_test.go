package auth

import (
	"testing"
	"time"

	"github.com/Dicklesworthstone/ntm/internal/config"
)

func TestWaitForShellPrompt(t *testing.T) {
	// Setup orchestrator with mocked capture
	orch := NewOrchestrator(config.Default())

	tests := []struct {
		name        string
		mockOutputs []string // Sequence of outputs to return
		timeout     time.Duration
		wantErr     bool
	}{
		{
			name: "detect bash prompt immediately",
			mockOutputs: []string{
				"user@host:~$",
			},
			timeout: 1 * time.Second,
			wantErr: false,
		},
		{
			name: "detect zsh prompt after delay",
			mockOutputs: []string{
				"output line 1",
				"output line 2",
				"user@host %",
			},
			timeout: 2 * time.Second,
			wantErr: false,
		},
		{
			name: "timeout waiting for prompt",
			mockOutputs: []string{
				"still running...",
				"still running...",
				"still running...",
			},
			timeout: 100 * time.Millisecond, // Fast timeout
			wantErr: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			idx := 0
			orch.captureOutput = func(paneID string, lines int) (string, error) {
				if idx >= len(tt.mockOutputs) {
					// Return last output if we run out
					return tt.mockOutputs[len(tt.mockOutputs)-1], nil
				}
				out := tt.mockOutputs[idx]
				idx++
				return out, nil
			}

			// Reduce ticker in WaitForShellPrompt via race condition or just rely on fast test execution?
			// The ticker is 500ms. We should probably make the test timeout slightly larger than ticker
			// or refactor ticker interval to be configurable.
			// For this test, let's just accept the 500ms poll and ensure our timeout allows for it.
			// Actually, mocking ticker is hard without further refactoring.
			// Let's rely on the timeout behavior.

			start := time.Now()
			err := orch.WaitForShellPrompt("dummy", tt.timeout)
			duration := time.Since(start)

			if (err != nil) != tt.wantErr {
				t.Errorf("WaitForShellPrompt() error = %v, wantErr %v", err, tt.wantErr)
			}

			if !tt.wantErr && duration > tt.timeout {
				t.Errorf("WaitForShellPrompt() took %v, want < %v", duration, tt.timeout)
			}
		})
	}
}

// Mock test for ExecuteRestartStrategy would require mocking TerminateSession and StartNewAgentSession
// which are methods on the struct.
// To test ExecuteRestartStrategy fully, we'd need to mock tmux calls inside those methods or interface them out.
// Given the scope, testing logic of WaitForShellPrompt is the most critical part of this task.
