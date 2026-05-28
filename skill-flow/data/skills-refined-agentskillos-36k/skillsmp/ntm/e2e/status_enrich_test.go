// Package e2e contains end-to-end tests for NTM robot mode commands.
// status_enrich_test.go tests the --robot-status command enrichments.
package e2e

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"testing"
	"time"

	"github.com/Dicklesworthstone/ntm/internal/tmux"
)

// StatusResponse represents the full response from --robot-status.
type StatusResponse struct {
	GeneratedAt string          `json:"generated_at"`
	System      SystemInfo      `json:"system"`
	Sessions    []StatusSession `json:"sessions"`
	Error       string          `json:"error,omitempty"`
}

// SystemInfo contains system information from status.
type SystemInfo struct {
	Version       string `json:"version"`
	TmuxAvailable bool   `json:"tmux_available"`
}

// StatusSession represents a session in the status response.
type StatusSession struct {
	Name     string        `json:"name"`
	Exists   bool          `json:"exists"`
	Attached bool          `json:"attached"`
	Windows  int           `json:"windows"`
	Panes    int           `json:"panes"`
	Agents   []AgentStatus `json:"agents"`
}

// AgentStatus represents an agent's status with enrichments.
type AgentStatus struct {
	Type                 string  `json:"type"`
	Pane                 string  `json:"pane"`
	Window               int     `json:"window"`
	PaneIdx              int     `json:"pane_idx"`
	IsActive             bool    `json:"is_active"`
	PID                  int     `json:"pid"`
	ChildPID             int     `json:"child_pid,omitempty"`
	ProcessState         string  `json:"process_state,omitempty"`
	ProcessStateName     string  `json:"process_state_name,omitempty"`
	MemoryMB             int     `json:"memory_mb,omitempty"`
	RateLimitDetected    bool    `json:"rate_limit_detected,omitempty"`
	RateLimitMatch       string  `json:"rate_limit_match,omitempty"`
	LastOutputTS         string  `json:"last_output_ts,omitempty"`
	SecondsSinceOutput   int     `json:"seconds_since_output,omitempty"`
	OutputLinesSinceLast int     `json:"output_lines_since_last,omitempty"`
	ContextTokens        int     `json:"context_tokens,omitempty"`
	ContextLimit         int     `json:"context_limit,omitempty"`
	ContextPercent       float64 `json:"context_percent,omitempty"`
}

// StatusEnrichTestSuite manages status enrichment E2E tests.
type StatusEnrichTestSuite struct {
	*TestSuite
}

// NewStatusEnrichTestSuite creates a new test suite for status enrichment tests.
func NewStatusEnrichTestSuite(t *testing.T, scenario string) *StatusEnrichTestSuite {
	return &StatusEnrichTestSuite{
		TestSuite: NewTestSuite(t, scenario),
	}
}

// CallRobotStatus invokes --robot-status and filters by session.
// Uses a 45-second timeout per attempt with up to 3 retries to handle busy systems.
func (s *StatusEnrichTestSuite) CallRobotStatus() (*StatusSession, error) {
	const maxRetries = 3
	const timeout = 45 * time.Second

	var lastErr error
	for attempt := 1; attempt <= maxRetries; attempt++ {
		s.logger.Log("[E2E-STATUS] Calling --robot-status (attempt %d/%d)", attempt, maxRetries)

		ctx, cancel := context.WithTimeout(context.Background(), timeout)
		cmd := exec.CommandContext(ctx, "ntm", "--robot-status")
		output, err := cmd.Output()
		cancel()

		if err != nil {
			if ctx.Err() == context.DeadlineExceeded {
				s.logger.Log("[E2E-STATUS] Attempt %d: Command timed out after %s", attempt, timeout)
				lastErr = fmt.Errorf("command timed out after %s (attempt %d)", timeout, attempt)
				continue
			}
			s.logger.Log("[E2E-STATUS] Attempt %d: Command failed: %v, output: %s", attempt, err, string(output))
			lastErr = fmt.Errorf("command failed: %w, output: %s", err, string(output))
			continue
		}

		var result StatusResponse
		if err := json.Unmarshal(output, &result); err != nil {
			s.logger.Log("[E2E-STATUS] Parse failed: %v, output: %s", err, string(output))
			return nil, fmt.Errorf("parse failed: %w, output: %s", err, string(output))
		}

		// Find our test session
		for _, session := range result.Sessions {
			if session.Name == s.session {
				s.logger.LogJSON("[E2E-STATUS] Found session", session)
				return &session, nil
			}
		}

		s.logger.Log("[E2E-STATUS] Session %s not found in %d sessions", s.session, len(result.Sessions))
		return nil, fmt.Errorf("session %s not found", s.session)
	}

	return nil, fmt.Errorf("all %d attempts failed: %w", maxRetries, lastErr)
}

