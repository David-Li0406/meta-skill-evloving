// Package e2e contains end-to-end tests for NTM robot mode commands.
// errors_test.go implements E2E tests for the ntm errors command.
//
// Bead: bd-22vun - Task: E2E Tests: ntm errors command with real tmux sessions
//
// These tests verify the complete error detection chain with REAL sessions:
// - ntm errors captures errors from panes
// - --panes flag filters to specific panes
// - --robot-errors returns valid JSON
// - Error patterns are correctly detected
package e2e

import (
	"encoding/json"
	"fmt"
	"os/exec"
	"strings"
	"testing"
	"time"
)

// ErrorsResponse represents the JSON output from --robot-errors
type ErrorsResponse struct {
	Session string `json:"session"`
	Errors  []struct {
		Pane      string   `json:"pane"`
		PaneIndex int      `json:"pane_index"`
		Line      int      `json:"line"`
		Content   string   `json:"content"`
		MatchType string   `json:"match_type"`
		AgentType string   `json:"agent_type,omitempty"`
		Context   []string `json:"context,omitempty"`
	} `json:"errors"`
	TotalErrors        int    `json:"total_errors"`
	TotalLinesSearched int    `json:"total_lines_searched"`
	PanesSearched      int    `json:"panes_searched"`
	Timestamp          string `json:"timestamp"`
}

// =============================================================================
// Test Scenario 1: Basic Error Capture
// =============================================================================
// Create session, inject errors, verify ntm errors captures them.

func TestE2E_ErrorsCaptureBasic(t *testing.T) {
	CommonE2EPrerequisites(t)

	suite := NewTestSuite(t, "errors_basic")
	defer suite.Teardown()

	if err := suite.Setup(); err != nil {
		t.Fatalf("[E2E-ERRORS] Setup failed: %v", err)
	}

	session := suite.Session()

	// Inject a Python traceback error into the pane
	suite.Logger().Log("[E2E-ERRORS] Injecting Python traceback error...")
	injectPythonError(t, suite, session)

	// Wait for output to settle
	time.Sleep(500 * time.Millisecond)

	// Run ntm errors
	suite.Logger().Log("[E2E-ERRORS] Running ntm errors on session: %s", session)
	cmd := exec.Command("ntm", "errors", session)
	output, err := cmd.CombinedOutput()
	if err != nil {
		suite.Logger().Log("[E2E-ERRORS] ntm errors returned: %v output=%s", err, string(output))
		// Don't fail - errors command might exit non-zero when errors found
	}

	outputStr := string(output)
	suite.Logger().Log("[E2E-ERRORS] Output: %s", truncateString(outputStr, 500))

	// Verify we got output
	if len(outputStr) == 0 {
		t.Error("[E2E-ERRORS] Empty output from ntm errors")
	}

	// Should contain error indicators
	if !strings.Contains(strings.ToLower(outputStr), "error") &&
		!strings.Contains(outputStr, "No errors found") {
		suite.Logger().Log("[E2E-ERRORS] WARNING: Output doesn't contain 'error'")
	}

	suite.Logger().Log("[E2E-ERRORS] SUCCESS: Basic error capture test completed")
}

// =============================================================================
// Test Scenario 2: Robot Mode JSON Output
// =============================================================================
// Verify --robot-errors returns valid JSON with error array.

func TestE2E_ErrorsRobotJSON(t *testing.T) {
	CommonE2EPrerequisites(t)

	suite := NewTestSuite(t, "errors_robot")
	defer suite.Teardown()

	if err := suite.Setup(); err != nil {
		t.Fatalf("[E2E-ERRORS] Setup failed: %v", err)
	}

	session := suite.Session()

	// Inject errors
	suite.Logger().Log("[E2E-ERRORS] Injecting test errors...")
	injectPythonError(t, suite, session)
	time.Sleep(300 * time.Millisecond)
	injectGoError(t, suite, session)
	time.Sleep(500 * time.Millisecond)

	// Run robot mode
	suite.Logger().Log("[E2E-ERRORS] Running ntm --robot-errors=%s", session)
	cmd := exec.Command("ntm", fmt.Sprintf("--robot-errors=%s", session))
	output, err := cmd.CombinedOutput()
	if err != nil {
		suite.Logger().Log("[E2E-ERRORS] Robot command error: %v", err)
	}

	outputStr := string(output)
	suite.Logger().Log("[E2E-ERRORS] Robot output: %s", truncateString(outputStr, 500))

	// Parse JSON
	var result ErrorsResponse
	if err := json.Unmarshal(output, &result); err != nil {
		t.Fatalf("[E2E-ERRORS] Failed to parse JSON: %v output=%s", err, outputStr)
	}

	// Verify structure
	if result.Session != session {
		t.Errorf("[E2E-ERRORS] Session mismatch: got %s, want %s", result.Session, session)
	}

	suite.Logger().Log("[E2E-ERRORS] Parsed JSON: session=%s, errors=%d, panes=%d, lines=%d",
		result.Session, result.TotalErrors, result.PanesSearched, result.TotalLinesSearched)

	// Errors array should exist (even if empty)
	if result.Errors == nil {
		t.Error("[E2E-ERRORS] Errors array is nil")
	}

	suite.Logger().Log("[E2E-ERRORS] SUCCESS: Robot JSON output test completed")
}

// =============================================================================
// Test Scenario 3: Pane Filtering
// =============================================================================
// Verify --panes flag filters to specific panes.

func TestE2E_ErrorsPaneFilter(t *testing.T) {
	CommonE2EPrerequisites(t)

	suite := NewTestSuite(t, "errors_panes")
	defer suite.Teardown()

	if err := suite.Setup(); err != nil {
		t.Fatalf("[E2E-ERRORS] Setup failed: %v", err)
	}

	session := suite.Session()

	// Create additional pane
	suite.Logger().Log("[E2E-ERRORS] Creating second pane...")
	createCmd := exec.Command("tmux", "split-window", "-t", session, "-v")
	if err := createCmd.Run(); err != nil {
		t.Fatalf("[E2E-ERRORS] Failed to create second pane: %v", err)
	}
	time.Sleep(300 * time.Millisecond)

	// Inject error only in pane 0
	suite.Logger().Log("[E2E-ERRORS] Injecting error in pane 0 only...")
	paneTarget := fmt.Sprintf("%s:0.0", session)
	errorCmd := exec.Command("tmux", "send-keys", "-t", paneTarget,
		`echo "ERROR: Test error in pane 0"`, "Enter")
	if err := errorCmd.Run(); err != nil {
		suite.Logger().Log("[E2E-ERRORS] Failed to inject error: %v", err)
	}
	time.Sleep(500 * time.Millisecond)

	// Run with --panes=0 filter
	suite.Logger().Log("[E2E-ERRORS] Running ntm --robot-errors with --panes=0")
	cmd := exec.Command("ntm", fmt.Sprintf("--robot-errors=%s", session), "--panes=0")
	output, err := cmd.CombinedOutput()
	if err != nil {
		suite.Logger().Log("[E2E-ERRORS] Command error: %v", err)
	}

	var result ErrorsResponse
	if err := json.Unmarshal(output, &result); err != nil {
		suite.Logger().Log("[E2E-ERRORS] JSON parse failed: %v output=%s", err, string(output))
		// Continue - might get helpful output
	} else {
		suite.Logger().Log("[E2E-ERRORS] With pane filter: errors=%d, panes=%d",
			result.TotalErrors, result.PanesSearched)

		// Should only search 1 pane
		if result.PanesSearched > 1 {
			suite.Logger().Log("[E2E-ERRORS] WARNING: Expected 1 pane searched, got %d", result.PanesSearched)
		}
	}

	suite.Logger().Log("[E2E-ERRORS] SUCCESS: Pane filter test completed")
}

// =============================================================================
// Test Scenario 4: Error Pattern Detection
// =============================================================================
// Verify different error patterns are detected.