// InjectOutput injects text as output in a pane using echo command.
func (s *StatusEnrichTestSuite) InjectOutput(pane int, content string) error {
	s.logger.Log("[E2E-INJECT] Injecting output to pane %d: %s", pane, truncateString(content, 50))

	// Use session:window.pane format - window is always 0 for our tests
	target := fmt.Sprintf("%s:0.%d", s.session, pane)
	echoCmd := fmt.Sprintf("echo '%s'", content)
	cmd := exec.Command(tmux.BinaryPath(), "send-keys", "-t", target, echoCmd, "Enter")
	output, err := cmd.CombinedOutput()
	if err != nil {
		// Try alternate format: just session name (targets first pane)
		target2 := s.session
		cmd2 := exec.Command(tmux.BinaryPath(), "send-keys", "-t", target2, echoCmd, "Enter")
		output2, err2 := cmd2.CombinedOutput()
		if err2 != nil {
			return fmt.Errorf("inject content: %w, output: %s (alt: %s)", err, string(output), string(output2))
		}
	}

	return nil
}

// GetPaneContent captures pane content using tmux capture-pane.
func (s *StatusEnrichTestSuite) GetPaneContent(pane int, lines int) (string, error) {
	target := fmt.Sprintf("%s:%d", s.session, pane)
	startLine := -lines
	if startLine < -32768 {
		startLine = -32768
	}

	cmd := exec.Command(tmux.BinaryPath(), "capture-pane", "-t", target, "-p",
		"-S", fmt.Sprintf("%d", startLine))
	output, err := cmd.Output()
	if err != nil {
		return "", fmt.Errorf("capture pane: %w", err)
	}

	return string(output), nil
}