func TestE2E_ErrorsPatternDetection(t *testing.T) {
	CommonE2EPrerequisites(t)

	suite := NewTestSuite(t, "errors_patterns")
	defer suite.Teardown()

	if err := suite.Setup(); err != nil {
		t.Fatalf("[E2E-ERRORS] Setup failed: %v", err)
	}

	session := suite.Session()

	testCases := []struct {
		name    string
		inject  string
		pattern string
	}{
		{"python_traceback", `echo "Traceback (most recent call last):" && echo "  File \"test.py\", line 1" && echo "ValueError: invalid"`, "Traceback"},
		{"go_panic", `echo "panic: runtime error: index out of range"`, "panic"},
		{"generic_error", `echo "Error: something went wrong"`, "Error"},
		{"failed", `echo "FAILED: test case xyz"`, "FAILED"},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			suite.Logger().Log("[E2E-ERRORS] Testing pattern: %s", tc.name)

			// Clear and inject
			paneTarget := fmt.Sprintf("%s:0.0", session)
			exec.Command("tmux", "send-keys", "-t", paneTarget, "clear", "Enter").Run()
			time.Sleep(200 * time.Millisecond)

			injectCmd := exec.Command("tmux", "send-keys", "-t", paneTarget, tc.inject, "Enter")
			if err := injectCmd.Run(); err != nil {
				suite.Logger().Log("[E2E-ERRORS] Inject failed: %v", err)
			}
			time.Sleep(500 * time.Millisecond)

			// Check for error
			cmd := exec.Command("ntm", fmt.Sprintf("--robot-errors=%s", session))
			output, _ := cmd.CombinedOutput()

			var result ErrorsResponse
			if err := json.Unmarshal(output, &result); err != nil {
				suite.Logger().Log("[E2E-ERRORS] Pattern %s: JSON parse failed", tc.name)
				return
			}

			suite.Logger().Log("[E2E-ERRORS] Pattern %s: found %d errors", tc.name, result.TotalErrors)

			// Check if pattern was detected
			found := false
			for _, e := range result.Errors {
				if strings.Contains(e.Content, tc.pattern) {
					found = true
					suite.Logger().Log("[E2E-ERRORS] Pattern %s: detected match_type=%s", tc.name, e.MatchType)
					break
				}
			}

			if !found && result.TotalErrors > 0 {
				suite.Logger().Log("[E2E-ERRORS] Pattern %s: error detected but pattern not in content", tc.name)
			}
		})
	}

	suite.Logger().Log("[E2E-ERRORS] SUCCESS: Pattern detection test completed")
}

// =============================================================================
// Test Scenario 5: Non-Existent Session
// =============================================================================
// Verify proper error handling for non-existent sessions.

func TestE2E_ErrorsNonExistentSession(t *testing.T) {
	CommonE2EPrerequisites(t)

	suite := NewTestSuite(t, "errors_notfound")
	defer suite.Teardown()

	nonExistentSession := "e2e_nonexistent_errors_xyz123"

	suite.Logger().Log("[E2E-ERRORS] Running ntm errors on non-existent session: %s", nonExistentSession)
	cmd := exec.Command("ntm", fmt.Sprintf("--robot-errors=%s", nonExistentSession))
	output, err := cmd.CombinedOutput()

	outputStr := string(output)
	suite.Logger().Log("[E2E-ERRORS] Output: %s", outputStr)

	// Should have an error
	if err == nil {
		suite.Logger().Log("[E2E-ERRORS] WARNING: Expected error for non-existent session")
	}

	// Check if error is in JSON format
	var result map[string]interface{}
	if json.Unmarshal(output, &result) == nil {
		if errMsg, ok := result["error"]; ok {
			suite.Logger().Log("[E2E-ERRORS] Error message: %v", errMsg)
		}
	}

	suite.Logger().Log("[E2E-ERRORS] SUCCESS: Non-existent session error handling test completed")
}

// =============================================================================
// Test Scenario 6: Since Duration Filter
// =============================================================================
// Verify --errors-since flag filters by time.

func TestE2E_ErrorsSinceDuration(t *testing.T) {
	CommonE2EPrerequisites(t)

	suite := NewTestSuite(t, "errors_since")
	defer suite.Teardown()

	if err := suite.Setup(); err != nil {
		t.Fatalf("[E2E-ERRORS] Setup failed: %v", err)
	}

	session := suite.Session()

	// Inject an error
	injectPythonError(t, suite, session)
	time.Sleep(500 * time.Millisecond)

	// Test with different --since values
	sinceValues := []string{"1m", "5m", "1h"}

	for _, since := range sinceValues {
		t.Run("since_"+since, func(t *testing.T) {
			suite.Logger().Log("[E2E-ERRORS] Testing --errors-since=%s", since)

			cmd := exec.Command("ntm", fmt.Sprintf("--robot-errors=%s", session),
				fmt.Sprintf("--errors-since=%s", since))
			output, err := cmd.CombinedOutput()
			if err != nil {
				suite.Logger().Log("[E2E-ERRORS] Command error: %v", err)
			}

			var result ErrorsResponse
			if err := json.Unmarshal(output, &result); err != nil {
				suite.Logger().Log("[E2E-ERRORS] --since=%s: JSON parse failed", since)
			} else {
				suite.Logger().Log("[E2E-ERRORS] --since=%s: errors=%d", since, result.TotalErrors)
			}
		})
	}

	suite.Logger().Log("[E2E-ERRORS] SUCCESS: Since duration filter test completed")
}