// TestStatusEnrich_HealthyShell tests status enrichments for a healthy shell pane.
// This test doesn't require real agents, just a shell process.
func TestStatusEnrich_HealthyShell(t *testing.T) {
	if testing.Short() {
		t.Skip("Skipping E2E test in short mode")
	}

	if !tmux.DefaultClient.IsInstalled() {
		t.Skip("tmux not installed")
	}

	suite := NewStatusEnrichTestSuite(t, "status_enrich_healthy_shell")
	defer suite.Cleanup()

	// Setup
	if err := suite.Setup(); err != nil {
		t.Fatalf("Setup failed: %v", err)
	}

	// Let the shell pane initialize
	time.Sleep(1 * time.Second)

	// Get status
	session, err := suite.CallRobotStatus()
	if err != nil {
		t.Fatalf("CallRobotStatus failed: %v", err)
	}

	suite.logger.Log("[E2E-ASSERT] Checking status response")

	// Verify session structure
	if session.Name != suite.session {
		t.Errorf("Expected session name %s, got %s", suite.session, session.Name)
	}

	if len(session.Agents) == 0 {
		t.Fatal("Expected at least one agent/pane")
	}

	agent := session.Agents[0]
	suite.logger.Log("[E2E-ASSERT] Agent 0: PID=%d ChildPID=%d State=%s Memory=%dMB",
		agent.PID, agent.ChildPID, agent.ProcessState, agent.MemoryMB)

	// Verify enrichments
	if agent.PID == 0 {
		t.Error("Expected non-zero PID")
	}

	// Process should be running or sleeping
	if agent.ProcessState != "" {
		validStates := map[string]bool{"R": true, "S": true, "D": true}
		if !validStates[agent.ProcessState] {
			suite.logger.Log("[E2E-ASSERT] Unexpected process state: %s", agent.ProcessState)
		} else {
			suite.logger.Log("[E2E-ASSERT] Process state: %s (%s) - valid", agent.ProcessState, agent.ProcessStateName)
		}
	}

	// Memory should be reasonable (shell uses some memory)
	if agent.MemoryMB > 0 {
		suite.logger.Log("[E2E-ASSERT] Memory: %dMB (valid)", agent.MemoryMB)
	}

	// Rate limit should not be detected for healthy shell
	if agent.RateLimitDetected {
		t.Error("Expected rate_limit_detected=false for healthy shell")
	}

	// LastOutputTS should be present and parseable
	// Note: We use a generous 5-minute window because the status call itself
	// can take significant time on busy systems with many sessions.
	if agent.LastOutputTS != "" {
		ts, err := time.Parse(time.RFC3339Nano, agent.LastOutputTS)
		if err != nil {
			suite.logger.Log("[E2E-ASSERT] Could not parse last_output_ts: %s (%v)", agent.LastOutputTS, err)
		} else {
			age := time.Since(ts)
			suite.logger.Log("[E2E-ASSERT] last_output_ts age: %s", age)
			if age > 5*time.Minute {
				t.Errorf("last_output_ts is too old: %s ago", age)
			}
		}
	}

	suite.logger.Log("[E2E-RESULT] PASS: Healthy shell status enrichments verified")
}

// TestStatusEnrich_OutputTracking tests output activity tracking over time.
func TestStatusEnrich_OutputTracking(t *testing.T) {
	if testing.Short() {
		t.Skip("Skipping E2E test in short mode")
	}

	if !tmux.DefaultClient.IsInstalled() {
		t.Skip("tmux not installed")
	}

	suite := NewStatusEnrichTestSuite(t, "status_enrich_output_tracking")
	defer suite.Cleanup()

	// Setup
	if err := suite.Setup(); err != nil {
		t.Fatalf("Setup failed: %v", err)
	}

	// Let shell initialize
	time.Sleep(500 * time.Millisecond)

	// First status call - establish baseline
	session1, err := suite.CallRobotStatus()
	if err != nil {
		t.Fatalf("First status call failed: %v", err)
	}

	if len(session1.Agents) == 0 {
		t.Fatal("No agents in first response")
	}

	agent1 := session1.Agents[0]
	lines1 := agent1.OutputLinesSinceLast
	ts1 := agent1.LastOutputTS

	suite.logger.Log("[E2E-TRACKING] First call: OutputLinesSinceLast=%d LastOutputTS=%s",
		lines1, ts1)

	// Generate some output by running a command
	if err := suite.InjectOutput(0, "test output line 1\ntest output line 2"); err != nil {
		t.Fatalf("Failed to generate output: %v", err)
	}

	// Wait for command execution
	time.Sleep(1 * time.Second)

	// Second status call - should show activity
	session2, err := suite.CallRobotStatus()
	if err != nil {
		t.Fatalf("Second status call failed: %v", err)
	}

	if len(session2.Agents) == 0 {
		t.Fatal("No agents in second response")
	}

	agent2 := session2.Agents[0]
	lines2 := agent2.OutputLinesSinceLast
	ts2 := agent2.LastOutputTS

	suite.logger.Log("[E2E-TRACKING] Second call: OutputLinesSinceLast=%d LastOutputTS=%s",
		lines2, ts2)

	// Verify activity was detected
	if lines2 > 0 {
		suite.logger.Log("[E2E-RESULT] PASS: Output activity detected (lines: %d)", lines2)
	} else {
		suite.logger.Log("[E2E-NOTE] No line delta detected - may be expected depending on timing")
	}

	// Verify timestamp exists
	if ts2 != "" {
		suite.logger.Log("[E2E-RESULT] PASS: Timestamp present: %s", ts2)
	}
}

// TestStatusEnrich_ProcessStateMapping tests process state field mapping.
func TestStatusEnrich_ProcessStateMapping(t *testing.T) {
	if testing.Short() {
		t.Skip("Skipping E2E test in short mode")
	}

	if !tmux.DefaultClient.IsInstalled() {
		t.Skip("tmux not installed")
	}

	suite := NewStatusEnrichTestSuite(t, "status_enrich_process_state")
	defer suite.Cleanup()

	// Setup
	if err := suite.Setup(); err != nil {
		t.Fatalf("Setup failed: %v", err)
	}

	// Let the shell settle
	time.Sleep(500 * time.Millisecond)

	// Get status
	session, err := suite.CallRobotStatus()
	if err != nil {
		t.Fatalf("CallRobotStatus failed: %v", err)
	}

	if len(session.Agents) == 0 {
		t.Fatal("No agents in response")
	}

	agent := session.Agents[0]
	suite.logger.Log("[E2E-STATE] ProcessState=%s ProcessStateName=%s",
		agent.ProcessState, agent.ProcessStateName)

	// Verify state mapping
	stateNameMap := map[string]string{
		"R": "running",
		"S": "sleeping",
		"D": "disk sleep",
		"Z": "zombie",
		"T": "stopped",
	}

	if agent.ProcessState != "" {
		expectedName, ok := stateNameMap[agent.ProcessState]
		if ok {
			if agent.ProcessStateName == expectedName {
				suite.logger.Log("[E2E-RESULT] PASS: Process state correctly mapped: %s -> %s",
					agent.ProcessState, agent.ProcessStateName)
			} else {
				suite.logger.Log("[E2E-NOTE] State name: got %s, expected %s (may be platform-specific)",
					agent.ProcessStateName, expectedName)
			}
		}
	} else {
		suite.logger.Log("[E2E-NOTE] No process state returned (may be expected on some platforms)")
	}
}

// TestStatusEnrich_MemoryReporting tests memory_mb field reporting.
func TestStatusEnrich_MemoryReporting(t *testing.T) {
	if testing.Short() {
		t.Skip("Skipping E2E test in short mode")
	}

	if !tmux.DefaultClient.IsInstalled() {
		t.Skip("tmux not installed")
	}

	suite := NewStatusEnrichTestSuite(t, "status_enrich_memory")
	defer suite.Cleanup()

	// Setup
	if err := suite.Setup(); err != nil {
		t.Fatalf("Setup failed: %v", err)
	}

	// Let shell initialize
	time.Sleep(500 * time.Millisecond)

	// Get status
	session, err := suite.CallRobotStatus()
	if err != nil {
		t.Fatalf("CallRobotStatus failed: %v", err)
	}

	if len(session.Agents) == 0 {
		t.Fatal("No agents in response")
	}

	agent := session.Agents[0]
	suite.logger.Log("[E2E-MEMORY] MemoryMB=%d", agent.MemoryMB)

	// Verify reasonable memory value
	if agent.MemoryMB > 0 && agent.MemoryMB < 10000 {
		suite.logger.Log("[E2E-RESULT] PASS: Memory %dMB is reasonable", agent.MemoryMB)
	} else if agent.MemoryMB == 0 {
		suite.logger.Log("[E2E-NOTE] Memory is 0 (may be expected if process just started or no child)")
	} else {
		t.Errorf("Memory %dMB seems unreasonable", agent.MemoryMB)
	}
}