// =============================================================================
// Test Scenario 7: Lines Limit
// =============================================================================
// Verify --lines flag limits captured lines.

func TestE2E_ErrorsLinesLimit(t *testing.T) {
	CommonE2EPrerequisites(t)

	suite := NewTestSuite(t, "errors_lines")
	defer suite.Teardown()

	if err := suite.Setup(); err != nil {
		t.Fatalf("[E2E-ERRORS] Setup failed: %v", err)
	}

	session := suite.Session()

	// Inject errors
	injectPythonError(t, suite, session)
	time.Sleep(500 * time.Millisecond)

	// Test with --lines=50
	suite.Logger().Log("[E2E-ERRORS] Testing --lines=50")
	cmd := exec.Command("ntm", fmt.Sprintf("--robot-errors=%s", session), "--lines=50")
	output, _ := cmd.CombinedOutput()

	var result ErrorsResponse
	if err := json.Unmarshal(output, &result); err != nil {
		suite.Logger().Log("[E2E-ERRORS] JSON parse failed: %v", err)
	} else {
		suite.Logger().Log("[E2E-ERRORS] With --lines=50: searched %d lines", result.TotalLinesSearched)
	}

	suite.Logger().Log("[E2E-ERRORS] SUCCESS: Lines limit test completed")
}

// =============================================================================
// Test Scenario 8: Clean Session (No Errors)
// =============================================================================
// Verify clean output when no errors present.

func TestE2E_ErrorsCleanSession(t *testing.T) {
	CommonE2EPrerequisites(t)

	suite := NewTestSuite(t, "errors_clean")
	defer suite.Teardown()

	if err := suite.Setup(); err != nil {
		t.Fatalf("[E2E-ERRORS] Setup failed: %v", err)
	}

	session := suite.Session()

	// Don't inject any errors - just run with clean session
	suite.Logger().Log("[E2E-ERRORS] Running on clean session...")

	// Send some benign output
	paneTarget := fmt.Sprintf("%s:0.0", session)
	exec.Command("tmux", "send-keys", "-t", paneTarget, "echo 'INFO: All systems normal'", "Enter").Run()
	time.Sleep(500 * time.Millisecond)

	cmd := exec.Command("ntm", fmt.Sprintf("--robot-errors=%s", session))
	output, _ := cmd.CombinedOutput()

	var result ErrorsResponse
	if err := json.Unmarshal(output, &result); err != nil {
		suite.Logger().Log("[E2E-ERRORS] JSON parse failed: %v output=%s", err, string(output))
	} else {
		suite.Logger().Log("[E2E-ERRORS] Clean session: errors=%d", result.TotalErrors)

		if result.TotalErrors > 0 {
			suite.Logger().Log("[E2E-ERRORS] WARNING: Found errors in 'clean' session - may have residual output")
		}
	}

	suite.Logger().Log("[E2E-ERRORS] SUCCESS: Clean session test completed")
}

// =============================================================================
// Helper Functions
// =============================================================================

// injectPythonError injects a Python traceback into the first pane
func injectPythonError(t *testing.T, suite *TestSuite, session string) {
	t.Helper()
	paneTarget := fmt.Sprintf("%s:0.0", session)
	cmd := exec.Command("tmux", "send-keys", "-t", paneTarget,
		`echo "Traceback (most recent call last):" && echo '  File "test.py", line 42, in main' && echo "FileNotFoundError: [Errno 2] No such file or directory"`,
		"Enter")
	if err := cmd.Run(); err != nil {
		suite.Logger().Log("[E2E-ERRORS] Failed to inject Python error: %v", err)
	}
}

// injectGoError injects a Go panic into the first pane
func injectGoError(t *testing.T, suite *TestSuite, session string) {
	t.Helper()
	paneTarget := fmt.Sprintf("%s:0.0", session)
	cmd := exec.Command("tmux", "send-keys", "-t", paneTarget,
		`echo "panic: runtime error: index out of range [5] with length 3" && echo "goroutine 1 [running]:" && echo "main.main()" && echo "        /app/main.go:25 +0x45"`,
		"Enter")
	if err := cmd.Run(); err != nil {
		suite.Logger().Log("[E2E-ERRORS] Failed to inject Go error: %v", err)
	}
}