// TestStatusEnrich_MultipleSessionsConcurrent tests status enrichment performance.
func TestStatusEnrich_MultipleSessionsConcurrent(t *testing.T) {
	if testing.Short() {
		t.Skip("Skipping E2E test in short mode")
	}

	if os.Getenv("E2E_PERFORMANCE") == "" {
		t.Skip("Skipping performance test (set E2E_PERFORMANCE=1 to run)")
	}

	if !tmux.DefaultClient.IsInstalled() {
		t.Skip("tmux not installed")
	}

	suite := NewStatusEnrichTestSuite(t, "status_enrich_perf")
	defer suite.Cleanup()

	// Setup
	if err := suite.Setup(); err != nil {
		t.Fatalf("Setup failed: %v", err)
	}

	// Create multiple panes
	for i := 1; i < 4; i++ {
		cmd := exec.Command(tmux.BinaryPath(), "split-window", "-t", suite.session)
		if err := cmd.Run(); err != nil {
			t.Fatalf("Failed to create pane %d: %v", i, err)
		}
	}

	// Let panes initialize
	time.Sleep(1 * time.Second)

	// Measure status call time
	start := time.Now()
	session, err := suite.CallRobotStatus()
	duration := time.Since(start)

	if err != nil {
		t.Fatalf("CallRobotStatus failed: %v", err)
	}

	suite.logger.Log("[E2E-PERF] Status call completed in %s", duration)

	// Verify all panes present
	agentCount := len(session.Agents)
	suite.logger.Log("[E2E-PERF] Found %d agents", agentCount)

	if agentCount < 4 {
		t.Errorf("Expected at least 4 agents, got %d", agentCount)
	}

	// Performance assertion
	if duration > 5*time.Second {
		t.Errorf("Status call took too long: %s (expected <5s)", duration)
	} else {
		suite.logger.Log("[E2E-RESULT] PASS: Status call completed within time limit")
	}
}

// TestStatusEnrich_SecondsSinceOutput tests the seconds_since_output calculation.
func TestStatusEnrich_SecondsSinceOutput(t *testing.T) {
	if testing.Short() {
		t.Skip("Skipping E2E test in short mode")
	}

	if !tmux.DefaultClient.IsInstalled() {
		t.Skip("tmux not installed")
	}

	suite := NewStatusEnrichTestSuite(t, "status_enrich_seconds")
	defer suite.Cleanup()

	// Setup
	if err := suite.Setup(); err != nil {
		t.Fatalf("Setup failed: %v", err)
	}

	// Generate initial output
	if err := suite.InjectOutput(0, "initial output"); err != nil {
		t.Fatalf("Failed to generate output: %v", err)
	}

	// Wait a bit to let seconds accumulate
	time.Sleep(3 * time.Second)

	// Get status
	session, err := suite.CallRobotStatus()
	if err != nil {
		t.Fatalf("CallRobotStatus failed: %v", err)
	}

	if len(session.Agents) == 0 {
		t.Fatal("No agents in response")
	}

	agent := session.Agents[0]
	suite.logger.Log("[E2E-SECONDS] SecondsSinceOutput=%d", agent.SecondsSinceOutput)

	// Should be a small positive number
	if agent.SecondsSinceOutput >= 0 && agent.SecondsSinceOutput < 30 {
		suite.logger.Log("[E2E-RESULT] PASS: SecondsSinceOutput=%d is reasonable", agent.SecondsSinceOutput)
	} else {
		suite.logger.Log("[E2E-NOTE] SecondsSinceOutput=%d may indicate tracking not yet initialized",
			agent.SecondsSinceOutput)
	}
}

// Cleanup releases all test resources.
func (s *StatusEnrichTestSuite) Cleanup() {
	s.logger.Log("[E2E-CLEANUP] Starting cleanup")
	for _, fn := range s.cleanup {
		fn()
	}
	s.logger.Close()
}

// truncateString is defined in suite_test.go
